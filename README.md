# End-of-Life Crystalline Silicon PV Waste Estimation Tool
## Overview

This repository contains the code and data used to estimate future end-of-life (EoL) crystalline silicon (c-Si) photovoltaic (PV) waste generation and secondary silicon recovery in the European Union.

The application is implemented as an interactive Streamlit dashboard.

---

## Requirements

Before running the application, install:

### Python

Python 3.10 or later

## Install Required Packages

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

Required packages:

```text
streamlit
pandas
numpy
scipy
plotly
openpyxl
graphviz
```

## Running the Application

Open a terminal in the project directory and execute:

```bash
streamlit run main.py
```

This will execute the code and take you to your web browser,

---

## Troubleshooting

### Module Not Found Error

Install the missing package or reinstall all dependencies:

```bash
pip install -r requirements.txt
```

### Missing Excel File

Ensure that:

```text
inputs.xlsx
```

is located in the same folder as:

```text
main.py
```

### Streamlit Not Found

Install Streamlit:

```bash
pip install streamlit
```

or run:

```bash
python -m streamlit run main.py
```

---

## Citation

If this software contributes to your work, please cite the associated publication and the Zenodo record linked to this repository.

---

## Contact

nagarajan.ganesan@sintef.no
For questions regarding the model and methodology, please contact the corresponding author.
