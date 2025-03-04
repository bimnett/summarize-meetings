FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (libopus and ffmpeg)
RUN apt-get update && apt-get install -y \
    libopus-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .
COPY summarize.py .
COPY utils.py .

CMD ["python", "-u", "bot.py"]