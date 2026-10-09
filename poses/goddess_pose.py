def check_goddess_pose(angles):
    knees_bent = (
        70 <= angles["left_knee"] <= 130
        and 70 <= angles["right_knee"] <= 130
    )

    arms_straight = (
        angles["left_elbow"] >= 150
        and angles["right_elbow"] >= 150
    )

    arms_open = (
        60 <= angles["left_shoulder"] <= 130
        and 60 <= angles["right_shoulder"] <= 130
    )

    return knees_bent and arms_straight and arms_open