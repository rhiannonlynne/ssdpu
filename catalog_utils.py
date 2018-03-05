import os
import pandas as pd


def _convert_designation(x):
    # Match astorb designation to MOC designation.
    x.designation = str(x.designation).rstrip(' ').lstrip(' ').replace(' ', '_')
    return x


def read_sdss_moc(filename='ADR4.dat'):
    """Read SDSS Moving Object Catalog.

    SDSS MOC available from:
    http://faculty.washington.edu/ivezic/sdssmoc/sdssmoc.html

    The SDSS MOC provides visible colors for moving objects, with varying numbers of
    observations per object. Estimates of the uncertainties are provided.
    SDSS observations provide simultaneous ugrizy measurements.

    Parameters
    ----------
    filename : str, opt
        The full path to the MOC catalog file.

    Returns
    -------
    pandas.DataFrame
    """
    names=['sdssID', 'run', 'col', 'field', 'obj', 'pixrow', 'pixcol',
           'time', 'ra', 'dec', 'l', 'b', 'phi',
           'vmu', 'vmuerr', 'vnu', 'vnuerr', 'vl', 'vb',
           'u', 'uerr', 'g', 'gerr', 'r', 'rerr', 'i', 'ierr', 'z', 'zerr',
           'sdssa', 'aerr', 'V', 'B', 'idFlag', 'numberId', 'designation',
           'detectionCount', 'totalCount', 'sdss_flags',
           'calcRA', 'calcDec', 'calcAppMag', 'helioDistance', 'geoDistance', 'phase',
           'catalogId', 'H', 'G1', 'obsArc', 'epoch', 'a', 'e', 'inc', 'lonNode', 'argPeri', 'meanAnom',
           'elemCatalogId', 'aProper', 'eProper', 'siniProper' ]
    # a* color = 0.89 (g - r) + 0.45 (r - i) - 0.57
    moc = pd.read_table(filename, delim_whitespace=True, names=names, usecols=names)
    return moc


def read_astorb(filename='astorb.dat'):
    """Read ASTORB data file.

    ASTORB available from:
    ftp://ftp.lowell.edu/pub/elgb/astorb.html
    ASTORB is made available by Dr. Edward Bowell.
    ASTORB is made possible by funding from NASA grant NAG5-4741 and the Lowell Observatory Endowment.

    This provides updated osculating element orbits, and an estimate of their ephemeris uncertainty.
    To get the updated ephemeris uncertainty, it makes sense to update this input data frequently.


    Parameters
    ----------
    filename : str, opt
        The full path to the MOC catalog file.

    Returns
    -------
    pandas.DataFrame
    """
    names=['numberId', 'designation', 'computer', 'H', 'G1', 'B-V',
           'diameter_IRAS_km', 'classification_IRAS',
           'planet_crossing', 'orbit_comp', 'survey', 'mpc_crit', 'lowell_obs', 'rank',
           'obsArc', 'nObs', 'epoch', 'meanAnom', 'argPeri', 'lonNode', 'inc', 'e', 'a',
           'date_comp', 'ceu', 'deltaceu', 'ceudate',
           'peumax', 'peumaxdate', 'peumax10', 'peumax10date', 'peumax2', 'peumax2date']
    widths = [7, 19, 16, 6, 6, 5, 6, 5, 4, 4, 4, 4, 4, 4, 6, 6, 9, 11, 11, 11, 10, 11, 13, 9, 8, 8, 9, 8, 9, 8, 9, 8, 9]
    astorb = pd.read_fwf(filename, index_col=False, names=names, widths=widths)
    astorb = astorb.apply(_convert_designation, axis=1)
    astorb['numberId'] = astorb['numberId'].fillna(0).astype(int)
    return astorb


# ASTDYS proper elements
# family classifications
# http://hamilton.dm.unipi.it/astdys/index.php?pc=5
