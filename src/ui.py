"""
==========================================================
AI Fake News Detection
User Interface Module

Author : Shrine Pakhredia
==========================================================
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

from predict import predict_news


# ==========================================================
# Load CSS
# ==========================================================

def load_css():

    with open("assets/styles.css", "r", encoding="utf-8") as css_file:

        st.markdown(

            f"<style>{css_file.read()}</style>",

            unsafe_allow_html=True

        )


# ==========================================================
# Initialize Session State
# ==========================================================

def initialize_session():

    if "history" not in st.session_state:

        st.session_state.history = []

    if "news_text" not in st.session_state:

        st.session_state.news_text = ""


# ==========================================================
# Header
# ==========================================================

def show_header():

    st.title("📰 AI Fake News Detection")

    st.caption(
        "Detect Fake News using Machine Learning, Natural Language Processing and Streamlit."
    )

    st.divider()


# ==========================================================
# Analyze Tab
# ==========================================================

def analyze_news_tab():

    st.subheader("Analyze News")

    news = st.text_area(

        "Enter News Article",

        value=st.session_state.news_text,

        height=250,

        placeholder="Paste complete news article here..."

    )

    col1, col2, col3 = st.columns(3)

    with col1:

        sample = st.button(

            "📄 Load Sample",

            use_container_width=True

        )

    with col2:

        clear = st.button(

            "🗑 Clear",

            use_container_width=True

        )

    with col3:

        analyze = st.button(

            "🚀 Analyze",

            use_container_width=True

        )


    # ------------------------------------------------------

    if sample:

        st.session_state.news_text = (

            "NASA has announced a new mission to Mars "
            "to study climate change and collect soil samples."

        )

        st.rerun()


    if clear:

        st.session_state.news_text = ""

        st.rerun()


    if analyze:

        if news.strip() == "":

            st.warning("Please enter a news article.")

            return


        with st.spinner("Analyzing News..."):

            result = predict_news(news)


        st.session_state.history.insert(

            0,

            {

        "Time": datetime.now().strftime("%d-%m-%Y %H:%M"),

        "Prediction": result["prediction"],

        "Confidence (%)": result["confidence"],

        "Risk": result["risk_level"],

        "Processing (sec)": result["processing_time"],

        "Words": result["word_count"]

            }

            )


        st.divider()

        st.subheader("Prediction Result")


        if "REAL" in result["prediction"]:

            st.success(result["prediction"])

        else:

            st.error(result["prediction"])


        st.metric(

            "Model Confidence",

            f"{result['confidence']} %"

        )


        st.progress(

            result["confidence"] / 100
        )
        st.divider()

        info1, info2 = st.columns(2)

        with info1:

         st.metric(

            "⚡ Processing Time",

            f"{result['processing_time']} sec"

          )

        with info2:

            st.metric(

              "🛡 Risk Level",

                result["risk_level"]

            )



        col1, col2 = st.columns(2)


        with col1:

            st.metric(

                "❌ Fake Probability",

                f"{result['fake_probability']} %"

            )

            st.progress(

                result["fake_probability"] / 100

            )


        with col2:

            st.metric(

                "✅ Real Probability",

                f"{result['real_probability']} %"

            )

            st.progress(

                result["real_probability"] / 100

            )
        st.divider()

        st.subheader("📊 Prediction Probability")

        chart_data = pd.DataFrame(

            {

                "Category": ["Fake News", "Real News"],

                "Probability": [

                    result["fake_probability"],

                    result["real_probability"]

                ]

            }

        )

        fig = px.bar(

            chart_data,

            x="Category",

            y="Probability",

            text="Probability",

            color="Category",

            color_discrete_sequence=[

                "#ff4b4b",

                "#00cc96"

            ]

        )

        fig.update_traces(

            width=0.28,

            texttemplate="%{text:.1f}%",

            textposition="outside",

            marker_line_width=0

        )

        fig.update_layout(

            height=270,

            bargap=0.65,

            showlegend=False,

            xaxis_title="",

            yaxis_title="Probability (%)",

            plot_bgcolor="rgba(0,0,0,0)",

            paper_bgcolor="rgba(0,0,0,0)",

            margin=dict(

                l=20,

                r=20,

                t=20,

                b=20

            )

        )


        fig.update_yaxes(

            range=[0,100],

            showgrid=False

        )

        fig.update_xaxes(

            showgrid=False
        )



        st.plotly_chart(

            fig,

            use_container_width=True

        )


        st.divider()

        st.subheader("Article Statistics")

        words = len(news.split())

        characters = len(news)

        reading_time = max(1, round(words / 200))

        s1, s2, s3 = st.columns(3)

        s1.metric("Words", words)

        s2.metric("Characters", characters)

        s3.metric("Reading Time", f"{reading_time} min")
        st.divider()

        st.subheader("🧠 Model Explanation")

        with st.container(border=True):

            st.write(result["explanation"])

        st.divider()

        st.subheader("Top Keywords")

        if result["top_keywords"]:

            cols = st.columns(len(result["top_keywords"]))

            for col, keyword in zip(cols, result["top_keywords"]):

                with col:

                    st.success(keyword)

        else:

            st.info("No Significant keywords found. ")

# ==========================================================
# History Tab
# ==========================================================

def history_tab():

    st.subheader("📜 Prediction History")

    if len(st.session_state.history) == 0:

        st.info("No predictions available.")

        return

    history_df = pd.DataFrame(

        st.session_state.history

    )

    st.dataframe(

        history_df,

        use_container_width=True,

        hide_index=True

    )

    csv = history_df.to_csv(

        index=False

    ).encode("utf-8")

    st.download_button(

        label="⬇ Download History",

        data=csv,

        file_name="prediction_history.csv",

        mime="text/csv",

        use_container_width=True

    )


# ==========================================================
# About Tab
# ==========================================================

def about_tab():

    st.subheader("ℹ About This Project")

    st.markdown("""

### 📰 AI Fake News Detection

This application detects whether a news article is **Real** or **Fake**
using Natural Language Processing and Machine Learning.

---

### 🤖 Model Information

| Property | Value |
|----------|-------|
| Algorithm | Random Forest |
| Feature Extraction | TF-IDF |
| Language | Python |
| Framework | Streamlit |
| Dataset Size | 44,898 Articles |

---

### ⚙ Workflow

1. Text Cleaning
2. Tokenization
3. TF-IDF Vectorization
4. Random Forest Prediction
5. Confidence Calculation

---

### 👨‍💻 Developer

**Shrine Pakhredia**

B.Tech Artificial Intelligence & Machine Learning

""")



# ==========================================================
# Footer
# ==========================================================

def footer():

    st.divider()

    st.caption(

    "Made with using Python, Streamlit & Scikit-Learn"

    )

    st.caption(

    "© 2026 Shrine Pakhredia"

    )



# ==========================================================
# Run UI
# ==========================================================

def run_ui():

    load_css()

    initialize_session()

    show_header()

    analyze_tab, history, about = st.tabs(

        [

            "📰 Analyze",

            "📜 History",

            "ℹ About"

        ]

    )

    with analyze_tab:

        analyze_news_tab()

    with history:

        history_tab()

    with about:

        about_tab()

    footer()