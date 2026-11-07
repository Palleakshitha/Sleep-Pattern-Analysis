import streamlit as st
from datetime import time

import database
from prediction import predict_sleep
from recommendations import get_recommendations


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sleep Pattern Analysis",
    page_icon="😴",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .title {
        font-size: 38px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .card {
        padding: 20px;
        border-radius: 12px;
        background-color: #f5f7fa;
        border: 1px solid #e0e0e0;
        margin-bottom: 15px;
    }

    .result {
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        background-color: #f5f7fa;
        border: 2px solid #cccccc;
        margin: 20px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DATABASE
# =========================================================

database.create_database()


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""


# =========================================================
# LOGIN / REGISTER PAGE
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="title">😴 Sleep Pattern Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Health Prediction Outcome</div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(
        ["🔐 Login", "📝 Register"]
    )

    # -----------------------------------------------------
    # LOGIN
    # -----------------------------------------------------

    with tab1:

        st.subheader("Login")

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True,
            type="primary"
        ):

            if not email or not password:

                st.warning(
                    "Please enter both email and password."
                )

            else:

                user = database.login_user(
                    email,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user_name = user[1]
                    st.session_state.user_email = user[2]

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid Email or Password."
                    )

    # -----------------------------------------------------
    # REGISTER
    # -----------------------------------------------------

    with tab2:

        st.subheader("Create New Account")

        name = st.text_input(
            "Full Name",
            placeholder="Enter your name",
            key="register_name"
        )

        reg_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="register_email"
        )

        reg_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm your password",
            key="confirm_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if (
                not name
                or not reg_email
                or not reg_password
            ):

                st.warning(
                    "Please fill all fields."
                )

            elif reg_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(reg_password) < 6:

                st.warning(
                    "Password should contain at least 6 characters."
                )

            else:

                result = database.register_user(
                    name,
                    reg_email,
                    reg_password
                )

                if result:

                    st.success(
                        "Account created successfully. "
                        "Please login."
                    )

                else:

                    st.error(
                        "An account with this email already exists."
                    )

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title(
    "😴 Sleep Pattern Analysis"
)

st.sidebar.write(
    f"Welcome, **{st.session_state.user_name}**"
)

st.sidebar.write(
    st.session_state.user_email
)

st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "❤️ Health Data",
        "📜 Prediction History"
    ]
)

