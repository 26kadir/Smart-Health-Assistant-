from flask import (
    Flask, render_template, render_template_string,
    request, session, redirect, url_for
)
from datetime import datetime

app = Flask(__name__)
app.secret_key = "smart-health-assistant-secret-key"

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


def make_result(assessment, risk, message, warning):
    return {
        "assessment": assessment,
        "risk": risk,
        "message": message,
        "warning": warning
    }


def analyze_symptoms(symptoms, temperature="", duration=""):
    text = symptoms.lower()
    def has(*words):
        return any(word in text for word in words)

    fever = has("fever", "bukhar")
    cough = has("cough", "khansi")
    sore_throat = has("sore throat", "gale mein dard")
    runny_nose = has("runny nose", "cold", "naak behna")
    headache = has("headache", "sir dard")
    vomiting = has("vomiting", "ulti")
    diarrhea = has("diarrhea", "loose motion")
    stomach_pain = has("stomach pain", "abdominal pain", "pet dard")
    body_pain = has("body pain", "body ache", "badan dard")
    fatigue = has("fatigue", "weakness", "thakan")
    dizziness = has("dizziness", "chakkar")
    joint_pain = has("joint pain", "joint ache")
    swelling = has("swelling", "sujan")
    frequent_urination = has("frequent urination", "bar bar urine")
    excessive_thirst = has("excessive thirst", "zyada pyas")
    increased_hunger = has("increased hunger", "zyada bhook")
    blurred_vision = has("blurred vision", "dhundhla dikhna")
    burning_urination = has("burning urination", "urine burning")
    back_pain = has("back pain", "kamar dard")
    skin_rash = has("skin rash", "rash", "daane")
    itching = has("itching", "khujli")

    chest_pain = has("chest pain", "seene mein dard")
    breathing = has(
        "breathing difficulty",
        "difficulty breathing",
        "saans lene mein dikkat"
    )
    confusion = has("confusion", "behoshi", "fainting")
    severe_bleeding = has("severe bleeding", "heavy bleeding")
    severe_pain = has("severe pain", "bahut tez dard")

    # Check temperature
    try:
        temp_value = float(temperature) if temperature else None

        if temp_value is not None:
            if temp_value > 45 and temp_value >= 100.4:
                fever = True
            elif temp_value <= 45 and temp_value >= 38:
                fever = True
    except (ValueError, TypeError):
        temp_value = None

    # Emergency symptoms
    if (
        breathing or chest_pain or confusion
        or severe_bleeding or severe_pain
    ):
        return make_result(
            "Urgent Medical Attention Recommended",
            "High Priority",
            "Some reported symptoms may require urgent medical evaluation. "
            "Please seek emergency medical help.",
            "Do not delay medical care, especially if symptoms are severe "
            "or getting worse."
        )

    # Flu-like symptoms
    if fever and cough and body_pain and fatigue:
        return make_result(
            "Flu-Like Symptoms",
            "Moderate Priority",
            "Fever, cough, body pain and fatigue can occur with influenza "
            "and other infections. A healthcare professional may recommend "
            "testing if needed.",
            "Watch for breathing difficulty, chest pain or worsening fever."
        )

    if fever and cough and sore_throat:
        return make_result(
            "Respiratory Illness-Like Symptoms",
            "Moderate Priority",
            "Fever, cough and sore throat can occur with respiratory "
            "infections. A clinician may recommend testing if needed.",
            "Seek medical advice if fever persists or symptoms worsen."
        )

    if cough and runny_nose and not fever:
        return make_result(
            "Common Cold-Like Symptoms",
            "Low Priority",
            "Cough and runny nose may occur with a common cold or other "
            "respiratory conditions.",
            "Consult a doctor if symptoms persist or become severe."
        )

    # Blood sugar-related symptoms
    if frequent_urination and excessive_thirst and increased_hunger:
        return make_result(
            "Possible Blood Sugar Concern",
            "Moderate Priority",
            "Frequent urination, excessive thirst and increased hunger "
            "can be associated with high blood sugar. A blood glucose "
            "test and medical evaluation may be useful.",
            "This is not a diabetes diagnosis. Please consult a doctor."
        )

    if frequent_urination and excessive_thirst:
        return make_result(
            "Blood Sugar-Related Symptoms",
            "Moderate Priority",
            "These symptoms can have several causes, including blood "
            "sugar changes. Medical evaluation may be helpful.",
            "Consider discussing a blood glucose test with a doctor."
        )

    if blurred_vision and frequent_urination:
        return make_result(
            "Symptoms Requiring Blood Sugar Evaluation",
            "Moderate Priority",
            "Blurred vision with frequent urination can have different "
            "causes and should be medically evaluated.",
            "Arrange a medical check-up, especially if symptoms are new."
        )
    # Joint and urinary symptoms
    if joint_pain and swelling:
        return make_result(
            "Joint Inflammation-Like Symptoms",
            "Moderate Priority",
            "Joint pain with swelling may have several causes, including "
            "inflammation or gout. A clinician can decide whether tests "
            "such as uric acid measurement are appropriate.",
            "Do not self-diagnose gout based on symptoms alone."
        )

    if burning_urination and frequent_urination:
        return make_result(
            "Urinary Tract Infection-Like Symptoms",
            "Moderate Priority",
            "Burning and frequent urination can occur with a urinary "
            "tract infection. A urine test may be considered.",
            "Consult a healthcare professional for proper evaluation."
        )

    if back_pain and burning_urination:
        return make_result(
            "Urinary Symptoms with Back Pain",
            "Moderate Priority",
            "Urinary burning with back pain needs medical assessment. "
            "A kidney or urinary condition may need to be ruled out.",
            "Seek prompt medical advice, particularly with fever or chills."
        )

    # Skin symptoms
    if skin_rash and itching:
        return make_result(
            "Skin Irritation or Allergy-Like Symptoms",
            "Low Priority",
            "Rash and itching may occur with allergies, irritation or "
            "skin conditions.",
            "Seek medical advice if the rash spreads, becomes painful "
            "or is associated with swelling or breathing difficulty."
        )

    # Digestive symptoms
    if vomiting and diarrhea:
        return make_result(
            "Digestive Illness-Like Symptoms",
            "Moderate Priority",
            "Vomiting and diarrhea can cause dehydration. Small frequent "
            "sips of fluids may help while arranging care if needed.",
            "Seek urgent care for severe dehydration, blood in stool "
            "or inability to keep fluids down."
        )

    if stomach_pain and vomiting:
        return make_result(
            "Abdominal Symptoms Requiring Evaluation",
            "Moderate Priority",
            "Abdominal pain with vomiting can have multiple causes. "
            "A clinician should assess persistent or severe symptoms.",
            "Seek urgent care if pain is severe or worsening."
        )

    if stomach_pain:
        return make_result(
            "Abdominal Pain",
            "Low Priority",
            "Abdominal pain can have many possible causes. Its location, "
            "duration and severity are important for evaluation.",
            "Seek medical help for severe or persistent pain."
        )

    if headache and vomiting:
        return make_result(
            "Headache with Vomiting",
            "Moderate Priority",
            "Headache with vomiting may need medical assessment, "
            "especially if it is sudden or severe.",
            "Seek urgent care for sudden severe headache, confusion "
            "or vision changes."
        )

    if headache:
        return make_result(
            "Headache",
            "Low Priority",
            "Headaches can be related to several factors, including "
            "sleep, dehydration or other medical conditions.",
            "Seek medical advice if headaches are frequent or severe."
        )

    if diarrhea:
        return make_result(
            "Diarrhea",
            "Moderate Priority",
            "Diarrhea can lead to fluid loss. Maintain hydration "
            "and monitor symptoms.",
            "Seek care for blood in stool, dehydration or persistent symptoms."
        )

    if vomiting:
        return make_result(
            "Vomiting",
            "Moderate Priority",
            "Vomiting can have several causes. Monitor hydration "
            "and seek medical advice if it continues.",
            "Seek urgent care if you cannot keep fluids down."
        )

    if back_pain and joint_pain:
        return make_result(
            "Musculoskeletal Pain",
            "Low Priority",
            "Back and joint pain may be associated with muscle strain "
            "or other musculoskeletal conditions.",
            "Consult a doctor if pain persists or limits movement."
        )

    if body_pain and fatigue:
        return make_result(
            "Body Pain and Fatigue",
            "Low Priority",
            "These symptoms can occur due to several causes, including "
            "infections, poor sleep or physical strain.",
            "Seek medical advice if symptoms persist or worsen."
        )

    if dizziness:
        return make_result(
            "Dizziness",
            "Moderate Priority",
            "Dizziness can have different causes. Sit or lie down "
            "if you feel unsteady.",
            "Seek urgent care if dizziness occurs with chest pain, "
            "fainting or weakness."
        )

    if fever:
        extra = ""
        if duration:
            extra = " Reported duration: " + duration + "."

        return make_result(
            "Fever",
            "Moderate Priority",
            "Fever can occur with many infections and other conditions. "
            "Rest, drink fluids and monitor your temperature." + extra,
            "Consult a doctor if fever persists, rises or is accompanied "
            "by concerning symptoms."
        )

    if fatigue:
        return make_result(
            "Fatigue or Weakness",
            "Low Priority",
            "Fatigue may have several causes, including sleep issues, "
            "stress or medical conditions.",
            "Seek medical advice if it continues or affects daily activities."
        )

    if cough:
        return make_result(
            "Cough",
            "Low Priority",
            "Cough can occur due to infections, allergies or irritation.",
            "Seek care if you develop breathing difficulty or chest pain."
        )

    if sore_throat:
        return make_result(
            "Sore Throat",
            "Low Priority",
            "A sore throat can occur with respiratory infections "
            "or irritation.",
            "Consult a doctor if symptoms are severe or persistent."
        )

    if runny_nose:
        return make_result(
            "Runny Nose",
            "Low Priority",
            "A runny nose may occur with a cold or allergies.",
            "Seek advice if symptoms persist or worsen."
        )

    return make_result(
        "General Health Assessment",
        "Low Priority",
        "The selected symptoms do not match a specific pattern in "
        "this basic screening system.",
        "This tool cannot diagnose diseases. Consult a healthcare "
        "professional for an accurate assessment."
    )
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
@app.route("/check", methods=["POST"])
def check_symptoms():

    patient_name = request.form.get("patient_name", "").strip()
    gender = request.form.get("gender", "").strip()
    age_group = request.form.get("age_group", "").strip()
    pattern = request.form.get("pattern", "").strip()

    symptom_list = request.form.getlist("symptom_list")
    symptoms = ", ".join(symptom_list)

    temperature = request.form.get("temperature", "").strip()
    duration = request.form.get("duration", "").strip()

    if not symptoms and not temperature:
        result = make_result(
            "No Information Provided",
            "Not Available",
            "Please enter at least one symptom or your temperature.",
            "No assessment was performed."
        )

        result["patient_name"] = patient_name
        result["gender"] = gender
        result["age_group"] = age_group
        result["temperature"] = temperature
        result["duration"] = duration
        result["pattern"] = pattern
        result["symptoms"] = []

        return render_template(
            "result.html",
            symptoms="Not provided",
            result=result,
            assessment=result["assessment"],
            risk=result["risk"],
            message=result["message"],
            warning=result["warning"],
            temperature=temperature,
            duration=duration
        )

    if not symptoms and temperature:
        symptoms = "Fever"

    result = analyze_symptoms(symptoms, temperature, duration)

    result["patient_name"] = patient_name
    result["gender"] = gender
    result["age_group"] = age_group
    result["temperature"] = temperature
    result["duration"] = duration
    result["pattern"] = pattern
    result["symptoms"] = symptom_list

    records = session.get("history", [])

    records.insert(0, {
        "symptoms": symptoms,
        "assessment": result["assessment"],
        "risk": result["risk"],
        "date": datetime.now().strftime("%d-%m-%Y %I:%M %p")
    })

    session["history"] = records[:20]

    return render_template(
        "result.html",
        symptoms=symptoms,
        result=result,
        assessment=result["assessment"],
        risk=result["risk"],
        message=result["message"],
        warning=result["warning"],
        temperature=temperature,
        duration=duration
    )
