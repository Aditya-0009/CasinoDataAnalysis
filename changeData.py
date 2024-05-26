import csv

# Open the CSV file for reading
with open('gambling_data.csv', 'r', newline='') as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Modify the data as needed
for row in data:
    amount_spent = float(row['Amount_spent'])
    winning_history = row['Winning_history']
    if amount_spent > 3000 and winning_history != 'Yes':
        row['Winning_history'] = 'Yes'

# Open the same CSV file for writing (this will overwrite the file)
fieldnames = reader.fieldnames

with open('gambling_data.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

# The file has been modified, and winning history values have been updated for individuals with Amount_spent > 3000
