#!/usr/bin/env python3
"""Test script to check Google AI package imports"""

print("Testing Google AI package imports...")

# Test google.genai
try:
    import google.genai as genai
    print("✅ google.genai imported successfully")
    print(f"   Available attributes: {[attr for attr in dir(genai) if not attr.startswith('_')][:10]}")
except ImportError as e:
    print(f"❌ Failed to import google.genai: {e}")

# Test google.generativeai
try:
    import google.generativeai as genai_alt
    print("✅ google.generativeai imported successfully")
    print(f"   Available attributes: {[attr for attr in dir(genai_alt) if not attr.startswith('_')][:10]}")
except ImportError as e:
    print(f"❌ Failed to import google.generativeai: {e}")

# Test other potential imports
try:
    import google
    print(f"✅ google package available, submodules: {[attr for attr in dir(google) if not attr.startswith('_')]}")
except ImportError as e:
    print(f"❌ Failed to import google: {e}")
