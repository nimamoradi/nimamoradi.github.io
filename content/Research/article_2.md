Title: Logistic Regression Example
Date: 2019-06-10
Tags: Python,Machine Learning, Regression, Logic, Nima Moradi
Category: Research
Summary: An example of logistic regression using python

# Logistic Regression

Logistic Regression is a binary classification algorithm that predicts with the given input how much is probable that output is either 1 or 0. Regression analysis is a method that wants to find a relation between one independent variable and one dependent variable.

for instance, we are the owner of a gym club and we want to have weight loss program for are attendants we have gathered data of exercise hour and weight loss in a single month and we want to predict how much time is a need for our newcomer john to loss 5 pounds in a month.
![here is an approach to the problem](https://raw.githubusercontent.com/nimamoradi/ML-notebook/5fb934ad6fd19a4f17e96be2dd7a72b33d323851/classification/images/linear-regression.jpg)
gym owner will try to draw a line we yield to least sum of squares to find a pattern to between weight loss and exercise hour
as we can we this equation can be modeled using a linear equation

ŷ = b0 + b1x
<br>
<br>
the problem that we have is gym owner wants to predict that John could achieve more than 5-pound loss with 20 hours a month for probability value should be always between 0 up to 1 whereas weight loss can be any number here we look logistic regression that uses sigmoid function in order to bound linear regression to 0 or 1


![sigmoid function diagram](https://github.com/nimamoradi/ML-notebook/blob/master/classification/images/sigmoid.jpg?raw=1)


ŷ = σ(b0 + b1x)

### we will classifiy liris with logistic regression

<pre>
<code>
from sklearn.linear_model import LogisticRegression

from sklearn.model_selection  import train_test_split
from sklearn.metrics import accuracy_score
</code>
</pre>
### For working better with data
<pre>
<code>
import pandas as pd
import numpy as np 
</code>
</pre>
### For visualizeing data
<pre>
<code>
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
</code>
</pre>

### Loading dataset
sklearn has a built-in tool for loading common datasets for educational purposes we used direct loading from CSV
<pre>
<code>
dataset = pd.read_csv('./datasets/Iris.csv')
X = dataset.iloc[:, 0:4 ].values
Y = dataset.iloc[:, 4].values
</code>
</pre>
### Splitting dataset into training and testing
<pre>
<code>
X_train, X_test, y_train, y_test = train_test_split(X, Y, 
                                                    test_size=0.25, 
                                                    random_state=0)
</code>
</pre>
### define and fit model
<pre>
<code>
clf = LogisticRegression(random_state=0, solver='lbfgs',
                          multi_class='multinomial').fit(X_train, y_train)
print(clf.score(X, Y))
</code>
</pre>
### Predicting the Test set results
<pre>
<code>
y_pred = clf.predict(X_test)
print(y_pred)

# accuracy on test set
accuracy_score(y_test, y_pred, normalize=True, sample_weight=None)
</code>
</pre>