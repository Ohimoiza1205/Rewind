import logging
from typing import Optional, Dict
from app.services.twelvelabs_service import analyze_video_complete
from app.services.gemini_service import generate_scene_description
from app.services.elevenlabs_service import generate_narration
from app.services.firebase_service import firebase_service

logger = logging.getLogger(__name__)


def process_video_ai(video_id: str, video_path: str) -> Optional[Dict]:
    """
    Process video through complete AI pipeline
    
    1. Analyze with TwelveLabs (real API)
    2. Generate descriptions with Gemini
    3. Create voice narration with ElevenLabs
    
    Args:
        video_id: Unique video identifier
        video_path: Path to video file
    
    Returns:
        Dictionary with scenes and narrations
    """
    try:
        logger.info(f"Starting AI pipeline for video: {video_id}")
        
        # Step 1: TwelveLabs analysis
        logger.info("Uploading to TwelveLabs and analyzing...")
        twelvelabs_result = analyze_video_complete(video_path)
        
        scenes = twelvelabs_result.get("scenes", [])
        logger.info(f"TwelveLabs found {len(scenes)} scenes")
        
        # Step 2 & 3: Enhance each scene with Gemini + ElevenLabs
        enriched_scenes = []
        
        for scene in scenes:
            logger.info(f"Processing scene at {scene['timestamp']}")
            
            # Generate description with Gemini
            description = generate_scene_description(scene)
            
            # Generate narration with ElevenLabs
            audio_url = generate_narration(description)
            
            enriched_scenes.append({
                "timestamp": scene["timestamp"],
                "objects": scene.get("objects", []),
                "people": scene.get("people", []),
                "transcript": scene.get("transcript", ""),
                "description": description,
                "audio_url": audio_url
            })
            
            logger.info(f"Scene at {scene['timestamp']} processed successfully")
        
        result = {
            "video_id": video_id,
            "twelvelabs_video_id": twelvelabs_result["video_id"],
            "status": "complete",
            "scenes": enriched_scenes,
            "total_scenes": len(enriched_scenes)
        }
        
        # Save to Firebase (will use mock mode if enabled)
        try:
            firebase_service.save_video_analysis(video_id, video_id, result)
        except Exception as e:
            logger.warning(f"Could not save to Firebase: {str(e)}")
        
        logger.info(f"AI pipeline complete for {video_id}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in AI pipeline: {str(e)}")
        return None