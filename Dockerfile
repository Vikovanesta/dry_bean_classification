# Dockerfile

# Pakai slim base image Python
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Install semua package Python yang dibutuhkan dari requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file ke dalam direktori kerja /app.
COPY . .

#  Run di port 5000
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]