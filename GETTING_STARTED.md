# Getting Started

- **[Dependencies/Prerequisite Downloads](#dependenciesprerequisite-downloads)**
- **[Installing pyIPCS](#installing-pyipcs)**

---

## Dependencies/Prerequisite Downloads

- **[Back to Top](#getting-started)**

---

1. **pyIPCS Can Only be Used on a z/OS System**
    - *pyIPCS can not be run on your local system*

2. **Complete Necessary Setup for IPCS on your z/OS Environment**
    - *[Getting Started with IPCS](https://www.ibm.com/docs/en/zos/3.1.0?topic=guide-getting-started-ipcs)*

3. **Python 3.12 or Greater**
    - *To run pyIPCS your Python version must be 3.12 or greater*
    - *[IBM Open Enterprise SDK for Python](https://www.ibm.com/products/open-enterprise-python-zos)*

4. **Install IBM Supported `zoautil_py` Python Package Versions `1.4.x` or `1.3.x`**
    - *[Installing and Configuring ZOAU](https://www.ibm.com/docs/en/zoau/1.4.x?topic=installing-zoau)*
    - *[Install ZOAU Python APIs](https://www.ibm.com/docs/en/zoau/1.4.x?topic=installing-zoau#install-zoau-python-apis-optional)*
    - *[ZOAU Python APIs](https://www.ibm.com/docs/en/zoau/1.4.x?topic=python-apis)*

5. **Download Visual Studio Code and Install Zowe Explorer (Optional)**
    - *VS Code is the recommended IDE for Mainframe Development and pyIPCS*
      - *[Download Visual Studio Code](https://code.visualstudio.com/download)*
    - *Zowe Explorer is an open source software which allows for mainframe development on VS Code*
      - *[Install Zowe Explorer](https://docs.zowe.org/stable/getting-started/user-roadmap-zowe-explorer)*

---

## Installing pyIPCS

- **[Back to Top](#getting-started)**

---

1. **Clone The pyIPCS Repo**

2. **Navigate to your Cloned pyIPCS Repo**
    - `cd path/to/pyIPCS`

3. **Build the Wheel File**
    - `pip wheel .`
    - *After executing the above command a whl file should exist within the `/pyIPCS` directory*
        - *Example:* `pyipcs-[version]-py3-none-any.whl`

4. **Install the pyIPCS Package**
    - `pip install --force-reinstall pyipcs-[version]-py3-none-any.whl`

5. **Use the pyIPCS Package**
