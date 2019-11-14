#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    This script aims at constructing a regression model to explain the uv upturn of early-type galaxies in redshift.
    The model consists in a Bayesian Grouped Logit Model (or simply Binomial Model).
    @author:  Maria Luiza Linhares Dantas
    @date:    2017.09.18
    @version: 0.0.1

"""
# ======================================================================================================================
import numpy as np
import pystan
import matplotlib.pyplot as plt
import statsmodels.api as sm


# ======================================================================================================================

# Main thread

if __name__ == '__main__':

    # Configuring paths and inputs -------------------------------------------------------------------------------------
    my_data = np.loadtxt('/home/mldantas/Dropbox/DoutoradoIAG/GAMAZOO/regression_dataset.csv', delimiter=',', dtype=str)

    my_dictionary = {}
    for i in range(len(my_data[0, :])):                                         # Converting numpy array into dictionary
         my_dictionary[my_data[0, i]] = np.array(my_data[0 + 1:, i], dtype=str)

    uvup_galaxies    = my_dictionary['number_galaxies_uvup'].astype(int)               # this is the 'y' variable
    redseq_galaxies  = my_dictionary['number_galaxies_redsequence'].astype(int)        # this is the m variable
    average_redshift = my_dictionary['average_redshift'].astype(float)                 # this is the x1 variable

    # Regression parameters --------------------------------------------------------------------------------------------
    n_obs = uvup_galaxies.size

    m  = redseq_galaxies
    x1 = average_redshift
    y  = uvup_galaxies

    regression_data = {}
    regression_data['K'] = 2      # number of betas
    # regression_data['X'] = sm.add_constant(np.column_stack((x1, x1**2)))
    regression_data['X'] = sm.add_constant(x1)
    regression_data['N'] = n_obs
    regression_data['Y'] = y
    regression_data['m'] = m

    # Fit: STAN code ---------------------------------------------------------------------------------------------------
    stan_code = """
    data{
        int<lower=0> N;
        int<lower=0> K;
        matrix[N, K] X;
        int Y[N];
        int m[N];
    }

    parameters{
        vector[K] beta;
    }

    transformed parameters{
        vector[N] eta;
        vector[N] p;

        eta = X * beta;
        for (i in 1:N) p[i] = inv_logit(eta[i]);
    }

    model{
        Y ~ binomial(m, p);
    }
    """

    fit = pystan.stan(model_code=stan_code, data=regression_data, iter=10000, chains=3, warmup=5000, n_jobs=3)

    # Output -----------------------------------------------------------------------------------------------------------
    nlines = 8
    output = str(fit).split('\n')
    for item in output[:nlines]:
        print(item)

    fit.plot()
    plt.tight_layout()
    # plt.savefig('./posteriors.pdf', dpi=100)
    plt.show()