Unix: [![Unix Build Status](https://img.shields.io/travis/jacebrowning/env-diff/master.svg)](https://travis-ci.org/jacebrowning/env-diff) Windows: [![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/env-diff/master.svg)](https://ci.appveyor.com/project/jacebrowning/env-diff)<br>Metrics: [![Coverage Status](https://img.shields.io/coveralls/jacebrowning/env-diff/master.svg)](https://coveralls.io/r/jacebrowning/env-diff) [![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/jacebrowning/env-diff.svg)](https://scrutinizer-ci.com/g/jacebrowning/env-diff/?branch=master)<br>Usage: [![PyPI Version](https://img.shields.io/pypi/v/env-diff.svg)](https://pypi.python.org/pypi/env-diff)

# Overview

Compares expected environment variables to those set in production.

# Setup

## Requirements

* Python 3.6+

## Installation

Install env-diff with pip:

```sh
$ pip install env-diff
```

or directly from the source code:

```sh
$ git clone https://github.com/jacebrowning/env-diff.git
$ cd env-diff
$ python setup.py install
```

# Usage

Generate a sample config file:

```sh
$ env-diff --init
```

Customize this file to match your project:

- `files`: a list of file paths that contain the names of environment variables used in your project
- `environments`: a list of the environments in which your project runs
    + `name`: name of the environment
    + `command`: command to display currently set environment variables

Display the differences between environment variables in your environments:

```sh
$ env-diff
```


