FROM python:latest

COPY ./inputs.zip /tmp/inputs.zip
COPY ./requirements.txt /tmp/
RUN mkdir /src/
COPY ./debris_processor/* /src/
RUN unzip /tmp/inputs.zip -d /tmp/ && \
    pip install -r /tmp/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "/src/debris_area_viz.py" ]