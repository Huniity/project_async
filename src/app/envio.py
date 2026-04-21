import requests
import base64
import os
import math
import uuid
import time

CHUNK_SIZE = 10 * 1024 * 1024  # 10MB


def send_file(file_path, api_url, timeout=30):
    """Send file to API in chunks with base64 encoding."""
    start_time = time.time()

    file_size = os.path.getsize(file_path)
    total_chunks = math.ceil(file_size / CHUNK_SIZE)

    file_id = str(uuid.uuid4())
    file_name = os.path.basename(file_path)

    print(
        f"Sending: {file_name} "
        f"({file_size / 1024 / 1024:.2f}MB) → {total_chunks} chunks"
    )

    successful_chunks = 0
    failed_chunks = 0

    try:
        with open(file_path, "rb") as f:
            for chunk_number in range(1, total_chunks + 1):
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break

                payload = {
                    "file_id": file_id,
                    "file_name": file_name,
                    "chunk_number": chunk_number,
                    "total_chunks": total_chunks,
                    "data": base64.b64encode(chunk).decode("utf-8")
                }

                try:
                    r = requests.post(api_url, json=payload, timeout=timeout)

                    if r.status_code == 200:
                        successful_chunks += 1

                        if chunk_number % 10 == 0 or chunk_number == total_chunks:
                            print(f"  → Chunk {chunk_number}/{total_chunks}")
                    else:
                        failed_chunks += 1
                        print(f"  ✗ Chunk {chunk_number} failed: {r.status_code}")
                        break

                except requests.RequestException as e:
                    failed_chunks += 1
                    print(f"  ✗ Network error on chunk {chunk_number}: {str(e)[:60]}")
                    break

        elapsed = time.time() - start_time

        if successful_chunks == total_chunks:
            speed = (file_size / 1024 / 1024) / elapsed
            print(
                f"✓ {file_name}: {successful_chunks}/{total_chunks} chunks "
                f"({elapsed:.1f}s, {speed:.1f}MB/s)\n"
            )
            return True
        else:
            print(
                f"✗ {file_name}: Failed - only "
                f"{successful_chunks}/{total_chunks} chunks sent\n"
            )
            return False

    except Exception as e:
        print(f"✗ Error processing {file_name}: {e}\n")
        return False


def run(output_dir: str = "./output", api_url: str = "http://127.0.0.1:8000/json"):
    start_all = time.time()

    if not os.path.exists(output_dir):
        print(f"Error: Output folder not found: {output_dir}")
        return

    json_files = sorted([f for f in os.listdir(output_dir) if f.endswith(".json")])

    if not json_files:
        print(f"No JSON files found in {output_dir}")
        return

    print(f"Found {len(json_files)} JSON file(s)\n")

    successful_files = 0
    failed_files = 0

    for file_name in json_files:
        file_path = os.path.join(output_dir, file_name)

        if os.path.isfile(file_path):
            if send_file(file_path, api_url):
                successful_files += 1
            else:
                failed_files += 1

    total_elapsed = time.time() - start_all

    print(
        f"Completed: {successful_files} succeeded, "
        f"{failed_files} failed ({total_elapsed:.1f}s total)"
    )


if __name__ == "__main__":
    run()