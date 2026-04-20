up:
	uv run python script_csv.py --output-dir input --files 5 --rows 5000000 --seed 42
	docker compose up --build