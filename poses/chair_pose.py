def check_chair_pose(angles):
    knees_bent = (
        70 <= angles["left_knee"] <= 130
        and 70 <= angles["right_knee"] <= 130
    )

    arms_straight = (
        angles["left_elbow"] >= 150
        and angles["right_elbow"] >= 150
    )

    arms_raised = (
        angles["left_shoulder"] >= 120
        and angles["right_shoulder"] >= 120
    )

    return knees_bent and arms_straight and arms_raised