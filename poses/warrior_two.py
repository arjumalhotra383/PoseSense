def check_warrior_two(angles):

    left_knee = angles["left_knee"]
    right_knee = angles["right_knee"]

    left_elbow = angles["left_elbow"]
    right_elbow = angles["right_elbow"]

    # Check which knee is bent
    left_bent = 70 <= left_knee <= 120
    right_bent = 70 <= right_knee <= 120

    # Check which knee is straight
    left_straight = left_knee >= 150
    right_straight = right_knee >= 150

    # Arms should be straight
    arms_straight = (
        left_elbow >= 150
        and right_elbow >= 150
    )

    # Correct Warrior II
    correct = (
        (
            left_bent and right_straight
        )
        or
        (
            right_bent and left_straight
        )
    ) and arms_straight

    return correct