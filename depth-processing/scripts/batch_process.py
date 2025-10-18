import argparse
from pathlib import Path
import json
import sys
import time
import logging

sys.path.append(str(Path(__file__).parent.parent / "src"))

from extract_frames import extract_frames, extract_audio, get_video_metadata
from generate_depth_maps import generate_depth_maps
from pointcloud_generator import process_frame_to_pointcloud

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VideoPipeline:
    """
    Complete end-to-end pipeline for video to 3D point cloud conversion
    """
    
    def __init__(self, output_base="output"):
        self.output_base = Path(output_base)
        self.output_base.mkdir(parents=True, exist_ok=True)
        self.stats = {
            'start_time': None,
            'end_time': None,
            'stages': {}
        }
    
    def process_video(self, video_path, fps=2, model_type="DPT_Large", 
                     downsample=2, include_mesh=True, extract_audio_track=True):
        """
        Complete pipeline: video -> frames -> depth -> point clouds
        
        Args:
            video_path: Path to input video
            fps: Frames per second to extract
            model_type: MiDaS model type
            downsample: Point cloud downsampling factor
            include_mesh: Generate mesh data
            extract_audio_track: Extract audio for narration
            
        Returns:
            Complete pipeline metadata
        """
        self.stats['start_time'] = time.time()
        
        video_path = Path(video_path)
        video_name = video_path.stem
        
        logger.info("="*70)
        logger.info("REWIND - Video to 3D Point Cloud Pipeline")
        logger.info("="*70)
        logger.info(f"Processing: {video_path.name}")
        
        frames_dir = self.output_base / "frames" / video_name
        depth_dir = self.output_base / "depth_maps" / video_name
        pointcloud_dir = self.output_base / "pointclouds" / video_name
        audio_dir = self.output_base / "audio"
        
        logger.info("\n[Stage 1/4] Extracting video metadata")
        stage_start = time.time()
        video_metadata = get_video_metadata(video_path)
        self.stats['stages']['metadata'] = time.time() - stage_start
        
        logger.info("\n[Stage 2/4] Extracting frames")
        stage_start = time.time()
        frame_files = extract_frames(video_path, frames_dir, fps=fps, quality=2)
        self.stats['stages']['frames'] = time.time() - stage_start
        
        if not frame_files:
            logger.error("Frame extraction failed. Aborting pipeline.")
            return None
        
        if extract_audio_track:
            audio_path = audio_dir / f"{video_name}.mp3"
            extract_audio(video_path, audio_path)
        
        logger.info("\n[Stage 3/4] Generating depth maps")
        stage_start = time.time()
        depth_metadata = generate_depth_maps(
            frames_dir, 
            depth_dir, 
            model_type=model_type,
            save_visualization=True
        )
        self.stats['stages']['depth'] = time.time() - stage_start
        
        if not depth_metadata:
            logger.error("Depth map generation failed. Aborting pipeline.")
            return None
        
        logger.info("\n[Stage 4/4] Creating 3D point clouds")
        stage_start = time.time()
        
        pointcloud_dir.mkdir(parents=True, exist_ok=True)
        
        depth_files = sorted(depth_dir.glob("*_depth.png"))
        
        pointcloud_metadata = {
            "video_name": video_name,
            "video_metadata": video_metadata,
            "pipeline_settings": {
                "extraction_fps": fps,
                "model_type": model_type,
                "downsample_factor": downsample,
                "includes_mesh": include_mesh
            },
            "pointclouds": []
        }
        
        for i, (frame_path, depth_path) in enumerate(zip(frame_files, depth_files)):
            logger.info(f"Processing point cloud {i+1}/{len(frame_files)}")
            
            try:
                pointcloud_data, json_path = process_frame_to_pointcloud(
                    frame_path,
                    depth_path,
                    pointcloud_dir,
                    downsample=downsample,
                    include_mesh=include_mesh
                )
                
                pointcloud_metadata["pointclouds"].append({
                    "index": i,
                    "timestamp": i / fps,
                    "frame": frame_path.name,
                    "depth_map": depth_path.name,
                    "pointcloud": json_path.name,
                    "point_count": pointcloud_data['count'],
                    "bounds": pointcloud_data['bounds']
                })
                
            except Exception as e:
                logger.error(f"Failed to create point cloud {i}: {e}")
                continue
        
        self.stats['stages']['pointclouds'] = time.time() - stage_start
        
        pipeline_metadata_path = pointcloud_dir / "pipeline_metadata.json"
        with open(pipeline_metadata_path, 'w') as f:
            json.dump(pointcloud_metadata, f, indent=2)
        
        self.stats['end_time'] = time.time()
        self.stats['total_time'] = self.stats['end_time'] - self.stats['start_time']
        
        self._print_summary(pointcloud_metadata)
        
        return pointcloud_metadata
    
    def _print_summary(self, metadata):
        """Print pipeline execution summary"""
        logger.info("\n" + "="*70)
        logger.info("PIPELINE COMPLETE")
        logger.info("="*70)
        
        logger.info(f"\nVideo: {metadata['video_name']}")
        logger.info(f"Total frames processed: {len(metadata['pointclouds'])}")
        
        total_points = sum(pc['point_count'] for pc in metadata['pointclouds'])
        avg_points = total_points / len(metadata['pointclouds']) if metadata['pointclouds'] else 0
        
        logger.info(f"Total points generated: {total_points:,}")
        logger.info(f"Average points per frame: {avg_points:,.0f}")
        
        logger.info("\nProcessing times:")
        logger.info(f"  Metadata extraction: {self.stats['stages'].get('metadata', 0):.2f}s")
        logger.info(f"  Frame extraction: {self.stats['stages'].get('frames', 0):.2f}s")
        logger.info(f"  Depth map generation: {self.stats['stages'].get('depth', 0):.2f}s")
        logger.info(f"  Point cloud creation: {self.stats['stages'].get('pointclouds', 0):.2f}s")
        logger.info(f"  Total pipeline time: {self.stats['total_time']:.2f}s")
        
        logger.info("\nOutput locations:")
        logger.info(f"  Frames: {self.output_base}/frames/{metadata['video_name']}")
        logger.info(f"  Depth maps: {self.output_base}/depth_maps/{metadata['video_name']}")
        logger.info(f"  Point clouds: {self.output_base}/pointclouds/{metadata['video_name']}")
        
        logger.info("\nReady for Three.js integration!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Complete video processing pipeline for Rewind',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'video',
        type=str,
        help='Path to input video file'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=2,
        help='Frames per second to extract (default: 2)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='output',
        help='Base output directory (default: output)'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='DPT_Large',
        choices=['DPT_Large', 'DPT_Hybrid', 'MiDaS_small'],
        help='MiDaS model type (default: DPT_Large for best quality)'
    )
    parser.add_argument(
        '--downsample',
        type=int,
        default=2,
        help='Point cloud downsampling factor (default: 2)'
    )
    parser.add_argument(
        '--no-mesh',
        action='store_true',
        help='Skip mesh generation'
    )
    parser.add_argument(
        '--no-audio',
        action='store_true',
        help='Skip audio extraction'
    )
    
    args = parser.parse_args()
    
    video_path = Path(args.video)
    
    if not video_path.exists():
        logger.error(f"Video file not found: {video_path}")
        sys.exit(1)
    
    pipeline = VideoPipeline(output_base=args.output)
    
    try:
        metadata = pipeline.process_video(
            video_path,
            fps=args.fps,
            model_type=args.model,
            downsample=args.downsample,
            include_mesh=not args.no_mesh,
            extract_audio_track=not args.no_audio
        )
        
        if metadata:
            logger.info("\nPipeline executed successfully!")
            sys.exit(0)
        else:
            logger.error("\nPipeline failed!")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Pipeline error: {e}", exc_info=True)
        sys.exit(1)