@app.route("/history")
def history():
    records = session.get("history", [])
    return render_template("history.html", records=records)


@app.route("/clear-history", methods=["GET", "POST"])
def clear_history():
    session["history"] = []
    return render_template("history.html", records=[])
# Delete Individual History Record
@app.route("/delete-history/<int:index>", methods=["POST"])
def delete_history(index):
    records = session.get("history", [])

    if 0 <= index < len(records):
        records.pop(index)
        session["history"] = records

    return render_template("history.html", records=records)

@app.route("/dashboard")
def dashboard():
    records = session.get("history", [])

    total = len(records)

    high_priority = sum(
        1 for item in records
        if item.get("risk") == "High Priority"
    )

    moderate = sum(
        1 for item in records
        if item.get("risk") == "Moderate Priority"
    )

    return render_template(
        "dashboard.html",
        records=records,
        total=total,
        high_priority=high_priority,
        moderate=moderate
    )


# Doctor appointment route
@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    if request.method == "POST":
        patient_name = request.form.get("patient_name", "").strip()
        phone = request.form.get("phone", "").strip()
        doctor = request.form.get("doctor", "").strip()
        appointment_date = request.form.get("appointment_date", "").strip()
        appointment_time = request.form.get("appointment_time", "").strip()
        reason = request.form.get("reason", "").strip()
        if not all([
            patient_name, phone, doctor,
            appointment_date, appointment_time
        ]):
            return render_template_string(
                APPOINTMENT_PAGE,
                message="Please fill in all required fields.",
                success=False
            )

        appointments_list = session.get("appointments", [])

        appointments_list.insert(0, {
            "patient_name": patient_name,
            "phone": phone,
            "doctor": doctor,
            "appointment_date": appointment_date,
            "appointment_time": appointment_time,
            "reason": reason,
            "submitted_at": datetime.now().strftime("%d-%m-%Y %I:%M %p")
        })

        session["appointments"] = appointments_list[:20]

        return render_template_string(
            APPOINTMENT_PAGE,
            message="Appointment request saved successfully.",
            success=True
        )

    return render_template_string(
        APPOINTMENT_PAGE,
        message="",
        success=False
    )


