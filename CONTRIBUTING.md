# Contributing to Chess Agent

Thank you for your interest in contributing to Chess Agent! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with the following information:

- A clear and descriptive title.
- Steps to reproduce the bug.
- Expected behavior and actual behavior.
- Any relevant logs or screenshots.

### Suggesting Enhancements

If you have an idea for an enhancement, please open an issue on GitHub with the following information:

- A clear and descriptive title.
- A detailed description of the enhancement.
- Any relevant examples or mockups.

### Pull Requests

1. **Fork the Repository**: Start by forking the repository to your GitHub account.

2. **Create a Branch**: Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**: Make your changes and ensure they are well-documented and tested.

4. **Commit Changes**: Commit your changes with a clear and descriptive commit message:
   ```bash
   git commit -m "Add your feature"
   ```

5. **Push Changes**: Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Submit a Pull Request**: Open a pull request from your fork to the main repository. Ensure your pull request includes:
   - A clear and descriptive title.
   - A detailed description of the changes.
   - Any relevant issue numbers.

7. **Review and Merge**: Once your pull request is reviewed and approved, it will be merged into the main repository.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/rishimule/chess_agent.git
   cd chess_agent
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

4. Install test dependencies:
   ```bash
   pip install -r tests/requirements.txt
   ```

5. Run the tests to ensure everything is working:
   ```bash
   PYTHONPATH=src python -m pytest tests/ -v
   ```

## Code Style

- Follow PEP 8 guidelines for Python code.
- Use meaningful variable and function names.
- Comment your code where necessary.

## License

By contributing to Chess Agent, you agree that your contributions will be licensed under the project's MIT License. 