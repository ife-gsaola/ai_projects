# -*- coding: utf-8 -*-
"""Linear Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QfOXYc5AP2e9SvbUG5yheB_8f-FB950G
"""

#Importing necessary libraries.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()
from sklearn.linear_model import LinearRegression

#uploading data through google colab

from google.colab import files
uploaded = files.upload()

data = pd.read_csv("houseprice_data.csv")
data.head()

#statistical investigation on the data
data.describe(include='all')

# data['yr_built'].isnull().sum()
data['yr_renovated'].count()

#Check for multicolinearity between the features. This is to ensure that one of any two
#---variables that explains themselves are dropped.

cor = data.corr()
plt.figure(figsize=(15,7))
sns.heatmap(cor, annot=True, cmap = plt.cm.CMRmap_r)
plt.show ()

"""# Feature Engineering"""

!pip install uszipcode

#getting city name using the search engine function in uszipcode

from uszipcode import SearchEngine
# Create a search engine instance
search = SearchEngine()

# Function to get city name from zip code
def get_city_name(zip_code):
    try:
        result = search.by_zipcode(zip_code)
        return result.major_city
    except Exception as e:
        return f"Error: {e}"

# Apply the function to the 'zip_code' column and create a new 'city_name' column
data['city_name'] = data['zipcode'].apply(get_city_name)

#Categorizing the year bult values for further analysis
bin_edges = [1900, 1950, 2000, 2015]

# Create a new column with the categorized years
bin_labels = ['1900-1950', '1950-2000', '2000-2015']
data['year_built_category'] = pd.cut(data['yr_built'], bins=bin_edges, labels=bin_labels, right=False)

"""# Data Visualization

**In the graph below,houses built between 2000-2015 are more expensive.Further analysis is carried out to find out if these houses are more in number.**
"""

sns.set(style="whitegrid")

# Plotting the bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x='year_built_category', y='price', data=data, ci=None)
plt.title('Price vs Year Category')
plt.xlabel('Year Built Category')
plt.ylabel('Price')
plt.show()

"""**Also, Medina has the most expensive houses among the cities in the data, despite having the list number of houses in the next plot. According to google search, Medina, Ohio's cost of living is 4% higher than the national average (https://www.payscale.com/cost-of-living-calculator/Ohio-Medina**"""

sns.set(style="whitegrid")

# Plotting the bar chart
plt.figure(figsize=(10, 6))
barplot = sns.barplot(x='city_name', y='price', data=data, ci=None)
plt.title('Price vs city name')
plt.xlabel('city name')
plt.ylabel('Price')

# Rotate x-axis labels
barplot.set_xticklabels(barplot.get_xticklabels(), rotation=45, horizontalalignment='right')

plt.show()

# sns.set(style="whitegrid")

# Plotting the bar chart of year categories
plt.figure(figsize=(8, 5))
countplot = sns.countplot(x='city_name', data=data, palette='viridis')
plt.title('Distribution of city name')
plt.xlabel('city name')
plt.ylabel('Count')
countplot.set_xticklabels(barplot.get_xticklabels(), rotation=45, horizontalalignment='right')

plt.show()

"""**In the bar chart below, houses in Medina and other expensive places are built in between 1900-1950, yet, they are expensive than the houses built between 2000-2015 in Seattle**

**Looking up Seattle vs Medina, here is what I found on google "The whole Seattle metropolitan area is a relatively expensive one, but Medina is the most expensive one. Billionaires aside, the average income in Medina is close to $190,000 dollars, which makes it difficult for those with an average income to live in Medina." (https://neighborsmovingseattle.com/living-in-medina-washington-whats-it-really-like)**





"""

plt.figure(figsize=(15, 6))

# Plotting the count of year categories for each city
sns.countplot(x='city_name', hue='year_built_category', data=data, palette='viridis')

plt.title('Count of Year Categories for Each City')
plt.xlabel('City names')
plt.ylabel('Count')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Show legend
plt.legend(title='Year Category')

plt.show()

sns.set(style="whitegrid")

