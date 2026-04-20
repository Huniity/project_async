# cli.py
# -------
# Handles user-facing input via the terminal and delegates
# all processing to the worker module (owned by teammates).
# Interface contract:
#   process_files(files: list[Path], output_dir: Path, workers: int, chunk_size: int)

import typer
from pathlib import Path

app = typer.Typer(help="CSV → JSON pipeline CLI.")

@app.command()
def convert(
    input_dir: Path = typer.Argument(..., exists=True, file_okay=False, help="Directory containing CSV files."),
    output_dir: Path = typer.Argument(..., file_okay=False, help="Directory to write JSON output."),
    workers: int = typer.Option(4, "--workers", "-w", help="Number of parallel workers."),
    chunk_size: int = typer.Option(10_000, "--chunk-size", "-c", help="Rows per processing chunk."),
):
    """Convert all CSV files in INPUT_DIR to JSON files in OUTPUT_DIR."""
    # Imported here to keep cli.py decoupled from implementation details.
    # Requires worker module to be available at runtime, not at import time.
    from csv_pipeline.worker import process_files

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_files = list(input_dir.glob("*.csv"))

    if not csv_files:
        typer.echo("No CSV files found.", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Found {len(csv_files)} file(s). Starting with {workers} workers...")
    process_files(csv_files, output_dir, workers=workers, chunk_size=chunk_size)
    typer.echo("Done.")

def main():
    app()