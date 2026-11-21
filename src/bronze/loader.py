import os
import json
import pandas as pd


class BronzeLoader:

    def load_json(self, path):

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data["vulnerabilities"]

    def transform(self, vulnerabilities):

        df = pd.DataFrame(vulnerabilities)

        return df

    def save_parquet(self, df, path):

        os.makedirs(
            os.path.dirname(path),
            exist_ok=True
        )

        df.to_parquet(
            path,
            index=False
        )

        print(f"Bronze salva em {path}")

    def process(self, input_path, output_path):

        vulnerabilities = self.load_json(input_path)

        df = self.transform(vulnerabilities)

        self.save_parquet(
            df,
            output_path
        )

        return df