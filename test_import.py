#!/usr/bin/env python3
"""
Test script to verify vision-agent installation and imports
"""

def test_imports():
    """Test importing vision-agent modules"""
    try:
        import vision_agent
        print("✓ vision_agent imported successfully")
        print(f"  Version: {getattr(vision_agent, '__version__', 'unknown')}")
    except ImportError as e:
        print(f"✗ Failed to import vision_agent: {e}")
        return False
    
    try:
        from vision_agent.agent import VisionAgentCoderV2
        print("✓ VisionAgentCoderV2 imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import VisionAgentCoderV2: {e}")
        return False
    
    try:
        from vision_agent.models import AgentMessage
        print("✓ AgentMessage imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import AgentMessage: {e}")
        return False
    
    try:
        import vision_agent.tools as T
        print("✓ vision_agent.tools imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import vision_agent.tools: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✓ matplotlib imported successfully")
        print(f"  Version: {plt.matplotlib.__version__}")
    except ImportError as e:
        print(f"✗ Failed to import matplotlib: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing vision-agent installation...")
    print("=" * 50)
    
    success = test_imports()
    
    print("=" * 50)
    if success:
        print("✓ All imports successful! Vision-agent is ready to use.")
    else:
        print("✗ Some imports failed. Check the error messages above.")
