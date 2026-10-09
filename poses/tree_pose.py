def check_tree_pose(angles):

    left_knee = angles["left_knee"]
    right_knee = angles["right_knee"]

    # One leg should be bent
    left_bent = 30 <= left_knee <= 100
    right_bent = 30 <= right_knee <= 100

    # The supporting leg should be mostly straight
    left_straight = left_knee >= 150
    right_straight = right_knee >= 150

    # Tree Pose is considered correct
    # when one knee is bent and the other is straight

    correct = (
        (left_bent and right_straight)
        or
        (right_bent and left_straight)
    )

    return correct