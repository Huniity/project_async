import requests
import base64
import os
import math
import uuid

API_URL = "http://127.0.0.1:8000/json"
CHUNK_SIZE = 10 * 1024 * 1024

def send_file(file_path):
    file_size = os.path.getsize(file_path)
    total_chunks = math.ceil(file_size / CHUNK_SIZE)
    file_id = str(uuid.uuid4())

    with open(file_path, "rb") as f:
        for chunk_number in range(1, total_chunks + 1):
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break

            payload = {
                "file_id": file_id,
                "file_name": os.path.basename(file_path),
                "chunk_number": chunk_number,
                "total_chunks": total_chunks,
                "data": base64.b64encode(chunk).decode("utf-8")
            }

            try:
                r = requests.post(API_URL, json=payload, timeout=30)

                if r.status_code != 200:
                    print(f"Erro chunk {chunk_number}: {r.text}")
                    break

                print(f"Chunk {chunk_number}/{total_chunks} OK")

            except requests.RequestException as e:
                print(f"Erro de rede no chunk {chunk_number}: {e}")
                break


folder_path = "./jsons"

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)

    if os.path.isfile(file_path):
        print(f"A enviar: {file_path}")
        send_file(file_path)