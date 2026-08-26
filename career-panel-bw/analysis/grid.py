# -*- coding: utf-8 -*-
"""The pre-specified moderation hypotheses.

Each entry is a claim of the form the career literature routinely reports:
the return to some career input depends on some characteristic of the worker
or the job. The hypotheses were fixed before any of them was estimated, and
all sixteen are reported whatever they show.
"""

# focal   the time-varying career input whose return is at issue
# mod     the moderator
# claim   the substantive proposition, stated as the literature states it
H = [
    # ---- NLS Young Women -------------------------------------------------
    dict(key="W1", panel="NLSW", focal="tenure", mod="collgrad",
         claim="Employer tenure raises wages more for college graduates."),
    dict(key="W2", panel="NLSW", focal="exper", mod="collgrad",
         claim="General work experience raises wages more for college "
               "graduates."),
    dict(key="W3", panel="NLSW", focal="tenure", mod="union",
         claim="Employer tenure raises wages more under a union contract."),
    dict(key="W4", panel="NLSW", focal="wks_ue", mod="collgrad",
         claim="Time spent unemployed depresses wages less for college "
               "graduates."),
    dict(key="W5", panel="NLSW", focal="wks_ue", mod="union",
         claim="Time spent unemployed depresses wages less for union "
               "members."),
    dict(key="W6", panel="NLSW", focal="exper", mod="married",
         claim="Work experience raises wages less for married women."),
    dict(key="W7", panel="NLSW", focal="hours", mod="collgrad",
         claim="Longer hours raise wages more for college graduates."),
    dict(key="W8", panel="NLSW", focal="tenure", mod="south",
         claim="Employer tenure raises wages less in the South."),
    # ---- NLSY79 young men ------------------------------------------------
    dict(key="M1", panel="NLSY79M", focal="exper", mod="postsec",
         claim="Work experience raises wages more for those with "
               "post-secondary schooling."),
    dict(key="M2", panel="NLSY79M", focal="exper", mod="union",
         claim="Work experience raises wages less under a union contract."),
    dict(key="M3", panel="NLSY79M", focal="exper", mod="married",
         claim="Work experience raises wages more for married men."),
    dict(key="M4", panel="NLSY79M", focal="hours", mod="postsec",
         claim="Longer hours raise wages more for those with "
               "post-secondary schooling."),
    dict(key="M5", panel="NLSY79M", focal="union", mod="postsec",
         claim="The union wage premium is smaller for the more educated."),
    dict(key="M6", panel="NLSY79M", focal="exper", mod="south",
         claim="Work experience raises wages less in the South."),
    dict(key="M7", panel="NLSY79M", focal="hours", mod="union",
         claim="Longer hours raise wages less under a union contract."),
    dict(key="M8", panel="NLSY79M", focal="married", mod="postsec",
         claim="The marriage wage premium is smaller for the more "
               "educated."),
]

# controls carried in every specification for a panel, besides the focal
# variable, the moderator and their product
CONTROLS = {
    "NLSW": ["tenure", "tenuresq", "exper", "expersq", "hours", "union",
             "married", "south", "urban"],
    "NLSY79M": ["exper", "expersq", "hours", "union", "married", "south",
                "urban"],
}

# person-level variables added only where they are identified, that is in the
# cross-sectional and pooled specifications
PERSON_LEVEL = {
    "NLSW": ["grade", "collgrad", "black"],
    "NLSY79M": ["grade", "postsec", "black", "hisp"],
}

LABEL = {
    "tenure": "employer tenure", "exper": "work experience",
    "hours": "weekly hours", "wks_ue": "weeks unemployed, per ten",
    "union": "union coverage", "married": "married",
    "collgrad": "college graduate", "postsec": "post-secondary schooling",
    "south": "resident in the South", "urban": "urban residence",
    "grade": "years of schooling", "black": "Black",
    "hisp": "Hispanic", "lwage": "log hourly wage",
}

PANEL_LABEL = {
    "NLSW": "NLS Young Women",
    "NLSY79M": "NLSY79 young men",
}


def by_panel(name):
    return [h for h in H if h["panel"] == name]
