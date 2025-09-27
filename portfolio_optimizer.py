import cvxpy as cp
import pandas as pd
class Optimizer():
    def __init__(self):
        self.a=pd.DataFrame([[ 0.23, -0.41],
            [ 1.12,  0.56],
            [-0.89,  0.75]])


    def Minimum_Variance(self,a:pd.DataFrame):
        'Recommend this for clients who want absolute safety first.'
        a=a*0.01
        cov_matrix = a.cov().values
        w = cp.Variable(a.shape[1])
        portfolio_variance = cp.quad_form(w, cov_matrix)
        objective = cp.Minimize(portfolio_variance)
        constraints = [cp.sum(w) == 1, w >= 0]
        problem = cp.Problem(objective, constraints)
        problem.solve()
        weights = w.value
        return problem.value, weights

    def Maximum_Sharpe_Ratio(self,urf,a):
        'Recommend this to investors who want the best bang for their buck'
        mu = a.mean().values * 252   
        Sigma = a.cov().values * 252 
        n_assets = a.shape[1]
        rf = urf 
        w = cp.Variable(n_assets)
        objective = cp.Maximize((mu - rf) @ w)
        constraints = [
            cp.quad_form(w, Sigma) <= 1,  
            cp.sum(w) == 1,               
            w >= 0                        
        ]
        problem = cp.Problem(objective, constraints)
        problem.solve()
        weights = w.value
        return problem.value ,weights
    
    def Sector_Constraints():
        'For ESG portfolios or regulatory compliance'
        