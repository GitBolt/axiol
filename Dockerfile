FROM python:3

COPY /axiol /main 

WORKDIR /main

RUN pip install discord.py pymongo dnspython requests

CMD ["python3", "bot.py"]
