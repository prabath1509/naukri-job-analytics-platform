GREENHOUSE_BOARDS = [
    "databricks",
    "airbnb",
    "stripe",
    "figma",
    "reddit",
    "robinhood",
    "affirm",
    "asana",
    "pinterest",
    "lyft",
    "scaleai",
    "instacart",
    "anthropic",
    "samsara",
    "twilio",
    "brex",
    "coinbase",
    "okta",
    "toast",
    "cloudflare",
    "gusto",
    "discord",
    "dropbox",
    "webflow",
    "squarespace",
]


LEVER_COMPANIES = {
    "figma": "Figma",
    "mongodb": "MongoDB",
    "scale-ai": "Scale AI",
    "applydigital": "Apply Digital",
    "brightwheel": "Brightwheel",
    "postscript": "Postscript",
    "sourcegraph": "Sourcegraph",
    "1password": "1Password",
}


WORKDAY_COMPANIES = [
    {
        "company": "Mastercard",
        "url": (
            "https://mastercard.wd1.myworkdayjobs.com/"
            "wday/cxs/mastercard/CorporateCareers/jobs"
        ),
    },
    {
        "company": "Salesforce",
        "url": (
            "https://salesforce.wd12.myworkdayjobs.com/"
            "wday/cxs/salesforce/External_Career_Site/jobs"
        ),
    },
    {
        "company": "Adobe",
        "url": (
            "https://adobe.wd5.myworkdayjobs.com/"
            "wday/cxs/adobe/external_experienced/jobs"
        ),
    },
    {
        "company": "Intel",
        "url": (
            "https://intel.wd1.myworkdayjobs.com/"
            "wday/cxs/intel/External/jobs"
        ),
    },
    {
        "company": "PayPal",
        "url": (
            "https://paypal.wd1.myworkdayjobs.com/"
            "wday/cxs/paypal/jobs/jobs"
        ),
    },
    {
        "company": "Autodesk",
        "url": (
            "https://autodesk.wd1.myworkdayjobs.com/"
            "wday/cxs/autodesk/Ext/jobs"
        ),
    },
]


SMARTRECRUITERS_COMPANIES = [
    "bosch",
    "visa",
    "logitech",
    "ubisoft",
    "dhl",
    "pandora",
    "volvogroup",
    "tesla",
]


def validate_source_registry():
    checks = {
        "greenhouse_unique": (
            len(GREENHOUSE_BOARDS)
            == len(set(GREENHOUSE_BOARDS))
        ),
        "lever_unique": (
            len(LEVER_COMPANIES)
            == len(set(LEVER_COMPANIES))
        ),
        "workday_company_unique": (
            len(WORKDAY_COMPANIES)
            == len(
                {
                    source["company"]
                    for source in WORKDAY_COMPANIES
                }
            )
        ),
        "workday_url_unique": (
            len(WORKDAY_COMPANIES)
            == len(
                {
                    source["url"]
                    for source in WORKDAY_COMPANIES
                }
            )
        ),
        "smartrecruiters_unique": (
            len(SMARTRECRUITERS_COMPANIES)
            == len(set(SMARTRECRUITERS_COMPANIES))
        ),
    }

    return checks


def get_source_capacity():
    return {
        "Greenhouse": len(GREENHOUSE_BOARDS),
        "Lever": len(LEVER_COMPANIES),
        "Workday": len(WORKDAY_COMPANIES),
        "SmartRecruiters": len(
            SMARTRECRUITERS_COMPANIES
        ),
    }