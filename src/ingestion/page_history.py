from datetime import datetime, timedelta
import requests
import pandas as pd
import time

USER_AGENT = (
    "WikipediaTrafficForecast/1.0 "
    "(https://github.com/akt052/Wikipedia-Traffic-Forecasting-MLOps-Platform; akshat0akt52@gmail.com)"
)

HEADERS = {"User-Agent": USER_AGENT}

ARTICLE_URL = (
    "https://wikimedia.org/api/rest_v1/"
    "metrics/pageviews/per-article"
)


def download_history(
    pages_csv="data/raw/pages.csv",
    output_csv="data/raw/pageviews.csv",
    history_days=1800
):

    pages_df = pd.read_csv(pages_csv)

    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=history_days)

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    records = []

    total_pages = len(pages_df)

    for idx, page in enumerate(
        pages_df["page_name"]
    ):

        print(
            f"[{idx+1}/{total_pages}] "
            f"{page}"
        )

        page_encoded = (
            requests.utils.quote(page)
        )

        url = (
            f"{ARTICLE_URL}/"
            f"en.wikipedia.org/"
            f"all-access/"
            f"user/"
            f"{page_encoded}/"
            f"daily/"
            f"{start_str}/"
            f"{end_str}"
        )

        try:

            r = requests.get(
                url,
                headers=HEADERS,
                timeout=30
            )

            if r.status_code != 200:
                print(
                    f"Failed: {page}"
                )
                continue

            data = r.json()

            for item in data["items"]:

                records.append({
                    "page_name": page,
                    "date": item["timestamp"][:8],
                    "views": item["views"]
                })

        except Exception as e:

            print(
                f"Error for {page}: {e}"
            )

        time.sleep(0.3)

    df = pd.DataFrame(records)

    df["date"] = pd.to_datetime(
        df["date"],
        format="%Y%m%d"
    )

    df.to_csv(
        output_csv,
        index=False
    )

    return df


if __name__ == "__main__":

    df = download_history()

    print(df.head())
    print("Rows:", len(df))