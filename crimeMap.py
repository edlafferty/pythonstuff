#! /usr/bin/python3

# Import modules
import folium
import folium.plugins as plugins # import special to get around folium bug
import pandas
import os
os.chdir("C:\\Users\\edlaf\\Documents\\pythonstuff\\map_env")


# Set up maps, feature group, and overlays
NYC_map = folium.Map(location=[40.71,-73.30], zoom_start=12)
NYC_map.add_tile_layer()
crime_group = folium.FeatureGroup(name="Crime")
crime_Fig = folium.Figure(title="New York City Crimes Committed Map")
crime_Fig.add_child(NYC_map)
marker_cluster_w = folium.plugins.MarkerCluster(name="Weapons crimes")
marker_cluster_l = folium.plugins.MarkerCluster(name="Larceny crimes")
marker_cluster_d = folium.plugins.MarkerCluster(name="Drug crimes")
marker_cluster_m = folium.plugins.MarkerCluster(name="Mischief crimes")
marker_cluster_r = folium.plugins.MarkerCluster(name="Rape crimes")
marker_cluster_h = folium.plugins.MarkerCluster(name="Harassment crimes")
marker_cluster_o = folium.plugins.MarkerCluster(name="Other crimes")
marker_cluster_v = folium.plugins.MarkerCluster(name="Volcanoes")


# Read in data to a dataframe
NYCcrimedata=pandas.read_csv('Crime_Map_NYC.csv')
USVolcanoedata=pandas.read_csv('Volcanoes_USA.txt')


def pop_Map(marker, crimeType):
    """Add markers to overlays based upon crime type
    
    Arguments: 
      marker: folium marker object to place on overlay
      crimeType: Category of crime committed
    """
    if "WEAPON" in crimeType:
        marker_cluster_w.add_child(marker)
    elif "LARCENY" in crimeType:
        marker_cluster_l.add_child(marker)
    elif "CONTROLLED SUB" in crimeType or "MARIJUANA" in crimeType:
        marker_cluster_d.add_child(marker)
    elif "MISCHIEF" in crimeType:
        marker_cluster_m.add_child(marker)
    elif "RAPE" in crimeType:
        marker_cluster_r.add_child(marker)
    elif "HARASS" in crimeType:
        marker_cluster_h.add_child(marker)
    else:
        marker_cluster_o.add_child(marker)
    return()


def crime_Color(crimeType):
    """Choose approriate color for marker based upon crime type
    
    Arguments: 
      crimeType: Category of crime committed
    """
    if "WEAPON" in crimeType:
        crimeColor="blue"
    elif "LARCENY" in crimeType:
        crimeColor="cadetblue"
    elif "CONTROLLED SUB" in crimeType or "MARIJUANA" in crimeType:
        crimeColor="darkblue"
    elif "MISCHIEF" in crimeType:
        crimeColor="lightblue"
    elif "RAPE" in crimeType:
        crimeColor="red"
    elif "HARASS" in crimeType:
        crimeColor="darkred"
    else:
        crimeColor="lightred"
    return(crimeColor)


# Create markers for crime, by category, and place on the appropriate overlay map
for crime_loc in NYCcrimedata[0:100].iterrows():
    lit_Marker = folium.Marker(location=[crime_loc[1]['Latitude'],crime_loc[1]['Longitude']], 
                      popup=crime_loc[1]['PD_DESC'], 
                      icon=folium.Icon(color=crime_Color(crime_loc[1]['PD_DESC'])))
    pop_Map(lit_Marker,crime_loc[1]['PD_DESC'])
for volcanoe_loc in USVolcanoedata[0:100].iterrows():
    lit_Marker = folium.CircleMarker(location=[volcanoe_loc[1]['LAT'],volcanoe_loc[1]['LON']], 
                      popup="Name: " + volcanoe_loc[1]['NAME']+"\n"+"Loc: "+volcanoe_loc[1]['LOCATION'], 
                      fill_color="beige", color="grey", fill_opacity=0.7)
#                      icon=folium.Icon(color="beige"))
    marker_cluster_v.add_child(lit_Marker)
    

# Add overlay maps to main map
NYC_map.add_child(marker_cluster_w)
NYC_map.add_child(marker_cluster_m)
NYC_map.add_child(marker_cluster_d)
NYC_map.add_child(marker_cluster_l)
NYC_map.add_child(marker_cluster_r)
NYC_map.add_child(marker_cluster_h)
NYC_map.add_child(marker_cluster_o)
#NYC_map.add_child(marker_cluster_v)
# Add layer control object to main map ans create/save map
NYC_map.add_child(folium.LayerControl())
NYC_map.save("MainMap.html")