@app.route("/appointment-history")
def appointment_history():
    appointments_list = session.get("appointments", [])

    return render_template_string(
        APPOINTMENT_HISTORY_PAGE,
        appointments=appointments_list
    )
# Appointment form
APPOINTMENT_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Doctor Appointment | Smart Health Assistant</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            margin: 0;
            padding: 25px;
        }

        .container {
            max-width: 650px;
            margin: 30px auto;
            background: white;
            padding: 28px;
            border-radius: 14px;
            box-shadow: 0 4px 18px #0001;
        }

        h1 {
            color: #087f8c;
        }

        label {
            display: block;
            margin-top: 15px;
            font-weight: bold;
        }

        input, select, textarea {
            width: 100%;
            box-sizing: border-box;
            padding: 12px;
            margin-top: 7px;
            border: 1px solid #ccd5df;
            border-radius: 7px;
        }

        button {
            margin-top: 20px;
            padding: 13px 22px;
            background: #087f8c;
            color: white;
            border: 0;
            border-radius: 7px;
            cursor: pointer;
        }

        a {
            color: #087f8c;
        }

        .message {
            padding: 12px;
            background: #e8f7ee;
            border-radius: 7px;
        }

        .error {
            background: #fff0f0;
        }
    </style>
</head>

<body>
<div class="container">

    <h1>Doctor Appointment</h1>
    <p>Submit an appointment request using the form below.</p>

    {% if message %}
        <p class="message {% if not success %}error{% endif %}">
            {{ message }}
        </p>
    {% endif %}

    <form method="POST" action="{{ url_for('appointments') }}">

        <label>Patient Name *</label>
        <input type="text" name="patient_name" required>

        <label>Phone Number *</label>
        <input type="tel" name="phone" required>

        <label>Select Doctor / Department *</label>
        <select name="doctor" required>
            <option value="">Choose a department</option>
            <option value="General Physician">General Physician</option>
            <option value="Cardiologist">Cardiologist</option>
            <option value="Dermatologist">Dermatologist</option>
            <option value="Orthopedic">Orthopedic</option>
            <option value="ENT Specialist">ENT Specialist</option>
            <option value="Other">Other</option>
        </select>

        <label>Appointment Date *</label>
        <input type="date" name="appointment_date" required>

        <label>Preferred Time *</label>
        <input type="time" name="appointment_time" required>

        <label>Reason for Appointment</label>
        <textarea name="reason" rows="4"
                  placeholder="Describe your concern"></textarea>

        <button type="submit">Submit Request</button>

    </form>

    <p>
        <a href="{{ url_for('appointment_history') }}">
            View Appointment Requests
        </a>
    </p>

    <p>
        <a href="{{ url_for('home') }}">Back to Home</a>
    </p>

