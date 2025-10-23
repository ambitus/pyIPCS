# pyIPCS Test README

---

## Install `pytest` to run pyIPCS tests

- **`pip install pytest`**

---

## Run all tests

- `pytest  path/to/pyIPCS/src/tests/`

<br>

- ***Note:** Certain tests require `"TEST_DUMPS"` to be specified in `src/tests/settings.json`*
  - *These tests will be skipped otherwise*

---

## Run subset of tests

- **Run all tests in specific directory**
  - `pytest  path/to/pyIPCS/src/tests/test_session/`

<br>

- **Run tests from a specific file**
  - `pytest  path/to/pyIPCS/src/tests/test_session/test_open_close.py`

---

## How to run tests with custom settings

### Create: `src/tests/settings.json`

<br>

- **Custom Settings Include**
  - `"TEST_HLQ"`
    - Custom high level qualifier
  - `"TEST_DIRECTORY"`
    - Custom directory on your local filesystem
  - `"TEST_ALLOCATIONS"`
    - Dictionary of allocations where keys are DD names and values are string data set allocation requests or lists of cataloged datasets.
  - `"TEST_DUMPS"`
    - List of z/OS dump dataset names
  - ***Note:** Values will be set to defaults if not included or set to `null`*
    - *Refer to the logic in `src/tests/conftest.py` to fully understand how changing these values will impact testing*

### Example `src/tests/settings.json`

- ***Note:** Keys can be excluded or set to `null`*

```json
{
  "TEST_HLQ": "YOUR.HLQ",

  "TEST_DIRECTORY": "/your/test/directory",

  "TEST_ALLOCATIONS": {
      "SYSEXEC": ["YOUR.SYSEXEC"], 
      "SYSPROC": ["YOUR.SBLSCLI0"]
  },

  "TEST_DUMPS": ["YOUR.DUMP1", "YOUR.DUMP2"]
}
```

---

## Important Note While Running Tests

- **Due to possible invalid garbage collection by `pytest` there may be user warnings that pop up even when a test has passed successfully**

<br>

- **It is important for a user running tests to be aware of these `pytest` cleanup issues and make sure there no leftover files or z/OS datasets after test execution**
