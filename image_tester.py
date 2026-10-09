
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
    "10": ("Downward-Facing Dog", "downward_dog"),
}


def test_image(image_path, pose_key):

    frame = cv2.imread(image_path)

    if frame is None:
        print(f"Could not read image: {image_path}")
        return

    detector = PoseDetector()
    classifier = PoseClassifier()
    feedback_system = FeedbackSystem()

    try:
        results = detector.detect(frame)

        if not results.pose_landmarks:
            print("No person detected in image.")

            cv2.putText(
                frame,
                "No person detected",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        else:
            detector.draw_landmarks(frame, results)

            landmarks = results.pose_landmarks.landmark
            angles = classifier.get_angles(landmarks)

            pose_name, pose_key_name = POSES[pose_key]

            classify_method = getattr(
                classifier,
                f"classify_{pose_key_name}"
            )

            feedback_method = getattr(
                feedback_system,
                f"{pose_key_name}_feedback"
            )

            correct = classify_method(angles)
            messages = feedback_method(angles)

            status = "CORRECT" if correct else "NOT CORRECT"
            color = (0, 255, 0) if correct else (0, 0, 255)

            print(f"\nPose: {pose_name}")
            print(f"Rule result: {status}")

            print("\nAngles:")
            for name, value in angles.items():
                print(f"{name}: {value:.1f} degrees")

            print("\nFeedback:")
            for message in messages:
                print("-", message)

            cv2.putText(
                frame,
                f"{pose_name}: {status}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

            y = 80

            for message in messages:
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

    finally:
        detector.close()

    height, width = frame.shape[:2]

    if width > 1200:
        scale = 1200 / width
        frame = cv2.resize(
            frame,
            (1200, int(height * scale))
        )

    cv2.imshow("PoseSense - Image Test", frame)

    print("\nPress any key on the image window to close.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":

    print("\n========== POSESENSE IMAGE TESTER ==========\n")

    for key, (name, _) in POSES.items():
        print(f"{key}. {name}")

    choice = input("\nChoose a pose (1-10): ").strip()

    if choice not in POSES:
        print("Invalid choice. Choose a number from 1 to 10.")

    else:
        image_path = input(
            "Image path (Enter for person.jpg): "
        ).strip()

        if not image_path:
            image_path = "person.jpg"

        test_image(image_path, choice)
