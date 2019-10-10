# Traffic Management
A simple programme to manage traffic in a simplified model of a city,
based on planning (PDDL) and utility-driven search algorithm
(see the task specifications file: '*assessment_CS5060_ASMNT_C_2019_2020.pdf*').


## Installation and running
### Special dependencies
The package requires package *PyDDL* to be installed. It can be found at:
https://github.com/garydoranjr/pyddl.

It can be installed by executing the following command:

```console
C:\Users\xyz> pip install -e git+https://github.com/garydoranjr/pyddl.git#egg=pyddl
```

Detailed/alternative installation instructions are available at the project home page.


## Installation
To install the program, please run the *setup.py* script:

```console
C:\Users\xyz> cd path_to_the_project\traffic_management
C:\path_to_the_project\traffic_management> python setup.py install
```

### Execution
The main planner script is: '*traffic_management/traffic_planner/traffic_lights_system.py*'
After navigating to the '*traffic_management/traffic_planner/*' directory, it can be executed by:

```console
C:\...\traffic_management> cd traffic_planner
C:\...\traffic_management\traffic_planner> python traffic_lights_system.py
```

To learn about the available options to adjust the planning problem, use:

```console
C:\...\traffic_management\traffic_planner> python traffic_lights_system.py --help
```

##  Disclaimer
Code in package *custom_pyddl* is a customised version of *PyDDL*.

The aforementioned customisation includes:
- **for PDDL-like domain and problem definition:**
    - subclassing of certain classes (Action, Problem, State) - with the main purpose
    of adjusting the way of handling numerical effects of actions (see the respective docstrings)
    - rewriting some of the classes (GroundedAction), whose original structure was not suitable
    for subclassing; this heavily uses the original code, but also adds/alters some functionalities
- **for the planner:**
    - rewriting the planner in a form of a class
    - borrowing a considerable part of the original planner
    to maintain its compatibility with the domain and problem definition (usage, syntax, etc.)
    - replacing the A* search technique with a utility-driven hill-climbing algorithm
