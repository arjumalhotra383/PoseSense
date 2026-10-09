import cv2
import mediapipe as mp

# Load image
image = cv2.imread("person.jpg")

if image is None:
    print("ERROR: person.jpg could not be loaded.")
    exit()

print("Image loaded successfully!")
print("Image size:", image.shape)

# MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

with mp_pose.Pose(
    static_image_mode=True,
    model_complexity=1,
    min_detection_confidence=0.2
) as pose:

    # OpenCV BGR -> RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect pose
    results = pose.process(rgb_image)

    if results.pose_landmarks:
        print("Person detected!")
        print("Number of landmarks:", len(results.pose_landmarks.landmark))

        # Draw body landmarks
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        # Show result
        cv2.imshow("PoseSense - Pose Detection", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        print("No person detected.")