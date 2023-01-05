FROM python:3.10

LABEL maintainer="wei-coding"

ADD . /run/mlserver

WORKDIR /run/mlserver
RUN pip install -r ./requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000