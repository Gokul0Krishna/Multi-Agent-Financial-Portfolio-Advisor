# import os
# from dotenv import load_dotenv
# import psycopg2

# DB_PASSWORD = os.getenv('server_password')

# # print(DB_PASSWORD)

# conn = psycopg2.connect(
#     dbname="postgres", user="postgres", password=DB_PASSWORD, host="localhost",port = '5432'
# )
# conn.autocommit = True
# cur = conn.cursor()
# print(cur.execute("SELECT version();"))
# cur.close()
# conn.close()

import pandas as pd
import cvxpy as cp
import numpy as np
from scipy.optimize import minimize

a=pd.DataFrame([[ 0.23, -0.41],
            [ 1.12,  0.56],
            [-0.89,  0.75]])

a=a*0.01

# cov_matrix = a.cov().values
# w = cp.Variable(a.shape[1])
# portfolio_variance = cp.quad_form(w, cov_matrix)
# objective = cp.Minimize(portfolio_variance)
# constraints = [cp.sum(w) == 1, w >= 0]
# problem = cp.Problem(objective, constraints)
# problem.solve()
# print(cov_matrix,'\n')
# print(w,'\n')
# print(portfolio_variance,'\n')
# print(objective,'\n')
# print(constraints,'\n')
# print(problem,'\n')
# weights = w.value
# print("Optimal Weights:", weights,'\n')
# print("Minimum Variance:", problem.value,'\n')

# mu = a.mean().values * 252   # annualized expected returns
# Sigma = a.cov().values * 252  # annualized covariance
# n_assets = a.shape[1]
# rf = 0.04 
# w = cp.Variable(n_assets)
# objective = cp.Maximize((mu - rf) @ w)
# constraints = [
#     cp.quad_form(w, Sigma) <= 1,  # risk normalization
#     cp.sum(w) == 1,               # fully invested
#     w >= 0                        # no short selling
# ]
# problem = cp.Problem(objective, constraints)
# problem.solve()
# weights = w.value
# # expected_return = mu @ weights
# expected_volatility = np.sqrt(weights.T @ Sigma @ weights)
# sharpe_ratio = (expected_return - rf) / expected_volatility

# print("Optimal Weights:", weights)
# print("Minimum Variance:", problem.value,'\n')
# print("Expected Return:", round(expected_return, 4))
# print("Expected Volatility:", round(expected_volatility, 4))
# print("Sharpe Ratio:", round(sharpe_ratio, 4))
a=a*0.01
Sigma = a.cov().values * 252  # annual covariance matrix
n_assets = a.shape[1]
w = cp.Variable(n_assets)
x0 = np.ones(n_assets) / n_assets
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
bounds = [(0, 1) for _ in range(n_assets)]
sigma_p = np.sqrt(w.T @ Sigma @ w)
mrc = Sigma @ w / sigma_p  # marginal risk contribution
rc = w * mrc
result = minimize(rc, x0,
                  args=(Sigma,), method='SLSQP',
                  bounds=bounds, constraints=constraints)
w_opt = result.x
print(w_opt)
