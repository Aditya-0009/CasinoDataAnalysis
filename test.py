import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset (replace 'your_data.csv' with your actual data file)
data = pd.read_csv("gambling_data.csv")

# Convert the 'Duration_of_play' column from minutes to hours
data['Duration_of_play_hours'] = data['Duration_of_play'] / 60

# Sidebar with user inputs
st.sidebar.title("Data Analysis App")

selected_category = st.sidebar.selectbox("Choose the category you want to compare with Amount Spent:", data.columns)

# If the selected column is numeric, display a range slider for user input
if selected_category in ["Income", "Age", "Frequency_of_visits", "Gambling_experience", "Duration_of_play_hours"]:
    # Define custom bins for income, age, frequency of visits, gambling experience, or duration of play (in hours)
    if selected_category == "Income":
        bins = [0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, float('inf')]
    elif selected_category == "Age":
        bins = [10 * i for i in range(int(data['Age'].min()) // 10, (int(data['Age'].max()) // 10) + 2)]  # Age range in intervals of 10
    elif selected_category == "Frequency_of_visits":
        bins = [i for i in range(0, int(data['Frequency_of_visits'].max()) + 5, 5)]
    elif selected_category == "Gambling_experience":
        bins = [i for i in range(0, int(data['Gambling_experience'].max()) + 2, 2)]
    else:  # selected_category == "Duration_of_play_hours"
        bins = [i for i in range(0, int(data['Duration_of_play_hours'].max()) + 2, 1)]

    selected_range = st.sidebar.slider(f"Select a range for {selected_category}:", float(data[selected_category].min()), float(data[selected_category].max()), (float(data[selected_category].min()), float(data[selected_category].max())))
else:
    selected_factors = st.sidebar.multiselect(f"Choose the factors available for {selected_category}:", data[selected_category].unique())

# Data analysis and graph generation
if selected_category in ["Income", "Age", "Frequency_of_visits", "Gambling_experience", "Duration_of_play_hours"]:
    # Use custom bins for income, age, frequency of visits, gambling experience, or duration of play (in hours)
    filtered_data = data[(data[selected_category] >= selected_range[0]) & (data[selected_category] <= selected_range[1])]
else:
    filtered_data = data[data[selected_category].isin(selected_factors)]

if not filtered_data.empty:
    # If the selected category is "Income", "Age", "Frequency_of_visits", "Gambling_experience", or "Duration_of_play_hours", create a new column for income, age, frequency of visits, gambling experience, or duration of play (in hours) ranges
    if selected_category in ["Income", "Age", "Frequency_of_visits", "Gambling_experience", "Duration_of_play_hours"]:
        range_label = "IncomeRange" if selected_category == "Income" else ("AgeRange" if selected_category == "Age" else ("FrequencyRange" if selected_category == "Frequency_of_visits" else ("GamblingExperienceRange" if selected_category == "Gambling_experience" else "DurationOfPlayRange")))
        filtered_data[range_label] = pd.cut(filtered_data[selected_category], bins=bins, labels=[f"{lower}-{upper}" for lower, upper in zip(bins[:-1], bins[1:])])
        selected_category = range_label  # Update the selected category to the new column

    # Group and calculate the mean amount spent for each factor
    factor_mean_spent = filtered_data.groupby(selected_category)['Amount_spent'].mean()

    # Find the index of the factor with the highest average amount spent
    max_spent_index = factor_mean_spent.idxmax()

    # Create a bar plot
    fig, ax = plt.subplots(figsize=(10, 6))  # Increase the figure size
    bars = ax.bar(factor_mean_spent.index, factor_mean_spent)

    # Highlight the bar with the highest value in red
    for i, bar in enumerate(bars):
        if factor_mean_spent.index[i] == max_spent_index:
            bar.set_color('red')

    plt.xlabel(selected_category)
    plt.ylabel("Average Amount Spent")
    plt.title(f"Average Amount Spent by {selected_category}")

    # Rotate the x-axis labels
    plt.xticks(rotation=45)

    # Display the plot
    st.pyplot(fig)

else:
    st.warning(f"No data available for the selected category {selected_category}.")
