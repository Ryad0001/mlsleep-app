import streamlit as st
import requests
import time

# --- URLs de l'API FastAPI
API_TRAIN_URL = "https://mlsleep-api.onrender.com/train"
API_PREDICT_URL = "https://mlsleep-api.onrender.com/predict"
API_STATUS_URL = "https://mlsleep-api.onrender.com/status"

# --- Mapping des classes prédictives
label_map = {
    0: "Insomnie",
    1: "Apnée du sommeil",
    2: "Aucun trouble détecté"
}

# --- Initialiser l'état du modèle
if "model_ready" not in st.session_state:
    st.session_state["model_ready"] = False

# --- Fonction pour vérifier l'état du modèle
def check_model_status():
    try:
        r = requests.get(API_STATUS_URL, verify=False)
        if r.status_code == 200:
            status = r.json().get("status")
            st.session_state["model_ready"] = (status == "ready")
        else:
            st.session_state["model_ready"] = False
    except:
        st.session_state["model_ready"] = False

# --- Appel initial pour savoir si le modèle est prêt
check_model_status()

# --- Interface Streamlit
st.title("💤 Prédiction des troubles du sommeil")

st.subheader("📝 Données utilisateur")

# Message d'avertissement si modèle non chargé
if not st.session_state["model_ready"]:
    st.warning("⚠️ Le modèle n'est pas encore chargé. Veuillez cliquer sur 'Réentraîner le modèle' ci-dessous avant de prédire.")

# Formulaire utilisateur
gender = st.selectbox("Genre", ["Male", "Female", "Other"])
age = st.slider("Âge", 10, 100, 25)
occupation = st.selectbox("Profession", ["Student", "Employee", "Self-employed", "Unemployed", "Other"])
sleep_duration = st.slider("Durée de sommeil (heures)", 0.0, 12.0, 7.0, step=0.5)
quality_of_sleep = st.slider("Qualité du sommeil (1 à 10)", 1, 10, 6)
physical_activity_level = st.slider("Activité physique (1 à 10)", 1, 10, 5)
stress_level = st.slider("Niveau de stress (1 à 10)", 1, 10, 5)
bmi_category = st.selectbox("Catégorie IMC", ["Normal", "Overweight", "Obese", "Underweight"])
blood_pressure = st.selectbox("Tension artérielle", ["Normal", "High", "Low"])
heart_rate = st.number_input("Fréquence cardiaque", 40, 150, 70)
daily_steps = st.number_input("Nombre de pas quotidiens", 0, 30000, 5000)
systolic = st.number_input("Tension systolique", 80, 200, 120)
diastolic = st.number_input("Tension diastolique", 40, 120, 80)

# --- Bouton de réentraînement du modèle
if st.button("🔁 Réentraîner le modèle maintenant"):
    with st.spinner("Entraînement en cours..."):
        try:
            r = requests.post(API_TRAIN_URL, verify=False)
            if r.status_code == 200:
                time.sleep(2)
                check_model_status()
                if st.session_state["model_ready"]:
                    st.success("✅ Modèle réentraîné et prêt.")
                else:
                    st.warning("Modèle entraîné mais pas encore prêt.")
            else:
                st.error(f"Erreur : {r.status_code} - {r.text}")
        except Exception as e:
            st.error(f"Erreur lors de l’appel à l’API : {e}")

# --- Bouton de prédiction
if st.button("🔮 Prédire"):
    if not st.session_state["model_ready"]:
        st.error("⛔ Le modèle n'est pas prêt. Veuillez l'entraîner avant de prédire.")
    else:
        data = {
            "Gender": gender,
            "Age": age,
            "Occupation": occupation,
            "Sleep_Duration": sleep_duration,
            "Quality_of_Sleep": quality_of_sleep,
            "Physical_Activity_Level": physical_activity_level,
            "Stress_Level": stress_level,
            "BMI_Category": bmi_category,
            "Blood_Pressure": blood_pressure,
            "Heart_Rate": heart_rate,
            "Daily_Steps": daily_steps,
            "Systolic": systolic,
            "Diastolic": diastolic
        }

        try:
            r = requests.post(API_PREDICT_URL, json=data, verify=False)
            if r.status_code == 200:
                prediction = r.json().get("prediction")
                label = label_map.get(prediction, "Inconnu")
                st.success(f"💤 Trouble prédit : {label}")
            else:
                st.error(f"Erreur {r.status_code} : {r.text}")
        except Exception as e:
            st.error(f"Erreur lors de la communication avec l’API : {e}")
