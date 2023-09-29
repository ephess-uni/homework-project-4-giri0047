# hp_4.py
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict

def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = []
    for date_str in old_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        new_date_str = date_obj.strftime('%d %b %Y')
        new_dates.append(new_date_str)
    return new_dates

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        raise TypeError("start must be a string, and n must be an integer")

    start_date = datetime.strptime(start, '%Y-%m-%d')
    date_list = [start_date + timedelta(days=i) for i in range(n)]
    return date_list

def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    date_list = date_range(start_date, len(values))
    result = [(date, value) for date, value in zip(date_list, values)]
    return result

def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    late_fees = defaultdict(float)

    with open(infile, 'r') as csv_file:
        csv_reader = DictReader(csv_file)
        for row in csv_reader:
            date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%y')
            if date_returned > date_due:
                days_late = (date_returned - date_due).days
                late_fee = days_late * 0.25
                late_fees[row['patron_id']] += late_fee

    with open(outfile, 'w', newline='') as csv_output:
        fieldnames = ['patron_id', 'late_fees']
        csv_writer = DictWriter(csv_output, fieldnames=fieldnames)
        csv_writer.writeheader()
        for patron_id, fee in late_fees.items():
            csv_writer.writerow({'patron_id': patron_id, 'late_fees': "{:.2f}".format(fee)})

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

