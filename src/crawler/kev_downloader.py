import os
import requests


class KEVDownloader:

    URL = (
        "https://www.cisa.gov/sites/default/files/feeds/"
        "known_exploited_vulnerabilities.json"
    )

    def download(self):

        print("Baixando catálogo KEV da CISA...")

        response = requests.get(
            self.URL,
            timeout=60
        )

        response.raise_for_status()

        return response.json()

    def save(self, data, output_path):

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            import json

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(f"Arquivo salvo em {output_path}")

    def run(self, output_path):

        data = self.download()

        self.save(
            data,
            output_path
        )

        return data