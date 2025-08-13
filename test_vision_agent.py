#!/usr/bin/env python3
"""
Vision Agent Test Runner Script
==============================

This script provides comprehensive testing of the Vision Agent library setup,
including library imports, API key configuration checks, and basic functionality
tests. It demonstrates what works without real API keys and provides guidance
for full setup.

Usage:
    python3 test_vision_agent.py

Features:
    - Library import testing
    - API key configuration validation
    - Mock functionality demonstrations
    - Environment compatibility checks
    - Comprehensive error handling and guidance
"""

import os
import sys
import traceback
from pathlib import Path
import tempfile
import json

class VisionAgentTester:
    """Comprehensive Vision Agent testing class"""

    def __init__(self):
        self.test_results = {
            'imports': {},
            'api_keys': {},
            'functionality': {},
            'environment': {},
            'overall_status': 'unknown'
        }
        self.mock_api_keys = {
            'VISION_AGENT_API_KEY': 'mock-va-key-12345',
            'ANTHROPIC_API_KEY': 'mock-anthropic-key-67890',
            'GOOGLE_API_KEY': 'mock-google-key-abcdef'
        }

    def print_header(self, title, char="="):
        """Print a formatted header"""
        print(f"\n{char * 60}")
        print(f"{title:^60}")
        print(f"{char * 60}")

    def print_section(self, title):
        """Print a section header"""
        print(f"\n{'─' * 40}")
        print(f"🔍 {title}")
        print(f"{'─' * 40}")

    def test_python_environment(self):
        """Test Python environment and basic dependencies"""
        self.print_section("Python Environment Check")

        try:
            # Python version
            python_version = sys.version
            print(f"✅ Python Version: {python_version.split()[0]}")
            self.test_results['environment']['python_version'] = python_version.split()[0]

            # Platform info
            import platform
            print(f"✅ Platform: {platform.system()} {platform.release()}")
            self.test_results['environment']['platform'] = (
                f"{platform.system()} {platform.release()}"
            )

            # Working directory
            cwd = os.getcwd()
            print(f"✅ Working Directory: {cwd}")
            self.test_results['environment']['working_directory'] = cwd

            return True

        except Exception as e:
            print(f"❌ Environment check failed: {e}")
            self.test_results['environment']['error'] = str(e)
            return False

    def test_basic_imports(self):
        """Test importing basic required libraries"""
        self.print_section("Basic Dependencies Import Test")

        basic_libs = {
            'os': 'os',
            'sys': 'sys',
            'pathlib': 'pathlib',
            'numpy': 'numpy',
            'matplotlib': 'matplotlib.pyplot',
            'PIL': 'PIL.Image',
            'requests': 'requests'
        }

        success_count = 0
        for lib_name, import_path in basic_libs.items():
            try:
                if '.' in import_path:
                    module_parts = import_path.split('.')
                    module = __import__(module_parts[0])
                    for part in module_parts[1:]:
                        module = getattr(module, part)
                else:
                    module = __import__(import_path)

                version = getattr(module, '__version__', 'unknown')
                print(f"✅ {lib_name}: {version}")
                self.test_results['imports'][lib_name] = {'status': 'success', 'version': version}
                success_count += 1

            except ImportError as e:
                print(f"❌ {lib_name}: Import failed - {e}")
                self.test_results['imports'][lib_name] = {'status': 'failed', 'error': str(e)}
            except Exception as e:
                print(f"⚠️  {lib_name}: Available but error getting version - {e}")
                self.test_results['imports'][lib_name] = {'status': 'partial', 'error': str(e)}
                success_count += 1

        print(f"\n📊 Basic Dependencies: {success_count}/{len(basic_libs)} successful")
        return success_count == len(basic_libs)

    def test_vision_agent_imports(self):
        """Test importing Vision Agent specific modules"""
        self.print_section("Vision Agent Library Import Test")

        vision_agent_modules = {
            'vision_agent': 'vision_agent',
            'vision_agent.agent': 'vision_agent.agent',
            'vision_agent.models': 'vision_agent.models',
            'vision_agent.tools': 'vision_agent.tools'
        }

        success_count = 0
        for module_name, import_path in vision_agent_modules.items():
            try:
                module = __import__(import_path, fromlist=[''])
                version = getattr(module, '__version__', 'unknown')
                print(f"✅ {module_name}: {version}")
                self.test_results['imports'][module_name] = {
                    'status': 'success', 'version': version}
                success_count += 1

            except ImportError as e:
                print(f"❌ {module_name}: Import failed - {e}")
                self.test_results['imports'][module_name] = {'status': 'failed', 'error': str(e)}

                # Provide specific guidance
                if 'libGL' in str(e):
                    print(f"   💡 OpenGL library issue - common in headless environments")
                elif 'No module named' in str(e):
                    print(f"   💡 Module not installed or installation incomplete")

            except Exception as e:
                print(f"⚠️  {module_name}: Unexpected error - {e}")
                self.test_results['imports'][module_name] = {'status': 'error', 'error': str(e)}

        print(f"\n📊 Vision Agent Modules: {success_count}/{len(vision_agent_modules)} successful")
        return success_count > 0

    def test_specific_classes(self):
        """Test importing specific Vision Agent classes"""
        self.print_section("Vision Agent Classes Import Test")

        classes_to_test = [
            ('VisionAgentCoderV2', 'vision_agent.agent', 'VisionAgentCoderV2'),
            ('AgentMessage', 'vision_agent.models', 'AgentMessage'),
        ]

        success_count = 0
        for class_name, module_path, class_attr in classes_to_test:
            try:
                module = __import__(module_path, fromlist=[class_attr])
                cls = getattr(module, class_attr)
                print(f"✅ {class_name}: Available")
                self.test_results['imports'][class_name] = {'status': 'success'}
                success_count += 1

            except ImportError as e:
                print(f"❌ {class_name}: Import failed - {e}")
                self.test_results['imports'][class_name] = {'status': 'failed', 'error': str(e)}
            except AttributeError as e:
                print(f"❌ {class_name}: Class not found - {e}")
                self.test_results['imports'][class_name] = {'status': 'failed', 'error': str(e)}
            except Exception as e:
                print(f"⚠️  {class_name}: Unexpected error - {e}")
                self.test_results['imports'][class_name] = {'status': 'error', 'error': str(e)}

        print(f"\n📊 Vision Agent Classes: {success_count}/{len(classes_to_test)} successful")
        return success_count > 0

    def check_api_keys(self):
        """Check API key configuration"""
        self.print_section("API Key Configuration Check")

        required_keys = ['VISION_AGENT_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY']

        print("Current API Key Status:")
        for key in required_keys:
            value = os.getenv(key)
            if value:
                print(f"✅ {key}: Set (length: {len(value)})")
                self.test_results['api_keys'][key] = {'status': 'set', 'length': len(value)}
            else:
                print(f"❌ {key}: Not set")
                self.test_results['api_keys'][key] = {'status': 'missing'}

        # Check .env file
        env_file = Path('.env')
        if env_file.exists():
            print(f"✅ .env file found: {env_file.absolute()}")
            self.test_results['api_keys']['env_file'] = {
                'status': 'found', 'path': str(env_file.absolute())}
        else:
            print(f"❌ .env file not found in current directory")
            self.test_results['api_keys']['env_file'] = {'status': 'missing'}

        return any(os.getenv(key) for key in required_keys)

    def test_with_mock_api_keys(self):
        """Test functionality with mock API keys"""
        self.print_section("Mock API Key Testing")

        print("Setting up mock API keys for testing...")
        original_env = {}

        # Backup original environment
        for key in self.mock_api_keys:
            original_env[key] = os.getenv(key)

        try:
            # Set mock API keys
            for key, value in self.mock_api_keys.items():
                os.environ[key] = value
                print(f"✅ Mock {key}: {value[:20]}...")

            # Test basic initialization (without actual API calls)
            success = self.test_mock_functionality()

            return success

        finally:
            # Restore original environment
            for key, original_value in original_env.items():
                if original_value is not None:
                    os.environ[key] = original_value
                elif key in os.environ:
                    del os.environ[key]
            print("🔄 Original environment restored")

    def test_mock_functionality(self):
        """Test basic functionality with mock API keys"""
        print("\n🧪 Testing basic functionality with mock API keys...")

        success_count = 0
        total_tests = 0

        # Test 1: VisionAgentCoderV2 initialization
        total_tests += 1
        try:
            from vision_agent.agent import VisionAgentCoderV2
            print("✅ VisionAgentCoderV2 import successful")

            # Try to initialize (this might fail due to API validation)
            try:
                agent = VisionAgentCoderV2(verbose=False)
                print("✅ VisionAgentCoderV2 initialization successful")
                success_count += 1
            except Exception as e:
                print(f"⚠️  VisionAgentCoderV2 initialization failed: {e}")
                print("   💡 This is expected with mock API keys")

        except Exception as e:
            print(f"❌ VisionAgentCoderV2 test failed: {e}")

        # Test 2: AgentMessage creation
        total_tests += 1
        try:
            from vision_agent.models import AgentMessage

            message = AgentMessage(
                role="user",
                content="Test message",
                media=["test.jpg"]
            )
            print("✅ AgentMessage creation successful")
            success_count += 1

        except Exception as e:
            print(f"❌ AgentMessage test failed: {e}")

        # Test 3: Tools module availability
        total_tests += 1
        try:
            import vision_agent.tools as T

            # Check if basic functions exist
            functions_to_check = ['load_image', 'save_image']
            available_functions = [f for f in functions_to_check if hasattr(T, f)]

            if available_functions:
                print(
                    f"✅ Tools module: {len(available_functions)}/"
                    f"{len(functions_to_check)} functions available")
                success_count += 1
            else:
                print("⚠️  Tools module: No expected functions found")

        except Exception as e:
            print(f"❌ Tools module test failed: {e}")

        print(f"\n📊 Mock Functionality Tests: {success_count}/{total_tests} successful")
        self.test_results['functionality']['mock_tests'] = {
            'successful': success_count,
            'total': total_tests,
            'success_rate': success_count / total_tests if total_tests > 0 else 0
        }

        return success_count > 0

    def test_sample_files(self):
        """Test availability of sample files and scripts"""
        self.print_section("Sample Files and Scripts Check")

        files_to_check = [
            ('quickstart/people.jpg', 'Sample image with people'),
            ('quickstart/landscape.jpg', 'Sample landscape image'),
            ('quickstart/source.py', 'Basic VisionAgent script'),
            ('quickstart/test_tools.py', 'Direct tools usage script'),
            ('.env', 'Environment configuration'),
            ('README.md', 'Project documentation')
        ]

        success_count = 0
        for file_path, description in files_to_check:
            path = Path(file_path)
            if path.exists():
                size = path.stat().st_size
                print(f"✅ {file_path}: {description} ({size:,} bytes)")
                success_count += 1
            else:
                print(f"❌ {file_path}: {description} - Not found")

        print(f"\n📊 Sample Files: {success_count}/{len(files_to_check)} found")
        self.test_results['functionality']['sample_files'] = {
            'found': success_count,
            'total': len(files_to_check)
        }

        return success_count > len(files_to_check) // 2

    def run_integration_test(self):
        """Run a simple integration test"""
        self.print_section("Integration Test")

        print("🧪 Running integration test with available components...")

        try:
            # Test matplotlib visualization (should work)
            import matplotlib
            matplotlib.use('Agg')  # Non-interactive backend
            import matplotlib.pyplot as plt
            import numpy as np

            # Create a simple test plot
            fig, ax = plt.subplots(figsize=(6, 4))
            x = np.linspace(0, 10, 100)
            y = np.sin(x)
            ax.plot(x, y, label='sin(x)')
            ax.set_title('Vision Agent Test - Matplotlib Integration')
            ax.legend()

            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                plt.savefig(tmp.name, dpi=100, bbox_inches='tight')
                test_plot_path = tmp.name

            plt.close()

            # Check if file was created
            if Path(test_plot_path).exists():
                size = Path(test_plot_path).stat().st_size
                print(f"✅ Matplotlib integration test successful ({size:,} bytes)")

                # Clean up
                Path(test_plot_path).unlink()

                self.test_results['functionality']['integration_test'] = {'status': 'success'}
                return True
            else:
                print("❌ Matplotlib integration test failed - file not created")
                self.test_results['functionality']['integration_test'] = {
                    'status': 'failed', 'error': 'File not created'}
                return False

        except Exception as e:
            print(f"❌ Integration test failed: {e}")
            self.test_results['functionality']['integration_test'] = {
                'status': 'failed', 'error': str(e)}
            return False

    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        self.print_header("TEST SUMMARY REPORT")

        # Calculate overall scores
        import_success = sum(1 for result in self.test_results['imports'].values()
                           if result.get('status') == 'success')
        import_total = len(self.test_results['imports'])

        api_keys_set = sum(1 for result in self.test_results['api_keys'].values()
                          if result.get('status') == 'set')
        api_keys_total = len([k for k in self.test_results['api_keys'].keys() if k != 'env_file'])

        functionality_tests = self.test_results['functionality'].get('mock_tests', {})
        func_success = functionality_tests.get('successful', 0)
        func_total = functionality_tests.get('total', 0)

        print(f"📊 OVERALL RESULTS:")
        print(f"   • Imports: {import_success}/{import_total} successful")
        print(f"   • API Keys: {api_keys_set}/{api_keys_total} configured")
        print(f"   • Functionality: {func_success}/{func_total} tests passed")

        # Determine overall status
        if import_success >= import_total * 0.7:
            if api_keys_set > 0:
                self.test_results['overall_status'] = 'ready'
                print(f"\n🎉 STATUS: READY FOR USE")
                print(f"   Vision Agent is properly installed and configured!")
            else:
                self.test_results['overall_status'] = 'needs_api_keys'
                print(f"\n⚠️  STATUS: NEEDS API KEYS")
                print(f"   Vision Agent is installed but requires API key configuration.")
        else:
            self.test_results['overall_status'] = 'needs_setup'
            print(f"\n❌ STATUS: NEEDS SETUP")
            print(f"   Vision Agent installation is incomplete or has issues.")

        # Provide next steps
        print(f"\n🎯 NEXT STEPS:")
        if self.test_results['overall_status'] == 'ready':
            print(f"   1. Run example scripts in the quickstart/ directory")
            print(f"   2. Try different prompts and images")
            print(f"   3. Explore advanced features")
        elif self.test_results['overall_status'] == 'needs_api_keys':
            print(f"   1. Get API keys from the required providers")
            print(f"   2. Update the .env file with your actual API keys")
            print(f"   3. Load environment variables: export $(cat .env | grep -v '^#' | xargs)")
            print(f"   4. Run the example scripts")
        else:
            print(f"   1. Check installation issues above")
            print(f"   2. Reinstall missing dependencies")
            print(f"   3. Verify system requirements")
            print(f"   4. Run this test again")

        # Save results to file
        self.save_test_results()

    def save_test_results(self):
        """Save test results to a JSON file"""
        try:
            results_file = Path('vision_agent_test_results.json')
            with open(results_file, 'w') as f:
                json.dump(self.test_results, f, indent=2, default=str)
            print(f"\n💾 Test results saved to: {results_file}")
        except Exception as e:
            print(f"\n⚠️  Could not save test results: {e}")

    def run_all_tests(self):
        """Run all tests in sequence"""
        self.print_header("VISION AGENT COMPREHENSIVE TEST SUITE")

        print("🚀 Starting comprehensive Vision Agent testing...")
        print("This will test installation, configuration, and basic functionality.")

        # Run all test categories
        tests = [
            ("Python Environment", self.test_python_environment),
            ("Basic Dependencies", self.test_basic_imports),
            ("Vision Agent Imports", self.test_vision_agent_imports),
            ("Vision Agent Classes", self.test_specific_classes),
            ("API Key Configuration", self.check_api_keys),
            ("Mock API Key Testing", self.test_with_mock_api_keys),
            ("Sample Files", self.test_sample_files),
            ("Integration Test", self.run_integration_test)
        ]

        results = {}
        for test_name, test_func in tests:
            try:
                print(f"\n🔄 Running: {test_name}")
                result = test_func()
                results[test_name] = result
                status = "✅ PASSED" if result else "❌ FAILED"
                print(f"   Result: {status}")
            except Exception as e:
                print(f"   Result: ⚠️  ERROR - {e}")
                results[test_name] = False

        # Generate final report
        self.generate_summary_report()

        return results

def main():
    """Main function to run the Vision Agent test suite"""
    tester = VisionAgentTester()

    try:
        results = tester.run_all_tests()

        # Exit with appropriate code
        success_count = sum(1 for result in results.values() if result)
        total_count = len(results)

        if success_count >= total_count * 0.7:
            print(
                f"\n🎉 Testing completed successfully! ({success_count}/{total_count} tests passed)")
            sys.exit(0)
        else:
            print(
                f"\n⚠️  Testing completed with issues. ({success_count}/{total_count} tests passed)")
            sys.exit(1)

    except KeyboardInterrupt:
        print(f"\n\n⚠️  Testing interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Testing failed with unexpected error: {e}")
        print(f"Error details: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()


