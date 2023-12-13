# parse-dbgap-application
This repository contains python scripts to parse information out of a dbGaP application PDF.

Right now, there is one script provided:

* `parse_dars.py`: parse the list of DARs that have been applied for in the dbGaP application PDF.

## Usage

### On AnVIL

See the [workflow on Dockstore](https://dockstore.org/my-workflows/github.com/UW-GAC/parse-dbgap-application).
To run the workflow, you will need to upload the dbGaP application PDF to a Google bucket and provide the path to the PDF as an input to the workflow.
The workflow runs two steps:

1. Extract DARs into a text file.
2. Render an Rmarkdown report with basic info about the requested DARs.

### Local use

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


## Updating the docker images

```
docker build -t uwgac/parse-dbgap-application:<tag> .
docker push uwgac/parse-dbgap-application:<tag>
```
