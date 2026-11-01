
import os
import cv2
import numpy as np
import streamlit as st

from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="College Signature Identification",
    page_icon="✍️",
    layout="centered"
)

DATASET_DIR = "signature_demo_dataset"
IMG_SIZE = (128, 64)


# ---------------- IMAGE PREPROCESSING ----------------

def preprocess_signature_from_path(image_path):
    """
    Loads signature image from path,
    converts it into grayscale, resizes and normalizes.
    """

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        return None

    img_resized = cv2.resize(img, IMG_SIZE)

    return (img_resized / 255.0).flatten()


def preprocess_signature_uploaded(uploaded_file):
    """
    Processes uploaded signature image.
    """

    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    img = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_GRAYSCALE
    )

    if img is None:
        return None

    img_resized = cv2.resize(img, IMG_SIZE)

    return (img_resized / 255.0).flatten()


# ---------------- LOAD DATASET ----------------

@st.cache_data
def load_dataset():

    data = []
    labels = []

    if not os.path.exists(DATASET_DIR):
        return np.array([]), np.array([])

    for student_name in os.listdir(DATASET_DIR):

        student_folder = os.path.join(
            DATASET_DIR,
            student_name
        )

        if not os.path.isdir(student_folder):
            continue

        for file_name in os.listdir(student_folder):

            if file_name.lower().endswith(
                ('.png', '.jpg', '.jpeg')
            ):

                file_path = os.path.join(
                    student_folder,
                    file_name
                )

                features = preprocess_signature_from_path(
                    file_path
                )

                if features is not None:
                    data.append(features)
                    labels.append(student_name)

    return np.array(data), np.array(labels)


# ---------------- APPLICATION UI ----------------

st.title("✍ College Signature Identification System")

st.markdown(
    "Identify student signatures using "
    "Computer Vision and Machine Learning."
)


# ---------------- SIDEBAR CONTROLS ----------------

st.sidebar.header("Configuration & Controls")

k_neighbors = st.sidebar.slider(
    "KNN Neighbors (K)",
    min_value=1,
    max_value=7,
    value=3
)

test_split_size = st.sidebar.slider(
    "Test Split Ratio",
    min_value=0.1,
    max_value=0.4,
    value=0.2,
    step=0.05
)


# ---------------- LOAD DATASET ----------------

if not os.path.exists(DATASET_DIR):

    st.warning(
        f"Dataset folder '{DATASET_DIR}' not found. "
        "Please create it and add student folders."
    )

else:

    X, y = load_dataset()

    if len(X) == 0:

        st.warning(
            "No signature images found. "
            "Please add JPG, JPEG or PNG images."
        )

    else:

        unique_students = np.unique(y)
        total_students = len(unique_students)

        st.sidebar.success(
            f"Loaded {len(X)} signatures "
            f"across {total_students} students."
        )

        # ---------------- TRAIN MODEL ----------------

        if st.sidebar.button(
            "Train Model",
            type="primary"
        ):

            class_counts = {
                student: int(np.sum(y == student))
                for student in unique_students
            }

            if total_students < 2:

                st.error(
                    "At least two different students "
                    "are required for classification."
                )

            elif min(class_counts.values()) < 2:

                st.error(
                    "Each student must have at least "
                    "two signature images."
                )

            else:

                try:

                    X_train, X_test, y_train, y_test = (
                        train_test_split(
                            X,
                            y,
                            test_size=test_split_size,
                            random_state=42,
                            stratify=y
                        )
                    )

                    if k_neighbors > len(X_train):

                        st.error(
                            "K cannot be greater than "
                            "the number of training samples."
                        )

                    else:

                        with st.spinner(
                            "Training KNN classifier..."
                        ):

                            model = KNeighborsClassifier(
                                n_neighbors=k_neighbors
                            )

                            model.fit(X_train, y_train)

                            y_pred = model.predict(X_test)

                            acc = accuracy_score(
                                y_test,
                                y_pred
                            )

                            report = classification_report(
                                y_test,
                                y_pred,
                                output_dict=True,
                                zero_division=0
                            )

                            st.session_state["model"] = model
                            st.session_state["is_trained"] = True
                            st.session_state["accuracy"] = acc
                            st.session_state["report"] = report
                            st.session_state["student_count"] = total_students

                        st.success(
                            "Model trained successfully!"
                        )

                except ValueError as e:

                    st.error(
                        f"Training error: {e}"
                    )


        # ---------------- MODEL PERFORMANCE ----------------

        if st.session_state.get("is_trained", False):

            st.subheader("📊 Model Performance")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Test Accuracy",
                    f"{st.session_state['accuracy'] * 100:.2f}%"
                )

            with col2:

                st.metric(
                    "Students",
                    st.session_state["student_count"]
                )

            with st.expander(
                "View Detailed Classification Report"
            ):

                st.json(
                    st.session_state["report"]
                )

        st.divider()

        # ---------------- SIGNATURE PREDICTION ----------------

        st.subheader("🔍 Test a New Signature")

        uploaded_file = st.file_uploader(
            "Upload a signature image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file is not None:

            image = Image.open(uploaded_file).convert("RGB")

            st.image(
                image,
                caption="Uploaded Signature",
                width=300
            )

            uploaded_file.seek(0)

            features = preprocess_signature_uploaded(
                uploaded_file
            )

            if features is None:

                st.error(
                    "Unable to process the uploaded image."
                )

            elif st.session_state.get("is_trained", False):

                model = st.session_state["model"]

                prediction = model.predict(
                    [features]
                )[0]

                probabilities = model.predict_proba(
                    [features]
                )[0]

                confidence = np.max(probabilities) * 100

                st.success(
                    f"Predicted Student: {prediction}"
                )

                st.metric(
                    "Prediction Confidence",
                    f"{confidence:.2f}%"
                )

                st.caption(
                    "This is the model's estimated class probability, "
                    "not proof of signature authenticity."
                )

            else:

                st.info(
                    "Please train the model first "
                    "using the sidebar button."
                )

