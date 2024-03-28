
import csv
from N2G import yed_diagram

def read_csv_data(filepath):
    data = []
    with open(filepath, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def assign_icon(role):
    icons = {
        "Web Server": "rectangle",
        "Database Server": "roundrectangle",
        "Application Server": "diamond",
        "Firewall": "parallelogram",
        "Monitoring System": "ellipse",
        "Gateway": "triangle",
        "Docker Swarm Node": "hexagon",
        "Kubernetes Node": "octagon",
        "Podman Container": "trapezoid",
        "Independent Server": "ellipse",
        "Client": "star",  
        "Operator": "cloud"  
    }
    return icons.get(role, "rectangle")

def create_enriched_diagram(cmdb_filepath, kmdb_filepath):
    cmdb_data = read_csv_data(cmdb_filepath)
    kmdb_data = read_csv_data(kmdb_filepath)
    diagram = yed_diagram()

    environment_colors = {"Production": "#FFCCCC", "Development": "#CCFFCC", "Testing": "#CCCCFF"}
    cluster_colors = {"Docker Swarm": "#FFFFCC", "Kubernetes": "#CCFFFF", "Podman": "#FFCCFF", "Independent": "#D5D5D5"}
    
    for item in cmdb_data:
        node_description = "\n".join([f"{k}: {v}" for k, v in item.items() if k != "Hostname"])
        group_color = environment_colors.get(item["Ambiente"], "#FFFFFF")
        cluster_group_color = cluster_colors.get(item.get("Cluster", "Independent"), "#D5D5D5")
        
        diagram.add_node(item["Hostname"], label=item["Hostname"], shape="rectangle", 
                         icon=assign_icon(item["Ruolo/Funzione"]), description=node_description, 
                         group=item["Ambiente"] + ", " + item["Ruolo/Funzione"], 
                         group_color=group_color, secondary_group_color=cluster_group_color)

    relation_colors = {"Dipendente": "#0000FF", "Dipendono": "#FF0000"}
    for item in kmdb_data:
        dependents = item["Dipendono"].split(", ")
        for dep in dependents:
            if dep and dep != "N/A":
                diagram.add_link(item["Hostname"], dep, label="Dependence", 
                                 attributes={"LineStyle": {"color": relation_colors["Dipendente"], "width": "2.0"}})

    diagram.add_node("Client", label="Client", shape="star", description="Node representing a client", icon="star")
    diagram.add_node("Operator", label="Operator", shape="cloud", description="Node representing an operator", icon="cloud")
    for item in cmdb_data:
        if "Client" in item["Ruolo/Funzione"]:
            diagram.add_link("Client", item["Hostname"], label="Client Access", 
                             attributes={"LineStyle": {"color": "#00FF00", "width": "2.0"}})
        if "Operator" in item["Ruolo/Funzione"]:
            diagram.add_link("Operator", item["Hostname"], label="Operator Monitoring", 
                             attributes={"LineStyle": {"color": "#FF00FF", "width": "2.0"}})

    diagram.dump_file(filename="cmdb_kmdb_diagram_refined.graphml", folder="./")


cmdb_filepath = "./cmdb_updated.csv"
kmdb_filepath = "./kmdb_updated.csv"


create_enriched_diagram(cmdb_filepath, kmdb_filepath)

print("Diagramma arricchito creato con successo e salvato come 'cmdb_kmdb_diagram_refined.graphml'.")
