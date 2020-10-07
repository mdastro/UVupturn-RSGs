#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Selection of key columns of the extinction dataframe from the GAMA survey.
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
    path = '/home/mldantas/Dropbox/GAMA_Catalog/GalacticExtinction'
    extinction_all = pd.read_csv(os.path.join(path, 'GalacticExtinction.csv'))

    extinction_all = pd.DataFrame(extinction_all)

    selection_extinction_uv_sdss = extinction_all[['CATAID', 'EBV', 'A_FUV', 'A_NUV', 'A_B', 'A_u', 'A_g', 'A_r',
                                                   'A_i', 'A_z']]

    selection_extinction_ukidss = extinction_all[['CATAID', 'A_Y', 'A_J', 'A_H', 'A_K']]

    selection_extinction_uv_sdss.to_csv(os.path.join(path, 'extinction_selection_uv_sdss.csv'), sep=',', header=True,
                                        index=False)
    selection_extinction_ukidss.to_csv(os.path.join(path, 'extinction_selection_ukidss.csv'), sep=',', header=True,
                                        index=False)

