import pandas as pd
import numpy as np
import random

# Set a random seed for reproducibility
np.random.seed(0)
random.seed(42)

# Function to generate age values with specified distribution
def generate_age_values(n, p_28_38=0.7):
    num_age_values_28_to_38 = int(n * p_28_38)
    age_values = (
        [random.randint(28, 38) for _ in range(num_age_values_28_to_38)] +
        [random.randint(18, 27) for _ in range((n - num_age_values_28_to_38) // 2)] +
        [random.randint(39, 85) for _ in range(n - num_age_values_28_to_38 - (n - num_age_values_28_to_38) // 2)]
    )
    random.shuffle(age_values)
    return age_values

# Function to generate gender values with specified distribution
def generate_gender_values(n, p_males=0.5):
    num_males = int(n * p_males)
    num_females = n - num_males
    gender_values = ['Male'] * num_males + ['Female'] * num_females
    random.shuffle(gender_values)
    return gender_values

# Function to generate location values with specified distribution
def generate_location_values(n, p_urban=0.7):
    num_urban = int(n * p_urban)
    num_rural = n - num_urban
    location_values = ['Urban'] * num_urban + ['Rural'] * num_rural
    random.shuffle(location_values)
    return location_values

# Function to generate Frequency_of_visits values with specified distribution
def generate_frequency_values(n, p_20_30=0.8):
    num_20_to_30 = int(n * p_20_30)
    num_other_values = n - num_20_to_30
    frequency_values = [random.randint(1, 19) for _ in range(num_other_values)]
    frequency_values += [random.randint(20, 30) for _ in range(num_20_to_30)]
    random.shuffle(frequency_values)
    return frequency_values

# Define the number of data points
n = 350  # Adjust the total number of data points as needed

# Generate age, gender, location, and frequency values using the functions
age_values = generate_age_values(n)
gender_values = generate_gender_values(n)
location_values = generate_location_values(n)
frequency_values = generate_frequency_values(n)

# Create a dictionary to store the data
data = {
    'Age': age_values,
    'Gender': gender_values,
    'Income': np.random.randint(20000, 100000, n),
    'Education': np.random.choice(['High School', 'College', 'Bachelor', 'Masters', 'PhD'], n),
    'Location': location_values,
    'Frequency_of_visits': frequency_values,
    'Gambling_experience': np.random.randint(1, 10, n),
    'Types_of_games': np.random.choice(['Slots', 'Roulette', 'Poker', 'Blackjack', 'Baccarat', 'Craps', 'Keno', 'Video Poker'], n),
    'Duration_of_play': np.random.randint(30, 600, n),
    'Winning_history': np.random.choice(['Yes', 'No'], n),
    'Alcohol_consumption': np.random.choice(['Yes', 'No'], n),
    'Amount_spent': np.random.uniform(50, 5000, n)
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# Calculate the mean "Amount Spent" for male and female groups
male_mean_amount_spent = df[df['Gender'] == 'Male']['Amount_spent'].mean()
female_mean_amount_spent = df[df['Gender'] == 'Female']['Amount_spent'].mean()

# Adjust the "Amount Spent" values for males
# Make sure that males' average spending is greater than females'
df.loc[df['Gender'] == 'Male', 'Amount_spent'] += male_mean_amount_spent - female_mean_amount_spent

# Save the DataFrame to a CSV file in the same folder as the script
file_path = 'gambling_data.csv'
df.to_csv(file_path, index=False)

print(f'CSV file saved at: {file_path}')
