
import cv2

from pose_detector import PoseDetector
from pose_classifier import PoseClassifier
from feedback import FeedbackSystem


POSES = {
    "1": ("Warrior II", "warrior_two"),
    "2": ("Tree Pose", "tree_pose"),
    "3": ("Mountain Pose", "mountain_pose"),
    "4": ("Chair Pose", "chair_pose"),
    "5": ("Warrior I", "warrior_one"),
    "6": ("Goddess Pose", "goddess_pose"),
    "7": ("Triangle Pose", "triangle_pose"),
    "8": ("High Lunge", "high_lunge"),
    "9": ("Plank Pose", "plank_pose"),
    "0": ("Downward-Facing Dog", "downward_dog"),
}


def main():

    detector = PoseDetector()
    classifier = PoseClassifier()
    feedback_system = FeedbackSystem()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("ERROR: Could not open camera.")
        detector.close()
        return

    selected_key = "1"

    print("\n========== POSESENSE ==========")
    print("Select a pose using its keyboard key:")

    for key, (name, _) in POSES.items():
        print(f"{key} = {name}")

    print("Q = Quit")
    print("\nStarting webcam...")

    try:
        while True:

            success, frame = camera.read()

            if not success:
                print("Could not read camera frame.")
                break

            frame = cv2.flip(frame, 1)
            results = detector.detect(frame)

            pose_name, pose_key = POSES[selected_key]

            cv2.putText(
                frame,
                f"Selected: {pose_name}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            if results.pose_landmarks:

                detector.draw_landmarks(frame, results)
                landmarks = results.pose_landmarks.landmark
                angles = classifier.get_angles(landmarks)

                classify_method = getattr(
                    classifier,
                    f"classify_{pose_key}"
                )

                feedback_method = getattr(
                    feedback_system,
                    f"{pose_key}_feedback"
                )

                pose_correct = classify_method(angles)
                feedback = feedback_method(angles)

                if pose_correct:
                    status = f"{pose_name}: RULE CHECK PASSED"
                    status_color = (0, 255, 0)
                else:
                    status = f"{pose_name}: NEEDS ADJUSTMENT"
                    status_color = (0, 0, 255)

                cv2.putText(
                    frame,
                    status,
                    (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    status_color,
                    2
                )

                y = 110

                for message in feedback[:4]:
                    cv2.putText(
                        frame,
                        message,
                        (20, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (0, 255, 255),
                        2
                    )
                    y += 30

                angle_text = [
                    f"L Knee: {angles['left_knee']:.0f}",
                    f"R Knee: {angles['right_knee']:.0f}",
                    f"L Elbow: {angles['left_elbow']:.0f}",
                    f"R Elbow: {angles['right_elbow']:.0f}",
                ]

                y_angle = max(y + 10, 250)

                for text in angle_text:
                    cv2.putText(
                        frame,
                        text,
                        (20, y_angle),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (255, 255, 255),
                        2
                    )
                    y_angle += 25

            else:
                cv2.putText(
                    frame,
                    "No person detected",
                    (20, 75),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

            cv2.imshow(
                "PoseSense - Yoga Pose Correction",
                frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            key_char = chr(key) if key < 128 else ""

            if key_char in POSES:
                selected_key = key_char
                print(
                    "Selected pose:",
                    POSES[selected_key][0]
                )

    finally:
        camera.release()
        cv2.destroyAllWindows()
        detector.close()


if __name__ == "__main__":
    main()
