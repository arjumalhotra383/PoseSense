def check_warrior_one(angles):
    left_bent = 70 <= angles["left_knee"] <= 120
    right_bent = 70 <= angles["right_knee"] <= 120

    left_straight = angles["left_knee"] >= 150
    right_straight = angles["right_knee"] >= 150

    arms_straight = (
        angles["left_elbow"] >= 150
        and angles["right_elbow"] >= 150
    )

    arms_raised = (
        angles["left_shoulder"] >= 120
        and angles["right_shoulder"] >= 120
    )

    legs_valid = (
        (left_bent and right_straight)
        or (right_bent and left_straight)
    )

    return legs_valid and arms_straight and arms_raised