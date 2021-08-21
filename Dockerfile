FROM python:3

COPY / /main

WORKDIR /main

RUN pip install motor dnspython pillow nltk discord.py 

CMD ["python3", "-u","run.py"]
