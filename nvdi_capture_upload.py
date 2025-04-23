import cv2
import numpy as np
import os
import paramiko
from datetime import datetime

# === SFTP Configuration ===
hostname = 'your.sftp.server.com'
port = 22
username = 'your_username'
password = 'your_password'
remote_path = '/uploads/'  # must exist on server

# === Timestamp filenames ===
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
photo_name = f'photo_{now}.jpg'
ndvi_name = f'ndvi_{now}.jpg'

# === CAPTURE IMAGE ===
print("📸 Capturing image...")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open camera")
ret, frame = cap.read()
cap.release()
if not ret:
    raise RuntimeError("Image capture failed")
cv2.imwrite(photo_name, frame)
print(f"✅ Saved: {photo_name}")

# === NDVI PROCESSING ===
print("🧠 Processing NDVI...")
nir = frame[:, :, 2].astype(float)  # Red channel = NIR
vis = frame[:, :, 0].astype(float)  # Blue channel = VIS
bottom = (nir + vis)
bottom[bottom == 0] = 0.01
ndvi = (nir - vis) / bottom
ndvi_norm = cv2.normalize(ndvi, None, 0, 255, cv2.NORM_MINMAX)
ndvi_img = np.uint8(ndvi_norm)
ndvi_colored = cv2.applyColorMap(ndvi_img, cv2.COLORMAP_JET)
cv2.imwrite(ndvi_name, ndvi_colored)
print(f"✅ Saved NDVI image: {ndvi_name}")

# === SFTP UPLOAD ===
print("📡 Connecting to SFTP...")
try:
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(photo_name, os.path.join(remote_path, photo_name))
    sftp.put(ndvi_name, os.path.join(remote_path, ndvi_name))
    sftp.close()
    transport.close()
    print("✅ Uploaded to SFTP server")
except Exception as e:
    print(f"❌ Upload failed: {e}")
