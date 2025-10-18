# Depth Processing - REWIND

Monocular depth estimation pipeline for converting 2D video frames into navigable 3D spaces.

## Overview

Processes video frames through MiDaS and DPT models to generate depth maps and point clouds for 3D visualization.

## Key Technologies

- **MiDaS v3.1**: Monocular depth estimation
- **DPT**: Dense Prediction Transformers
- **PyTorch**: Deep learning framework
- **Open3D**: 3D data processing
- **OpenCV**: Computer vision operations

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Download MiDaS models
python scripts/setup_midas.py

# Process a video
python scripts/generate_depth_maps.py --input video.mp4 --output output/
```

## Project Structure

```
depth-processing/
├── models/              # Pre-trained model weights
├── scripts/             # Processing scripts
├── src/                 # Core depth estimation
├── output/              # Generated artifacts
│   ├── frames/         # Extracted frames
│   ├── depth_maps/     # Depth predictions
│   └── pointclouds/    # 3D point clouds
└── test_videos/        # Sample videos
```

## Core Scripts

### `setup_midas.py`
Downloads pre-trained MiDaS and DPT model weights.

### `extract_frames.py`
Extracts video frames at specified FPS using FFmpeg.

### `generate_depth_maps.py`
Generates depth maps from extracted frames using MiDaS/DPT.

### `depth_to_pointcloud.py`
Converts depth maps to 3D point clouds using Open3D.

### `batch_process.py`
Processes multiple videos in parallel.

## Usage

### Process Single Video

```bash
python scripts/generate_depth_maps.py \
  --input path/to/video.mp4 \
  --output output/ \
  --model dpt_hybrid \
  --fps 2
```

### Batch Processing

```bash
python scripts/batch_process.py \
  --input-dir test_videos/ \
  --output-dir output/ \
  --workers 4
```

### GPU Acceleration

```bash
# Enable CUDA if available
python scripts/generate_depth_maps.py \
  --input video.mp4 \
  --output output/ \
  --device cuda
```

## Model Selection

### MiDaS Small
- Fastest inference
- Lower accuracy
- Best for real-time processing

### MiDaS Large
- Balanced speed/accuracy
- Recommended for most use cases

### DPT Hybrid
- Highest accuracy
- Slower inference
- Best for final production

## Output Formats

### Depth Maps
- Format: PNG (16-bit grayscale)
- Resolution: Same as input frame
- Normalized: 0-65535 range

### Point Clouds
- Format: PLY (binary)
- Coordinates: (x, y, z)
- Colors: RGB from original frame

## Performance Optimization

### GPU Acceleration
CUDA support provides ~10x speedup over CPU.

### Frame Sampling
Process every 2nd frame (2 FPS) to reduce computation while maintaining quality.

### Batch Processing
Process multiple frames simultaneously to maximize GPU utilization.

### Model Caching
Models loaded once and reused across frames.

## Requirements

- Python 3.10+
- CUDA 11.8+ (optional, for GPU)
- FFmpeg 6.0+
- 8GB+ RAM (16GB recommended)
- GPU with 4GB+ VRAM (optional)

## Troubleshooting

**CUDA out of memory**: Reduce batch size or use smaller model

**Slow processing**: Enable GPU or reduce frame rate

**Poor depth quality**: Use DPT-Hybrid model or higher resolution input

**FFmpeg errors**: Ensure FFmpeg is installed and in PATH

## Advanced Configuration

Edit `src/depth_estimator.py` for custom settings:

```python
DEPTH_CONFIG = {
    'model_type': 'dpt_hybrid',
    'optimize': True,
    'height': 384,
    'square': False
}
```

## Contributing

See main repository [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for guidelines.

## Team

Depth processing developed by **Peace Enesi** - [GitHub](https://github.com/AhuoyizaEnesi) | [LinkedIn](https://www.linkedin.com/in/peace-enesi/)