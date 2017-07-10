Unix: [![Unix Build Status](https://img.shields.io/travis/jacebrowning/env-diff/master.svg)](https://travis-ci.org/jacebrowning/env-diff) Windows: [![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/env-diff/master.svg)](https://ci.appveyor.com/project/jacebrowning/env-diff)<br>Metrics: [![Coverage Status](https://img.shields.io/coveralls/jacebrowning/env-diff/master.svg)](https://coveralls.io/r/jacebrowning/env-diff) [![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/jacebrowning/env-diff.svg)](https://scrutinizer-ci.com/g/jacebrowning/env-diff/?branch=master)<br>Usage: [![PyPI Version](https://img.shields.io/pypi/v/env-diff.svg)](https://pypi.python.org/pypi/env-diff)

# Overview

`env-diff` is a command-line to tool to generate reports to compare the value of environment variables in each of your environments against the defaults defined in various files. It will help you you find:

- variables absent from production, but will be required for a new feature in test
- production values that shouldn't be shared to your staging environment
- variables set that are no longer referenced in any files

This tool was built with [Heroku](https://www.heroku.com/continuous-delivery) in mind, but should work with any infrastructure that supports running commands remotely.

# Setup

## Requirements

* Python 3.6+

## Installation

Install `env-diff` with pip:

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

- `sourcefiles`: contain references to environment variables used in your project
    + `path`: relative path to source file
- `environments`: the environments in which your project runs
    + `name`: name of the environment
    + `command`: command to display currently set environment variables

Generate reports to show the differences between each environment variable:

```sh
$ env-diff
```

# Demo

Input YAML config file:

![input](https://raw.githubusercontent.com/jacebrowning/env-diff/master/docs/demo/input.png)

Running in a terminal:

![run](https://raw.githubusercontent.com/jacebrowning/env-diff/master/docs/demo/run.png)

Output (as viewed in [TableTool](https://github.com/jakob/TableTool)):

![output](https://raw.githubusercontent.com/jacebrowning/env-diff/master/docs/demo/output.png)




