
CSCFILE = 'chandra_filtered_small.fits'

from astropy.io import fits
#import multiprocessing
#pool = multiprocessing.Pool(processes=4)

hdulist = fits.open(CSCFILE)
tdata   = hdulist[1].data

from astropy.io import ascii

import numpy as np

NVALS = 1000
ii    = np.random.randint(0, len(tdata)+1, NVALS)
ascii.write([tdata['RA'][ii], tdata['DEC'][ii]], 'ra_dec_table.txt', names=['ra','dec'])

ascii.write([ii, tdata['DETECT_ID'][ii], tdata['RA'][ii], tdata['DEC'][ii]], 
    'random_objects.txt', names=['index','DETECT_ID','RA','DEC'])
