FROM python:3.8
COPY ./app /app
RUN pip install -r /app/requirements.txt
WORKDIR /app
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]