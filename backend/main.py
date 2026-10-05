from datetime import datetime
from pathlib import Path

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError


# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "plant_disease_model.keras"
CLASS_NAMES_PATH = PROJECT_ROOT / "models" / "class_names.txt"


# =========================================================
# LOAD MODEL
# =========================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found:\n{MODEL_PATH}")

if not CLASS_NAMES_PATH.exists():
    raise FileNotFoundError(
        f"Class names file not found:\n{CLASS_NAMES_PATH}"
    )

print("Loading Plant Disease Detection model...")

model = tf.keras.models.load_model(MODEL_PATH)

class_names = CLASS_NAMES_PATH.read_text(
    encoding="utf-8"
).splitlines()

print("Model loaded successfully.")
print(f"Number of classes: {len(class_names)}")


# =========================================================
# FASTAPI
# =========================================================

app = FastAPI(
    title="CropCare AI API",
    description=(
        "AI-powered plant disease detection and "
        "agricultural advisory API."
    ),
    version="3.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# DISEASE ADVISORY DATABASE
# =========================================================

DISEASE_ADVISORY = {

    # -----------------------------------------------------
    # APPLE
    # -----------------------------------------------------

    "Apple_scab": {
        "severity": "Moderate",
        "spread_risk": "High",
        "action": "Remove affected leaves and begin disease management.",
        "treatment": (
            "Remove severely affected leaves and use an appropriate "
            "fungicide according to the product label."
        ),
        "fertilizer": (
            "Maintain balanced nutrition and avoid excessive nitrogen."
        ),
        "watering": (
            "Water at the soil level and avoid prolonged leaf wetness."
        ),
        "prevention": (
            "Remove fallen infected leaves, improve airflow, and "
            "maintain good orchard sanitation."
        ),
    },

    "Apple_Black_rot": {
        "severity": "High",
        "spread_risk": "High",
        "action": "Remove infected plant material and begin treatment.",
        "treatment": (
            "Prune and remove infected plant material and follow "
            "local agricultural guidance for appropriate fungicide use."
        ),
        "fertilizer": (
            "Maintain balanced nutrition and avoid excessive nitrogen."
        ),
        "watering": (
            "Avoid overhead irrigation and prolonged leaf wetness."
        ),
        "prevention": (
            "Remove mummified fruit and dead wood and maintain good airflow."
        ),
    },

    "Apple_Cedar_apple_rust": {
        "severity": "Moderate",
        "spread_risk": "Moderate",
        "action": "Monitor closely and manage infected foliage.",
        "treatment": (
            "Remove severely affected foliage and use an appropriate "
            "fungicide according to local agricultural recommendations."
        ),
        "fertilizer": (
            "Maintain balanced crop nutrition."
        ),
        "watering": (
            "Water near the root zone and avoid unnecessary leaf wetness."
        ),
        "prevention": (
            "Improve airflow and manage nearby host plants where appropriate."
        ),
    },


    # -----------------------------------------------------
    # CHERRY
    # -----------------------------------------------------

    "Cherry_(including_sour)_Powdery_mildew": {
        "severity": "Moderate",
        "spread_risk": "High",
        "action": "Improve airflow and begin mildew management.",
        "treatment": (
            "Remove severely affected foliage and use an appropriate "
            "fungicide according to the product label."
        ),
        "fertilizer": (
            "Avoid excessive nitrogen and maintain balanced nutrition."
        ),
        "watering": (
            "Water near the soil and avoid unnecessary leaf wetness."
        ),
        "prevention": (
            "Avoid overcrowding and maintain good air circulation."
        ),
    },


    # -----------------------------------------------------
    # CORN
    # -----------------------------------------------------

    "Corn_(maize)_Cercospora_leaf_spot Gray_leaf_spot": {
        "severity": "Moderate",
        "spread_risk": "High",
        "action": "Remove heavily affected material and monitor spread.",
        "treatment": (
            "Follow local agricultural recommendations for disease "
            "management and appropriate fungicide use."
        ),
        "fertilizer": (
            "Maintain balanced soil nutrition and avoid excessive nitrogen."
        ),
        "watering": (
            "Avoid unnecessary leaf wetness and improve field drainage."
        ),
        "prevention": (
            "Practice crop rotation, manage crop residue, and maintain "
            "good field airflow."
        ),
    },

    "Corn_(maize)_Common_rust_": {
        "severity": "Moderate",
        "spread_risk": "Moderate",
        "action": "Monitor the crop and manage symptoms if they increase.",
        "treatment": (
            "Monitor disease development and follow local agricultural "
            "recommendations for treatment."
        ),
        "fertilizer": (
            "Maintain balanced nutrition appropriate for crop growth."
        ),
        "watering": (
            "Maintain appropriate soil moisture and avoid waterlogging."
        ),
        "prevention": (
            "Use healthy planting material and maintain good field hygiene."
        ),
    },

    "Corn_(maize)_Northern_Leaf_Blight": {
        "severity": "High",
        "spread_risk": "High",
        "action": "Act quickly to limit disease spread.",
        "treatment": (
            "Remove severely affected plant material where practical and "
            "follow local agricultural recommendations for fungicide use."
        ),
        "fertilizer": (
            "Maintain balanced crop nutrition without excessive nitrogen."
        ),
        "watering": (
            "Avoid prolonged leaf wetness and improve field drainage."
        ),
        "prevention": (
            "Practice crop rotation, manage infected residue, and improve "
            "air circulation."
        ),
    },


    # -----------------------------------------------------
    # GRAPE
    # -----------------------------------------------------

    "Grape_Black_rot": {
        "severity": "High",
        "spread_risk": "High",
        "action": "Remove infected material and begin disease management.",
        "treatment": (
            "Remove infected leaves and fruit and follow local agricultural "
            "guidance for appropriate fungicide treatment."
        ),
        "fertilizer": (
            "Maintain balanced vineyard nutrition."
        ),
        "watering": (
            "Avoid excessive moisture and prolonged leaf wetness."
        ),
        "prevention": (
            "Improve canopy airflow and remove infected plant debris."
        ),
    },

    "Grape_Esca_(Black_Measles)": {
        "severity": "High",
        "spread_risk": "Moderate",
        "action": "Inspect affected vines and seek crop-specific guidance.",
        "treatment": (
            "Remove severely affected plant material where appropriate "
            "and consult local viticulture guidance."
        ),
        "fertilizer": (
            "Maintain balanced nutrition based on soil requirements."
        ),
        "watering": (
            "Avoid water stress and excessive irrigation."
        ),
        "prevention": (
            "Maintain vineyard sanitation and carefully manage pruning wounds."
        ),
    },

    "Grape_Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "severity": "Moderate",
        "spread_risk": "High",
        "action": "Monitor spread and improve canopy ventilation.",
        "treatment": (
            "Remove severely affected foliage and follow local agricultural "
            "recommendations for appropriate disease management."
        ),
        "fertilizer": (
            "Maintain balanced nutrition."
        ),
        "watering": (
            "Avoid prolonged leaf wetness."
        ),
        "prevention": (
            "Improve airflow and remove infected plant debris."
        ),
    },


    # -----------------------------------------------------
    # ORANGE
    # -----------------------------------------------------

    "Orange_Haunglongbing_(Citrus_greening)": {
        "severity": "Critical",
        "spread_risk": "Very High",
        "action": "Isolate and seek professional agricultural guidance.",
        "treatment": (
            "There is no simple curative treatment for citrus greening. "
            "Follow local agricultural authority recommendations."
        ),
        "fertilizer": (
            "Maintain balanced nutrition to support affected trees."
        ),
        "watering": (
            "Maintain consistent soil moisture without waterlogging."
        ),
        "prevention": (
            "Monitor and manage the insect vectors responsible for spreading "
            "the disease according to local agricultural guidance."
        ),
    },


    # -----------------------------------------------------
    # PEACH
    # -----------------------------------------------------

    "Peach_Bacterial_spot": {
        "severity": "Moderate",
        "spread_risk": "High",
        "action": "Reduce leaf wetness and monitor disease progression.",
        "treatment": (
            "Remove severely affected material and follow local agricultural "
            "recommendations for bacterial disease management."
        ),
        "fertilizer": (
            "Maintain balanced nutrition."
        ),
        "watering": (
            "Avoid overhead watering and prolonged leaf wetness."
        ),
        "prevention": (
            "Improve airflow and avoid handling plants when foliage is wet."
        ),
    },


    # -----------------------------------------------------
    # PEPPER
    # -----------------------------------------------------

    "Pepper,_bell_Bacterial_spot": {
        "severity": "Moderate",
        "spread_risk": "High",
        "action": "Remove severely affected leaves and monitor spread.",
        "treatment": (
            "Remove affected plant material and follow local agricultural "
            "recommendations for bacterial spot management."
        ),
        "fertilizer": (
            "Maintain balanced nutrition according to soil requirements."
        ),
        "watering": (
            "Avoid overhead irrigation and prolonged leaf wetness."
        ),
        "prevention": (
            "Use clean planting material and maintain good field hygiene."
        ),
    },


    # -----------------------------------------------------
    # POTATO
    # -----------------------------------------------------

    "Potato_Early_blight": {
        "severity": "Moderate",
        "spread_risk": "High",
        "action": "Begin disease management and monitor nearby foliage.",
        "treatment": (
            "Remove severely affected leaves and use an appropriate "
            "fungicide according to the product label."
        ),
        "fertilizer": (
            "Maintain balanced nutrition and avoid excessive nitrogen."
        ),
        "watering": (
            "Water at soil level and avoid prolonged leaf wetness."
        ),
        "prevention": (
            "Practice crop rotation, remove infected residue, and improve airflow."
        ),
    },

    "Potato_Late_blight": {
        "severity": "Critical",
        "spread_risk": "Very High",
        "action": "Act immediately to limit rapid disease spread.",
        "treatment": (
            "Remove severely affected plant material and seek local "
            "agricultural guidance for appropriate fungicide management."
        ),
        "fertilizer": (
            "Maintain balanced nutrition without excessive nitrogen."
        ),
        "watering": (
            "Avoid overhead irrigation and prolonged leaf wetness."
        ),
        "prevention": (
            "Remove infected material, improve airflow, and avoid handling "
            "wet foliage."
        ),
    },


    # -----------------------------------------------------
    # SQUASH
    # -----------------------------------------------------

    "Squash_Powdery_mildew": {
        "severity": "Moderate",
        "spread_risk": "High",
        "action": "Improve airflow and manage affected foliage.",
        "treatment": (
            "Remove severely affected leaves and use an appropriate "
            "fungicide according to the product label."
        ),
        "fertilizer": (
            "Avoid excessive nitrogen and maintain balanced nutrition."
        ),
        "watering": (
            "Water near the soil and maintain good airflow."
        ),
        "prevention": (
            "Avoid overcrowding and maintain adequate ventilation."
        ),
    },


    # -----------------------------------------------------
    # STRAWBERRY
    # -----------------------------------------------------

    "Strawberry_Leaf_scorch": {
        "severity": "Moderate",
        "spread_risk": "Moderate",
        "action": "Remove severely affected leaves and monitor the plant.",
        "treatment": (
            "Remove severely affected foliage and follow local agricultural "
            "recommendations for disease management."
        ),
        "fertilizer": (
            "Maintain balanced nutrition and avoid excessive fertilization."
        ),
        "watering": (
            "Maintain consistent soil moisture without waterlogging."
        ),
        "prevention": (
            "Improve airflow, remove infected foliage, and maintain field hygiene."
        ),
    },


    # -----------------------------------------------------
    # TOMATO
    # -----------------------------------------------------

    "Tomato_Bacterial_spot": {
        "severity": "Moderate",
        "spread_risk": "High",
        "action": "Reduce leaf wetness and remove severely affected foliage.",
        "treatment": (
            "Remove severely affected material and follow local agricultural "
            "recommendations for bacterial disease management."
        ),
        "fertilizer": (
            "Maintain balanced crop nutrition."
        ),
        "watering": (
            "Avoid overhead irrigation and prolonged leaf wetness."
        ),
        "prevention": (
            "Use clean planting material and maintain good field hygiene."
        ),
    },

    "Tomato_Early_blight": {
        "severity": "Moderate",
        "spread_risk": "High",
        "action": "Begin disease management and monitor nearby leaves.",
        "treatment": (
            "Remove severely affected leaves and use an appropriate "
            "fungicide according to the product label."
        ),
        "fertilizer": (
            "Maintain balanced nutrition and avoid excessive nitrogen."
        ),
        "watering": (
            "Water near the soil and avoid prolonged leaf wetness."
        ),
        "prevention": (
            "Practice crop rotation, remove infected debris, and improve airflow."
        ),
    },

    "Tomato_Late_blight": {
        "severity": "Critical",
        "spread_risk": "Very High",
        "action": "Act quickly and seek crop-specific agricultural guidance.",
        "treatment": (
            "Remove affected plant material and follow local agricultural "
            "recommendations for appropriate disease management."
        ),
        "fertilizer": (
            "Maintain balanced nutrition without excessive nitrogen."
        ),
        "watering": (
            "Avoid overhead irrigation and prolonged leaf wetness."
        ),
        "prevention": (
            "Improve airflow, remove infected material, and avoid wet foliage."
        ),
    },

    "Tomato_Leaf_Mold": {
        "severity": "Moderate",
        "spread_risk": "High",
        "action": "Improve ventilation and reduce prolonged humidity.",
        "treatment": (
            "Remove severely affected leaves and follow local agricultural "
            "guidance for appropriate fungicide management."
        ),
        "fertilizer": (
            "Maintain balanced nutrition and avoid excessive nitrogen."
        ),
        "watering": (
            "Avoid overhead watering and reduce prolonged leaf wetness."
        ),
        "prevention": (
            "Improve greenhouse or field ventilation and avoid overcrowding."
        ),
    },

    "Tomato_Septoria_leaf_spot": {
        "severity": "Moderate",
        "spread_risk": "High",
        "action": "Remove affected foliage and monitor disease progression.",
        "treatment": (
            "Remove severely affected leaves and use appropriate treatment "
            "according to local agricultural guidance."
        ),
        "fertilizer": (
            "Maintain balanced nutrition."
        ),
        "watering": (
            "Water at soil level and avoid wetting foliage."
        ),
        "prevention": (
            "Remove infected leaves and plant debris and improve airflow."
        ),
    },

    "Tomato_Spider_mites Two-spotted_spider_mite": {
        "severity": "High",
        "spread_risk": "High",
        "action": "Inspect nearby plants and begin pest management.",
        "treatment": (
            "Inspect the underside of leaves and follow integrated pest "
            "management recommendations appropriate for spider mites."
        ),
        "fertilizer": (
            "Avoid excessive nitrogen, which can encourage tender growth."
        ),
        "watering": (
            "Maintain adequate soil moisture and avoid plant stress."
        ),
        "prevention": (
            "Monitor plants regularly, manage weeds, and encourage "
            "beneficial predators where practical."
        ),
    },

    "Tomato_Target_Spot": {
        "severity": "Moderate",
        "spread_risk": "High",
        "action": "Remove affected foliage and improve airflow.",
        "treatment": (
            "Remove severely affected leaves and follow local agricultural "
            "recommendations for appropriate treatment."
        ),
        "fertilizer": (
            "Maintain balanced crop nutrition."
        ),
        "watering": (
            "Avoid overhead irrigation and prolonged leaf wetness."
        ),
        "prevention": (
            "Improve airflow, remove infected debris, and practice crop rotation."
        ),
    },

    "Tomato_Tomato_Yellow_Leaf_Curl_Virus": {
        "severity": "High",
        "spread_risk": "Very High",
        "action": "Inspect nearby plants and control disease vectors.",
        "treatment": (
            "There is no direct cure for the virus. Remove severely affected "
            "plants where appropriate and follow local agricultural guidance."
        ),
        "fertilizer": (
            "Maintain balanced nutrition to reduce plant stress."
        ),
        "watering": (
            "Maintain consistent soil moisture and avoid water stress."
        ),
        "prevention": (
            "Monitor and manage whitefly vectors and remove infected plants "
            "according to local recommendations."
        ),
    },

    "Tomato_Tomato_mosaic_virus": {
        "severity": "High",
        "spread_risk": "High",
        "action": "Isolate affected plants and improve sanitation.",
        "treatment": (
            "There is no direct cure for the virus. Remove severely affected "
            "plants where appropriate and follow local agricultural guidance."
        ),
        "fertilizer": (
            "Maintain balanced nutrition and reduce plant stress."
        ),
        "watering": (
            "Maintain consistent soil moisture."
        ),
        "prevention": (
            "Disinfect tools, use clean planting material, and avoid handling "
            "healthy plants after infected plants."
        ),
    },
}


