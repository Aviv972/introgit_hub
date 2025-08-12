# Vision Agent Library Exploration

This project demonstrates how to set up and use the Landing AI Vision Agent library for computer vision tasks including image analysis, object detection, and code generation.

## Overview

Vision Agent is a Visual AI pilot from LandingAI that can:
- Generate code from natural language prompts and images
- Perform object detection and counting
- Track objects in videos
- Use various computer vision tools directly

## Project Structure

```
/home/daytona/introgit_hub/
├── README.md                 # This file - setup and usage guide
├── .env                      # API keys configuration (template)
├── test_import.py           # Installation verification script
├── quickstart/              # Main examples directory
│   ├── source.py            # Basic VisionAgent prompt example
│   ├── test_tools.py        # Direct tools usage example
│   └── [sample images]      # Test images for examples
├── test_vision_agent.py     # Comprehensive test runner
└── USAGE_GUIDE.md          # Detailed usage documentation
```

## Prerequisites

- Python 3.9 or higher (currently using Python 3.13.3)
- Internet connection for API calls
- API keys from three providers (see setup below)

## Installation Status

✅ **Vision Agent Library**: Installed (v1.1.19)  
✅ **Core Dependencies**: matplotlib, numpy, anthropic  
⚠️  **Display Libraries**: Limited due to headless environment  
❌ **API Keys**: Not configured (required for full functionality)

## API Keys Setup

You need to obtain API keys from three providers:

### 1. Vision Agent API Key
- **Website**: https://va.landing.ai/home
- **API Key Page**: https://va.landing.ai/settings/api-key
- **Purpose**: Access to Vision Agent's code generation capabilities

### 2. Anthropic API Key
- **Website**: https://console.anthropic.com/
- **API Key Page**: https://console.anthropic.com/settings/keys
- **Purpose**: Powers Claude 3.7 Sonnet model for planning and code generation

### 3. Google API Key
- **Website**: https://aistudio.google.com/
- **API Key Page**: https://aistudio.google.com/app/apikey
- **Purpose**: Powers Gemini Flash 2.0 Experimental model

### Setting Up API Keys

1. **Edit the .env file**:
   ```bash
   nano .env
   ```

2. **Uncomment and replace the placeholder values**:
   ```bash
   VISION_AGENT_API_KEY=your-actual-vision-agent-key
   ANTHROPIC_API_KEY=your-actual-anthropic-key
   GOOGLE_API_KEY=your-actual-google-key
   ```

3. **Load environment variables** (for current session):
   ```bash
   export $(cat .env | grep -v '^#' | xargs)
   ```

## Quick Start

### 1. Verify Installation
```bash
python3 test_import.py
```

### 2. Test Basic Functionality
```bash
python3 test_vision_agent.py
```

### 3. Run Vision Agent Examples
```bash
cd quickstart
python3 source.py          # Basic image description
python3 test_tools.py      # Direct tools usage
```

## Expected Behavior

### Without API Keys
- ❌ Vision Agent code generation will fail
- ❌ API-dependent tools will not work
- ✅ Library imports and basic structure work
- ✅ Local image processing may work

### With API Keys
- ✅ Full Vision Agent functionality
- ✅ Code generation from prompts
- ✅ Object detection and counting
- ✅ Image analysis and description

## Common Issues

### Import Errors
- **libGL.so.1 missing**: Common in headless environments, may not affect core functionality
- **Display issues**: Use `matplotlib.use('Agg')` for headless environments

### API Errors
- **Authentication failed**: Check API key validity and format
- **Rate limits**: Free tiers have usage limits
- **Network issues**: Ensure internet connectivity

### Dependencies
- **Missing packages**: Run installation verification script
- **Version conflicts**: Some dependency versions may conflict but shouldn't prevent basic usage

## Next Steps

1. **Get API Keys**: Follow the setup guide above
2. **Download Sample Images**: Add test images to the quickstart folder
3. **Run Examples**: Try the provided example scripts
4. **Explore Tools**: Experiment with different vision tools
5. **Read Documentation**: Check USAGE_GUIDE.md for detailed examples

## Resources

- **GitHub Repository**: https://github.com/landing-ai/vision-agent
- **Documentation**: https://landing-ai.github.io/vision-agent/
- **Discord Community**: https://discord.com/invite/RVcW3j9RgR
- **Video Tutorials**: https://www.youtube.com/playlist?list=PLrKGAzovU85fvo22OnVtPl90mxBygIf79

## Support

If you encounter issues:
1. Check the troubleshooting section in USAGE_GUIDE.md
2. Verify your API keys are correctly set
3. Run the test scripts to identify specific problems
4. Join the Discord community for help

---

**Note**: This is an exploration project. Some functionality may be limited due to the headless environment and missing system dependencies.
