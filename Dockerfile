FROM python:3.7-alpine
ADD . /var/sources/api/
WORKDIR /var/sources/api
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python app.py
EXPOSE 3000
