FROM python:3

COPY /axiol /main 

WORKDIR /main

RUN pip install pymongo dnspython pillow nltk discord.py 

CMD ["python3", "bot.py"]
