from numpy import interp

AGE_POINTS = {
    18: 0,
    25: 1,
    30: 2,
    35: 3,
    40: 5,
    45: 6,
    50: 8,
    55: 11,
    60: 14,
    65: 18,
    70: 22,
    75: 26,
    80: 30,
    85: 35,
    90: 39,
    100: 48,
}

TUMOR_MAX_SIZE_CM_SURVIVAL_POINTS = {
    1: 7,
    5: 33,
    10: 54,
    15: 65,
    20: 73,
    25: 82,
    30: 91,
    35: 100,
}

TUMOR_MAX_SIZE_CM_METASTASIS_POINTS = {
    1: 9,
    5: 43,
    10: 68,
    15: 76,
    20: 82,
    25: 88,
    30: 94,
    35: 100,
}

GRADING_SURVIVAL_POINTS = {
    1: 0,
    2: 30,
    3: 44,
}

GRADING_METASTASIS_POINTS = {
    1: 0,
    2: 39,
    3: 53,
}

HISTOLOGY_SURVIVAL_POINTS = {
    "leio": 28,
    "dd/pleom lipo": 12,
    "myxoid lipo": 0,
    "mpnst": 19,
    "myxofibro": 15,
    "other": 21,
    "synovial": 30,
    "ups": 7,
    "vascular": 53,
}

HISTOLOGY_METASTASIS_POINTS = {
    "leio": 36,
    "dd/pleom lipo": 7,
    "myxoid lipo": 6,
    "mpnst": 17,
    "myxofibro": 0,
    "other": 22,
    "synovial": 27,
    "ups": 14,
    "vascular": 36,
}

POINTS_5Y_OS = {
    37: 0.98,
    50: 0.97,
    65: 0.95,
    87: 0.90,
    110: 0.80,
    124: 0.70,
    144: 0.50,
    152: 0.40,
    160: 0.30,
    169: 0.20,
    180: 0.10,
}

POINTS_5Y_METASTASIS = {
    15: 0.01,
    88: 0.10,
    111: 0.20,
    126: 0.30,
    137: 0.40,
    146: 0.50,
    163: 0.70,
    172: 0.80,
    183: 0.90,
}

POINTS_10Y_OS = {
    25: 0.98,
    37: 0.97,
    53: 0.95,
    74: 0.90,
    97: 0.80,
    111: 0.70,
    131: 0.50,
    139: 0.40,
    148: 0.30,
    156: 0.20,
    167: 0.10,
    188: 0.01,
}

POINTS_10Y_METASTASIS = {
    11: 0.01,
    84: 0.10,
    107: 0.20,
    121: 0.30,
    133: 0.40,
    142: 0.50,
    159: 0.70,
    168: 0.80,
    179: 0.90,
    187: 0.95,
}


def calc(age, size, grading, histo):
    input_complete = True
    points = 0

    age_survival_points = 0
    if age:
        age = max(int(age), 18)
        age_survival_points = list(
            {k: v for k, v in AGE_POINTS.items() if k <= age}.values()
        )[-1]
    else:
        input_complete = False

    size_survival_points = 0
    size_metastasis_points = 0
    if size:
        size = max(int(size), 1)
        size_survival_points = list(
            {
                k: v for k, v in TUMOR_MAX_SIZE_CM_SURVIVAL_POINTS.items() if k <= size
            }.values()
        )[-1]
        size_metastasis_points = list(
            {
                k: v
                for k, v in TUMOR_MAX_SIZE_CM_METASTASIS_POINTS.items()
                if k <= size
            }.values()
        )[-1]
    else:
        input_complete = False

    grading_survival_points = 0
    grading_metastasis_points = 0
    if grading:
        grading_survival_points = list(
            {
                k: v for k, v in GRADING_SURVIVAL_POINTS.items() if k <= int(grading)
            }.values()
        )[-1]
        grading_metastasis_points = list(
            {
                k: v for k, v in GRADING_METASTASIS_POINTS.items() if k <= int(grading)
            }.values()
        )[-1]
    else:
        input_complete = False

    if histo.lower() in HISTOLOGY_SURVIVAL_POINTS.keys():
        histo_survival_points = HISTOLOGY_SURVIVAL_POINTS.get(histo.lower())
        histo_metastasis_points = HISTOLOGY_METASTASIS_POINTS.get(histo.lower())
    else:
        histo_survival_points = HISTOLOGY_SURVIVAL_POINTS["other"]
        histo_metastasis_points = HISTOLOGY_METASTASIS_POINTS["other"]

    points_survival = (
        age_survival_points
        + size_survival_points
        + grading_survival_points
        + histo_survival_points
    )
    points_metastasis = (
        size_metastasis_points + grading_metastasis_points + histo_metastasis_points
    )

    points_survival = min(max(points_survival, 25), 188)
    points_metastasis = min(max(points_metastasis, 11), 187)

    five_year_os = round(
        interp(points_survival, list(POINTS_5Y_OS.keys()), list(POINTS_5Y_OS.values())),
        2,
    )
    ten_year_os = round(
        interp(
            points_survival, list(POINTS_10Y_OS.keys()), list(POINTS_10Y_OS.values())
        ),
        2,
    )

    five_year_metastasis = round(
        interp(
            points_metastasis,
            list(POINTS_5Y_METASTASIS.keys()),
            list(POINTS_5Y_METASTASIS.values()),
        ),
        2,
    )
    ten_year_metastasis = round(
        interp(
            points_metastasis,
            list(POINTS_10Y_METASTASIS.keys()),
            list(POINTS_10Y_METASTASIS.values()),
        ),
        2,
    )

    return (
        str(five_year_os),
        str(ten_year_os),
        str(five_year_metastasis),
        str(ten_year_metastasis),
        str(points_survival),
        str(points_metastasis),
        str(input_complete),
    )
