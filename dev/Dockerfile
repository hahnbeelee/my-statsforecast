FROM python:3.10

COPY dev/requirements.txt setup/

RUN pip install -r setup/requirements.txt

# Settuping the working environment.
# This will server as an empty directory where all the files be dropped to.
WORKDIR /workdir/
