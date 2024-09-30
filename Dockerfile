FROM python:3
LABEL authors="ivklepova23@gmail.com"
WORKDIR /course_drf
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
