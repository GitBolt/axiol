FROM python:3

COPY /axiol /main 

WORKDIR /main

RUN pip install discord.py pymongo dnspython youtube_dl pynacl nltk torch 
RUN apt-get update && apt-get install -y ffmpeg

CMD ["python3", "bot.py"]