</div>
</body>
</html>
"""


# Appointment history page
APPOINTMENT_HISTORY_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appointment History</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            padding: 25px;
        }

        .container {
            max-width: 800px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 12px;
        }

        .record {
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin: 12px 0;
        }

        a {
            color: #087f8c;
        }
    </style>
</head>

<body>
<div class="container">

    <h1>Appointment Requests</h1>

    {% if appointments %}

        {% for item in appointments %}

            <div class="record">
                <h3>{{ item.patient_name }}</h3>

                <p><b>Phone:</b> {{ item.phone }}</p>
                <p><b>Department:</b> {{ item.doctor }}</p>
                <p><b>Date:</b> {{ item.appointment_date }}</p>
                <p><b>Time:</b> {{ item.appointment_time }}</p>
                <p><b>Reason:</b> {{ item.reason or "Not provided" }}</p>
                <p><b>Submitted:</b> {{ item.submitted_at }}</p>
            </div>

        {% endfor %}

    {% else %}

        <p>No appointment requests have been submitted yet.</p>

    {% endif %}

    <p>
        <a href="{{ url_for('appointments') }}">New Appointment</a>
    </p>

    <p>
        <a href="{{ url_for('home') }}">Back to Home</a>
    </p>

</div>
</body>
</html>
"""


# Start Flask application
if __name__ == "__main__":
    app.run(debug=True)
