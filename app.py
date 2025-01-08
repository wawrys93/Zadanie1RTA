from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

# Model i scaler
MODEL_FILE = 'model.pkl'
SCALER_FILE = 'scaler.pkl'

# Załaduj model i scaler, jeśli istnieją
if os.path.exists(MODEL_FILE) and os.path.exists(SCALER_FILE):
    model = joblib.load(MODEL_FILE)
    scaler = joblib.load(SCALER_FILE)
else:
    # Tymczasowe dane do stworzenia modelu (np. dane losowe)
    np.random.seed(42)
    temp_data = np.random.rand(100, 20)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(temp_data)
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(scaled_data)

    # Zapisz model i scaler
    joblib.dump(model, MODEL_FILE)
    joblib.dump(scaler, SCALER_FILE)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Pobierz dane wejściowe w formacie JSON
        data = request.get_json()

        # Konwertuj dane na ramkę danych Pandas
        df = pd.DataFrame(data)

        # Obsługa brakujących danych - uzupełnij średnimi wartościami
        df.fillna(df.mean(), inplace=True)

        # Sprawdzenie liczby zmiennych i dostosowanie
        if df.shape[1] != scaler.n_features_in_:
            return jsonify({"error": "Nieprawidłowa liczba zmiennych. Oczekiwano {} kolumn.".format(scaler.n_features_in_)})

        # Standaryzacja danych wejściowych
        scaled_data = scaler.transform(df)

        # Przewidywanie anomalii
        predictions = model.predict(scaled_data)
        scores = model.decision_function(scaled_data)

        # Konwersja wyników na format JSON
        result = [{"prediction": int(pred), "score": float(score)} for pred, score in zip(predictions, scores)]

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
