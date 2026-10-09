
import mediapipe as mp

from angle_utils import calculate_angle, get_point

from poses.warrior_two import check_warrior_two
from poses.tree_pose import check_tree_pose
from poses.mountain_pose import check_mountain_pose
from poses.chair_pose import check_chair_pose
from poses.warrior_one import check_warrior_one
from poses.goddess_pose import check_goddess_pose
from poses.triangle_pose import check_triangle_pose
from poses.high_lunge import check_high_lunge
from poses.plank_pose import check_plank_pose
from poses.downward_dog import check_downward_dog


class PoseClassifier:

    def __init__(self):
        self.mp_pose = mp.solutions.pose

    def get_angles(self, landmarks):

        names = self.mp_pose.PoseLandmark

        def point(name):
            return get_point(landmarks[name])

        def angle(a, b, c):
            return calculate_angle(
                point(a), point(b), point(c)
            )

        angles = {
            "left_elbow": angle(
                names.LEFT_SHOULDER,
                names.LEFT_ELBOW,
                names.LEFT_WRIST
            ),
            "right_elbow": angle(
                names.RIGHT_SHOULDER,
                names.RIGHT_ELBOW,
                names.RIGHT_WRIST
            ),
            "left_knee": angle(
                names.LEFT_HIP,
                names.LEFT_KNEE,
                names.LEFT_ANKLE
            ),
            "right_knee": angle(
                names.RIGHT_HIP,
                names.RIGHT_KNEE,
                names.RIGHT_ANKLE
            ),
            "left_shoulder": angle(
                names.LEFT_ELBOW,
                names.LEFT_SHOULDER,
                names.LEFT_HIP
            ),
            "right_shoulder": angle(
                names.RIGHT_ELBOW,
                names.RIGHT_SHOULDER,
                names.RIGHT_HIP
            ),
            "left_hip": angle(
                names.LEFT_SHOULDER,
                names.LEFT_HIP,
                names.LEFT_KNEE
            ),
            "right_hip": angle(
                names.RIGHT_SHOULDER,
                names.RIGHT_HIP,
                names.RIGHT_KNEE
            ),
        }

        return angles

    def classify_warrior_two(self, angles):
        return check_warrior_two(angles)

    def classify_tree_pose(self, angles):
        return check_tree_pose(angles)

    def classify_mountain_pose(self, angles):
        return check_mountain_pose(angles)

    def classify_chair_pose(self, angles):
        return check_chair_pose(angles)

    def classify_warrior_one(self, angles):
        return check_warrior_one(angles)

    def classify_goddess_pose(self, angles):
        return check_goddess_pose(angles)

    def classify_triangle_pose(self, angles):
        return check_triangle_pose(angles)

    def classify_high_lunge(self, angles):
        return check_high_lunge(angles)

    def classify_plank_pose(self, angles):
        return check_plank_pose(angles)

    def classify_downward_dog(self, angles):
        return check_downward_dog(angles)
