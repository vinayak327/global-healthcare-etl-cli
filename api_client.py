import requests
import logging

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_data(self, country, start_date, end_date):
        try:
            logging.info(f"Fetching data from {self.base_url}")
            resp = requests.get(self.base_url)
            resp.raise_for_status()
            all_countries = resp.json()

            country_data = next(
                (c for c in all_countries if c.get("country", {}).get("name", "").lower() == country.lower()),
                None
            )
            if not country_data:
                logging.error(f"No data found for country: {country}")
                return []

            records = []
            for date_str, info in country_data.get("dates", {}).items():
                if start_date <= date_str <= end_date:
                    nc = info.get("new", {})
                    cv = info.get("cumulative", {})
                    records.append({
                        "date": date_str,
                        "country": country_data["country"]["name"],
                        "total_cases": cv.get("cases", 0),
                        "new_cases": nc.get("cases", 0),
                        "total_deaths": cv.get("deaths", 0),
                        "new_deaths": nc.get("deaths", 0)
                    })

            logging.info(f"Fetched {len(records)} days for country {country}")
            return records

        except requests.RequestException as e:
            logging.error(f"API error: {e}")
            return []
