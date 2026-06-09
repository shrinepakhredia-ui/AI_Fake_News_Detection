import streamlit as st

from predict import predict_news


# Page Configuration

st.set_page_config(
    page_title="Fake News Detection",
    page_icon="📰",
    layout="centered"
)

# Sidebar

st.sidebar.title("📌 Project Information")

st.sidebar.write("""
### AI-Powered Fake News Detection

This application uses:

- Random Forest Classifier
- TF-IDF Vectorization
- NLP Text Preprocessing
- Machine Learning

Developed using Python & Streamlit.
""")

# Main Title

st.title("📰 AI-Powered Fake News Detection")

st.write(
    "Paste any news article below and click **Predict News**."
)

# Text Area

news = st.text_area(
    "Enter News Article",
    height=250,
    placeholder="Paste complete news article here..."
)

# Predict Button

if st.button("Predict News"):

    if news.strip() == "":

        st.warning("⚠ Please enter a news article.")

    else:

        with st.spinner("Analyzing News..."):

            result = predict_news(news)

        st.divider()

        st.subheader("Prediction Result")

        if "REAL" in result["prediction"]:

            st.success(result["prediction"])

        else:

            st.error(result["prediction"])

        st.metric(
            "Confidence",
            f"{result['confidence']} %"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.info(
                f"Fake Probability\n\n{result['fake_probability']} %"
            )

        with col2:

            st.info(
                f"Real Probability\n\n{result['real_probability']} %"
            )

# Footer

st.divider()

st.caption(
    "AI-Powered Fake News Detection | B.Tech AIML Project"
)