# Anomaly Detection API

## Opis projektu

Ten projekt implementuje serwis WWW do wykrywania anomalii w danych wejściowych przy użyciu modelu Isolation Forest. Serwis został napisany w Pythonie z użyciem Flask i umożliwia łatwe uruchomienie w kontenerze Docker.

## Funkcjonalności
- Obsługuje brakujące dane poprzez uzupełnianie średnimi wartościami.
- Standaryzuje dane wejściowe.
- Obsługuje elastyczną liczbę zmiennych wejściowych.
- Generuje predykcję oraz score anomalii.
- Zawiera endpoint do sprawdzania stanu serwisu.

## Struktura projektu
```
.
├── app.py                 # Główna aplikacja Flask
├── Dockerfile             # Plik konfiguracyjny Dockera
├── requirements.txt       # Lista wymaganych bibliotek
├── model.pkl              # Plik z zapisanym modelem ML (generowany automatycznie)
├── scaler.pkl             # Plik z zapisanym scalerem (generowany automatycznie)
└── README.md              # Dokumentacja projektu
```

## Uruchamianie aplikacji

### 1. Klonowanie repozytorium
```
git clone <URL_REPOZYTORIUM>
cd anomaly_detection_api
```

### 2. Budowanie obrazu Dockera
```
docker build -t anomaly-api .
```

### 3. Uruchamianie kontenera
```
docker run -p 5000:5000 anomaly-api
```

### 4. Testowanie API
- Sprawdzenie stanu serwisu:
```
curl http://localhost:5000/health
```
- Wysyłanie danych do analizy:
```
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '[{"feature1": 1.2, "feature2": 3.4, ..., "feature20": 5.6}]'
```

## Zależności
- Flask
- Numpy
- Pandas
- Scikit-learn
- Joblib

## Autor
Projekt przygotowany jako część zadania zaliczeniowego z przedmiotu Programowanie Aplikacji Webowych.
