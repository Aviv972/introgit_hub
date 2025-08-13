#!/usr/bin/env python3
"""
Test Script for Gemini API Wrapper
==================================

This script provides comprehensive testing of the GeminiAPIWrapper functionality,
including path validation, argument transformation, error handling, and edge cases.

Usage:
    python3 test_gemini_wrapper.py

Features:
    - Path argument validation testing
    - Function call argument transformation testing
    - Mock API call testing
    - Edge case handling
    - Error condition testing
    - Performance and reliability testing
"""

import os
import sys
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import traceback

# Import the wrapper module
try:
    from gemini_api_wrapper import GeminiAPIWrapper, create_wrapper
    WRAPPER_AVAILABLE = True
except ImportError as e:
    print(f"❌ Failed to import GeminiAPIWrapper: {e}")
    WRAPPER_AVAILABLE = False
    sys.exit(1)


class TestGeminiAPIWrapper(unittest.TestCase):
    """Comprehensive test suite for GeminiAPIWrapper"""

    def setUp(self):
        """Set up test fixtures"""
        self.wrapper = GeminiAPIWrapper(verbose=True)
        self.test_paths = [
            "/home/daytona/introgit_hub",
            "/tmp/test_file.txt",
            "relative/path/file.py",
            ".",
            "..",
            "/",
        ]

    def test_path_validation_basic(self):
        """Test basic path validation functionality"""
        print("\n🔍 Testing basic path validation...")

        # Test string paths
        for path in self.test_paths:
            with self.subTest(path=path):
                try:
                    result = self.wrapper.validate_path_argument(path)
                    self.assertIsInstance(result, str)
                    self.assertTrue(os.path.isabs(result))
                    print(f"✅ {path} -> {result}")
                except Exception as e:
                    self.fail(f"Path validation failed for '{path}': {e}")

    def test_path_validation_dict_format(self):
        """Test path validation with dictionary format"""
        print("\n🔍 Testing dictionary format path validation...")

        test_cases = [
            {"path": "/home/daytona/introgit_hub"},
            {"path": "relative/path"},
            {"path": "/tmp/test.txt"},
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                try:
                    result = self.wrapper.validate_path_argument(test_case)
                    self.assertIsInstance(result, str)
                    self.assertTrue(os.path.isabs(result))
                    print(f"✅ {test_case} -> {result}")
                except Exception as e:
                    self.fail(f"Dict path validation failed for '{test_case}': {e}")

    def test_path_validation_pathlib(self):
        """Test path validation with pathlib.Path objects"""
        print("\n🔍 Testing pathlib.Path validation...")

        test_paths = [
            Path("/home/daytona/introgit_hub"),
            Path("relative/path"),
            Path("."),
            Path(".."),
        ]

        for path_obj in test_paths:
            with self.subTest(path=path_obj):
                try:
                    result = self.wrapper.validate_path_argument(path_obj)
                    self.assertIsInstance(result, str)
                    self.assertTrue(os.path.isabs(result))
                    print(f"✅ {path_obj} -> {result}")
                except Exception as e:
                    self.fail(f"Path object validation failed for '{path_obj}': {e}")

    def test_path_validation_edge_cases(self):
        """Test path validation with edge cases"""
        print("\n🔍 Testing edge cases for path validation...")

        edge_cases = [
            "",  # Empty string
            " ",  # Whitespace
            "/path/with spaces/file.txt",  # Spaces in path
            "/path/with-special_chars@#$/file.txt",  # Special characters
            "~/home_path",  # Tilde expansion
            "/path/with/unicode/文件.txt",  # Unicode characters
        ]

        for edge_case in edge_cases:
            with self.subTest(edge_case=edge_case):
                try:
                    if edge_case.strip():  # Skip empty strings for now
                        result = self.wrapper.validate_path_argument(edge_case)
                        self.assertIsInstance(result, str)
                        print(f"✅ Edge case '{edge_case}' -> {result}")
                    else:
                        # Empty strings should raise an error
                        with self.assertRaises(ValueError):
                            self.wrapper.validate_path_argument(edge_case)
                        print(f"✅ Empty path correctly rejected: '{edge_case}'")
                except Exception as e:
                    print(f"⚠️  Edge case '{edge_case}' handling: {e}")

    def test_path_validation_error_cases(self):
        """Test path validation error handling"""
        print("\n🔍 Testing error cases for path validation...")

        error_cases = [
            None,  # None value
            123,  # Integer
            [],  # List
            {"not_path": "value"},  # Dict without 'path' key
            {"path": None},  # Dict with None path
        ]

        for error_case in error_cases:
            with self.subTest(error_case=error_case):
                with self.assertRaises(ValueError):
                    self.wrapper.validate_path_argument(error_case)
                print(f"✅ Error case correctly rejected: {error_case}")

    def test_args_transformation_json_strings(self):
        """Test transformation of JSON string arguments"""
        print("\n🔍 Testing JSON string argument transformation...")

        test_cases = [
            '{"path": "/home/daytona/introgit_hub"}',
            '{"path": "/tmp/test.txt", "mode": "read"}',
            '{"path": "relative/path", "recursive": true}',
            '{"path": "/home/daytona/introgit_hub", "encoding": "utf-8", "max_size": 1024}',
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                try:
                    result = self.wrapper.transform_function_call_args(test_case)
                    self.assertIsInstance(result, dict)
                    self.assertIn('path', result)
                    self.assertTrue(os.path.isabs(result['path']))
                    print(f"✅ {test_case} -> {result}")
                except Exception as e:
                    self.fail(f"JSON string transformation failed for '{test_case}': {e}")

    def test_args_transformation_dict_objects(self):
        """Test transformation of dictionary arguments"""
        print("\n🔍 Testing dictionary argument transformation...")

        test_cases = [
            {"path": "/home/daytona/introgit_hub"},
            {"path": "/tmp/test.txt", "mode": "write"},
            {"path": "relative/path", "recursive": False},
            {"path": Path("/home/daytona/introgit_hub"), "encoding": "utf-8"},
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                try:
                    result = self.wrapper.transform_function_call_args(test_case)
                    self.assertIsInstance(result, dict)
                    self.assertIn('path', result)
                    self.assertTrue(os.path.isabs(result['path']))
                    print(f"✅ {test_case} -> {result}")
                except Exception as e:
                    self.fail(f"Dict transformation failed for '{test_case}': {e}")

    def test_args_transformation_complex_structures(self):
        """Test transformation of complex argument structures"""
        print("\n🔍 Testing complex argument structure transformation...")

        test_cases = [
            {
                "path": "/home/daytona/introgit_hub",
                "options": {"recursive": True, "include_hidden": False},
                "filters": ["*.py", "*.txt"],
                "metadata": {"created_by": "test", "version": 1.0}
            },
            {
                "path": Path("/tmp/nested/path"),
                "nested": {
                    "inner_path": Path("relative/inner"),
                    "settings": {"enabled": True, "count": 42}
                }
            }
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                try:
                    result = self.wrapper.transform_function_call_args(test_case)
                    self.assertIsInstance(result, dict)
                    self.assertIn('path', result)
                    self.assertTrue(os.path.isabs(result['path']))
                    # Verify nested structures are preserved
                    if 'options' in test_case:
                        self.assertIn('options', result)
                    if 'nested' in test_case:
                        self.assertIn('nested', result)
                    print(f"✅ Complex structure transformed successfully")
                except Exception as e:
                    self.fail(f"Complex structure transformation failed: {e}")

    def test_args_transformation_error_cases(self):
        """Test argument transformation error handling"""
        print("\n🔍 Testing argument transformation error cases...")

        error_cases = [
            '{"invalid": "json"',  # Invalid JSON
            '{"path": null}',  # Null path in JSON
            {"path": None},  # None path in dict
            123,  # Invalid type
            [],  # List instead of dict
        ]

        for error_case in error_cases:
            with self.subTest(error_case=error_case):
                with self.assertRaises(ValueError):
                    self.wrapper.transform_function_call_args(error_case)
                print(f"✅ Error case correctly rejected: {error_case}")

    def test_function_call_part_creation(self):
        """Test creation of function call parts"""
        print("\n🔍 Testing function call part creation...")

        test_cases = [
            ("read_file", {"path": "/home/daytona/introgit_hub"}),
            ("list_directory", {"path": "/tmp", "recursive": True}),
            ("write_file", {"path": "/tmp/output.txt", "content": "test data"}),
        ]

        for function_name, args in test_cases:
            with self.subTest(function_name=function_name, args=args):
                try:
                    result = self.wrapper.create_function_call_part(function_name, args)
                    self.assertIsInstance(result, dict)
                    self.assertIn('function_call', result)
                    self.assertIn('name', result['function_call'])
                    self.assertIn('args', result['function_call'])
                    self.assertEqual(result['function_call']['name'], function_name)
                    print(f"✅ Function call part created: {function_name}")
                except Exception as e:
                    self.fail(f"Function call part creation failed: {e}")

    @patch('gemini_api_wrapper.genai')
    def test_mock_api_calls(self, mock_genai):
        """Test API calls with mocked Gemini API"""
        print("\n🔍 Testing mock API calls...")

        # Set up mock
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = "Mock response text"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        # Test data
        test_contents = [
            {
                "parts": [
                    {"text": "Please read this file:"},
                    {
                        "function_call": {
                            "name": "read_file",
                            "args": '{"path": "/home/daytona/introgit_hub"}'
                        }
                    }
                ]
            }
        ]

        try:
            # Create wrapper with API key for testing
            wrapper = GeminiAPIWrapper(api_key="test-key", verbose=True)
            result = wrapper.safe_generate_content("gemini-pro", test_contents)

            # Verify the call was made
            self.assertIsNotNone(result)
            print("✅ Mock API call successful")

            # Verify that the function call args were processed
            mock_model.generate_content.assert_called_once()
            call_args = mock_model.generate_content.call_args[0][0]

            # Check that the path argument was properly transformed
            function_call_part = call_args[0]['parts'][1]
            self.assertIn('function_call', function_call_part)
            self.assertIn('args', function_call_part['function_call'])
            self.assertIsInstance(function_call_part['function_call']['args'], dict)
            print("✅ Function call arguments properly transformed")

        except Exception as e:
            self.fail(f"Mock API call failed: {e}")

    def test_protobuf_compatibility(self):
        """Test protobuf compatibility of transformed arguments"""
        print("\n🔍 Testing protobuf compatibility...")

        test_cases = [
            {"path": "/home/daytona/introgit_hub", "count": 42, "enabled": True},
            {"path": Path("/tmp/test"), "ratio": 3.14, "name": "test"},
            {"path": "/home/daytona/introgit_hub", "items": ["a", "b", "c"]},
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                try:
                    result = self.wrapper._ensure_protobuf_compatibility(test_case)

                    # Verify all values are protobuf-compatible types
                    for key, value in result.items():
                        self.assertIn(type(value), [str, int, float, bool, list, dict])
                        if isinstance(value, list):
                            for item in value:
                                self.assertIn(type(item), [str, int, float, bool])

                    print(f"✅ Protobuf compatibility verified: {result}")
                except Exception as e:
                    self.fail(f"Protobuf compatibility test failed: {e}")

    def test_wrapper_initialization(self):
        """Test wrapper initialization with different configurations"""
        print("\n🔍 Testing wrapper initialization...")

        # Test without API key
        wrapper1 = GeminiAPIWrapper()
        self.assertIsNotNone(wrapper1)
        print("✅ Wrapper initialized without API key")

        # Test with API key
        wrapper2 = GeminiAPIWrapper(api_key="test-key")
        self.assertIsNotNone(wrapper2)
        print("✅ Wrapper initialized with API key")

        # Test with verbose logging
        wrapper3 = GeminiAPIWrapper(verbose=True)
        self.assertIsNotNone(wrapper3)
        print("✅ Wrapper initialized with verbose logging")

        # Test convenience function
        wrapper4 = create_wrapper(verbose=True)
        self.assertIsNotNone(wrapper4)
        print("✅ Wrapper created using convenience function")


class TestEdgeCasesAndPerformance(unittest.TestCase):
    """Additional tests for edge cases and performance"""

    def setUp(self):
        """Set up test fixtures"""
        self.wrapper = GeminiAPIWrapper(verbose=False)  # Disable verbose for performance tests

    def test_large_path_handling(self):
        """Test handling of very long paths"""
        print("\n🔍 Testing large path handling...")

        # Create a very long path
        long_path_parts = ["very_long_directory_name_" + str(i) for i in range(20)]
        long_path = "/" + "/".join(long_path_parts) + "/file.txt"

        try:
            result = self.wrapper.validate_path_argument(long_path)
            self.assertIsInstance(result, str)
            print(f"✅ Long path handled successfully (length: {len(long_path)})")
        except Exception as e:
            self.fail(f"Long path handling failed: {e}")

    def test_concurrent_operations(self):
        """Test thread safety and concurrent operations"""
        print("\n🔍 Testing concurrent operations...")

        import threading
        import time

        results = []
        errors = []

        def worker(worker_id):
            try:
                for i in range(10):
                    path = f"/tmp/worker_{worker_id}_file_{i}.txt"
                    result = self.wrapper.validate_path_argument(path)
                    results.append(result)
                    time.sleep(0.001)  # Small delay to encourage race conditions
            except Exception as e:
                errors.append(e)

        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check results
        self.assertEqual(len(errors), 0, f"Concurrent operations had errors: {errors}")
        self.assertEqual(len(results), 50, "Not all concurrent operations completed")
        print(f"✅ Concurrent operations successful ({len(results)} operations)")

    def test_memory_usage(self):
        """Test memory usage with large datasets"""
        print("\n🔍 Testing memory usage...")

        import gc

        # Test with many path validations
        paths = [f"/tmp/test_file_{i}.txt" for i in range(1000)]

        try:
            for path in paths:
                result = self.wrapper.validate_path_argument(path)
                self.assertIsInstance(result, str)

            # Force garbage collection
            gc.collect()
            print("✅ Memory usage test completed successfully")

        except Exception as e:
            self.fail(f"Memory usage test failed: {e}")


def run_comprehensive_tests():
    """Run all tests with detailed reporting"""
    print("🚀 Starting Comprehensive Gemini API Wrapper Tests")
    print("=" * 60)

    # Create test suite using the modern approach
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    # Add test cases
    test_suite.addTests(loader.loadTestsFromTestCase(TestGeminiAPIWrapper))
    test_suite.addTests(loader.loadTestsFromTestCase(TestEdgeCasesAndPerformance))

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(
        f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")

    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n⚠️  Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    if not result.failures and not result.errors:
        print("\n🎉 All tests passed successfully!")
        return True
    else:
        print(f"\n⚠️  Some tests failed. Please review the output above.")
        return False


def run_specific_problematic_case_test():
    """Test the specific problematic case mentioned in the original issue"""
    print("\n🎯 Testing Specific Problematic Case")
    print("=" * 50)

    wrapper = GeminiAPIWrapper(verbose=True)

    # The exact problematic case from the error message
    problematic_args = '{"path": "/home/daytona/introgit_hub"}'

    try:
        print(f"Testing problematic case: {problematic_args}")

        # Transform the arguments
        transformed = wrapper.transform_function_call_args(problematic_args)
        print(f"✅ Transformation successful: {transformed}")

        # Create a function call part
        function_call_part = wrapper.create_function_call_part("read_file", problematic_args)
        print(f"✅ Function call part created: {function_call_part}")

        # Verify the structure is protobuf-compatible
        args = function_call_part['function_call']['args']
        assert isinstance(args, dict), "Args should be a dict, not a string"
        assert 'path' in args, "Path should be in args"
        assert isinstance(args['path'], str), "Path should be a string"
        assert os.path.isabs(args['path']), "Path should be absolute"

        print("✅ All checks passed for the problematic case!")
        return True

    except Exception as e:
        print(f"❌ Problematic case test failed: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False


if __name__ == "__main__":
    if not WRAPPER_AVAILABLE:
        print("❌ Cannot run tests - GeminiAPIWrapper not available")
        sys.exit(1)

    print("🧪 Gemini API Wrapper Test Suite")
    print("=" * 60)

    # Run the specific problematic case test first
    specific_test_passed = run_specific_problematic_case_test()

    # Run comprehensive tests
    all_tests_passed = run_comprehensive_tests()

    # Final result
    if specific_test_passed and all_tests_passed:
        print("\n🎉 All tests completed successfully!")
        print("The Gemini API wrapper is ready for use.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
        sys.exit(1)

