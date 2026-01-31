from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.coordinate_parser import parse_to_geojson
from services.sentinel_client import fetch_satellite_image
from services.gee_bridge import call_backend_rusle
import schemas

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.post("/api/rusle", response_model=schemas.RUSLEResponse)
async def compute_rusle(request: schemas.RUSLERequest):
    # 1. Parse coordinates → GeoJSON
    try:
        geojson = parse_to_geojson(request.coordinates)
        if geojson['area_km2'] > 1000:
            raise HTTPException(400, "Area too large (>1000 km²)")
    except Exception as e:
        raise HTTPException(400, f"Invalid polygon: {e}")
    
    # 2. Fetch satellite image (parallel with RUSLE)
    satellite_task = fetch_satellite_image(geojson, request.options.date_range)
    
    # 3. Call backend/ML for RUSLE computation
    rusle_result = await call_backend_rusle(geojson, request.options)
    
    # 4. Merge results
    satellite_img = await satellite_task
    return {
        "polygon": geojson,
        "satellite_image": satellite_img,  # Base64 or URL
        "erosion": rusle_result['erosion'],
        "factors": rusle_result['factors'],
        "highlights": rusle_result['hotspots'],
        "validation": rusle_result['sensitivity']
    }
