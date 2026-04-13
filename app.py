import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import os

# ---------------- INIT ----------------
if not os.path.exists("users.csv"):
    pd.DataFrame(columns=["username","password"]).to_csv("users.csv", index=False)

if not os.path.exists("data.csv"):
    pd.DataFrame(columns=["username","Name","Technical","Communication","Confidence","Result"]).to_csv("data.csv", index=False)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""

# ---------------- UI ----------------
st.set_page_config(page_title="AI Interview Assistant", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color:white;
}
.card {
    background: rgba(255,255,255,0.08);
    padding:40px;
    border-radius:20px;
    width:420px;
    margin:auto;
}
.stButton>button {
    background: linear-gradient(to right,#ff7b00,#ff3d00);
    color:white;
    border-radius:10px;
    height:3em;
    width:100%;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:

    st.markdown("<h1 style='text-align:center;'>🎯 AI Interview Assistant</h1>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    option = st.radio("", ["Login","Register"], horizontal=True)
    users = pd.read_csv("users.csv")

    if option == "Login":
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            if not users[(users['username']==user) & (users['password']==pwd)].empty:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):
            users = pd.concat([users, pd.DataFrame([{"username":new_user,"password":new_pass}])])
            users.to_csv("users.csv", index=False)
            st.success("Registered!")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---------------- MAIN ----------------
data = pd.read_csv("data.csv")

st.sidebar.title(f"👤 {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

page = st.sidebar.radio("", ["Dashboard","Prediction","Interview","History","Add Candidate"])

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("📊 Dashboard")

    user_data = data[data['username'] == st.session_state.user]
    st.dataframe(user_data)

    if not user_data.empty:
        avg = user_data[['Technical','Communication','Confidence']].mean()
        fig, ax = plt.subplots(figsize=(4,2))
        avg.plot(kind='bar', ax=ax)
        st.pyplot(fig)

# ---------------- PREDICTION ----------------
elif page == "Prediction":
    st.title("🤖 Prediction")

    X = data[['Technical','Communication','Confidence']]
    y = data['Result']

    model = RandomForestClassifier()
    model.fit(X,y)

    tech = st.slider("Technical",0,10,5)
    comm = st.slider("Communication",0,10,5)
    conf = st.slider("Confidence",0,10,5)

    if st.button("Predict"):
        result = model.predict([[tech,comm,conf]])[0]

        if result == "Selected":
            st.success("Selected ✅")
        else:
            st.error("Rejected ❌")

# ---------------- INTERVIEW (AI ASSISTANT) ----------------
elif page == "Interview":

    st.title("🎥 AI Interview Assistant + English Trainer")

    role = st.selectbox("Select Role", ["HR","Technical"])

    if role == "HR":
        questions = ["Tell me about yourself","What are your strengths?","Why should we hire you?"]
    else:
        questions = ["Explain Python","What is API?","What is OOP?"]

    if "q_index" not in st.session_state:
        st.session_state.q_index = 0

    if "answers" not in st.session_state:
        st.session_state.answers = []

    st.camera_input("📷 Camera ON")

    # -------- AI ASSISTANT --------
    st.markdown("## 🤖 AI Assistant")

    if st.button("📌 Explain Question"):
        st.info("Understand the question clearly and answer step-by-step.")

    if st.button("💬 Answer Structure"):
        st.success("Intro → Points → Example → Conclusion")

    if st.button("🧠 Smart Tip"):
        st.warning("Always include examples!")

    # -------- ENGLISH TRAINER --------
    st.markdown("## 📘 English Trainer")

    if st.button("🔤 Improve English"):
        st.info("Use simple grammar, speak clearly, avoid mistakes.")

    if st.button("💬 Sentence Starters"):
        st.success("I believe that... | From my experience... | In my opinion...")

    if st.button("✨ Make it Professional"):
        st.write("I know Python ➡️ I have strong knowledge in Python")

    # -------- INTERVIEW --------
    if st.session_state.q_index < len(questions):

        q = questions[st.session_state.q_index]
        st.subheader(q)

        if st.button("💡 Hint"):
            st.info("Start simple and explain clearly")

        if st.button("😰 I'm Stuck"):
            st.warning("Relax! Say what you know 💪")

        ans = st.text_area("Your Answer")
        st.audio_input("🎤 Speak")

        # CONFIDENCE SCORE
        confidence = min(len(ans.split()) * 2, 100)
        st.progress(confidence)
        st.write(f"Confidence Score: {confidence}%")

        if st.button("Next"):
            st.session_state.answers.append(ans)
            st.session_state.q_index += 1
            st.rerun()

    else:
        st.success("🎉 Interview Completed")

        total = sum(len(a.split()) for a in st.session_state.answers)

        st.markdown("## 📊 Final Feedback")

        if total > 50:
            st.success("Excellent 🔥")
        else:
            st.warning("Practice more 😅")

        if st.button("Restart"):
            st.session_state.q_index = 0
            st.session_state.answers = []
            st.rerun()

# ---------------- HISTORY ----------------
elif page == "History":
    st.title("📜 Interview History")
    user_data = data[data['username'] == st.session_state.user]
    st.dataframe(user_data)

# ---------------- ADD ----------------
elif page == "Add Candidate":

    st.title("➕ Add Candidate")

    name = st.text_input("Name")
    tech = st.slider("Technical",0,10,5)
    comm = st.slider("Communication",0,10,5)
    conf = st.slider("Confidence",0,10,5)

    if st.button("Add"):
        new = {
            "username": st.session_state.user,
            "Name": name,
            "Technical": tech,
            "Communication": comm,
            "Confidence": conf,
            "Result": "Pending"
        }

        data = pd.concat([data,pd.DataFrame([new])])
        data.to_csv("data.csv", index=False)

        st.success("Added ✅")