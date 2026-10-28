# Development Environment Setup

## 1. Create a Virtual Environment (Recommended)

```bash
cd pyIPCS
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## 2. Complete pyIPCS Installation

Make sure you have all the necessary prerequisites and have pyIPCS correctly installed — see the [Installation](../getting-started/installation) guide.

## 3. Install Development Dependencies and Pre-commit Hooks

```bash
pip install -r requirements-dev.txt
pre-commit install
```

## 4. Configure Git & DCO (Developer Certificate of Origin)

All contributions to pyIPCS require a [DCO sign-off](https://github.com/openmainframeproject/tsc/blob/master/process/contribution_guidelines.md#developer-certificate-of-origin).
Configure your Git identity so the sign-off is applied correctly:

```bash
git config user.name "<YOUR_NAME>"
git config user.email "<YOUR_EMAIL>"
```

The DCO sign-off is added automatically when you commit with the `-s` flag:

```bash
git commit -s -m "Your commit message"
```

This appends a `Signed-off-by` trailer to the commit message:

```
Your commit message

Signed-off-by: Your Name <your.email@example.com>
```
