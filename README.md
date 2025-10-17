# Open-Meteo Exporter

Prometheus exporter for Open-Meteo weather data. Fetches current weather conditions from the Open-Meteo API and exposes them as Prometheus metrics.

## Features

- Exports current weather data for multiple locations
- Configurable scrape intervals
- Built-in monitoring metrics for scrape health
- Docker support

## Configuration

### Exporter Configuration

Create a `config.yaml` file:

```yaml
# Port for Prometheus metrics endpoint
port: 9091

# Scrape interval in seconds (900 = 15 minutes)
scrape_interval: 900
```

### Location Configuration

Create a `locations/config.yaml` file:

```yaml
locations:
  - name: "London"
    lat: 51.5074
    lon: -0.1278
  - name: "New York"
    lat: 40.7128
    lon: -74.0060
```

## Metrics

All metrics include labels: `lat`, `lon`, `name`

### Weather Metrics

| Metric | Description | Unit |
|--------|-------------|------|
| `openmeteo_temperature_celsius` | Temperature at 2 meters | Celsius |
| `openmeteo_apparent_temperature_celsius` | Feels-like temperature | Celsius |
| `openmeteo_relative_humidity_percent` | Relative humidity | Percent |
| `openmeteo_precipitation_mm` | Total precipitation | Millimeters |
| `openmeteo_rain_mm` | Rain amount | Millimeters |
| `openmeteo_showers_mm` | Shower amount | Millimeters |
| `openmeteo_snowfall_cm` | Snowfall amount | Centimeters |
| `openmeteo_weather_code` | WMO Weather interpretation code | Code |
| `openmeteo_cloud_cover_percent` | Cloud cover | Percent |
| `openmeteo_pressure_msl_hpa` | Atmospheric pressure at mean sea level | hPa |
| `openmeteo_surface_pressure_hpa` | Surface atmospheric pressure | hPa |
| `openmeteo_wind_speed_kmh` | Wind speed at 10 meters | km/h |
| `openmeteo_wind_direction_degrees` | Wind direction at 10 meters | Degrees (0-360) |
| `openmeteo_wind_gusts_kmh` | Wind gusts at 10 meters | km/h |
| `openmeteo_visibility_meters` | Visibility distance | Meters |
| `openmeteo_is_day` | Day (1) or night (0) indicator | Boolean |

### Monitoring Metrics

| Metric | Description | Type |
|--------|-------------|------|
| `openmeteo_last_scrape_timestamp` | Unix timestamp of last successful scrape | Gauge |
| `openmeteo_scrape_success` | Last scrape success status (0 or 1) | Gauge |
| `openmeteo_scrape_errors_total` | Total number of scrape errors | Counter |

## Usage

### Running Locally

```bash
python exporter.py config.yaml
```

### Running with Docker

Build the image:

```bash
docker build -t openmeteo-exporter .
```

Run the container:

```bash
docker run -d \
  -p 9091:9091 \
  -v /path/to/config:/config \
  openmeteo-exporter
```

### Prometheus Configuration

Add to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'openmeteo'
    static_configs:
      - targets: ['localhost:9091']
```

## Requirements

- Python 3.9 or higher
- Dependencies listed in `pyproject.toml`

## API

Uses the Open-Meteo API (https://open-meteo.com), which is free and requires no API key.

## License

See LICENSE file for details.