# Plotting the scatter plot with color-coded points
plt.figure(figsize=(10, 6))
sns.scatterplot(x='yr_built', y='price', hue='year_built_category', data=data, palette='viridis')
plt.title('price vs Years with Year Category')
plt.xlabel('Years')
plt.ylabel('price')
plt.show()

# sns.set(style="whitegrid")

# Plotting the bar chart of year categories
plt.figure(figsize=(8, 5))
sns.countplot(x='year_built_category', data=data, palette='viridis')
plt.title('Distribution of Year Categories')
plt.xlabel('Year Category')
plt.ylabel('Count')
plt.show()

#One of the assumptions of OLS is that there must be no multicorrelation between variables
 #Therefore, multi correlated variables are removed to reduce the number of features.

 Xfeat = data.drop(['price','year_built_category','city_name'], axis=1)

 #function to detect multi correlation
 def correlation (dataset, threshold):
    col_corr = set()
    corr_matrix = Xfeat.corr()
    for i in range(len(corr_matrix.columns)):
      for j in range(i):
        if abs(corr_matrix.iloc[i,j]) > threshold:
          colname = corr_matrix.columns[i]
          col_corr.add(colname)
    return col_corr

corr_features = correlation(Xfeat, 0.6)
len(set(corr_features))
corr_features

"""# Developing Regression Model"""

X = Xfeat.drop(corr_features, axis=1)
y = data['price']

#spliting data into test and train data to avoid overfitting
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0 )

"""**From the scatter plot below, it is observed that faily linear relationship betwen price and all variables except "View".**"""

f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, sharey=True, figsize =(15,3))
ax1.scatter(X_train['bedrooms'], y_train)
ax1.set_title('Price and Bedrooms')

ax2.scatter(X_train['bathrooms'], y_train)
ax2.set_title('Price and bathroom')

ax3.scatter(X_train['view'], y_train)
ax3.set_title('Price and view')

ax4.scatter(X_train['sqft_basement'], y_train)
ax4.set_title('Price and Basement')


plt.show()

#declaring the linear regression model
linear_model = LinearRegression()
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Fit the model on the training data
linear_model.fit(X_train, y_train)

# Make predictions on the test data
predictions = linear_model.predict(X_test)

# Evaluating the model effectiveness
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)

# Print the evaluation metrics
print(f'Mean Squared Error (MSE): {mse}')
print(f'R-squared: {r2}')
print(f'Mean Absolute Error (MAE): {mae}')

slope, intercept = np.polyfit(predictions, y_test, 1)
line = slope * predictions + intercept

# Create a scatter plot with the regression line
plt.figure(figsize=(10, 6))
plt.scatter(predictions, y_test, color='pink', label='Actual Data')
plt.plot(predictions, line, color='blue', label='Regression Line')
plt.title('Actual vs Predicted Data with Regression Line')
plt.xlabel('Predictions')
plt.ylabel('Actual Data')
plt.legend()
plt.show()

X_test.shape, y_test.shape

"""# Building another model with different parameter

**Testing another model by passing in more features and adjusting the model parameters**
"""

#increasing the features passing in the whole data

X = data.drop(['price','year_built_category','city_name'], axis=1)
y = data['price']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100 )

# scalling the data to keep all data points close to each other for  model improvement

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

#declaring the linear regression model
linear_model = LinearRegression(fit_intercept=True,copy_X=True, n_jobs=None, positive=False)
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Fit the model on the training data
linear_model.fit(X_train_scaled, y_train)

# Make predictions on the test data
predictions = linear_model.predict(X_test_scaled)

# Evaluating the model effectiveness
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)

# Print the evaluation metrics
print(f'Mean Squared Error (MSE): {mse}')
print(f'R-squared: {r2}')
print(f'Mean Absolute Error (MAE): {mae}')

slope, intercept = np.polyfit(predictions, y_test, 1)
line = slope * predictions + intercept

# Create a scatter plot with the regression line
plt.figure(figsize=(10, 6))
plt.scatter(predictions, y_test, color='red', label='Actual Data')
plt.plot(predictions, line, color='blue', label='Regression Line')
plt.title('Actual vs Predicted Data with Regression Line')
plt.xlabel('Predictions')
plt.ylabel('Actual Data')
plt.legend()
plt.show()