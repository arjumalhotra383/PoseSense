
import cv2
import av
import numpy as np
import streamlit as st

from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

from pose_detector import PoseDetector
from pose_classifier import PoseClassifier
from feedback import FeedbackSystem


st.set_page_config(
    page_title="PoseSense | Yoga Pose Checker",
    page_icon="🧘",
    layout="wide"
)

POSES = {
    "Warrior II": "warrior_two",
    "Tree Pose": "tree_pose",
    "Mountain Pose": "mountain_pose",
    "Chair Pose": "chair_pose",
    "Warrior I": "warrior_one",
    "Goddess Pose": "goddess_pose",
    "Triangle Pose": "triangle_pose",
    "High Lunge": "high_lunge",
    "Plank Pose": "plank_pose",
    "Downward-Facing Dog": "downward_dog",
}


class YogaVideoProcessor(VideoProcessorBase):
    def __init__(self, pose_name, pose_key):
        self.pose_name = pose_name
        self.pose_key = pose_key
        self.detector = PoseDetector()
        self.classifier = PoseClassifier()
        self.feedback_system = FeedbackSystem()

    def recv(self, video_frame):
        frame = video_frame.to_ndarray(format="bgr24")
        frame = cv2.flip(frame, 1)

        results = self.detector.detect(frame)

        cv2.putText(
            frame,
            f"Pose: {self.pose_name}",
            (15, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        if results.pose_landmarks:
            self.detector.draw_landmarks(frame, results)

            angles = self.classifier.get_angles(
                results.pose_landmarks.landmark
            )

            check = getattr(
                self.classifier, f"classify_{self.pose_key}"
            )
            feedback_fn = getattr(
                self.feedback_system, f"{self.pose_key}_feedback"
            )

            passed = check(angles)
            messages = feedback_fn(angles)

            status = "RULE CHECK PASSED" if passed else "NEEDS ADJUSTMENT"
            cv2.putText(
                frame,
                status,
                (15, 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 200, 0) if passed else (0, 0, 255),
                2
            )

            y = 100
            for message in messages[:3]:
                cv2.putText(
                    frame,
                    str(message)[:65],
                    (15, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.45,
                    (255, 255, 255),
                    1
                )
                y += 25
        else:
            cv2.putText(
                frame,
                "No person detected",
                (15, 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

        return av.VideoFrame.from_ndarray(frame, format="bgr24")


st.title("🧘 PoseSense")
st.subheader("Yoga Pose Detection and Feedback")

st.write(
    "Check your yoga pose using an uploaded image or your live webcam."
)

st.info(
    "PoseSense uses MediaPipe landmarks and rule-based checks. "
    "Results are estimates, not professional or medical advice."
)

mode = st.radio(
    "Choose your input method",
    ["Upload Image", "Live Webcam"],
    horizontal=True
)

selected_pose = st.selectbox(
    "Choose your yoga pose",
    list(POSES.keys())
)
pose_key = POSES[selected_pose]


if mode == "Upload Image":
    uploaded_file = st.file_uploader(
        "Upload a yoga pose image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image_bytes = np.frombuffer(
            uploaded_file.getvalue(), np.uint8
        )
        image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

        if image is None:
            st.error("Could not read this image. Please try another.")
        else:
            st.image(
                cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
                caption="Uploaded image",
                use_container_width=True
            )

            if st.button("Analyze My Pose", type="primary"):
                detector = PoseDetector()

                try:
                    with st.spinner("Analyzing your pose..."):
                        results = detector.detect(image)

                        if not results.pose_landmarks:
                            st.error(
                                "No person detected. Try a clear, "
                                "full-body image with good lighting."
                            )
                        else:
                            annotated = detector.draw_landmarks(
                                image.copy(), results
                            )
                            classifier = PoseClassifier()
                            feedback_system = FeedbackSystem()

                            angles = classifier.get_angles(
                                results.pose_landmarks.landmark
                            )

                            check = getattr(
                                classifier, f"classify_{pose_key}"
                            )
                            feedback_fn = getattr(
                                feedback_system, f"{pose_key}_feedback"
                            )

                            passed = check(angles)
                            messages = feedback_fn(angles)

                            st.image(
                                cv2.cvtColor(
                                    annotated, cv2.COLOR_BGR2RGB
                                ),
                                caption="Detected body landmarks",
                                use_container_width=True
                            )

                            if passed:
                                st.success(
                                    f"{selected_pose}: Rule check passed"
                                )
                            else:
                                st.warning(
                                    f"{selected_pose}: Needs adjustment"
                                )

                            st.caption(
                                "This is a rule-based estimate, not a "
                                "validated measure of yoga correctness."
                            )

                            st.subheader("Joint Angles")
                            left, right = st.columns(2)

                            with left:
                                st.metric(
                                    "Left Knee",
                                    f"{angles['left_knee']:.1f}°"
                                )
                                st.metric(
                                    "Left Elbow",
                                    f"{angles['left_elbow']:.1f}°"
                                )
                                st.metric(
                                    "Left Shoulder",
                                    f"{angles['left_shoulder']:.1f}°"
                                )

                            with right:
                                st.metric(
                                    "Right Knee",
                                    f"{angles['right_knee']:.1f}°"
                                )
                                st.metric(
                                    "Right Elbow",
                                    f"{angles['right_elbow']:.1f}°"
                                )
                                st.metric(
                                    "Right Shoulder",
                                    f"{angles['right_shoulder']:.1f}°"
                                )

                            st.subheader("Feedback")
                            for message in messages:
                                st.write(f"• {message}")

                except Exception as error:
                    st.error(f"Analysis failed: {error}")
                finally:
                    detector.close()


else:
    st.write(
        "Allow camera access in your browser when prompted. "
        "Stand far enough away for your full body to be visible."
    )

    webrtc_streamer(
        key=f"posesense-{pose_key}",
        video_processor_factory=lambda: YogaVideoProcessor(
            selected_pose, pose_key
        ),
        media_stream_constraints={
            "video": True,
            "audio": False
        },
        async_processing=True
    )

    st.caption(
        "Live results are based on simple angle rules and may be inaccurate."
    )


st.divider()
st.caption(
    "PoseSense | Python • OpenCV • MediaPipe • Streamlit"
)
