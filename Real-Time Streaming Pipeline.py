# Databricks notebook source
import requests 

url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
response = requests.get(url)
data = response.json()

print(data)

# COMMAND ----------

earthquakes = data['features']

for quake in earthquakes:
    print(quake['properties']['place'], quake['properties']['mag'])

# COMMAND ----------

rows = []
for quake in earthquakes:
    rows.append({
    "place":quake['properties']['place'],
    "magnitude": quake['properties']['mag'],
    "time_raw":quake['properties']['time'],
    "tsunami_flag": quake['properties']['tsunami']
})

earthquakes_df = spark.createDataFrame(rows)
earthquakes_df.display()

# COMMAND ----------

earthquakes_df.write.mode("append").saveAsTable("earthquake_stream")

# COMMAND ----------

url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
response = requests.get(url)
data = response.json()
earthquakees = data['features']

rows = []
for quake in earthquakees:
    rows.append({
        "place": quake['properties']['place'],
        "magnitude": quake['properties']['mag'],
        "time_raw": quake['properties']['time'],
        "tsunami_flag": quake['properties']['tsunami']
    })

earthquakes_df = spark.createDataFrame(rows)
earthquakes_df.write.mode("append").saveAsTable("earthquakes_stream")

print(f"Saved {len(rows)} earthquakes at this check-in.")


# COMMAND ----------


