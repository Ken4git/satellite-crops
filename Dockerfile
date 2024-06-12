FROM python:3.12.4-slim-bullseye

COPY requirements_prod.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY data/cred.json /satellite-crops-1caf69ecbfe8.json

COPY satellitecrops /satellitecrops
COPY mapping_crops.csv mapping_crops.csv
#COPY out_image.jp2 out_image.jp2


COPY setup.py setup.py
RUN pip install .

RUN mkdir -p /root/.lewagon/satellite-crops/training_outputs/models/

CMD uvicorn satellitecrops.api.fast:app --port 8000 --host 0.0.0.0
