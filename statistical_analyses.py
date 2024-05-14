import pingouin as pg
import pandas as pd
import scipy.stats
import numpy as np
import pwlf
from scipy.stats import linregress
from scipy.stats import zscore
from statsmodels.formula.api import glm
import statsmodels.api as sm

def get_r(n, alpha):

    t_stat = np.abs(scipy.stats.t.ppf(alpha/2, n-2))
    gamma = (t_stat**2)/(n-2)
    r = np.sqrt(gamma/(1+gamma))

    return r

def get_mediation_analysis(df, xvar, meds, yvar, covs):
    
    df = df.copy(deep=True)
    
    if len(covs) > 0:
        med_pg = pg.mediation_analysis(df, x=xvar, m=meds, y=yvar, seed=42, 
                                       covar=covs,  n_boot=10000, alpha=0.05).round(200)
    else:
        med_pg = pg.mediation_analysis(df, x=xvar, m=meds, y=yvar, seed=42,
                                        n_boot=10000, alpha=0.05).round(200)
             
    return med_pg


def get_partial_corr(df, xvar, yvar, covs=[], method='spearman'):
    
    df = df.copy(deep=True)
    
    if len(covs) > 0:
        pg_corr = pg.partial_corr(data=df, x=xvar, y=yvar, covar=covs, method=method)
    else:
        pg_corr = pg.partial_corr(data=df, x=xvar, y=yvar, method=method)
    
    return pg_corr


def get_net_mean(df, rois, nets):
    
    rois = rois.copy(deep=True)
    df = df.copy(deep=True)
    
    if isinstance(nets,list):
        net_indices = rois.loc[rois['Network'].isin(nets)].index
    else:
        net_indices = rois.loc[rois['Network'] == nets].index

    net_df = df[map(str, net_indices)]
    net_mean_df = net_df.mean(axis=1)/len(net_indices)
    
    return net_mean_df


def get_ancova(df, feature_index, between, covar='MoCA_Edu'):
    
    df = df.copy(deep=True)
    aov = pg.ancova(dv=feature_index, between=between, data=df, covar=covar)    
    
    return aov 

    
def get_piecewise_regression(data,  xvar, yvar):
    
    data = data.copy(deep=True)
    x = data[xvar]
    y = data[yvar]
    
    my_pwlf = pwlf.PiecewiseLinFit(x,y)
    breaks = my_pwlf.fit(2)
    print(breaks)
    
    x_hat = np.linspace(x.min(), x.max(), 100)
    y_hat = my_pwlf.predict(x_hat)
    
    return breaks, y_hat


def regress_by_cov(data, var, covs):
    
    data = data.copy(deep=True)   
    
    data[var] = zscore(data[var], nan_policy='omit')
    
    for cov in covs:
        data[cov] = zscore(data[cov], nan_policy='omit')
        cov_slope, cov_int, _, _, _ = linregress(data[var], data[cov])  
        cov_trend = data[cov]*cov_slope + cov_int
        data[var] = data[var] - cov_trend  
        
    return data[var]


def estimate_cog(data, features, target):
    
    data = data.copy(deep=True)
    cols = features.copy()
    cols.append(target)
    data.dropna(subset=cols, inplace=True)
    data = data[cols]
    
    #data = data.loc[data['Processing_Speed'] < 100]
    
    stripped_features = []
    for feat in features:
        renamed_feat = ''.join([i for i in feat if not i.isdigit()])
        renamed_feat = renamed_feat.replace('-', '').replace(' ','')
        
        data.rename(columns={feat:renamed_feat}, inplace=True)
        stripped_features.append(renamed_feat)
    
    cols = stripped_features.copy()
    cols.append(target)
    
    for col in cols:
        data[col] = zscore(data[col], nan_policy='omit')
        #data[col] = minmax_scale(data[col], feature_range=(0,1))
        
    
    formula = target +' ~ '
    for feature in stripped_features:
        formula = formula + feature + ' + '
        
    formula = formula[:-3]
        
    
    model = glm(formula, data=data, family=sm.families.Gaussian()).fit()
    print(model.summary())
    
    print(model.aic)
    
    predictions = model.predict(data)
    
    return model, predictions, data[target]
