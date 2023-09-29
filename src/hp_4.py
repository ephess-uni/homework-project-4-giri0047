# hp_4.py
import csv
from datetime import datetime
from collections import defaultdict

def fees_report(infile, outfile):
    with open(infile, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        
        late_fees = defaultdict(float)  # Initialize late fees dictionary
        
        for row in reader:
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%y')  # Parse the date with two-digit year
            date_due = datetime.strptime(row['date_due'], '%m/%d/%y')  # Parse the date_due with two-digit year
            
            # Calculate late fee if the book was returned late
            if date_returned > date_due:
                days_late = (date_returned - date_due).days
                late_fee = days_late * 0.25
                late_fees[row['patron_id']] += late_fee  # Accumulate late fees by patron_id
        
        # Write the summary report to the outfile
        with open(outfile, 'w', newline='') as out_file:
            fieldnames = ['patron_id', 'late_fees']
            writer = csv.DictWriter(out_file, fieldnames=fieldnames)
            writer.writeheader()
            
            for patron_id, late_fee in late_fees.items():
                writer.writerow({'patron_id': patron_id, 'late_fees': round(late_fee, 2)})