# =========================================================
# HEALTHY ADVISORY
# =========================================================

HEALTHY_ADVISORY = {
    "severity": "None",
    "spread_risk": "Low",
    "action": "Continue regular monitoring.",
    "treatment": (
        "No disease treatment is required. Continue regular monitoring "
        "and maintain balanced crop care."
    ),
    "fertilizer": (
        "Use a balanced fertilizer according to crop growth stage "
        "and soil requirements."
    ),
    "watering": (
        "Maintain consistent soil moisture and avoid both waterlogging "
        "and prolonged dryness."
    ),
    "prevention": (
        "Continue monitoring for pests, nutrient deficiencies, and "
        "early disease symptoms."
    ),
}


# =========================================================
# FALLBACK ADVISORY
# =========================================================

DEFAULT_ADVISORY = {
    "severity": "Unknown",
    "spread_risk": "Unknown",
    "action": "Monitor the plant and consult local agricultural guidance.",
    "treatment": (
        "Monitor the affected plant closely and consult local "
        "agricultural guidance for disease-specific treatment."
    ),
    "fertilizer": (
        "Maintain balanced fertilization according to crop requirements "
        "and soil conditions."
    ),
    "watering": (
        "Maintain appropriate soil moisture and avoid prolonged leaf wetness."
    ),
    "prevention": (
        "Maintain good field hygiene, airflow, and regular plant monitoring."
    ),
}


