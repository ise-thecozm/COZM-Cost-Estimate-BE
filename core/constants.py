"""
Port of constants.ts — LOCATIONS, TIER_BENEFITS, EXCHANGE_RATES,
COUNTRY_INSIGHTS, and has_totalization_agreement.
"""

LOCATIONS = [
    {
        "code": "US", "name": "United States", "currency": "USD",
        "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 16100,
        "standardDeductionJoint": 32200, "socialSecurityRateEmployee": 0.0765,
        "socialSecurityRateEmployer": 0.0765, "socialSecurityCap": 184500,
        "taxBrackets": [
            {"min": 0, "max": 12400, "rate": 0.1},
            {"min": 12401, "max": 50400, "rate": 0.12},
            {"min": 50401, "max": 105700, "rate": 0.22},
            {"min": 105701, "max": 201775, "rate": 0.24},
            {"min": 201776, "max": 256225, "rate": 0.32},
            {"min": 256226, "max": 640600, "rate": 0.35},
            {"min": 640600, "max": None, "rate": 0.37},
        ],
        "taxBracketsJoint": [
            {"min": 0, "max": 24800, "rate": 0.1},
            {"min": 24801, "max": 100800, "rate": 0.12},
            {"min": 100801, "max": 211400, "rate": 0.22},
            {"min": 211401, "max": 403550, "rate": 0.24},
            {"min": 403551, "max": 512450, "rate": 0.32},
            {"min": 512451, "max": 768700, "rate": 0.35},
            {"min": 768700, "max": None, "rate": 0.37},
        ],
        "cities": [
            {"code": "AK", "name": "Alaska", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0},
            {"code": "FL", "name": "Florida", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0},
            {"code": "NV", "name": "Nevada", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0},
            {"code": "NH", "name": "New Hampshire", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0},
            {"code": "SD", "name": "South Dakota", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0},
            {"code": "TN", "name": "Tennessee", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0},
            {"code": "TX", "name": "Texas", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0},
            {"code": "WY", "name": "Wyoming", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0},
            {"code": "WA", "name": "Washington", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0.07},
            {"code": "AZ", "name": "Arizona", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0.025},
            {"code": "CO", "name": "Colorado", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0.044},
            {"code": "IL", "name": "Illinois", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0.0495},
            {"code": "IN", "name": "Indiana", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0.0295},
            {"code": "KY", "name": "Kentucky", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0.035},
            {"code": "MI", "name": "Michigan", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0.0425},
            {"code": "NC", "name": "North Carolina", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0.0399},
            {"code": "PA", "name": "Pennsylvania", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0.0307},
            {
                "code": "CA", "name": "California", "avgTax": 0.30, "colaIndex": 115,
                "stateStandardDeduction": 5363, "stateStandardDeductionJoint": 10726, "stateTaxRate": 0.09,
                "stateTaxBrackets": [
                    {"min": 0, "max": 10412, "rate": 0.01}, {"min": 10413, "max": 24684, "rate": 0.02},
                    {"min": 24685, "max": 38959, "rate": 0.04}, {"min": 38960, "max": 54081, "rate": 0.06},
                    {"min": 54082, "max": 68350, "rate": 0.08}, {"min": 68351, "max": 349137, "rate": 0.093},
                    {"min": 349138, "max": 418961, "rate": 0.103}, {"min": 418962, "max": 698271, "rate": 0.113},
                    {"min": 698272, "max": None, "rate": 0.123},
                ],
                "stateTaxBracketsJoint": [
                    {"min": 0, "max": 20824, "rate": 0.01}, {"min": 20825, "max": 49368, "rate": 0.02},
                    {"min": 49369, "max": 77918, "rate": 0.04}, {"min": 77919, "max": 108162, "rate": 0.06},
                    {"min": 108163, "max": 136700, "rate": 0.08}, {"min": 136701, "max": 698274, "rate": 0.093},
                    {"min": 698275, "max": 837922, "rate": 0.103}, {"min": 837923, "max": 1396542, "rate": 0.113},
                    {"min": 1396543, "max": None, "rate": 0.123},
                ],
            },
            {
                "code": "NY", "name": "New York", "avgTax": 0.30, "colaIndex": 110,
                "stateStandardDeduction": 8000, "stateStandardDeductionJoint": 16050, "stateTaxRate": 0.055,
                "stateTaxBrackets": [
                    {"min": 0, "max": 8500, "rate": 0.04}, {"min": 8501, "max": 11700, "rate": 0.045},
                    {"min": 11701, "max": 13900, "rate": 0.0525}, {"min": 13901, "max": 80650, "rate": 0.055},
                    {"min": 80651, "max": 215400, "rate": 0.06}, {"min": 215401, "max": 1077550, "rate": 0.0685},
                    {"min": 1077551, "max": 5000000, "rate": 0.0965}, {"min": 5000001, "max": 25000000, "rate": 0.103},
                    {"min": 25000001, "max": None, "rate": 0.109},
                ],
                "stateTaxBracketsJoint": [
                    {"min": 0, "max": 17150, "rate": 0.04}, {"min": 17151, "max": 23600, "rate": 0.045},
                    {"min": 23601, "max": 27900, "rate": 0.0525}, {"min": 27901, "max": 161550, "rate": 0.055},
                    {"min": 161551, "max": 323200, "rate": 0.06}, {"min": 323201, "max": 2155350, "rate": 0.0685},
                    {"min": 2155351, "max": 5000000, "rate": 0.0965}, {"min": 5000001, "max": 25000000, "rate": 0.103},
                    {"min": 25000001, "max": None, "rate": 0.109},
                ],
            },
            {"code": "NYC", "name": "New York City, NY", "avgTax": 0.35, "colaIndex": 110, "stateTaxRate": 0.06, "localTaxRate": 0.038},
            {"code": "PHL", "name": "Philadelphia, PA", "avgTax": 0.25, "colaIndex": 100, "stateTaxRate": 0.0307, "localTaxRate": 0.0374},
            {"code": "SFO", "name": "San Francisco, CA", "avgTax": 0.32, "colaIndex": 115, "stateTaxRate": 0.093},
            {"code": "DET", "name": "Detroit, MI", "avgTax": 0.25, "colaIndex": 90, "stateTaxRate": 0.0425, "localTaxRate": 0.024},
            {"code": "NJ", "name": "New Jersey", "avgTax": 0.25, "colaIndex": 105, "stateTaxRate": 0.06},
            {"code": "RI", "name": "Rhode Island", "avgTax": 0.25, "colaIndex": 100, "stateTaxRate": 0.0375},
            {"code": "HI", "name": "Hawaii", "avgTax": 0.25, "colaIndex": 110, "stateTaxRate": 0.08},
            {"code": "MA", "name": "Massachusetts", "avgTax": 0.28, "colaIndex": 108, "stateTaxRate": 0.05},
            {"code": "CT", "name": "Connecticut", "avgTax": 0.28, "colaIndex": 105, "stateTaxRate": 0.05},
            {"code": "OR", "name": "Oregon", "avgTax": 0.28, "colaIndex": 100, "stateTaxRate": 0.08},
            {"code": "AL", "name": "Alabama", "avgTax": 0.20, "colaIndex": 90, "stateTaxRate": 0.02},
            {"code": "AR", "name": "Arkansas", "avgTax": 0.20, "colaIndex": 90, "stateTaxRate": 0.02},
            {"code": "DE", "name": "Delaware", "avgTax": 0.20, "colaIndex": 95, "stateTaxRate": 0.022},
            {"code": "GA", "name": "Georgia", "avgTax": 0.20, "colaIndex": 95, "stateTaxRate": 0.0549},
            {"code": "ID", "name": "Idaho", "avgTax": 0.20, "colaIndex": 95, "stateTaxRate": 0.058},
            {"code": "IA", "name": "Iowa", "avgTax": 0.20, "colaIndex": 90, "stateTaxRate": 0.038},
            {"code": "KS", "name": "Kansas", "avgTax": 0.20, "colaIndex": 90, "stateTaxRate": 0.052},
            {"code": "LA", "name": "Louisiana", "avgTax": 0.20, "colaIndex": 90, "stateTaxRate": 0.03},
            {"code": "ME", "name": "Maine", "avgTax": 0.20, "colaIndex": 95, "stateTaxRate": 0.058},
            {"code": "MD", "name": "Maryland", "avgTax": 0.25, "colaIndex": 100, "stateTaxRate": 0.0475},
            {"code": "MN", "name": "Minnesota", "avgTax": 0.25, "colaIndex": 100, "stateTaxRate": 0.0535},
            {"code": "MS", "name": "Mississippi", "avgTax": 0.20, "colaIndex": 90, "stateTaxRate": 0.04},
            {"code": "MO", "name": "Missouri", "avgTax": 0.20, "colaIndex": 90, "stateTaxRate": 0.04},
            {"code": "MT", "name": "Montana", "avgTax": 0.20, "colaIndex": 95, "stateTaxRate": 0.047},
            {"code": "NE", "name": "Nebraska", "avgTax": 0.20, "colaIndex": 90, "stateTaxRate": 0.0246},
            {"code": "NM", "name": "New Mexico", "avgTax": 0.20, "colaIndex": 90, "stateTaxRate": 0.015},
            {"code": "ND", "name": "North Dakota", "avgTax": 0.20, "colaIndex": 90, "stateTaxRate": 0.0195},
            {"code": "OH", "name": "Ohio", "avgTax": 0.20, "colaIndex": 90, "stateTaxRate": 0.0275},
            {"code": "OK", "name": "Oklahoma", "avgTax": 0.20, "colaIndex": 90, "stateTaxRate": 0.0025},
            {"code": "SC", "name": "South Carolina", "avgTax": 0.20, "colaIndex": 90, "stateTaxRate": 0.03},
            {"code": "UT", "name": "Utah", "avgTax": 0.20, "colaIndex": 95, "stateTaxRate": 0.0455},
            {"code": "VT", "name": "Vermont", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0.0335},
            {"code": "VA", "name": "Virginia", "avgTax": 0.20, "colaIndex": 100, "stateTaxRate": 0.02},
            {"code": "WV", "name": "West Virginia", "avgTax": 0.20, "colaIndex": 90, "stateTaxRate": 0.0236},
            {"code": "WI", "name": "Wisconsin", "avgTax": 0.20, "colaIndex": 95, "stateTaxRate": 0.035},
            {"code": "DC", "name": "District of Columbia", "avgTax": 0.25, "colaIndex": 110, "stateTaxRate": 0.04},
            {"code": "BAL", "name": "Baltimore, MD", "avgTax": 0.25, "colaIndex": 100, "stateTaxRate": 0.0475, "localTaxRate": 0.0305},
            {"code": "CLE", "name": "Cleveland, OH", "avgTax": 0.22, "colaIndex": 95, "stateTaxRate": 0.02, "localTaxRate": 0.02},
            {"code": "CIN", "name": "Cincinnati, OH", "avgTax": 0.22, "colaIndex": 95, "stateTaxRate": 0.018, "localTaxRate": 0.018},
            {"code": "COLU", "name": "Columbus, OH", "avgTax": 0.22, "colaIndex": 95, "stateTaxRate": 0.025, "localTaxRate": 0.025},
            {"code": "KCM", "name": "Kansas City, MO", "avgTax": 0.22, "colaIndex": 90, "stateTaxRate": 0.01, "localTaxRate": 0.01},
            {"code": "STL", "name": "St. Louis, MO", "avgTax": 0.22, "colaIndex": 90, "stateTaxRate": 0.01, "localTaxRate": 0.01},
        ],
    },
    {
        "code": "UK", "name": "United Kingdom", "currency": "GBP",
        "fiscalYear": "2026-27 (6 Apr 2026 - 5 Apr 2027)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.1, "socialSecurityRateEmployer": 0.15, "socialSecurityCap": 0,
        "taxBrackets": [
            {"min": 12571, "max": 50270, "rate": 0.2},
            {"min": 50271, "max": 125140, "rate": 0.4},
            {"min": 125140, "max": None, "rate": 0.45},
        ],
        "cities": [
            {"code": "LDN", "name": "London", "avgTax": 0.35, "colaIndex": 110},
            {"code": "MAN", "name": "Manchester", "avgTax": 0.32, "colaIndex": 100},
            {"code": "BIR", "name": "Birmingham", "avgTax": 0.32, "colaIndex": 95},
            {"code": "EDI", "name": "Edinburgh", "avgTax": 0.32, "colaIndex": 96},
        ],
    },
    {
        "code": "CA", "name": "Canada", "currency": "CAD",
        "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 16000,
        "socialSecurityRateEmployee": 0.1158, "socialSecurityRateEmployer": 0.1223, "socialSecurityCap": 0,
        "taxBrackets": [
            {"min": 0, "max": 58523, "rate": 0.14}, {"min": 58524, "max": 117045, "rate": 0.205},
            {"min": 117046, "max": 181440, "rate": 0.26}, {"min": 181441, "max": 258482, "rate": 0.29},
            {"min": 258482, "max": None, "rate": 0.33},
        ],
        "cities": [
            {"code": "AB", "name": "Alberta", "avgTax": 0.25, "colaIndex": 100, "stateTaxRate": 0.10},
            {"code": "BC", "name": "British Columbia", "avgTax": 0.25, "colaIndex": 110, "stateTaxRate": 0.0506},
            {"code": "MB", "name": "Manitoba", "avgTax": 0.25, "colaIndex": 95, "stateTaxRate": 0.108},
            {"code": "NB", "name": "New Brunswick", "avgTax": 0.25, "colaIndex": 95, "stateTaxRate": 0.094},
            {"code": "NL", "name": "Newfoundland and Labrador", "avgTax": 0.25, "colaIndex": 95, "stateTaxRate": 0.087},
            {"code": "NT", "name": "Northwest Territories", "avgTax": 0.25, "colaIndex": 105, "stateTaxRate": 0.059},
            {"code": "NS", "name": "Nova Scotia", "avgTax": 0.25, "colaIndex": 95, "stateTaxRate": 0.0879},
            {"code": "NU", "name": "Nunavut", "avgTax": 0.25, "colaIndex": 110, "stateTaxRate": 0.04},
            {"code": "ON", "name": "Ontario", "avgTax": 0.25, "colaIndex": 105, "stateTaxRate": 0.0505},
            {"code": "PE", "name": "Prince Edward Island", "avgTax": 0.25, "colaIndex": 95, "stateTaxRate": 0.095},
            {"code": "QC", "name": "Quebec", "avgTax": 0.30, "colaIndex": 100, "stateTaxRate": 0.14},
            {"code": "SK", "name": "Saskatchewan", "avgTax": 0.25, "colaIndex": 95, "stateTaxRate": 0.105},
            {"code": "YT", "name": "Yukon", "avgTax": 0.25, "colaIndex": 105, "stateTaxRate": 0.064},
            {"code": "TOR", "name": "Toronto, ON", "avgTax": 0.33, "colaIndex": 105, "stateTaxRate": 0.0505},
            {"code": "VAN", "name": "Vancouver, BC", "avgTax": 0.33, "colaIndex": 115, "stateTaxRate": 0.0506},
            {"code": "MTL", "name": "Montreal, QC", "avgTax": 0.35, "colaIndex": 100, "stateTaxRate": 0.14},
        ],
    },
    {
        "code": "SO", "name": "South Korea", "currency": "KRW",
        "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.09, "socialSecurityRateEmployer": 0.105, "socialSecurityCap": 70800000,
        "taxBrackets": [
            {"min": 0, "max": 14000000, "rate": 0.06}, {"min": 14000001, "max": 50000000, "rate": 0.15},
            {"min": 50000001, "max": 88000000, "rate": 0.24}, {"min": 88000001, "max": 150000000, "rate": 0.35},
            {"min": 150000001, "max": 300000000, "rate": 0.38}, {"min": 300000001, "max": 500000000, "rate": 0.40},
            {"min": 500000001, "max": 1000000000, "rate": 0.42}, {"min": 1000000001, "max": None, "rate": 0.45},
        ],
        "cities": [{"code": "SEL", "name": "Seoul", "avgTax": 0.35, "colaIndex": 98}],
    },
    {
        "code": "AU", "name": "Australia", "currency": "AUD",
        "fiscalYear": "2025-26 (1 July 2025 - 30 June 2026)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.02, "socialSecurityRateEmployer": 0.12, "socialSecurityCap": 250000,
        "taxBrackets": [
            {"min": 0, "max": 18200, "rate": 0.0}, {"min": 18201, "max": 45000, "rate": 0.16},
            {"min": 45001, "max": 135000, "rate": 0.3}, {"min": 135001, "max": 190000, "rate": 0.37},
            {"min": 190001, "max": None, "rate": 0.45},
        ],
        "cities": [
            {"code": "SYD", "name": "Sydney", "avgTax": 0.32, "colaIndex": 100},
            {"code": "MEL", "name": "Melbourne", "avgTax": 0.30, "colaIndex": 98},
        ],
    },
    {
        "code": "BO", "name": "Bolivia", "currency": "BOB", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.1271, "socialSecurityRateEmployer": 0.1671, "socialSecurityCap": 0,
        "taxBrackets": [{"min": 0, "max": None, "rate": 0.13}],
        "cities": [{"code": "LPB", "name": "La Paz", "avgTax": 0.13, "colaIndex": 60}],
    },
    {
        "code": "BR", "name": "Brazil", "currency": "BRL", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.14, "socialSecurityRateEmployer": 0.29, "socialSecurityCap": 0,
        "taxBrackets": [
            {"min": 0, "max": 30639, "rate": 0.00}, {"min": 30640, "max": 40499, "rate": 0.075},
            {"min": 40500, "max": 55477, "rate": 0.15}, {"min": 55478, "max": 78227, "rate": 0.225},
            {"min": 78228, "max": None, "rate": 0.275},
        ],
        "cities": [{"code": "SAO", "name": "São Paulo", "avgTax": 0.27, "colaIndex": 85}],
    },
    {
        "code": "BN", "name": "Brunei", "currency": "BND", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.085, "socialSecurityRateEmployer": 0.085, "socialSecurityCap": 2800,
        "taxBrackets": [],
        "cities": [{"code": "BWN", "name": "Bandar Seri Begawan", "avgTax": 0.0, "colaIndex": 90}],
    },
    {
        "code": "CL", "name": "Chile", "currency": "CLP", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.176, "socialSecurityRateEmployer": 0.034, "socialSecurityCap": 0,
        "taxBrackets": [
            {"min": 0, "max": 8670000, "rate": 0.00}, {"min": 8670001, "max": 19280000, "rate": 0.04},
            {"min": 19280001, "max": 32130000, "rate": 0.08}, {"min": 32130001, "max": 44970000, "rate": 0.135},
            {"min": 44970001, "max": 57800000, "rate": 0.23}, {"min": 57800001, "max": 77180000, "rate": 0.304},
            {"min": 77180001, "max": 102480000, "rate": 0.35}, {"min": 102480001, "max": None, "rate": 0.40},
        ],
        "cities": [{"code": "SCL", "name": "Santiago", "avgTax": 0.20, "colaIndex": 80}],
    },
    {
        "code": "CO", "name": "Colombia", "currency": "COP", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.09, "socialSecurityRateEmployer": 0.3002, "socialSecurityCap": 0,
        "taxBrackets": [
            {"min": 0, "max": 54280000, "rate": 0.00}, {"min": 54280001, "max": 84660000, "rate": 0.19},
            {"min": 84660001, "max": 204180000, "rate": 0.28}, {"min": 204180001, "max": 431650000, "rate": 0.33},
            {"min": 431650001, "max": 945000000, "rate": 0.35}, {"min": 945000001, "max": 1545000000, "rate": 0.37},
            {"min": 1545000001, "max": None, "rate": 0.39},
        ],
        "cities": [{"code": "BOG", "name": "Bogotá", "avgTax": 0.25, "colaIndex": 65}],
    },
    {
        "code": "CR", "name": "Costa Rica", "currency": "CRC", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.0983, "socialSecurityRateEmployer": 0.2283, "socialSecurityCap": 0,
        "taxBrackets": [
            {"min": 0, "max": 4195000, "rate": 0.00}, {"min": 4195001, "max": 6244000, "rate": 0.10},
            {"min": 6244001, "max": 10407000, "rate": 0.15}, {"min": 10407001, "max": 20814000, "rate": 0.20},
            {"min": 20814001, "max": None, "rate": 0.25},
        ],
        "cities": [{"code": "SJO", "name": "San José", "avgTax": 0.20, "colaIndex": 75}],
    },
    {
        "code": "EC", "name": "Ecuador", "currency": "USD", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.0945, "socialSecurityRateEmployer": 0.2048, "socialSecurityCap": 0,
        "taxBrackets": [
            {"min": 0, "max": 11722, "rate": 0.00}, {"min": 11723, "max": 14930, "rate": 0.05},
            {"min": 14931, "max": 19718, "rate": 0.10}, {"min": 19719, "max": 26031, "rate": 0.12},
            {"min": 26032, "max": 34255, "rate": 0.15}, {"min": 34256, "max": 45414, "rate": 0.20},
            {"min": 45415, "max": 60450, "rate": 0.25}, {"min": 60451, "max": 80606, "rate": 0.30},
            {"min": 80607, "max": None, "rate": 0.35},
        ],
        "cities": [{"code": "UIO", "name": "Quito", "avgTax": 0.15, "colaIndex": 60}],
    },
    {
        "code": "EE", "name": "Estonia", "currency": "EUR", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 7848,
        "socialSecurityRateEmployee": 0.036, "socialSecurityRateEmployer": 0.338, "socialSecurityCap": 0,
        "taxBrackets": [{"min": 0, "max": 7848, "rate": 0.00}, {"min": 7849, "max": None, "rate": 0.22}],
        "cities": [{"code": "TLL", "name": "Tallinn", "avgTax": 0.22, "colaIndex": 85}],
    },
    {
        "code": "FI", "name": "Finland", "currency": "EUR", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.1017, "socialSecurityRateEmployer": 0.0222, "socialSecurityCap": 0,
        "taxBrackets": [
            {"min": 0, "max": 20200, "rate": 0.00}, {"min": 20201, "max": 30000, "rate": 0.1264},
            {"min": 30001, "max": 52100, "rate": 0.19}, {"min": 52101, "max": 81900, "rate": 0.3025},
            {"min": 81901, "max": 119100, "rate": 0.34}, {"min": 119101, "max": None, "rate": 0.42},
        ],
        "cities": [{"code": "HEL", "name": "Helsinki", "avgTax": 0.45, "colaIndex": 105}],
    },
    {
        "code": "DE", "name": "Germany", "currency": "EUR", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.123, "socialSecurityRateEmployer": 0.123, "socialSecurityCap": 101400,
        "taxBrackets": [
            {"min": 0, "max": 12348, "rate": 0.0}, {"min": 12349, "max": 277825, "rate": 0.14},
            {"min": 277826, "max": None, "rate": 0.45},
        ],
        "cities": [{"code": "BER", "name": "Berlin", "avgTax": 0.40, "colaIndex": 105}],
    },
    {
        "code": "GR", "name": "Greece", "currency": "EUR", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.1387, "socialSecurityRateEmployer": 0.2229, "socialSecurityCap": 7761,
        "taxBrackets": [
            {"min": 0, "max": 10000, "rate": 0.09}, {"min": 10001, "max": 20000, "rate": 0.22},
            {"min": 20001, "max": 30000, "rate": 0.28}, {"min": 30001, "max": 40000, "rate": 0.36},
            {"min": 40001, "max": None, "rate": 0.44},
        ],
        "cities": [{"code": "ATH", "name": "Athens", "avgTax": 0.30, "colaIndex": 80}],
    },
    {
        "code": "GU", "name": "Guam", "currency": "USD", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.0765, "socialSecurityRateEmployer": 0.0765, "socialSecurityCap": 184500,
        "taxBrackets": [],
        "cities": [{"code": "GUM", "name": "Hagåtña", "avgTax": 0.20, "colaIndex": 100}],
    },
    {
        "code": "HK", "name": "Hong Kong", "currency": "HKD",
        "fiscalYear": "2025/26 (1 Apr 2025 - 31 Mar 2026)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.05, "socialSecurityRateEmployer": 0.05, "socialSecurityCap": 30000,
        "taxBrackets": [{"min": 0, "max": None, "rate": 0.15}],
        "cities": [{"code": "HKG", "name": "Hong Kong", "avgTax": 0.15, "colaIndex": 110}],
    },
    {
        "code": "LV", "name": "Latvia", "currency": "EUR", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.105, "socialSecurityRateEmployer": 0.2359, "socialSecurityCap": 105300,
        "taxBrackets": [{"min": 0, "max": 105300, "rate": 0.255}, {"min": 105300, "max": None, "rate": 0.33}],
        "cities": [{"code": "RIX", "name": "Riga", "avgTax": 0.23, "colaIndex": 80}],
    },
    {
        "code": "LT", "name": "Lithuania", "currency": "EUR", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.2081, "socialSecurityRateEmployer": 0.0177, "socialSecurityCap": 0,
        "taxBrackets": [
            {"min": 0, "max": 82962, "rate": 0.2}, {"min": 82963, "max": 138270, "rate": 0.25},
            {"min": 138270, "max": None, "rate": 0.32},
        ],
        "cities": [{"code": "VNO", "name": "Vilnius", "avgTax": 0.20, "colaIndex": 75}],
    },
    {
        "code": "MY", "name": "Malaysia", "currency": "MYR", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 9000,
        "socialSecurityRateEmployee": 0.117, "socialSecurityRateEmployer": 0.1395, "socialSecurityCap": 0,
        "taxBrackets": [
            {"min": 0, "max": 5000, "rate": 0.00}, {"min": 5001, "max": 20000, "rate": 0.01},
            {"min": 20001, "max": 35000, "rate": 0.03}, {"min": 35001, "max": 50000, "rate": 0.06},
            {"min": 50001, "max": 70000, "rate": 0.11}, {"min": 70001, "max": 100000, "rate": 0.19},
            {"min": 100001, "max": 400000, "rate": 0.25}, {"min": 400001, "max": 600000, "rate": 0.26},
            {"min": 600001, "max": 2000000, "rate": 0.28}, {"min": 2000001, "max": None, "rate": 0.30},
        ],
        "cities": [{"code": "KUL", "name": "Kuala Lumpur", "avgTax": 0.20, "colaIndex": 60}],
    },
    {
        "code": "NL", "name": "Netherlands", "currency": "EUR", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.325, "socialSecurityRateEmployer": 0.151, "socialSecurityCap": 79412,
        "taxBrackets": [{"min": 0, "max": 38441, "rate": 0.3582}, {"min": 38442, "max": None, "rate": 0.495}],
        "cities": [{"code": "AMS", "name": "Amsterdam", "avgTax": 0.40, "colaIndex": 105}],
    },
    {
        "code": "PA", "name": "Panama", "currency": "USD", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.11, "socialSecurityRateEmployer": 0.1573, "socialSecurityCap": 0,
        "taxBrackets": [
            {"min": 0, "max": 11000, "rate": 0.0}, {"min": 11001, "max": 50000, "rate": 0.15},
            {"min": 50000, "max": None, "rate": 0.25},
        ],
        "cities": [{"code": "PTY", "name": "Panama City", "avgTax": 0.15, "colaIndex": 85}],
    },
    {
        "code": "PE", "name": "Peru", "currency": "PEN", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.12, "socialSecurityRateEmployer": 0.09, "socialSecurityCap": 0,
        "taxBrackets": [
            {"min": 0, "max": 37450, "rate": 0.00}, {"min": 37451, "max": 165850, "rate": 0.08},
            {"min": 165851, "max": 240750, "rate": 0.14}, {"min": 240751, "max": 963000, "rate": 0.17},
            {"min": 963001, "max": 1926000, "rate": 0.20}, {"min": 1926001, "max": None, "rate": 0.30},
        ],
        "cities": [{"code": "LIM", "name": "Lima", "avgTax": 0.25, "colaIndex": 70}],
    },
    {
        "code": "SG", "name": "Singapore", "currency": "SGD",
        "fiscalYear": "YA2026 (income year 2025)", "standardDeduction": 1000,
        "socialSecurityRateEmployee": 0.2, "socialSecurityRateEmployer": 0.1725, "socialSecurityCap": 8000,
        "taxBrackets": [
            {"min": 0, "max": 20000, "rate": 0.00}, {"min": 20001, "max": 30000, "rate": 0.02},
            {"min": 30001, "max": 40000, "rate": 0.035}, {"min": 40001, "max": 80000, "rate": 0.07},
            {"min": 80001, "max": 120000, "rate": 0.115}, {"min": 120001, "max": 160000, "rate": 0.15},
            {"min": 160001, "max": 200000, "rate": 0.18}, {"min": 200001, "max": 240000, "rate": 0.19},
            {"min": 240001, "max": 280000, "rate": 0.195}, {"min": 280001, "max": 320000, "rate": 0.20},
            {"min": 320001, "max": None, "rate": 0.22},
        ],
        "cities": [{"code": "SIN", "name": "Singapore", "avgTax": 0.15, "colaIndex": 120}],
    },
    {
        "code": "ES", "name": "Spain", "currency": "EUR", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.065, "socialSecurityRateEmployer": 0.3045, "socialSecurityCap": 5101,
        "taxBrackets": [
            {"min": 0, "max": 12450, "rate": 0.19}, {"min": 12451, "max": 20200, "rate": 0.24},
            {"min": 20201, "max": 35200, "rate": 0.30}, {"min": 35201, "max": 60000, "rate": 0.37},
            {"min": 60001, "max": 300000, "rate": 0.45}, {"min": 300001, "max": None, "rate": 0.47},
        ],
        "cities": [{"code": "MAD", "name": "Madrid", "avgTax": 0.35, "colaIndex": 90}],
    },
    {
        "code": "UY", "name": "Uruguay", "currency": "UYU", "fiscalYear": "2026 (Jan-Dec)", "standardDeduction": 0,
        "socialSecurityRateEmployee": 0.1812, "socialSecurityRateEmployer": 0.1263, "socialSecurityCap": 0,
        "taxBrackets": [
            {"min": 0, "max": 577000, "rate": 0.00}, {"min": 577001, "max": 824000, "rate": 0.10},
            {"min": 824001, "max": 1237000, "rate": 0.15}, {"min": 1237001, "max": 4123000, "rate": 0.24},
            {"min": 4123001, "max": 6185000, "rate": 0.25}, {"min": 6185001, "max": 9484000, "rate": 0.27},
            {"min": 9484001, "max": 16493000, "rate": 0.30}, {"min": 16493001, "max": None, "rate": 0.36},
        ],
        "cities": [{"code": "MVD", "name": "Montevideo", "avgTax": 0.25, "colaIndex": 80}],
    },
]

