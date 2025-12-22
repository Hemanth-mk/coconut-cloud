import streamlit as st
import requests
import tempfile
from PIL import Image

AWS_BACKEND_URL = "http://13.200.229.67:8000/predict"

st.set_page_config(
    page_title="Coconut Disease Detection",
    page_icon="🥥",
    layout="centered"
)

st.title("🌴 Coconut Disease Detection (Client App)")
st.caption("AI inference runs securely on AWS server")

uploaded = st.file_uploader(
    "Upload coconut tree image",
    type=["jpg", "jpeg", "png"]
)

if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="Uploaded Image", width=350)

    if st.button("🔍 Predict Disease"):
        st.info("Connecting to AI server...")

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            image.save(tmp.name)
            img_path = tmp.name

        try:
            with open(img_path, "rb") as f:
                response = requests.post(
                    AWS_BACKEND_URL,
                    files={"image": f},
                    timeout=10
                )
        except requests.exceptions.ReadTimeout:
            st.error("❌ AI server timeout. Try again.")
            st.stop()
        except Exception as e:
            st.error("❌ Unable to connect to AI server.")
            st.stop()

        if response.status_code != 200:
            st.error("❌ Prediction failed on server.")
            st.stop()

        data = response.json()

        disease = data.get("disease", "Unknown")
        confidence = data.get("confidence", 0)

        st.success(f"✅ Disease: {disease}")
        st.info(f"Confidence: {confidence*100:.2f}%")
