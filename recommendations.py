def get_recommendations(data, prediction):

    recommendations = []

    # --------------------------------------------------
    # USER DATA
    # --------------------------------------------------

    sleep_duration = float(data.get("Sleep Duration", 0))
    sleep_quality = float(data.get("Quality of Sleep", 0))
    sleep_efficiency = float(data.get("Sleep Efficiency (%)", 0))

    stress_level = float(data.get("Stress Level", 0))
    physical_activity = float(
        data.get("Physical Activity Level", 0)
    )
    daily_steps = float(data.get("Daily Steps", 0))

    screen_time = float(
        data.get("Screen Time Before Sleep (hrs)", 0)
    )

    caffeine = float(
        data.get("Caffeine Intake (cups/day)", 0)
    )

    water = float(
        data.get("Water Intake (L/day)", 0)
    )

    heart_rate = float(
        data.get("Heart Rate", 0)
    )

    spo2 = float(
        data.get("SpO2 (%)", 0)
    )

    hrv = float(
        data.get("HRV (ms)", 0)
    )

    respiratory_rate = float(
        data.get("Respiratory Rate", 0)
    )

    alcohol = str(
        data.get("Alcohol Consumption", "No")
    )

    smoking = str(
        data.get("Smoking", "No")
    )

    exercise_type = str(
        data.get("Exercise Type", "None")
    )

    bmi = str(
        data.get("BMI Category", "")
    )

    # --------------------------------------------------
    # PRIORITY LIST
    # --------------------------------------------------

    priority = []

    # --------------------------------------------------
    # SLEEP DURATION
    # --------------------------------------------------

    if sleep_duration < 6:

        priority.append((
            5,
            "Sleep Duration",
            f"You reported only {sleep_duration:.1f} hours "
            "of sleep. This is one of the main areas requiring "
            "attention. Try maintaining a consistent bedtime and "
            "wake-up schedule and allow enough time for sleep."
        ))

    elif sleep_duration < 7:

        priority.append((
            4,
            "Sleep Duration",
            f"You reported {sleep_duration:.1f} hours of sleep. "
            "Try gradually increasing your sleep opportunity and "
            "maintaining a regular sleep schedule."
        ))

    elif sleep_duration > 10:

        priority.append((
            2,
            "Sleep Duration",
            f"You reported {sleep_duration:.1f} hours of sleep. "
            "If this pattern is persistent and you still feel tired, "
            "consider discussing it with a healthcare professional."
        ))

    # --------------------------------------------------
    # SLEEP QUALITY
    # --------------------------------------------------

    if sleep_quality <= 4:

        priority.append((
            5,
            "Sleep Quality",
            f"Your sleep quality score is {sleep_quality:.0f}/10. "
            "Focus on a consistent bedtime routine, a comfortable "
            "sleep environment, and reducing stimulating activities "
            "before sleep."
        ))

    elif sleep_quality <= 6:

        priority.append((
            3,
            "Sleep Quality",
            f"Your sleep quality score is {sleep_quality:.0f}/10. "
            "Improving your bedtime routine and reducing distractions "
            "before sleep may help support better sleep quality."
        ))

    # --------------------------------------------------
    # SLEEP EFFICIENCY
    # --------------------------------------------------

    if sleep_efficiency < 70:

        priority.append((
            5,
            "Sleep Efficiency",
            f"Your sleep efficiency is {sleep_efficiency:.0f}%. "
            "Try maintaining consistent sleep and wake times and "
            "keeping your sleep environment comfortable."
        ))

    elif sleep_efficiency < 85:

        priority.append((
            3,
            "Sleep Efficiency",
            f"Your sleep efficiency is {sleep_efficiency:.0f}%. "
            "A consistent sleep schedule and relaxing bedtime routine "
            "may help improve sleep regularity."
        ))

    # --------------------------------------------------
    # STRESS
    # --------------------------------------------------

    if stress_level >= 8:

        priority.append((
            5,
            "Stress",
            f"Your stress level is {stress_level:.0f}/10. "
            "Stress appears to be an important area to address. "
            "Consider relaxation activities, breathing exercises, "
            "and reducing stimulating activities before bedtime."
        ))

    elif stress_level >= 6:

        priority.append((
            3,
            "Stress",
            f"Your stress level is {stress_level:.0f}/10. "
            "Consider adding regular relaxation activities and "
            "maintaining a consistent sleep routine."
        ))

    # --------------------------------------------------
    # PHYSICAL ACTIVITY
    # --------------------------------------------------

    if physical_activity < 15:

        priority.append((
            4,
            "Physical Activity",
            f"You reported {physical_activity:.0f} minutes/day "
            "of physical activity. Consider gradually adding "
            "regular movement during the day according to your ability."
        ))

    elif physical_activity < 30:

        priority.append((
            3,
            "Physical Activity",
            f"You reported {physical_activity:.0f} minutes/day "
            "of physical activity. Gradually increasing daily "
            "movement may support overall health and sleep."
        ))

    # --------------------------------------------------
    # DAILY STEPS
    # --------------------------------------------------

    if daily_steps < 4000:

        priority.append((
            4,
            "Daily Movement",
            f"You reported approximately {daily_steps:.0f} steps/day. "
            "Try increasing your daily movement gradually through "
            "walking or another activity you enjoy."
        ))

    elif daily_steps < 7000:

        priority.append((
            2,
            "Daily Movement",
            f"You reported approximately {daily_steps:.0f} steps/day. "
            "Consider gradually increasing your daily movement."
        ))

    # --------------------------------------------------
    # SCREEN TIME
    # --------------------------------------------------

    if screen_time >= 4:

        priority.append((
            4,
            "Screen Time",
            f"You reported {screen_time:.1f} hours of screen time "
            "before sleep. Consider reducing stimulating screen "
            "activities close to bedtime."
        ))

    elif screen_time >= 2:

        priority.append((
            2,
            "Screen Time",
            f"You reported {screen_time:.1f} hours of screen time "
            "before sleep. Consider reducing screen use as bedtime "
            "approaches."
        ))

    # --------------------------------------------------
    # CAFFEINE
    # --------------------------------------------------

    if caffeine >= 4:

        priority.append((
            4,
            "Caffeine",
            f"You reported {caffeine:.0f} cups of caffeine per day. "
            "Consider reducing caffeine intake, particularly later "
            "in the day."
        ))

    elif caffeine >= 2:

        priority.append((
            2,
            "Caffeine",
            f"You reported {caffeine:.0f} cups of caffeine per day. "
            "Consider avoiding caffeine close to bedtime."
        ))

    # --------------------------------------------------
    # WATER
    # --------------------------------------------------

    if water < 1:

        priority.append((
            2,
            "Hydration",
            f"You reported {water:.1f} L/day of water intake. "
            "Make sure you drink enough fluids throughout the day "
            "according to your individual needs."
        ))

    # --------------------------------------------------
    # ALCOHOL
    # --------------------------------------------------

    if alcohol.lower() == "yes":

        priority.append((
            3,
            "Alcohol",
            "Alcohol can interfere with sleep quality. "
            "Consider avoiding alcohol close to bedtime."
        ))

    # --------------------------------------------------
    # SMOKING
    # --------------------------------------------------

    if smoking.lower() == "yes":

        priority.append((
            3,
            "Smoking",
            "Smoking can affect overall health and sleep. "
            "Consider discussing cessation support with a "
            "healthcare professional."
        ))

    # --------------------------------------------------
    # EXERCISE TYPE
    # --------------------------------------------------

    if exercise_type == "None" and physical_activity < 30:

        priority.append((
            3,
            "Exercise",
            "No regular exercise activity was reported. "
            "Consider gradually introducing an activity such as "
            "walking, cycling, swimming, or yoga."
        ))

    # --------------------------------------------------
    # BMI
    # --------------------------------------------------

    if bmi.lower() in ["overweight", "obese"]:

        priority.append((
            1,
            "Lifestyle",
            "Focus on regular physical activity, balanced nutrition, "
            "and consistent sleep habits. Avoid extreme dieting or "
            "restrictive eating."
        ))

    # --------------------------------------------------
    # HEART RATE
    # --------------------------------------------------

    if heart_rate > 100:

        priority.append((
            3,
            "Heart Rate",
            f"Your recorded heart rate is {heart_rate:.0f} BPM. "
            "If this occurs repeatedly while resting or you have "
            "concerning symptoms, discuss it with a healthcare "
            "professional."
        ))

    elif heart_rate < 50:

        priority.append((
            3,
            "Heart Rate",
            f"Your recorded heart rate is {heart_rate:.0f} BPM. "
            "If this is unusual for you or occurs with symptoms, "
            "consider discussing it with a healthcare professional."
        ))

    # --------------------------------------------------
    # SpO2
    # --------------------------------------------------

    if spo2 < 92:

        priority.append((
            5,
            "SpO2",
            f"Your recorded SpO₂ is {spo2:.0f}%. "
            "Because this is a health-related measurement, "
            "a persistently unusual reading should be checked "
            "with a healthcare professional."
        ))

    elif spo2 < 95:

        priority.append((
            3,
            "SpO2",
            f"Your recorded SpO₂ is {spo2:.0f}%. "
            "If readings remain unusual or you experience symptoms, "
            "discuss them with a healthcare professional."
        ))

    # --------------------------------------------------
    # RESPIRATORY RATE
    # --------------------------------------------------

    if respiratory_rate < 10 or respiratory_rate > 25:

        priority.append((
            3,
            "Respiratory Rate",
            f"Your recorded respiratory rate is "
            f"{respiratory_rate:.0f} breaths/min. "
            "If this pattern is persistent or unusual for you, "
            "consider discussing it with a healthcare professional."
        ))

    # --------------------------------------------------
    # HRV
    # --------------------------------------------------

    if 0 < hrv < 25:

        priority.append((
            2,
            "HRV",
            f"Your recorded HRV is {hrv:.0f} ms. "
            "HRV varies considerably between individuals, so "
            "trends over time are generally more useful than "
            "a single reading."
        ))

    # --------------------------------------------------
    # MODEL PREDICTION
    # --------------------------------------------------

    prediction_text = str(prediction).lower()

    if prediction_text in [
        "1",
        "sleep disorder detected",
        "insomnia",
        "sleep apnea"
    ]:

        priority.append((
            5,
            "Sleep Prediction",
            "The machine-learning model identified a possible "
            "sleep-related issue based on the provided data. "
            "This is not a medical diagnosis. If sleep problems "
            "persist, consider discussing them with a healthcare "
            "professional."
        ))

    # --------------------------------------------------
    # SORT BY PRIORITY
    # --------------------------------------------------

    priority.sort(
        key=lambda item: item[0],
        reverse=True
    )

    # --------------------------------------------------
    # RETURN TOP 6
    # --------------------------------------------------

    for _, category, message in priority[:6]:

        recommendations.append({
            "category": category,
            "message": message
        })

    # --------------------------------------------------
    # DEFAULT
    # --------------------------------------------------

    if not recommendations:

        recommendations.append({
            "category": "Overall",
            "message":
                "Your current inputs do not indicate a major "
                "recommendation area. Continue maintaining regular "
                "sleep, physical activity, and healthy daily habits."
        })

    return recommendations