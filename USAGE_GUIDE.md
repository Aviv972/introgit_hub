# Vision Agent Usage Guide

This comprehensive guide provides detailed instructions for setting up and using the Landing AI Vision Agent library for computer vision tasks.

## Table of Contents

- [Quick Start](#quick-start)
- [API Keys Setup](#api-keys-setup)
- [Running Examples](#running-examples)
- [Expected Outputs](#expected-outputs)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)
- [FAQ](#faq)

## Quick Start

### 1. Verify Installation

First, run the comprehensive test suite to check your installation:

```bash
python3 test_vision_agent.py
```

This will show you:
- ✅ What's working correctly
- ❌ What needs to be configured
- 🎯 Next steps to take

### 2. Set Up API Keys (Required)

Vision Agent requires API keys from three providers. Follow the [API Keys Setup](#api-keys-setup) section below.

### 3. Run Your First Example

Once API keys are configured:

```bash
cd quickstart
python3 source.py
```

## API Keys Setup

Vision Agent requires API keys from three providers to function properly.

### 🔑 Vision Agent API Key

**Purpose**: Access to Vision Agent's code generation capabilities

1. **Create Account**: Go to https://va.landing.ai/home
2. **Sign Up**: Create a free account with your email
3. **Get API Key**: Navigate to https://va.landing.ai/settings/api-key
4. **Copy Key**: Copy your API key (starts with `va_`)

### 🔑 Anthropic API Key

**Purpose**: Powers Claude 3.7 Sonnet model for planning and code generation

1. **Create Account**: Go to https://console.anthropic.com/
2. **Sign Up**: Create an account (requires phone verification)
3. **Get API Key**: Go to https://console.anthropic.com/settings/keys
4. **Generate Key**: Click "Create Key" and copy it (starts with `sk-ant-`)

**Free Tier**: $5 in free credits for new accounts

### 🔑 Google API Key

**Purpose**: Powers Gemini Flash 2.0 Experimental model

1. **Create Account**: Go to https://aistudio.google.com/
2. **Sign In**: Use your Google account
3. **Get API Key**: Go to https://aistudio.google.com/app/apikey
4. **Create Key**: Click "Create API Key" and copy it

**Free Tier**: Generous free usage limits

### 🔧 Configure Environment Variables

#### Method 1: Using .env File (Recommended)

1. **Edit the .env file**:
   ```bash
   nano .env
   ```

2. **Uncomment and replace the placeholder values**:
   ```bash
   # Remove the # and replace with your actual keys
   VISION_AGENT_API_KEY=va_your_actual_vision_agent_key_here
   ANTHROPIC_API_KEY=sk-ant-your_actual_anthropic_key_here
   GOOGLE_API_KEY=your_actual_google_key_here
   ```

3. **Load environment variables**:
   ```bash
   export $(cat .env | grep -v '^#' | xargs)
   ```

#### Method 2: Direct Export (Temporary)

```bash
export VISION_AGENT_API_KEY="va_your_key_here"
export ANTHROPIC_API_KEY="sk-ant-your_key_here"
export GOOGLE_API_KEY="your_key_here"
```

#### Method 3: System-wide (Permanent)

Add to your `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export VISION_AGENT_API_KEY="va_your_key_here"' >> ~/.bashrc
echo 'export ANTHROPIC_API_KEY="sk-ant-your_key_here"' >> ~/.bashrc
echo 'export GOOGLE_API_KEY="your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### ✅ Verify API Keys

Run the test script to verify your API keys are properly configured:

```bash
python3 test_vision_agent.py
```

Look for:
```
✅ VISION_AGENT_API_KEY: Set (length: XX)
✅ ANTHROPIC_API_KEY: Set (length: XX)
✅ GOOGLE_API_KEY: Set (length: XX)
```

## Running Examples

### 📝 Basic VisionAgent Prompt Script

**File**: `quickstart/source.py`
**Purpose**: Generate code from natural language prompts and images

```bash
cd quickstart
python3 source.py
```

**What it does**:
1. Checks API keys and sample images
2. Uses VisionAgentCoderV2 to analyze an image
3. Generates Python code for image description
4. Saves the generated code to `generated_code.py`

**Example prompt**: "Describe the image"

### 🔧 Direct Tools Usage Script

**File**: `quickstart/test_tools.py`
**Purpose**: Use Vision Agent tools directly for object detection

```bash
cd quickstart
python3 test_tools.py
```

**What it does**:
1. Tests vision_agent.tools import
2. Loads sample images
3. Runs object detection (or mock demonstration)
4. Creates visualizations with bounding boxes
5. Saves results as PNG files

### 🧪 Comprehensive Test Runner

**File**: `test_vision_agent.py`
**Purpose**: Test installation and configuration

```bash
python3 test_vision_agent.py
```

**What it does**:
1. Tests all imports and dependencies
2. Checks API key configuration
3. Runs mock functionality tests
4. Generates comprehensive report
5. Saves results to JSON file

## Expected Outputs

### ✅ Successful source.py Run

```
🎯 VisionAgent Basic Prompt Script
========================================

1️⃣  Checking API Keys...
✅ All required API keys are set

2️⃣  Checking Sample Images...
✅ Found sample image: people.jpg

3️⃣  Running VisionAgent Example...
📝 Initializing VisionAgentCoderV2...
🖼️  Processing image: people.jpg
💭 Prompt: 'Describe the image'

⏳ Generating code... (this may take a while)
✅ Code generation completed!
📄 Generated code saved to: generated_code.py
📊 Code length: 1234 characters
🧪 Test length: 567 characters

📋 Generated Code Preview:
------------------------------
 1: import vision_agent.tools as T
 2: import matplotlib.pyplot as plt
 3: 
 4: # Load the image
 5: image = T.load_image("people.jpg")
 6: ...

🎉 VisionAgent example completed successfully!
📁 Check the generated_code.py file for the results.
```

### ✅ Successful test_tools.py Run

```
🔧 VisionAgent Direct Tools Usage Demo
==================================================
🔍 Checking dependencies...
✅ matplotlib: 3.10.3
✅ numpy: 2.2.6
✅ PIL/Pillow: 11.2.1

🔧 Testing vision_agent.tools import...
✅ vision_agent.tools imported successfully
✅ load_image: Available
✅ countgd_object_detection: Available
✅ overlay_bounding_boxes: Available
✅ save_image: Available

🖼️  Looking for sample images...
✅ Found: people.jpg
✅ Found: landscape.jpg

🎯 Running object detection demo on: people.jpg
============================================================
🔧 Attempting to use vision_agent.tools...
📂 Loading image...
✅ Image loaded successfully
🔍 Running object detection...
✅ Detection completed: 3 objects found
🎨 Creating visualization with vision_agent tools...
✅ Vision Agent visualization saved to: people_detected_va.png

📊 Detection Summary:
   - Image: people.jpg
   - Objects detected: 3
   - Visualization: detection_results_people.png
   - Detection 1: person (confidence: 0.95) at [120, 45, 280, 420]
   - Detection 2: person (confidence: 0.87) at [300, 60, 450, 380]
   - Detection 3: person (confidence: 0.82) at [480, 80, 620, 400]

==================================================
📋 DEMO SUMMARY
==================================================
✅ Successfully processed 2 image(s)
📁 Check the generated PNG files for visualization results
🔧 VisionAgent tools were used for detection
```

### ✅ Generated Files

After running the examples, you should see these files:

```
/home/daytona/introgit_hub/
├── quickstart/
│   ├── generated_code.py          # Generated by source.py
│   ├── people_detected_va.png     # Generated by test_tools.py (if tools work)
│   └── detection_results_*.png    # Visualization files
├── vision_agent_test_results.json # Test results from test_vision_agent.py
└── ...
```

## Troubleshooting

### 🔑 API Key Issues

#### Problem: "Missing required API keys"
```
❌ Missing required API keys:
   - VISION_AGENT_API_KEY
   - ANTHROPIC_API_KEY
   - GOOGLE_API_KEY
```

**Solutions**:
1. **Check .env file**: Ensure keys are uncommented (no `#` at start)
2. **Load environment**: Run `export $(cat .env | grep -v '^#' | xargs)`
3. **Verify keys**: Run `echo $VISION_AGENT_API_KEY` to check if set
4. **Check format**: Ensure no extra spaces or quotes

#### Problem: "Authentication failed" or "Invalid API key"
**Solutions**:
1. **Verify key format**:
   - Vision Agent: starts with `va_`
   - Anthropic: starts with `sk-ant-`
   - Google: alphanumeric string
2. **Check key validity**: Log into provider dashboards to verify keys
3. **Regenerate keys**: Create new keys if old ones are invalid
4. **Check account status**: Ensure accounts are active and have credits

#### Problem: "Rate limit exceeded"
**Solutions**:
1. **Wait**: Rate limits reset after time (usually 1 minute to 1 hour)
2. **Upgrade plan**: Consider paid tiers for higher limits
3. **Reduce requests**: Use smaller images or fewer API calls

### 🖥️ System and Installation Issues

#### Problem: "libGL.so.1: cannot open shared object file"
```
❌ Failed to import vision_agent: libGL.so.1: cannot open shared object file: No such file or directory
```

**Solutions**:
1. **Expected in headless environments**: This is normal in Docker/cloud environments
2. **Use mock mode**: Scripts will fall back to mock demonstrations
3. **Install OpenGL** (if you have admin access):
   ```bash
   sudo apt-get update
   sudo apt-get install libgl1-mesa-glx libglib2.0-0
   ```
4. **Use alternative backend**: Scripts automatically set `matplotlib.use('Agg')`

#### Problem: "No module named 'vision_agent'"
**Solutions**:
1. **Reinstall**: `pip install --force-reinstall vision-agent`
2. **Check Python environment**: Ensure you're using the right Python/pip
3. **Install dependencies**: `pip install --no-deps vision-agent` then install deps manually
4. **Virtual environment**: Consider using a clean virtual environment

#### Problem: Import errors for specific modules
**Solutions**:
1. **Install missing packages**:
   ```bash
   pip install matplotlib numpy pillow requests anthropic google-generativeai
   ```
2. **Update packages**: `pip install --upgrade vision-agent`
3. **Check compatibility**: Ensure Python 3.9+ is being used

### 🖼️ Image and File Issues

#### Problem: "No sample images found"
**Solutions**:
1. **Check directory**: Ensure you're in the right directory
2. **Re-download images**: Run the download script again
3. **Manual download**: Download any `.jpg` or `.png` images to `quickstart/`
4. **Check permissions**: Ensure files are readable

#### Problem: "Permission denied" when saving files
**Solutions**:
1. **Check write permissions**: `ls -la` to check directory permissions
2. **Change directory**: `cd` to a writable directory
3. **Run with different user**: If in a restricted environment

### 🔧 Functionality Issues

#### Problem: Generated code doesn't work
**Solutions**:
1. **Check generated_code.py**: Review the generated code for issues
2. **Install missing imports**: The generated code might need additional packages
3. **Try different prompts**: Some prompts work better than others
4. **Check image quality**: Use clear, high-quality images

#### Problem: Object detection finds no objects
**Solutions**:
1. **Try different object types**: Instead of "person", try "car", "dog", "cat"
2. **Use clearer images**: Ensure objects are clearly visible
3. **Check confidence thresholds**: Lower detection thresholds if needed
4. **Try different images**: Some images work better than others

### 🌐 Network Issues

#### Problem: "Connection timeout" or "Network error"
**Solutions**:
1. **Check internet**: Ensure stable internet connection
2. **Check firewall**: Ensure API endpoints aren't blocked
3. **Try VPN**: Some regions might have restrictions
4. **Wait and retry**: Temporary network issues often resolve themselves

#### Problem: "SSL certificate verification failed"
**Solutions**:
1. **Update certificates**: `pip install --upgrade certifi`
2. **Check system time**: Ensure system clock is correct
3. **Corporate network**: Check if behind corporate firewall

## Advanced Usage

### 🎨 Custom Prompts

Try different prompts with `source.py`:

```python
# Edit source.py and change the content:
AgentMessage(
    role="user",
    content="Count the number of people in this image and draw bounding boxes around them",
    media=["people.jpg"]
)
```

**Effective prompt examples**:
- "Describe what you see in this image"
- "Count the number of [objects] in this image"
- "Detect and label all objects in this image"
- "Create a function to analyze this image for [specific task]"
- "Generate code to process similar images for [use case]"

### 🔧 Direct Tool Usage

Explore different tools in `test_tools.py`:

```python
# Different object detection
dets = T.countgd_object_detection("car", image)
dets = T.countgd_object_detection("dog", image)
dets = T.countgd_object_detection("bottle", image)

# Other available tools (if working)
# T.florence2_object_detection()
# T.owlv2_sam2_video_tracking()
# T.extract_frames_and_timestamps()
```

### 📊 Batch Processing

Process multiple images:

```python
import os
from pathlib import Path

image_dir = Path("quickstart")
for image_file in image_dir.glob("*.jpg"):
    print(f"Processing {image_file}")
    # Your processing code here
```

### 🎥 Video Processing

If you have video files and full functionality:

```python
import vision_agent.tools as T

# Extract frames from video
frames_and_ts = T.extract_frames_and_timestamps("video.mp4")
frames = [f["frame"] for f in frames_and_ts]

# Track objects in video
tracks = T.countgd_sam2_video_tracking("person", frames)

# Create visualization
viz = T.overlay_segmentation_masks(frames, tracks)
T.save_video(viz, "tracked_video.mp4")
```

## FAQ

### ❓ Do I need all three API keys?

**Yes**, Vision Agent requires all three API keys to function properly:
- **Vision Agent API**: Core functionality
- **Anthropic API**: Claude model for planning
- **Google API**: Gemini model for processing

### ❓ Are the API keys free?

**Partially**:
- **Vision Agent**: Free tier available
- **Anthropic**: $5 free credits for new accounts
- **Google**: Generous free usage limits

### ❓ Can I use different models?

**Yes**, you can configure different models by editing the Vision Agent configuration files, but the default models (Claude 3.7 Sonnet and Gemini Flash 2.0) are recommended for best performance.

### ❓ Why do I get OpenGL errors?

This is **normal in headless environments** (Docker, cloud servers, etc.). The scripts are designed to work around this limitation using mock demonstrations and non-interactive backends.

### ❓ How long does code generation take?

**Typically 30 seconds to 2 minutes**, depending on:
- Image complexity
- Prompt complexity
- API response times
- Network speed

### ❓ Can I use my own images?

**Yes**, just add your images to the `quickstart/` directory. Supported formats: `.jpg`, `.jpeg`, `.png`, `.bmp`

### ❓ What if the generated code doesn't work?

1. **Check the code**: Review `generated_code.py` for obvious issues
2. **Install dependencies**: The generated code might need additional packages
3. **Try different prompts**: More specific prompts often work better
4. **Check image quality**: Use clear, well-lit images

### ❓ How do I get help?

1. **Check this guide**: Most issues are covered in the troubleshooting section
2. **Run test script**: `python3 test_vision_agent.py` for diagnostic info
3. **Vision Agent Discord**: https://discord.com/invite/RVcW3j9RgR
4. **GitHub Issues**: https://github.com/landing-ai/vision-agent/issues
5. **Documentation**: https://landing-ai.github.io/vision-agent/

### ❓ Can I use this in production?

**Yes**, but consider:
- **API costs**: Monitor usage and costs
- **Rate limits**: Implement proper error handling
- **Security**: Keep API keys secure
- **Reliability**: Have fallback mechanisms

---

## 🎉 You're Ready!

If you've followed this guide, you should now have:
- ✅ Vision Agent properly installed
- ✅ API keys configured
- ✅ Working examples
- ✅ Understanding of troubleshooting

**Next steps**:
1. Experiment with different prompts and images
2. Explore the generated code to understand how Vision Agent works
3. Build your own computer vision applications
4. Join the community for support and inspiration

Happy coding with Vision Agent! 🚀
