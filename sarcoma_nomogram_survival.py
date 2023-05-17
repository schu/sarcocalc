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

TUMOR_MAX_SIZE_CM_POINTS = {
    1: 7,
    5: 33,
    10: 54,
    15: 65,
    20: 73,
    25: 82,
    30: 91,
    35: 100,
}

GRADING_POINTS = {
    1: 0,
    2: 30,
    3: 44,
}

HISTOLOGY_POINTS = {
    'leio': 28,
    'dd/pleom lipo': 12,
    'myxoid lipo': 0,
    'mpnst': 19,
    'myxofibro': 15,
    'other': 21,
    'synovial': 30,
    'ups': 7,
    'vascular': 53,
}

POINTS_5Y_OS = {
    180: 0.10,
    169: 0.20,
    160: 0.30,
    152: 0.40,
    144: 0.50,
    124: 0.70,
    110: 0.80,
    87: 0.90,
    65: 0.95,
    50: 0.97,
    37: 0.98,
}

def calc_5yos(age, size, grading, histo):
    points = 0

    age = max(int(age), 18)
    age_points = list({ k: v for k, v in AGE_POINTS.items() if k <= age }.values())[-1]

    size = max(int(size), 1)
    size_points = list({ k: v for k, v in TUMOR_MAX_SIZE_CM_POINTS.items() if k <= size }.values())[-1]

    grading_points = list({ k: v for k, v in GRADING_POINTS.items() if k <= int(grading) }.values())[-1]

    histo_points = HISTOLOGY_POINTS.get(histo.lower())

    points = age_points + size_points + grading_points + histo_points

    points = min(max(points, 37), 180)

    five_year_os = list({ k: v for k, v in POINTS_5Y_OS.items() if k >= points }.values())[-1]

    return str(five_year_os)
