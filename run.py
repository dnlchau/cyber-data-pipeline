from src.crawler.kev_downloader import KEVDownloader
from src.bronze.loader import BronzeLoader
from src.silver.processor import SilverProcessor


RAW_PATH = "data/raw/kev.json"
BRONZE_PATH = "data/bronze/kev.parquet"
SILVER_PATH = "data/silver/kev.parquet"


def main():

    print("=" * 60)
    print("CISA KEV DATA PIPELINE")
    print("=" * 60)

    # Download
    downloader = KEVDownloader()

    downloader.run(RAW_PATH)

    # Bronze
    bronze = BronzeLoader()

    bronze.process(
        RAW_PATH,
        BRONZE_PATH
    )

    # Silver
    silver = SilverProcessor()

    df = silver.process(
        BRONZE_PATH,
        SILVER_PATH
    )

    print()
    print("=" * 60)
    print("PIPELINE FINALIZADO")
    print("=" * 60)
    print(f"Total de CVEs: {len(df)}")
    print(f"Fabricantes: {df['vendorProject'].nunique()}")
    print(f"Produtos: {df['product'].nunique()}")
    print(f"Ransomware: {df['ransomware'].sum()}")
    print("=" * 60)


if __name__ == "__main__":
    main()