st.sidebar.divider()

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.user_email = ""

    st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.title(
        "🏠 Health Dashboard"
    )

    st.write(
        f"Welcome back, "
        f"**{st.session_state.user_name}**!"
    )

    st.info(
        "Enter your latest health and sleep information "
        "from the Health Data section to obtain a prediction."
    )

    history = database.get_history(
        st.session_state.user_email
    )

    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    if not history.empty:

        latest = history.iloc[0]

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Sleep Duration",
                f"{latest['sleep_duration']:.1f} hrs"
            )

        with col2:

            st.metric(
                "Heart Rate",
                f"{latest['heart_rate']:.0f} BPM"
            )
        with col3:

            st.metric(
                "Latest Prediction",
                str(latest["prediction"])
            )

        st.divider()

        st.subheader(
            "📊 Recent Prediction"
        )

        st.dataframe(
            history.head(10),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.subheader(
            "📊 Your Dashboard"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Sleep Duration",
                "--"
            )

        with col2:
            st.metric(
                "Heart Rate",
                "--"
            )

        with col3:
            st.metric(
                "Stress Level",
                "--"
            )

        with col4:
            st.metric(
                "Prediction",
                "--"
            )

        st.warning(
            "No prediction history available yet. "
            "Go to Health Data and enter your information."
        )

    st.divider()

    st.subheader(
        "📌 System Features"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            ### 🤖 ML Prediction

            Uses a trained Random Forest machine learning
            model to analyze sleep-related health data.
            """
        )

    with col2:

        st.markdown(
            """
            ### 🎯 Personalized Recommendations

            Analyzes the entered sleep, lifestyle and
            wearable measurements and generates
            prioritized recommendations.
            """
        )

    with col3:

        st.markdown(
            """
            ### 📜 History

            Stores previous predictions so users can
            monitor their sleep-related information.
            """
        )


# =========================================================
# HEALTH DATA
# =========================================================

elif menu == "❤️ Health Data":

    st.title(
        "❤️ Health Data Entry"
    )

    st.write(
        "Enter your health and lifestyle information below."
    )

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    st.subheader(
        "👤 Basic Information"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=100,
            value=25,
            step=1
        )

    with col2:

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ]
        )

    with col3:

        occupation = st.selectbox(
            "Occupation",
            [
                "Software Engineer",
                "Doctor",
                "Teacher",
                "Engineer",
                "Accountant",
                "Nurse",
                "Lawyer",
                "Manager",
                "Sales Representative",
                "Scientist",
                "Student",
                "Other"
            ]
        )

    # =====================================================
    # SLEEP INFORMATION
    # =====================================================

    st.subheader(
        "😴 Sleep Information"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        sleep_duration = st.number_input(
            "Sleep Duration (hours)",
            min_value=1.0,
            max_value=15.0,
            value=7.0,
            step=0.1
        )

    with col2:

        quality_sleep = st.number_input(
            "Quality of Sleep",
            min_value=1,
            max_value=10,
            value=7,
            step=1
        )

    with col3:

        sleep_efficiency = st.number_input(
            "Sleep Efficiency (%)",
            min_value=1.0,
            max_value=100.0,
            value=85.0,
            step=1.0
        )

    col1, col2 = st.columns(2)

    with col1:

        sleep_start = st.time_input(
            "Sleep Start Time",
            value=time(22, 30)
        )

    with col2:

        wake_up = st.time_input(
            "Wake-up Time",
            value=time(6, 30)
        )

    # =====================================================
    # ACTIVITY AND STRESS
    # =====================================================

    st.subheader(
        "🏃 Activity & Stress"
    )

    col1, col2 = st.columns(2)

    with col1:

        physical_activity = st.number_input(
            "Physical Activity Level (minutes/day)",
            min_value=0.0,
            max_value=300.0,
            value=30.0,
            step=1.0
        )

    with col2:

        daily_steps = st.number_input(
            "Daily Steps",
            min_value=0,
            max_value=50000,
            value=7000,
            step=500
        )

    exercise_type = st.selectbox(
        "Exercise Type",
        [
            "None",
            "Walking",
            "Running",
            "Cycling",
            "Gym",
            "Yoga",
            "Swimming",
            "Other"
        ]
    )

    # =====================================================
    # BODY INFORMATION
    # =====================================================

    st.subheader(
        "🩺 Body & Health Information"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        bmi = st.selectbox(
            "BMI Category",
            [
                "Normal",
                "Normal Weight",
                "Overweight",
                "Obese"
            ]
        )

    with col2:

        systolic_bp = st.number_input(
            "Systolic BP",
            min_value=70.0,
            max_value=250.0,
            value=120.0,
            step=1.0
        )

    with col3:

        diastolic_bp = st.number_input(
            "Diastolic BP",
            min_value=40.0,
            max_value=150.0,
            value=80.0,
            step=1.0
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        heart_rate = st.number_input(
            "Heart Rate (BPM)",
            min_value=30.0,
            max_value=220.0,
            value=72.0,
            step=1.0
        )

    with col2:

        spo2 = st.number_input(
            "SpO2 (%)",
            min_value=50.0,
            max_value=100.0,
            value=98.0,
            step=1.0
        )

    with col3:

        body_temperature = st.number_input(
            "Body Temperature (°C)",
            min_value=30.0,
            max_value=45.0,
            value=36.5,
            step=0.1
        )

    # =====================================================
    # LIFESTYLE INFORMATION
    # =====================================================

    st.subheader(
        "🍎 Lifestyle Information"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        water_intake = st.number_input(
            "Water Intake (L/day)",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.1
        )

    with col2:

        screen_time = st.number_input(
            "Screen Time Before Sleep (hrs)",
            min_value=0.0,
            max_value=12.0,
            value=2.0,
            step=0.5
        )

    with col3:

        caffeine = st.number_input(
            "Caffeine Intake (cups/day)",
            min_value=0.0,
            max_value=20.0,
            value=1.0,
            step=1.0
        )

    col1, col2 = st.columns(2)

    with col1:

        alcohol = st.selectbox(
            "Alcohol Consumption",
            [
                "No",
                "Yes"
            ]
        )

    with col2:

        smoking = st.selectbox(
            "Smoking",
            [
                "No",
                "Yes"
            ]
        )

    # =====================================================
    # SENSOR DATA
    # =====================================================

    st.subheader(
        "⌚ Wearable Sensor Data"
    )

    col1, col2 = st.columns(2)

    with col1:

        hrv = st.number_input(
            "HRV (ms)",
            min_value=0.0,
            max_value=300.0,
            value=50.0,
            step=1.0
        )

    with col2:

        respiratory_rate = st.number_input(
            "Respiratory Rate",
            min_value=5.0,
            max_value=40.0,
            value=16.0,
            step=1.0
        )

    # =====================================================
    # PREDICT BUTTON
    # =====================================================

    st.divider()

    predict_button = st.button(
        "🔮 Predict Sleep Condition",
        use_container_width=True,
        type="primary"
    )

    # =====================================================
    # PREDICTION
    # =====================================================

    if predict_button:

        # -------------------------------------------------
        # CREATE INPUT DATA
        # -------------------------------------------------

        input_data = {

            "Gender": gender,

            "Age": age,

            "Occupation": occupation,

            "Sleep Duration": sleep_duration,

            "Quality of Sleep": quality_sleep,

            "Physical Activity Level": physical_activity,

            "BMI Category": bmi,

            "Systolic BP": systolic_bp,

            "Diastolic BP": diastolic_bp,

            "Heart Rate": heart_rate,

            "Daily Steps": daily_steps,

            "Water Intake (L/day)": water_intake,

            "Screen Time Before Sleep (hrs)": screen_time,

            "Caffeine Intake (cups/day)": caffeine,

            "Alcohol Consumption": alcohol,

            "Smoking": smoking,

            "Sleep Start Time": str(sleep_start),

            "Wake-up Time": str(wake_up),

            "Sleep Efficiency (%)": sleep_efficiency,

            "SpO2 (%)": spo2,

            "Body Temperature (°C)": body_temperature,

            "HRV (ms)": hrv,

            "Respiratory Rate": respiratory_rate,

            "Exercise Type": exercise_type
        }

        try:

            # =================================================
            # MODEL PREDICTION
            # =================================================

            with st.spinner(
                "Analyzing your sleep and health data..."
            ):

                prediction, confidence = predict_sleep(
                    input_data
                )

            # -------------------------------------------------
            # CONVERT MODEL OUTPUT
            # -------------------------------------------------

            prediction_text = str(prediction)

            if prediction_text == "0":

                display_prediction = (
                    "No Sleep Disorder Detected"
                )

            elif prediction_text == "1":

                display_prediction = (
                    "Sleep Disorder Detected"
                )

            else:

                display_prediction = prediction_text

            # =================================================
            # PREDICTION RESULT
            # =================================================

            st.success(
                "Prediction completed successfully!"
            )

            st.markdown(
                '<div class="result">',
                unsafe_allow_html=True
            )

            st.subheader(
                "🤖 Prediction Result"
            )

            st.markdown(
                f"## {display_prediction}"
            )

            if confidence > 0:

                st.progress(
                    min(confidence / 100, 1.0)
                )

                st.write(
                    f"Prediction Confidence: "
                    f"**{confidence:.2f}%**"
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            # =================================================
            # HEALTH STATUS
            # =================================================

            st.subheader(
                "🩺 General Health Status"
            )

            health_score = 0

            if 7 <= sleep_duration <= 9:
                health_score += 1

            if physical_activity >= 30:
                health_score += 1

            if daily_steps >= 7000:
                health_score += 1

            if 95 <= spo2 <= 100:
                health_score += 1

            if 60 <= heart_rate <= 100:
                health_score += 1

            if health_score >= 5:

                health_status = (
                    "Generally Healthy Indicators"
                )

            elif health_score >= 3:

                health_status = (
                    "Needs Attention"
                )

            else:

                health_status = (
                    "Needs Lifestyle Improvement"
                )

            st.info(
                f"Health Status: **{health_status}**"
            )

            # =================================================
            # PERSONALIZED RECOMMENDATIONS
            # =================================================

            st.subheader(
                "🎯 Personalized Recommendations"
            )

            recommendations = get_recommendations(
                input_data,
                prediction
            )

            for recommendation in recommendations:

                st.markdown(
                    f"### 💡 "
                    f"{recommendation['category']}"
                )

                st.info(
                    recommendation["message"]
                )

            # =================================================
            # SAVE HISTORY
            # =================================================

            database.save_history(
                st.session_state.user_email,
                display_prediction,
                sleep_duration,
                heart_rate,
                
            )

            st.success(
                "Prediction has been saved to your history."
            )

            st.caption(
                "Note: This system provides a "
                "machine-learning-based prediction and "
                "general health information. It is not "
                "a medical diagnosis."
            )

        except Exception as e:

            st.error(
                "Prediction could not be completed."
            )

            st.exception(e)


# =========================================================
# PREDICTION HISTORY
# =========================================================

elif menu == "📜 Prediction History":

    st.title(
        "📜 Prediction History"
    )

    history = database.get_history(
        st.session_state.user_email
    )

    if history.empty:

        st.info(
            "No prediction history available yet."
        )

    else:

        st.subheader(
            "Previous Predictions"
        )

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader(
            "📈 History Summary"
        )

        col1, col2 = st.columns(3)

        with col1:

            st.metric(
                "Total Predictions",
                len(history)
            )

        with col2:

            avg_sleep = history[
                "sleep_duration"
            ].mean()

            st.metric(
                "Average Sleep",
                f"{avg_sleep:.1f} hrs"
            )

        
        st.divider()

        st.subheader(
            "😴 Sleep Trend"
        )

        if len(history) > 1:

            chart_data = history[
                [
                    "sleep_duration",
                    "heart_rate",
                    
                ]
            ].copy()

            chart_data = chart_data.iloc[::-1]

            st.line_chart(
                chart_data
            )

        else:

            st.info(
                "More prediction records are needed "
                "to display trends."
            )