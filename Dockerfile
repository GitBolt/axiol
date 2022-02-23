FROM python:3

COPY /axiol /root 

WORKDIR /root

RUN pip install motor dnspython pillow disnake

CMD ["python3", "-u","bot.py"]
