# Installation

## Prerequisites

### Platform

- **pyIPCS can only be used on a z/OS system** — it cannot run on Linux, macOS, or Windows

### IPCS Setup

- Complete the necessary IPCS setup on your z/OS environment before using pyIPCS
  - *[Getting Started with IPCS](https://www.ibm.com/docs/en/zos/3.2.0?topic=guide-getting-started-ipcs)*

### Python Version

- **Python 3.12 or greater** is required
  - *[IBM Open Enterprise SDK for Python](https://www.ibm.com/products/open-enterprise-python-zos)*

### `zoautil_py`

- The IBM-supported `zoautil_py` package (version `1.4.x`) must be installed
  - *[Installing and Configuring ZOAU](https://www.ibm.com/docs/en/zoau/1.4.x?topic=installing-zoau)*
  - *[Install ZOAU Python APIs](https://www.ibm.com/docs/en/zoau/1.4.x?topic=installing-zoau#install-zoau-python-apis-optional)*
  - *[ZOAU Python APIs](https://www.ibm.com/docs/en/zoau/1.4.x?topic=python-apis)*

## Installation Steps

1. **Clone the repository** on your z/OS system

2. **Navigate to the cloned directory**

   ```bash
   cd path/to/pyIPCS
   ```

3. **Install the package**

   ```bash
   pip install .
   ```

## Optional Tooling

- **Visual Studio Code** with the **Zowe Explorer** extension is the recommended IDE for mainframe development with pyIPCS
  - *[Download Visual Studio Code](https://code.visualstudio.com/download)*
  - *[Install Zowe Explorer](https://docs.zowe.org/stable/getting-started/user-roadmap-zowe-explorer)*
