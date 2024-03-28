import csv
import random
from random import choice, randint, sample
import numpy as np

# Tipologie di dispositivi
tipi_dispositivi = ["Container", "VM", "Baremetal", "Firewall", "Gateway", "Monitor"]

# Ruoli/Funzioni
ruoli = [
    "Kubernetes Node", "Docker Swarm Node", "Database Oracle", "Database MongoDB", 
    "Queue Management", "Load Balancer", "Cache", "Firewall", "Gateway", "Monitoring System"
]

# Sistemi operativi
sistemi_operativi = ["Ubuntu 20.04", "CentOS 8", "Debian 10", "Windows Server 2019"]

# Ambiente
ambienti = ["Produzione", "Test", "Sviluppo"]

# Generazione degli hostname
hostname_base = ["kube-node", "docker-node", "oracle-db", "mongo-db", "queue-mgr", "lb", "cache", "firewall", "gateway", "monitor"]
hostnames = [f"{choice(hostname_base)}-{i}" for i in range(1, 201)]

# Creazione di URL
url_base = ["internal.company", "service.local", "public-service.com"]
urls = [f"http://{hostname}.{choice(url_base)}" for hostname in hostnames]

# Assegnazione degli IP
ip_base = ["192.168", "10.10", "172.16"]
ips = [f"{choice(ip_base)}.{randint(1, 254)}.{randint(1, 254)}" for _ in range(200)]

# CMDB
cmdb_data = []
for i in range(200):
    dispositivo = {
        "Tipo": choice(tipi_dispositivi),
        "Hostname": hostnames[i],
        "IP": ips[i],
        "URL": urls[i],
        "CPU": f"{randint(1, 16)} cores",
        "RAM": f"{randint(4, 128)} GB",
        "VRAM": f"{randint(1, 16)} GB" if randint(1, 100) <= 20 else "N/A",  # 20% dei dispositivi hanno VRAM
        "Hard Disk": f"{randint(128, 2048)} GB",
        "Interfacce di Rete": f"eth0: {ips[i]}",
        "OS": choice(sistemi_operativi),
        "Macchina di Monitoraggio": f"monitor-{randint(1, 10)}",
        "Macchina Gateway": f"gateway-{randint(1, 5)}",
        "Ambiente": choice(ambienti),
        "Ruolo/Funzione": choice(ruoli),
        "Stato": "Active" if randint(0, 1) else "Maintenance",
    }
    cmdb_data.append(dispositivo)

cmdb_df_new = pd.DataFrame(cmdb_data)

cmdb_df_new.head(), cmdb_df_new.shape

# KMDB
applicativi_possibili = ["Redis", "PostgreSQL", "Docker", "Apache", "Nginx", "Node.js", "RabbitMQ", "MySQL"]
def genera_applicativi():
    return ', '.join(sample(applicativi_possibili, randint(3, 7)))  # Tra 3 e 7 applicativi


servizi_possibili = ["HTTPS", "SSH", "SMTP", "SFTP", "FTP", "SNMP"]
def genera_servizi():
    return ', '.join(sample(servizi_possibili, randint(2, 4)))  # Tra 2 e 4 servizi

def genera_porte():
    return ', '.join([str(randint(1024, 65535)) for _ in range(randint(2, 4))])  # Tra 2 e 4 porte

protocolli_possibili = ["TCP", "UDP", "HTTPS", "SSH"]
def genera_protocolli():
    return ', '.join(sample(protocolli_possibili, randint(2, 4)))  # Tra 2 e 4 protocolli

politiche_backup = [
    "Offsite Backup", "Monthly Backup", "Real-time Replication", "Daily Backup", "Encrypted Backup", 
    "Incremental Backup", "Differential Backup", "On-site Backup", "Cloud Backup", "Snapshot Backup"
]

politiche_sicurezza = [
    "Multi-factor Authentication", "Regular Security Audits", "Restricted Access Policies", "Advanced Security Policy", 
    "Data Encryption", "Network Segmentation", "Anti-virus and Anti-malware", "Firewall Policies", 
    "Intrusion Detection Systems", "Regular Software Updates"
]

def genera_dipendenze():
    return ', '.join(sample(hostnames, randint(1, 5)))  # Tra 1 e 5 hostnames come dipendenze

kmdb_data = []
for hostname in hostnames:
    dispositivo_kmdb = {
        "Hostname": hostname,
        "Dipendente": genera_dipendenze(),
        "Dipendono": genera_dipendenze(),
        "Sistema di Monitoraggio": f"{choice(hostnames)} - {choice(['Nagios', 'Prometheus'])}",
        "Applicativi Installati": genera_applicativi(),
        "Servizi Forniti": genera_servizi(),
        "Porte di Comunicazione": genera_porte(),
        "Protocolli per la Comunicazione": genera_protocolli(),
        "Politiche di Backup": choice(politiche_backup),
        "Politiche di Sicurezza": choice(politiche_sicurezza),
        "Note": "Auto-generated entry for KMDB"
    }
    kmdb_data.append(dispositivo_kmdb)

kmdb_df_new = pd.DataFrame(kmdb_data)

kmdb_df_new.head(), kmdb_df_new.shape

# Salvataggio dei file CMDB e KMDB in formato CSV
cmdb_file_path = './cmdb_updated.csv'
kmdb_file_path = './kmdb_updated.csv'

cmdb_df_new.to_csv(cmdb_file_path, index=False)
kmdb_df_new.to_csv(kmdb_file_path, index=False)
