FROM python

WORKDIR .

COPY . .
RUN pip install aiogram

CMD [ "python", "telegram_bot.py" ]