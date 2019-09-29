# Traffic Management

A simple programme to manage traffic in a simplified model of a city,
based on planning (PDDL) and utility-driven search algorithm
(see the task specifications file: '*assessment_CS5060_ASMNT_C_2019_2020.pdf*').

##  Disclaimer
Code in package *custom_pyddl* is a customised version of Python package *pyddl*, which can be found at:
https://github.com/garydoranjr/pyddl.

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


### Note
Due to subclassing, the original *pyddl* package is still needed to run this program.
It can be installed by executing the following command:

*pip install -e git+https://github.com/garydoranjr/pyddl.git#egg=pyddl*

Detailed/alternative installation instructions are available at the project home page
(https://github.com/garydoranjr/pyddl).