#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Selection of key columns of the K corrections dataframes from the GAMA survey.
    @author:  Maria Luiza Linhares Dantas
    @date:    2017.26.05
    @version: 0.0.1

"""

from __future__ import division
import pandas as pd
import os


# Main thread
if __name__ == '__main__':

    # Configuring the inputs -------------------------------------------------------------------------------------------
    path = '/home/mldantas/Dropbox/GAMA_Catalog/kCorrections'
    k1_all = pd.read_csv(os.path.join(path, 'kcorr_z01.csv'))

    k1_all = pd.DataFrame(k1_all)

    selection_k1 = k1_all[['CATAID', 'U_MODEL', 'U_MODEL_ERR', 'G_MODEL', 'G_MODEL_ERR', 'R_MODEL', 'R_MODEL_ERR',
                           'I_MODEL', 'I_MODEL_ERR', 'Z_MODEL', 'Z_MODEL_ERR', 'KCORR_FUV', 'KCORR_NUV', 'KCORR_U',
                           'KCORR_G', 'KCORR_R', 'KCORR_I', 'KCORR_Z', 'KCORR_Y', 'KCORR_J', 'KCORR_H', 'KCORR_K',
                           'CHI2', 'MASS', 'INTSFH', 'METS', 'B300', 'B1000']]

    selection_k1.to_csv(os.path.join(path, 'k1_selection.csv'), sep=',', header=True, index=False)
