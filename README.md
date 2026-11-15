---
title: Harvest Atlas
emoji: 🌱
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: NASA-powered crop rotation decision lab
---

# Harvest Atlas

NASA-powered crop-rotation decision support.

Pick a field on the map (or use GPS), set your priorities and soil context, and get:

- NASA POWER agro-climatology (temperature, rainfall, humidity, root-zone wetness,
  solar radiation, wind, growing degree days)
- Measured 0-30 cm soil texture, pH, organic carbon and bulk density from
  OpenLandMap SoilDB via OpenGeoHub TiTiler
- Optional NASA AppEEARS satellite samples (MODIS NDVI, land-surface temperature,
  SMAP soil moisture)
- A field vulnerability diagnosis (heat, water, erosion, volatility, soil)
- Three AI rotation scenarios scored against your current-practice baseline

## Data sources

- NASA POWER - https://power.larc.nasa.gov (free, no key)
- NASA GIBS - https://gibs.earthdata.nasa.gov (MODIS Terra overlays)
- OpenLandMap SoilDB - https://openlandmap.org (CC-BY 4.0)
- NASA AppEEARS - optional, needs free Earthdata Login
- OpenStreetMap Nominatim - reverse geocoding

## Configuration

Set these as **Space secrets** (Settings -> Variables and secrets):

| Secret | Required | Purpose |
|---|---|---|
| `GROQ_API_KEY` | yes, for the 3 AI scenarios | Groq API key |
| `GROQ_API_KEY_2` | optional | Fallback on rate limit |
| `GROQ_MODEL` | optional | Default `openai/gpt-oss-120b` |
| `EARTHDATA_USERNAME` | optional | NASA AppEEARS samples |
| `EARTHDATA_PASSWORD` | optional | NASA AppEEARS samples |

Without a Groq key the map and NASA diagnostics still work; only the AI scenario
comparison is unavailable.

## Run locally

```
pip install -r requirements.txt
python serve.py
```

Do not run `python main.py` on a server: its `main()` starts an interactive
terminal chat loop and will block or exit. Use `serve.py`.
