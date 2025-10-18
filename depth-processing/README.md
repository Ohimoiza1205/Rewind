# Depth Processing Module

High-quality video to 3D point cloud conversion pipeline for Rewind project.

## Overview

This module handles the complete pipeline from video input to Three.js-ready 3D point clouds:
1. Frame extraction from video
2. Depth map generation using MiDaS
3. Point cloud creation optimized for web rendering
4. Mesh generation for smooth visualization

## Installation

```bash
cd depth-processing
pip install -r requirements.txt
```

## Quick Start

Process a complete video in one command:

```bash
python scripts/batch_process.py path/to/video.mp4 --fps 2 --output output
```

## Pipeline Stages

### Stage 1: Frame Extraction

```bash
python scripts/extract_frames.py video.mp4 --fps 2 --output output/frames --audio
```

Options:
- `--fps`: Frames per second to extract (default: 2)
- `--audio`: Also extract audio track
- `--quality`: JPEG quality, 1-31 (default: 2, very high)

### Stage 2: Depth Map Generation

```bash
python scripts/generate_depth_maps.py output/frames --output output/depth_maps --model DPT_Large
```

Options:
- `--model`: Model type (DPT_Large, DPT_Hybrid, MiDaS_small)
- `--no-viz`: Skip colored visualizations
- `--create-video`: Create video from depth visualizations

### Stage 3: Point Cloud Generation

```bash
python scripts/depth_to_pointcloud.py output/frames output/depth_maps --output output/pointclouds
```

Options:
- `--focal-length`: Camera focal length in pixels (default: 525.0)
- `--downsample`: Downsampling factor for performance (default: 2)
- `--no-mesh`: Skip mesh generation
- `--analyze`: Analyze point cloud quality

## Module Structure

```
depth-processing/
├── src/
│   ├── depth_estimator.py       # MiDaS depth estimation
│   ├── pointcloud_generator.py  # Point cloud creation
│   └── depth_optimizer.py       # Quality optimization
├── scripts/
│   ├── extract_frames.py        # Video to frames
│   ├── generate_depth_maps.py   # Frames to depth
│   ├── depth_to_pointcloud.py   # Depth to 3D
│   └── batch_process.py         # Complete pipeline
├── output/
│   ├── frames/                  # Extracted frames
│   ├── depth_maps/              # Depth maps
│   └── pointclouds/             # 3D data (JSON)
└── test_videos/                 # Sample videos
```

## Output Format

Point clouds are exported as JSON files optimized for Three.js:

```json
{
  "type": "Mesh",
  "points": [[x, y, z], ...],
  "colors": [[r, g, b], ...],
  "mesh": {
    "vertices": [[x, y, z], ...],
    "faces": [[i1, i2, i3], ...],
    "colors": [[r, g, b], ...]
  },
  "metadata": {
    "count": 50000,
    "bounds": {
      "min": [-5, -5, -10],
      "max": [5, 5, 0]
    }
  }
}
```

## Quality Settings

### High Quality (Demo/Production)
```bash
python scripts/batch_process.py video.mp4 \
  --fps 2 \
  --model DPT_Large \
  --downsample 1
```

### Balanced (Development)
```bash
python scripts/batch_process.py video.mp4 \
  --fps 2 \
  --model DPT_Hybrid \
  --downsample 2
```

### Fast (Testing)
```bash
python scripts/batch_process.py video.mp4 \
  --fps 1 \
  --model MiDaS_small \
  --downsample 4
```

## Performance

Typical processing times (30-second video, 1920x1080):
- Frame extraction: ~5 seconds
- Depth generation (DPT_Large): ~30 seconds (GPU) / ~3 minutes (CPU)
- Point cloud creation: ~10 seconds

Total: ~45 seconds with GPU, ~3.5 minutes with CPU

## Integration with Frontend

Point cloud JSON files can be loaded directly in Three.js:

```javascript
// Load point cloud
const response = await fetch('output/pointclouds/video_name/frame_0000.json');
const data = await response.json();

// Create geometry
const geometry = new THREE.BufferGeometry();
geometry.setAttribute('position', new THREE.Float32BufferAttribute(data.points.flat(), 3));
geometry.setAttribute('color', new THREE.Float32BufferAttribute(data.colors.flat(), 3));

// Create point cloud
const material = new THREE.PointsMaterial({ size: 0.01, vertexColors: true });
const pointCloud = new THREE.Points(geometry, material);
scene.add(pointCloud);
```

## Troubleshooting

### Issue: FFmpeg not found
```bash
# Windows
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

### Issue: CUDA out of memory
Use smaller model or reduce resolution:
```bash
python scripts/batch_process.py video.mp4 --model MiDaS_small
```

### Issue: Point clouds too large
Increase downsampling:
```bash
python scripts/batch_process.py video.mp4 --downsample 4
```

## Advanced Usage

### Temporal Smoothing
For videos with camera motion, apply temporal smoothing to reduce jitter.

### Custom Focal Length
Calculate focal length from camera specs:
```
focal_length_px = (focal_length_mm / sensor_width_mm) * image_width_px
```

### Batch Processing Multiple Videos
```bash
for video in videos/*.mp4; do
  python scripts/batch_process.py "$video" --output output
done
```