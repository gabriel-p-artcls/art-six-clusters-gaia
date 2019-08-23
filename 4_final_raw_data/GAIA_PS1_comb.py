
import os
from astropy.io import ascii
import numpy as np


files = os.listdir('.')
for f in files:
    if os.path.isfile(f) and not f.endswith('.py') and\
            not f.startswith('README'):

        name = f.split('.')[0].split('_')[0]
        print(name)

        data = ascii.read(name + '_match.dat')

        # Generate PS1 colors and errors.
        data['g-r'] = data['gmag'] - data['rmag']
        data['e_g-r'] = np.sqrt(data['e_gmag']**2 + data['e_rmag']**2)
        data['g-i'] = data['gmag'] - data['imag']
        data['e_g-i'] = np.sqrt(data['e_gmag']**2 + data['e_imag']**2)
        data['i-z'] = data['imag'] - data['zmag']
        data['e_i-z'] = np.sqrt(data['e_imag']**2 + data['e_zmag']**2)

        data_out = data[
            'DR2Name', '_x_1', '_y_1', 'RA_ICRS', 'DE_ICRS', 'Gmag', 'e_Gmag',
            'BP-RP', 'e_BP-RP', 'g-r', 'e_g-r', 'g-i', 'e_g-i', 'i-z', 'e_i-z',
            'Plx', 'e_Plx', 'pmRA', 'e_pmRA', 'pmDE', 'e_pmDE']

        ascii.write(data_out, name + '.dat', overwrite=True)
