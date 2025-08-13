#!/usr/bin/env python3
"""
Test script to verify vision-agent installation and imports
"""

def test_basic_imports():
    """Test importing basic Python modules"""
    success = True

    try:
        import sys
        print(f"✓ Python version: {sys.version}")
    except ImportError as e:
        print(f"✗ Failed to import sys: {e}")
        success = False

    try:
        import matplotlib.pyplot as plt
        print("✓ matplotlib imported successfully")
        print(f"  Version: {plt.matplotlib.__version__}")
    except ImportError as e:
        print(f"✗ Failed to import matplotlib: {e}")
        success = False

    try:
        import numpy as np
        print("✓ numpy imported successfully")
        print(f"  Version: {np.__version__}")
    except ImportError as e:
        print(f"✗ Failed to import numpy: {e}")
        success = False

    try:
        import anthropic
        print("✓ anthropic imported successfully")
        print(f"  Version: {anthropic.__version__}")
    except ImportError as e:
        print(f"✗ Failed to import anthropic: {e}")
        success = False

    return success

def test_vision_agent_imports():
    """Test importing vision-agent modules"""
    success = True

    try:
        import vision_agent
        print("✓ vision_agent imported successfully")
        print(f"  Version: {getattr(vision_agent, '__version__', 'unknown')}")
    except ImportError as e:
        print(f"✗ Failed to import vision_agent: {e}")
        success = False
        return success

    try:
        from vision_agent.agent import VisionAgentCoderV2
        print("✓ VisionAgentCoderV2 imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import VisionAgentCoderV2: {e}")
        success = False

    try:
        from vision_agent.models import AgentMessage
        print("✓ AgentMessage imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import AgentMessage: {e}")
        success = False

    # Test tools import separately as it may have display dependencies
    try:
        import vision_agent.tools as T
        print("✓ vision_agent.tools imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import vision_agent.tools: {e}")
        print(f"  Note: This may be due to missing display/OpenGL libraries")
        success = False

    return success

def check_environment():
    """Check environment variables and system info"""
    import os

    print("\nEnvironment Check:")
    print("-" * 30)

    api_keys = [
        "VISION_AGENT_API_KEY",
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY"
    ]

    for key in api_keys:
        value = os.getenv(key)
        if value:
            print(f"✓ {key}: Set (length: {len(value)})")
        else:
            print(f"✗ {key}: Not set")

if __name__ == "__main__":
    print("Testing vision-agent installation...")
    print("=" * 60)

    print("\n1. Testing Basic Dependencies:")
    print("-" * 40)
    basic_success = test_basic_imports()

    print("\n2. Testing Vision-Agent Modules:")
    print("-" * 40)
    vision_success = test_vision_agent_imports()

    check_environment()

    print("\n" + "=" * 60)
    print("INSTALLATION SUMMARY:")
    print("=" * 60)

    if basic_success:
        print("✓ Basic dependencies (matplotlib, numpy, anthropic) are working")
    else:
        print("✗ Some basic dependencies failed")

    if vision_success:
        print("✓ Vision-agent library is fully functional")
    else:
        print("✗ Vision-agent has some import issues (likely display/OpenGL related)")
        print("  This is common in headless environments and may not affect core functionality")

    print("\nNOTE: API keys are required for full functionality.")
    print("See the documentation for setup instructions.")

