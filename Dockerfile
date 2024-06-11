FROM python:3.12.4-slim-bullseye

COPY satellitecrops /satellitecrops
COPY requirements.txt requirements.txt
COPY mapping_crops.csv mapping_crops.csv
COPY out_image.jp2 out_image.jp2

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY setup.py setup.py
RUN pip install .

CMD python /satellitecrops/interface/main.py
