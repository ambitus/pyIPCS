# Getting Started

- __[Dependencies/Prerequisite Downloads](#dependenciesprerequisite-downloads)__
- __[Installing pyIPCS](#installing-pyipcs)__

---
---

## Dependencies/Prerequisite Downloads

- __[Back to Top](#getting-started)__

---

### 1. pyIPCS Can Only be Used on a z/OS System

- pyIPCS can not be run on your local system

---

### 2. Complete Necessary Setup for IPCS on your z/OS Environment

- __[Getting Started with IPCS](https://www.ibm.com/docs/en/zos/3.1.0?topic=guide-getting-started-ipcs)__

---

### 3. Be Able to Run the BLSCDDIR CLIST

- pyIPCS uses the BLSCDDIR CLIST to perform necessary dump directory creation
- __Example:__ `%blscddir dsn(sys1.ddir)`
- __[Using the BLSCDDIR CLIST](https://www.ibm.com/docs/en/zos/3.1.0?topic=clist-creating-sysplex-dump-directory)__

---

### 4. Python 3.11 or Greater

- To run pyIPCS your Python version must be 3.11 or greater
- __[IBM Open Enterprise SDK for Python](https://www.ibm.com/products/open-enterprise-python-zos)__

---

### 5. IBM Supported `zoautil_py` Python Package Version `1.3.x`

- __[Installing and Configuring ZOAU](https://www.ibm.com/docs/en/zoau/1.3.0?topic=installing-zoau)__
- __[Install ZOAU Python APIs](https://www.ibm.com/docs/en/zoau/1.3.0?topic=installing-zoau#install-zoau-python-apis-optional)__
- __[ZOAU Python APIs](https://www.ibm.com/docs/en/zoau/1.3.0?topic=python-apis)__

---

### 6. Download Visual Studio Code and Install Zowe Explorer (Optional)

- VS Code is the recommended IDE for Mainframe Development and pyIPCS
- Zowe Explorer is an open source software which allows for mainframe development on VS Code
- __[Download Visual Studio Code](https://code.visualstudio.com/download)__
- __[Install Zowe Explorer](https://docs.zowe.org/stable/getting-started/user-roadmap-zowe-explorer)__

---
---

## Installing pyIPCS

- __[Back to Top](#getting-started)__

---

### 1. Clone The pyIPCS Repo

---

### 2. Navigate to your Cloned pyIPCS Repo

```bash
cd path/to/pyIPCS
```

---

### 3. Build the Wheel File

```bash
pip wheel .
```

- After executing the above command there should exist a file that looks something like `pyipcs-1.1.0-py3-none-any.whl` within the `/pyIPCS` directory

---

### 4. Install the pyIPCS Package

```bash
pip install --force-reinstall pyipcs-1.1.0-py3-none-any.whl
```

---

### 5. Use the pyIPCS Package
