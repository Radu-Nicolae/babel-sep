[//]: # (Style guideline: one sentence per line. i.e. insert new line after each period.)

# Assignment 1 - Testing

The current project is the sum of all work of [_Group 7_](https://canvas.vu.nl/groups/365690)'s project for the first assignment of the **Software Engineering Processes (XB_0089)** course

---

## Table of contents

| Task                                                                                                                                   | Sections                                                                                                                                                                                    |
|----------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [3.1. Project Choice](https://sep-vu.gitbook.io/software-engineering-processes/assignment-1-testing#id-3.1-project-choice)             | [Project choice](#project-choice)                                                                                                                                                           |
| [3.2. Coverage Measurement](https://sep-vu.gitbook.io/software-engineering-processes/assignment-1-testing#id-3.2-coverage-measurement) | [Executing (external) coverage tool](#executing-external-coverage-tool) <br> [Executing (our own) coverage tool](#executing-our-own-coverage-tool) <br> [Instrumentation](#instrumentation) |
| [3.3 Coverage Improvement](https://sep-vu.gitbook.io/software-engineering-processes/assignment-1-testing#id-3.2-coverage-measurement)  |                                                                                                                                                                                             |
| [3.4 Report](https://sep-vu.gitbook.io/software-engineering-processes/assignment-1-testing#id-3.4-report-readme.md)                    | [README.md](README.md)                                                                                                                                                                      |

---

## Project choice

The project of choice is [Babel](https://github.com/python-babel/babel). Latest release of the project at the time of writing is [v2.15.0](https://github.com/python-babel/babel/releases/tag/v2.15.0).
> Babel is a Python library that provides an integrated collection of utilities that assist with internationalizing and localizing Python applications (in particular web-based applications.)

| Requirement                     |                                   Babel                                   |
|---------------------------------|:-------------------------------------------------------------------------:|
| Hosted on GitHub                |         [Repository Link](https://github.com/python-babel/babel)          |
| Open Source License             |        [BSD-3-Clause](https://opensource.org/license/bsd-3-clause)        |
| Automated unit tests            | [Test Directory](https://github.com/python-babel/babel/tree/master/tests) |
| Existing branch coverage < 100% |                                    89%                                    |
| Contributors                    |                                    150                                    |
| Lines of code                   |                   17 KLOC <br>11 KLOC (excluding tests)                   |

---

## Executing (external) coverage tool

We aim to calculate the project's total coverage using the `coverage.py` tool.
To do this, we first set up the project's environment, following its [documentation](https://babel.pocoo.org/en/latest/installation.html#living-on-the-edge) and install the necessary [dependencies](requirements.txt).

### Setup

> **TL;DR** - Setup
>
> ```bash
> make setup_sep
> ```
> Or without `make`:
> ```bash
> virtualenv venv > /dev/null
> cp -r sep_coverage venv/lib/python3.12/site-packages/
> (. ./venv/bin/activate && pip install -r requirements.txt && export PYTHONPATH=$(realpath venv/lib/python3.12/site-packages/) && python setup.py import_cldr && pip install --editable .) > /dev/null 2>&1
> ```
> [➡️ Skip setup explanation](#running)

A virtual environment _venv_ is required to run coverage. We first installed `virtualenv` and `pip` using each operating system's package manager (either [brew](https://brew.sh/) or [pacman](https://wiki.archlinux.org/title/pacman)).

After that, we copy the local package _sep_coverage_ (created by ourselves) to the virtual environment's site-packages directory.
An explanation for this will come in the [Own coverage tool](#executing-our-own-coverage-tool) section.

> ⚠️ **WARNING**: The setup assumes that the latest version of python (3.12) is installed on the system, as well as the `virtualenv` and `pip` packages. If this is not the case, the setup will fail.

The project's [documentation](https://babel.pocoo.org/en/latest/installation.html#living-on-the-edge) was followed to install the project's dependencies and import the CLDR (Common Locale Data Repository) data.
However, it does not mention the need to set the `PYTHONPATH` environment variable to the virtual environment's site-packages directory.
This is to ensure that some tests that create a separate virtual environment will maintain the correct path to the _sep_coverage_ package.
Also, there are [some external packages](requirements.txt) that need to be installed.

The entire process is summed up in the `setup_sep` target of the [Makefile](Makefile).

![Proof Makefile](https://i.imgur.com/QFELCcQ.png)

### Running

> **TL;DR** - Running
>
> ```bash
> make coverage_extern
>```
> Or without `make`:
> ```bash
> . ./venv/bin/activate && coverage run --omit='sep_coverage/*','tests/*' -m pytest && coverage report > coverage_report.txt
> cat coverage_report.txt
> ```
> [➡️ Skip running explanation](#results)

We first enter the python virtual environment by sourcing the `activate` script in the `venv` directory.

The coverage.py tool has a `run` command that runs the coverage test and a `report` command that generates a report of the coverage in plain text.
These two commands will represent our two-step process in running the coverage.

The `run` command takes one argument, `--omit`, which is used to specify which files to omit from the coverage report and another argument `-m pytest` to run the tests using the pytest module.
We are using pytest to run the tests that generate the coverage for the project, because
it is the testing framework used by the project itself.

**IMPORTANT**: We omit the files in the `sep_coverage/` package and the `tests/` directory from the coverage report. This is because the sep_coverage package is our own coverage tool, and the tests directory contains are not of interest for the purposes of coverage, _as the tests themselves generate the coverage_. We are only interested in the coverage of the `babel` package.

Finally, we generate the coverage report using the `report` command.

The entire process is summed up in the `coverage_extern` target of the [Makefile](Makefile).

![Proof Makefile](https://i.imgur.com/VRk5EjD.png)

### Results

The entire result file, containing coverage data for every single file in the project, can be found in [report/extern_coverage_before.txt](report/extern_coverage_before.txt).

| Total Statements | Total Missed | Coverage |
|------------------|--------------|----------|
| 4526             | 490          | 89.17%   |

---

## Executing (our own) coverage tool

We create our own coverage tool, `sep_coverage`, using **manual instrumentation** to measure the coverage of _some parts_ of the project.
The tool is documented under [sep_coverage/README.md](sep_coverage/README.md).

> **TL;DR** - Running
>
> ⚙️ **Prerequisite**: [Setup](#setup) (only has to be done once)
>
> ```bash
> make coverage_sep
> ```
> or without `make`:
> ```bash
> . ./venv/bin/activate && python3 sep_coverage.py
> ```
> [➡️ Skip to results](#results-1)

### Breakdown of the tool

The **sep_coverage** tool is built as a python package under the `sep_coverage/` directory.
Because of this, it must be copied under the virtual environment's site-packages directory to be imported by the project.

At each `instrument()` call, the tool stores the identifier of the statement in a set mapped to each entity (file, class, function, method) that the statement belongs to.
Each entity is indexed in [sep_coverage/program_entity.py](sep_coverage/program_entity.py), containing a range of statements that it covers.

After execution, we can use the set of each entity to calculate how many statements were reached, as the length of the set.
The total number of statements is simply equal to the upper bound of the range, minus the lower bound plus one.

We can use this information to calculate the coverage of each entity, given the following formula, where C = coverage, M = total statements, N = total missed statements:

<div style="text-align:center"><img alt="formula" src="https://latex.codecogs.com/png.image?\LARGE&space;\dpi{110}\bg{white}C=\frac{T-M}{T}"/></div>

When the tool is run, the coverage test is executed, and then the coverage data is printed to _stdout_.

### Methodology of instrumentation

Each team member look at the coverage report of generated by `coverage.py` (specifically the html report created by running `coverage html`) and choose at least two functions or methods with low coverage to instrument.
The [html coverage report page](htmlcov/index.html) provides useful information, such as which exact lines are not covered by the tests.

Each function, method, class (_Entity_) is instrumented by the following syntax:

```python
import sep_coverage

sep_coverage.instrument([ENTITY_FLAG_1, ENTITY_FLAG_2, ...], instrument_id)
```

This method allows us to store the following coverage information for each instrumented line of code:

- Which entity the line belongs to (file, class, function or method)
- The instrument identifier of the line
- Whether the line was executed during the tests

### Results

The coverage report generated by our tool, before the coverage improvement can be found in [report/sep_coverage_before.txt](report/sep_coverage_before.txt).

| Total Statements | Total Missed | Coverage |
|------------------|--------------|----------|
| 57               | 25           | 56.14%   |

Since we are only instrumenting a small part of the project, the coverage **is expected to be low**.
We specifically targeted parts of the code that were not covered by the tests, in order to work on improving coverage in the next step.

---

## Instrumentation

[//]: # (TODO:)
[//]: # (2. Instrumentation of functions for coverage measurement There is evidence code diff + screenshot of the results that each student measured the coverage of 2 functions.)
[//]: # (3. Functionality of the instrumentation for coverage measurement There is evidence execution during the presentation that the instrumentation of each group member works)

