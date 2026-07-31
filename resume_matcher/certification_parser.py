CERTIFICATIONS = [

    "google data analytics",

    "microsoft power bi",

    "power bi data analyst associate",

    "aws cloud practitioner",

    "azure fundamentals",

    "azure data fundamentals",

    "tableau desktop specialist",

    "oracle sql",

    "snowflake",

    "ibm data analyst",

    "ibm data science",

    "coursera",

    "forage",

    "databricks",

    "sap",

    "google cloud",

    "aws certified solutions architect",

    "microsoft azure administrator"

]


def extract_certifications(resume_text):

    text = resume_text.lower()

    found = []

    for cert in CERTIFICATIONS:

        if cert in text:

            found.append(cert.title())

    found = sorted(

        list(set(found))

    )

    return {

        "Certifications": found,

        "Certification Count": len(found)

    }