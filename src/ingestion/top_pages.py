from collections import defaultdict
from datetime import datetime
import requests
import pandas as pd
from dateutil.relativedelta import relativedelta
import time

USER_AGENT = (
    "WikipediaTrafficForecast/1.0 "
    "(https://github.com/akt052/Wikipedia-Traffic-Forecasting-MLOps-Platform; akshat0akt52@gmail.com)"
)

HEADERS = {"User-Agent": USER_AGENT}

TOP_URL = (
    "https://wikimedia.org/api/rest_v1/"
    "metrics/pageviews/top"
)

EXCLUDED = {
    "Main_Page",
    "-"
}


def get_top_pages(
    n_months: int = 12,
    top_k: int = 500,
):
    page_views = defaultdict(int)

    today = datetime.utcnow().replace(day=1)

    for i in range(n_months):

        month = today - relativedelta(months=i)

        year = month.year
        month_num = month.month

        url = (
            f"{TOP_URL}/"
            f"en.wikipedia.org/"
            f"all-access/"
            f"{year}/"
            f"{month_num:02d}/"
            f"all-days"
        )

        print("Fetching:", url)

        r = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )

        if r.status_code != 200:
            print("Failed:", r.status_code)
            continue

        data = r.json()

        for day in data["items"]:

            for article in day["articles"]:

                page = article["article"]

                if page in EXCLUDED:
                    continue

                if page.startswith("Special:"):
                    continue

                page_views[page] += article["views"]

        time.sleep(0.5)

    pages_df = (
        pd.DataFrame(
            page_views.items(),
            columns=[
                "page_name",
                "total_views_last_12_months"
            ]
        )
        .sort_values(
            "total_views_last_12_months",
            ascending=False
        )
        .head(top_k)
    )

    return pages_df


if __name__ == "__main__":

    pages = get_top_pages()

    pages.to_csv(
        "data/raw/pages.csv",
        index=False
    )

    print(pages.head())
    print(f"Saved {len(pages)} pages")