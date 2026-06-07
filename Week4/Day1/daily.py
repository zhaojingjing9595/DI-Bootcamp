import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# Tasks:

# 1. Data Preparation:

# Hint 1: Use np.random.uniform(low, high, size) to generate the temperature data.
# print(temp_data)
# Hint 2: Create a DataFrame using pd.DataFrame(data, index, columns) with appropriate index and columns.
# Use NumPy to generate a synthetic dataset representing average monthly temperatures (in degrees Celsius) for 12 months across 10 different cities. The temperatures should range from -5 to 35 degrees.

# Convert this NumPy array into a Pandas DataFrame, adding city names as index and months as columns.
temp_data = np.random.uniform(-5, 35, (10, 12))
temp_data = np.round(temp_data, 0)

months = np.arange(1, 13)
cities = np.array([f'city_{i}' for i in range(1, 11)])
df = pd.DataFrame(temp_data, index=cities, columns=months )
# 2. Data Analysis:

# Hint 1: Calculate the annual average temperature using DataFrame.mean(axis).
# Hint 2: Find the city with the highest and lowest average temperature using idxmax() and idxmin() methods.

# Calculate the annual average temperature for each city.
df['annual_avg'] = df.mean(axis=1)
# Identify the city with the highest and lowest average temperature for the year.
highest_city = df['annual_avg'].idxmax()
lowest_city = df['annual_avg'].idxmin()
print(f'the city with the highest average temperature for the year is {highest_city}')
print(f'the city with the lowest average temperature for the year is {lowest_city}')
print(df)

# 3. Data Visualization:
df.drop('annual_avg', axis=1).plot()
plt.xlabel('Months')
plt.ylabel('Temperature (°C)')
plt.legend(title='Cities')
plt.show()