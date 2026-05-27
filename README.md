# GmE 205 – Laboratory Exercise 7

## Overview

---

## Environment Setup

---

## How to Run

---

## Outputs

---

## Reflection

1. What role does PostGIS play in this architecture?

   PostGIS serves as the data source.

2. What role does Flask play in this laboratory?

   Flask is the API Layer serving as the middle man between the source PostGIS and the applicaiton that needs the data from PostGIS.

3. Why is GeoJSON useful for spatial web services?

   JSON is the standard format for transactions in the web. GeoJSON is just an extension of JSON with spatial components.

4. How does ST_AsGeoJSON() support distributed GIS?

   ST_AsGeoJSON makes it easy for PostGIS to convert the geometry information into GeoJSON, a format that is ideal for transferring spatial vector data over the web.

5. Why is QGIS considered a heavy client?

   QGIS is considered a heavy client because of the many features and capabilities the application has.

6. Why is a REST API better than manually exporting shapefiles?

   Using REST API instead of manually exporting shapefiles is more convenient since no file transfer needs to happen and more robust in terms of data integrity since the source of truth for the data will be on the source of the REST API unlike on exporting shapefiles where the exported shapefile can become stale.

7. How does this laboratory demonstrate distributed geospatial computing?

   This laboratory excercise demonstrated that geospatial resources can come from different/distributed sources by having the source be stored in a database, and the access of the source be managed by an API layer and the actual processing of the souce data manage by the QGIS application.

8. What advantages does service-based GIS architecture provide?

   Service-based GIS archhitecture makes it so that each component of the GIS stack can specialize on their field. For example, GIS data stores can specialize in the storage and management of data, API layers can specialize in bridging the data from the source to the application and applications can specialize in spatial processes without worryiing how the spatial data they are processing is stored.

9. How does this architecture support scalability in spatial systems?

   Since the resources needed is distributed, each component of the spatial systems can be scaled independently of other components.

---
