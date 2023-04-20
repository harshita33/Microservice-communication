FROM python

WORKDIR /app

COPY ./consumer_two .
RUN pip install -r requirements.txt

CMD [ "python", "insertion.py" ]