EXCHANGE_RATES = {
    'USD': 1.0, 'EUR': 0.95, 'GBP': 0.79, 'CHF': 0.90, 'SGD': 1.36,
    'CAD': 1.42, 'INR': 86.5, 'AED': 3.67, 'JPY': 150.0, 'AUD': 1.52,
    'CNY': 7.20, 'BRL': 5.00, 'MXN': 17.00, 'RUB': 92.0, 'IDR': 15500,
    'ARS': 850.0, 'TRY': 31.0, 'SAR': 3.75, 'ZAR': 19.0, 'KRW': 1330,
    'DKK': 7.0, 'SEK': 10.5, 'HKD': 7.8, 'MYR': 4.75, 'PEN': 3.75,
    'UYU': 39.0, 'CLP': 980.0, 'COP': 3900.0, 'CRC': 510.0, 'BND': 1.36, 'BOB': 6.9,
}

TIER_BENEFITS = {
    "Long term assignment": {
        "housingLimit": 8000, "educationLimit": 25000, "mobilityPremium": 0,
        "transpLimit": 6000, "homeLeaveLimit": 3000, "relocationLimit": 15000,
        "immigrationLimit": 3500, "taxPrepLimit": 2500,
    },
    "Short term assignment": {
        "housingLimit": 4000, "educationLimit": 15000, "mobilityPremium": 0,
        "transpLimit": 4000, "homeLeaveLimit": 2000, "relocationLimit": 8000,
        "immigrationLimit": 2000, "taxPrepLimit": 1500,
    },
    "Rotator": {
        "housingLimit": 2500, "educationLimit": 0, "mobilityPremium": 0,
        "transpLimit": 2000, "homeLeaveLimit": 1500, "relocationLimit": 5000,
        "immigrationLimit": 2000, "taxPrepLimit": 1000,
    },
    "Local Plus": {
        "housingLimit": 1500, "educationLimit": 0, "mobilityPremium": 0,
        "transpLimit": 1000, "homeLeaveLimit": 0, "relocationLimit": 5000,
        "immigrationLimit": 2000, "taxPrepLimit": 500,
    },
    "Local": {
        "housingLimit": 0, "educationLimit": 0, "mobilityPremium": 0,
        "transpLimit": 0, "homeLeaveLimit": 0, "relocationLimit": 5000,
        "immigrationLimit": 2000, "taxPrepLimit": 500,
    },
}

