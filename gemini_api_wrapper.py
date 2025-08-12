#!/usr/bin/env python3
"""
Gemini API Function Call Wrapper
================================

This module provides a wrapper for the Gemini API to handle function call arguments
properly, specifically addressing the protobuf structure validation issue with path
arguments that causes HTTP 400 Bad Request errors.

The main issue occurs when function call arguments are passed as simple JSON strings
instead of properly structured protobuf-compatible objects.

Usage:
    from gemini_api_wrapper import GeminiAPIWrapper
    
    wrapper = GeminiAPIWrapper()
    # Use wrapper methods to make API calls with proper argument formatting
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
import traceback

# Try to import the Google Generative AI package
try:
    import google.genai as genai
    GENAI_AVAILABLE = True
except ImportError:
    try:
        import google.generativeai as genai
        GENAI_AVAILABLE = True
    except ImportError:
        genai = None
        GENAI_AVAILABLE = False


class GeminiAPIWrapper:
    """
    Wrapper class for Gemini API that handles proper formatting of function call arguments.
    
    This wrapper addresses the specific issue where path arguments in function calls
    need to be properly structured for protobuf compatibility.
    """
    
    def __init__(self, api_key: Optional[str] = None, verbose: bool = False):
        """
        Initialize the Gemini API wrapper.
        
        Args:
            api_key: Google API key. If None, will try to get from environment.
            verbose: Enable verbose logging for debugging.
        """
        self.logger = self._setup_logging(verbose)
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        
        if not GENAI_AVAILABLE:
            self.logger.warning("Google Generative AI package not available. API calls will be mocked.")
        elif self.api_key:
            try:
                # Configure the API key based on the available package
                if hasattr(genai, 'configure'):
                    genai.configure(api_key=self.api_key)
                else:
                    # For google.genai package, we might need a different configuration method
                    self.client = genai.Client(api_key=self.api_key)
                self.logger.info("Gemini API configured successfully")
            except Exception as e:
                self.logger.error(f"Failed to configure Gemini API: {e}")
        else:
            self.logger.warning("No Google API key provided. API calls will fail.")
    
    def _setup_logging(self, verbose: bool) -> logging.Logger:
        """Set up logging for the wrapper."""
        logger = logging.getLogger('GeminiAPIWrapper')
        logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def validate_path_argument(self, path: Union[str, Path, Dict[str, Any]]) -> str:
        """
        Validate and sanitize path arguments.
        
        Args:
            path: Path argument that can be a string, Path object, or dict containing path.
            
        Returns:
            Validated path as string.
            
        Raises:
            ValueError: If path is invalid or cannot be processed.
        """
        try:
            if isinstance(path, dict):
                if 'path' in path:
                    path_value = path['path']
                else:
                    raise ValueError("Dictionary must contain 'path' key")
            else:
                path_value = path
            
            # Convert to Path object for validation
            if isinstance(path_value, str):
                path_obj = Path(path_value)
            elif isinstance(path_value, Path):
                path_obj = path_value
            else:
                raise ValueError(f"Unsupported path type: {type(path_value)}")
            
            # Convert to absolute path string
            validated_path = str(path_obj.resolve())
            
            self.logger.debug(f"Path validated: {path} -> {validated_path}")
            return validated_path
            
        except Exception as e:
            error_msg = f"Failed to validate path argument '{path}': {str(e)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg) from e
    
    def transform_function_call_args(self, args: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Transform function call arguments to protobuf-compatible format.
        
        The Gemini API expects function call arguments as properly structured objects,
        not as JSON strings. This method handles the transformation.
        
        Args:
            args: Function call arguments (can be JSON string or dict).
            
        Returns:
            Properly formatted arguments dict.
            
        Raises:
            ValueError: If arguments cannot be processed.
        """
        try:
            # If args is a string, try to parse as JSON
            if isinstance(args, str):
                try:
                    parsed_args = json.loads(args)
                    self.logger.debug(f"Parsed JSON string args: {args} -> {parsed_args}")
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON in arguments: {args}") from e
            elif isinstance(args, dict):
                parsed_args = args.copy()
            else:
                raise ValueError(f"Unsupported argument type: {type(args)}")
            
            # Process path arguments specifically
            if 'path' in parsed_args:
                validated_path = self.validate_path_argument(parsed_args['path'])
                parsed_args['path'] = validated_path
                self.logger.debug(f"Transformed path argument: {parsed_args['path']}")
            
            # Ensure all values are properly typed for protobuf
            formatted_args = self._ensure_protobuf_compatibility(parsed_args)
            
            self.logger.debug(f"Final transformed args: {formatted_args}")
            return formatted_args
            
        except Exception as e:
            error_msg = f"Failed to transform function call arguments: {str(e)}"
            self.logger.error(error_msg)
            self.logger.error(f"Original args: {args}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            raise ValueError(error_msg) from e
    
    def _ensure_protobuf_compatibility(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure all argument values are compatible with protobuf structure.
        
        Args:
            args: Dictionary of arguments to process.
            
        Returns:
            Dictionary with protobuf-compatible values.
        """
        compatible_args = {}
        
        for key, value in args.items():
            if isinstance(value, (str, int, float, bool)):
                compatible_args[key] = value
            elif isinstance(value, Path):
                compatible_args[key] = str(value)
            elif isinstance(value, list):
                # Handle lists by ensuring all elements are compatible
                compatible_args[key] = [
                    str(item) if isinstance(item, Path) else item
                    for item in value
                ]
            elif isinstance(value, dict):
                # Recursively process nested dictionaries
                compatible_args[key] = self._ensure_protobuf_compatibility(value)
            else:
                # Convert other types to string as fallback
                compatible_args[key] = str(value)
                self.logger.warning(f"Converted {key} value to string: {type(value)} -> str")
        
        return compatible_args
    
    def create_function_call_part(self, function_name: str, args: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a properly formatted function call part for Gemini API.
        
        Args:
            function_name: Name of the function to call.
            args: Function arguments.
            
        Returns:
            Properly formatted function call part.
        """
        try:
            transformed_args = self.transform_function_call_args(args)
            
            function_call_part = {
                "function_call": {
                    "name": function_name,
                    "args": transformed_args
                }
            }
            
            self.logger.info(f"Created function call part for '{function_name}'")
            self.logger.debug(f"Function call part: {function_call_part}")
            
            return function_call_part
            
        except Exception as e:
            error_msg = f"Failed to create function call part: {str(e)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg) from e
    
    def safe_generate_content(self, model_name: str, contents: List[Dict[str, Any]], **kwargs) -> Any:
        """
        Safely generate content using Gemini API with proper error handling.
        
        Args:
            model_name: Name of the Gemini model to use.
            contents: List of content parts for the API call.
            **kwargs: Additional arguments for the generate_content call.
            
        Returns:
            Generated content response.
            
        Raises:
            Exception: If API call fails after processing.
        """
        try:
            # Process contents to ensure function calls are properly formatted
            processed_contents = []
            
            for content in contents:
                if isinstance(content, dict) and 'parts' in content:
                    processed_parts = []
                    
                    for part in content['parts']:
                        if isinstance(part, dict) and 'function_call' in part:
                            # This part contains a function call - ensure it's properly formatted
                            function_call = part['function_call']
                            if 'args' in function_call:
                                # Transform the args to ensure proper formatting
                                transformed_args = self.transform_function_call_args(function_call['args'])
                                processed_part = {
                                    'function_call': {
                                        'name': function_call['name'],
                                        'args': transformed_args
                                    }
                                }
                                processed_parts.append(processed_part)
                                self.logger.debug(f"Processed function call part: {processed_part}")
                            else:
                                processed_parts.append(part)
                        else:
                            processed_parts.append(part)
                    
                    processed_content = content.copy()
                    processed_content['parts'] = processed_parts
                    processed_contents.append(processed_content)
                else:
                    processed_contents.append(content)
            
            # Make the API call with processed contents
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(processed_contents, **kwargs)
            
            self.logger.info(f"Successfully generated content using model '{model_name}'")
            return response
            
        except Exception as e:
            error_msg = f"Failed to generate content: {str(e)}"
            self.logger.error(error_msg)
            self.logger.error(f"Model: {model_name}")
            self.logger.error(f"Contents: {contents}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            raise


def create_wrapper(api_key: Optional[str] = None, verbose: bool = False) -> GeminiAPIWrapper:
    """
    Convenience function to create a GeminiAPIWrapper instance.
    
    Args:
        api_key: Google API key. If None, will try to get from environment.
        verbose: Enable verbose logging.
        
    Returns:
        Configured GeminiAPIWrapper instance.
    """
    return GeminiAPIWrapper(api_key=api_key, verbose=verbose)


# Example usage and testing functions
def test_path_validation():
    """Test the path validation functionality."""
    wrapper = GeminiAPIWrapper(verbose=True)
    
    test_cases = [
        "/home/daytona/introgit_hub",
        {"path": "/home/daytona/introgit_hub"},
        Path("/home/daytona/introgit_hub"),
        "relative/path",
        {"path": "relative/path"},
    ]
    
    print("Testing path validation:")
    for test_case in test_cases:
        try:
            result = wrapper.validate_path_argument(test_case)
            print(f"✅ {test_case} -> {result}")
        except Exception as e:
            print(f"❌ {test_case} -> Error: {e}")


def test_args_transformation():
    """Test the function call arguments transformation."""
    wrapper = GeminiAPIWrapper(verbose=True)
    
    test_cases = [
        '{"path": "/home/daytona/introgit_hub"}',
        {"path": "/home/daytona/introgit_hub"},
        {"path": "/home/daytona/introgit_hub", "mode": "read"},
        '{"path": "/home/daytona/introgit_hub", "recursive": true}',
    ]
    
    print("\nTesting arguments transformation:")
    for test_case in test_cases:
        try:
            result = wrapper.transform_function_call_args(test_case)
            print(f"✅ {test_case} -> {result}")
        except Exception as e:
            print(f"❌ {test_case} -> Error: {e}")


if __name__ == "__main__":
    print("Gemini API Wrapper - Test Mode")
    print("=" * 50)
    
    test_path_validation()
    test_args_transformation()
    
    print("\n" + "=" * 50)
    print("Test completed. Check the output above for results.")


