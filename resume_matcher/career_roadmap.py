ROADMAP = {

    "Python":[

        "Practice Python fundamentals",

        "Complete 20 coding exercises",

        "Build one automation project"

    ],

    "SQL":[

        "Master JOINs",

        "Practice Window Functions",

        "Build SQL reporting project"

    ],

    "Power BI":[

        "Learn DAX",

        "Create KPI Dashboard",

        "Publish dashboard online"

    ],

    "Excel":[

        "Pivot Tables",

        "Power Query",

        "Dashboard"

    ],

    "Azure":[

        "Azure Fundamentals",

        "Deploy one cloud project"

    ],

    "AWS":[

        "Cloud Practitioner",

        "S3",

        "EC2"

    ],

    "Snowflake":[

        "Snowflake Essentials",

        "Build Warehouse"

    ]

}


def generate_career_roadmap(gap):

    roadmap = []

    for skill in gap["Missing Skills"]:

        if skill in ROADMAP:

            roadmap.append({

                "Skill":skill,

                "Tasks":ROADMAP[skill]

            })

    return roadmap