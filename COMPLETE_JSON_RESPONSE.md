# Complete JSON Response Structure

This document shows the **single JSON object** sent from the middleware to the frontend containing ALL data from RUSLE, satellite imagery, crop prediction, and carbon sequestration models.

## Full Response Schema

```json
{
  "success": true,
  "computation_time_sec": 3.24,
  "timestamp": "2026-02-01T04:20:00.000000",
  
  // ============ POLYGON METADATA ============
  "polygon": {
    "type": "Feature",
    "geometry": {
      "type": "Polygon",
      "coordinates": [
        [[-1.5, 52.0], [-1.4, 52.0], [-1.45, 52.05], [-1.5, 52.0]]
      ]
    },
    "properties": {
      "centroid": [-1.45, 52.02],
      "bbox": [-1.5, 52.0, -1.4, 52.05],
      "area_hectares": 1910.01
    }
  },
  
  "polygon_metadata": {
    "area_km2": 19.10,
    "centroid": [-1.45, 52.02],
    "bbox": [-1.5, 52.0, -1.4, 52.05],
    "num_vertices": 4
  },
  
  // ============ SATELLITE IMAGERY ============
  "satellite_image": "data:image/png;base64,iVBORw0KGgoAAAANSU...[602KB of base64 data]",
  
  // ============ RUSLE EROSION ANALYSIS ============
  "erosion": {
    "mean": 4.44,
    "max": 15.23,
    "min": 0.82,
    "stddev": 3.12,
    "p50": 3.98,
    "p95": 11.76,
    "total_soil_loss_tonnes": 8485.64
  },
  
  "factors": {
    "R": {
      "mean": 1850.5,
      "stddev": 120.3,
      "min": 1620.0,
      "max": 2100.0,
      "unit": "MJ mm ha⁻¹ h⁻¹ yr⁻¹",
      "contribution_pct": 35.2,
      "source": "ERA5 rainfall data"
    },
    "K": {
      "mean": 0.030,
      "stddev": 0.005,
      "min": 0.025,
      "max": 0.038,
      "unit": "t ha h ha⁻¹ MJ⁻¹ mm⁻¹",
      "contribution_pct": 15.8,
      "source": "Regional defaults (UK/Northern Europe)"
    },
    "LS": {
      "mean": 2.45,
      "stddev": 1.82,
      "min": 0.1,
      "max": 8.92,
      "unit": "dimensionless",
      "contribution_pct": 42.1,
      "source": "NASA SRTM DEM"
    },
    "C": {
      "mean": 0.08,
      "stddev": 0.04,
      "min": 0.02,
      "max": 0.18,
      "unit": "dimensionless",
      "contribution_pct": 25.4,
      "source": "Sentinel-2 NDVI"
    },
    "P": {
      "mean": 1.0,
      "stddev": 0.0,
      "min": 1.0,
      "max": 1.0,
      "unit": "dimensionless",
      "contribution_pct": 0.0,
      "source": "No conservation practices"
    }
  },
  
  // ============ HOTSPOTS (ML-flagged high-risk areas) ============
  "highlights": [
    {
      "id": "hotspot_1",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[-1.48, 52.03], [-1.47, 52.03], [-1.47, 52.04], [-1.48, 52.04], [-1.48, 52.03]]]
      },
      "properties": {
        "area_ha": 12.4,
        "mean_erosion": 28.5,
        "max_erosion": 45.2,
        "dominant_factor": "LS"
      },
      "reason": "Steep slope (LS > 5.0) + Low vegetation cover (C > 0.12)",
      "severity": "high"
    },
    {
      "id": "hotspot_2",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[-1.42, 52.01], [-1.41, 52.01], [-1.41, 52.02], [-1.42, 52.02], [-1.42, 52.01]]]
      },
      "properties": {
        "area_ha": 8.7,
        "mean_erosion": 32.1,
        "max_erosion": 38.9,
        "dominant_factor": "C"
      },
      "reason": "Bare soil detected (C > 0.15) + Moderate slope (LS > 2.0)",
      "severity": "high"
    }
  ],
  
  "num_hotspots": 2,
  
  // ============ VALIDATION METRICS ============
  "validation": {
    "high_veg_reduction_pct": 68.2,
    "flat_terrain_reduction_pct": 85.1,
    "bare_soil_increase_pct": 230.5,
    "model_valid": true,
    "notes": "All sensitivity tests passed expected ranges"
  },
  
  // ============ CROP YIELD PREDICTION (NEW!) ============
  "crop_yield": {
    "yield_t_ha": 5.44,
    "crop_name": "Soft wheat",
    "location": [-1.45, 52.02],
    "week": 25,
    "coverage": "europe",
    "error": null
  },
  
  // ============ CARBON SEQUESTRATION (NEW!) ============
  "carbon_sequestration": {
    "carbon_rate_mg_ha_yr": 1.4977,
    "location": [-1.45, 52.02],
    "climate": {
      "annual_mean_temp_c": 10.2,
      "annual_mean_precip_mm": 785.0
    },
    "soil": {
      "classification": "Cambisols"
    },
    "coverage": "global",
    "error": null
  },
  
  // ============ OPTIONAL: MAP TILES ============
  "tile_urls": null
}
```

