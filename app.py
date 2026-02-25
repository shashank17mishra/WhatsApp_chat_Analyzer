import streamlit as st
import preprocessor as ps
import helper as h
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="WhatsApp Chat Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 WhatsApp Chat Analytics Dashboard")
st.markdown("---")

# -------------------------------------------------------
# SIDEBAR CONTROLS
# -------------------------------------------------------
st.sidebar.header("⚙ Controls")

uploaded_file = st.sidebar.file_uploader("Upload WhatsApp Chat (.txt)")

dark_mode = st.sidebar.toggle("🌙 Dark Mode")

template = "plotly_dark" if dark_mode else "plotly_white"

# -------------------------------------------------------
# PDF GENERATION FUNCTION
# -------------------------------------------------------
def generate_pdf(stats, selected_user):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(f"WhatsApp Analytics Report - {selected_user}", styles["Title"]))
    elements.append(Spacer(1, 0.5 * inch))

    data = [
        ["Metric", "Value"],
        ["Total Messages", stats[0]],
        ["Total Words", stats[1]],
        ["Media Shared", stats[2]],
        ["Links Shared", stats[3]],
    ]

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer


# -------------------------------------------------------
# MAIN LOGIC
# -------------------------------------------------------
if uploaded_file is not None:

    data = uploaded_file.getvalue().decode("utf-8")
    df = ps.preprocess(data)

    user_list = df["Sender"].unique().tolist()
    if "group_notification" in user_list:
        user_list.remove("group_notification")

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Select User", user_list)

    if st.sidebar.button("Generate Analysis"):

        # =====================================================
        # 1️⃣ OVERVIEW
        # =====================================================
        st.subheader("📌 Overview")

        stats = h.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Messages", stats[0])
        col2.metric("Total Words", stats[1])
        col3.metric("Media Shared", stats[2])
        col4.metric("Links Shared", stats[3])

        pdf = generate_pdf(stats, selected_user)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf,
            file_name="chat_analysis_report.pdf",
            mime="application/pdf"
        )

        st.markdown("---")

        # =====================================================
        # 2️⃣ MESSAGE TRENDS
        # =====================================================
        st.subheader("📈 Message Trends")

        col1, col2 = st.columns(2)

        with col1:
            timeline = h.m_a_month(selected_user, df)
            fig = px.line(timeline, x="time", y="Message", markers=True)
            fig.update_layout(template=template, title="Monthly Activity", title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            daily = h.daily_timeline(selected_user, df)
            fig = px.line(daily, x="date_", y="Message", markers=True)
            fig.update_layout(template=template, title="Daily Activity", title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # =====================================================
        # 3️⃣ ANIMATED MONTHLY GROWTH
        # =====================================================
        st.subheader("🎞 Monthly Chat")

        anim_data = h.monthly_animation(selected_user, df)

        fig = px.bar(
            anim_data,
            x="Month",
            y="Message",
            animation_frame="Year",
            color="Message",
            color_continuous_scale="Blues"
        )
        fig.update_layout(template=template, title="Monthly Evolution", title_x=1.0)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # =====================================================
        # 4️⃣ GROUP ANALYSIS
        # =====================================================
        if selected_user == "Overall":
            st.subheader("👥 Group Engagement")

            name, count = h.most_busy_sender(df)

            fig = px.bar(
                x=name,
                y=count,
                color=count,
                color_continuous_scale="Blues"
            )
            fig.update_layout(template=template, title="Most Active Users", title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(h.msg_sender_p(df), use_container_width=True)

        st.markdown("---")

        # =====================================================
        # 5️⃣ TEXT ANALYSIS
        # =====================================================
        st.subheader("📝 Text Insights")

        col1, col2 = st.columns(2)

        with col1:
            wc = h.cr_wordcloud(selected_user, df)
            if wc:
                st.image(wc.to_array(), use_container_width=True)

        with col2:
            common_words = h.word_counter(selected_user, df)
            fig = px.bar(
                common_words,
                x="Frequency",
                y="Word",
                orientation="h"
            )
            fig.update_layout(template=template, yaxis=dict(autorange="reversed"),
                              title="Most Common Words", title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # =====================================================
        # 6️⃣ EMOJI ANALYSIS
        # =====================================================
        st.subheader("😂 Emoji Insights")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(h.emoji_f(selected_user, df), use_container_width=True)

        with col2:
            fig = h.emoji_plotly_chart(selected_user, df)
            if fig:
                fig.update_layout(template=template)
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # =====================================================
        # 7️⃣ ACTIVITY HEATMAP
        # =====================================================
        st.subheader("🔥 Activity Heatmap (Day vs Hour)")

        heatmap_data = h.activity_heatmap(selected_user, df)

        fig = px.imshow(
            heatmap_data,
            aspect="auto",
            color_continuous_scale="Viridis"
        )
        fig.update_layout(template=template, title="Chat Intensity", title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # =====================================================
        # 8️⃣ ACTIVITY PATTERNS
        # =====================================================
        st.subheader("📅 Activity Patterns")

        col1, col2 = st.columns(2)

        with col1:
            day_data = h.most_active_day(selected_user, df)
            fig = px.bar(day_data, x="Day", y="Message", color="Message")
            fig.update_layout(template=template, title="Most Active Day", title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            month_data = h.most_active_month(selected_user, df)
            fig = px.bar(month_data, x="month", y="Message", color="Message")
            fig.update_layout(template=template, title="Most Active Month", title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("😊 Sentiment Analysis")

        sent_df, sent_counts = h.sentiment_analysis(selected_user, df)

        col1, col2 = st.columns(2)

        # Pie Chart
        with col1:
            fig = px.pie(
                sent_counts,
                names="Sentiment",
                values="Count",
                title="Sentiment Distribution",
                color="Sentiment",
                color_discrete_map={
                    "Positive": "green",
                    "Negative": "red",
                    "Neutral": "gray"
                }
            )
            fig.update_layout(template=template, title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)

        # Bar Chart
        with col2:
            fig = px.bar(
                sent_counts,
                x="Sentiment",
                y="Count",
                color="Sentiment"
            )
            fig.update_layout(template=template, title="Sentiment Count", title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("📊 Sentiment Over Time")

        timeline = h.sentiment_timeline(selected_user, df)

        fig = px.line(
            timeline,
            x="date_only",
            y="Count",
            color="Sentiment_Label",
            markers=True
        )

        fig.update_layout(template=template, title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)