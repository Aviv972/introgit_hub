<general_rules>
- **Python Version Requirement**: This project requires Python 3.9 or higher. Always verify the Python version before development.
- **API Key Configuration**: Before any development work, configure the required API keys in a `.env` file in the root directory. Three API keys are required: VISION_AGENT_API_KEY, ANTHROPIC_API_KEY, and GOOGLE_API_KEY.
- **Installation Verification**: Always run `python3 test_import.py` before starting development to verify that all dependencies are properly installed and importable.
- **Headless Environment Support**: When working in headless environments, use `matplotlib.use('Agg')` at the beginning of scripts to avoid display-related errors.
- **Internet Connectivity**: Ensure internet connectivity is available as the Vision Agent library requires API calls to external services for full functionality.
- **Environment Variables**: Load environment variables from the `.env` file using `export $(cat .env | grep -v '^#' | xargs)` or similar methods before running scripts that require API access.
</general_rules>

<repository_structure>
This repository follows a flat project structure designed for Vision Agent library exploration:

- **Root Level Files**:
  - `README.md`: Primary documentation with setup instructions and usage examples
  - `test_import.py`: Installation verification script that tests all dependency imports
  - `hello.html`: Simple HTML file (appears to be a basic test file)

- **quickstart/ Directory**: Contains sample images for testing Vision Agent functionality:
  - `landscape.jpg` and `people.jpg`: Test images for computer vision tasks

- **Referenced but Missing Files**: 
  - `test_vision_agent.py`: Mentioned in documentation but not yet created - should contain comprehensive Vision Agent functionality tests
  - `.env`: API keys configuration file (template referenced in README)

The project is structured as an exploration/demonstration repository rather than a production application, focusing on Vision Agent capabilities including image analysis, object detection, and AI-driven code generation.
</repository_structure>

<dependencies_and_installation>
**Core Dependencies**:
- `vision-agent` (v1.1.19): Main library for computer vision and AI code generation
- `matplotlib`: For image processing and visualization
- `numpy`: Numerical computing support
- `anthropic`: Claude API integration

**Installation Notes**:
- No `requirements.txt` file exists - dependencies must be installed manually
- Python 3.9+ is required for compatibility
- Some dependencies may have display/OpenGL requirements that can cause issues in headless environments
- Installation verification is handled through the `test_import.py` script rather than traditional package management

**Manual Installation Process**:
1. Install Python 3.9 or higher
2. Install dependencies individually: `pip install vision-agent matplotlib numpy anthropic`
3. Run `python3 test_import.py` to verify successful installation
4. Configure API keys in `.env` file for full functionality

Note: The project intentionally lacks formal dependency management files, requiring manual setup as part of the exploration process.
</dependencies_and_installation>

<testing_instructions>
**Testing Framework**: No formal testing framework (pytest, unittest) is configured. Testing is handled through custom verification scripts.

**Primary Testing Tool**:
- `test_import.py`: Verifies that all required dependencies can be imported successfully and displays version information. This should be run before any development work.

**Testing Approach**:
- Import verification testing for all core dependencies
- Environment variable checking for API key configuration
- Basic functionality validation for vision-agent modules
- Manual testing using sample images in the `quickstart/` directory

**Missing Test Infrastructure**:
- `test_vision_agent.py`: Referenced in documentation but not yet created. This should be developed to provide comprehensive testing of Vision Agent functionality including code generation, object detection, and image analysis features.

**Running Tests**:
- Execute `python3 test_import.py` to verify installation and basic imports
- Test scripts may require API keys to be configured for full functionality testing
- Use sample images from `quickstart/` directory for manual vision testing

The testing strategy focuses on verification and exploration rather than comprehensive unit testing, reflecting the project's nature as a library exploration tool.
</testing_instructions>

<pull_request_formatting>
</pull_request_formatting>
