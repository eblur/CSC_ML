
## Take the cleaned Chandra catalog from Moritz 
##    and get E(B-V) values from Schlafely & Finkbeiner (2011)
##     http://irsa.ipac.caltech.edu/applications/DUST/docs/dustProgramInterface.html 

import numpy as np
import urllib2
import xml.etree.ElementTree as etree

def get_ext_value(url_str):
    response = urllib2.urlopen(url_str)
    xml_str  = response.read()
    xml_root = etree.fromstring(xml_str)
    stats    = xml_root[1].find('statistics')
    val_obj  = stats.find('refPixelValueSandF')
    val_str  = val_obj.text.strip()
    return np.float(val_str.rstrip(' (mag)'))

from astropy import units as u
from astropy.coordinates import SkyCoord

def convert_coords(ra_deg, dec_deg):
    c = SkyCoord(ra=ra_deg*u.degree, dec=dec_deg*u.degree, frame='icrs')
    sign = ''
    if c.dec >= 0.0: sign = '+'
    if c.dec < 0.0: sign=r'%20'
    result = "%s%s%s" % (c.ra.to_string(sep=':'),sign,c.dec.to_string(sep=':'))
    return result

##------------------------------------------
## The main shebang

CSCFILE = 'chandra_filtered_small.fits'

from astropy.io import fits
#import multiprocessing
#pool = multiprocessing.Pool(processes=4)

hdulist = fits.open(CSCFILE)
tdata   = hdulist[1].data

def get_one_tbl_value(i):
    ra_deg  = tdata['RA'][i]
    dec_deg = tdata['DEC'][i]
    url_str = "http://irsa.ipac.caltech.edu/cgi-bin/DUST/nph-dust?locstr=" + \
        convert_coords(ra_deg, dec_deg)
    print(url_str)
    return get_ext_value(url_str)
    

ext_vals = []
for i in range(len(tdata)):
    ext_vals.append( get_one_tbl_value(i) )

#ext_vals = pool.map(get_one_tbl_value, range(20))
#pool.join()
#pool.close()

print(ext_vals)


## Create a new fits file for this info

col1 = fits.Column(name='DETECT_ID', format='29A', array=tdata['DETECT_ID'])
col2 = fits.Column(name='E(B-V)', format='20A', array=np.array(ext_vals))

final_cols  = fits.ColDefs([col1,col2])
new_hdulist = fits.new_table(final_cols)

hdu = fits.PrimaryHDU()
prihdr = fits.Header()

prihdu = fits.PrimaryHDU(header=prihdr)
thdulist = fits.HDUList([prihdu, new_hdulist])
thdulist.writeto('ext_values.fits')

hdulist.close()