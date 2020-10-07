#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    This script aims at constructing a logistic regression model to explain the uv upturn of early-type galaxies in
    redshift.
    The model consists in a Bayesian Logistic Regression
    This version: several improvements made. Betas retrieved successfully.
    @author:  Maria Luiza Linhares Dantas
    @date:    2017.09.20
    @version: 0.0.2

"""
# ======================================================================================================================
import numpy as np
import pystan
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns


# ======================================================================================================================

# Main thread

if __name__ == '__main__':

    # Configuring paths and inputs -------------------------------------------------------------------------------------
    my_data = np.loadtxt('/home/mldantas/Dropbox/DoutoradoIAG/GAMAZOO/logit_dataset.csv', delimiter=',', dtype=str)

    my_dictionary = {}
    for i in range(len(my_data[0, :])):                                         # Converting numpy array into dictionary
         my_dictionary[my_data[0, i]] = np.array(my_data[0 + 1:, i], dtype=str)

    logit_class = my_dictionary['logit_class(1-uvup;2-uvweak)'].astype(int)
    redshift    = my_dictionary['redshift'].astype(float)

    index = np.where(redshift<=0.4)

    x1 = redshift[index]
    y  = logit_class[index]                                             # whether this is a galaxy with uv upturn or not
    n_obs = x1.size

    regression_data = {}
    regression_data['K'] = 3      # number of betas
    regression_data['X'] = sm.add_constant(np.column_stack((x1, x1**2)))
    # regression_data['X'] = sm.add_constant(x1)
    regression_data['N'] = n_obs
    regression_data['Y'] = y
    regression_data['LogN'] = np.log(n_obs)

    # Fit: STAN code ---------------------------------------------------------------------------------------------------
    stan_code = """
    data{
        int<lower=0> N;
        int<lower=0> K;
        int Y[N];
        matrix[N,K] X;
        real LogN;
    }

    parameters{
        vector[K] beta;
    }

    transformed parameters{
        vector[N] eta;
        eta = X * beta;
    }

    model{
        Y ~ bernoulli_logit(eta);
    }

    generated quantities{
        real LLi[N];
        real AIC;
        real BIC;
        real LogL;
        vector[N] etanew;
        real<lower=0, upper=1.0> pnew[N];
        etanew = X * beta;
        for (i in 1:N){
            pnew[i] = inv_logit(etanew[i]);
            LLi[i] = bernoulli_lpmf(1|pnew[i]);
        }
        LogL = sum(LLi);
        AIC = -2 * LogL + 2 * K;
        BIC = -2 * LogL + LogN * K;
    }
    """

    fit = pystan.stan(model_code=stan_code, data=regression_data, iter=7000, chains=3, warmup=4000, n_jobs=1)

    # Output -----------------------------------------------------------------------------------------------------------

    lines = list(range(8)) + [2 * n_obs + 8, 2 * n_obs + 9, 2 * n_obs + 10]
    output = str(fit).split('\n')

    for i in lines:
        print(output[i])

    posteriors = list(fit.extract(u'beta').items()[0])