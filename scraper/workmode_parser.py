import re


def detect_work_mode(location):

    if not location:
        return "Unknown"

    location = str(location).lower()

    remote_keywords = [

        "remote",

        "work from home",

        "wfh",

        "home based",

        "telecommute"

    ]

    hybrid_keywords = [

        "hybrid",

        "remote/bangalore",

        "remote /",

        "hybrid work"

    ]

    for word in hybrid_keywords:

        if word in location:

            return "Hybrid"

    for word in remote_keywords:

        if word in location:

            return "Remote"

    return "On-site"