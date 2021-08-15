FROM python:3

COPY /axiol /main 

WORKDIR /main

RUN pip install motor dnspython pillow nltk git+https://github.com/rapptz/discord.py 

CMD ["python3", "bot.py"]
