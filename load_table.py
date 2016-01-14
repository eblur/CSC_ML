from astropy.io import fits
from numpy import *

#data['column_name'] should give you a specific column

hdulist = fits.open('chandra_filtered_small.fits')
data = hdulist[1].data
cols = hdulist[1].columns
