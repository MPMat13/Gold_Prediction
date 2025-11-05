import pandas as pd
import yfinance as yf
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class DataScrapper:
    def __init__(self, tickers: dict):
        """
        tickers: dict { 'friendly_name': 'YF_code' }
        """
        self.tickers = tickers
        self.data = None
        self.df = None

    def __str__(self):
        return f"Tickers mapping:\n{self.tickers}"

    def download(self, start_date: str, end_date: str):
        """
        Download data for all tickers at once. Falls back to per-ticker download if needed.
        """
        self.start_date = start_date
        self.end_date = end_date
        logger.info("Starting bulk data download...")

        try:
            codes = list(self.tickers.values())

            data = yf.download(
                codes,
                start=start_date,
                end=end_date,
                group_by='ticker',
                auto_adjust=True,
                progress=True
            )

            logger.info("Bulk download completed. Processing data...")
            self.processed_data(data)

        except Exception:
            logger.error("Bulk download failed. Attempting fallback method...", exc_info=True)
            self.fallback()

    def fallback(self):
        """
        Download tickers one by one (slower but more robust).
        """
        logger.info("Running fallback download (per ticker)...")
        fallback_data = {}

        for name, code in self.tickers.items():
            try:
                logger.info(f"Downloading {code}...")
                temp_data = yf.download(code, start=self.start_date, end=self.end_date, progress=False)
                if not temp_data.empty:
                    if "Adj Close" in temp_data.columns:
                        fallback_data[name] = temp_data["Adj Close"]
                    else:
                        fallback_data[name] = temp_data["Close"]
                    logger.info(f"Successfully downloaded {code}")
                else:
                    logger.warning(f"No data for {code}")
                time.sleep(1)  # avoid hitting API limits
            except Exception:
                logger.error(f"Failed to download {code}", exc_info=True)

        if fallback_data:
            self.create_df(fallback_data, filename="financial_data_fallback")
        else:
            logger.error("No data downloaded in fallback method.")

    def processed_data(self, raw_data: pd.DataFrame):
        """
        Extract Adjusted Close/Close prices into a clean DataFrame.
        """
        processed_data = {}
        for name, ticker in self.tickers.items():
            if ticker in raw_data:
                if "Adj Close" in raw_data[ticker]:
                    processed_data[name] = raw_data[ticker]["Adj Close"]
                else:
                    processed_data[name] = raw_data[ticker]["Close"]
            else:
                logger.warning(f"No data available for {ticker}")

        self.create_df(processed_data, filename="financial_data")

    def create_df(self, data: dict, filename: str):
        """
        Create cleaned DataFrame and save to CSV.
        """
        df = pd.DataFrame(data)
        df = df.dropna(how="all").ffill()
        self.df = df
        self.save_csv(df, filename)

    def save_csv(self, df: pd.DataFrame, filename: str):
        """
        Save dataframe to CSV with logging.
        """
        csv_filename = f"data/{filename}_{self.start_date}_{self.end_date}.csv"
        df.to_csv(csv_filename, encoding="utf-8")

        logger.info(f"Data saved to {csv_filename}")
        logger.info(f"Dataset shape: {df.shape}")
        logger.info(f"Columns: {df.columns.tolist()}")
        logger.info(f"Date range: {df.index.min()} to {df.index.max()}")
        logger.info("Columns included:")
        for col in df.columns:
            logger.info(f"- {col}")
