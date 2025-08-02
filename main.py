import argparse
import logging
from api_client import APIClient
from data_transformer import DataTransformer
from mysql_handler import MySQLHandler
from configparser import ConfigParser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

config = ConfigParser()
config.read("config.ini")

api_url = config['api']['base_url']
db_handler = MySQLHandler("config.ini")
api_client = APIClient(api_url)
transformer = DataTransformer()

parser = argparse.ArgumentParser(description="Global Healthcare Data ETL & Analysis CLI")
subparsers = parser.add_subparsers(dest="command")

fetch_parser = subparsers.add_parser("fetch_data", help="Fetch and load data")
fetch_parser.add_argument("country", type=str, help="Country name (e.g. India)")
fetch_parser.add_argument("start_date", type=str, help="Start date (YYYY-MM-DD)")
fetch_parser.add_argument("end_date", type=str, help="End date (YYYY-MM-DD)")

query_parser = subparsers.add_parser("query_data", help="Run predefined queries")
query_subparsers = query_parser.add_subparsers(dest="query_type")

total_cases_parser = query_subparsers.add_parser("total_cases", help="Total cases for a country")
total_cases_parser.add_argument("country", type=str)

daily_parser = query_subparsers.add_parser("daily_trends", help="Daily trend for a metric")
daily_parser.add_argument("country", type=str)
daily_parser.add_argument("metric", type=str)

top_parser = query_subparsers.add_parser("top_n_countries_by_metric", help="Top N countries by metric")
top_parser.add_argument("n", type=int)
top_parser.add_argument("metric", type=str)

subparsers.add_parser("list_tables", help="List tables in the database")
subparsers.add_parser("drop_tables", help="Drop all tables (USE WITH CAUTION)")

def main():
    args = parser.parse_args()

    if args.command == "fetch_data":
        db_handler.create_tables()
        raw = api_client.fetch_data(args.country, args.start_date, args.end_date)
        if not raw:
            logging.error("No data returned from API. Aborting.")
            db_handler.close()
            return

        daily_data = transformer.clean_and_transform(raw, 'daily_cases')
        db_handler.insert_data("daily_cases", daily_data)

    elif args.command == "query_data":
        if args.query_type == "total_cases":
            query = "SELECT SUM(new_cases) FROM daily_cases WHERE country_name = %s"
            result = db_handler.query(query, (args.country,))
            print(f"Total COVID-19 Cases in {args.country}: {result[0][0]}")
        elif args.query_type == "daily_trends":
            query = f"SELECT report_date, {args.metric} FROM daily_cases WHERE country_name = %s ORDER BY report_date"
            results = db_handler.query(query, (args.country,))
            print(f"Date       | {args.metric.capitalize()}")
            print("-" * 30)
            for row in results:
                print(f"{row[0]} | {row[1]}")
        elif args.query_type == "top_n_countries_by_metric":
            query = f"""
                SELECT country_name, SUM({args.metric}) AS total
                FROM daily_cases
                GROUP BY country_name
                ORDER BY total DESC
                LIMIT %s
            """
            results = db_handler.query(query, (args.n,))
            print("Rank | Country        | Total")
            print("-" * 30)
            for i, row in enumerate(results, 1):
                print(f"{i:<4} | {row[0]:<14} | {row[1]}")

    elif args.command == "list_tables":
        tables = db_handler.list_tables()
        print("Tables in DB:")
        for (table,) in tables:
            print(f"- {table}")

    elif args.command == "drop_tables":
        confirm = input("Are you sure you want to drop all tables? (yes/no): ")
        if confirm.lower() == "yes":
            db_handler.drop_tables()
        else:
            print("Aborted.")

    else:
        parser.print_help()

    db_handler.close()

if __name__ == "__main__":
    main()
