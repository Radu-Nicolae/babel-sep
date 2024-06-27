[//]: # (Style guideline: one sentence per line. i.e. insert new line after each period.)

# Assignment 1 - Testing

The current project is the sum of all work of [_Group 7_](https://canvas.vu.nl/groups/365690)'s project for the first assignment of the **Software Engineering Processes (XB_0089)** course.

The presentation of the project in Google Slides is available [here](https://docs.google.com/presentation/d/15BjP3BdKf-idsQpiZxpE2ipv24Csj1lQmtNdSsQj4L8/edit#slide=id.g2e48b51bef8_0_224).

## Table of contents

| Task                                                                                                                                   | Sections                                                                                                                                                                                    |
|----------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [3.1. Project Choice](https://sep-vu.gitbook.io/software-engineering-processes/assignment-1-testing#id-3.1-project-choice)             | [Project choice](#project-choice)                                                                                                                                                           |
| [3.2. Coverage Measurement](https://sep-vu.gitbook.io/software-engineering-processes/assignment-1-testing#id-3.2-coverage-measurement) | [Executing (external) coverage tool](#executing-external-coverage-tool) <br> <sub><sup> [4.1 Execution of existing coverage measurement tool](#41-execution-of-existing-coverage-measurement-tool) </sup></sub> <br> [Instrumentation](#instrumentation) <br> <sub><sup>[4.2 Instrumentation of functions for coverage measurement](#42-instrumentation-of-functions-for-coverage-measurement) </sup></sub> <br> [Executing (our own) coverage tool](#executing-our-own-coverage-tool) <br> <sub><sup>[4.3 Functionality of the instrumentation for coverage measurement](#43-functionality-of-the-instrumentation-for-coverage-measurement) </sup></sub>|
| [3.3 Coverage Improvement](https://sep-vu.gitbook.io/software-engineering-processes/assignment-1-testing#id-3.2-coverage-measurement) | [Tests overview](#tests-overview) <br><sub><sup>[4.4 Creation/enhancement of new tests](#44-creationenhancement-of-new-tests) </sup></sub> <br>  <sub><sup>[4.5 Functionality of the new/enhanced tests](#45-functionality-of-the-newenhanced-tests) </sup></sub> <br> [Overall coverage improvement](#overall-coverage-improvement) <br> <sub><sup>[4.6 Effectiveness of each new/enhanced test in improving coverage](#46-effectiveness-of-each-newenhanced-test-in-improving-coverage) </sup></sub> <br>  <sub><sup>[4.7 Overall improvement in coverage](#47-overall-improvement-in-coverage)</sup></sub>|  <br> |                                                                                                                                                                                             |
| [3.4 Report](https://sep-vu.gitbook.io/software-engineering-processes/assignment-1-testing#id-3.4-report-readme.md)                    | [README.md](README.md)                                                                                                                                                                      |

<br>

## Project choice

The project of choice is [Babel](https://github.com/python-babel/babel). Latest release of the project as of Jun 11th, 2024, is [v2.15.0](https://github.com/python-babel/babel/releases/tag/v2.15.0).
> _"Babel is a Python library that provides an integrated collection of utilities that assist with internationalizing and localizing Python applications (in particular web-based applications.)"
>
> from Babel's README.md

| Requirement                     |                                   Babel                                   |
|---------------------------------|:-------------------------------------------------------------------------:|
| Hosted on GitHub                |         [Repository Link](https://github.com/python-babel/babel)          |
| Open Source License             |        [BSD-3-Clause](https://opensource.org/license/bsd-3-clause)        |
| Automated unit tests            | [Test Directory](https://github.com/python-babel/babel/tree/master/tests) |
| Existing branch coverage < 100% |                                    89%                                    |
| Contributors                    |                                    150                                    |
| Lines of code                   |                   17 KLOC <br>11 KLOC (excluding tests)                   |

<br> 

## Executing (external) coverage tool
### 4.1 Execution of existing coverage measurement tool

We calculate the project's total coverage using the `coverage.py` tool.
We first set up the project's environment, following its [documentation](https://babel.pocoo.org/en/latest/installation.html#living-on-the-edge) and install the necessary [dependencies](requirements.txt).

### Setup

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

After that, we copy the local package _sep_coverage_ (created by ourselves) to the virtual environment's site-packages directory (further expanded in [Own coverage tool](#executing-our-own-coverage-tool) section).


> ⚠️ **WARNING**: The setup assumes that the latest version of python (3.12) is installed on the system, as well as the `virtualenv` and `pip` packages. If this is not the case, the setup will fail.

The project's [documentation](https://babel.pocoo.org/en/latest/installation.html#living-on-the-edge) was followed to install the project's dependencies and import the CLDR (Common Locale Data Repository) data.
However, it does not mention the need to set the `PYTHONPATH` environment variable to the virtual environment's site-packages directory.
This is to ensure that some tests that create a separate virtual environment will maintain the correct path to the _sep_coverage_ package.
Also, there are [some external packages](requirements.txt) that need to be installed.

The entire process is summed up in the `setup_sep` target of the [Makefile](Makefile).

![Proof Makefile](https://i.imgur.com/QFELCcQ.png)

### Running

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
We are using pytest to run the tests that generate the coverage for the project. Pytest is also the testing framework used by the project itself.

**IMPORTANT**: We omit the files in the `sep_coverage/` package and the `tests/` directory from the coverage report. This is because the sep_coverage package is our own coverage tool, and the tests directory contains are not of interest for the purposes of coverage, _as the tests themselves generate the coverage_. We are only interested in the coverage of the `babel` package.

Finally, we generate the coverage report using the `report` command.

The entire process is summed up in the `coverage_extern` target of the [Makefile](Makefile).

![Proof Makefile](https://i.imgur.com/VRk5EjD.png)

### Results

The entire result file, containing coverage data for every single file in the project, can be found in [report/extern_coverage_before.txt](report/extern_coverage_before.txt).

| Total Statements | Total Missed | Coverage |
|------------------|--------------|----------|
| 4526             | 490          | 89.17%   |

<br> 

## Executing (our own) coverage tool
### 4.3 Functionality of the instrumentation for coverage measurement

We create our own coverage tool, `sep_coverage`, using **manual instrumentation** to measure the coverage of _some parts_ of the project.
The tool is documented under [sep_coverage/README.md](sep_coverage/README.md).

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
The total number of statements is equal to the upper bound of the range, minus the lower bound plus one.

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

<br>

## Instrumentation
### 4.2 Instrumentation of functions for coverage measurement
| Member  | Entities Instrumented                                                                                                                                               | Total lines of code |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|
| Daniel  | [FixedOffsetTimezone](babel/util.py) <br> [_locales_to_names()](babel/support.py)                                                                                   | 14                  |
| Gleb    | [get_timezone()](babel/dates.py) <br> [_get_time()](babel/dates.py)                                                                                                 | 26                  |                                                         
| Mateusz | [_get_tzinfo()](babel/localtime/_helpers.py) <br> [_get_tzinfo_or_raise()](babel/localtime/_helpers.py) <br> [_get_tzinfo_from_file()](babel/localtime/_helpers.py) | 49                  |
| Radu    | [format_date()](babel/dates.py) <br> [\_\_str\_\_()](babel/dates.py)                                                                                                | 38                  |                                                                             

### Instrumentation proofs

<details>
<summary>Daniel Halasz</summary>

![_locales_to_names()](https://i.imgur.com/PmQVeqt.png)
![_FixedOffsetTimezone](https://i.imgur.com/PmQVeqt.png)

</details>

<details>
<summary>Mateusz Kwiatkowski</summary>

![_get_tzinfo](https://i.imgur.com/3SMtCA3.png)
![_get_tzinfo_or_raise](https://i.imgur.com/bVsJHiQ.png)
![_get_tzinfo_from_file](https://i.imgur.com/eR4xsh1.png)

</details>

<details>
<summary>Radu Nicolae</summary>

![format_date()](https://i.imgur.com/a04oABT.png)
![\_\_str()\_\_](https://i.imgur.com/2bl5gUS.png)

</details>

<details>
<summary>Gleb Mishchenko</summary>

![get_timezone()](https://i.imgur.com/vrlfXoo.png)
![_get_time()](https://i.imgur.com/NAIQ5tJ.png)

</details>

### Measurement proofs

![Coverage measurement](https://i.imgur.com/k82uZJg.png)

[//]: # (TODO:)

[//]: # (2. Instrumentation of functions for coverage measurement There is evidence code diff + screenshot of the results that each student measured the coverage of 2 functions.)

[//]: # (3. Functionality of the instrumentation for coverage measurement There is evidence execution during the presentation that the instrumentation of each group member works)

## Coverage improvement
### Tests overview
---
### 4.4 Creation/enhancement of new tests
Below is the evidence (code) that each student created/enhanced 2 tests, repsectively to their instrumented functions.

<details>
<summary>Daniel Halasz</summary>

![_locales_to_names()](https://i.imgur.com/lcX4vSU.png)

</details>

<details>
<summary>Mateusz Kwiatkowski</summary>

![test_get_tzinfo](https://i.imgur.com/VkMSyW8.png)
![test_get_tzinfo_from_file](https://i.imgur.com/fs4rgSQ.png)

</details>

<details>
<summary>Radu Nicolae</summary>

![format_date()](https://i.imgur.com/BiEKBcb.png)

</details>

<details>
<summary>Gleb Mishchenko</summary>

![get_timezone()](https://i.imgur.com/A7YLS2J.png)

</details>

### 4.5 Functionality of the new/enhanced tests
### General approach

Each team member after instrumenting their respective functions, and after looking at the coverage report of generated by `coverage.py` implemented specific tests to increase the coverage of these functions. 

Each function got tested in a distinct, specific way, unique to its purpose. For example in `tests_mateusz.py` the coverage of the _get_tzinfo_or_raise() function is achieved by making sure certain `errors` and `assertions` are raised (or not). 

```python
    with pytest.raises(LookupError):
        _helpers._get_tzinfo_or_raise("Continent/City")

    tzinfo = _helpers._get_tzinfo_or_raise("America/New_York")
    assert tzinfo is not None
    assert tzinfo.zone == "America/New_York"
```

This method allowed each team member to successfully increase the overall coverage of their chosen functions, as, for example, more statements and if-else branches are reached after implementing the tests. 

The correctness of our tests is presented with the following screenshot, after running `pytest` with the new tests.

![pytest](https://i.imgur.com/SnlE65A.png)

### Overall coverage improvement
---
### 4.6 Effectiveness of each new/enhanced test in improving coverage


The coverage report generated by our tool before the coverage improvement is summarized in the following table

| Total Statements | Total Missed | Coverage |
|------------------|--------------|----------|
| 57               | 25           | 56.14%   |


Since we specifically targeted parts of the code that were not covered by the general tests, and each team member managed to increase their instrumented function coverage almost to its fullest, we report the following coverage **after** implementing the enhanced tests

| Total Statements | Total Missed | Coverage |
|------------------|--------------|----------|
| 57               | 4           | 92.98%   |

This improvement is also showcased in the following screenshot. After running the suggested tool, `coverage.py`, on the initial directory and the directory with the ehnanced tests, we compared the two reports with `diff`. 

![effectiv](https://i.imgur.com/GUptPa8.png)
### 4.7 Overall improvement in coverage
With this we conclude that the total overall improvement that we reached amounted to **1.12%**. The following screenshots of running `coverage.py` without and with the enhanced tests show the total coverage measured before and after.

## Before
![before](https://i.imgur.com/2R85Tkt.png)

## After
![after](https://i.imgur.com/gOt8paA.png)