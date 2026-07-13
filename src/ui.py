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
def dashboard_card(icon, title, value):

    st.markdown(
        f"""
<div class="dashboard-card" style="
background:linear-gradient(145deg,#1e293b,#0f172a);
padding:22px;
border-radius:18px;
text-align:center;
border:1px solid rgba(255,255,255,.08);
box-shadow:0 10px 25px rgba(0,0,0,.25);
height:170px;
display:flex;
flex-direction:column;
justify-content:center;
">

<div style="font-size:34px;">
{icon}
</div>

<div style="
margin-top:12px;
font-size:12px;
letter-spacing:1.3px;
color:#94a3b8;
font-weight:600;
">

{title}

</div>

<div style="
margin-top:14px;
font-size:22px;
font-weight:700;
color:white;
">

{value}

</div>

</div>
""",
        unsafe_allow_html=True,
    )
def show_header():

    st.markdown(
        """
<div style="
background:linear-gradient(135deg,#0f172a,#1e3a8a,#2563eb);
padding:40px;
border-radius:22px;
color:white;
box-shadow:0 12px 35px rgba(0,0,0,.25);
margin-bottom:25px;
">

<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">

<div>

<h1 style="margin:0;font-size:40px;">
📰 AI Fake News Detection
</h1>

<p style="margin-top:12px;
font-size:18px;
opacity:.92;">

Detect Fake & Misleading News using
Machine Learning, NLP & Source Intelligence.

</p>

</div>

<div style="
background:rgba(255,255,255,.12);
padding:18px 22px;
border-radius:18px;
text-align:center;
min-width:170px;
">

<div style="font-size:14px;">
⚡ Powered by
</div>

<div style="font-size:26px;font-weight:bold;">
Random Forest
</div>

<div style="font-size:26px;font-weight:bold;">
TF-IDF + NLP
</div>


</div>

</div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("### 🚀 Platform Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        dashboard_card(
            "🧠",
            "Random Forest",
            "Machine Learning Model"
        )

    with c2:
        dashboard_card(
            "📊",
            "5000 FEATURES",
            "TF-IDF Vectorizer"
        )

    with c3:
        dashboard_card(
            "🌍",
            "URL ANALYSIS",
            "Publisher Verification"
        )

    with c4:
        dashboard_card(
            "🛡",
            "AI Trust Score",
            "Source Intelligence"
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

            "🚀 Analyze News",

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

            with st.spinner("🌐 Extracting article from the news website..."):

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



        with st.spinner("🤖 AI is analyzing the article... Please wait"):

            if input_mode == "📝 Paste News Text":

                result = predict_news(news,None)

            else:

                result = predict_news(
                    article["text"],
                    url
                )



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

        st.success("✅ Analysis Completed Successfully")

        show_prediction_card(result)

        st.divider()

        st.subheader("🌐 Source Reliability")

        left, right = st.columns([3,1])

        with left:
            st.progress(
                result["source_score"]/100
            )

        with right:
            st.metric(
                "Source",
                f"{result['source_score']}%"
            )

        if result["source_level"]== "Very High":
            st.success(
                f"🟢 Reliability : {result['source_level']}"
            )

        elif result["source_level"]== "High":
            st.info(
                f"🔵 Reliability : {result['source_level']}"
            )

        elif result["source_level"]== "Moderate":
            st.warning(
                f"🟡 Reliability : {result['source_level']}"
            )

        else:
            st.error(
                f"🔴 Reliability : {result['source_level']}"
            )

        if result["trusted_source"]:
            st.success(
                "✅ Verified News Publisher"
            )

        else:
            st.warning(
                "⚠️ Source Not Verified"
            )


        st.divider()

        st.subheader("📰 Overall News Authenticity")

        left, right = st.columns([3,1])

        with left:

            st.progress(

                result["authenticity_score"]/100

            )

        with right:

            st.metric(

                "Authenticity",

                f"{result['authenticity_score']}%"

            )

        level = result["authenticity_level"]

        if level == "High":

            st.success(

                f"🟢 {level}"

            )

        elif level == " Good":

            st.info(

                f"🔵 {level}"

            )

        elif level == "Verify":

            st.warning(

                f"🟡 {level}"

            )

        else:

            st.error(

                f"🔴 {level}"

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

        st.markdown("""
            ## 📊 Prediction Confidence Distribution

            Comparison of the predicted probabilities for Fake and Real News.

            """)

        chart_data = pd.DataFrame(
            {
                "Category": ["Real News", "Fake News"],
                "Probability": [
                    result["real_probability"],
                    result["fake_probability"]
                ]
            }
        )

        fig = px.pie(

            chart_data,

            names="Category",

            values="Probability",

            hole=0.72,

            color="Category",

            color_discrete_map={
                "Real News": "#22c55e",
                "Fake News": "#ef4444"
            }

        )

        fig.update_traces(

            textposition="inside",

            textinfo="percent+label",

            marker=dict(
                line=dict(color="#111827", width=3)
            ),

            pull=[0,0.04]

        )

        fig.update_layout(

            height=420,

            showlegend=True,

            legend_title=None,

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            margin=dict(l=20,r=20,t=20,b=20),

            font=dict(size=15)

        )

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={
                "displayModeBar":False
            }

        )


        col1, col2 = st.columns(2)

        with col1:

            st.success(f"✅ Real Probability : {result['real_probability']}%")

        with col2:

            st.error(f"❌ Fake Probability : {result['fake_probability']}%")


        st.divider()

        st.markdown("""
            ## 📑 Article Statistics

            Basic textual insights extracted from the submitted article.

            """)

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

            chips = ""

            for keyword in result["top_keywords"]:

                chips += f"""
        <span style="
        display:inline-block;
        padding:8px 16px;
        margin:6px;
        background:#1d4ed8;
        color:white;
        border-radius:999px;
        font-size:14px;
        font-weight:600;
        ">
        {keyword}
        </span>
        """

            st.markdown(chips, unsafe_allow_html=True)

        else:

            st.info("No keywords detected.")
        st.divider()

        st.markdown("""
            ## ✅ Why did the AI trust this article?

            The following indicators contributed to the final trust score.

            """)

        if result["trust_reasons"]:

            for reason in result["trust_reasons"]:

                st.markdown(f"""
                <div style="
                padding:14px;
                border-radius:12px;
                background:#16253d;
                margin-bottom:10px;
                border-left:5px solid #22c55e;
                color:white;">
                ✅ {reason}
                </div>
                """, unsafe_allow_html=True)

        else:

            st.warning("No trust indicators available.")

        st.divider()

        st.markdown("""

        ## 🤖 AI Verdict

        A concise summary generated by the AI after evaluating the article.

        """)

        st.info(result["ai_verdict"])

        st.divider()

        st.markdown("""

        ## 🤖 AI Assessment Report

        The explanation below describes how the AI reached its prediction based on language patterns, confidence score and source analysis.

        """)

        with st.container(border=True):

            st.markdown(result["explanation"])


# History Tab

def history_tab():

    st.markdown("""
    # 📜 Prediction Analytics Dashboard

    Review every prediction generated during this session along with AI confidence,
    risk level and processing statistics.

    ---
    """)

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

    average_confidence = round(
        history_df["Confidence(%)"].mean(),
        2
    )

    highest_confidence = round(
        history_df["Confidence(%)"].max(),
        2
    )

    lowest_confidence = round(
        history_df["Confidence(%)"].min(),
        2
    )

    average_time = round(
        history_df["Processing (sec)"].mean(),
        3
    )

    col1, col2, col3, col4, col5, col6 = st.columns(6)

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

    with col5:
        st.metric(
            "🚀 Highest",
            f"{highest_confidence}%"
        )

    with col6:
        st.metric(
            "⚡ Avg Time",
            f"{average_time}s"
        )


    st.divider()

    st.markdown("""
    ## 📊 Prediction Distribution

    Visual representation of AI prediction results.

    """)

    chart = pd.DataFrame(
        {
            "Category": ["Real News", "Fake News"],
            "Count": [real_predictions, fake_predictions]
        }
    )

    fig = px.pie(
        chart,
        values="Count",
        names="Category",
        hole=.60
    )

    fig.update_layout(
        height=350,
        showlegend=True,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


    st.divider()

    st.markdown("""
    ## 📈 Confidence Trend

    AI confidence across all predictions made during this session.

    """)

    trend_df = history_df.copy()

    trend_df = trend_df.iloc[::-1].reset_index(drop=True)

    trend_df["Prediction No."] = trend_df.index + 1

    fig2 = px.line(

        trend_df,

        x="Prediction No.",

        y="Confidence(%)",

        markers=True

    )

    fig2.update_layout(

        height=350,

        xaxis_title="Prediction",

        yaxis_title="Confidence (%)",

        margin=dict(

            l=20,

            r=20,

            t=20,

            b=20

        )

    )

    st.plotly_chart(

        fig2,

        use_container_width=True,

        config={

            "displayModeBar":False

        }

    )

    history_df["Confidence(%)"] = history_df["Confidence(%)"].astype(float)

    styled_df = history_df.style.format({
        "Confidence (%)" : "{:.2f}%"

    }).background_gradient(

        subset=["Confidence(%)"],
        cmap="Greens"
    )

    st.markdown("""

    ## 📌 Session Insights

    Quick overview of the current prediction session.

    """)

    a1, a2, a3 = st.columns(3)

    with a1:

        st.info(
            f"🏆 Highest Confidence : {highest_confidence}%"
        )

    with a2:

        st.info(
            f"📉 Lowest Confidence : {lowest_confidence}%"
        )

    with a3:

        st.info(
            f"⚡ Average Processing Time : {average_time}s"
        )

    st.markdown("""

    ## 📋 Prediction History Table

    Complete record of all predictions generated during this session.

    """)

    st.dataframe(

        styled_df,
        use_container_width=True,
        hide_index=True

    )

    csv = history_df.to_csv(

        index=False

    ).encode("utf-8")

    st.download_button(

        label="📥 Export History",

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


def show_prediction_card(result):

    prediction = result["prediction"]
    confidence = result["confidence"]
    authenticity = result["authenticity_level"]

    if "REAL" in prediction:
        border = "#22c55e"
        bg = "linear-gradient(135deg,#052e16,#14532d)"
        icon = "✅"
    else:
        border = "#ef4444"
        bg = "linear-gradient(135deg,#450a0a,#7f1d1d)"
        icon = "❌"

    st.markdown(
        f"""
<div style="
background:{bg};
padding:30px;
border-radius:20px;
border-left:8px solid {border};
margin-top:15px;
margin-bottom:20px;
box-shadow:0 15px 35px rgba(0,0,0,.35);
">

<h2 style="margin:0;color:white;">
{icon} {prediction}
</h2>

<p style="
margin-top:8px;
font-size:18px;
color:#dbeafe;
">

AI successfully evaluated linguistic patterns, source credibility and confidence metrics.
</p>

<hr style="border:1px solid rgba(255,255,255,.12);margin:18px 0;">

<div style="
display:flex;
justify-content:space-between;
font-size:18px;
font-weight:600;
color:white;
">

<div>

🎯 Confidence

<br>

<span style="font-size:34px;font-weight:800;color:#60a5fa;">

{confidence}%

</span>

</div>

<div>

📰 Authenticity

<br>

<span style="font-size:24px;color:#4ade80;">

{authenticity}

</span>

</div>

</div>

</div>
""",
        unsafe_allow_html=True
    )

    st.progress(confidence / 100)

    st.caption(
        "🤖 Confidence is calculated using AI prediction certainty, source reliability and linguistic analysis."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🧠 Trust Score",
            f"{result['trust_score']}%"
        )

    with c2:
        st.metric(
            "🛡 Risk",
            result["risk_level"]
        )

    with c3:
        st.metric(
            "🌍 Publisher",
            result["publisher"]
        )

    with c4:
        st.metric(
            "⚡ Time",
            f"{result['processing_time']} sec"
        )



# About Tab

def about_tab():

    st.subheader("ℹ About This Project")

    st.markdown("""
    # 👨‍💻 Developer

    ### Shrine Pakhredia
    **B.Tech Artificial Intelligence & Machine Learning**

    Building intelligent AI applications using Machine Learning, NLP and modern Python technologies.

    ---
    """)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
    ### 🚀 Core Features

    ✅ Fake News Detection

    ✅ News URL Analysis

    ✅ Trusted Publisher Verification

    ✅ Source Reliability Score

    ✅ AI Trust Score

    ✅ Authenticity Score

    ✅ Keyword Extraction

    ✅ Prediction History

    ✅ CSV Export
    """)

    with col2:

        st.markdown("""
    ### 🛠 Tech Stack

    🐍 Python

    🤖 Scikit-Learn

    ⚡ Streamlit

    📊 Plotly

    📰 Newspaper3k

    📚 Pandas

    💾 Joblib

    🔤 TF-IDF

    🌲 Random Forest
    """)

    st.divider()

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric("📰 Dataset","44,898")

    with c2:
        st.metric("🧠 Features","5000")

    with c3:
        st.metric("🤖 Model","Random Forest")

    with c4:
        st.metric("⚡ Version","Pro")

    st.divider()

    st.success("🎯 Designed to help identify fake and misleading news articles using Artificial Intelligence and Natural Language Processing.")

    st.info("💡 This project combines Machine Learning predictions with source credibility analysis, AI trust scoring and authenticity evaluation to improve decision making.")



# Footer

def footer():

    st.divider()

    st.markdown(
        """
<div style="
text-align:center;
padding:20px;
color:#9ca3af;
font-size:15px;
">

📰 <b>AI Fake News Detection Pro</b>

<br><br>

Built with ❤️ using Python • Streamlit • Scikit-Learn • Plotly

<br><br>

© 2026 <b>Shrine Pakhredia</b>

</div>
""",
        unsafe_allow_html=True
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