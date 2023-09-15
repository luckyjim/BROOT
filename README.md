# BROOT presentation

BROOT is a browser for [ROOT files](https://root.cern/manual/io), format defined and used by CERN collaboration.

BROOT is an alternative to the [TBrowser tool](https://root.cern/manual/root_files/#root-object-browser)

BROOT doesn't use the ROOT library but the IO-specific library [uproot](https://uproot.readthedocs.io/en/latest/).



# BROOT GUI

## Table for each TTree
![BROOT_table](docs/BROOT2.png)

### Basic print value

![BROOT_print](docs/BROOT_print.png)

### Basic plots

Range of plot is configurable with GUI, same syntax as [numpy](https://numpy.org/doc/stable/user/basics.indexing.html#basic-indexing) array. [Matplotlib](https://matplotlib.org/) is used to create the figures.

#### Plot 1D

![BROOT_1d](docs/BROOT_plot_1d.png)

#### Power spectrum density

You can configure the frequency of sampling with GUI.

![BROOT_1d](docs/BROOT_psd.png)

#### Histogram

![BROOT_1d](docs/BROOT_histo.png)

# Installation

Check if tkinter library is correctly installed with

```
python -m tkinter
```

else see [installation documentation](https://tkdocs.com/tutorial/install.html)

then BROOT installs very simply with pip install

```
python -m pip install git+https://github.com/luckyjim/BROOT.git 
```

run BROOT in a terminal with this command

```
BROOT.py
```

upgrading pip and setuptools packages can help

```
pip install --upgrade setuptools pip
```



