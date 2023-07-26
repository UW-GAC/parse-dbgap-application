# parse-dbgap-application
This repository contains python scripts to parse information out of a dbGaP application PDF.

Right now, there is one script provided:

* `parse_dars.py`: parse the list of DARs that have been applied for in the dbGaP application PDF.

## Usage

* Clone the repository:

```
git clone https://github.com/UW-GAC/parse-dbgap-application.git
```

* Create a virtual environment:

```
python -m venv venv
```

* Insall requirements

```
pip install -m requirements.txt
```

* Run script

```
python parse_dars.py <path_to_application_pdf> <path_to_output_tsv>
```
