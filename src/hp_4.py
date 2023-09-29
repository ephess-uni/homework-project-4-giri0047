# hp_4.py
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    reformatted_dates = []
    for date_str in old_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        reformatted_date_str = date_obj.strftime('%d %b %Y')
        reformatted_dates.append(reformatted_date_str)
    return reformatted_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError("start must be a string")
    if not isinstance(n, int):
        raise TypeError("n must be an integer")

    start_date = datetime.strptime(start, '%Y-%m-%d')
    date_sequence = [start_date + timedelta(days=i) for i in range(n)]
    return date_sequence


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    if not isinstance(values, list) or not all(isinstance(v, (int, float)) for v in values):
        raise TypeError("values must be a list of numerical values")

    if not isinstance(start_date, str):
        raise TypeError("start_date must be a string")

    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    date_sequence = [start_date_obj + timedelta(days=i) for i in range(len(values))]
    result = [(date, value) for date, value in zip(date_sequence, values)]
    return result


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    def calculate_late_fee(date_returned, date_due):
        if date_returned > date_due:
            days_late = (date_returned - date_due).days
            return days_late * 0.25
        return 0.0

    late_fees = defaultdict(float)
    with open(infile, 'r') as csv_file:
        reader = DictReader(csv_file)
        for row in reader:
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%y')
            date_due = datetime.strptime(row['date_due'], '%m/%d/%y')
            late_fee = calculate_late_fee(date_returned, date_due)
            late_fees[row['patron_id']] += late_fee

    with open(outfile, 'w', newline='') as out_file:
        fieldnames = ['patron_id', 'late_fees']
        writer = DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()
        for patron_id, late_fee in late_fees.items():
            writer.writerow({'patron_id': patron_id, 'late_fees': round(late_fee, 2)})
