def check_plank_pose(angles):
    knees_straight = (
        angles["left_knee"] >= 150
        and angles["right_knee"] >= 150
    )

    elbows_straight = (
        angles["left_elbow"] >= 150
        and angles["right_elbow"] >= 150
    )

    body_aligned = (
        angles["left_hip"] >= 150
        and angles["right_hip"] >= 150
    )

    return knees_straight and elbows_straight and body_aligned