import pandas as pd
import os
import time
import logging
from multiprocessing import Pool


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def convert_csv_to_json(csv_file, json_file, chunk_size=10000):
    """Convert CSV to JSON with chunked reading for memory efficiency."""
    start_time = time.time()
    file_size = os.path.getsize(csv_file)

    logger.info(
        f"Starting conversion: {os.path.basename(csv_file)} "
        f"({file_size / 1024 / 1024:.2f}MB)"
    )

    chunk_count = 0
    total_rows = 0

    try:
        with open(json_file, 'w') as out_f:
            for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
                out_f.write(chunk.to_json(orient='records', lines=True))
                out_f.write('\n')

                chunk_count += 1
                total_rows += len(chunk)

                if chunk_count % 50 == 0:
                    logger.debug(
                        f"  → Processed {chunk_count} chunks "
                        f"({total_rows:,} rows)"
                    )

        elapsed = time.time() - start_time
        output_size = os.path.getsize(json_file)

        logger.info(
            f"✓ Completed: {os.path.basename(csv_file)} → "
            f"{os.path.basename(json_file)} | "
            f"Chunks: {chunk_count} | Rows: {total_rows:,} | "
            f"Output: {output_size / 1024 / 1024:.2f}MB | "
            f"Time: {elapsed:.2f}s"
        )

        return elapsed

    except Exception as e:
        logger.error(f"✗ Failed to convert {os.path.basename(csv_file)}: {e}")
        raise


def run(input_dir: str = "input", output_dir: str = "output", workers: int = 4):
    start_all = time.time()

    logger.info("=" * 70)
    logger.info("CSV to JSON Conversion Pipeline Started")
    logger.info("=" * 70)

    os.makedirs(output_dir, exist_ok=True)

    files = sorted(os.listdir(input_dir))
    csv_files = [os.path.join(input_dir, f) for f in files if f.endswith(".csv")]

    json_files = [
        os.path.join(output_dir, f.replace(".csv", ".json"))
        for f in files if f.endswith(".csv")
    ]

    if not csv_files:
        logger.warning(f"No CSV files found in '{input_dir}'")
        return

    logger.info(f"Found {len(csv_files)} CSV file(s) to process")
    logger.info(f"Using {workers} worker(s)")

    with Pool(workers) as pool:
        pool.starmap(convert_csv_to_json, list(zip(csv_files, json_files)))

    total_elapsed = time.time() - start_all

    logger.info("=" * 70)
    logger.info(f"Pipeline completed in {total_elapsed:.2f}s")
    logger.info(f"Average time per file: {total_elapsed / len(csv_files):.2f}s")
    logger.info("=" * 70)


if __name__ == "__main__":
    run()