import googlemaps
from typing import List
import polyline
import folium

class Map():
    def __init__(self, start: str, end: str, waypoints: List[str], transportation: str, api_key):
        self.gmaps = googlemaps.Client(key=api_key)
        self.start_name = start
        self.end_name = end
        self.waypoints_names = waypoints
        self.transportation = transportation

    def get_direction(self):
        return self.gmaps.directions(
            self.start_name, 
            self.end_name,
            waypoints=self.waypoints_names,
            optimize_waypoints=True,  # This will optimize the order of waypoints
            mode=self.transportation)
        
        # Extract route information
    def draw_map(self):
        directions_result = self.get_direction()
        route = directions_result[0]['legs']
        start_location = route[0]['start_location']
        end_location = route[-1]['end_location']
        overview_polyline = directions_result[0]['overview_polyline']['points']

        # Decode the polyline to get coordinates
        waypoints_coordinates = polyline.decode(overview_polyline)

        # Create a map centered on the midpoint of the route
        center_lat = (start_location['lat'] + end_location['lat']) / 2
        center_lng = (start_location['lng'] + end_location['lng']) / 2
        m = folium.Map(location=[center_lat, center_lng], zoom_start=5)

        # Add markers for start and end points
        folium.Marker(
            [start_location['lat'], start_location['lng']],
            popup='Start: ' + self.start_name,
            icon=folium.Icon(color='green', icon='play')
        ).add_to(m)

        folium.Marker(
            [end_location['lat'], end_location['lng']],
            popup='End: ' + self.end_name,
            icon=folium.Icon(color='red', icon='stop')
        ).add_to(m)

        for i, leg in enumerate(route[:-1]):  # Exclude the last leg
            end_loc = leg['end_location']
            folium.Marker(
                [end_loc['lat'], end_loc['lng']],
                popup=f'Stop: \n{self.waypoints_names[i]}',
                icon=folium.Icon(color='blue', icon='flag')
            ).add_to(m)
        
        # Draw the route line
        folium.PolyLine(
            locations=waypoints_coordinates,
            weight=5,
            color='blue',
            opacity=0.8
        ).add_to(m)

        # Save the map
        m.save('./templates/route_map.html')
        




        


