# PyCy3

This project is an attempt to recreate the [R-based RCy3 Cytoscape Automation library](https://github.com/cytoscape/RCy3) as a Python package. The idea is to allow a Cytoscape workflow to be written in one language (R or Python) and translated to another language (Python or R) without having to learn different Cytoscape interfaces. The current Cytoscape Python interface ([Py2Cytoscape](https://github.com/cytoscape/py2cytoscape)) has different features than the Cytoscape R library, and therefore doesn't fit my purpose.

Additionally, this project attempts to maintain the same function signatures, return values, function implementation and module structure as the RCy3, thereby enabling smooth maintenance and evolution of both RCy3 and PyCy3.

This project uses PyCharm because of its excellent code management and debugging features.

Over time, PyCy3 functionality should match RCy3 functionality. Once that occurs, novel Py2Cytoscape functions will be added to both as appropriate.

An overall scorecard comparing Py2Cytoscape, RCy3 and PyCy3 can be found [here](https://docs.google.com/spreadsheets/d/1uhBTbOMI4QMKUpLaOTuf6BP5wgqU6-pOzkj6BNmC4CY/edit?usp=sharing). Pay close attention to columns E and F, which show how much of RCy3 is reflected in PyCy3.
 
## How to install

```shell
pip install python-igraph requests pandas networkx
git clone git://github.com/bdemchak/PyCy3
cd PyCy3
python setup.py install # or python setup.py install --user
```

## How to use

```python
import PyCy3
dir(PyCy3)
PyCy3.import_network_from_file("galfiltered.sif") # Before running this, save galfiltered.sif in the current directory.
```
