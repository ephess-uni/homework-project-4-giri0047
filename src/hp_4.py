# hp_4.py
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict

def reformat_dates(dates):
    """Reformats a list of date strings from yyyy-mm-dd to dd mmm yyyy."""
    formatted_dates = [datetime.strptime(date, '%Y-%m-%d').strftime('%d %b %Y') for date in dates]
    return formatted_dates

def date_range(start, n):
    """Generates a daily sequence of n datetime objects starting from the given start date."""
    if not isinstance(start, str) or not start:
        raise TypeError("start must be a non-empty string in 'yyyy-mm-dd' format.")
    if not isinstance(n, int) or n <= 0:
        raise TypeError("n must be a positive integer.")

    start_date = datetime.strptime(start, '%Y-%m-%d')
    date_objects = [start_date + timedelta(days=i) for i in range(n)]
    return date_objects

def add_date_range(values, start_date):
    """Adds a daily date range to a list of values, starting from the given start_date."""
    if not values or not all(isinstance(value, (int, float)) for value in values):
        raise ValueError("values must be a non-empty list of numerical values.")
    if not isinstance(start_date, str) or not start_date:
        raise ValueError("start_date must be a non-empty string in 'yyyy-mm-dd' format.")

    date_objects = date_range(start_date, len(values))
    result = [(date_obj, value) for date_obj, value in zip(date_objects, values)]
    return result

def fees_report(infile, outfile):
    """Calculates late fees per patron ID and writes a summary report to outfile."""
    late_fees = defaultdict(float)

    with open(infile, 'r') as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%y')
            days_late = max((date_returned - date_due).days, 0)  # Ensure non-negative late days
            late_fee = days_late * 0.25
            late_fees[row['patron_id']] += late_fee

    with open(outfile, 'w', newline='') as csvfile:
        fieldnames = ['patron_id', 'late_fees']
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for patron_id, fee in late_fees.items():
            writer.writerow({'patron_id': patron_id, 'late_fees': "{:.2f}".format(fee)})

if __name__ == '__main__':
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')
    OUTFILE = 'book_fees.csv'
    fees_report(BOOK_RETURNS_PATH, OUTFILE)
    
    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
