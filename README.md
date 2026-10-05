# 🌱 CropCare AI — Intelligent Plant Disease Detection & Agricultural Advisory

CropCare AI is an AI-powered agricultural assistance platform that combines **plant disease classification, crop advisory, and weather-based recommendations** in a single web application.

## ✨ Features

### 🌿 Plant Disease Detection

- Deep-learning image classification using MobileNetV2
- 38 PlantVillage disease/healthy classes
- Top-3 model predictions with confidence scores

## 🧠 Machine Learning

The disease classifier was trained using the **PlantVillage dataset** and transfer learning with **MobileNetV2**.

### Model Configuration

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
models/plant_disease_model.keras