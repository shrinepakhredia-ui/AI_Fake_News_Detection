import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

from predict import predict_news

from src.url_extractor import extract_article



# Load CSS

def load_css():

    with open("assets/styles.css", "r", encoding="utf-8") as css_file:

        st.markdown(

            f"<style>{css_file.read()}</style>",

            unsafe_allow_html=True

        )


# Initialize Session State

def initialize_session():

    if "history" not in st.session_state:

        st.session_state.history = []

    if "news_text" not in st.session_state:

        st.session_state.news_text = ""


# Header

def show_header():

    st.title("📰 AI Fake News Detection")

    st.caption(
        "Detect Fake News using Machine Learning, Natural Language Processing and Streamlit."
    )

    st.divider()


# Analyze Tab

def analyze_news_tab():

    st.subheader("Analyze News")

    input_mode = st.radio(

        "Choose Input Type",
        (
            "📝 Paste News Text",

            "🔗 Analyze News URL"
        ),

        horizontal=True

    )

    news = ""

    url = ""

    if input_mode == "📝 Paste News Text":

        news = st.text_area(

            "Enter News Article",

            value=st.session_state.news_text,

            height=250,

            placeholder="Paste complete news article here..."

        )

    else:

        url = st.text_input(

            "Enter News URL",

            placeholder="https://example.com/news"

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

        if input_mode == "📝 Paste News Text":

            if news.strip() == "":

                st.warning("Please enter a news article.")

                return

        else:

            if url.strip() == "":

                st.warning("Please enter a news URL.")

                return

            with st.spinner("Extracting article..."):

                article = extract_article(url)

            if not article["success"]:

                st.error("Unable to extract the article.")

                st.caption(article["error"])

                return

            if article["trusted"]:

                st.success(
                    f"✅ Verified Publisher: {article['publisher']}"
                )

                st.caption(
                    f"Domain: {article['domain']}"
                )

            else:
                st.warning(
                    "⚠️ Source Not Verified"
                )

                st.caption(
                    f"Domain: {article['domain']}"
                )

            st.subheader(article["title"])
            if article["authors"]:

                st.caption(
                    "✍ Author: " + ", ".join(article["authors"])
                )

            news = article["text"]

        if input_mode == "🔗 Analyze News URL":

            st.divider()

            st.subheader("📰 Extracted Article")

            st.write("### " + article["title"])

            if article["top_image"]:

                st.image(

                    article["top_image"],

                    use_container_width=True

                )

            if article["authors"]:

                st.caption(

                    "Author: " +

                    ", ".join(article["authors"])

                )

            if article["publish_date"]:

                st.caption(

                    f"Published: {article['publish_date']}"

                )

            with st.expander("View Extracted Article"):

                st.write(news)



        with st.spinner("Analyzing News..."):

            result = predict_news(news)


        st.session_state.history.insert(

            0,

            {

        "Time": datetime.now().strftime("%d-%m-%Y %H:%M"),

        "Prediction": result["prediction"],

        "Confidence(%)": result["confidence"],

        "Risk": result["risk_level"],

        "Processing (sec)": result["processing_time"],

        "Words": result["word_count"]

            }

            )


        st.divider()

        st.subheader("🎯 Prediction Result")

        if "REAL" in result["prediction"]:
            st.success(result["prediction"])

        else:

            st.error(result["prediction"])

        st.metric(
            "🎯 Model Confidence",

            f"{result['confidence']}%"
        )

        st.progress(
            result["confidence"]/100
        )

        st.divider()

        card1,card2 = st.columns(2)

        with card1:

            st.metric(

                "🧠 AI Trust Score",
                f"{result['trust_score']}%"
            )

        with card2:
            st.metric(

                "🛡 Risk Level",
                result["risk_level"]
            )

        card3, card4 = st.columns(2)

        with card3:
            st.metric(
                "🏢 Publisher",
                result["publisher"]
            )

        with card4:
            st.metric(
                "⚡ Processing Time",
                f"{result['processing_time']}sec"
            )

        if article["trusted"]:
            st.success( f"🟢 Verified Source ({article['publisher']})")

        else:
            st.warning("🟡 Source Not Verified")



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

                "#9f0101",

                "#0ee8ae"

            ]

        )

        fig.update_traces(

            width=0.18,

            texttemplate="%{text:.1f}%",

            textposition="outside",

            marker_line_width=0

        )

        fig.update_layout(

            height=330,

            bargap=0.80,

            plot_bgcolor="rgba(0,0,0,0)",

            paper_bgcolor="rgba(0,0,0,0)",

            showlegend=False,

            xaxis_title=None,

            yaxis_title="Probability (%)",

            font=dict(
                size=14
            ),


            margin=dict(

                l=20,

                r=20,

                t=20,

                b=20

            )

        )


        fig.update_yaxes(

            range=[0,105],

            showgrid=False

        )

        fig.update_xaxes(

            showgrid=False
        )



        st.plotly_chart(

            fig,

            use_container_width=True,

            config={
                "displayModeBar": False
            }

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

        st.subheader("🔑 Top Keywords")

        if result["top_keywords"]:

            keyword_cols = st.columns(min(len(result["top_keywords"]), 5))

            for col, keyword in zip(keyword_cols, result["top_keywords"]):

                with col:

                    st.info(keyword)

        else:

            st.info("No keywords detected.")

        st.divider()

        st.subheader("✅ Trust Factors")

        if result["trust_reasons"]:

            for reason in result["trust_reasons"]:

                st.success(reason)

        else:

            st.warning("No trust indicators available.")


        st.divider()

        st.subheader("🧠 AI Model Explanation")

        with st.container(border=True):

            st.markdown(result["explanation"])


        st.divider()

        st.subheader("Top Keywords")

        if result["top_keywords"]:

            cols = st.columns(len(result["top_keywords"]))

            for col, keyword in zip(cols, result["top_keywords"]):

                with col:

                    st.success(keyword)

        else:

            st.info("No Significant keywords found. ")

# History Tab

def history_tab():

    st.subheader("📜 Prediction History")

    if len(st.session_state.history) == 0:

        st.info("No predictions available.")

        return

    history_df = pd.DataFrame(

        st.session_state.history

    )

    total_predictions = len(history_df)

    real_predictions = len(
        history_df[
            history_df["Prediction"].str.contains(
                "REAL",
                case=False,
                na=False
            )
        ]
    )

    fake_predictions = total_predictions - real_predictions
    average_confidence= round(
        history_df["Confidence(%)"].mean(),
        2
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📊 Total",
            total_predictions
        )

    with col2:
        st.metric(
            "✅ Real",
            real_predictions
        )

    with col3:
        st.metric(
            "❌ Fake",
            fake_predictions
        )

    with col4:
        st.metric(
            "🎯 Avg Confidence",
            f"{average_confidence}%"
        )

    st.divider()

    history_df["Confidence(%)"] = history_df["Confidence(%)"].astype(float)

    styled_df = history_df.style.format({
        "Confidence (%)" : "{:.2f}%"

    }).background_gradient(

        subset=["Confidence(%)"],
        cmap="Greens"
    )

    st.dataframe(

        styled_df,
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

    st.divider()

    if st.button(
        "🗑 Clear History",
        use_container_width=True
    ):

        st.session_state.history.clear()
        st.success("History Cleared Successfully.")
        st.rerun()


# About Tab

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



# Footer

def footer():

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.caption(
            "📰 AI Fake News Detection"

        )

    with col2:

        st.caption(

            "Made with ❤️ using Python • Streamlit • Scikit-Learn"

        )

    st.caption(
        "© 2026 Shrine Pakhredia"
    )



# Run UI

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