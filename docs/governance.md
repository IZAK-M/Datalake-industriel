# Politique de Gouvernance — Datalake Industriel

## Contexte
Datalake déployé pour un équipementier automobile exploitant 5 lignes de production instrumentées de capteurs (température, pression, temps de fonctionnement). Infrastructure basée sur MinIO (stockage objet S3-compatible) et OpenMetadata (catalogue de données).

---

## Matrice des droits d'accès

| Rôle | raw/ | staging/ | curated/ | archive/ |
|---|---|---|---|---|
| `data-analyst` | ❌ | ❌ | ✅ Lecture seule | ❌ |
| `data-engineer` | ✅ Lecture/Écriture | ✅ Lecture/Écriture | ✅ Lecture/Écriture | ❌ |
| `admin` | ✅ Tous droits | ✅ Tous droits | ✅ Tous droits | ✅ Tous droits |

---

## Description des rôles

### `data-analyst`
- **Périmètre** : Accès en lecture seule sur le bucket `curated/`
- **Justification** : Les données curated sont nettoyées, harmonisées et validées. Le data analyst n'a pas besoin d'accéder aux données brutes ou intermédiaires.
- **Responsabilités** : Exploitation des données pour analyses et reporting. Aucune modification des données autorisée.

### `data-engineer`
- **Périmètre** : Lecture/écriture sur `raw/` et `staging/`
- **Justification** : Responsable des pipelines d'ingestion et de transformation. Doit pouvoir déposer les fichiers bruts et les transformer vers staging.
- **Responsabilités** : Maintien des pipelines, qualité des données, documentation des transformations.

### `admin`
- **Périmètre** : Tous droits sur tous les buckets
- **Justification** : Gestion de l'infrastructure, création des comptes de service, configuration des policies et règles ILM.
- **Responsabilités** : Sécurité globale, gestion des accès, audit des logs, rotation des credentials.

---

## Règles de cycle de vie (ILM)

| Règle | Bucket | Délai | Action |
|---|---|---|---|
| Archivage automatique | `curated/` | 180 jours | Déplacement vers `archive/` |
| Suppression automatique | `archive/` | 2 ans | Suppression définitive |
| Rétention permanente | `raw/` | Indéfini | Aucune suppression — source de vérité |

---

## Sécurité

- **Chiffrement** : SSE-S3 activé sur les buckets `raw/`, `staging/`, `curated/`
- **Audit** : Logs d'accès MinIO activés sur tous les buckets
- **Credentials** : Stockés dans un fichier `.env` non versionné, jamais en clair dans le code
- **Rotation** : Les credentials de service doivent être rotés tous les 90 jours

---

## Responsabilités par rôle

| Responsabilité | data-analyst | data-engineer | admin |
|---|---|---|---|
| Ingestion des données brutes | ❌ | ✅ | ✅ |
| Transformation et nettoyage | ❌ | ✅ | ✅ |
| Exploitation analytique | ✅ | ✅ | ✅ |
| Gestion des accès | ❌ | ❌ | ✅ |
| Configuration ILM | ❌ | ❌ | ✅ |
| Audit des logs | ❌ | ❌ | ✅ |
