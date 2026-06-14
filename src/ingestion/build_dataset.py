from top_pages import get_top_pages
from page_history import download_history


def main():

    print(
        "\nSTEP 1: Collecting top pages\n"
    )

    pages = get_top_pages(
        n_months=12,
        top_k=500
    )

    pages.to_csv(
        "data/raw/pages.csv",
        index=False
    )

    print(
        "\nSTEP 2: Downloading history\n"
    )

    download_history(
        pages_csv="data/raw/pages.csv",
        output_csv="data/raw/pageviews.csv",
        history_days=1800
    )

    print(
        "\nDataset generation complete."
    )


if __name__ == "__main__":
    main()