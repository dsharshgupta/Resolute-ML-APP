FROM python:3.11-alpine
COPY . /app
COPY data ./app/data
COPY models ./app/models
COPY static ./app/static
COPY templates ./app/templates
WORKDIR /app
RUN apk add --no-cache gcc musl-dev
RUN apk add --no-cache gcc musl-dev g++
RUN pip install -r requirements.txt
CMD python app.py