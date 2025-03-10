import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# ✅ Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

# ✅ Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=
    "You are a highly skilled radiology AI specializing in medical diagnostics. "
    "Your task is to analyze the provided medical scan (X-ray, MRI, CT) "
    "and cross-reference it with the patient's symptoms to generate an accurate diagnosis. "
    "Ensure that your response is structured, medically relevant, and avoids any false information."
)

# ✅ Streamlit Page Config
st.set_page_config(page_title="AI Medical Image Analysis", page_icon="🩺", layout="wide")

# ✅ UI Title
st.markdown("<h1 style='text-align: center;'>🩺 AI Medical Image Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload a medical scan & describe your symptoms for AI-powered diagnostics.</p>", unsafe_allow_html=True)

# ✅ Sidebar Instructions
st.sidebar.title("📝 Instructions")
st.sidebar.write("""
1️⃣ **Upload an X-ray, MRI, or medical scan** of any body part.\n
2️⃣ **Describe any symptoms or concerns** (optional but recommended).\n
3️⃣ Click **'Analyze Image'** to receive an AI-generated diagnostic report.
""")
st.sidebar.info("⚠️ This tool is for informational purposes only. Consult a doctor for medical advice.")

# ✅ Image Upload Section
st.markdown("### 📸 Upload a Medical Scan (X-ray, MRI, CT, etc.)")
uploaded_image = st.file_uploader("Choose a file...", type=["jpg", "png", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="📷 Uploaded Medical Image", use_container_width=True)

# ✅ Symptoms Input Section
st.markdown("### 📝 Describe Your Symptoms (Optional)")
symptoms = st.text_area("Describe any condition:", placeholder="Example: Pain in the knee after an injury, swelling around the joint...")

# ✅ Diagnosis Button
submit = st.button("🔍 Analyze Image")

# ✅ AI Processing
if submit:
    if not uploaded_image:
        st.error("🚨 Please upload an X-ray, MRI, or medical scan.")
    else:
        with st.spinner("🤖 AI is analyzing the image and description... Please wait."):

            # ✅ Convert Image to Bytes
            img_bytes = BytesIO()
            image.save(img_bytes, format="PNG")
            img_data = img_bytes.getvalue()

            # ✅ Prepare AI Query
            query = (
                "Analyze this medical image and correlate findings with the given patient symptoms. "
                "First, identify the body part in the image. Then, detect abnormalities like fractures, infections, or tumors. "
                "If symptoms are provided, compare them with visual findings to enhance diagnostic accuracy. "
                "Generate a structured medical report with:\n"
                "1️⃣ **Detected Body Part**\n"
                "2️⃣ **Observed Findings (Fractures, Infections, Tumors, etc.)**\n"
                "3️⃣ **Possible Diagnosis**\n"
                "4️⃣ **Recommended Next Steps (e.g., consult a radiologist, MRI needed, etc.)**\n"
                "5️⃣ **Caution: Reminder that this is an AI-generated analysis, and a doctor should be consulted.**"
            )

            try:
                # ✅ Send Image & Text to Gemini
                response = model.generate_content(
                    [query, {"mime_type": "image/png", "data": img_data}, f"Patient symptoms: {symptoms}"],
                    stream=False
                )

                # ✅ Display AI Diagnosis
                if response and response.text:
                    st.success("✅ AI Diagnosis Generated!")
                    st.subheader("🧑‍⚕️ AI Diagnosis:")
                    st.write(response.text)
                else:
                    st.error("❌ AI couldn't generate a response. Please try again.")

            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

# ✅ Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #7F8C8D;'>⚕️ AI Medical Image Analysis | © 2025</p>", unsafe_allow_html=True)