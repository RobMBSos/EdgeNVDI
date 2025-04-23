FROM python:3.11-slim

RUN apt update && apt install -y libgl1 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "ndvi_capture_upload.py"]
