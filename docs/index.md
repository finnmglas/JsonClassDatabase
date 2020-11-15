[![PyPI - Version][pypi-version-badge]][pypi]
[![Downloads][pepi-downloads-badge]][pepy tech]
[![Code style: black][code-black-badge]][code-black]

# JSON Class Database

En- and decode data-types and classes to JSON-type files or databases.

<a id="installation"></a>
## Installation

To install, run `pip install jcdb`.

<a id="usage"></a>
## Usage

Get started by importing `jcdb`:

```python
import jcdb
```

Inherit from the `jcdb.Object` class:

```python
# Create a dummy class
class I(jcdb.Object):
  pass

I.register(I)

# Create an object
i = I()

# Serialize / deserialize objects
i.encode() == I.decode(i.encode()) # True
```

This also works well if your inheriting class contains objects
of other inheriting `Object` classes that are registered.

## About

The JCDB source code is hosted [on GitHub](https://github.com/finnmglas/jcdb), the Python module [on PyPI][pypi] and its docs on [readthedocs](https://jcdb.readthedocs.io). It is provided under the MIT license.

JCDB is a project by [Finn M Glas][website], you can [sponsor] it or [contact Finn][contact] about major issues or cooperations.

<!-- Finns owned media -->
  [contact]: https://contact.finnmglas.com
  [sponsor]: https://sponsor.finnmglas.com
  [website]: https://www.finnmglas.com

<!-- GitHub related -->

  [joingh]: https://github.com/join
  [newissue]: https://github.com/finnmglas/jcdb/issues/new/choose
  [fork]: https://github.com/finnmglas/jcdb/fork
  [star]: https://github.com/finnmglas/jcdb/stargazers
  [shield-star]: https://img.shields.io/github/stars/finnmglas/jcdb?label=Star&style=social

  [shield-fork]: https://img.shields.io/github/forks/finnmglas/jcdb?label=Fork&style=social

<!-- Python Package -->
  [pypi]: https://pypi.org/project/jcdb/
  [pypi-version-badge]: https://img.shields.io/pypi/v/jcdb?color=000

  [pepy tech]: https://pepy.tech/project/jcdb
  [pepi-downloads-badge]: https://img.shields.io/badge/dynamic/json?style=flat&color=000&maxAge=10800&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fjcdb

  [code-black]: https://github.com/psf/black
  [code-black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg

<!-- Legal -->
  [MIT]: https://choosealicense.com/licenses/mit/
