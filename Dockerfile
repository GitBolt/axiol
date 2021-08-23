FROM python:3

COPY / /main

WORKDIR /main

RUN pip install motor dnspython Pillow nltk discord.py colorama termcolor pymongo python-dotenv

CMD ["python3", "-u", "bot.py"]