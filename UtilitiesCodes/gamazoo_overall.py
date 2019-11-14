#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Boxplot with the distributions of magnitude of SDSS, GALEX, and UKIDSS.
    @author:  Maria Luiza Linhares Dantas
    @date:    2016.01.10
    @version: 0.0.1

"""

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Main thread
if __name__ == '__main__':

    # Configuring the inputs -------------------------------------------------------------------------------------------
    my_data = np.loadtxt('/home/mldantas/Dropbox/DoutoradoIAG/GAMAZOO/GAMA_zoo_GALEX.csv', delimiter=',', dtype=object)

    dictionary = {}
    for i in range(len(my_data[0, :])):                                         # Converting numpy array into dictionary
        dictionary[my_data[0, i]] = np.array(my_data[0 + 1:, i], dtype=str)

    # pd.DataFrame(my_data)
    mag_f = dictionary['BEST_MAG_FUV'].astype(float)
    mag_n = dictionary['BEST_MAG_NUV'].astype(float)
    mag_u = dictionary['MAG_PETRO_U'].astype(float)
    mag_g = dictionary['MAG_PETRO_G'].astype(float)
    mag_r = dictionary['MAG_PETRO_R'].astype(float)
    mag_i = dictionary['MAG_PETRO_I'].astype(float)
    mag_z = dictionary['MAG_PETRO_Z'].astype(float)
    mag_y = dictionary['MAG_PETRO_Y'].astype(float)
    mag_j = dictionary['MAG_PETRO_J'].astype(float)
    mag_h = dictionary['MAG_PETRO_H'].astype(float)
    mag_k = dictionary['MAG_PETRO_K'].astype(float)

    ellipticity = dictionary['p_el'].astype(float)
    diskyness = dictionary['p_cs'].astype(float)

    # print type(ellipticity[0])
    # exit()
    #
    # galaxy_type = []
    # if (ellipticity >= 0.5):
    #     galaxy_type.append('Elliptical')
    # elif (ellipticity < 0.5):
    #     galaxy_type.append('Spiral')
    # else:
    #     galaxy_type.append('Undefined')
    # galaxy_type = np.array(galaxy_type)

    index_el = np.where(ellipticity>=0.5)
    index_sp = np.where(diskyness>=0.5)

    data_el = [mag_f[index_el], mag_n[index_el], mag_u[index_el], mag_g[index_el], mag_r[index_el], mag_i[index_el],
               mag_z[index_el], mag_y[index_el], mag_j[index_el], mag_h[index_el], mag_k[index_el]]

    data_sp = [mag_f[index_sp], mag_n[index_sp], mag_u[index_sp], mag_g[index_sp], mag_r[index_sp], mag_i[index_sp],
               mag_z[index_sp], mag_y[index_sp], mag_j[index_sp], mag_h[index_sp], mag_k[index_sp]]

    plt.subplot(2, 1, 1)
    plot01 = sns.boxplot(data=data_el, notch=True)
    # sns.stripplot(data=data_el, size=4, jitter=True, edgecolor="gray")
    plt.title("Ellipticals: %d" % mag_f[index_el].size, size='15')
    plt.ylabel(r"Magnitude distribution", size='20')
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['FUV', 'NUV', 'u', 'g', 'r', 'i', 'z', 'Y', 'J', 'H', 'K'])
    plt.tick_params('both', labelsize='20')
    plt.ylim(5, 35)
    plt.gca().invert_yaxis()

    plt.subplot(2, 1, 2)
    plot01 = sns.boxplot(data=data_sp, notch=True)
    # sns.stripplot(data=data_sp, size=4, jitter=True, edgecolor="gray")
    plt.title("Spirals: %d" % mag_f[index_sp].size, size='15')
    plt.xlabel(r"GALEX, SDSS & UKIDSS photometry", size='20')
    plt.ylabel(r"Magnitude distribution", size='20')
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['FUV', 'NUV', 'u', 'g', 'r', 'i', 'z', 'Y', 'J', 'H', 'K'])
    plt.tick_params('both', labelsize='20')
    plt.ylim(5, 35)
    plt.gca().invert_yaxis()

    plt.show()