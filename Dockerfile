FROM python:3
LABEL authors="ivklepova23@gmail.com"
WORKDIR /course_drf
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
