from fastapi import FastAPI, Query
import networkx as nx
import googlemaps
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Initialize Google Maps client
gmaps = googlemaps.Client(key=os.getenv("GMAPS_API_KEY"))

# Create a graph
graph = nx.Graph()

@app.get("/")
def read_root():
    return {"message": "Optimal Path Finder API is running!"}

@app.get("/shortest_path/")
def shortest_path(
    origin: str = Query(..., description="Start location"),
    destination: str = Query(..., description="End location"),
    algorithm: str = Query("dijkstra", description="Algorithm: dijkstra or astar")
):
    try:
        # Get coordinates for origin & destination
        origin_coords = gmaps.geocode(origin)[0]['geometry']['location']
        dest_coords = gmaps.geocode(destination)[0]['geometry']['location']

        # Convert to tuples
        start = (origin_coords['lat'], origin_coords['lng'])
        end = (dest_coords['lat'], dest_coords['lng'])

        # Compute shortest path
        if algorithm == "dijkstra":
            path = nx.shortest_path(graph, source=start, target=end, weight="weight")
        elif algorithm == "astar":
            path = nx.astar_path(graph, source=start, target=end, weight="weight")
        else:
            return {"error": "Invalid algorithm. Choose 'dijkstra' or 'astar'."}

        return {"path": path}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
