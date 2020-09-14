import pandas as pd
import statsmodels.api as sm
from sklearn import linear_model

df = pd.read_csv(r'joined_filtered_dataset.csv')
df = df.drop('id', axis=1)
df = df.drop('key_emotion', axis=1)
df = df.dropna()
X = df.drop("perceived_trust", axis=1)
Y = df['perceived_trust']

regr = linear_model.LinearRegression()
regr.fit(X, Y)

print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)

"""model = sm.OLS(Y, X)
results = model.fit()"""

print(results)

result = sm.ols()