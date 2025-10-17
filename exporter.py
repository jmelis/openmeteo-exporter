#!/usr/bin/env python3
"""
Open-Meteo Prometheus Exporter

Fetches current weather data from Open-Meteo API and exports it as Prometheus metrics.
"""

import sys
import time
import logging
from typing import Dict, List

import yaml
import requests
from prometheus_client import start_http_server, Gauge, Counter


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OpenMeteoExporter:
    """Prometheus exporter for Open-Meteo weather data"""

    API_BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self):
        # Weather metrics
        self.temperature = Gauge(
            'openmeteo_temperature_celsius',
            'Temperature at 2 meters in Celsius',
            ['lat', 'lon', 'name']
        )

        self.relative_humidity = Gauge(
            'openmeteo_relative_humidity_percent',
            'Relative humidity percentage',
            ['lat', 'lon', 'name']
        )

        self.apparent_temperature = Gauge(
            'openmeteo_apparent_temperature_celsius',
            'Apparent/feels-like temperature in Celsius',
            ['lat', 'lon', 'name']
        )

        self.precipitation = Gauge(
            'openmeteo_precipitation_mm',
            'Total precipitation in millimeters',
            ['lat', 'lon', 'name']
        )

        self.rain = Gauge(
            'openmeteo_rain_mm',
            'Rain amount in millimeters',
            ['lat', 'lon', 'name']
        )

        self.showers = Gauge(
            'openmeteo_showers_mm',
            'Shower amount in millimeters',
            ['lat', 'lon', 'name']
        )

        self.snowfall = Gauge(
            'openmeteo_snowfall_cm',
            'Snowfall amount in centimeters',
            ['lat', 'lon', 'name']
        )

        self.weather_code = Gauge(
            'openmeteo_weather_code',
            'WMO Weather interpretation code',
            ['lat', 'lon', 'name']
        )

        self.cloud_cover = Gauge(
            'openmeteo_cloud_cover_percent',
            'Cloud cover percentage',
            ['lat', 'lon', 'name']
        )

        self.pressure_msl = Gauge(
            'openmeteo_pressure_msl_hpa',
            'Atmospheric pressure at mean sea level in hPa',
            ['lat', 'lon', 'name']
        )

        self.surface_pressure = Gauge(
            'openmeteo_surface_pressure_hpa',
            'Surface atmospheric pressure in hPa',
            ['lat', 'lon', 'name']
        )

        self.wind_speed = Gauge(
            'openmeteo_wind_speed_kmh',
            'Wind speed at 10 meters in km/h',
            ['lat', 'lon', 'name']
        )

        self.wind_direction = Gauge(
            'openmeteo_wind_direction_degrees',
            'Wind direction at 10 meters in degrees (0-360)',
            ['lat', 'lon', 'name']
        )

        self.wind_gusts = Gauge(
            'openmeteo_wind_gusts_kmh',
            'Wind gusts at 10 meters in km/h',
            ['lat', 'lon', 'name']
        )

        self.visibility = Gauge(
            'openmeteo_visibility_meters',
            'Visibility distance in meters',
            ['lat', 'lon', 'name']
        )

        self.is_day = Gauge(
            'openmeteo_is_day',
            'Whether it is day (1) or night (0)',
            ['lat', 'lon', 'name']
        )

        # Monitoring metrics
        self.last_scrape_timestamp = Gauge(
            'openmeteo_last_scrape_timestamp',
            'Unix timestamp of the last successful scrape',
            ['lat', 'lon', 'name']
        )

        self.scrape_success = Gauge(
            'openmeteo_scrape_success',
            'Whether the last scrape was successful (0 or 1)',
            ['lat', 'lon', 'name']
        )

        self.scrape_errors_total = Counter(
            'openmeteo_scrape_errors_total',
            'Total number of scrape errors',
            ['lat', 'lon', 'name']
        )

    def fetch_weather_data(self, lat: float, lon: float) -> Dict:
        """
        Fetch current weather data from Open-Meteo API

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            API response dictionary
        """
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': ','.join([
                'temperature_2m',
                'relative_humidity_2m',
                'apparent_temperature',
                'precipitation',
                'rain',
                'showers',
                'snowfall',
                'weather_code',
                'cloud_cover',
                'pressure_msl',
                'surface_pressure',
                'wind_speed_10m',
                'wind_direction_10m',
                'wind_gusts_10m',
                'visibility',
                'is_day'
            ])
        }

        response = requests.get(self.API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def collect_metrics_for_location(self, lat: float, lon: float, name: str) -> None:
        """Collect weather metrics for a specific location"""
        try:
            logger.info(f"Collecting weather data for {name} ({lat}, {lon})")

            data = self.fetch_weather_data(lat, lon)

            if 'current' not in data:
                logger.warning(f"No current weather data in API response for {name}")
                self.scrape_success.labels(lat=str(lat), lon=str(lon), name=name).set(0)
                return

            current = data['current']

            # Set all weather metrics
            labels = {'lat': str(lat), 'lon': str(lon), 'name': name}

            self.temperature.labels(**labels).set(current.get('temperature_2m', 0))
            self.relative_humidity.labels(**labels).set(current.get('relative_humidity_2m', 0))
            self.apparent_temperature.labels(**labels).set(current.get('apparent_temperature', 0))
            self.precipitation.labels(**labels).set(current.get('precipitation', 0))
            self.rain.labels(**labels).set(current.get('rain', 0))
            self.showers.labels(**labels).set(current.get('showers', 0))
            self.snowfall.labels(**labels).set(current.get('snowfall', 0))
            self.weather_code.labels(**labels).set(current.get('weather_code', 0))
            self.cloud_cover.labels(**labels).set(current.get('cloud_cover', 0))
            self.pressure_msl.labels(**labels).set(current.get('pressure_msl', 0))
            self.surface_pressure.labels(**labels).set(current.get('surface_pressure', 0))
            self.wind_speed.labels(**labels).set(current.get('wind_speed_10m', 0))
            self.wind_direction.labels(**labels).set(current.get('wind_direction_10m', 0))
            self.wind_gusts.labels(**labels).set(current.get('wind_gusts_10m', 0))
            self.visibility.labels(**labels).set(current.get('visibility', 0))
            self.is_day.labels(**labels).set(current.get('is_day', 0))

            # Update monitoring metrics
            self.last_scrape_timestamp.labels(**labels).set(time.time())
            self.scrape_success.labels(**labels).set(1)

            logger.info(f"Successfully collected weather data for {name}")

        except Exception as e:
            logger.error(f"Error collecting metrics for {name} ({lat}, {lon}): {e}")
            labels = {'lat': str(lat), 'lon': str(lon), 'name': name}
            self.scrape_errors_total.labels(**labels).inc()
            self.scrape_success.labels(**labels).set(0)

    def collect_all_locations(self, locations: List[Dict]) -> None:
        """Collect metrics for all configured locations"""
        for location in locations:
            lat = location['lat']
            lon = location['lon']
            name = location.get('name', f"{lat},{lon}")
            self.collect_metrics_for_location(lat, lon, name)


def load_config(config_path: str) -> Dict:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Loaded configuration from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    # Default config path
    config_path = sys.argv[1] if len(sys.argv) > 1 else '/config/config.yaml'
    locations_path = '/config/locations/config.yaml'

    # Load exporter config
    config = load_config(config_path)
    port = config.get('port', 9091)
    scrape_interval = config.get('scrape_interval', 900)  # 15 minutes default

    # Load locations
    locations_config = load_config(locations_path)
    locations = locations_config.get('locations', [])

    if not locations:
        logger.error("No locations configured in locations config file")
        sys.exit(1)

    logger.info(f"Starting Open-Meteo Exporter on port {port}")
    logger.info(f"Scrape interval: {scrape_interval} seconds")
    logger.info(f"Monitoring {len(locations)} location(s)")

    # Initialize exporter
    exporter = OpenMeteoExporter()

    # Start Prometheus HTTP server
    start_http_server(port)
    logger.info(f"Prometheus metrics available at http://localhost:{port}/metrics")

    # Main collection loop
    while True:
        try:
            exporter.collect_all_locations(locations)
        except Exception as e:
            logger.error(f"Error in collection loop: {e}")

        time.sleep(scrape_interval)


if __name__ == '__main__':
    main()
