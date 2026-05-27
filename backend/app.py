from flask import Flask, jsonify, Response
from flask_cors import CORS
from database import get_connection
import json


app = Flask(__name__)
CORS(app)


def geojson_response(geojson_data):
    """
    Return a QGIS-friendly GeoJSON response.
    
    application/geo+json tells GIS clients that the response
    should be interpreted as GeoJSON.
    """
    
    return Response(
        json.dumps(geojson_data),
        mimetype="application/geo+json"
    )
    
    
@app.route("/")
def home():
    """
    Root endpoint.
    Used to check if the Flask API is running.
    """
    
    return jsonify({
        "message": "GmE 205 Laboratory 6 Flask API is running.",
        "available_endpoints": [
            "/api/parcels",
            "/api/parcels.geojson",
            "/api/roads",
            "/api/roads.geojson",
            "/api/layers"
        ],
        "qgis_recommended_endpoints": [
            "http://127.0.0.1:5000/api/parcels.geojson",
            "http://127.0.0.1:5000/api/roads.geojson"
        ]
    })
    

@app.route("/api/layers")
def get_layers():
    """
    Return basic metadata about available spatial layers.
    """

    return jsonify({
        "layers": [
            {
                "name": "parcel",
                "endpoint": "/api/parcels.geojson",
                "geometry_type": "MultiPolygon",
                "crs": "EPSG:4326"
            },
            {
                "name": "roads",
                "endpoint": "/api/roads.geojson",
                "geometry_type": "MultiLineString",
                "crs": "EPSG:4326"
            }
        ]
    })
    
    
@app.route("/api/parcels")
@app.route("/api/parcels.geojson")
def get_parcels():
    """
    Retrieve parcel records from PostGIS and return them as GeoJSON.
    
    ST_Force2D is used to remove Z values.
    This makes the GeoJSON easier for QGIS/GDAL to read through HTTP.
    """
    
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        query = """
            SELECT
            ASS_ACTUAL,
            ASS_CLASSI,
            ST_AsGeoJSON(ST_Force2D(geom)) AS geometry
            FROM parcel;
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        features = []
        for row in rows:
            feature = {
                "type": "Feature",
                "properties": {
                    "ASS_ACTUAL": row[0],
                    "ASS_CLASSI": row[1]
                },
                "geometry": json.loads(row[2])
            }
            
            features.append(feature)
            
        geojson = {
            "type": "FeatureCollection",
            "name": "parcel",
            "features": features
        }
        
        return geojson_response(geojson)
    
    except Exception as error:
        return jsonify({
            "error": "Failed to load parcel data.",
            "details": str(error)
        }), 500
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
            
@app.route("/api/roads")
@app.route("/api/roads.geojson")
def get_roads():
    """
    Retrieve road records from PostGIS and return them as GeoJSON.
    
    ST_Force2D is used to remove Z values.
    The column "road condi" must be quoted because it contains a space.
    """
    
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        query = """
            SELECT
                R_CLASS,
                S_Type,
                "road condi",
                ST_AsGeoJSON(ST_Force2D(geom)) AS geometry
            FROM roads;
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        features = []
        
        for row in rows:
            feature = {
                "type": "Feature",
                "properties": {
                    "R_CLASS": row[0],
                    "S_Type": row[1],
                    "ROAD_CONDI": row[2]
                },
                "geometry": json.loads(row[3])
            }
            
            features.append(feature)
            
        geojson = {
            "type": "FeatureCollection",
            "name": "roads",
            "features": features
        }
        
        return geojson_response(geojson)
    
    except Exception as error:
        return jsonify({
            "error": "Failed to load road data.",
            "details": str(error)
        }), 500
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
if __name__ == "__main__":
    app.run(debug=True)