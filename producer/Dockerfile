FROM python:3.8

WORKDIR /usr/app

ADD ./requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
ADD ./ ./

CMD ["python3", "main.py"]
