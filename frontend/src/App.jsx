import "./App.css";
import { useState } from "react";
import axios from "axios";
import jsPDF from "jspdf";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const WEATHER_API_KEY = import.meta.env.VITE_WEATHER_API_KEY;

const cropDetails = {
  Rice: {
    season: "Kharif",
    soil: "Clayey Soil",
    water: "High",
    harvest: "120-150 Days",
  },

  Wheat: {
    season: "Rabi",
    soil: "Loamy Soil",
    water: "Medium",
    harvest: "110-130 Days",
  },

  Tomato: {
    season: "Rabi",
    soil: "Well-drained Loamy Soil",
    water: "Medium",
    harvest: "90-110 Days",
  },

  Potato: {
    season: "Rabi",
    soil: "Sandy Loam",
    water: "Medium",
    harvest: "90-120 Days",
  },

  Maize: {
    season: "Kharif",
    soil: "Fertile Loamy Soil",
    water: "Medium",
    harvest: "90-120 Days",
  },

  Cotton: {
    season: "Kharif",
    soil: "Black Cotton Soil",
    water: "Medium",
    harvest: "150-180 Days",
  },

  Sugarcane: {
    season: "Spring",
    soil: "Loamy Soil",
    water: "High",
    harvest: "10-18 Months",
  },

  Chilli: {
    season: "Kharif",
    soil: "Well-drained Sandy Loam",
    water: "Medium",
    harvest: "120-150 Days",
  },

  Mango: {
    season: "Summer",
    soil: "Deep Loamy Soil",
    water: "Low",
    harvest: "4-6 Years (Tree)",
  },
};

