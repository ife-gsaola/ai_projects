# -*- coding: utf-8 -*-
"""Workshop_6_NLP.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ytt_3mIMbD9skJjhtLWDt3AdrQB_Oukv
"""

# Commented out IPython magic to ensure Python compatibility.

# Importing necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Step 1: defining the classification models
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

# Importing visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()
# %matplotlib inline
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.express as px
# %matplotlib inline
# %matplotlib notebook

import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
from wordcloud import STOPWORDS

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/DATA MINING/Tweets.csv')
data.head()

data.shape

data.dropna(inplace=True)

data.shape

# Extracting a sample
data = data.sample(n=10000, random_state = 48)
data.reset_index(drop=True, inplace=True)

# Commented out IPython magic to ensure Python compatibility.
# Create stopword list:
stopwords = set(STOPWORDS)
stopwords.update(["br", "href"])
textt = " ".join(review for review in data.tweet)
wordcloud = WordCloud(stopwords=stopwords).generate(textt)
# %matplotlib inline
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
# plt.savefig('wordcloud11.png')
plt.show()

data

data.rename(columns={'sentiment': 'score'}, inplace=True)

# split data - positive and negative sentiment:
positive_data = data[data['score'] == 1]
negative_data = data[data['score'] == 0]

# Word cloud positive
stopwords = set(STOPWORDS)
stopwords.update(["br", "href","good","great"])
## good and great removed because they were included in negative sentiment
pos = " ".join(review for review in positive_data.tweet)
wordcloud2 = WordCloud(stopwords=stopwords).generate(pos)
plt.imshow(wordcloud2, interpolation='bilinear')
plt.axis("off")
plt.show()

neg = " ".join(str(review) for review in negative_data.tweet)
wordcloud3 = WordCloud(stopwords=stopwords).generate(neg)
plt.imshow(wordcloud3, interpolation='bilinear')
plt.axis("off")
plt.savefig('wordcloud33.png')
plt.show()

# review distribution
data['score'] = data['score'].replace({0 : 'negative'})
data['score'] = data['score'].replace({1 : 'positive'})

fig = px.histogram(data, x="score")
fig.update_traces(marker_color="indianred",marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5)
fig.update_layout(title_text='Tweet Sentiment')
fig.show(renderer="colab")

# removing punctuation method 1
def remove_punctuation(text):
    final = "".join(u for u in text if u not in ("?", ".", ";", ":",  "!",'"'))
    return final

data['Text'] = data['tweet'].apply(remove_punctuation)
data = data.dropna(subset=['tweet'])
data['Summary'] = data['tweet'].apply(remove_punctuation)

data.head()

# Stopwords
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
allstopwords = stopwords.words('english')
data['Text']=data.Text.apply(lambda x: " ".join(i for i in x.split() if i not in allstopwords))
data['Summary']=data.Summary.apply(lambda x: " ".join(i for i in x.split() if i not in allstopwords))

# Extracting input and output
X=data['Summary']
# X=df['Text']
y=data['sentiment']

# count vectorizer:
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(token_pattern=r'\b\w+\b')
X = vectorizer.fit_transform(X)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

SVM_classifier = svm.SVC()
RF_classifier = RandomForestClassifier()
KNN_classifier = KNeighborsClassifier()
DT_classifier=DecisionTreeClassifier()
NB_classifier = GaussianNB()
LR_classifier = LogisticRegression()

# Step 2: training the models
SVM_classifier.fit(X_train, y_train)
RF_classifier.fit(X_train, y_train)
KNN_classifier.fit(X_train, y_train)
DT_classifier.fit(X_train, y_train)
LR_classifier.fit(X_train,y_train)
NB_classifier.fit(X_train.toarray(),y_train)

#Step 3: prediction
y_pred1=SVM_classifier.predict(X_test)
y_pred2=RF_classifier.predict(X_test)
y_pred3=KNN_classifier.predict(X_test)
y_pred4=DT_classifier.predict(X_test)
y_pred5=LR_classifier.predict(X_test)
y_pred6=NB_classifier.predict(X_test.toarray())