## Response Breakdown

### 1. **RUSLE Erosion Data** (existing)
- `erosion`: Statistical summary (mean, max, min, std, percentiles)
- `factors`: Individual RUSLE factors (R, K, LS, C, P) with sources
- `highlights`: ML-detected high-risk hotspot polygons
- `validation`: Model sensitivity metrics

### 2. **Satellite Imagery** (existing)
- `satellite_image`: Base64-encoded PNG from Sentinel-2
- 512x512 RGB image centered on polygon
- Used as map background in frontend

### 3. **Crop Yield Prediction** (NEW!)
- `crop_yield.yield_t_ha`: Predicted yield in tonnes/hectare
- `crop_yield.crop_name`: Crop type (Soft wheat, Durum wheat, Total wheat)
- `crop_yield.coverage`: "europe" if data available, "out_of_coverage" if not
- `crop_yield.error`: null if successful, error message if failed

### 4. **Carbon Sequestration** (NEW!)
- `carbon_sequestration.carbon_rate_mg_ha_yr`: Carbon accumulation rate
- `carbon_sequestration.climate`: 10-year average temperature and precipitation
- `carbon_sequestration.soil`: Soil classification from SoilGrids
- `carbon_sequestration.coverage`: "global" (works worldwide)
- `carbon_sequestration.error`: null if successful, error message if failed

## Frontend Integration

The frontend receives this **single JSON object** and can display:

### Existing Features:
- ✅ Erosion heatmap overlay
- ✅ Factor breakdowns (R, K, LS, C, P)
- ✅ Hotspot markers with explanations
- ✅ Satellite background imagery

### New Features to Add:
- 🌾 **Crop Yield Card** (show only if `crop_yield.coverage === "europe"`)
  ```typescript
  if (response.crop_yield?.yield_t_ha) {
    <Card>
      <CardTitle>🌾 Crop Yield Forecast</CardTitle>
      <p>{response.crop_yield.yield_t_ha} t/ha</p>
      <p>{response.crop_yield.crop_name}</p>
    </Card>
  }
  ```

- 🌲 **Carbon Potential Card** (show for all locations)
  ```typescript
  if (response.carbon_sequestration?.carbon_rate_mg_ha_yr) {
    <Card>
      <CardTitle>🌲 Forest Carbon Potential</CardTitle>
      <p>{response.carbon_sequestration.carbon_rate_mg_ha_yr} Mg C/ha/yr</p>
      <p>Temp: {response.carbon_sequestration.climate.annual_mean_temp_c}°C</p>
      <p>Rainfall: {response.carbon_sequestration.climate.annual_mean_precip_mm}mm</p>
      <p>Soil: {response.carbon_sequestration.soil.classification}</p>
    </Card>
  }
  ```

## Error Handling

All sections are optional - if a service fails:
- `crop_yield`: Will have `error` field populated, `yield_t_ha` = null
- `carbon_sequestration`: Will have `error` field populated, `carbon_rate_mg_ha_yr` = null
- `satellite_image`: Falls back to 1x1 transparent PNG
- `erosion`: If RUSLE fails, entire response has `success: false`

The frontend should check for null values and show appropriate fallback UI.

## API Endpoint

**Single endpoint** returns everything:
```
POST /polygon
Content-Type: application/json

{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[lon, lat], ...]]
  },
  "properties": {}
}
```

**Response**: One complete JSON object with all data (RUSLE + Satellite + Crop + Carbon)