COUNTRY_INSIGHTS = {
    'NL': """### Netherlands — 30% Ruling
The Dutch regime remains Europe's most well-known expatriate scheme but faces continued erosion. The **30% tax-free benefit drops to 27% from January 1, 2027** under Tax Plan 2025, passed December 17, 2024.

**Current parameters (2026):**
- **Benefit:** 30% of gross salary paid tax-free
- **Duration:** 5 years maximum
- **Salary thresholds:** €48,013 standard; €36,497 for under-30s with Master's degree
- **Salary cap:** €262,000 (income above fully taxed)
- **Prior residence:** Must have lived >150km from Dutch border for 16 of 24 months before start
- **Top marginal rate:** 49.50%""",

    'BE': """### Belgium — Special Tax Regime for Inpatriates (ISRT)
Belgium significantly enhanced its regime via **law published December 30, 2025** (retroactive to January 1, 2025).

**Current parameters:**
- **Benefit:** 35% tax-free allowance (increased from 30%)
- **Cap:** Abolished—the 35% now applies without limit
- **Duration:** 5 years
- **Minimum salary:** €70,000 (reduced from €75,000)
- **Prior residence:** Not resident within 150km of Belgian border for past 60 months
- **Top marginal rate:** 50% plus 0-9% municipal surcharge""",

    'LU': """### Luxembourg — Impatriate Regime
Luxembourg completely overhauled its regime effective **January 1, 2025**, replacing the complex system with a straightforward 50% exemption.

**Current parameters:**
- **Benefit:** 50% exemption on gross annual remuneration up to €400,000
- **Duration:** 8 years
- **Minimum salary:** €75,000 gross annual base
- **Prior residence:** Not resident within 150km of Luxembourg border for past 5 years
- **Top marginal rate:** 45.78%""",

    'FR': """### France — Impatriate Regime (Article 155 B CGI)
The French regime offers flexible exemption options and remains stable.

**Current parameters:**
- **Benefit options:** Either 30% flat-rate exemption OR actual contractual impatriation bonus
- **Additional exemption:** Salary for foreign workdays (capped at 20% of taxable compensation)
- **Combined cap:** Total exemptions cannot exceed 50% of compensation
- **Duration:** 8 years
- **Prior residence:** Not French tax resident for 5 calendar years before arrival
- **Top marginal rate:** ~49%""",

    'UK': """### United Kingdom — FIG Regime (Foreign Income and Gains)
The **non-dom regime ended April 6, 2025**, replaced by the FIG regime.

**Current parameters:**
- **Benefit:** 100% relief on all foreign income and gains
- **Duration:** 4 consecutive tax years only
- **Prior residence:** Must not have been UK tax resident in any of the **10 consecutive years** before arrival
- **Overseas Workday Relief cap:** Lower of £300,000 or 30% of employment income
- **Top marginal rate:** 45% (60% effective rate between £100,000-£125,140)""",

    'IE': """### Ireland — SARP (Special Assignee Relief Programme)
**SARP has been extended for 5 years to December 31, 2030** under Finance Bill 2025.

**Current parameters:**
- **Benefit:** 30% income tax exemption on qualifying income between €125,000 and €1,000,000
- **Duration:** 5 consecutive tax years
- **Minimum salary:** €125,000 (increased from €100,000 effective January 1, 2026)
- **Prior residence:** Not Irish tax resident for 5 tax years before arrival
- **Top marginal rate:** ~52%""",

    'IT': """### Italy — Regime Impatriati
Italy's regime was substantially reformed for 2024 onwards.

**Current parameters:**
- **Benefit:** 50% income tax exemption (60% if worker has/adopts minor children)
- **Income cap:** €600,000 per year
- **Duration:** 5 years fixed (no extensions)
- **Prior non-residence:** 3 years (6-7 years if transferred from same employer/group)
- **Top marginal rate:** ~45-47%""",

    'ES': """### Spain — Beckham Law
Spain's regime remains stable with no major changes in 2025-2026.

**Current parameters:**
- **Benefit:** 24% flat tax rate on Spanish-sourced income up to €600,000; 47% on excess
- **Foreign income:** Excluded from Spanish taxation
- **Duration:** 6 consecutive tax years
- **Prior residence:** Not Spanish tax resident in previous 5 years
- **Top marginal rate (standard):** ~47-50%""",

    'PT': """### Portugal — NHR 2.0 / IFICI
The **original NHR regime ended for new applicants on March 31, 2025**. Replaced by IFICI.

**Current parameters:**
- **Benefit:** 20% flat tax rate on qualifying Portuguese-sourced employment income; foreign-source income exempt
- **Duration:** 10 years
- **Prior residence:** Not Portuguese tax resident in previous 5 years
- **Eligible activities:** Higher education, R&D, certified startups, technology/innovation centers
- **Top marginal rate (standard):** ~48-53%""",

    'GR': """### Greece — 50% Tax Exemption for Inbound Workers
Greece's regime continues unchanged, offering a straightforward 50% exemption for 7 years.

**Current parameters:**
- **Benefit:** 50% income tax exemption on Greek employment and business activity income
- **Duration:** 7 consecutive tax years
- **Prior residence:** Not Greek tax resident for 5 out of 6 years preceding transfer
- **Top marginal rate:** ~44%""",

    'DK': """### Denmark — Researcher Tax Scheme (Forskerordningen)
Denmark has made a **major 2026 policy shift**, reducing the salary threshold by 16%.

**Current parameters:**
- **Benefit:** 27% flat tax + 8% labor market contribution = **32.84% effective rate**
- **Duration:** 7 years maximum
- **Monthly salary threshold (2026):** DKK 65,400 (~€8,764)
- **Top marginal rate:** ~60.5%""",

    'SE': """### Sweden — Expert Tax Relief (Expertskatten)
Sweden extended the benefit period to 7 years in 2024.

**Current parameters:**
- **Benefit:** 25% of salary/benefits exempt from income tax and social security
- **Duration:** 7 years
- **Monthly salary threshold (2025):** SEK 88,200 (~€8,352)
- **Top marginal rate:** ~52%""",

    'AE': """### UAE — Zero Income Tax
The UAE maintains **zero personal income tax** as of February 2026.

**Current parameters:**
- **Benefit:** 0% personal income tax; no individual tax registration or reporting obligations
- **Duration:** Permanent
- **Corporate tax (since June 2023):** 9% on taxable income above AED 375,000
- **Tax residency:** 183 days presence in rolling 12-month period""",

    'SG': """### Singapore — Not Ordinarily Resident (NOR) Scheme — DISCONTINUED
**The NOR Scheme has ceased.** The last NOR status granted was valid from YA 2020 to YA 2024.

**Current standard rates:**
- Top marginal rate: **24%** (on income above S$1,000,000)
- 2025 tax rebate: 60% of tax payable, capped at S$200""",

    'HK': """### Hong Kong — Territorial Tax System
Hong Kong's territorial system continues to provide significant benefits for expatriates.

**Current parameters:**
- **Principle:** Only Hong Kong-sourced income taxed
- **Progressive rates:** 2% to 17%
- **Standard rate:** 15% on first HKD 5,000,000; 16% on remainder
- **No taxes on:** Capital gains, inheritance, payroll, or sales/VAT""",

    'DE': """### Germany — No Special Expat Regime
Germany does not offer a preferential tax regime for inbound assignees. All residents are taxed on worldwide income at standard progressive rates.

**Current parameters (2026):**
- **Top marginal rate:** 45% on income above €277,826 (plus 5.5% solidarity surcharge, reduced for most since 2021)
- **Solidarity surcharge:** Only applies when income tax exceeds €18,130; tapers out for most earners
- **Church tax:** 8–9% of income tax if registered (optional via deregistration)
- **Standard allowance:** €12,096 basic personal allowance (tax-free)
- **Joint filing:** Available for married couples via Ehegattensplitting (splitting method)
- **Social insurance (employee):** ~20% of gross salary (pension ~9.3%, health ~7.3%, unemployment ~1.3%, care ~1.7%)
- **Social insurance cap:** Annual ceiling applies per branch (e.g., pension cap €96,600 West / €93,600 East in 2025)

**Key assignee considerations:**
- **Seconded workers:** If A1 Certificate of Coverage applies, home-country social security continues; host social security waived
- **Tax treaty network:** Germany has over 90 double tax treaties; check relevant treaty to determine taxing rights
- **183-day rule:** Standard treaty threshold for employment income taxation
- **No lump-sum or flat-rate option:** Tax liability calculated on actual gross income only""",

    'CH': """### Switzerland — Lump Sum / Forfait Fiscal
Switzerland offers two regimes: standard cantonal/federal taxation and the expenditure-based lump-sum regime.

**Lump-Sum Taxation (Forfait Fiscal):**
- **Eligibility:** Foreign nationals taking up Swiss residence for the first time (or after 10-year absence) who do not engage in Swiss gainful activity
- **Tax base:** Based on annual living expenses (minimum 7× annual rent or CHF 421,200 federal floor; cantons may set higher floors)
- **Duration:** Indefinite (subject to review if circumstances change)
- **Cantons:** Zug, Schwyz, Valais, Ticino most favorable; Zurich abolished it in 2010

**Standard Rates:**
- **Federal top rate:** 11.5% on income above CHF 912,600
- **Cantonal rates:** Vary widely — Zug ~22% combined; Geneva ~42%; Zurich ~40%
- **Wealth tax:** Cantonal only; typically 0.1–1% annually on net assets""",

    'CA': """### Canada — No Special Expat Regime
Canada taxes residents on worldwide income at standard federal + provincial rates with no inpatriate exemption.

**Current parameters (2026):**
- **Federal top rate:** 33% on income above CAD 253,414
- **Combined top rates:** Ontario ~53.5%; Quebec ~53.3%; Alberta ~48%; BC ~53.5%
- **Basic personal amount:** CAD 16,129 (federal)
- **Social insurance (CPP/EI):** ~6% employee combined (CPP ~5.95% up to CAD 73,200; EI ~1.66% up to CAD 63,200)

**Key assignee considerations:**
- **Tax treaty network:** Extensive — 93+ tax treaties; US–Canada treaty particularly comprehensive
- **Departure tax:** On deemed disposition of most capital property when ceasing Canadian residency
- **Provincial variation:** Significant rate differences make province of posting material""",

    'AU': """### Australia — No Expat Tax Regime (Temporary Resident Concession)
Australia provides a limited concession for temporary residents.

**Current parameters (2026):**
- **Temporary resident:** Only Australian-sourced income taxed; most foreign income/gains exempt
- **Eligibility:** Holds a temporary visa and is not a citizen/permanent resident
- **Top marginal rate:** 45% on income above AUD 190,000 (plus 2% Medicare levy)
- **Low Income Tax Offset:** Up to AUD 700
- **Superannuation (employer):** 12% compulsory employer contribution (from 1 July 2025)""",

    'JP': """### Japan — No Special Expat Regime (Non-Permanent Resident Status)
Japan offers a partial exemption during the first 5 years via non-permanent resident status.

**Non-Permanent Resident (NPR):**
- **Eligibility:** Has domicile/residence in Japan but has not had it for 5+ years in the past 10 years
- **Benefit:** Foreign-source income taxed only if remitted to Japan
- **Duration:** Up to 5 years; becomes permanent resident thereafter (worldwide taxation)

**Standard Rates (2026):**
- **National top rate:** 45% on income above JPY 40,000,000
- **Inhabitant tax:** Flat 10% (prefectural + municipal)
- **Combined top rate:** ~55%
- **Reconstruction surtax:** 2.1% of national income tax (through 2037)""",

    'FI': """### Finland — No Special Expat Regime
Finland has no inpatriate tax exemption. All tax residents are taxed on worldwide income at progressive national + municipal rates.

**Current parameters (2026):**
- **National top rate:** 44% on income above €85,800
- **Municipal tax:** Flat rate set by each municipality, typically 19–22% (Helsinki ~19.5%)
- **Combined top rate:** ~60–65% including national, municipal, and social contributions
- **Church tax:** 1–2% if registered (avoidable)
- **Key social contributions (employee):** Pension ~7.15%, unemployment ~1.50%, health ~1.96%

**Key assignee considerations:**
- **Progressive solidarity:** Finland has one of Europe's highest combined marginal rates for high earners
- **Tax treaty network:** Finland has 70+ treaties; assignees from US, UK, Germany benefit from standard 183-day rules
- **A1/CoC:** Finnish social security waived if home-country A1 applies""",

    'NO': """### Norway — No Special Expat Regime
Norway taxes all residents on worldwide income at standard progressive rates. No general inpatriate exemption exists.

**Current parameters (2026):**
- **National bracket tax:** Tiered from 1.7% to 17.5% on income above NOK 208,050
- **Flat base rate:** 22% on general income (capital/business)
- **Combined top rate:** ~47.4% on employment income above NOK 1,000,000+
- **Social insurance (employee):** 7.8% on employment income
- **Wealth tax:** 1% on net wealth above NOK 1,700,000 (municipality) + 0.3% national above NOK 20M

**Key assignee considerations:**
- **Svalbard regime:** Flat 8% income tax if based on Svalbard archipelago
- **183-day rule:** Standard treaty threshold; Norway has ~90 double tax treaties
- **A1/CoC:** Norwegian social insurance waived if EEA A1 or bilateral agreement applies""",

    'AT': """### Austria — No Special Expat Regime
Austria taxes residents on worldwide income without a dedicated inpatriate scheme.

**Current parameters (2026):**
- **Top marginal rate:** 55% on income above €1,000,000; 50% on income above €90,000
- **Standard brackets:** 0% up to €12,816; 20–50% on €12,816–€1,000,000
- **Social insurance (employee):** ~18.2% of gross salary (pension, health, unemployment, accident combined)
- **13th/14th month payments:** Taxed at reduced 6% flat rate (significant benefit for many assignees)

**Key assignee considerations:**
- **Austria–EU totalization:** A1 Certificate waives Austrian social security for EEA-based assignees
- **Double tax treaty network:** 90+ treaties including US, UK, Canada, Australia
- **No lump-sum regime:** Tax liability based on actual gross income""",

    'US': """### United States — No Inpatriate Regime (Worldwide Taxation)
The US taxes citizens and residents on worldwide income. There is no special inbound assignee regime, but non-resident aliens follow a separate set of rules.

**Current parameters (2026):**
- **Federal top rate:** 37% on income above $626,350 (single) / $751,600 (married filing jointly)
- **Standard deduction:** $16,100 (single) / $32,200 (MFJ)
- **Child tax credit:** $2,000 per qualifying child under 17
- **FICA (employee):** Social Security 6.2% up to $184,500; Medicare 1.45% uncapped (+ 0.9% above $200k single)
- **State tax:** 0% (AK, FL, NV, NH, SD, TN, TX, WY, WA) to ~13.3% (CA top)

**Key assignee (inbound) considerations:**
- **Substantial Presence Test:** 183-day rule (weighted over 3 years) triggers US resident status
- **Tax treaty:** May reduce or eliminate US source-income taxation for treaty-country nationals
- **Social Security Totalization:** US has 30+ agreements; home-country A1 equivalent may apply
- **ITIN vs SSN:** Non-residents without SSN need Individual Taxpayer Identification Number""",

    'IN': """### India — No Special Expat Regime
India taxes residents on worldwide income at standard progressive rates. Non-residents pay tax only on India-sourced income.

**Current parameters (2026, new tax regime default):**
- **Top marginal rate:** 30% + 4% health & education cess on income above INR 1,500,000
- **Surcharge:** 10–25% of income tax for high earners (up to 37% repealed; now max 25%)
- **Standard deduction (salaried):** INR 75,000 under new regime
- **Effective top rate:** ~39% including surcharge and cess

**Key assignee (inbound) considerations:**
- **Residency rule:** Resident if present 182+ days in India in the tax year (or 60+ days + 365 in prior 4 years)
- **RNOR status:** Returning after long absence — taxed only on India-sourced + remitted income for up to 2 years
- **Social security (PF):** 12% employer + 12% employee; international workers from treaty countries may be exempt""",

    'ZA': """### South Africa — No Special Expat Regime (Amended Foreign Employment Exemption)
South Africa amended its foreign employment exemption effective March 1, 2020.

**Current parameters (2026):**
- **Top marginal rate:** 45% on income above ZAR 1,817,001
- **Foreign employment exemption:** First ZAR 1,257,438 of foreign employment income exempt if:
  - Employee is a South African tax resident
  - Worked in a foreign country for more than 183 days in any 12-month period (and 60+ continuous days)
- **Social contributions (UIF):** 1% employee + 1% employer on income up to ZAR 17,712/month

**Key assignee (outbound) considerations:**
- **Financial emigration:** Formal cease of SA tax residency triggers exit charge (deemed disposal of assets)
- **Expat tax planning:** The ZAR 1.25M exemption cap means high earners still face SA tax on excess""",
}