function App() {
  const [image, setImage] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const [crop, setCrop] = useState("");
  const [location, setLocation] = useState("");
  const [weather, setWeather] = useState(null);

  const handleImage = (event) => {
    const file = event.target.files[0];

    if (file) {
      setSelectedFile(file);
      setImage(URL.createObjectURL(file));
      setResult(null);
      setWeather(null);
    }
  };

  const analyzePlant = async () => {
    if (!selectedFile) {
      alert("Please upload a plant image.");
      return;
    }

    if (!crop) {
      alert("Please select a crop.");
      return;
    }

    if (!location.trim()) {
      alert("Please enter your farm location.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setLoading(true);

    try {
      // =====================================================
      // AI DISEASE PREDICTION
      // =====================================================

      const response = await axios.post(
        `${API_BASE_URL}/predict`,
        formData
      );

      setResult(response.data);

      // =====================================================
      // WEATHER ANALYSIS
      // =====================================================

      if (WEATHER_API_KEY) {
        try {
          const weatherResponse = await axios.get(
            `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(
              location
            )}&appid=${WEATHER_API_KEY}&units=metric`
          );

          const data = weatherResponse.data;

          let advice = "";

          if (data.weather?.[0]?.main === "Rain") {
            advice =
              "🌧 Rain expected. Avoid spraying pesticides today.";
          } else if (data.main?.temp > 35) {
            advice =
              "☀ High temperature. Irrigate crops in the morning or evening.";
          } else if (data.main?.humidity > 80) {
            advice =
              "💧 High humidity. Monitor crops closely for fungal diseases.";
          } else {
            advice =
              "🌱 Weather is suitable for normal farming activities.";
          }

          setWeather({
            condition: data.weather?.[0]?.main || "Unknown",
            temperature: data.main?.temp ?? "--",
            humidity: data.main?.humidity ?? "--",
            advice,
          });
        } catch (weatherError) {
          console.error("Weather Error:", weatherError);
          setWeather(null);
        }
      }

      // =====================================================
      // HISTORY
      // =====================================================

      setHistory((prev) => [
        {
          crop,
          location,
          ...response.data,
        },
        ...prev.slice(0, 4),
      ]);
    } catch (error) {
      console.error("Prediction Error:", error);

      if (error.response?.data?.detail) {
        alert(error.response.data.detail);
      } else {
        alert(
          "Unable to connect to the CropCare AI backend."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // PDF REPORT
  // =========================================================

  const downloadReport = () => {
    if (!result) return;

    const doc = new jsPDF();

    doc.setFontSize(22);
    doc.text("CropCare AI Report", 20, 20);

    doc.setFontSize(12);

    doc.text(`Selected Crop: ${crop}`, 20, 40);
    doc.text(`Detected Crop: ${result.crop}`, 20, 50);
    doc.text(`Location: ${location}`, 20, 60);
    doc.text(`Disease: ${result.disease}`, 20, 70);
    doc.text(`Confidence: ${result.confidence}%`, 20, 80);
    doc.text(`Status: ${result.status}`, 20, 90);
    doc.text(`Severity: ${result.severity}`, 20, 100);
    doc.text(`Spread Risk: ${result.spread_risk}`, 20, 110);

    doc.text(
      `Action Required: ${result.action_required}`,
      20,
      125,
      {
        maxWidth: 170,
      }
    );

    doc.text(
      `Treatment: ${result.treatment}`,
      20,
      145,
      {
        maxWidth: 170,
      }
    );

    doc.text(
      `Fertilizer: ${result.fertilizer}`,
      20,
      165,
      {
        maxWidth: 170,
      }
    );

    doc.text(
      `Watering: ${result.watering}`,
      20,
      185,
      {
        maxWidth: 170,
      }
    );

    doc.text(
      `Prevention: ${result.prevention}`,
      20,
      205,
      {
        maxWidth: 170,
      }
    );

    doc.text(
      "Generated by CropCare AI",
      20,
      230
    );

    doc.save("CropCare_AI_Report.pdf");
  };

  // =========================================================
  // HEALTH INDEX
  // =========================================================

  const healthInfo = (() => {
    if (!result) return null;

    if (result.status === "Healthy") {
      return {
        score: 98,
        recovery: "Excellent",
        days: "Already Healthy",
      };
    }

    if (result.severity === "Moderate") {
      return {
        score: 76,
        recovery: "90%",
        days: "7-10 Days",
      };
    }

    if (result.severity === "High") {
      return {
        score: 42,
        recovery: "65%",
        days: "15-20 Days",
      };
    }

    if (result.severity === "Critical") {
      return {
        score: 25,
        recovery: "Needs Immediate Attention",
        days: "Varies by Crop",
      };
    }

    return {
      score: 60,
      recovery: "75%",
      days: "10-15 Days",
    };
  })();

  // =========================================================
  // STATUS CLASS
  // =========================================================

  const getStatusClass = () => {
    if (result?.status === "Healthy") {
      return "status-badge success";
    }

    if (
      result?.severity === "Critical" ||
      result?.status === "Critical"
    ) {
      return "status-badge danger";
    }

    return "status-badge warning";
  };

  // =========================================================
  // RENDER
  // =========================================================

  return (
    <div className="hero">
      <div className="hero-card">

        {/* =================================================
            HERO HEADER
        ================================================= */}

        <div className="hero-header">
          <div className="hero-badge">
            🌿 AI Powered Agriculture
          </div>

          <h1>
            CropCare
            <span>AI</span>
          </h1>

          <h2>
            Smart Crop Disease Detection
            <br />
            & Intelligent Farming Advisory
          </h2>

          <p>
            Analyze plant health, detect diseases,
            receive weather-based recommendations,
            crop advisory, and AI-powered farming insights.
          </p>
        </div>

        {/* =================================================
            CROP SELECTION
        ================================================= */}

        <div className="crop-select">
          <label htmlFor="crop">
            🌱 Select Crop
          </label>

          <select
            id="crop"
            name="crop"
            value={crop}
            onChange={(e) => setCrop(e.target.value)}
          >
            <option value="">
              Choose Crop
            </option>

            <option>Rice</option>
            <option>Wheat</option>
            <option>Tomato</option>
            <option>Potato</option>
            <option>Maize</option>
            <option>Cotton</option>
            <option>Sugarcane</option>
            <option>Chilli</option>
            <option>Mango</option>
          </select>
        </div>

        {/* =================================================
            LOCATION
        ================================================= */}

        <div className="location-input">
          <label htmlFor="location">
            📍 Farm Location
          </label>

          <input
            id="location"
            name="location"
            type="text"
            placeholder="Enter your village or city"
            value={location}
            onChange={(e) =>
              setLocation(e.target.value)
            }
          />
        </div>

        {/* =================================================
            IMAGE UPLOAD
        ================================================= */}

        <label className="upload-btn">
          📤 Upload Plant Image

          <input
            type="file"
            accept="image/*"
            hidden
            onChange={handleImage}
          />
        </label>

        {/* =================================================
            IMAGE PREVIEW
        ================================================= */}

        {image && (
          <div className="preview">
            <h3>🌿 Uploaded Image</h3>

            <img
              src={image}
              alt="Uploaded plant"
            />

            <button
              className="analyze-btn"
              onClick={analyzePlant}
              disabled={loading}
            >
              {loading
                ? "🔍 Analyzing..."
                : "🤖 Analyze Plant"}
            </button>
          </div>
        )}

        {/* =================================================
            LOADING
        ================================================= */}

        {loading && (
          <h2
            style={{
              marginTop: 30,
              color: "#2E7D32",
            }}
          >
            🔍 AI is analyzing your crop...
          </h2>
        )}

        {/* =================================================
            AI ANALYSIS
        ================================================= */}

        {result && (
          <div className="result-card">

            <h2>
              🌿 AI Analysis Dashboard
            </h2>

            {/* =================================================
                DASHBOARD GRID
            ================================================= */}

            <div className="dashboard-grid">

              <div className="dashboard-card">
                <h4>🌱 Selected Crop</h4>
                <p>{crop}</p>
              </div>

              <div className="dashboard-card">
                <h4>🤖 Detected Crop</h4>
                <p>{result.crop}</p>
              </div>

              <div className="dashboard-card">
                <h4>📍 Location</h4>
                <p>{location}</p>
              </div>

              <div className="dashboard-card">
                <h4>🦠 Disease</h4>
                <p>{result.disease}</p>
              </div>

              <div className="dashboard-card">
                <h4>🎯 Confidence</h4>
                <p>{result.confidence}%</p>
              </div>

              <div className="dashboard-card">
                <h4>❤️ Plant Status</h4>
                <p>{result.status}</p>
              </div>

              <div className="dashboard-card">
                <h4>⚠️ Severity</h4>
                <p>{result.severity}</p>
              </div>

              <div className="dashboard-card">
                <h4>📈 Spread Risk</h4>
                <p>{result.spread_risk}</p>
              </div>

            </div>

            {/* =================================================
                MODEL NOTE
            ================================================= */}

            {result.model_note && (
              <div className="severity-action">
                <strong>🤖 AI Assessment Note</strong>

                <p>
                  {result.model_note}
                </p>
              </div>
            )}

            {/* =================================================
                WEATHER
            ================================================= */}

            {weather && (
              <div className="weather-card">

                <h3>
                  🌤 Weather Advisory
                </h3>

                <div className="weather-grid">

                  <div>
                    <strong>
                      Condition
                    </strong>
                    <p>
                      {weather.condition}
                    </p>
                  </div>

                  <div>
                    <strong>
                      Temperature
                    </strong>
                    <p>
                      {weather.temperature}°C
                    </p>
                  </div>

                  <div>
                    <strong>
                      Humidity
                    </strong>
                    <p>
                      {weather.humidity}%
                    </p>
                  </div>

                </div>

                <div className="weather-advice">
                  {weather.advice}
                </div>

              </div>
            )}

            {/* =================================================
                CROP ADVISORY
            ================================================= */}

            {crop && cropDetails[crop] && (
              <div className="crop-advisory">

                <h3>
                  🌾 Crop Advisory
                </h3>

                <div className="crop-grid">

                  <div className="crop-box">
                    <h4>
                      🌱 Best Season
                    </h4>
                    <p>
                      {cropDetails[crop].season}
                    </p>
                  </div>

                  <div className="crop-box">
                    <h4>
                      🌍 Soil Type
                    </h4>
                    <p>
                      {cropDetails[crop].soil}
                    </p>
                  </div>

                  <div className="crop-box">
                    <h4>
                      💧 Water Need
                    </h4>
                    <p>
                      {cropDetails[crop].water}
                    </p>
                  </div>

                  <div className="crop-box">
                    <h4>
                      ⏳ Harvest Time
                    </h4>
                    <p>
                      {cropDetails[crop].harvest}
                    </p>
                  </div>

                </div>

              </div>
            )}

            {/* =================================================
                DISEASE SEVERITY
            ================================================= */}

            <div className="severity-card">

              <h3>
                🦠 Disease Severity Analysis
              </h3>

              <div className="severity-grid">

                <div className="severity-box">
                  <h4>
                    🔴 Severity
                  </h4>

                  <p>
                    {result.severity || "Not available"}
                  </p>
                </div>

                <div className="severity-box">
                  <h4>
                    📈 Spread Risk
                  </h4>

                  <p>
                    {result.spread_risk || "Not available"}
                  </p>
                </div>

              </div>

              <div className="severity-action">

                <strong>
                  ⏰ Action Required
                </strong>

                <p>
                  {result.action_required ||
                    "Continue monitoring the plant."}
                </p>

              </div>

            </div>

            {/* =================================================
                HEALTH INDEX
            ================================================= */}

            {healthInfo && (
              <div className="health-index">

                <h3>
                  🌿 AI Plant Health Index
                </h3>

                <div className="health-grid">

                  <div className="health-box">
                    <h4>
                      Health Score
                    </h4>

                    <p>
                      {healthInfo.score}%
                    </p>
                  </div>

                  <div className="health-box">
                    <h4>
                      Recovery Chance
                    </h4>

                    <p>
                      {healthInfo.recovery}
                    </p>
                  </div>

                  <div className="health-box">
                    <h4>
                      Estimated Recovery
                    </h4>

                    <p>
                      {healthInfo.days}
                    </p>
                  </div>

                </div>

              </div>
            )}

            {/* =================================================
                CONFIDENCE BAR
            ================================================= */}

            <div className="confidence-box">

              <p>
                <strong>
                  Confidence Score
                </strong>
              </p>

              <div className="progress">

                <div
                  className="progress-fill"
                  style={{
                    width: `${Math.min(
                      Math.max(result.confidence, 0),
                      100
                    )}%`,
                  }}
                />

              </div>

              <span>
                {result.confidence}%
              </span>

            </div>

            {/* =================================================
                STATUS
            ================================================= */}

            <p>
              <strong>
                Plant Status:
              </strong>{" "}

              <span className={getStatusClass()}>
                {result.status}
              </span>
            </p>

            {/* =================================================
                HEALTH STARS
            ================================================= */}

            <div className="health-score">

              <h3>
                🌿 Plant Health Score
              </h3>

              <div className="stars">

                {result.status === "Healthy"
                  ? "⭐⭐⭐⭐⭐"
                  : result.severity === "Critical"
                  ? "⭐☆☆☆☆"
                  : result.severity === "High"
                  ? "⭐⭐☆☆☆"
                  : "⭐⭐⭐☆☆"}

              </div>

            </div>

            {/* =================================================
                RECOMMENDATIONS
            ================================================= */}

            <div className="info-grid">

              <div className="info-card">
                <h4>
                  ⏰ Action Required
                </h4>

                <p>
                  {result.action_required}
                </p>
              </div>

              <div className="info-card">
                <h4>
                  💊 Treatment
                </h4>

                <p>
                  {result.treatment}
                </p>
              </div>

              <div className="info-card">
                <h4>
                  🌾 Recommended Fertilizer
                </h4>

                <p>
                  {result.fertilizer}
                </p>
              </div>

              <div className="info-card">
                <h4>
                  💧 Watering Advice
                </h4>

                <p>
                  {result.watering}
                </p>
              </div>

              <div className="info-card">
                <h4>
                  🛡 Prevention
                </h4>

                <p>
                  {result.prevention}
                </p>
              </div>

            </div>

            {/* =================================================
                TOP 3 PREDICTIONS
            ================================================= */}

            {result.top_predictions?.length > 0 && (
              <div className="severity-card">

                <h3>
                  🧠 AI Prediction Alternatives
                </h3>

                <div className="info-grid">

                  {result.top_predictions.map(
                    (prediction, index) => (
                      <div
                        className="info-card"
                        key={`${prediction.class_name}-${index}`}
                      >
                        <h4>
                          #{index + 1}{" "}
                          {prediction.disease}
                        </h4>

                        <p>
                          Crop: {prediction.crop}
                        </p>

                        <p>
                          Confidence:{" "}
                          {prediction.confidence}%
                        </p>
                      </div>
                    )
                  )}

                </div>

              </div>
            )}

            {/* =================================================
                DOWNLOAD REPORT
            ================================================= */}

            <button
              className="download-btn"
              onClick={downloadReport}
            >
              📄 Download AI Report
            </button>

          </div>
        )}

        {/* =================================================
            HISTORY
        ================================================= */}

        {history.length > 0 && (
          <div className="history-card">

            <h2>
              📜 Previous Analyses
            </h2>

            {history.map((item, index) => (
              <div
                className="history-item"
                key={index}
              >

                <h4>
                  {item.crop}
                </h4>

                <p>
                  🦠 {item.disease}
                </p>

                <p>
                  🤖 Detected: {item.crop === item.crop
                    ? item.crop
                    : item.crop}
                </p>

                <p>
                  📍 {item.location}
                </p>

                <p>
                  🎯 {item.confidence}%{" "}
                  &nbsp; | &nbsp;
                  ❤️ {item.status}
                </p>

              </div>
            ))}

          </div>
        )}

      </div>
    </div>
  );
}

export default App;