FROM python:3

COPY /axiol /main 

WORKDIR /main

RUN pip install discord.py pymongo dnspython nltk torch  requests numpy

CMD ["python3", "bot.py"]
