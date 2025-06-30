import sqlite3
import streamlit as st
import requests
from urllib.parse import urlparse, parse_qs

st.set_page_config(page_title="🎓 Scholar Hub App", layout="wide")

# ------------------- CSS Styling -------------------
st.markdown("""
    <style>
    .main {
        background-color: #f7f9fc;
    }
    .card {
        background-color: #ffffff;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .card img {
        width: 100%;
        max-width: 340px;
        border-radius: 10px;
        object-fit: cover;
        margin-bottom: 0.5rem;
    }
    .rating {
        color: #f39c12;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Scholar Hub - Career Companion - Explore Your Future")

# ------------------- Connect DB -------------------
conn = sqlite3.connect("Scholar_Hub.db")
cursor = conn.cursor()

# ------------------- Fetch Levels -------------------
cursor.execute("SELECT id, level_name FROM levels")
levels = cursor.fetchall()
level_options = {name: id for id, name in levels}
selected_level = st.selectbox("🎓 Select Class Level", list(level_options.keys()))

# ------------------- Fetch Streams -------------------
cursor.execute("SELECT id, stream_name FROM streams")
streams = cursor.fetchall()
stream_options = {name: id for id, name in streams}
selected_stream = st.selectbox("🧭 Select Stream", ["None"] + list(stream_options.keys()))

# ------------------- Fetch Exams -------------------
level_id = level_options[selected_level]
stream_id = None if selected_stream == "None" else stream_options[selected_stream]

if stream_id is None:
    cursor.execute("SELECT id, exam_name FROM exams WHERE level_id = ? AND stream_id IS NULL", (level_id,))
else:
    cursor.execute("SELECT id, exam_name FROM exams WHERE level_id = ? AND stream_id = ?", (level_id, stream_id))

exams = cursor.fetchall()

if not exams:
    st.warning("No exams found for this combination.")
    st.stop()

exam_options = {exam[1]: exam[0] for exam in exams}
selected_exam = st.selectbox("🎯 Select Your Exam", list(exam_options.keys()))
exam_id = exam_options[selected_exam]

# ------------------- Fetch Resources -------------------
cursor.execute("""
SELECT subject, teacher_name, youtube_url, rating
FROM resources
WHERE exam_id = ?
""", (exam_id,))
resources = cursor.fetchall()

# ------------------- Channel Posters -------------------
channel_posters = {
    "Physics Wallah": "https://yt3.googleusercontent.com/ytc/AGIKgqMwK54FJAp1r9Fh2KnJ-4gslxO-LEArE2xT4T6Z=s176-c-k-c0x00ffffff-no-rj",
    "Vedantu JEE": "https://yt3.googleusercontent.com/ytc/AGIKgqMmsQ_Wq9pgKEUwYzU6L3qHckfH87qKrlfNu_t2=s176-c-k-c0x00ffffff-no-rj",
    "Unacademy Class 11 & 12": "https://yt3.googleusercontent.com/ytc/AGIKgqMqVrc7EzCDWBIVtu3H4IQlDeF0ivn6BFf3UI2d=s176-c-k-c0x00ffffff-no-rj",
    "Commerce Baba": "https://yt3.ggpht.com/ytc/AGIKgqP6G5pG2OGx1FJWceBt1lV2N3CEYlfTztn5VoVW=s176-c-k-c0x00ffffff-no-rj",
    "English Academy": "https://yt3.ggpht.com/ytc/AGIKgqO07zH0gEcdJ4o4UBfyb4S_AxhH6b4N7Kw0Ippf=s176-c-k-c0x00ffffff-no-rj",
}
fallback_poster = "https://www.iconpacks.net/icons/2/free-youtube-logo-icon-2431-thumb.png"

# ------------------- Helper Function -------------------
def extract_youtube_id(url):
    if "watch?v=" in url:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        return query.get("v", [None])[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    return None

# ------------------- Display -------------------
if resources:
    st.markdown(f"## 📚 Recommended Resources for **{selected_exam}**")
    cols = st.columns(3)  # Show 3 cards per row

    for idx, (subject, teacher, url, rating) in enumerate(resources):
        with cols[idx % 3]:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            if url.lower().endswith(".pdf"):
                st.image("https://upload.wikimedia.org/wikipedia/commons/8/87/PDF_file_icon.svg", width=120)
                st.markdown(f"**Subject:** {subject}")
                st.markdown(f"**Resource:** {teacher}")
                st.markdown("**Type:** 📄 Downloadable PDF")
                st.markdown(f"**Rating:** {'⭐' * rating}")
                
                try:
                    pdf_data = requests.get(url).content
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_data,
                        file_name="training_resources.pdf"
                    )
                except:
                    st.error("❌ Failed to load PDF.")

            else:
                youtube_id = extract_youtube_id(url)
                poster_url = (
                    f"https://img.youtube.com/vi/{youtube_id}/0.jpg"
                    if youtube_id else channel_posters.get(teacher, fallback_poster)
                )

                st.image(poster_url, use_column_width=True)
                st.markdown(f"**Subject:** {subject}")
                st.markdown(f"**Channel:** {teacher}")
                st.markdown(f"**Rating:** {'⭐' * rating}")
                st.link_button("▶️ Watch Now", url)

            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No resources available for this exam yet.")

conn.close()
