[![PyPI version](https://img.shields.io/pypi/v/psplib?style=flat-square&label=PyPI)](https://pypi.org/project/psplib/)
[![CI](https://img.shields.io/github/actions/workflow/status/PyJobShop/PSPLIB/.github%2Fworkflows%2FCI.yml?branch=main&style=flat-square&logo=github&label=CI)](https://github.com/PyJobShop/PSPLIB/actions/workflows/CI.yml)

# PSPLIB

This library implements parsers for various project scheduling benchmark instances, including:
- Resource-Constrained Project Scheduling Problem (RCPSP)
- Multi-Mode RCPSP (MMRCPSP)
- RCPSP with Minimal and Maximal Time Lags (RCPSP/max)
- Resource-Constrained Multi Project Scheduling Problem (RCMPSP)
- RCPSP with flexible project structure (RCPSP-PS) and RCPSP with alternative subgraphs (RCPSP-AS)

`psplib` has no dependencies and can be installed in the usual way:

```
pip install psplib
```

## Example usage

``` python
>>> from psplib import parse
>>> instance = parse("data/j301_1.sm", instance_format="psplib") 
>>> instance.num_resources
4

>>> instance.resources
[Resource(capacity=12, renewable=True), ..., Resource(capacity=12, renewable=True)]

>>> instance.num_activities
32

>>> instance.activities
[Activity(modes=[Mode(duration=0, demands=[0, 0, 0, 0])], successors=[1, 2, 3], delays=None, name=''), 
 Activity(modes=[Mode(duration=8, demands=[4, 0, 0, 0])], successors=[5, 10, 14], delays=None, name=''),
 ...,
 Activity(modes=[Mode(duration=0, demands=[0, 0, 0, 0])], successors=[], delays=None, name='')]
```

See [this](https://github.com/PyJobShop/PSPLIB/blob/main/example.ipynb) notebook for a slightly longer example demonstration of PSPLIB.

## Instance formats

`psplib` implements parsers for commonly used project scheduling instance formats, listed below. 
To parse a specific instance format, set the `instance_format` argument in `parse`.

1. `psplib`: The **PSPLIB format** is used by the [PSPLIB](https://www.om-db.wi.tum.de/psplib/) library to describe RCPSP and MMRCPSP instances.
2. `patterson`: The **Patterson format**: used for RCPSP instances, mostly used by the [OR&S](https://www.projectmanagement.ugent.be/research/data) library. See [this](http://www.p2engine.com/p2reader/patterson_format) website for more details.
3. `rcpsp_max`: The **RCPSP/max format** is used for RCPSP/max instances from [TU Clausthal](https://www.wiwi.tu-clausthal.de/en/ueber-uns/abteilungen/betriebswirtschaftslehre-insbesondere-produktion-und-logistik/research/research-areas/project-generator-progen/max-and-psp/max-library/single-mode-project-duration-problem-rcpsp/max).
4. `mplib`: The **MPLIB format** is used for RCMPSP instances from the [MPLIB](https://www.projectmanagement.ugent.be/research/data) library.
5. `rcpsp_ps`: The **RCPSP-PS format** is the format used by [Van der Beek et al. (2024)](https://www.sciencedirect.com/science/article/pii/S0377221724008269).
Specifically, we included an extra line that defines for each task whether it is optional or not.
6. `aslib`: The **ASLIB format** is the format used by RCPSP-AS instances from the ASLIB instance set at [OR&S project database](https://www.projectmanagement.ugent.be/research/data).
ASLIB consist of three different parts (a, b, c). 
To use this parser, you have to merge parts (a) and (b) into a single file - part (c) is not parsed.

## Instance databases

The following websites host widely-used project scheduling benchmark instances.

- [PSPLIB](https://www.om-db.wi.tum.de/psplib/) contains different problem sets for various types of resource constrained project scheduling problems as well as optimal and heuristic solutions.

- [OR&S project database](https://www.projectmanagement.ugent.be/research/data) is the research data website of the Operations Research and Scheduling (OR&S) Research group of the Faculty of Economics and Business Administration at Ghent University (Belgium). OR&S is very active in the field of project scheduling and has published instances for many project scheduling variants.

- [TU Clausthal](https://www.wiwi.tu-clausthal.de/ueber-uns/abteilungen/betriebswirtschaftslehre-insbesondere-produktion-und-logistik/forschung-und-transfer/schwerpunkte/projekt-generator) provides RCPSP/max benchmark instances. 
