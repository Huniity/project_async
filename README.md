# CSV Pipeline

Convert large CSV files to JSON and send them to an API in chunked batches.

## Features

- **Chunked CSV Reading**: Processes large CSV files efficiently (10K row chunks)
- **JSONL Output**: Converts to JSON Lines format (one JSON object per line)
- **Chunked API Upload**: Sends JSON files to API in 10MB chunks with base64 encoding
- **Mock API Server**: Built-in mock API server for testing
- **Docker Support**: Fully containerized workflow
- **CLI Interface**: Simple command-line interface for all operations

## Quick Start

### Local Development

1. **Install dependencies**:
```bash
uv sync
```

2. **Generate sample CSV files** (5 files × 5M rows each):
```bash
uv run python ops/script/create_mock_csv.py --output-dir input --files 5 --rows 5000000
```

3. **Convert CSVs to JSON**:
```bash
uv run python cli.py convert input output
```

4. **Start mock API server** (in separate terminal):
```bash
python mock_api.py
```

5. **Send JSON files to API**:
```bash
uv run python cli.py send output
```

### Using Makefile (Recommended)

```bash
# Generate CSVs with Docker
make up

# Convert CSVs to JSON
make convert

# Start mock API in separate terminal
make mock-api

# Send to API
make send

# Check API status
make api-status

# Stop containers and clean up
make down
```

## Project Structure

```
├── conversion.py          # CSV → JSON conversion logic
├── app/
│   └── envio.py          # API upload logic
├── src/
│   └── cli.py            # CLI interface
├── ops/
│   ├── Dockerfile        # Container image
│   └── script/
│       └── create_mock_csv.py  # CSV generator script
├── input/                # CSV input directory (generated)
├── output/               # JSON output directory (generated)
├── mock_api_output/      # Mock API received files (generated)
├── docker-compose.yaml   # Container orchestration
└── Makefile             # Task automation
```

## Pipeline Workflow

```
Input CSVs (input/)
    ↓
conversion.py (chunked reading: 10K rows)
    ↓
JSON Lines output (output/)
    ↓
app/envio.py (chunked upload: 10MB chunks)
    ↓
Mock API or Real API (http://127.0.0.1:8000/json)
    ↓
Reconstructed files (mock_api_output/)
```

## Commands

### Local Commands

| Command | Purpose |
|---------|---------|
| `uv sync` | Install dependencies |
| `python conversion.py [input] [output]` | Convert CSVs to JSON |
| `python app/envio.py` | Send JSON files to API |
| `python mock_api.py` | Start mock API server |
| `uv run python cli.py convert input output` | CLI convert command |
| `uv run python cli.py send output` | CLI send command |

### Makefile Commands

| Command | Purpose |
|---------|---------|
| `make up` | Generate sample CSVs in Docker |
| `make convert` | Convert CSVs to JSON in Docker |
| `make send` | Send JSON to API in Docker |
| `make mock-api` | Start mock API server |
| `make api-status` | Check mock API status |
| `make api-health` | Check mock API health |
| `make down` | Stop Docker containers and clean up |

## Configuration

### CSV Generation
- **Location**: `ops/script/create_mock_csv.py`
- **Default**: 5 files × 5M rows each
- **Columns**: auto-generated with various data types

### Conversion Settings
- **Chunk Size**: 10,000 rows per chunk (configurable in `conversion.py`)
- **Output Format**: JSON Lines (one JSON object per line)

### API Upload Settings
- **Chunk Size**: 10MB per chunk (configurable in `app/envio.py`)
- **Encoding**: Base64
- **Default URL**: `http://127.0.0.1:8000/json`

## Docker Usage

The project includes full Docker support via `docker-compose.yaml`:

```bash
# Build and generate CSVs
docker compose run csv_converter uv run python ops/script/create_mock_csv.py --output-dir /workspace/input --files 5 --rows 5000000

# Convert CSVs to JSON
docker compose run csv_converter uv run python cli.py convert /workspace/input /workspace/output

# Send to API
docker compose run csv_converter uv run python cli.py send /workspace/output
```

## Performance

Expected performance on 1.6GB input (5 × 320MB CSV files):
- **Conversion**: ~70 seconds → 2.7GB JSON output
- **Upload**: ~33 seconds (272 chunks to mock API)

## Mock API Endpoints

### POST /json
Receive chunked JSON data.

**Request**:
```json
{
  "file_id": "uuid-string",
  "file_name": "data_1.json",
  "chunk_number": 1,
  "total_chunks": 50,
  "data": "base64-encoded-chunk"
}
```

**Response** (in progress):
```json
{
  "status": "in_progress",
  "message": "Chunk 1/50 received",
  "chunks_received": 1,
  "total_chunks": 50
}
```

**Response** (complete):
```json
{
  "status": "success",
  "message": "File completely received and reconstructed",
  "file_name": "data_1.json",
  "total_chunks": 50,
  "file_size_mb": 550.25
}
```

### GET /health
Health check endpoint.

### GET /status
View received files and their status.

### GET /
API information and endpoints.

## Dependencies

- `python >= 3.14`
- `pandas >= 3.0.2` - CSV processing
- `requests >= 2.33.1` - HTTP requests
- `typer >= 0.12` - CLI interface
- `uv` - Package manager

## License

See [LICENSE](LICENSE) file.
