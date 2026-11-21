import json
import os


class JsonWriter:

    def save(self, data, path):

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

        print(f"{len(data)} registros salvos em {path}")