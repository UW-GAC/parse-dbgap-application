FROM ghcr.io/anvilproject/anvil-rstudio-bioconductor:3.17.1

RUN cd /usr/local && \
    git clone https://github.com/UW-GAC/parse-dbgap-application.git

# Install python requirements.
RUN python -m pip install --upgrade pip
RUN python -m pip install -r /usr/local/parse-dbgap-application/requirements.txt
