
class FeedbackSystem:

    def _check_arms_straight(self, angles, feedback):
        if angles["left_elbow"] < 150:
            feedback.append("Straighten your left arm")

        if angles["right_elbow"] < 150:
            feedback.append("Straighten your right arm")

    def _check_one_bent_one_straight(self, angles, feedback):
        left_knee = angles["left_knee"]
        right_knee = angles["right_knee"]

        left_bent = 70 <= left_knee <= 120
        right_bent = 70 <= right_knee <= 120
        left_straight = left_knee >= 150
        right_straight = right_knee >= 150

        if left_bent and right_straight:
            pass
        elif right_bent and left_straight:
            pass
        elif not left_bent and not right_bent:
            feedback.append("Bend one knee and keep the other leg straight")
        else:
            feedback.append("Straighten the leg that should be extended")

    def warrior_two_feedback(self, angles):
        feedback = []
        self._check_one_bent_one_straight(angles, feedback)
        self._check_arms_straight(angles, feedback)

        if not feedback:
            feedback.append("Great! Warrior II posture looks good")

        return feedback

    def tree_pose_feedback(self, angles):
        feedback = []

        left_knee = angles["left_knee"]
        right_knee = angles["right_knee"]

        left_bent = 30 <= left_knee <= 100
        right_bent = 30 <= right_knee <= 100
        left_straight = left_knee >= 150
        right_straight = right_knee >= 150

        if not (
            (left_bent and right_straight)
            or (right_bent and left_straight)
        ):
            feedback.append(
                "Bend one knee and keep the supporting leg straight"
            )
        else:
            feedback.append(
                "Leg angles look suitable; check foot placement and balance"
            )

        return feedback

    def mountain_pose_feedback(self, angles):
        feedback = []

        if angles["left_knee"] < 160:
            feedback.append("Straighten your left leg")

        if angles["right_knee"] < 160:
            feedback.append("Straighten your right leg")

        self._check_arms_straight(angles, feedback)

        if not feedback:
            feedback.append(
                "Legs and elbows look straight; check upright alignment"
            )

        return feedback

    def chair_pose_feedback(self, angles):
        feedback = []

        for side in ("left", "right"):
            if not 70 <= angles[f"{side}_knee"] <= 130:
                feedback.append(f"Adjust your {side} knee bend")

            if angles[f"{side}_elbow"] < 150:
                feedback.append(f"Straighten your {side} arm")

            if angles[f"{side}_shoulder"] < 120:
                feedback.append("Raise your arms higher")

        if not feedback:
            feedback.append(
                "Joint angles look suitable; check your squat and arm position"
            )

        return feedback

    def warrior_one_feedback(self, angles):
        feedback = []
        self._check_one_bent_one_straight(angles, feedback)
        self._check_arms_straight(angles, feedback)

        if (
            angles["left_shoulder"] < 120
            or angles["right_shoulder"] < 120
        ):
            feedback.append("Raise both arms overhead")

        if not feedback:
            feedback.append(
                "Joint angles look suitable; check hip alignment and stance"
            )

        return feedback

    def goddess_pose_feedback(self, angles):
        feedback = []

        for side in ("left", "right"):
            knee = angles[f"{side}_knee"]
            elbow = angles[f"{side}_elbow"]
            shoulder = angles[f"{side}_shoulder"]

            if not 70 <= knee <= 130:
                feedback.append(f"Adjust your {side} knee bend")

            if elbow < 150:
                feedback.append(f"Straighten your {side} arm")

            if not 60 <= shoulder <= 130:
                feedback.append("Adjust your arms to an open position")

        if not feedback:
            feedback.append(
                "Joint angles look suitable; check knee direction and stance"
            )

        return feedback

    def triangle_pose_feedback(self, angles):
        feedback = []

        for side in ("left", "right"):
            if angles[f"{side}_knee"] < 150:
                feedback.append(f"Straighten your {side} leg")

            if angles[f"{side}_elbow"] < 150:
                feedback.append(f"Straighten your {side} arm")

        if not feedback:
            feedback.append(
                "Joint angles look suitable; check torso tilt and hand position"
            )

        return feedback

    def high_lunge_feedback(self, angles):
        feedback = []
        self._check_one_bent_one_straight(angles, feedback)
        self._check_arms_straight(angles, feedback)

        if (
            angles["left_shoulder"] < 120
            or angles["right_shoulder"] < 120
        ):
            feedback.append("Raise both arms overhead")

        if not feedback:
            feedback.append(
                "Joint angles look suitable; check your stance and balance"
            )

        return feedback

    def plank_pose_feedback(self, angles):
        feedback = []

        if angles["left_knee"] < 150 or angles["right_knee"] < 150:
            feedback.append("Straighten both legs")

        if (
            angles["left_elbow"] < 150
            or angles["right_elbow"] < 150
        ):
            feedback.append("Straighten your arms")

        if (
            angles["left_hip"] < 150
            or angles["right_hip"] < 150
        ):
            feedback.append("Work toward a straighter body line")

        if not feedback:
            feedback.append(
                "Joint angles look suitable; verify shoulder and hip alignment"
            )

        return feedback

    def downward_dog_feedback(self, angles):
        feedback = []

        if angles["left_knee"] < 140 or angles["right_knee"] < 140:
            feedback.append("Work toward straighter legs")

        if (
            angles["left_elbow"] < 150
            or angles["right_elbow"] < 150
        ):
            feedback.append("Straighten both arms")

        if not (
            50 <= angles["left_hip"] <= 130
            and 50 <= angles["right_hip"] <= 130
        ):
            feedback.append("Adjust your hip angle into an inverted V")

        if not feedback:
            feedback.append(
                "Joint angles look suitable; check shoulder and spine alignment"
            )

        return feedback
