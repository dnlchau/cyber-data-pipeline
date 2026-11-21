import os
import pandas as pd


class SilverProcessor:

    def load(self, path):

        return pd.read_parquet(path)

    def transform(self, df):

        # Remove registros duplicados
        df = df.drop_duplicates(subset="cveID")

        # Limpa textos
        text_columns = [
            "vendorProject",
            "product",
            "vulnerabilityName",
            "shortDescription",
            "requiredAction",
        ]

        for col in text_columns:
            if col in df.columns:
                df[col] = (
                    df[col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

        # Datas
        df["dateAdded"] = pd.to_datetime(df["dateAdded"])
        df["dueDate"] = pd.to_datetime(df["dueDate"], errors="coerce")

        # Novas colunas
        df["year"] = df["dateAdded"].dt.year
        df["month"] = df["dateAdded"].dt.month
        df["month_name"] = df["dateAdded"].dt.month_name()

        # Tamanho da descrição
        df["description_length"] = (
            df["shortDescription"]
            .str.len()
        )

        # Quantidade de CWEs
        df["cwe_count"] = df["cwes"].apply(
            lambda x: len(x) if isinstance(x, list) else 0
        )

        # Possui ransomware?
        df["ransomware"] = (
            df["knownRansomwareCampaignUse"]
            .astype(str)
            .str.upper()
            .eq("KNOWN")
        )

        return df

    def save(self, df, path):

        os.makedirs(
            os.path.dirname(path),
            exist_ok=True
        )

        df.to_parquet(
            path,
            index=False
        )

        print(f"Silver salva em {path}")

    def process(self, input_path, output_path):

        df = self.load(input_path)

        df = self.transform(df)

        self.save(
            df,
            output_path
        )

        return df