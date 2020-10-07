#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Selection of key columns of Sersic dataframe from the GAMA survey.
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
    path = '/home/mldantas/Dropbox/GAMA_Catalog/SersicPhotometry/SersicCatAll/'
    sersic_all = pd.read_csv(os.path.join(path, 'SersicCatAll_w_header.csv'))

    sersic_all = pd.DataFrame(sersic_all)

    selection_sersic = sersic_all[['CATAID', 'SEX_INDEX_U', 'SEX_INDEX_G','SEX_INDEX_R', 'SEX_INDEX_I', 'SEX_INDEX_Z',
                                   'SEX_INDEX_Y', 'SEX_INDEX_J', 'SEX_INDEX_H', 'SEX_INDEX_K', 'GAL_INDEX_U',
                                   'GAL_INDEX_G', 'GAL_INDEX_R', 'GAL_INDEX_I', 'GAL_INDEX_Z', 'GAL_INDEX_Y',
                                   'GAL_INDEX_J', 'GAL_INDEX_H', 'GAL_INDEX_K', 'GAL_ELLIP_R', 'GAL_CHI2_R',
                                   'GAL_QFLAG_R', 'FILENAME', 'URL', 'URL_R', 'URL_K']]

    selection_sersic.to_csv(os.path.join(path, 'SersicCatAll_selection.csv'), sep=',', header=True, index=False)
