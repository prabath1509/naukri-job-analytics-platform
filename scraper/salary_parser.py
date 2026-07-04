# =========================================================
# scraper/salary_parser.py
# =========================================================

import re


INVALID_SALARY_VALUES = {
    "",
    "nan",
    "none",
    "null",
    "unknown",
    "not available",
    "not disclosed",
    "salary not disclosed",
}


UNPAID_VALUES = {
    "unpaid",
    "unpaid internship",
    "no stipend",
}


# =========================================================
# CLEAN NUMBER
# =========================================================

def _parse_number(value):

    if value is None:
        return None

    value = str(value).strip().replace(",", "")

    try:
        return float(value)

    except ValueError:
        return None


# =========================================================
# CONVERT RUPEES TO LPA
# =========================================================

def _rupees_to_lpa(value):

    if value is None:
        return None

    return round(
        float(value) / 100000,
        2,
    )


# =========================================================
# PARSE SALARY
# =========================================================

def parse_salary(text):

    if text is None:
        return None, None

    text = str(text).strip()

    salary_key = text.casefold()

    if salary_key in INVALID_SALARY_VALUES:
        return None, None

    if salary_key in UNPAID_VALUES:
        return 0.0, 0.0

    # =====================================================
    # MONTHLY SALARY
    # =====================================================

    if (
        "month" in salary_key
        or "/month" in salary_key
        or "monthly" in salary_key
        or "per month" in salary_key
    ):

        numbers = re.findall(
            r"\d+(?:,\d+)*(?:\.\d+)?",
            text,
        )

        values = [
            _parse_number(number)
            for number in numbers
        ]

        values = [
            value
            for value in values
            if value is not None
        ]

        if not values:
            return None, None

        annual_lpa_values = [
            _rupees_to_lpa(
                value * 12
            )
            for value in values
        ]

        if len(annual_lpa_values) >= 2:

            return (
                annual_lpa_values[0],
                annual_lpa_values[1],
            )

        return (
            annual_lpa_values[0],
            annual_lpa_values[0],
        )

    # =====================================================
    # LACS / LAKHS / LPA
    # =====================================================

    if (
        "lac" in salary_key
        or "lakh" in salary_key
        or "lpa" in salary_key
    ):

        numbers = re.findall(
            r"\d+(?:,\d+)*(?:\.\d+)?",
            text,
        )

        values = [
            _parse_number(number)
            for number in numbers
        ]

        values = [
            value
            for value in values
            if value is not None
        ]

        if not values:
            return None, None

        # Naukri can expose mixed ranges such as:
        # 50,000-3 Lacs PA
        #
        # Values >= 1000 are interpreted as rupees.
        normalized_values = []

        for value in values:

            if value >= 1000:

                normalized_values.append(
                    _rupees_to_lpa(value)
                )

            else:

                normalized_values.append(
                    round(value, 2)
                )

        if len(normalized_values) >= 2:

            return (
                normalized_values[0],
                normalized_values[1],
            )

        return (
            normalized_values[0],
            normalized_values[0],
        )

    # =====================================================
    # RUPEE / ANNUAL SALARY
    # =====================================================

    if (
        "₹" in text
        or "rs." in salary_key
        or "rs " in salary_key
        or "inr" in salary_key
        or "per annum" in salary_key
        or "/year" in salary_key
        or "yearly" in salary_key
        or "annual" in salary_key
        or "pa" in salary_key
    ):

        numbers = re.findall(
            r"\d+(?:,\d+)*(?:\.\d+)?",
            text,
        )

        values = [
            _parse_number(number)
            for number in numbers
        ]

        values = [
            value
            for value in values
            if value is not None
        ]

        if not values:
            return None, None

        annual_lpa_values = [
            _rupees_to_lpa(value)
            for value in values
        ]

        if len(annual_lpa_values) >= 2:

            return (
                annual_lpa_values[0],
                annual_lpa_values[1],
            )

        return (
            annual_lpa_values[0],
            annual_lpa_values[0],
        )

    return None, None