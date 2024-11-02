import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

def euclidean_distance(p1, p2):
    """ Calculate Euclidean distance between two points. """
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def find_best_label_position(node, pos, G, distance_offset=0.03, perpendicular_offset=0.13):
    """ Find the best label position around a node with an angle parallel to the closest edge. """
    x0, y0 = pos[node]
    # Find nearest neighbor to determine direction
    nearest_neighbor = min(G.neighbors(node), key=lambda n: euclidean_distance(pos[node], pos[n]), default=None)
    
    if not nearest_neighbor:
        return (x0, y0), 0

    # Calculate angle and position offset
    x1, y1 = pos[nearest_neighbor]
    angle = np.arctan2(y1 - y0, x1 - x0)
    perp_angle = angle + np.pi / 2
    label_x = x0 + distance_offset * np.cos(angle) + perpendicular_offset * np.cos(perp_angle)
    label_y = y0 + distance_offset * np.sin(angle) + perpendicular_offset * np.sin(perp_angle)
    
    # Convert angle to degrees and correct if upside down
    angle_deg = np.degrees(angle)
    if angle_deg > 90 or angle_deg < -90:
        angle_deg += 180

    return (label_x, label_y), angle_deg

class TubeMap:
    def __init__(self, data_file, line_colors):
        self.data_file = data_file
        self.line_colors = line_colors
        self.G = nx.Graph()
        self.pos = {}

    def load_data(self):
        """ Load the tube line data from a CSV file into the graph. """
        data = pd.read_csv(self.data_file)
        
        for _, row in data.iterrows():
            # Add nodes with positions and line color
            self.G.add_node(row['From Station'], pos=(row['Longitude_From'], row['Latitude_From']), line=row['Tube Line'])
            self.G.add_node(row['To Station'], pos=(row['Longitude_To'], row['Latitude_To']), line=row['Tube Line'])
            
            # Add edges with distance and line information
            self.G.add_edge(
                row['From Station'], 
                row['To Station'], 
                weight=row['Distance (km)'], 
                line=row['Tube Line']
            )

        # Extract positions for plotting
        self.pos = nx.get_node_attributes(self.G, 'pos')

    def plot_map(self, scale_factor=(1.5, 1.2)):
        """ Plot the tube map with nodes, edges, and central labels for each line. """
        # Scale positions independently for x and y axis
        scaled_pos = {station: (lon * scale_factor[0], lat * scale_factor[1]) for station, (lon, lat) in self.pos.items()}

        # Draw edges with line colors
        for line, color in self.line_colors.items():
            edges = [(u, v) for u, v, d in self.G.edges(data=True) if d['line'] == line]
            nx.draw_networkx_edges(self.G, scaled_pos, edgelist=edges, edge_color=color, width=4, alpha=0.8, label=line)

            # Draw nodes with line colors
            nodes = [node for node, data in self.G.nodes(data=True) if data['line'] == line]
            nx.draw_networkx_nodes(self.G, scaled_pos, nodelist=nodes, node_color=color, node_size=100)

        # Add node labels with calculated offsets and angles
        for station in self.pos:
            (lx, ly), angle = find_best_label_position(station, scaled_pos, self.G, distance_offset=0.0001, perpendicular_offset=0.0001)
            plt.text(lx, ly, station, fontsize=10, ha='center', color='black', rotation=angle, rotation_mode='anchor')

    def plot_line_labels(self, line_key_stations):
        """ Plot central labels for each line separately. """
        for line, key_station in line_key_stations.items():
            lon, lat = self.pos.get(key_station, (0, 0))
            scaled_lon, scaled_lat = lon * 1.5, lat * 1.2  # Adjust scaling if needed
            plt.text(scaled_lon, scaled_lat, line, fontsize=12, ha='center', color=self.line_colors[line], weight='bold')


# Define line colors and key stations
line_colors = {
    "Central": "Blue", 
    "Jubilee": "Gray", 
    "Piccadilly": "Green", 
    "Circle": "Purple"
}

# Create a TubeMap object and plot the map
tube_map = TubeMap(data_file='Task2Data/data.csv', line_colors=line_colors)
tube_map.load_data()

plt.figure(figsize=(12, 8))
tube_map.plot_map(scale_factor=(0.05, 0.05))  # Scale x and y independently for better spread

plt.title("Partition of London Tube Map")
plt.axis('equal')  # Maintain aspect ratio
plt.legend(loc='best', fontsize=10)
plt.show()