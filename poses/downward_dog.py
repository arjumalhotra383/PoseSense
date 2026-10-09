def check_downward_dog(angles):
    knees_straight = (
        angles["left_knee"] >= 140
        and angles["right_knee"] >= 140
    )

    elbows_straight = (
        angles["left_elbow"] >= 150
        and angles["right_elbow"] >= 150
    )

    hips_bent = (
        50 <= angles["left_hip"] <= 130
        and 50 <= angles["right_hip"] <= 130
    )

    return knees_straight and elbows_straight and hips_bent