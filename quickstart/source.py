#!/usr/bin/env python3
"""
Basic VisionAgent Prompt Script
===============================

This script demonstrates how to use VisionAgentCoderV2 to generate code for describing an image.
It includes proper error handling for missing API keys and provides informative messages.

Usage:
    python3 source.py

Requirements:
    - Vision Agent library installed
    - API keys set as environment variables:
      * VISION_AGENT_API_KEY
      * ANTHROPIC_API_KEY
      * GOOGLE_API_KEY
    - Sample image (people.jpg or landscape.jpg) in the same directory
"""

import os
import sys
from pathlib import Path

def check_api_keys():
    """Check if required API keys are set as environment variables"""
    required_keys = [
        "VISION_AGENT_API_KEY",
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY"
    ]

    missing_keys = []
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)

    if missing_keys:
        print("❌ Missing required API keys:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\n📋 To set up API keys:")
        print("1. Edit the .env file in the project root")
        print("2. Uncomment and add your actual API keys")
        print("3. Load them with: export $(cat ../.env | grep -v '^#' | xargs)")
        print("\n🔗 Get API keys from:")
        print("   - Vision Agent: https://va.landing.ai/settings/api-key")
        print("   - Anthropic: https://console.anthropic.com/settings/keys")
        print("   - Google: https://aistudio.google.com/app/apikey")
        return False

    print("✅ All required API keys are set")
    return True

def check_sample_images():
    """Check if sample images are available"""
    current_dir = Path(__file__).parent
    image_files = ["people.jpg", "landscape.jpg"]

    available_images = []
    for image_file in image_files:
        image_path = current_dir / image_file
        if image_path.exists():
            available_images.append(image_file)
            print(f"✅ Found sample image: {image_file}")

    if not available_images:
        print("❌ No sample images found in the quickstart directory")
        print("Expected files: people.jpg, landscape.jpg")
        return None

    return available_images[0]  # Return the first available image

def test_vision_agent_import():
    """Test importing VisionAgent modules"""
    try:
        from vision_agent.agent import VisionAgentCoderV2
        from vision_agent.models import AgentMessage
        print("✅ VisionAgent modules imported successfully")
        return VisionAgentCoderV2, AgentMessage
    except ImportError as e:
        print(f"❌ Failed to import VisionAgent modules: {e}")
        print("\n💡 This might be due to:")
        print("   - Missing system dependencies (OpenGL libraries)")
        print("   - Incomplete installation")
        print("   - Environment issues")
        print("\n🔧 Try running: python3 ../test_import.py")
        return None, None

def run_vision_agent_example(image_file):
    """Run the basic VisionAgent example"""
    print(f"\n🚀 Running VisionAgent with image: {image_file}")
    print("=" * 50)

    # Import the classes
    VisionAgentCoderV2, AgentMessage = test_vision_agent_import()
    if not VisionAgentCoderV2 or not AgentMessage:
        return False

    try:
        # Enable verbose output
        print("📝 Initializing VisionAgentCoderV2...")
        agent = VisionAgentCoderV2(verbose=True)

        # Add your prompt (content) and image file (media)
        print(f"🖼️  Processing image: {image_file}")
        print("💭 Prompt: 'Describe the image'")
        print("\n⏳ Generating code... (this may take a while)")

        code_context = agent.generate_code(
            [
                AgentMessage(
                    role="user",
                    content="Describe the image",
                    media=[image_file]
                )
            ]
        )

        # Write the output to a file
        output_file = "generated_code.py"
        with open(output_file, "w") as f:
            f.write(code_context.code + "\n" + code_context.test)

        print(f"✅ Code generation completed!")
        print(f"📄 Generated code saved to: {output_file}")
        print(f"📊 Code length: {len(code_context.code)} characters")
        print(f"🧪 Test length: {len(code_context.test)} characters")

        # Show a preview of the generated code
        print("\n📋 Generated Code Preview:")
        print("-" * 30)
        code_lines = code_context.code.split('\n')
        for i, line in enumerate(code_lines[:10]):  # Show first 10 lines
            print(f"{i+1:2d}: {line}")
        if len(code_lines) > 10:
            print(f"... ({len(code_lines) - 10} more lines)")

        return True

    except Exception as e:
        print(f"❌ Error during code generation: {e}")
        print(f"Error type: {type(e).__name__}")

        # Provide specific error guidance
        if "API" in str(e) or "key" in str(e).lower():
            print("\n💡 This looks like an API key issue:")
            print("   - Verify your API keys are correct")
            print("   - Check if you have sufficient API credits")
            print("   - Ensure keys are properly loaded as environment variables")
        elif "network" in str(e).lower() or "connection" in str(e).lower():
            print("\n💡 This looks like a network issue:")
            print("   - Check your internet connection")
            print("   - Verify API endpoints are accessible")
        else:
            print("\n💡 For troubleshooting:")
            print("   - Check the Vision Agent documentation")
            print("   - Verify all dependencies are installed")
            print("   - Try with a different image")

        return False

def main():
    """Main function to run the VisionAgent example"""
    print("🎯 VisionAgent Basic Prompt Script")
    print("=" * 40)

    # Check API keys
    print("\n1️⃣  Checking API Keys...")
    if not check_api_keys():
        print("\n⚠️  Cannot proceed without API keys. Please set them up first.")
        sys.exit(1)

    # Check sample images
    print("\n2️⃣  Checking Sample Images...")
    image_file = check_sample_images()
    if not image_file:
        print("\n⚠️  Cannot proceed without sample images.")
        sys.exit(1)

    # Run VisionAgent example
    print("\n3️⃣  Running VisionAgent Example...")
    success = run_vision_agent_example(image_file)

    if success:
        print("\n🎉 VisionAgent example completed successfully!")
        print("📁 Check the generated_code.py file for the results.")
    else:
        print("\n❌ VisionAgent example failed.")
        print("📖 Check the error messages above for troubleshooting guidance.")
        sys.exit(1)

if __name__ == "__main__":
    main()
