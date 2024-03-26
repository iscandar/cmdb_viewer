
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
        "docker-swarm": "icon-docker",
        "kube-master": "icon-kubernetes",
        "kube-node": "icon-kubernetes",
        "gateway": "icon-router",
        "web": "icon-web",
        "oracle-db": "icon-storage",
        "ml": "icon-auto-fix",
        "dev": "icon-developer-mode",
        "test": "icon-test-tube",
        "monitor": "icon-visibility",
        "independent": "icon-laptop"
    }
    return icons.get(role, "icon-help")

def create_enriched_diagram(cmdb_filepath, kmdb_filepath):
    cmdb_data = read_csv_data(cmdb_filepath)
    kmdb_data = read_csv_data(kmdb_filepath)
    diagram = yed_diagram()

    # Creazione dei gruppi basati su Ambiente e Ruolo/Funzione con colori diversi
    environment_colors = {"Prod": "#FFCCCC", "Dev": "#CCFFCC", "Test": "#CCCCFF"}
    for item in cmdb_data:
        node_description = "\n".join([f"{k}: {v}" for k, v in item.items() if k != "CI ID"])
        group_color = environment_colors.get(item["Ambiente"], "#FFFFFF")
        diagram.add_node(item["CI ID"], label=item["Hostname"], shape="rectangle", icon=assign_icon(item["Ruolo/Funzione"]), description=node_description, group=item["Ambiente"], group_color=group_color)

    # Aggiunta dei collegamenti con colori diversi e descrizioni
    for item in kmdb_data:
        dependencies = item["Dipendenze"].split(';')
        for dep in dependencies:
            if dep and dep != "N/A":
                diagram.add_link(item["ID CI"], dep, label=item.get("Flusso di Traffico In", ""),attributes={
    "LineStyle": {"color": "#0000FF", "width": "1.0"},
    "EdgeLabel": {"textColor": "#00FF00"},
})

    # Aggiunta di nodi per clienti e operatori
    diagram.add_node("Cliente", label="Cliente", shape="ellipse", icon="icon-user", description="Nodo che rappresenta un cliente")
    diagram.add_node("Operatore", label="Operatore", shape="ellipse", icon="icon-user-tie", description="Nodo che rappresenta un operatore")

    # Collegamenti dei clienti e operatori ai servizi
    for item in cmdb_data:
        if item["Ruolo/Funzione"] == "Web Server":
            diagram.add_link("Cliente", item["CI ID"],  label="Accesso Web",attributes={
    "LineStyle": {"color": "#FF0000", "width": "2.0"},
    "EdgeLabel": {"textColor": "#00FF00"},
})

        if item["Ruolo/Funzione"] == "Monitoring Server":
            diagram.add_link("Operatore", item["CI ID"], label="Monitoraggio",attributes={
    "LineStyle": {"color": "#00FF00", "width": "2.0"},
    "EdgeLabel": {"textColor": "#00FF00"},
})

    diagram.dump_file(filename="cmdb_kmdb_diagram_enriched.graphml", folder="./")

#cmdb_filepath = "./updated_cmdb_vms.csv"
#kmdb_filepath = "./kmdb_examples.csv"
#create_enriched_diagram(cmdb_filepath, kmdb_filepath)

#print("Diagramma arricchito creato con successo e salvato come 'cmdb_kmdb_diagram_enriched.graphml'.")
def read_csv_data(filepath):
    data = []
    with open(filepath, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def create_enriched_diagram(cmdb_filepath, kmdb_filepath):
    cmdb_data = read_csv_data(cmdb_filepath)
    kmdb_data = read_csv_data(kmdb_filepath)
    diagram = yed_diagram()

    # Configurazione per icone e colori
    icon_mapping = {
        "web": "web_icon.svg",  # Esempio di mappatura icona per 'web'
        "database": "database_icon.svg",
        # Aggiungi mappature per altri ruoli qui
    }
    color_mapping = {
        "Prod": "#FFCCCC",
        "Dev": "#CCFFCC",
        "Test": "#CCCCFF",
        # Altri colori per ambienti o ruoli
    }

    # Creazione nodi con icone SVG (o alternativa) e configurazione colori
    for item in cmdb_data:
        icon_path =""# icon_mapping.get(item["Ruolo/Funzione"], "default_icon.svg")
        group_color = color_mapping.get(item["Ambiente"], "#FFFFFF")
        # Se add_svg_node è disponibile, altrimenti usa un metodo alternativo
        diagram.add_node(item["Hostname"], label=item["Hostname"], shape="roundrectangle", description="".join(f"{k}: {v}" for k, v in item.items()), group=item["Ambiente"], group_color=group_color)# icon=icon_path,

    # Collegamenti con attributi personalizzati
    for item in kmdb_data:
        dependencies = item["Dipendenze"].split(';')
        for dep in dependencies:
            if dep and dep != "N/A":
                diagram.add_link(item["Hostname"], dep, label=item.get("Flusso di Traffico In", ""), attributes={"LineStyle": {"color": "#0000FF", "width": "2.0"}, "EdgeLabel": {"textColor": "#00FF00"}})


    diagram.dump_file(filename="cmdb_kmdb_diagram_enriched.graphml", folder="./")

cmdb_filepath = "./detailed_cmdb_updated.csv"
kmdb_filepath = "./detailed_kmdb_detailed_corrected.csv"
create_enriched_diagram(cmdb_filepath, kmdb_filepath)