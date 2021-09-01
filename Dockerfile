FROM python:3

COPY / /main

WORKDIR /main

RUN pip install git+https://github.com/rapptz/discord.py pymongo motor dnspython Pillow nltk colorama termcolor python-dotenv embed-templator

CMD ["python3", "-u", "bot.py"]