QUESTION_BANK = {

    "SQL": [
        "Explain INNER JOIN vs LEFT JOIN.",
        "What are Window Functions?",
        "Difference between RANK() and DENSE_RANK()?",
        "Write a query to find the second highest salary."
    ],

    "Python": [
        "What are list comprehensions?",
        "Explain generators.",
        "Difference between list and tuple?",
        "What is a decorator?"
    ],

    "Power BI": [
        "What is DAX?",
        "Difference between calculated column and measure?",
        "Explain Star Schema.",
        "What is Power Query?"
    ],

    "Excel": [
        "Explain VLOOKUP vs XLOOKUP.",
        "What are Pivot Tables?",
        "How do you remove duplicates?",
        "What is Conditional Formatting?"
    ],

    "Machine Learning": [
        "Explain overfitting.",
        "Bias vs Variance?",
        "What is Cross Validation?"
    ]
}


def generate_interview_questions(job_info, gap):

    questions = {}

    for skill in job_info["Skills"]:

        if skill in QUESTION_BANK:

            questions[skill] = QUESTION_BANK[skill]

    for skill in gap["Missing Skills"]:

        if skill in QUESTION_BANK:

            questions.setdefault(skill, QUESTION_BANK[skill])

    return questions