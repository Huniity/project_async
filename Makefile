up:
	docker compose build
	docker compose run csv_converter uv run python ops/script/create_mock_csv.py --output-dir /workspace/input --files 5 --rows 5000000 --seed 42
	chmod -R 777 input output 2>/dev/null || true
	@echo "✓ CSVs generated in Docker container"

down:
	docker compose down --volumes --remove-orphans
	@echo "✓ Docker containers stopped and removed"
	sudo rm -rf output input
	@echo "✓ Input and output directories cleaned"


convert:
	docker compose run csv_converter uv run python cli.py convert /workspace/input /workspace/output --workers 8
	chmod -R 777 output 2>/dev/null || true
	@echo "✓ CSVs converted to JSON in Docker container"

send:
	docker compose run csv_converter uv run python cli.py send /workspace/output --api-url http://api:8000/json
	@echo "✓ JSON files sent to API in Docker container"
