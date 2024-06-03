#version which removes the input file at the end
import os

class Graph:
    def __init__(self, size):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size
        self.resid_mapping = {}

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight  # For undirected graph

    def add_vertex_data(self, vertex, data, resid):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data
            self.resid_mapping[data] = resid

    def dijkstra(self, start_vertex_data):
        start_vertex = self.vertex_data.index(start_vertex_data)
        distances = [float('-inf')] * self.size
        distances[start_vertex] = 0
        visited = [False] * self.size

        for _ in range(self.size):
            max_distance = float('-inf')
            u = None
            for i in range(self.size):
                if not visited[i] and distances[i] > max_distance:
                    max_distance = distances[i]
                    u = i

            if u is None:
                break

            visited[u] = True

            for v in range(self.size):
                if self.adj_matrix[u][v] != 0 and not visited[v]:
                    alt = max(distances[u], self.adj_matrix[u][v])
                    if alt > distances[v]:
                        distances[v] = alt

        return distances

    def find_max_coupling_path_resid(self, start_vertex_data):
        distances = self.dijkstra(start_vertex_data)
        max_coupling = max(distances)
        max_coupling_vertex = self.vertex_data[distances.index(max_coupling)]
        return self.resid_mapping[max_coupling_vertex]

def read_average_coupling_values(file_path):
    vertex_mapping = {}
    vertex_index = 1  # Start from 1 since 0 is reserved for the source resid
    source_resid = None
    data = []

    with open(file_path, 'r') as file:
        next(file)  # Skip header
        for line in file:
            parts = line.strip().split()
            if len(parts) != 3:
                continue  # Skip any line that doesn't have exactly 3 elements

            src_resid = int(parts[0])
            tgt_resid = int(parts[1])
            avg_cpl = float(parts[2])  # Convert from eV to meV
            
            if source_resid is None:
                source_resid = src_resid
                vertex_mapping[src_resid] = 0  # Map source resid to 0
            
            if tgt_resid not in vertex_mapping:
                vertex_mapping[tgt_resid] = vertex_index
                vertex_index += 1

            data.append((src_resid, tgt_resid, avg_cpl))
    
    size = len(vertex_mapping)
    graph = Graph(size)
    graph.add_vertex_data(0, 'A', source_resid)  # Add source resid as vertex 0

    # Add the remaining vertex data
    for resid, index in vertex_mapping.items():
        if index != 0:
            label = chr(ord('A') + index)
            graph.add_vertex_data(index, label, resid)

    # Add edges to the graph
    for src_resid, tgt_resid, avg_cpl in data:
        u = vertex_mapping[src_resid]
        v = vertex_mapping[tgt_resid]
        graph.add_edge(v, u, avg_cpl)

    return graph

def main():
    file_path = 'average_coupling_values.txt'
    output_file = 'output_path.txt'
    graph = read_average_coupling_values(file_path)

    # Perform Dijkstra's algorithm
    print("\nDijkstra's Algorithm starting from vertex A:")
    distances = graph.dijkstra('A')
    for i, d in enumerate(distances):
        print(f"Distance from A to {graph.vertex_data[i]}: {d}")
        
    # Find the resid of the path with the largest coupling
    max_coupling_resid = graph.find_max_coupling_path_resid('A')
    print("Resid of the Target with Largest Coupling:", max_coupling_resid)
    
    # Save the resid to the output file
    with open(output_file, 'w') as f:
        f.write(f"{max_coupling_resid}\n")
    
    # Remove the input file
    os.remove(file_path)

if __name__ == "__main__":
    main()
