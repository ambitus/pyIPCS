# Contributing To pyIPCS

- **[Setting Up Your Development Environment](#setting-up-your-development-environment)**

- **[How to Submit Your Code Changes](#how-to-submit-your-code-changes)**

- **[Branch Naming Conventions](#branch-naming-conventions)**

- **[Running and Creating Tests](#running-and-creating-tests)**

- **[Style Guidelines](#style-guidelines)**

---
---

## *All code contributed must be made under an Apache 2 license.*

---
---

## Setting Up Your Development Environment

- **[Back to Top](#contributing-to-pyipcs)**

---

- **Create a Fork of pyIPCS**
  - **[Fork a repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo?tool=cli)**
    - *Has options for forking with Mac, Windows, and Linux*
    - *Has options for forking with GitHub CLI, Desktop, and Web browser*

- **[Getting Started](./GETTING_STARTED.md)**
  - Make sure you have followed the prerequisite and install steps in Getting Started

- **Run pyIPCS Development Setup Scripts**
  - Create a Python virtual environment (Optional)
  - ***Make setup scripts executable and run scripts***
    - pyIPCS Install Dependencies Setup script: `./dev/install_setup.sh`
    - DCO Setup script: `./dev/dco_setup.sh "Your Full Name" "your_public_github@email.com"`
    - Add pyIPCS Upstream Setup script: `./dev/upstream_setup.sh`

- **Within your fork open up a [Development Branch](#development-branch-naming-conventions) to begin development**

---
---

## How to Submit Your Code Changes

- **[Back to Top](#contributing-to-pyipcs)**

---

- ***All contributions must be accompanied by a [Developer Certification of Origin (DCO) signoff](https://github.com/openmainframeproject/tsc/blob/master/process/contribution_guidelines.md#developer-certificate-of-origin).***
  - ***You can include this automatically when you commit a change to your local git repository using `git commit -s`.***

<br>

- Switch to your **[Development Branch](#development-branch-naming-conventions)** on your fork

```bash
git checkout <development-branch>
```

- Develop in your **[Development Branch](#development-branch-naming-conventions)** on your fork

- Fetch the latest from upstream

```bash
git fetch upstream
```

- Merge from the develop branch

```bash
git merge upstream/develop
```

- Open a pull request from that branch to the develop branch in the main repository

---
---

## Branch Naming Conventions

- **[Back to Top](#contributing-to-pyipcs)**

---

### Development Branch Naming Conventions

- `update/...` *(Branch where new functionality or enhancements are being developed. Could include bug fixes or test development.)*
- `doc/...` *(Branch where non-code related updates are being made)*
- `exp/...` *(Throwaway branch for experimentation of new tools and functionality)*

### pyIPCS Stable and Latest Builds Branches

- `main` *(Stable - Current version of pyIPCS)*
- `develop/...` *(Latest - Branch for development of new versions of pyIPCS)*

---
---

## Running and Creating Tests

- **[Back to Top](#contributing-to-pyipcs)**

---

- **How to run tests: [Tests README](./src/tests/README.md)**

- **[pytest Documentation](https://docs.pytest.org/en/stable/contents.html)**

- **While creating tests, please refer to the following files for various settings, fixtures, and helpful mock Subcmd functions/objects to use in your tests:**
  - **`src/tests/conftest.py`**
  - **`src/tests/mock_subcmd.py`**
  - **`src/tests/mock_subcmd_jcl.py`**

- **pyIPCS tests are located in the [src/tests](./src/tests/) folder**

---
---

## Style Guidelines

- **[Back to Top](#contributing-to-pyipcs)**
- **[Markdown Style Guidelines](#markdown-style-guidelines)**
- **[Code Style Guidelines](#code-style-guidelines)**

---

### Markdown Style Guidelines

- **Markdown lint**
  - [markdown lint](https://github.ibm.com/zosdev/zai-devops/wiki/wiki-lints) or its [VSCode plugin](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint) *(Recommended)* or its [markdownlint-cli2 cli](https://www.npmjs.com/package/markdownlint-cli2).
  - ***All Markdown lint warnings must be addressed***

<br>

- **Code Spell Checker *(Recommended)***
  - To check for spelling warnings

<br>

- **VSCode Plugins**

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

- ***Before submitting code please make sure:***
  - *All contributions in `src/` have a `pylint` score of **10***.
  - All pyIPCS classes, functions, and tests include a corresponding docstring for explanation.
    - **NumPy Styling**
  
  - ***Refer to examples in the repo to correctly format docstrings***
