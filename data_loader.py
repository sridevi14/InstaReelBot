import pandas as pd
import re
from datetime import date

def load_google_sheet(url):
    """Load data from Google Sheets as CSV"""
    sheet_id = re.search(r"/d/([a-zA-Z0-9-_]+)", url).group(1)
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return pd.read_csv(csv_url)

def get_today_content(sheet_url):
    """Get content for today's date from Google Sheets"""
    df = load_google_sheet(sheet_url)
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    today = date.today()

    today_rows = df[df["Date"] == today]

    if today_rows.empty:
        return None, None, today

    row = today_rows.iloc[0]
    overlay_text = str(row["OverlayText"])
    caption = str(row["Caption"])

    return overlay_text, caption, today