# This function takes the confusion matrix (cm) from the cell above and produces all evaluation matrix
def confusion_metrics (conf_matrix):

    TP = conf_matrix[1][1]
    TN = conf_matrix[0][0]
    FP = conf_matrix[0][1]
    FN = conf_matrix[1][0]
    print('True Positives:', TP)
    print('True Negatives:', TN)
    print('False Positives:', FP)
    print('False Negatives:', FN)

    # calculate accuracy
    conf_accuracy = (float (TP+TN) / float(TP + TN + FP + FN))

    # calculate mis-classification
    conf_misclassification = 1- conf_accuracy

    # calculate the sensitivity
    conf_sensitivity = (TP / float(TP + FN))
    # calculate the specificity
    conf_specificity = (TN / float(TN + FP))

    # calculate precision
    conf_precision = (TN / float(TN + FP))
    # calculate f_1 score
    conf_f1 = 2 * ((conf_precision * conf_sensitivity) / (conf_precision + conf_sensitivity))
    print('-'*50)
    print(f'Accuracy: {round(conf_accuracy,2)}')
    print(f'Mis-Classification: {round(conf_misclassification,2)}')
    print(f'Sensitivity: {round(conf_sensitivity,2)}')
    print(f'Specificity: {round(conf_specificity,2)}')
    print(f'Precision: {round(conf_precision,2)}')
    print(f'f_1 Score: {round(conf_f1,2)}')

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Assuming classifiers and predictions are defined correctly

# SVM
cm1 = confusion_matrix(y_test, y_pred1, labels=SVM_classifier.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm1, display_labels=SVM_classifier.classes_)
plt.figure(figsize=(10, 8))  # Create a new figure
disp.plot()
plt.title("SVM")
plt.show()

# Random Forest
cm2 = confusion_matrix(y_test, y_pred2, labels=RF_classifier.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm2, display_labels=RF_classifier.classes_)
plt.figure(figsize=(10, 8))  # Create a new figure
disp.plot()
plt.title("Random Forest")
plt.show()

# KNN
cm3 = confusion_matrix(y_test, y_pred3, labels=KNN_classifier.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm3, display_labels=KNN_classifier.classes_)
plt.figure(figsize=(10, 8))  # Create a new figure
disp.plot()
plt.title("KNN")
plt.show()

# Decision Tree
cm4 = confusion_matrix(y_test, y_pred4, labels=DT_classifier.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm4, display_labels=DT_classifier.classes_)
plt.figure(figsize=(10, 8))  # Create a new figure
disp.plot()
plt.title("Decision Tree")
plt.show()

# Logistic Regression
cm5 = confusion_matrix(y_test, y_pred5, labels=LR_classifier.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm5, display_labels=LR_classifier.classes_)
plt.figure(figsize=(10, 8))  # Create a new figure
disp.plot()
plt.title("Logistic Regression")
plt.show()

# Naive Bayes
cm6 = confusion_matrix(y_test, y_pred6, labels=NB_classifier.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm6, display_labels=NB_classifier.classes_)
plt.figure(figsize=(10, 8))  # Create a new figure
disp.plot()
plt.title("Naive Bayes")
plt.show()

#printing the evaluation metrics for all classifiers
print('SVM metrics\n')
confusion_metrics(cm1)
print('\n\n')
print('RF metrics\n')
confusion_metrics(cm2)
print('\n\n')
print('KNN metrics\n')
confusion_metrics(cm3)
print('\n\n')
print('DT metrics\n')
confusion_metrics(cm4)
print('\n\n')
print('LR metrics\n')
confusion_metrics(cm5)
print('\n\n')
print('NB metrics\n')
confusion_metrics(cm6)
print('\n\n')

"""
The provided code conducts sentiment analysis on a dataset of tweets using six different classifiers: Support Vector Machine (SVM), Random Forest, K-Nearest Neighbors (KNN), Decision Tree, Logistic Regression, and Naive Bayes. Here's a breakdown of what the code accomplishes:

##Data Loading and Preprocessing:

The code imports necessary libraries and loads the tweet dataset from Google Drive.
It preprocesses the data by handling missing values, extracting a sample for faster processing, and visualizing word clouds for both positive and negative sentiments.

##Data Exploration and Visualization:

It explores the distribution of sentiment classes through histograms.
Word clouds are generated to visualize frequent words associated with positive and negative sentiments.

##Text Preprocessing:

Punctuation is removed from the tweet texts.
Stopwords are removed from the text using NLTK's stopwords corpus.


##Feature Extraction:

The text data is transformed into numerical features using CountVectorizer.


##Model Building:

Six classification models are initialized: SVM, Random Forest, KNN, Decision Tree, Logistic Regression, and Naive Bayes.
The models are trained on the training data.


##Model Evaluation:

Each trained model makes predictions on the test data.
Confusion matrices are generated for each model to visualize the performance.
Evaluation metrics such as accuracy, misclassification rate, sensitivity, specificity, precision, and F1-score are calculated and printed for each model.



##word count: 218
"""