import re
import functools
import pandas as pd

# When the column name is shortened, it is renamed such that the portion of
# the string after the `_` character is lower case. If a different name is
# required, it should be added to this dictionary.
column_dict = {'t' : 't',
               'mx' : 'mx',
               'my' : 'my',
               'mz' : 'mz',
               'E_total': 'E',
               'E_exch' : 'E_totalexchange',
               'E_demag' : 'E_demag',
               'E_Zeeman': 'E_zeeman',
               'E_anis' : 'E_totalanisotropy',
               'dt' : 'dt',
               'maxTorque' : 'maxtorque'}

def mumax_columns(filename, rename=True):
    """Extract the names of columns from a mumax `.txt` file.

    This function extracts the names of columns from an mumax `.txt`
    file and returns a list of strings. If `rename=True`, the columns
    will be renamed to shorter versions.

    Parameters
    ----------
    filename : str
        Name of a mumax `.txt` file
    rename : bool
        Flag (the default is `True`). If `rename=True`, the column
        names are renamed with their shorter versions.

    Returns
    -------
    list(str)

    Examples
    --------
    1. Extracting the names of columns from an mumax `.txt` file.

    >>> import os
    >>> import mumaxtxt as oo
    ...
    >>> txtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'mumax_samples', 'table1.txt')
    >>> columns = oo.mumax_columns(txtfile)
    >>> type(columns)
    <class 'list'>

    .. note::

           This function does not extract units for individual
           columns. For that `oommfodt.units` can be used.

    """
    with open(filename) as f:
        lines = f.readlines()

    columns = []
    splitted_line = lines[0][2:].rstrip().split("\t")
    for column in splitted_line:
        column = column.split(" ")[0]
        if rename:
            if column in column_dict.keys():
                column = column_dict[column]
                
        columns.append(column)
        
        
    return columns


def mumax_data(filename):
    """Read numerical data from a mumax `.txt` file.

    This function reads data from a mumax `.txt` file and returns it
    as a list of floats.

    Parameters
    ----------
    filename : str
        Name of a mumax `.txt` file

    Returns
    -------
    list(float)

    Examples
    --------
    1. Reading data from an mumaxc `.txt` file.

    >>> import os
    >>> import mumaxtxt as oo
    ...
    >>> txtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'mumax_samples', 'table1.txt')
    >>> data = oo.mumax_data(txtfile)
    >>> type(data)
    <class 'list'>

    """
    with open(filename) as f:
        lines = f.readlines()

    values = []
    for line in lines:
        if not line.startswith("#"):
            values.append(list(map(float, line.rstrip().split("\t"))))

    return values


def mumax_read(filename, rename=True):
    """Read an mumax `.txt` file and return it as `pandas.DataFrame`.

    This function reads column names and data from an mumax `.txt`
    file and returns a `pandas.DataFrame`. Because there is no
    appropriate way of adding metadata to the `pandas.DataFrame`,
    obtaining units from the `.txt` file is ignored and can be
    extracted using `oommfodt.units` function. If `rename=True`, the
    column names will be renamed to their shorter versions.

    Parameters
    ----------
    filename : str
        Name of an mumax `.txt` file
    rename : bool
        Flag (the default is `True`). If `rename=True`, the column
        names are renamed with their shorter versions.

    Returns
    -------
    pandas.DataFrame

    Examples
    --------
    1. Reading an mumax `.txt` file.

    >>> import os
    >>> import mumaxtxt as oo
    ...
    >>> txtfile = os.path.join(os.path.dirname(__file__),
    ...                        'tests', 'test_sample', 'mumax_samples', 'table1.txt')
    >>> df = oo.mumax_read(txtfile)
    >>> type(df)
    <class 'pandas.core.frame.DataFrame'>

    .. note::

           For more information on how the names of columns are
           renamed, please see `oommfodt.columns`.

    """
    return pd.DataFrame(mumax_data(filename),
                        columns=mumax_columns(filename, rename=rename))

