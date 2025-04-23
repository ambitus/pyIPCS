# pyIPCS Test README

---

## Install pytest

- `pip install pytest`

### Create `src/tests/settings.json`

- __Place the following default contents into `settings.json`:__

```json
{
    "TEST_DUMPS": [],

    "TEST_ALLOCATIONS": {
        "IPCSPARM": ["SYS1.PARMLIB"], 
        "SYSPROC": ["SYS1.SBLSCLI0"]
    },

    "TEST_HLQ": "",

    "TEST_DIRECTORY": "PYTEST"
}
```

- __Refer to the instructions below on how to change these default values to meet your testing needs__

---

### How to run tests against z/OS dumps

- To run pyIPCS tests that require z/OS dumps you must add their dataset names as strings to the empty list associated with variable `TEST_DUMPS` in `src/tests/settings.json`.

#### Example `TEST_DUMPS` in `src/tests/settings.json`

```python
"TEST_DUMPS" : [
    "MY.TEST.DUMP1",
    "MY.TEST.DUMP2",
    "YOUR.TEST.DUMP"
]
```

- __If the list `TEST_DUMPS` in `src/tests/settings.json` is left empty, tests that require z/OS dumps will be skipped__

---

### How to run tests with custom set of allocations

- To run pyIPCS tests with a custom set of allocations you must add them to the empty dictionary associated with variable `TEST_ALLOCATIONS` in `src/tests/settings.json`.
  - Keys are DD names and values are string data set allocation requests or lists of cataloged datasets.
- This dictionary will be passed to the `IpcsSession.update_allocations` method

#### Example `TEST_ALLOCATIONS` in `src/tests/settings.json`

```python
"TEST_ALLOCATIONS" : {
    "IPCSPARM" : [
        "MY.CUSTOM.PARMLIB"
    ],
    "SYSPROC" : [
        "MY.CUSTOM.SBLSCLI0",
        "MY.CUSTOM.OTHER"
    ]
}
```

##### By default `TEST_ALLOCATIONS` contains the default IpcsSession allocations

```python
"TEST_ALLOCATIONS" = {
    "IPCSPARM" : ["SYS1.PARMLIB"], 
    "SYSPROC" : ["SYS1.SBLSCLI0"]
}
```

---

### For Other Values Contained in `settings.json`

- __Refer to the logic in `src/tests/conftest.py` to understand how changing these values will impact testing__

---

### !!! Important Note While Running Tests

- __Due to possible invalid garbage collection by `pytest` there may be user warnings that pop up even when a test has passed successfully__.

- __It is important for a user running tests to be aware of these `pytest` cleanup issues and make sure there no leftover files or z/OS datasets after test execution__.

---

### Run all tests

- `pytest  path/to/pyIPCS/tests/`

---

### Run subset of tests

- __Run all IpcsSession tests__:
  - `pytest  path/to/pyIPCS/tests/test_session/`
- __Run tests for IpcsSesion open and close methods__
  - `pytest  path/to/pyIPCS/tests/test_session/test_open_close.py`
- __Run all Dump tests:__
  - `pytest  path/to/pyIPCS/tests/test_dump/`
