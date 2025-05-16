# Contributing To pyIPCS

- __[Setting Up Your Development Environment](#setting-up-your-development-environment)__
- __[How to Submit Your Code Changes](#how-to-submit-your-code-changes)__
- __[Branch Naming Conventions](#branch-naming-conventions)__
- __[Running and Creating Tests](#running-and-creating-tests)__
- __[Style Guidelines](#style-guidelines)__

---
---

## *All code contributed must be made under an Apache 2 license.*

---
---

## Setting Up Your Development Environment

- __[Back to Top](#contributing-to-pyipcs)__

---

- __Create a Fork of pyIPCS__
  - __[Fork a repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo?tool=cli)__
    - *Has options for forking with Mac, Windows, and Linux*
    - *Has options for forking with GitHub CLI, Desktop, and Web browser*
- __[Getting Started](./GETTING_STARTED.md)__
  - Make sure you have followed the prerequisite and install steps in Getting Started
- __Run pyIPCS Devlopment Setup Script__
  - Create a Python virtual enviroment (Optional)
  - pyIPCS Development Setup script: `dev/setup.sh`
    - Make script executable and run script
- __Within your fork open up a [Development Branch](#development-branch-naming-conventions) to begin devlopment__

---
---

## How to Submit Your Code Changes

- __[Back to Top](#contributing-to-pyipcs)__

---

- __*All contributions must be accompanied by a [Developer Certification of Origin (DCO) signoff](https://github.com/openmainframeproject/tsc/blob/master/process/contribution_guidelines.md#developer-certificate-of-origin).*__
  - __*You can include this automatically when you commit a change to your local git repository using `git commit -s`.*__

<br>

- Switch to your __[Development Branch](#development-branch-naming-conventions)__ on your fork

```bash
git checkout <development-branch>
```

- Develop in your __[Development Branch](#development-branch-naming-conventions)__ on your fork

- Fetch the latest from upstream

```bash
git fetch upstream
```

- Rebase onto the develop branch

```bash
git rebase upstream/develop
```

- Open a pull request from that branch to the develop branch in the main repository

---
---

## Branch Naming Conventions

- __[Back to Top](#contributing-to-pyipcs)__

---

### Development Branch Naming Conventions

- `update/...` *(Branch where new functionality or enhancements are being developed. Could include bug fixes or test development.)*
- `bug/...` *(Branch where specifically one or more bugs are being fixed. Could include test development)*
- `doc/...` *(Branch where non-code related updates are being made)*
- `exp/...` *(Throwaway branch for experimentation of new tools and functionality)*

### pyIPCS Stable and Latest Builds Branches

- `main` *(Stable - Current version of pyIPCS)*
- `develop/...` *(Latest - Branch for development of new versions of pyIPCS)*

---
---

## Running and Creating Tests

- __[Back to Top](#contributing-to-pyipcs)__

---

- __How to run tests: [Tests README](./src/tests/README.md)__
- __[pytest Documentation](https://docs.pytest.org/en/stable/contents.html)__
- __While creating tests, please refer to the following files for various settings, fixtures, and helpful mock Subcmd functions/objects to use in your tests:__
  - __`src/tests/conftest.py`__
  - __`src/tests/mock_subcmd.py`__
  - __`src/tests/mock_subcmd_jcl.py`__
- __pyIPCS tests are located in the [src/tests](./src/tests/) folder__

---
---

## Style Guidelines

- __[Back to Top](#contributing-to-pyipcs)__
- __[Markdown Style Guidelines](#markdown-style-guidelines)__
- __[Code Style Guidelines](#code-style-guidelines)__

---

### Markdown Style Guidelines

- __Markdown lint__
  - [markdown lint](https://github.ibm.com/zosdev/zai-devops/wiki/wiki-lints) or its [VSCode plugin](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint) *(Recommended)* or its [markdownlint-cli2 cli](https://www.npmjs.com/package/markdownlint-cli2).
  - __*All Markdown lint warnings must be addressed*__

<br>

- __Code Spell Checker *(Recommended)*__
  - To check for spelling warnings

<br>

- __VSCode Plugins__

```markdown
Name: markdownlint
Id: DavidAnson.vscode-markdownlint
Description: Markdown linting and style checking for Visual Studio Code
Version: 0.54.0
Publisher: David Anson
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint

Name: Code Spell Checker
Id: streetsidesoftware.code-spell-checker
Description: Spelling checker for source code
Version: 3.0.1
Publisher: Street Side Software
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker
```

### Code Style Guidelines

- We use `pylint` and `black` for style checking

<br>

- __*Before submitting code please make sure:*__
  - *All contributions in `src/` have a `pylint` score of __10__*.
  - All pyIPCS classes, functions, and tests include a corresponding docstring for explanation.
    - __pyIPCS Classes:__ Should include a description of the class, an Attributes section, and a Methods section.
    - __pyIPCS Functions/Methods:__ Should include a description of the function/method, an Args section, and a Returns section.
    - __Test Modules:__ Should include a description of the test module and a Tests section corresponding to the test within the class
    - __Test Functions:__ Should include a description of the test and a Object or Function section.
  - __*Refer to examples in the repo to correctly format docstrings*__
