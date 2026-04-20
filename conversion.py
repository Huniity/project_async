import pandas as pd
import os
from multiprocessing import Pool


def convert_csv_to_json(csv_file, json_file):
    df = pd.read_csv(csv_file)
    df.to_json(json_file, orient='records', lines=True)


if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    path = 'input'
    files = sorted(os.listdir(path))

    csv_files = [os.path.join(path, f) for f in files if f.endswith('.csv')]
    json_files = [os.path.join('output', f.replace('.csv', '.json')) for f in files if f.endswith('.csv')]

    args = list(zip(csv_files, json_files))

    with Pool(4) as pool:
        pool.starmap(convert_csv_to_json, args)