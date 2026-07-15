Real-Time Earthquake Streaming Pipeline

A scheduled, automated data ingestion pipeline built in Databricks, continuously pulling live, real-world data from the USGS Earthquake Hazards Program public API and appending it to a permanent, growing Delta table.

Overview

Unlike batch pipelines that process a complete, static file, this project ingests genuinely live data on a recurring schedule, demonstrating an incremental ("append-only") ingestion pattern commonly used in production data engineering when a true continuous streaming source (e.g., Kafka) isn't available or necessary.

Data Source

USGS Earthquake GeoJSON Feed — a free, public, no-authentication-required feed of real earthquakes from the past hour, refreshed continuously by the U.S. Geological Survey.

Architecture

USGS Live Feed (refreshed continuously)
        ↓
Databricks Job (scheduled every 5 minutes)
        ↓
Fetch → Parse → Extract fields
        ↓
Append to Delta table (earthquakes_stream)

Pipeline Steps


Fetch: Request the current GeoJSON feed via the requests library
Parse: Extract nested JSON fields (place, magnitude, time, tsunami flag) from each earthquake record
Transform: Convert the extracted records into a Spark DataFrame
Load: Append new records to a permanent Delta table using write.mode("append"), ensuring previously ingested data is never overwritten or lost


Automation

The pipeline is deployed as a Databricks Job with a recurring interval trigger, running automatically every 5 minutes without manual intervention — no code needs to be re-run by hand for new data to arrive.

Key Engineering Decisions


Append, not overwrite: since new earthquakes should accumulate over time rather than replace previous ones, append mode was used deliberately instead of the overwrite mode used in batch-style pipelines.
Polling over raw streaming: given the data source is a periodically-refreshed feed rather than a continuous socket/stream, a scheduled polling job is the appropriate and industry-common pattern, rather than forcing a more complex streaming framework onto a source that doesn't require it.


Tech Stack

Databricks · PySpark · Delta Lake · Python · Databricks Jobs (Lakeflow) · USGS Public API

Future Work


Convert the raw Unix timestamp field into a proper datetime type
Add deduplication logic to handle earthquakes that appear in multiple consecutive polling windows
Build a live dashboard visualizing recent seismic activity by magnitude and region.
