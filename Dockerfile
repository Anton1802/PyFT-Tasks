FROM python:3.12.6

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]