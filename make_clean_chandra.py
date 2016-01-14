import argparse

from astropy.table import Table


def make_chandra_smaller(filename, max_err):
    chandra = Table.read('preliminary_detlist.fits.gz')

    # filter out stuff that's marginal
    chandra = chandra[chandra['SRC_QUALITY'] == 'TRUE    ']
    # filter out stuff that's on a strak
    chandra = chandra[chandra['STREAK_SRC_FLAG'] == False]
    # filter out stuff that has large positionl errors
    chandra = chandra[chandra['ERR_ELLIPSE_R0'] < 2.]

    keep = \
    ['DETECT_ID',
     'LIKELIHOOD',
    # 'SRC_QUALITY',
    # 'EBAND',
     'THETA',
    # 'STREAK_SRC_FLAG',
     'RA',
     'DEC',
    # 'ERR_ELLIPSE_RA',
    # 'ERR_ELLIPSE_DEC',
    # 'ERR_ELLIPSE_R0',
    # 'ERR_ELLIPSE_R1',
    # 'ERR_ELLIPSE_ANG',
    # 'SRC_RDATA_B',
     'SRC_AMPL_B',
    # 'SRC_AMPL_LOLIM_B',
    # 'SRC_AMPL_HILIM_B',
    # 'SRC_RDATA_S',
     'SRC_AMPL_S',
    # 'SRC_AMPL_LOLIM_S',
    # 'SRC_AMPL_HILIM_S',
    # 'SRC_RDATA_M',
     'SRC_AMPL_M',
    # 'SRC_AMPL_LOLIM_M',
    # 'SRC_AMPL_HILIM_M',
    # 'SRC_RDATA_H',
     'SRC_AMPL_H',
    # 'SRC_AMPL_LOLIM_H',
    # 'SRC_AMPL_HILIM_H',
    # 'SRC_RDATA_W',
     'SRC_AMPL_W',
    # 'SRC_AMPL_LOLIM_W',
    # 'SRC_AMPL_HILIM_W',
     # 'EBAND_EXT',
     'EXTSRC_CLASS',
     'EXT_RDATA',
     'EXT_AMPL',
    # 'EXT_AMPL_LOLIM',
    # 'EXT_AMPL_HILIM',
     'EXT_SMAJ',
     'EXT_SMIN',
    # 'EXT_ROTANG',
    # 'EXT_SMAJ_LOLIM',
    # 'EXT_SMAJ_HILIM',
    # 'EXT_SMIN_LOLIM',
    # 'EXT_SMIN_HILIM',
    # 'EXT_ROTANG_LOLIM',
    # 'EXT_ROTANG_HILIM',
    ]
    chandra.keep_columns(keep)

    chandra.write('chandra_filtered_small.fits')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Put some cuts on Chandra Source catalog.')
    parser.add_argument('--filename', type=str, default='preliminary_detlist.fits.gz',
                        help='filename of Chandra source catalog')
    parser.add_argument('--maxposerr', type=float, default=1.,
                        help='maximal allows positional error in arcsec')
    args = parser.parse_args()
    make_chandra_smaller(args.filename, args.maxposerr)
