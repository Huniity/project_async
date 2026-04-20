# src/cli.py -- Veja lá qual'é o melhor jeito de organizar isso aqui, talvez seja melhor colocar em src/cli/main.py ou algo assim. 
# De qualquer forma, esse arquivo é o ponto de entrada para a CLI do projeto, usando Typer para facilitar a criação de comandos e opções. 
# Ele importa a função process_files do módulo worker, que é onde a lógica de processamento dos arquivos CSV para JSON deve estar implementada. 
# O comando convert é definido para aceitar um diretório de entrada, um diretório de saída, o número de trabalhadores paralelos 
# e o tamanho do chunk para processamento. O main() é a função que inicia a aplicação Typer.
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
    from csv_pipeline.worker import process_files  # your teammate's code

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