# =========================================================
# HELPERS
# =========================================================

def parse_class_name(class_name: str):
    if "___" in class_name:
        crop, disease = class_name.split("___", 1)
    else:
        crop = "Unknown"
        disease = class_name

    crop = crop.replace("_", " ").strip()

    disease = disease.replace("_", " ")
    disease = " ".join(disease.split())

    return crop, disease


def get_advisory(class_name: str, disease: str):
    if "healthy" in class_name.lower():
        return HEALTHY_ADVISORY

    advisory = DISEASE_ADVISORY.get(class_name)

    if advisory:
        return advisory

    return DEFAULT_ADVISORY


# =========================================================
# PREDICTION ENDPOINT
# =========================================================

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    if not file:
        raise HTTPException(
            status_code=400,
            detail="No image file was provided.",
        )

    allowed_types = {
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/webp",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid file type. Please upload a JPG, JPEG, "
                "PNG, or WEBP image."
            ),
        )

    try:
        image = Image.open(file.file)
        image.load()
        image = image.convert("RGB")

    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image.",
        )

    finally:
        await file.close()

    # -----------------------------------------------------
    # Original image information
    # -----------------------------------------------------

    image_width, image_height = image.size

    # -----------------------------------------------------
    # Prepare image
    # -----------------------------------------------------

    image_for_prediction = image.resize((224, 224))

    image_array = np.array(image_for_prediction)

    image_array = np.expand_dims(
        image_array,
        axis=0,
    )

    image_array = tf.keras.applications.mobilenet_v2.preprocess_input(
        image_array
    )

    # -----------------------------------------------------
    # Model prediction
    # -----------------------------------------------------

    predictions = model.predict(
        image_array,
        verbose=0,
    )[0]

    predicted_index = int(np.argmax(predictions))

    confidence = float(predictions[predicted_index])

    predicted_class = class_names[predicted_index]

    # -----------------------------------------------------
    # Top 3 predictions
    # -----------------------------------------------------

    top_indices = np.argsort(predictions)[-3:][::-1]

    top_predictions = []

    for index in top_indices:
        index = int(index)

        crop_name, disease_name = parse_class_name(
            class_names[index]
        )

        top_predictions.append({
            "crop": crop_name,
            "disease": disease_name,
            "class_name": class_names[index],
            "confidence": round(
                float(predictions[index]) * 100,
                2,
            ),
        })

    # -----------------------------------------------------
    # Parse primary prediction
    # -----------------------------------------------------

    crop, disease = parse_class_name(
        predicted_class
    )

    advisory = get_advisory(
        predicted_class,
        disease,
    )

    # -----------------------------------------------------
    # Model assessment
    # -----------------------------------------------------

    if "healthy" in predicted_class.lower():
        model_note = (
            "The AI classifier predicts a healthy plant based on "
            "the supported PlantVillage disease classes. Visible "
            "damage may also be caused by conditions outside the "
            "model's supported classes."
        )
    else:
        model_note = (
            "Prediction generated by the trained MobileNetV2 "
            "PlantVillage classifier. For field-level decisions, "
            "combine the prediction with crop conditions and "
            "local agricultural guidance."
        )

    # -----------------------------------------------------
    # Final response
    # -----------------------------------------------------

    return {
        "disease": disease,
        "crop": crop,
        "class_name": predicted_class,

        "confidence": round(
            confidence * 100,
            2,
        ),

        "status": (
            "Healthy"
            if "healthy" in predicted_class.lower()
            else advisory["severity"]
        ),

        "severity": advisory["severity"],
        "spread_risk": advisory["spread_risk"],
        "action_required": advisory["action"],

        "treatment": advisory["treatment"],
        "fertilizer": advisory["fertilizer"],
        "watering": advisory["watering"],
        "prevention": advisory["prevention"],

        "model_note": model_note,

        "top_predictions": top_predictions,

        "date": datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        ),

        "image_size": {
            "width": image_width,
            "height": image_height,
        },
    }