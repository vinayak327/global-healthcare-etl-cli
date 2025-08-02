import pandas as pd
import logging

class DataTransformer:
    def clean_and_transform(self, raw_data, table_type):
        if not raw_data:
            logging.warning("Empty raw data")
            return []

        df = pd.DataFrame(raw_data)
        df['report_date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['report_date'])
        df = df.sort_values('report_date')
        df['country_name'] = df['country']
        df = df.drop(columns=['date', 'country'])
        df = df.drop_duplicates(['country_name', 'report_date'])

        if table_type != 'daily_cases':
            logging.warning("Only 'daily_cases' supported")
            return []

        df = df[['report_date', 'country_name', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']]
        return df.to_dict(orient='records')
