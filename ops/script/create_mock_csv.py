import argparse
import csv
import random
from pathlib import Path
from typing import List, Union


FIRST_NAMES = [
    "Liam",
    "Noah",
    "Oliver",
    "Elijah",
    "James",
    "William",
    "Benjamin",
    "Lucas",
    "Henry",
    "Alexander",
    "Olivia",
    "Emma",
    "Charlotte",
    "Amelia",
    "Sophia",
    "Isabella",
    "Ava",
    "Mia",
    "Evelyn",
    "Luna",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
]

LOCATIONS = [
    "New York",
    "Los Angeles",
    "Chicago",
    "Houston",
    "Phoenix",
    "Philadelphia",
    "San Antonio",
    "San Diego",
    "Dallas",
    "San Jose",
]

EMAIL_DOMAINS = [
    "example.com",
    "mail.com",
    "test.org",
    "sample.net",
]


def build_row(record_id: int, rng: random.Random) -> List[Union[str, int]]:
    first_name = rng.choice(FIRST_NAMES)
    last_name = rng.choice(LAST_NAMES)
    name = f"{first_name} {last_name}"
    age = rng.randint(18, 90)
    location = rng.choice(LOCATIONS)
    email_domain = rng.choice(EMAIL_DOMAINS)
    email = f"{first_name.lower()}.{last_name.lower()}{record_id}@{email_domain}"
    return [record_id, name, age, email, location]


def generate_csv_files(
    output_dir: Path,
    files_count: int = 5,
    rows_per_file: int = 5_000_000,
    seed: int = 42,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    header = ["id", "name", "age", "email", "location"]

    for file_index in range(1, files_count + 1):
        file_path = output_dir / f"data_{file_index}.csv"
        start_id = (file_index - 1) * rows_per_file + 1

        with file_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)

            for offset in range(rows_per_file):
                record_id = start_id + offset
                writer.writerow(build_row(record_id, rng))

        print(f"Created {file_path} with {rows_per_file} rows")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate CSV files containing synthetic records with "
            "id, name, age, email, and location."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("input"),
        help="Directory where CSV files will be created (default: input)",
    )
    parser.add_argument(
        "--files",
        type=int,
        default=5,
        help="Number of CSV files to create (default: 5)",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=5_000_000,
        help="Rows per CSV file (default: 5,000,000)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for repeatable output (default: 42)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate_csv_files(
        output_dir=args.output_dir,
        files_count=args.files,
        rows_per_file=args.rows,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
