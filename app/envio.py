import requests
import base64
import os
import math

API_URL = "http://127.0.0.1:8000/json"
CHUNK_SIZE = 10 * 1024 * 1024  # 10 MB

def send_file(file_path):
    file_size = os.path.getsize(file_path)
    total_chunks = math.ceil(file_size / CHUNK_SIZE)

    with open(file_path, "rb") as f:
        chunk_number = 0

        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break

            chunk_number += 1

            payload = {
                "file_name": os.path.basename(file_path),
                "chunk_number": chunk_number,
                "total_chunks": total_chunks,
                "data": base64.b64encode(chunk).decode("utf-8")
            }

            r = requests.post(API_URL, json=payload)

            print(f"Chunk {chunk_number}/{total_chunks}: {r.status_code}")

folder_path = "./jsons"

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)

    if os.path.isfile(file_path):
        print(f"A enviar: {file_path}")
        send_file(file_path)