from flask import Flask, render_template, request, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "smart-health-assistant-secret-key"


def analyze_symptoms(symptoms):

    text = symptoms.lower()

    fever = any(x in text for x in [
        "fever", "high fever", "temperature", "high temperature"
    ])

    cough = any(x in text for x in [
        "cough", "coughing"
    ])

    sore_throat = any(x in text for x in [
        "sore throat", "throat pain", "throat hurts",
        "pain in throat"
    ])

    runny_nose = any(x in text for x in [
        "runny nose", "running nose", "blocked nose",
        "stuffy nose", "nasal congestion"
    ])

    headache = any(x in text for x in [
        "headache", "head pain"
    ])

    vomiting = any(x in text for x in [
        "vomiting", "vomit", "throwing up"
    ])

    diarrhea = any(x in text for x in [
        "diarrhea", "loose motion", "loose motions"
    ])

    stomach_pain = any(x in text for x in [
        "stomach pain", "abdominal pain",
        "belly pain", "abdomen pain"
    ])

    body_pain = any(x in text for x in [
        "body pain", "body ache",
        "muscle pain", "muscle ache"
    ])

    fatigue = any(x in text for x in [
        "fatigue", "tired", "tiredness",
        "weakness", "weak", "low energy"
    ])

    dizziness = any(x in text for x in [
        "dizziness", "dizzy",
        "light headed", "lightheaded"
    ])

    joint_pain = any(x in text for x in [
        "joint pain", "joint ache",
        "pain in joints"
    ])

    swelling = any(x in text for x in [
        "swelling", "swollen"
    ])

    frequent_urination = any(x in text for x in [
        "frequent urination",
        "urinating frequently",
        "pee frequently",
        "peeing frequently"
    ])

    excessive_thirst = any(x in text for x in [
        "excessive thirst",
        "very thirsty",
        "too much thirst",
        "thirsty all the time"
    ])

    increased_hunger = any(x in text for x in [
        "increased hunger",
        "very hungry",
        "excessive hunger"
    ])

    blurred_vision = any(x in text for x in [
        "blurred vision",
        "blurry vision",
        "vision is blurry"
    ])

    burning_urination = any(x in text for x in [
        "burning urination",
        "burning while urinating",
        "painful urination",
        "pain while urinating"
    ])

    back_pain = any(x in text for x in [
        "back pain",
        "lower back pain",
        "back ache"
    ])

    skin_rash = any(x in text for x in [
        "skin rash", "rash", "skin irritation"
    ])

    itching = any(x in text for x in [
        "itching", "itchy skin", "itchy"
    ])

    chest_pain = any(x in text for x in [
        "chest pain",
        "chest pressure",
        "pressure in chest",
        "chest tightness"
    ])

    breathing = any(x in text for x in [
        "difficulty breathing",
        "breathing difficulty",
        "shortness of breath",
        "breathlessness",
        "can't breathe",
        "cannot breathe"
    ])

    confusion = any(x in text for x in [
        "confusion",
        "confused",
        "fainting",
        "unconscious",
        "passed out"
    ])

    severe_bleeding = any(x in text for x in [
        "severe bleeding",
        "heavy bleeding",
        "blood vomiting",
        "vomiting blood",
        "blood in stool"
    ])

    severe_pain = any(x in text for x in [
        "severe pain",
        "very severe pain",
        "unbearable pain",
        "extreme pain"
    ])

    # 1. EMERGENCY

    if breathing or chest_pain or confusion or severe_bleeding or severe_pain:
        return {
            "assessment": "Urgent Medical Attention Recommended",
            "risk": "High Priority",
            "message": (
                "Some symptoms may require prompt medical assessment. "
                "This application cannot diagnose the cause."
            ),
            "warning": (
                "If symptoms are severe, sudden, rapidly worsening, "
                "or you feel unsafe, seek emergency medical care immediately."
            )
        }

    # 2. RESPIRATORY INFECTION

    if fever and cough and sore_throat:
        return {
            "assessment": "Respiratory Infection Symptoms",
            "risk": "Moderate",
            "message": (
                "Fever, cough and sore throat may occur with several "
                "respiratory illnesses."
            ),
            "warning": (
                "Seek medical advice if symptoms worsen, persist, "
                "or breathing difficulty develops."
            )
        }

    # 3. FLU-LIKE ILLNESS

    if fever and cough and body_pain and fatigue:
        return {
            "assessment": "Flu-Like Illness Pattern",
            "risk": "Moderate",
            "message": (
                "Fever, cough, body aches and fatigue can occur "
                "with several viral illnesses."
            ),
            "warning": (
                "Seek medical advice if symptoms become severe "
                "or persistent."
            )
        }

    # 4. COMMON COLD

    if runny_nose and sore_throat and cough:
        return {
            "assessment": "Common Cold / Upper Respiratory Symptoms",
            "risk": "Low to Moderate",
            "message": (
                "Runny nose, sore throat and cough commonly occur "
                "with upper respiratory illnesses."
            ),
            "warning": (
                "Monitor symptoms and seek medical advice if they "
                "become severe or persistent."
            )
        }

    # 5. DIABETES SCREENING

    if frequent_urination and excessive_thirst and increased_hunger:
        return {
            "assessment": "Diabetes-Related Symptoms - Screening Suggested",
            "risk": "Needs Medical Evaluation",
            "message": (
                "Frequent urination, excessive thirst and increased "
                "hunger can occur with diabetes, but symptoms alone "
                "cannot establish a diagnosis."
            ),
            "warning": (
                "Discuss these symptoms with a healthcare professional. "
                "Blood glucose testing may be appropriate."
            )
        }

    # 6. POSSIBLE BLOOD SUGAR PROBLEM

    if frequent_urination and excessive_thirst:
        return {
            "assessment": "Possible Blood Sugar Related Symptoms",
            "risk": "Needs Medical Evaluation",
            "message": (
                "Frequent urination and excessive thirst can have "
                "several causes, including blood sugar problems."
            ),
            "warning": (
                "Consider professional medical evaluation "
                "and appropriate blood glucose testing."
            )
        }

    # 7. VISION SCREENING

    if blurred_vision and frequent_urination:
        return {
            "assessment": "Vision and Urination Symptoms",
            "risk": "Needs Medical Evaluation",
            "message": (
                "Blurred vision and frequent urination can have "
                "several possible causes."
            ),
            "warning": (
                "Professional medical evaluation and appropriate "
                "testing may be needed."
            )
        }

    # 8. URIC ACID / GOUT SCREENING

    if joint_pain and swelling:
        return {
            "assessment": "Joint Pain and Swelling - Gout/Uric Acid Screening",
            "risk": "Needs Medical Evaluation",
            "message": (
                "Joint pain and swelling can occur with gout and "
                "other joint conditions. Symptoms cannot confirm "
                "high uric acid."
            ),
            "warning": (
                "A healthcare professional may recommend examination "
                "and blood testing such as serum uric acid."
            )
        }

    # 9. UTI SCREENING

    if burning_urination and frequent_urination:
        return {
            "assessment": "Urinary Tract Symptoms - UTI Screening",
            "risk": "Needs Medical Evaluation",
            "message": (
                "Burning and frequent urination can occur with "
                "urinary tract infections and other urinary conditions."
            ),
            "warning": (
                "A healthcare professional may recommend urine testing."
            )
        }

    # 10. SKIN / ALLERGY

    if skin_rash and itching:
        return {
            "assessment": "Skin Rash / Allergy-Like Symptoms",
            "risk": "Needs Monitoring",
            "message": (
                "A rash with itching can occur with allergies, "
                "irritation, infections and other skin conditions."
            ),
            "warning": (
                "Seek urgent medical attention if rash is accompanied "
                "by breathing difficulty or facial/throat swelling."
            )
        }

    # 11. GASTROINTESTINAL

    if vomiting and diarrhea:
        return {
            "assessment": "Gastrointestinal Symptoms",
            "risk": "Moderate",
            "message": (
                "Vomiting and diarrhea can cause fluid loss and "
                "may occur with digestive illnesses."
            ),
            "warning": (
                "Maintain hydration and seek medical advice if "
                "symptoms are severe."
            )
        }

    # 12. ABDOMINAL SYMPTOMS

    if stomach_pain and vomiting:
        return {
            "assessment": "Abdominal Symptoms with Vomiting",
            "risk": "Needs Medical Evaluation",
            "message": (
                "Abdominal pain with vomiting has many possible causes."
            ),
            "warning": (
                "Seek medical assessment if pain is severe, persistent, "
                "worsening, or associated with fever or bleeding."
            )
        }

    if stomach_pain:
        return {
            "assessment": "Abdominal Symptoms",
            "risk": "Needs Monitoring",
            "message": (
                "Abdominal pain can have many different causes. "
                "This application cannot determine the underlying cause."
            ),
            "warning": (
                "Seek medical assessment if pain is severe, sudden, "
                "persistent or worsening."
            )
        }

    # 13. HEADACHE

    if headache and vomiting:
        return {
            "assessment": "Headache with Vomiting",
            "risk": "Needs Medical Evaluation",
            "message": (
                "Headache accompanied by vomiting can have several "
                "possible causes."
            ),
            "warning": (
                "Seek prompt medical assessment if headache is sudden "
                "or severe."
            )
        }

    if headache:
        return {
            "assessment": "Headache",
            "risk": "Needs Monitoring",
            "message": (
                "Headaches can have many possible causes including "
                "dehydration, stress, poor sleep and illness."
            ),
            "warning": (
                "Seek medical care for a sudden severe or rapidly "
                "worsening headache."
            )
        }

    # 14. DIARRHEA

    if diarrhea:
        return {
            "assessment": "Diarrhea / Digestive Symptoms",
            "risk": "Moderate",
            "message": (
                "Diarrhea has several possible causes and may lead "
                "to dehydration."
            ),
            "warning": (
                "Maintain hydration and seek medical advice if "
                "symptoms are severe or persistent."
            )
        }

    # 15. VOMITING

    if vomiting:
        return {
            "assessment": "Vomiting",
            "risk": "Moderate",
            "message": (
                "Vomiting can occur with infections, digestive "
                "problems and other conditions."
            ),
            "warning": (
                "Seek medical advice if vomiting is persistent "
                "or fluids cannot be kept down."
            )
        }

    # 16. BACK / JOINT

    if back_pain and joint_pain:
        return {
            "assessment": "Musculoskeletal Symptoms",
            "risk": "Needs Monitoring",
            "message": (
                "Back and joint pain can have many causes including "
                "strain, posture-related problems and other conditions."
            ),
            "warning": (
                "Seek evaluation if pain is severe, persistent, "
                "or associated with weakness or numbness."
            )
        }

    # 17. BODY PAIN

    if body_pain and fatigue:
        return {
            "assessment": "General Body Symptoms",
            "risk": "Needs Monitoring",
            "message": (
                "Body aches and fatigue can occur with infections, "
                "dehydration, poor sleep, exertion and other conditions."
            ),
            "warning": (
                "Consult a healthcare professional if symptoms "
                "are severe or persistent."
            )
        }

    # 18. DIZZINESS

    if dizziness:
        return {
            "assessment": "Dizziness",
            "risk": "Needs Monitoring",
            "message": (
                "Dizziness can occur with dehydration, low blood "
                "pressure, illness and other conditions."
            ),
            "warning": (
                "Seek medical attention if dizziness is severe "
                "or associated with fainting or confusion."
            )
        }

    # 19. FATIGUE

    if fatigue:
        return {
            "assessment": "Fatigue / Weakness",
            "risk": "Needs Monitoring",
            "message": (
                "Fatigue or weakness can have many possible causes."
            ),
            "warning": (
                "Consult a healthcare professional if weakness "
                "is severe, persistent or worsening."
            )
        }

    # 20. FEVER

    if fever:
        return {
            "assessment": "Fever",
            "risk": "Needs Monitoring",
            "message": (
                "Fever can occur with infections and several "
                "other conditions."
            ),
            "warning": (
                "Seek medical advice if fever is persistent, very high, "
                "worsening, or accompanied by serious symptoms."
            )
        }

    # 21. COUGH

    if cough:
        return {
            "assessment": "Cough",
            "risk": "Needs Monitoring",
            "message": (
                "Cough can occur with infections, allergies, "
                "irritation and other conditions."
            ),
            "warning": (
                "Seek medical advice if cough becomes severe, "
                "persists, or breathing difficulty develops."
            )
        }

    # 22. SORE THROAT

    if sore_throat:
        return {
            "assessment": "Sore Throat",
            "risk": "Low to Moderate",
            "message": (
                "Sore throat can occur with respiratory infections, "
                "irritation and other conditions."
            ),
            "warning": (
                "Seek medical advice if symptoms are severe, persistent, "
                "or associated with difficulty breathing or swallowing."
            )
        }

    # 23. RUNNY NOSE

    if runny_nose:
        return {
            "assessment": "Nasal Symptoms",
            "risk": "Low",
            "message": (
                "Runny or blocked nose can occur with respiratory "
                "illnesses or allergies."
            ),
            "warning": (
                "Consult a healthcare professional if symptoms "
                "persist or become severe."
            )
        }

    # DEFAULT

    return {
        "assessment": "General Symptom Review",
        "risk": "Unable to Determine",
        "message": (
            "The symptoms entered do not match a specific screening "
            "pattern available in this prototype."
        ),
        "warning": (
            "Symptoms alone cannot establish a medical diagnosis. "
            "Consult a qualified healthcare professional if concerned."
        )
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check_symptoms():

    symptoms = request.form.get("symptoms", "").strip()

    if not symptoms:
        result = {
            "assessment": "No Symptoms Entered",
            "risk": "Not Assessed",
            "message": "Please enter at least one symptom to continue.",
            "warning": "No health assessment was performed."
        }

    else:
        result = analyze_symptoms(symptoms)

        history = session.get("history", [])

        history.insert(0, {
            "symptoms": symptoms,
            "assessment": result["assessment"],
            "risk": result["risk"],
            "date": datetime.now().strftime("%d-%m-%Y %I:%M %p")
        })

        session["history"] = history[:20]
        session.modified = True

    return render_template(
        "result.html",
        symptoms=symptoms,
        assessment=result["assessment"],
        risk=result["risk"],
        message=result["message"],
        warning=result["warning"]
    )


@app.route("/history")
def history():

    records = session.get("history", [])

    return render_template(
        "history.html",
        records=records
    )


@app.route("/clear-history")
def clear_history():

    session.pop("history", None)

    return render_template(
        "history.html",
        records=[]
    )


@app.route("/dashboard")
def dashboard():

    records = session.get("history", [])

    total = len(records)

    high_priority = sum(
        1 for record in records
        if record.get("risk") == "High Priority"
    )

    moderate = sum(
        1 for record in records
        if "Moderate" in record.get("risk", "")
    )

    return render_template(
        "dashboard.html",
        records=records,
        total=total,
        high_priority=high_priority,
        moderate=moderate
    )


if __name__ == "__main__":
    app.run(debug=True)