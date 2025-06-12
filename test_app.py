import pytest
import requests

# --- Fonction à tester
def make_prediction(data):
    API_PREDICT_URL = "https://mlsleepapi4-e6b7hhdzh0b9bjbt.francecentral-01.azurewebsites.net/predict"
    label_map = {
        0: "Insomnie",
        1: "Apnée du sommeil",
        2: "Aucun trouble détecté"
    }
    try:
        r = requests.post(API_PREDICT_URL, json=data)
        if r.status_code == 200:
            prediction = r.json().get("prediction")
            return label_map.get(prediction, "Inconnu")
        else:
            return f"Erreur {r.status_code}"
    except Exception as e:
        return f"Erreur API : {str(e)}"

# --- Tests
def test_make_prediction_valid(monkeypatch):
    class MockResponse:
        def __init__(self): self.status_code = 200
        def json(self): return {"prediction": 1}

    def mock_post(*args, **kwargs): return MockResponse()
    monkeypatch.setattr("requests.post", mock_post)

    sample_input = {
        "Gender": "Male",
        "Age": 30,
        "Occupation": "Employee",
        "Sleep_Duration": 7.0,
        "Quality_of_Sleep": 7,
        "Physical_Activity_Level": 5,
        "Stress_Level": 5,
        "BMI_Category": "Normal",
        "Blood_Pressure": "Normal",
        "Heart_Rate": 70,
        "Daily_Steps": 5000,
        "Systolic": 120,
        "Diastolic": 80
    }

    result = make_prediction(sample_input)
    assert result == "Apnée du sommeil"

def test_make_prediction_api_error(monkeypatch):
    def mock_post(*args, **kwargs): raise Exception("network error")
    monkeypatch.setattr("requests.post", mock_post)

    result = make_prediction({})
    assert "Erreur API" in result
