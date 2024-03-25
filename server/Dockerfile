FROM python:3.9

RUN pip install Flask gunicorn python-dotenv google-generativeai

WORKDIR /app

COPY src/ .

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 genai:app