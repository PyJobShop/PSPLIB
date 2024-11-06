[![PyPI version](https://img.shields.io/pypi/v/pysplib?style=flat-square&label=PyPI)](https://pypi.org/project/psplib/)
[![CI](https://img.shields.io/github/actions/workflow/status/PyJobShop/PSPLIB/.github%2Fworkflows%2FCI.yml?branch=main&style=flat-square&logo=github&label=CI)](https://github.com/PyJobShop/PSPLIB/actions/workflows/CI.yml)

# PSPLIB

This library implements parsers for various project scheduling benchmark instance formats, including:
- Resource-Constrained Project Scheduling Problem (RCPSP)
- Multi-Mode Resource-Constrained Project Scheduling Problem (MMRCPSP)
- Resource-Constrained Multi Project Scheduling Problem (RCMPSP)

`psplib` only depends on `numpy` and can be installed in the usual way:

```
pip install pyjobshop
```


## Example usage

``` python
>>> from psplib import parse
>>> instance = parse("j301_1.sm", instance_format="psplib") 
>>> instance.num_resources
4

>>> instance.resources
[Resource(capacity=12, renewable=True), ..., Resource(capacity=12, renewable=True)]

>>> instance.num_projects
1

>>> instance.projects
[Project(activities=[0, 1, ..., 31], release_date=0)]

>>> instance.num_activities
32

>>> instance.activities
[Activity(modes=[Mode(duration=0, demands=[0, 0, 0, 0])], successors=[1, 2, 3], name=''), 
 Activity(modes=[Mode(duration=8, demands=[4, 0, 0, 0])], successors=[5, 10, 14], name=''),
 ...,
 Activity(modes=[Mode(duration=0, demands=[0, 0, 0, 0])], successors=[], name='')]
```

All parsers return an instance of the [`ProjectInstance`](https://github.com/PyJobShop/PSPLIB/blob/main/psplib/ProjectInstance.py) class, which is an instance representation of the multi-project, multi-mode, resource-constrained project scheduling problem (MP-MM-RCPSP). 

## Instance formats

`psplib` implements parsers for three commonly used instance formats, listed below. 
To parse a specific instance format, set the `instance_format` argument in `parse`.

1. **PSPLIB format**: used by the [PSPLIB](https://www.om-db.wi.tum.de/psplib/) library to describe RCPSP and MMRCPSP instances.
2. **Patterson format**: used for RCPSP instances, mostly used by the [OR&S](https://www.projectmanagement.ugent.be/research/data) library. See [this](http://www.p2engine.com/p2reader/patterson_format) website for more details.
3. **MPLIB format**: used for RCMPSP instances from the [MPLIB](https://www.projectmanagement.ugent.be/research/data) library.

## Instance databases

The following websites host widely-used project scheduling benchmark instances.

- [PSPLIB](https://www.om-db.wi.tum.de/psplib/) contains different problem sets for various types of resource constrained project scheduling problems as well as optimal and heuristic solutions.

- [OR&S project database](https://www.projectmanagement.ugent.be/research/data) is the research data website of the Operations Research and Scheduling (OR&S) Research group of the Faculty of Economics and Business Administration at Ghent University (Belgium). OR&S is very active in the field of project scheduling and has published instances for many project scheduling variants.
