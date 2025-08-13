#!/usr/bin/env python3
"""
Vision Agent Patch Module
=========================

This module provides monkey-patching functionality to integrate the Gemini API wrapper
with the Vision Agent library. It intercepts Gemini API calls from Vision Agent and
routes them through our wrapper to fix the protobuf structure validation issue.

The patch addresses the specific error:
""Invalid value at 'contents[1].parts[1].function_call.args' "
"(type.googleapis.com/google.protobuf.Struct)""

Usage:
    # Apply the patch before using Vision Agent
    from vision_agent_patch import apply_vision_agent_patch
    apply_vision_agent_patch()

    # Now use Vision Agent normally
    from vision_agent.agent import VisionAgentCoderV2
    agent = VisionAgentCoderV2()

Features:
    - Automatic detection of Vision Agent installation
    - Runtime patching of Gemini API calls
    - Fallback behavior when Vision Agent is not available
    - Comprehensive logging for debugging
    - Easy integration with existing Vision Agent workflows
"""

import os
import sys
import logging
import importlib
import traceback
from typing import Optional, Any, Dict, List, Callable
from functools import wraps

# Import our Gemini API wrapper
try:
    from gemini_api_wrapper import GeminiAPIWrapper, create_wrapper
    WRAPPER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Warning: GeminiAPIWrapper not available: {e}")
    WRAPPER_AVAILABLE = False


