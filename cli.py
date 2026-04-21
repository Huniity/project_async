"""
CSV Pipeline CLI - Thin wrapper around conversion.py and app/envio.py
"""
import typer
from pathlib import Path
import sys
from src.app.conversion import run as run_conversion
from src.app.envio import run as run_envio

app = typer.Typer(help="CSV → JSON → API Pipeline")


@app.command()
def convert(
    input_dir: Path = typer.Argument("input", help="Directory with CSV files"),
    output_dir: Path = typer.Argument("output", help="Directory for JSON output"),
):
    """Convert CSV files to JSON."""
    try:
        run_conversion(str(input_dir), str(output_dir))
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def send(
    output_dir: Path = typer.Argument("output", help="Directory with JSON files"),
    api_url: str = typer.Option("http://127.0.0.1:8000/json", help="API endpoint URL"),
):
    """Send JSON files to API."""
    try:
        run_envio(str(output_dir), api_url)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


def main():
    app()


if __name__ == "__main__":
    main()