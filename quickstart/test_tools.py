#!/usr/bin/env python3
"""
Direct VisionAgent Tools Usage Script
====================================

This script demonstrates how to use vision_agent.tools directly for object detection
without using the full VisionAgent code generation pipeline. It includes visualization
with matplotlib and saving results.

Usage:
    python3 test_tools.py

Features:
    - Direct usage of countgd_object_detection tool
    - Image loading and processing
    - Bounding box visualization
    - Results saving and display
    - Error handling for missing dependencies

Requirements:
    - Vision Agent library installed
    - matplotlib for visualization
    - Sample images in the same directory
"""

import os
import sys
from pathlib import Path
import traceback

def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    # Check matplotlib
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        print(f"✅ matplotlib: {matplotlib.__version__}")
        
        # Set backend for headless environments
        matplotlib.use('Agg')  # Use non-interactive backend
        print("📊 Set matplotlib to non-interactive backend (Agg)")
        
    except ImportError as e:
        print(f"❌ matplotlib not available: {e}")
        return False
    
    # Check numpy
    try:
        import numpy as np
        print(f"✅ numpy: {np.__version__}")
    except ImportError as e:
        print(f"❌ numpy not available: {e}")
        return False
    
    # Check PIL/Pillow
    try:
        from PIL import Image
        print(f"✅ PIL/Pillow: {Image.__version__}")
    except ImportError as e:
        print(f"❌ PIL/Pillow not available: {e}")
        return False
    
    return True

def test_vision_agent_tools_import():
    """Test importing vision_agent.tools"""
    print("\n🔧 Testing vision_agent.tools import...")
    
    try:
        import vision_agent.tools as T
        print("✅ vision_agent.tools imported successfully")
        
        # Check available functions
        available_functions = [attr for attr in dir(T) if not attr.startswith('_')]
        print(f"📋 Available functions: {len(available_functions)}")
        
        # Check for specific functions we need
        required_functions = [
            'load_image',
            'countgd_object_detection', 
            'overlay_bounding_boxes',
            'save_image'
        ]
        
        missing_functions = []
        for func in required_functions:
            if hasattr(T, func):
                print(f"✅ {func}: Available")
            else:
                print(f"❌ {func}: Not available")
                missing_functions.append(func)
        
        if missing_functions:
            print(f"\n⚠️  Missing functions: {missing_functions}")
            print("This may be due to incomplete installation or environment issues.")
            return None
        
        return T
        
    except ImportError as e:
        print(f"❌ Failed to import vision_agent.tools: {e}")
        print("\n💡 This might be due to:")
        print("   - Missing system dependencies (OpenGL libraries)")
        print("   - Incomplete installation")
        print("   - Environment issues")
        return None

def find_sample_images():
    """Find available sample images"""
    print("\n🖼️  Looking for sample images...")
    
    current_dir = Path(__file__).parent
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    
    found_images = []
    for ext in image_extensions:
        for image_file in current_dir.glob(f"*{ext}"):
            found_images.append(str(image_file))
            print(f"✅ Found: {image_file.name}")
    
    if not found_images:
        print("❌ No sample images found")
        print("Expected files: people.jpg, landscape.jpg")
        return None
    
    return found_images

def create_mock_detection_results(image_path):
    """Create mock detection results for demonstration when tools don't work"""
    print(f"🎭 Creating mock detection results for: {Path(image_path).name}")
    
    # Mock detection results structure
    mock_results = [
        {
            'label': 'person',
            'bbox': [100, 50, 200, 300],  # [x1, y1, x2, y2]
            'score': 0.95
        },
        {
            'label': 'person', 
            'bbox': [250, 80, 350, 280],
            'score': 0.87
        }
    ]
    
    print(f"📊 Mock results: {len(mock_results)} detections")
    for i, result in enumerate(mock_results):
        print(f"   {i+1}. {result['label']} (confidence: {result['score']:.2f})")
    
    return mock_results

