import pandas as pd

# Load the dataset
df = pd.read_csv('gambling_data.csv')

# Check for rows where the 'amount_spend' values are more than 3000 and 'alcohol_consumption' is 'No'
mask = (df['amount_spend'] > 3000) & (df['alcohol_consumption'] == 'No')

# Modify the 'alcohol_consumption' for the selected rows
df.loc[mask, 'alcohol_consumption'] = 'Yes'

# Save the modified dataset to a new file
df.to_csv('gambling.csv', index=False)
