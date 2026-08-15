# Datalake Industriel — IoT Capteurs de Production

Déploiement d'un data lake moderne pour centraliser, documenter et sécuriser les flux de données issus de 5 lignes de production instrumentées de capteurs (température, pression, temps de fonctionnement), en vue d'un projet de maintenance prédictive.

---

## Stack technique

| Outil | Rôle |
|---|---|
| **MinIO** | Stockage objet S3-compatible |
| **OpenMetadata** | Catalogue de données et gouvernance |
| **Python / boto3** | Scripts d'ingestion et upload |
| **Docker Compose** | Orchestration des services |
| **Pandas** | Exploration et transformation des données |

---

## Architecture en couches

```
raw/        ← CSV bruts, partitionnés year=/month=/line=/
staging/    ← Données nettoyées, colonnes harmonisées, timestamp converti
curated/    ← Dataset unifié, prêt pour l'analyse et le ML
archive/    ← Données > 180 jours (règle ILM automatique)
```

---

## Structure du repo

```
Datalake-industriel/
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── docs/
│   ├── architecture.png       # Schéma d'architecture en couches
│   └── governance.md          # Politique de gouvernance et matrice des droits
├── infrastructure/
│   ├── docker-compose.yml     # MinIO
│   └── .env.example
├── openmetadata/
│   └── docker-compose.yml     # OpenMetadata + Elasticsearch + MySQL
├── ingestion/
│   └── upload_raw.py          # Upload boto3 avec partitionnement dynamique et MD5
└── notebooks/
    └── data_exploration.ipynb # Exploration des 5 CSV
```

---

## Prérequis

- Docker Desktop installé et lancé
- Python 3.9+
- Git

---

## Installation et lancement

### 1. Cloner le repo

```bash
git clone https://github.com/IZAK-M/Datalake-industriel.git
cd Datalake-industriel
git checkout dev
```

### 2. Configurer les variables d'environnement

```bash
cp infrastructure/.env.example .env
# Édite le fichier .env avec tes credentials
```

```env
MINIO_ROOT_USER=ton_user
MINIO_ROOT_PASSWORD=ton_password
```

### 3. Lancer MinIO

```bash
cd infrastructure
docker compose --env-file ../.env up -d
```

Accès console MinIO : **http://localhost:9001**

### 4. Lancer OpenMetadata

```bash
cd openmetadata
docker compose up -d
```

Accès OpenMetadata : **http://localhost:8585**
Credentials : `admin@open-metadata.org` / `admin`

> ⚠️ Le démarrage prend 3-5 minutes. Attendre que tous les services soient `healthy`.

### 5. Installer les dépendances Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 6. Télécharger les données

Télécharger les 5 CSV depuis [Zenodo](https://zenodo.org/records/15277168) et les placer dans `data/raw/`.

### 7. Uploader les fichiers vers MinIO

```bash
python3 ingestion/upload_raw.py
```

Ce script :
- Crée automatiquement les 4 buckets (`raw`, `staging`, `curated`, `archive`)
- Upload les 5 CSV avec partitionnement dynamique `year=/month=/line=/`
- Vérifie l'intégrité de chaque fichier via hash MD5

---

## Données

Source : [Synthetic Data from Industrial Sensor Monitoring — Zenodo](https://zenodo.org/records/15277168)

| Ligne | Fichier | Enregistrements | Particularité |
|---|---|---|---|
| LineA | LineA_Stable_10K.csv | 10 000 | Comportement stable, contient `elapsed_time` |
| LineB | LineB_Flux.csv | 5 000 | Flux moyen, contient `elapsed_time` |
| LineC | LineC_Turbulent.csv | 5 000 | Turbulent, sans `elapsed_time` |
| LineD | LineD_SpikeControl.csv | 5 000 | Pics de pression, sans `elapsed_time` |
| LineE | LineE_SmoothRun.csv | 5 000 | Variable, sans `elapsed_time` |

**Colonne `label`** : `0` = fonctionnement nominal, `1` = anomalie détectée

---

## Gouvernance

Voir [`docs/governance.md`](docs/governance.md) pour la politique complète d'accès et les règles ILM.

---

## Auteur

Izak Mohamed — Apprenti Data Engineer 
