# Prima di generare i nuovi file CMDB e KMDB, definiamo alcune impostazioni base e dati di esempio.

import csv
import random

# Definizione dei dati base per la generazione del CMDB
base_ip = ["10.0.0.", "10.0.1.", "192.168.1.", "172.16.0."]
os_choices = ["Ubuntu 20.04", "CentOS 8", "Debian 10", "Windows Server 2019"]
monitoring_tools = ["Prometheus", "Nagios", "CheckMK"]
roles = ["web", "kube-master", "kube-node", "docker-swarm", "oracle-db", "ml", "dev", "test", "monitor", "gateway", "independent"]
environments = ["Prod", "Dev", "Test"]
hostname_prefix = "vm"

# Funzioni di supporto per la generazione dei dati
def generate_ip(base_ip_list):
    return random.choice(base_ip_list) + str(random.randint(1, 254))

def generate_hostname(role, index):
    return f"{hostname_prefix}-{role}-{index}"

def generate_monitoring_machine():
    return random.choice(monitoring_tools)

def generate_url(role, index):
    if role in ["web", "kube-master", "kube-node"]:
        return f"http://www.{role}{index}.com:{random.choice([80, 8080, 443])}"
    return "N/A"

# Generazione del file CMDB
cmdb_data = []
for index, role in enumerate(roles * 10, start=1):  # Moltiplicazione per generare un numero sufficiente di VM
    vm_data = {
        "Hostname": generate_hostname(role, index),
        "IP": generate_ip(base_ip),
        "URL": generate_url(role, index),
        "OS": random.choice(os_choices),
        "Monitoraggio": generate_monitoring_machine(),
        "Ambiente": random.choice(environments),
        "Ruolo": role
    }
    cmdb_data.append(vm_data)

# Salvataggio del CMDB in CSV
cmdb_file_path = "./new_cmdb.csv"
with open(cmdb_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=cmdb_data[0].keys())
    writer.writeheader()
    writer.writerows(cmdb_data)

# Generazione del file KMDB basato sul CMDB appena creato
kmdb_data = []
for vm in cmdb_data:
    dependencies = random.sample([vm["Hostname"] for vm in cmdb_data if vm["Hostname"] != vm["Hostname"]], k=random.randint(1, 3))
    kmdb_data.append({
        "Hostname": vm["Hostname"],
        "Dipendenze": ";".join(dependencies),
        "Monitoraggio": vm["Monitoraggio"],
        "Ambiente": vm["Ambiente"],
        "Ruolo": vm["Ruolo"],
        "URL": vm["URL"]
    })

# Salvataggio del KMDB in CSV
kmdb_file_path = "./new_kmdb.csv"
with open(kmdb_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=kmdb_data[0].keys())
    writer.writeheader()
    writer.writerows(kmdb_data)


# Generazione dei nuovi file CMDB e KMDB con le specifiche dettagliate, escludendo le informazioni del CMDB dal KMDB.

# Generazione del CMDB aggiornato con dettagli come CPU, RAM, Hard Disk e almeno 20 colonne.
cmdb_data_updated = []
for index in range(1, 201):  # Generazione di 200 entità tra VMs, server, router, firewall, e gateway.
    entity_type = random.choice(["VM", "Server", "Router", "Firewall", "Gateway"])
    cmdb_entry = {
        "Hostname": f"{entity_type}-{index}",
        "IP": generate_ip(base_ip),
        "URL": generate_url(entity_type, index),
        "CPU": f"{random.choice([2, 4, 8, 16])} vCPUs",
        "RAM": f"{random.choice([8, 16, 32, 64])} GB",
        "Hard Disk": f"{random.choice([256, 512, 1024])} GB SSD",
        "OS": random.choice(os_choices),
        "Monitoraggio": random.choice(["Prometheus", "Nagios", "CheckMK"]),
        "Ambiente": random.choice(environments),
        "Ruolo": random.choice(roles),
        "ID CI": str(uuid.uuid4()),
        # Aggiunta di ulteriori dettagli per raggiungere almeno 20 colonne
        "Stato": random.choice(["Attivo", "Inattivo"]),
        "Porta": random.choice([22, 80, 443]),
        "Protocollo": random.choice(["HTTP", "HTTPS", "SSH"]),
        "Funzione": random.choice(["Produzione", "Test", "Sviluppo"]),
        "Localizzazione": random.choice(["Data Center 1", "Data Center 2"]),
        "Priorità": random.choice(["Alta", "Media", "Bassa"]),
        "Versione OS": random.choice(["Latest", "Stable", "Old"]),
        "Backup": random.choice(["Sì", "No"]),
        "Firewall": random.choice(["Sì", "No"]),
        "Note": "Generato automaticamente"
    }
    cmdb_data_updated.append(cmdb_entry)

# Salvataggio del CMDB in CSV
cmdb_file_path_updated = "/mnt/data/detailed_cmdb_updated.csv"
with open(cmdb_file_path_updated, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=cmdb_data_updated[0].keys())
    writer.writeheader()
    writer.writerows(cmdb_data_updated)



cmdb_file_path_updated

# Correzione dell'errore e rigenerazione del file KMDB con le specifiche dettagliate.

# Generazione di dati KMDB più accurata
kmdb_data_detailed_corrected = []
for vm in cmdb_data_updated:
    dependencies = random.sample([other_vm["Hostname"] for other_vm in cmdb_data_updated if other_vm["Hostname"] != vm["Hostname"]], k=random.randint(1, 3))
    kmdb_entry = {
        "Hostname": vm["Hostname"],
        "Dipendenze": ";".join(dependencies),
        "Componenti Dipendenti": ";".join(random.sample([other_vm["Hostname"] for other_vm in cmdb_data_updated if other_vm["Hostname"] != vm["Hostname"]], k=random.randint(1, 2))),
        "Monitorato da": random.choice(["Prometheus", "Nagios", "CheckMK"]),
        "Applicativi Installati": random.choice(["Docker", "Kubernetes", "Apache", "Nginx"]),
        "Servizi Forniti": vm["Ruolo"],
        "Flusso di Traffico In": random.choice(["80", "443"]),
        "Flusso di Traffico Out": random.choice(["80", "443"]),
        "Relazioni con Docker Swarm": "Sì" if vm["Ruolo"] == "docker-swarm" else "No",
        "Relazioni con Kubernetes": "Sì" if "kube" in vm["Ruolo"] else "No",
        "Politiche di Backup": random.choice(["Giornaliero", "Settimanale", "Nessuno"]),
        "Politiche di Sicurezza": "Standard",
        "Contatti di Supporto": "supporto@" + vm["Ruolo"] + ".com",
        "SLA": random.choice(["99%", "99.9%", "99.99%"]),
        "Note": "KMDB generato per simulazione"
    }
    kmdb_data_detailed_corrected.append(kmdb_entry)

# Salvataggio del KMDB corretto in CSV
kmdb_file_path_detailed_corrected = "/mnt/data/detailed_kmdb_detailed_corrected.csv"
with open(kmdb_file_path_detailed_corrected, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=kmdb_data_detailed_corrected[0].keys())
    writer.writeheader()
    writer.writerows(kmdb_data_detailed_corrected)

kmdb_file_path_detailed_corrected