# ---------------------------------------------------------------------------
# TOTALIZATION AGREEMENTS
# ---------------------------------------------------------------------------

_EU_EEA_SS = {
    'AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GR', 'HR',
    'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI',
    'SK', 'NO', 'UK',
}

_BILATERAL_SS_PAIRS = {
    # United States
    ('US', 'AT'), ('US', 'AU'), ('US', 'BE'), ('US', 'CA'), ('US', 'CH'), ('US', 'CL'),
    ('US', 'CZ'), ('US', 'DE'), ('US', 'DK'), ('US', 'ES'), ('US', 'FI'), ('US', 'FR'),
    ('US', 'GR'), ('US', 'HU'), ('US', 'IE'), ('US', 'IT'), ('US', 'JP'), ('US', 'KR'),
    ('US', 'LU'), ('US', 'NL'), ('US', 'NO'), ('US', 'PL'), ('US', 'PT'), ('US', 'SE'),
    ('US', 'SI'), ('US', 'SK'), ('US', 'UK'), ('US', 'UY'),
    # Canada
    ('CA', 'AT'), ('CA', 'AU'), ('CA', 'BE'), ('CA', 'CH'), ('CA', 'CL'), ('CA', 'CZ'),
    ('CA', 'DE'), ('CA', 'DK'), ('CA', 'ES'), ('CA', 'FI'), ('CA', 'FR'), ('CA', 'GR'),
    ('CA', 'HU'), ('CA', 'IE'), ('CA', 'IT'), ('CA', 'JP'), ('CA', 'KR'), ('CA', 'LU'),
    ('CA', 'NL'), ('CA', 'NO'), ('CA', 'PL'), ('CA', 'PT'), ('CA', 'SE'), ('CA', 'SI'),
    ('CA', 'SK'), ('CA', 'UY'),
    # Australia
    ('AU', 'AT'), ('AU', 'BE'), ('AU', 'CH'), ('AU', 'CL'), ('AU', 'CZ'), ('AU', 'DE'),
    ('AU', 'FI'), ('AU', 'GR'), ('AU', 'HU'), ('AU', 'IE'), ('AU', 'IT'), ('AU', 'JP'),
    ('AU', 'KR'), ('AU', 'NL'), ('AU', 'NO'), ('AU', 'PT'), ('AU', 'SE'), ('AU', 'SI'),
    ('AU', 'SK'),
    # Japan
    ('JP', 'BE'), ('JP', 'BR'), ('JP', 'CH'), ('JP', 'CZ'), ('JP', 'DE'), ('JP', 'ES'),
    ('JP', 'FI'), ('JP', 'FR'), ('JP', 'HU'), ('JP', 'IE'), ('JP', 'IT'), ('JP', 'KR'),
    ('JP', 'LU'), ('JP', 'NL'), ('JP', 'NO'), ('JP', 'PL'), ('JP', 'PT'), ('JP', 'SE'),
    ('JP', 'SI'), ('JP', 'SK'),
    # South Korea
    ('KR', 'AT'), ('KR', 'BE'), ('KR', 'CH'), ('KR', 'CZ'), ('KR', 'DE'), ('KR', 'DK'),
    ('KR', 'ES'), ('KR', 'FI'), ('KR', 'FR'), ('KR', 'HU'), ('KR', 'IE'), ('KR', 'IT'),
    ('KR', 'LU'), ('KR', 'NL'), ('KR', 'NO'), ('KR', 'PL'), ('KR', 'PT'), ('KR', 'SE'),
    ('KR', 'SI'), ('KR', 'SK'), ('KR', 'UY'),
    # Switzerland
    ('CH', 'AU'), ('CH', 'CA'), ('CH', 'CL'), ('CH', 'JP'), ('CH', 'KR'), ('CH', 'US'),
}

# Build bidirectional lookup set
_BILATERAL_SET = set()
for a, b in _BILATERAL_SS_PAIRS:
    _BILATERAL_SET.add((a, b))
    _BILATERAL_SET.add((b, a))


def has_totalization_agreement(home_code: str, host_code: str) -> bool:
    """Returns True when a valid totalization/SS agreement exists between two countries."""
    if not home_code or not host_code or home_code == host_code:
        return False
    if home_code in _EU_EEA_SS and host_code in _EU_EEA_SS:
        return True
    if home_code == 'CH' and host_code in _EU_EEA_SS:
        return True
    if host_code == 'CH' and home_code in _EU_EEA_SS:
        return True
    return (home_code, host_code) in _BILATERAL_SET