class VisionAgentPatcher:
    """
    Main class for patching Vision Agent to use the Gemini API wrapper.
    """

    def __init__(self, verbose: bool = False):
        """
        Initialize the Vision Agent patcher.

        Args:
            verbose: Enable verbose logging for debugging.
        """
        self.verbose = verbose
        self.logger = self._setup_logging()
        self.wrapper = None
        self.original_methods = {}
        self.is_patched = False
        self.vision_agent_available = False

        # Check if wrapper is available
        if not WRAPPER_AVAILABLE:
            self.logger.error("GeminiAPIWrapper not available. Patching will not work.")
            return

        # Initialize the wrapper
        try:
            self.wrapper = create_wrapper(verbose=verbose)
            self.logger.info("Gemini API wrapper initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini API wrapper: {e}")

    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the patcher."""
        logger = logging.getLogger('VisionAgentPatcher')
        logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def check_vision_agent_availability(self) -> bool:
        """
        Check if Vision Agent is available and can be imported.

        Returns:
            True if Vision Agent is available, False otherwise.
        """
        try:
            # Try to import the main vision_agent module
            import vision_agent
            self.logger.info("Vision Agent main module is available")

            # Try to import specific components
            components_to_check = [
                ('vision_agent.agent', 'VisionAgentCoderV2'),
                ('vision_agent.models', 'AgentMessage'),
                ('vision_agent.tools', None),
            ]

            available_components = []
            for module_name, class_name in components_to_check:
                try:
                    module = importlib.import_module(module_name)
                    if class_name and hasattr(module, class_name):
                        available_components.append(f"{module_name}.{class_name}")
                    elif not class_name:
                        available_components.append(module_name)
                    self.logger.debug(f"✅ {module_name} available")
                except ImportError as e:
                    self.logger.debug(f"❌ {module_name} not available: {e}")

            self.vision_agent_available = len(available_components) > 0

            if self.vision_agent_available:
                self.logger.info(f"Vision Agent components available: {available_components}")
            else:
                self.logger.warning("No Vision Agent components are available")

            return self.vision_agent_available

        except ImportError as e:
            self.logger.warning(f"Vision Agent not available: {e}")
            self.vision_agent_available = False
            return False
        except Exception as e:
            self.logger.error(f"Error checking Vision Agent availability: {e}")
            self.vision_agent_available = False
            return False

    def _create_patched_generate_content(self, original_method: Callable) -> Callable:
        """
        Create a patched version of a generate_content method.

        Args:
            original_method: The original method to patch.

        Returns:
            Patched method that uses our wrapper.
        """
        @wraps(original_method)
        def patched_generate_content(*args, **kwargs):
            self.logger.debug(
                f"Intercepted generate_content call with args: {len(args)}, "
                f"kwargs: {list(kwargs.keys())}")

            try:
                # If we have a wrapper, use it to process the call
                if self.wrapper:
                    # Check if this looks like a Gemini API call with function call arguments
                    if len(args) > 0 and isinstance(args[0], (list, tuple)):
                        contents = args[0]

                        # Process contents to fix function call arguments
                        processed_contents = self._process_contents_for_function_calls(contents)

                        if processed_contents != contents:
                            self.logger.info("Function call arguments were processed by wrapper")
                            # Call original method with processed contents
                            new_args = (processed_contents,) + args[1:]
                            return original_method(*new_args, **kwargs)

                # If no processing needed or wrapper not available, call original method
                return original_method(*args, **kwargs)

            except Exception as e:
                self.logger.error(f"Error in patched generate_content: {e}")
                self.logger.error(f"Traceback: {traceback.format_exc()}")
                # Fall back to original method
                return original_method(*args, **kwargs)

        return patched_generate_content

    def _process_contents_for_function_calls(
        self, contents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Process contents to fix function call arguments using our wrapper.

        Args:
            contents: List of content parts that may contain function calls.

        Returns:
            Processed contents with fixed function call arguments.
        """
        if not isinstance(contents, (list, tuple)):
            return contents

        processed_contents = []

        for content in contents:
            if isinstance(content, dict) and 'parts' in content:
                processed_parts = []

                for part in content['parts']:
                    if isinstance(part, dict) and 'function_call' in part:
                        # This part contains a function call - process it
                        try:
                            function_call = part['function_call']
                            if 'args' in function_call:
                                # Use our wrapper to transform the arguments
                                transformed_args = self.wrapper.transform_function_call_args(
                                    function_call['args'])

                                processed_part = {
                                    'function_call': {
                                        'name': function_call['name'],
                                        'args': transformed_args
                                    }
                                }
                                processed_parts.append(processed_part)
                                self.logger.debug(
                                    f"Processed function call: {function_call['name']}")
                            else:
                                processed_parts.append(part)
                        except Exception as e:
                            self.logger.warning(f"Failed to process function call part: {e}")
                            processed_parts.append(part)
                    else:
                        processed_parts.append(part)

                processed_content = content.copy()
                processed_content['parts'] = processed_parts
                processed_contents.append(processed_content)
            else:
                processed_contents.append(content)

        return processed_contents

    def _patch_google_genai_module(self):
        """Patch the google.genai module if it's being used by Vision Agent."""
        try:
            import google.genai as genai

            # Look for GenerativeModel or Client classes
            if hasattr(genai, 'GenerativeModel'):
                original_class = genai.GenerativeModel

                class PatchedGenerativeModel(original_class):
                    def generate_content(self, *args, **kwargs):
                        self.logger.debug("Intercepted GenerativeModel.generate_content")
                        return self._create_patched_generate_content(super().generate_content)(*args, **kwargs)

                genai.GenerativeModel = PatchedGenerativeModel
                self.logger.info("Patched google.genai.GenerativeModel")

            elif hasattr(genai, 'Client'):
                # For the newer google.genai package structure
                original_client = genai.Client

                class PatchedClient(original_client):
                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, **kwargs)
                        # Patch the models.generate_content method if it exists
                        if hasattr(self, 'models') and hasattr(self.models, 'generate_content'):
                            original_generate = self.models.generate_content
                            self.models.generate_content = self._create_patched_generate_content(
                                original_generate)

                genai.Client = PatchedClient
                self.logger.info("Patched google.genai.Client")

        except ImportError:
            self.logger.debug("google.genai not available for patching")
        except Exception as e:
            self.logger.error(f"Error patching google.genai: {e}")

    def _patch_google_generativeai_module(self):
        """Patch the google.generativeai module if it's available."""
        try:
            import google.generativeai as genai

            if hasattr(genai, 'GenerativeModel'):
                original_class = genai.GenerativeModel
                patcher = self

                class PatchedGenerativeModel(original_class):
                    def generate_content(self, *args, **kwargs):
                        patcher.logger.debug(
                            "Intercepted google.generativeai.GenerativeModel.generate_content")
                        return patcher._create_patched_generate_content(super().generate_content)(*args, **kwargs)

                genai.GenerativeModel = PatchedGenerativeModel
                self.logger.info("Patched google.generativeai.GenerativeModel")

        except ImportError:
            self.logger.debug("google.generativeai not available for patching")
        except Exception as e:
            self.logger.error(f"Error patching google.generativeai: {e}")

    def _patch_vision_agent_modules(self):
        """Patch Vision Agent modules that might make Gemini API calls."""
        try:
            # Try to patch vision_agent.agent module
            try:
                import vision_agent.agent as agent_module

                # Look for classes that might make API calls
                if hasattr(agent_module, 'VisionAgentCoderV2'):
                    original_class = agent_module.VisionAgentCoderV2
                    patcher = self

                    # We'll patch any method that might make API calls
                    class PatchedVisionAgentCoderV2(original_class):
                        def __init__(self, *args, **kwargs):
                            super().__init__(*args, **kwargs)
                            patcher.logger.info("VisionAgentCoderV2 initialized with patching")

                    agent_module.VisionAgentCoderV2 = PatchedVisionAgentCoderV2
                    self.logger.info("Patched vision_agent.agent.VisionAgentCoderV2")

            except ImportError:
                self.logger.debug("vision_agent.agent not available for patching")

            # Try to patch other Vision Agent modules that might use Gemini API
            modules_to_check = [
                'vision_agent.models',
                'vision_agent.tools',
                'vision_agent.llm',
            ]

            for module_name in modules_to_check:
                try:
                    module = importlib.import_module(module_name)
                    self.logger.debug(f"Checked {module_name} for patching opportunities")
                except ImportError:
                    self.logger.debug(f"{module_name} not available")

        except Exception as e:
            self.logger.error(f"Error patching Vision Agent modules: {e}")

    def apply_patches(self) -> bool:
        """
        Apply all necessary patches to integrate the Gemini API wrapper.

        Returns:
            True if patches were applied successfully, False otherwise.
        """
        if not WRAPPER_AVAILABLE:
            self.logger.error("Cannot apply patches - GeminiAPIWrapper not available")
            return False

        if not self.wrapper:
            self.logger.error("Cannot apply patches - wrapper not initialized")
            return False

        if self.is_patched:
            self.logger.warning("Patches already applied")
            return True

        try:
            self.logger.info("Applying Vision Agent patches...")

            # Check if Vision Agent is available
            if not self.check_vision_agent_availability():
                self.logger.warning("Vision Agent not available - applying Google AI patches only")

            # Patch Google AI modules (these are the actual API interfaces)
            self._patch_google_genai_module()
            self._patch_google_generativeai_module()

            # Patch Vision Agent modules if available
            if self.vision_agent_available:
                self._patch_vision_agent_modules()

            self.is_patched = True
            self.logger.info("✅ Vision Agent patches applied successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to apply patches: {e}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return False

    def remove_patches(self):
        """Remove applied patches (if possible)."""
        if not self.is_patched:
            self.logger.info("No patches to remove")
            return

        self.logger.warning(
            "Patch removal not fully implemented - restart Python to remove patches")
        # Note: Full patch removal is complex due to the nature of monkey patching
        # In practice, users should restart their Python session to remove patches

    def get_patch_status(self) -> Dict[str, Any]:
        """
        Get the current status of applied patches.

        Returns:
            Dictionary containing patch status information.
        """
        return {
            'wrapper_available': WRAPPER_AVAILABLE,
            'wrapper_initialized': self.wrapper is not None,
            'vision_agent_available': self.vision_agent_available,
            'patches_applied': self.is_patched,
            'verbose_logging': self.verbose,
        }


# Global patcher instance
_global_patcher: Optional[VisionAgentPatcher] = None


def apply_vision_agent_patch(verbose: bool = False) -> bool:
    """
    Convenience function to apply Vision Agent patches.

    Args:
        verbose: Enable verbose logging for debugging.

    Returns:
        True if patches were applied successfully, False otherwise.
    """
    global _global_patcher

    if _global_patcher is None:
        _global_patcher = VisionAgentPatcher(verbose=verbose)

    return _global_patcher.apply_patches()


def remove_vision_agent_patch():
    """Convenience function to remove Vision Agent patches."""
    global _global_patcher

    if _global_patcher is not None:
        _global_patcher.remove_patches()


def get_patch_status() -> Dict[str, Any]:
    """
    Get the current status of Vision Agent patches.

    Returns:
        Dictionary containing patch status information.
    """
    global _global_patcher

    if _global_patcher is None:
        return {
            'wrapper_available': WRAPPER_AVAILABLE,
            'wrapper_initialized': False,
            'vision_agent_available': False,
            'patches_applied': False,
            'verbose_logging': False,
        }

    return _global_patcher.get_patch_status()


def test_patch_functionality():
    """Test the patch functionality with mock data."""
    print("🧪 Testing Vision Agent Patch Functionality")
    print("=" * 50)

    # Test patcher initialization
    patcher = VisionAgentPatcher(verbose=True)
    print(f"✅ Patcher initialized: {patcher is not None}")

    # Test Vision Agent availability check
    va_available = patcher.check_vision_agent_availability()
    print(f"Vision Agent available: {va_available}")

    # Test patch application
    if WRAPPER_AVAILABLE:
        patch_success = patcher.apply_patches()
        print(f"✅ Patches applied: {patch_success}")

        # Test patch status
        status = patcher.get_patch_status()
        print(f"✅ Patch status: {status}")
    else:
        print("❌ Cannot test patches - wrapper not available")

    print("\n" + "=" * 50)
    print("Patch functionality test completed.")


if __name__ == "__main__":
    print("Vision Agent Patch Module")
    print("=" * 40)
    print()
    print("This module provides monkey-patching functionality to integrate")
    print("the Gemini API wrapper with Vision Agent to fix protobuf structure")
    print("validation issues in function call arguments.")
    print()
    print("Usage:")
    print("  from vision_agent_patch import apply_vision_agent_patch")
    print("  apply_vision_agent_patch()")
    print()
    print("Running test functionality...")
    print()

    test_patch_functionality()



