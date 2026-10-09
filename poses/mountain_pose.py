
def check_mountain_pose(angles):

    left_knee = angles["left_knee"]
    right_knee = angles["right_knee"]

    left_elbow = angles["left_elbow"]
    right_elbow = angles["right_elbow"]

    # Both legs should be mostly straight
    legs_straight = (
        left_knee >= 160
        and right_knee >= 160
    )

    # Both arms should be mostly straight
    arms_straight = (
        left_elbow >= 150
        and right_elbow >= 150
    )

    correct = legs_straight and arms_straight

    return correct
