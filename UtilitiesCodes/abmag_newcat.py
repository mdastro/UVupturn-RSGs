#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Creating new catalog with the corrected AB magnitudes, absolute magnitudes and adds a flag for the UV classification
    @author:  Maria Luiza Linhares Dantas
    @date:    2017.07.18
    @version: 0.0.3

    Comment 01: pivot wavelengths from http://www.astro.ljmu.ac.uk/~ikb/research/mags-fluxes/
    Comment 02: AB offsets for UKIDSS taken from: http://www.ukidss.org/technical/photom/hewett-ukidss.pdf
"""
# ======================================================================================================================

from __future__ import division
import os
import pandas as pd
import pyneb as pn
import numpy as np
from astropy.cosmology import FlatLambdaCDM

# ======================================================================================================================

# Main thread

if __name__ == '__main__':

    # Constants --------------------------------------------------------------------------------------------------------
    c = 2.99792458E18	# Light Speed in Angstrom/s

    # Configuring paths and inputs -------------------------------------------------------------------------------------
    data_path              = '/home/mldantas/Dropbox/DoutoradoIAG/GAMAZOO'
    raw_catalog            = 'myGAMA_SDSS_GALEX_UKIDSS.csv'
    pivot_wavelengths_file = 'pivot_wls.csv'
    offeset_ab_mags        = 'offset_abmags.csv'

    master_dataframe = pd.DataFrame(pd.read_csv(os.path.join(data_path, raw_catalog)))
    master_catalog = np.loadtxt(os.path.join(data_path, raw_catalog), delimiter=',', dtype=str)
    pivot_wavelengths = np.loadtxt(os.path.join(data_path, pivot_wavelengths_file), delimiter=',', dtype=float,
                                   skiprows=1)
    offeset_ab_mags = np.loadtxt(os.path.join(data_path, offeset_ab_mags), delimiter=',', dtype=float, skiprows=1)

    my_dictionary = {}
    for i in range(len(master_catalog[0, :])):                                  # Converting numpy array into dictionary
        my_dictionary[master_catalog[0, i]] = np.array(master_catalog[0 + 1:, i], dtype=str)

    # Selecting the magnitudes, extinction, kcorr,... ------------------------------------------------------------------
    ## magnitudes ------------------------------------------------------------------------------------------------------
    mag_apparent_all = np.column_stack((my_dictionary['BEST_MAG_FUV'].astype(float),
                                        my_dictionary['BEST_MAG_NUV'].astype(float),
                                        my_dictionary['U_MODEL'].astype(float),
                                        my_dictionary['G_MODEL'].astype(float),
                                        my_dictionary['R_MODEL'].astype(float),
                                        my_dictionary['I_MODEL'].astype(float),
                                        my_dictionary['Z_MODEL'].astype(float),
                                        my_dictionary['MAG_PETRO_Y'].astype(float),
                                        my_dictionary['MAG_PETRO_J'].astype(float),
                                        my_dictionary['MAG_PETRO_H'].astype(float),
                                        my_dictionary['MAG_PETRO_K'].astype(float)))

    ## k-corrections for z=0.0 -----------------------------------------------------------------------------------------
    kcorr_all = np.column_stack((my_dictionary['KCORR_FUV_k0'].astype(float),
                                 my_dictionary['KCORR_NUV_k0'].astype(float),
                                 my_dictionary['KCORR_U_k0'].astype(float),
                                 my_dictionary['KCORR_G_k0'].astype(float),
                                 my_dictionary['KCORR_R_k0'].astype(float),
                                 my_dictionary['KCORR_I_k0'].astype(float),
                                 my_dictionary['KCORR_Z_k0'].astype(float),
                                 my_dictionary['KCORR_Y_k0'].astype(float),
                                 my_dictionary['KCORR_J_k0'].astype(float),
                                 my_dictionary['KCORR_H_k0'].astype(float),
                                 my_dictionary['KCORR_K_k0'].astype(float)))

    ## extinction ------------------------------------------------------------------------------------------------------
    ebv = my_dictionary['EBV'].astype(float)
    dered = pn.RedCorr(law='F99', R_V=3.1, E_BV=ebv)

    extinction = []
    for i in range(pivot_wavelengths.size):
        extinction_i = dered.getCorr(pivot_wavelengths[i], rel_wave=None)                      # extinction in flux
        extinction_i = np.log10(extinction_i/2.5)                                              # extinction in magnitude
        extinction.append(extinction_i)
    extinction = np.array(extinction).T

    # Correcting magnitudes by: extinction, k-correction, offset -------------------------------------------------------
    mag_ab_all = []
    for each_band in range(mag_apparent_all[0, :].size):        # for each band among galex, sdss, and ukidss surveys:
        mag_ab_i = mag_apparent_all[:, each_band] - kcorr_all[:, each_band] - extinction[:, each_band] + \
                   offeset_ab_mags[each_band]
        mag_ab_all.append(mag_ab_i)
    mag_ab_all = np.array(mag_ab_all).T
    mag_ab_all = np.squeeze(mag_ab_all)        # literally squeezing the dimensions in order to be the smallest possible

    # Calculating absolute magnitude -----------------------------------------------------------------------------------
    adopted_cosmology = FlatLambdaCDM(H0=70, Om0=0.3)                                             # cosmology parameters
    redshift = my_dictionary['Z_HELIO'].astype(float)
    luminosity_distance = adopted_cosmology.luminosity_distance(redshift).value                   # in Mpc

    mag_absolute = []
    for each_band in range(mag_apparent_all[0, :].size):
        mag_absolute_i = mag_apparent_all[:, each_band] - 5 * np.log10(luminosity_distance[each_band]) - 25
        mag_absolute.append(mag_absolute_i)
    mag_absolute = np.array(mag_absolute).T

    # Defining the new catalog -----------------------------------------------------------------------------------------
    mag_ab_df = pd.DataFrame(mag_ab_all)
    mag_ab_df.columns = ['MAG_AB_FUV', 'MAG_AB_NUV', 'MAG_AB_U', 'MAG_AB_G', 'MAG_AB_R', 'MAG_AB_I', 'MAG_AB_Z',
                          'MAG_AB_Y', 'MAG_AB_J','MAG_AB_H','MAG_AB_K']
    mag_absolute_df = pd.DataFrame(mag_absolute)
    mag_absolute_df.columns = ['MAG_ABSOLUTE_FUV', 'MAG_ABSOLUTE_NUV', 'MAG_ABSOLUTE_U', 'MAG_ABSOLUTE_G',
                               'MAG_ABSOLUTE_R', 'MAG_ABSOLUTE_I', 'MAG_ABSOLUTE_Z', 'MAG_ABSOLUTE_Y', 'MAG_ABSOLUTE_J',
                               'MAG_ABSOLUTE_H','MAG_ABSOLUTE_K']

    # Creating an UV classification flag based on the paper of Yi et al. (2011) ----------------------------------------
    uv_color             = mag_ab_df['MAG_AB_FUV'] - mag_ab_df['MAG_AB_NUV']
    optical_uv_nuv_color = mag_ab_df['MAG_AB_NUV'] - mag_ab_df['MAG_AB_R']
    optical_uv_fuv_color = mag_ab_df['MAG_AB_FUV'] - mag_ab_df['MAG_AB_R']

    uv_class = []
    for i in range(mag_ab_df['MAG_AB_FUV'].size):
        if optical_uv_nuv_color[i] < 5.4:
            uv_class_i = 'RSF'
        elif (optical_uv_nuv_color[i] > 5.4) * (uv_color[i] < 0.9) * (optical_uv_fuv_color[i] < 6.6):
            uv_class_i = 'UV_UPTURN'
        else:
            uv_class_i = 'UV_WEAK'
        uv_class.append(uv_class_i)
    uv_class = np.array(uv_class)

    uv_class_df = pd.DataFrame(uv_class)
    uv_class_df.columns = ['UV_CLASS_YI2011']

    # Saving the new dataset into a csv --------------------------------------------------------------------------------
    complete_dataset = pd.concat([master_dataframe, mag_ab_df, mag_absolute_df,uv_class_df], axis=1)

    complete_dataset.to_csv(os.path.join(data_path, 'myGAMA_ALL_AB_ABSOL_MAGS.csv'), sep=',', header=True,
                            index=False)