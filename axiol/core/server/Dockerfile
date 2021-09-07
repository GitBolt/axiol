FROM python:3

COPY / /main

WORKDIR /main

RUN pip install fastapi uvicorn uvloop pynacl

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0

