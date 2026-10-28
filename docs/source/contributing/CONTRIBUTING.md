# Code Contribution Guidelines

This document describes the process for contributing code to pyIPCS — from forking the repository through getting your pull request merged.

Before contributing, please review the project's [Code of Conduct](https://github.com/openmainframeproject/tsc/blob/master/process/contribution_guidelines.md) and [Developer Certificate of Origin (DCO)](https://github.com/openmainframeproject/tsc/blob/master/process/contribution_guidelines.md#developer-certificate-of-origin) requirements. All contributions must include a DCO sign-off.

## Contribution Workflow

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/pyIPCS.git
cd pyIPCS
```

### 2. Set Up Your Environment

See the [Development Environment Setup](dev-setup) guide for full instructions on creating a virtual environment, installing dependencies, configuring pre-commit hooks, and setting up your Git identity for DCO sign-off.

### 3. Create a Branch

```bash
# Fetch latest changes
git fetch upstream

# Create a new branch from develop
git checkout -b feature/your-feature-name upstream/develop
```

### 4. Make Your Changes

- Write your code
- Add tests for new functionality
- Update documentation as needed — see the [Editing and Building Documentation](editing-docs) guide for how to edit source files and build a local preview
- Follow the style guidelines (see below)

### 5. Test Your Changes

See the [Running the Tests](running-tests) guide for instructions on running the test suite and available flags, and [Writing Tests](writing-tests) for markers, fixtures, and cleanup behavior.

### 6. Commit Your Changes

**Important:** All commits must include a DCO signoff.

```bash
# Stage your changes
git add .

# Commit with DCO signoff (-s flag)
git commit -s -m "Add feature: description of your changes"
```

The `-s` flag adds a "Signed-off-by" line to your commit message:

```
Add feature: description of your changes

Signed-off-by: Your Name <your.email@example.com>
```

### 7. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then create a pull request on GitHub from your branch to the `develop` branch of the main repository.

## Style Guidelines

### Python Code Style

#### Required Score

- **All code in `src/` must have a pylint score of 10.0**

```bash
# Check your code
pylint ./src
```

#### Code Formatting

We recommend using Black for consistent formatting:

```bash
# Install Black
pip install black

# Format your code
black ./src
```

#### Docstrings

- **All classes, functions, and methods must have docstrings**
- **Use Google-style docstrings**

### Documentation Style

See the [Editing and Building Documentation](editing-docs) guide for full instructions on editing source files, adding new pages, and building a local HTML preview.

#### Markdown

- Use markdownlint for consistency
- Follow the existing documentation structure
- Include code examples where appropriate

#### Spell Checking

- Use Code Spell Checker
- Add technical terms to `.cspell.json` if needed

### Required Tools

Install these VS Code extensions:

1. **markdownlint**
   - Identifier: `DavidAnson.vscode-markdownlint`

2. **Code Spell Checker**
   - Identifier: `streetsidesoftware.code-spell-checker`
