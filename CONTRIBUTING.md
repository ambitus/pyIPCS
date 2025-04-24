# Contributing To pyIPCS

- __[Getting Started](#getting-started)__
- __[Creating a Fork of pyIPCS](#creating-a-fork-of-pyipcs)__
- __[How to Submit Your Code Changes](#how-to-submit-your-code-changes)__
- __[Branch Naming Conventions](#branch-naming-conventions)__
- __[Running and Creating Tests](#running-and-creating-tests)__
- __[Style Guidelines](#style-guidelines)__

---
---

## *All code contributed must be made under an Apache 2 license.*

---
---

## [Getting Started](./GETTING_STARTED.md)

- __[Back to Top](#contributing-to-pyipcs)__

---

- Make sure you have followed the prerequisite and install steps in [Getting Started](./GETTING_STARTED.md) before contributing

---
---

## Creating a Fork of pyIPCS

- __[Back to Top](#contributing-to-pyipcs)__

---

- *In order to contribute code to pyIPCS, you must create a fork of the repository*
- __[Fork a repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo?tool=cli)__
  - *Has options for forking with Mac, Windows, and Linux*
  - *Has options for forking with GitHub CLI, Desktop, and Web browser*

---
---

## How to Submit Your Code Changes

- __[Back to Top](#contributing-to-pyipcs)__

---

- __*All contributions must be accompanied by a [Developer Certification of Origin (DCO) signoff](https://github.com/openmainframeproject/tsc/blob/master/process/contribution_guidelines.md#developer-certificate-of-origin).*__
  - __*You can include this automatically when you commit a change to your local git repository using `git commit -s`.*__

<br>

- __*The below steps will guide you through submission of your code changes from your [Development Branch](#development-branch-naming-conventions) on your fork, to to the appropriate [Version Branch](#pyipcs-version-branch-naming-conventions) in the main repository*__

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

- Rebase onto the target version branch from the main repository

```bash
git rebase upstream/<version-branch>
```

- Open a pull request from that branch to the appropriate __[Version Branch](#pyipcs-version-branch-naming-conventions)__ in the main repository

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

### pyIPCS Version Branch Naming Conventions

- `main` *(Current version of pyIPCS)*
- `release/...` *(Branch for development of new versions of pyIPCS)*

---
---

## Running and Creating Tests

- __[Back to Top](#contributing-to-pyipcs)__

---

- __How to run tests: [Tests README](./src/tests/README.md)__

<br>

- __[pytest Documentation](https://docs.pytest.org/en/stable/contents.html)__

<br>

- __While creating tests, please refer to the following files for various settings, fixtures, and helpful mock Subcmd functions/objects to use in your tests:__
  - __`src/tests/conftest.py`__
  - __`src/tests/mock_subcmd.py`__
  - __`src/tests/mock_subcmd_jcl.py`__

<br>

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
