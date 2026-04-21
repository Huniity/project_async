# CSV Pipeline

CSV to JSON pipeline for large datasets, with chunked conversion and chunked upload to an HTTP API.

## What This Project Does

1. Generates mock CSV files (optional).
2. Converts CSV files to JSON Lines output.
3. Uploads JSON files to an API in fixed-size chunks.

The pipeline is designed to be memory-efficient during conversion and robust for large-file uploads.

## Features

- Chunked CSV reading with pandas (`10_000` rows per chunk).
- JSON Lines output (one JSON object per line).
- Chunked HTTP upload (`10 MB` per request chunk).
- CLI commands powered by Typer.
- Docker workflow using `docker compose` + `Makefile`.
- Parallel CSV conversion using multiprocessing.

## Project Structure

```
.
├── cli.py                         # Typer CLI entrypoint
├── docker-compose.yaml            # Docker service definition
├── Makefile                       # Common pipeline commands
├── pyproject.toml                 # Python project metadata/deps
├── ops/
│   ├── Dockerfile                 # Runtime image for pipeline commands
│   └── script/
│       └── create_mock_csv.py     # Synthetic CSV generator
├── src/
│   └── app/
│       ├── conversion.py          # CSV -> JSON conversion logic
│       └── envio.py               # JSON upload logic
├── input/                         # Generated/input CSV files
└── output/                        # Generated JSON files
```

## Requirements

- Python `>= 3.14`
- `uv`
- Docker + Docker Compose (for containerized workflow)

## Quick Start

### Docker/Makefile workflow (recommended)

```bash
# Build image and generate sample CSV files in input/
make up

# Convert CSV -> JSON into output/
make convert

# Send JSON files to API
make send

# Stop containers and clean generated folders
make down
```

## CLI Usage

### Install dependencies

```bash
uv sync
```

### Convert CSV files

```bash
uv run python cli.py convert input output --workers 4
```

### Send JSON files to API

```bash
uv run python cli.py send output --api-url http://127.0.0.1:8000/json
```

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make up` | Build container and generate mock CSVs in `input/` |
| `make convert` | Convert CSV files from `input/` to JSON in `output/` |
| `make send` | Upload JSON files from `output/` to API |
| `make down` | Stop containers and remove generated `input/` and `output/` |

## Data Flow

```
input/*.csv
   -> src/app/conversion.py
   -> output/*.json (JSON Lines)
   -> src/app/envio.py
   -> POST chunks to API endpoint
```

## Configuration Details

- CSV generation script: `ops/script/create_mock_csv.py`
  - Defaults: 5 files, 5,000,000 rows each, seed 42.
- Conversion chunk size: `10_000` rows (`src/app/conversion.py`).
- Upload chunk size: `10 * 1024 * 1024` bytes (`src/app/envio.py`).
- Default upload URL: `http://127.0.0.1:8000/json`.

## Docker Note

The container uses `UV_PROJECT_ENVIRONMENT=/opt/venv` during image build so Docker does not overwrite the host `.venv` when `/workspace` is mounted.

## Dependencies

- `pandas`
- `requests`
- `typer`

See `pyproject.toml` for exact versions.

## License

See `LICENSE`.
