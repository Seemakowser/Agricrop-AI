\# 🌱 CropCare AI — Intelligent Plant Disease Detection \& Agricultural Advisory



CropCare AI is an AI-powered agricultural assistance platform that combines \*\*plant disease classification, crop advisory, and weather-based recommendations\*\* in a single web application.



Users can upload a plant image, select their crop and farm location, and receive an AI-generated plant health assessment along with practical agricultural recommendations.



\---



\## ✨ Features



\### 🌿 Plant Disease Detection



\- Deep-learning image classification using MobileNetV2

\- 38 PlantVillage disease/healthy classes

\- Top-3 model predictions with confidence scores



\### 🩺 Plant Health Assessment



\- Disease/status classification

\- Severity assessment

\- Spread-risk assessment

\- Recommended action



\### 💊 Agricultural Recommendations



\- Treatment guidance

\- Fertilizer recommendations

\- Watering guidance

\- Disease-prevention suggestions



\### 🌤 Weather-Based Advisory



\- OpenWeather API integration

\- Current temperature and humidity

\- Weather-aware farming recommendations



\### 🌾 Crop Advisory



\- Growing season

\- Soil requirements

\- Water requirements

\- Approximate harvest period



\### 📊 Analysis Dashboard



\- AI confidence score

\- Detected crop

\- Disease status

\- Severity and spread risk

\- Alternative predictions



\### 📄 PDF Reports



\- Downloadable AI analysis report



\### 📜 Analysis History



\- Keeps recent analyses during the current session



\### ⚠️ Model Limitation Awareness



\- Communicates that field conditions and plant damage outside the training distribution may not be reliably classified.



\---



\## 🧠 Machine Learning



The disease classifier was trained using the \*\*PlantVillage dataset\*\* and transfer learning with \*\*MobileNetV2\*\*.



\### Model Configuration



| Parameter | Value |

|---|---|

| Architecture | MobileNetV2 |

| Input Size | 224 × 224 |

| Classes | 38 |

| Transfer Learning | ImageNet |

| Data Augmentation | Yes |

| Validation Split | 20% |

| Training Epochs | 10 |

| Training Accuracy | 94.54% |

| Validation Accuracy | 94.32% |



The trained model is stored in:



```text

models/plant\_disease\_model.keras

```



Class labels are stored in:



```text

models/class\_names.txt

```



\### Supported Crops



The model supports disease and healthy classes across:



\- Apple

\- Blueberry

\- Cherry

\- Corn (maize)

\- Grape

\- Orange

\- Peach

\- Pepper

\- Potato

\- Raspberry

\- Soybean

\- Squash

\- Strawberry

\- Tomato



\---



\## 🏗 System Architecture



```text

&#x20;                   ┌──────────────────────┐

&#x20;                   │      User Image      │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │   React Frontend     │

&#x20;                   │     CropCare AI       │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              │ HTTP / multipart

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │     FastAPI API      │

&#x20;                   │       /predict       │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │    MobileNetV2       │

&#x20;                   │    38-Class Model    │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Disease + Confidence │

&#x20;                   │ Severity + Advisory  │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                ┌─────────────┴─────────────┐

&#x20;                ▼                           ▼

&#x20;      ┌──────────────────┐        ┌──────────────────┐

&#x20;      │ Crop Advisory    │        │ OpenWeather API  │

&#x20;      └──────────────────┘        └──────────────────┘

```



\---



\## 🛠 Tech Stack



\### Frontend



\- React

\- Vite

\- Axios

\- jsPDF

\- HTML

\- CSS



\### Backend



\- Python

\- FastAPI

\- Uvicorn

\- TensorFlow

\- NumPy

\- Pillow



\### Machine Learning



\- TensorFlow / Keras

\- MobileNetV2

\- Transfer Learning

\- Image Augmentation

\- PlantVillage Dataset



\### External API



\- OpenWeather API



\---



\## 📁 Project Structure



```text

Agricrop-AI/

│

├── backend/

│   ├── main.py

│   └── requirements.txt

│

├── frontend/

│   ├── src/

│   │   ├── App.jsx

│   │   ├── App.css

│   │   ├── index.css

│   │   └── main.jsx

│   ├── .env.example

│   ├── package.json

│   └── vite.config.js

│

├── ml/

│   └── train\_model.py

│

├── models/

│   ├── plant\_disease\_model.keras

│   └── class\_names.txt

│

├── .gitignore

└── README.md

```



\---



\## 🚀 Running Locally



\### 1. Clone the Repository



```bash

git clone https://github.com/YOUR\_USERNAME/Agricrop-AI.git

cd Agricrop-AI

```



Replace `YOUR\_USERNAME` with your GitHub username.



\### 2. Backend Setup



Open a terminal in the project folder:



```bash

cd backend

```



Create a virtual environment.



\#### Windows



```bash

python -m venv venv

venv\\Scripts\\activate

```



Install dependencies:



```bash

pip install -r requirements.txt

```



Start the API:



```bash

uvicorn main:app --reload

```



The backend will run at:



```text

http://127.0.0.1:8000

```



FastAPI documentation:



```text

http://127.0.0.1:8000/docs

```



\### 3. Frontend Setup



Open another terminal:



```bash

cd frontend

npm install

```



Create a local `.env` file.



Add:



```env

VITE\_WEATHER\_API\_KEY=your\_openweather\_api\_key

VITE\_API\_BASE\_URL=http://127.0.0.1:8000

```



Start the frontend:



```bash

npm run dev

```



Open the local Vite URL shown in the terminal, normally:



```text

http://localhost:5173

```



\---



\## 🔐 Environment Variables



The real `.env` file is intentionally excluded from Git.



Use `.env.example` as the template:



```env

VITE\_WEATHER\_API\_KEY=your\_openweather\_api\_key\_here

VITE\_API\_BASE\_URL=http://127.0.0.1:8000

```



\*\*Never commit a real API key to the repository.\*\*



\---



\## ⚠️ Model Limitations



The classifier is trained on the PlantVillage dataset, which primarily contains curated plant images.



Real-world field images can contain:



\- Physical damage

\- Nutrient deficiencies

\- Insect damage

\- Lighting variation

\- Background noise

\- Multiple plant conditions

\- Diseases or conditions not represented in the training classes



Therefore, a high softmax confidence does \*\*not necessarily guarantee correct real-world diagnosis\*\*.



CropCare AI communicates this limitation instead of presenting every prediction as a guaranteed diagnosis.



The application is intended as an \*\*agricultural assistance and screening tool\*\*, not a replacement for professional agricultural diagnosis.



\---



\## 🎯 Future Improvements



Potential future improvements include:



\- Field-image dataset collection and fine-tuning

\- Out-of-distribution / unknown-condition detection

\- More crop and disease classes

\- Multilingual agricultural guidance

\- Farmer-friendly mobile interface

\- Historical disease tracking

\- Location-aware agricultural recommendations

\- More advanced weather-based disease-risk prediction

\- Model performance evaluation on real-world field images



\---



\## 📌 Project Goal



CropCare AI demonstrates how \*\*computer vision, machine learning, weather data, and practical agricultural recommendations\*\* can be combined into a usable agricultural decision-support application.



The project focuses not only on model prediction, but also on communicating \*\*confidence, limitations, and actionable recommendations\*\* to the user.



\---



\### 🌱 Built with AI, machine learning, and a focus on practical agriculture.

