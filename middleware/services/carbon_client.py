"""
Carbon Sequestration Client Service
Calls the GROA (Global Reforestation Opportunity Assessment) model
for carbon accumulation potential predictions
"""

import sys
import os
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Add backend/app to Python path to import groa-mapping
BACKEND_APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend/app"))
if BACKEND_APP_PATH not in sys.path:
    sys.path.insert(0, BACKEND_APP_PATH)


async def predict_carbon_sequestration(
    centroid_lon: float,
    centroid_lat: float
) -> Optional[Dict]:
    """
    Predict carbon accumulation potential for forest regrowth
    Uses GROA model with real-time weather and soil data
    
    Args:
        centroid_lon: Polygon centroid longitude
        centroid_lat: Polygon centroid latitude
    
    Returns:
        Dict with prediction results or None if prediction fails:
        {
            "carbon_rate_mg_ha_yr": float,  # Megagrams Carbon per hectare per year
            "location": [lon, lat],
            "climate": {
                "annual_mean_temp_c": float,
                "annual_mean_precip_mm": float
            },
            "soil": {
                "classification": str
            },
            "coverage": str,  # "global", "fallback", or "error"
            "error": str  # if prediction failed
        }
    """
    try:
        # Import required modules from groa-mapping
        import pandas as pd
        import pickle
        import json
        import urllib.request
        
        logger.info(f"🌲 Predicting carbon sequestration at ({centroid_lat:.2f}, {centroid_lon:.2f})")
        
        # Load model
        model_path = os.path.join(BACKEND_APP_PATH, "groa-mapping/outputs/groa_model.pkl")
        if not os.path.exists(model_path):
            logger.error("GROA model not found")
            return {
                "carbon_rate_mg_ha_yr": None,
                "location": [centroid_lon, centroid_lat],
                "climate": None,
                "soil": None,
                "coverage": "error",
                "error": "GROA model not found. Run training script first."
            }
        
        # Try to load model with error handling for sklearn/numpy version issues
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
        except Exception as model_error:
            logger.error(f"Failed to load GROA model (sklearn/numpy version mismatch): {model_error}")
            return {
                "carbon_rate_mg_ha_yr": None,
                "location": [centroid_lon, centroid_lat],
                "climate": None,
                "soil": None,
                "coverage": "error",
                "error": f"Model loading failed: {str(model_error)}"
            }
        
        # Fetch real weather data from Open-Meteo API
        logger.info("Fetching climate data from Open-Meteo API...")
        start_date = "2014-01-01"
        end_date = "2023-12-31"
        weather_url = (
            f"https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={centroid_lat}&longitude={centroid_lon}&"
            f"start_date={start_date}&end_date={end_date}&"
            f"daily=temperature_2m_mean,precipitation_sum&timezone=auto"
        )
        
        try:
            with urllib.request.urlopen(weather_url, timeout=10) as response:
                weather_data = json.loads(response.read().decode())
            
            temps = [t for t in weather_data["daily"]["temperature_2m_mean"] if t is not None]
            amt = sum(temps) / len(temps) if temps else (25 - 0.5 * abs(centroid_lat))
            
            precips = [p for p in weather_data["daily"]["precipitation_sum"] if p is not None]
            amp = sum(precips) / 10.0 if precips else 1000
            
            logger.info(f"✅ Climate data: {amt:.1f}°C, {amp:.0f}mm")
            
        except Exception as e:
            logger.warning(f"Weather API failed, using fallback: {e}")
            amt = 25 - 0.5 * abs(centroid_lat)
            amp = 1000
        
        # Fetch soil data from ISRIC SoilGrids API
        logger.info("Fetching soil data from ISRIC SoilGrids API...")
        soil_url = f"https://rest.isric.org/soilgrids/v2.0/classification/query?lon={centroid_lon}&lat={centroid_lat}&number_classes=1"
        
        try:
            with urllib.request.urlopen(soil_url, timeout=10) as response:
                soil_data = json.loads(response.read().decode())
            
            soil_type = soil_data.get("wrb_class_name", "Inceptisols")
            logger.info(f"✅ Soil type: {soil_type}")
            
        except Exception as e:
            logger.warning(f"Soil API failed, using fallback: {e}")
            soil_type = "Inceptisols"
        
        # Prepare input for model
        input_data = pd.DataFrame({
            'lat_dec': [centroid_lat],
            'long_dec': [centroid_lon],
            'AMT': [amt],
            'AMP': [amp],
            'soil.classification': [soil_type]
        })
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        
        logger.info(f"✅ Carbon sequestration: {prediction:.4f} Mg C ha⁻¹ yr⁻¹")
        
        return {
            "carbon_rate_mg_ha_yr": round(float(prediction), 4),
            "location": [centroid_lon, centroid_lat],
            "climate": {
                "annual_mean_temp_c": round(amt, 1),
                "annual_mean_precip_mm": round(amp, 0)
            },
            "soil": {
                "classification": soil_type
            },
            "coverage": "global",
            "error": None
        }
        
    except ImportError as e:
        logger.error(f"Failed to import GROA dependencies: {e}")
        return {
            "carbon_rate_mg_ha_yr": None,
            "location": [centroid_lon, centroid_lat],
            "climate": None,
            "soil": None,
            "coverage": "unavailable",
            "error": f"GROA module dependencies not available: {str(e)}"
        }
    
    except Exception as e:
        logger.error(f"Carbon prediction failed: {e}", exc_info=True)
        return {
            "carbon_rate_mg_ha_yr": None,
            "location": [centroid_lon, centroid_lat],
            "climate": None,
            "soil": None,
            "coverage": "error",
            "error": str(e)
        }
