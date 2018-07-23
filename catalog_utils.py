import numpy as np
import pandas as pd

__all__ = ['read_mpcorb', 'read_sdss_moc', 'read_astorb', 'read_lcdb']

def _convert_designation(x):
    # Match astorb designation to MOC designation.
    x.name = str(x.name).rstrip(' ').lstrip(' ').replace(' ', '_')
    return x

def read_mpcorb(filename='MPCORB.DAT', header=False):
    """Read Minor Planet Center Orbit Database
    
    File contains published orbital elements for all numbered and unnumbered 
    multi-opposition minor planets.
    Get the file at:
    https://www.minorplanetcenter.net/iau/MPCORB.html    
    See documentation at:
    https://minorplanetcenter.net/iau/info/MPOrbitFormat.html
    
    Parameters
    ----------
    filename : str, opt
        The full path to the MPCORB catalog file.
    Returns
    -------
    pandas.DataFrame
    """
    if header:
        skiprows = 43
    else:
        skiprows = 0
    names = ['mpcId', 'H', 'G', 'epoch', 'meanAnomaly', 'argPeri', 
             'Omega', 'inc', 'e', 'meanDailymo','a', 'reference', 
             '#Obs', '#Opp', 'yr_1st&last_Obs','r.m.s', 
             'coarsePerts', 'precisePerts', 'computer', 
              '#','name','lastObs']
    colspecs = [(0,7),(8,13),(14,19),(20,25),(26,35),(37,46),
                (48,57),(59,68),(70,79),(80,91),(92,103),(108,116),
                (117,122),(123,126),(127,136),(137,141), 
                (142, 145),(146,149),(150,160),(166,194),(194,202)]
    mpc = pd.read_fwf(filename, names=names, usecols=names, index=False)
    return mpc


def read_sdss_moc(filename='ADR4.dat'):
    """Read SDSS Moving Object Catalog.
    SDSS MOC available from:
    http://faculty.washington.edu/ivezic/sdssmoc/sdssmoc.html
    Please see information on that page for citation information.
    Ivezic, Z., Juric, M., Lupton, R.H., Tabachnik, S. & Quinn, T. (the SDSS Collaboration) 2002,
    Survey and Other Telescope Technologies and Discoveries, J.A. Tyson, S. Wolff, Editors,
    Proceedings of SPIE Vol. 4836 (2002)
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
           'sdssa', 'aerr', 'V', 'B', 'idFlag', 'numberId', 'name',
           'detectionCount', 'totalCount', 'sdss_flags',
           'calcRA', 'calcDec', 'calcAppMag', 'helioDistance', 'geoDistance', 'phase',
           'catalogId', 'H', 'G1', 'obsArc', 'epoch', 'a', 'e', 'inc', 'Omega', 'argPeri', 
           'meanAnomaly','elemCatalogId', 'aProper', 'eProper', 'siniProper' ]
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
    names=['#', 'name', 'computer', 'H', 'G1', 'B-V',
           'diameter_IRAS_km', 'classification_IRAS',
           'planet_crossing', 'orbit_comp', 'survey', 'mpc_crit', 'lowell_obs', 'rank',
           'obsArc', '#Obs', 'epoch', 'meanAnomaly', 'argPeri', 'Omega', 'inc', 'e', 'a',
           'date_comp', 'ceu', 'deltaceu', 'ceudate',
           'peumax', 'peumaxdate', 'peumax10', 'peumax10date', 'peumax2', 'peumax2date']
    widths = [7, 19, 16, 6, 6, 5, 6, 5, 4, 4, 4, 4, 4, 4, 6, 6, 9, 11, 11, 11, 10, 11, 13,
              9, 8, 8, 9, 8, 9, 8, 9, 8, 9]
    astorb = pd.read_fwf(filename, index_col=False, names=names, widths=widths)
    astorb = astorb.apply(_convert_designation, axis=1)
    astorb['#'] = astorb['#'].fillna(0).astype(int)
    return astorb


# ASTDYS proper elements
# family classifications
# http://hamilton.dm.unipi.it/astdys/index.php?pc=5

def read_lcdb(filename='LC_SUM_PUB.TXT'):
    """Read LCDB file tabulating periods and associated information.
    LCDB available from:
    http://www.minorplanet.info/lightcurvedatabase.html
    Please see that page for citation information.
    Warner, B.D., Harris, A.W., Pravec, P. (2009). Icarus 202, 134-146.
    Updated <Date of last update>. http://www.MinorPlanet.info/lightcurvedatabase.html
    The Asteroid Lightcurve Database is a listing of asteroid lightcurve parameters and other information,
    e.g., estimated/measured diameters, absolute magnitudes (H), phase slope parameters (G), albedos, + more.
    Parameters
    ----------
    filename : str, opt
        The full path to the LCDB file (LC_SUM_PUB.TXT or similarly formatted files)
    Returns
    -------
    pandas.DataFrame
    """
    names = ['#', 'new', 'name', 'Desig', 'family', 'Csource', 'class', 'Dsource', 
         'Dflag', 'diameter','Hsource', 'H', 'Hband', 'Asource', 'Albedoflag',  
         'albedo', 'Pflag', 'period', 'Pdescr','Ampflag', 'AmpMin', 'AmpMax', 
         'U', 'notes', 'binary', 'priv' , 'pole', 'sparse', 'widefield']
    colspecs = [(0, 7), (8, 9), (10, 40), (41, 61), (62, 70), (71, 72), (73, 78), 
                (79, 80), (81, 82), (83, 92), (93, 94), (95, 100), (101, 102), 
                (104, 105), (106, 107), (108, 114), (115, 116), (117, 130), (131, 146), 
                (147, 148), (149, 153), (154, 158), (159, 161),(162, 167), (168, 171), 
                (172, 175), (176, 179), (180, 182), (183, 184)]
    lcdata = pd.read_fwf(filename, index_col=False, skiprows=5, names=names, colspecs=colspecs)
    lcdata['Frequency'] = 1.0/lcdata.period
    # Map flags to ints.
    tmp = lcdata.new.values
    tmp = np.where(tmp == '*', 1, 0)
    lcdata.new = tmp
    tmp = lcdata.sparse.values
    tmp = np.where(tmp == 'Y', 1, 0)
    lcdata.sparse = tmp
    tmp = lcdata.widefield.values
    tmp = np.where(tmp == 'Y', 1, 0)
    lcdata.widefield = tmp
    return lcdata
