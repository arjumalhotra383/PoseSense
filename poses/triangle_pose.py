def check_triangle_pose(angles):
    legs_straight = (
        angles["left_knee"] >= 150
        and angles["right_knee"] >= 150
    )

    arms_straight = (
        angles["left_elbow"] >= 150
        and angles["right_elbow"] >= 150
    )

    torso_tilted = (
        angles["left_hip"] < 150
        or angles["right_hip"] < 150
    )

    return legs_straight and arms_straight and torso_tilted