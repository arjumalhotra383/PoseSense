import math


def calculate_angle(a, b, c):
    """
    Calculates the angle at point b.

    a = first point
    b = joint
    c = third point
    """

    angle = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0])
        - math.atan2(a[1] - b[1], a[0] - b[0])
    )

    angle = abs(angle)

    if angle > 180:
        angle = 360 - angle

    return angle


def get_point(landmark):
    return (landmark.x, landmark.y)