def visualize_detections_matplotlib(image_path, detections, output_path):
    """Visualize detections using matplotlib"""
    print(f"\n🎨 Creating visualization with matplotlib...")
    
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        from PIL import Image
        import numpy as np
        
        # Load image
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Create figure and axis
        fig, ax = plt.subplots(1, figsize=(12, 8))
        ax.imshow(img_array)
        
        # Add bounding boxes
        colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']
        
        for i, detection in enumerate(detections):
            bbox = detection['bbox']
            label = detection['label']
            score = detection.get('score', 0.0)
            
            # Create rectangle patch
            x1, y1, x2, y2 = bbox
            width = x2 - x1
            height = y2 - y1
            
            color = colors[i % len(colors)]
            rect = patches.Rectangle(
                (x1, y1), width, height,
                linewidth=2, edgecolor=color, facecolor='none'
            )
            ax.add_patch(rect)
            
            # Add label
            ax.text(
                x1, y1 - 10,
                f"{label} ({score:.2f})",
                bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.7),
                fontsize=10, color='white', weight='bold'
            )
        
        ax.set_title(f"Object Detection Results - {Path(image_path).name}", fontsize=14)
        ax.axis('off')
        
        # Save the result
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()  # Close to free memory
        
        print(f"✅ Visualization saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating visualization: {e}")
        print(f"Error details: {traceback.format_exc()}")
        return False

def run_object_detection_demo(image_path, tools_module=None):
    """Run object detection demonstration"""
    print(f"\n🎯 Running object detection demo on: {Path(image_path).name}")
    print("=" * 60)
    
    detections = None
    
    if tools_module:
        # Try to use real vision_agent.tools
        print("🔧 Attempting to use vision_agent.tools...")
        try:
            # Load the image
            print("📂 Loading image...")
            image = tools_module.load_image(image_path)
            print("✅ Image loaded successfully")
            
            # Call the function to count objects in an image
            print("🔍 Running object detection...")
            detections = tools_module.countgd_object_detection("person", image)
            print(f"✅ Detection completed: {len(detections)} objects found")
            
            # Try to create visualization using vision_agent tools
            print("🎨 Creating visualization with vision_agent tools...")
            viz = tools_module.overlay_bounding_boxes(image, detections)
            
            # Save the visualization
            output_path = f"people_detected_va.png"
            tools_module.save_image(viz, output_path)
            print(f"✅ Vision Agent visualization saved to: {output_path}")
            
        except Exception as e:
            print(f"❌ Error using vision_agent.tools: {e}")
            print("🎭 Falling back to mock demonstration...")
            detections = None
    
    # If vision_agent.tools didn't work, use mock data
    if detections is None:
        detections = create_mock_detection_results(image_path)
    
    # Create matplotlib visualization
    output_path = f"detection_results_{Path(image_path).stem}.png"
    success = visualize_detections_matplotlib(image_path, detections, output_path)
    
    if success:
        print(f"\n📊 Detection Summary:")
        print(f"   - Image: {Path(image_path).name}")
        print(f"   - Objects detected: {len(detections)}")
        print(f"   - Visualization: {output_path}")
        
        # Show detection details
        for i, detection in enumerate(detections):
            label = detection['label']
            score = detection.get('score', 0.0)
            bbox = detection['bbox']
            print(f"   - Detection {i+1}: {label} (confidence: {score:.2f}) at {bbox}")
    
    return success

def main():
    """Main function to run the direct tools demonstration"""
    print("🔧 VisionAgent Direct Tools Usage Demo")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Missing required dependencies. Please install them first.")
        sys.exit(1)
    
    # Test vision_agent.tools import
    tools_module = test_vision_agent_tools_import()
    if tools_module:
        print("✅ VisionAgent tools are available")
    else:
        print("⚠️  VisionAgent tools not available - will use mock demonstration")
    
    # Find sample images
    sample_images = find_sample_images()
    if not sample_images:
        print("\n❌ No sample images found. Please add some images to test with.")
        sys.exit(1)
    
    # Run demonstrations on available images
    success_count = 0
    for image_path in sample_images[:2]:  # Limit to first 2 images
        try:
            success = run_object_detection_demo(image_path, tools_module)
            if success:
                success_count += 1
        except Exception as e:
            print(f"❌ Error processing {image_path}: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 DEMO SUMMARY")
    print("=" * 50)
    
    if success_count > 0:
        print(f"✅ Successfully processed {success_count} image(s)")
        print("📁 Check the generated PNG files for visualization results")
        
        if tools_module:
            print("🔧 VisionAgent tools were used for detection")
        else:
            print("🎭 Mock data was used for demonstration")
            print("💡 Install missing dependencies to use real VisionAgent tools")
        
        print("\n🎯 Next steps:")
        print("   - Set up API keys to use full VisionAgent functionality")
        print("   - Try different object types (e.g., 'car', 'dog', 'cat')")
        print("   - Experiment with different images")
        
    else:
        print("❌ No images were processed successfully")
        print("🔧 Check the error messages above for troubleshooting")

if __name__ == "__main__":
    main()
