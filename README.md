# NDVI Uploader

This project captures raw and NDVI-processed images from a Raspberry Pi camera and uploads them to an SFTP server.

## Features
- NDVI processing using OpenCV (NIR vs VIS)
- Upload via SFTP
- Modular design (works on Pi or Docker/Kubernetes)

## Usage
Install:
```bash
pip install -r requirements.txt


## Configuration
Edit ndvi_capture_upload.py to set your SFTP credentials and remote path.

* OPTIONAL
docker build -t ndvi-uploader .
docker run --rm ndvi-uploader
