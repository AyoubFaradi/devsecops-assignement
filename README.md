# Sécurisation d’une Application Python via une Pipeline DevSecOps CI/CD

![DevSecOps](https://img.shields.io/badge/DevSecOps-CI%2FCD-blue)
![Security](https://img.shields.io/badge/Security-Automated-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-informational)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-black)

---

## Présentation du projet

Ce projet consiste à mettre en œuvre une **démarche DevSecOps complète** afin de sécuriser une application web **Python Flask** initialement vulnérable.  
La sécurité est intégrée automatiquement dans une **pipeline CI/CD GitHub Actions**, permettant de détecter et bloquer toute vulnérabilité critique avant la mise en production.

L’objectif principal est de démontrer comment l’automatisation de la sécurité améliore la qualité, la fiabilité et la robustesse des applications.

---

## 🏗️ Architecture du projet

```bash
devsecops-assignment/
├── api/
│   └── app.py
├── requirements.txt
├── Dockerfile
├── .github/
│   └── workflows/
│       └── devsecops.yml
└── README.md
```
<img width="314" height="209" alt="image" src="https://github.com/user-attachments/assets/b71cad26-d986-430d-a6de-9c0a51e4b7e0" />


Pipeline DevSecOps CI/CD
La pipeline CI/CD est déclenchée automatiquement à chaque push sur la branche main et intègre les étapes suivantes :

CodeQL — Analyse SAST (Static Application Security Testing)

Bandit — Analyse de sécurité du code Python

Safety — Scan des dépendances (Supply Chain Security)

Docker Build — Construction de l’image Docker

Trivy — Scan de sécurité de l’image Docker

--> Toute vulnérabilité CRITICAL ou HIGH provoque l’échec automatique de la pipeline.

<img width="1247" height="892" alt="image" src="https://github.com/user-attachments/assets/e8c79b26-0895-4bac-b8a4-1bd4fdab8293" />

Vulnérabilités détectées — AVANT correction
Les analyses de sécurité ont permis d’identifier plusieurs vulnérabilités critiques dans le code initial.

Endpoint / Élément	Type de vulnérabilité	Outil	OWASP Top 10
/auth	SQL Injection	CodeQL	A03
/exec	Command Injection	Bandit	A03
/deserialize	Insecure Deserialization	Bandit	A08
/encrypt	Weak Cryptography (MD5)	Bandit	A02
/file	Path Traversal	CodeQL	A01
/debug	Sensitive Data Exposure	CodeQL	A02
API_KEY	Hardcoded Secret	Bandit	A02
/log	Log Injection	Bandit	A09

Pipeline en échec (avant correction)

<img width="1908" height="875" alt="image" src="https://github.com/user-attachments/assets/2b7e347d-369c-4deb-b030-1c165854bacb" />


📁 Analyse des fichiers — AVANT sécurisation
.github/workflows/devsecops.yml

<img width="1704" height="955" alt="image" src="https://github.com/user-attachments/assets/3f7ba773-ede6-4ca5-b92e-19917281334e" />

Dockerfile

<img width="1226" height="814" alt="image" src="https://github.com/user-attachments/assets/920e239d-ab5e-4b7c-9509-284962a505d5" />

requirements.txt

<img width="821" height="389" alt="image" src="https://github.com/user-attachments/assets/1f6cf1ec-ec0c-4408-9928-a0599367132b" />

app.py

<img width="1554" height="957" alt="image" src="https://github.com/user-attachments/assets/d610359c-9728-4a02-aba6-b54f4678baae" />

🔐 Corrections de sécurité appliquées
Les vulnérabilités détectées ont été corrigées selon les bonnes pratiques DevSecOps :

Vulnérabilité	Correction appliquée
SQL Injection	Requêtes SQL paramétrées
Command Injection	Suppression de l’endpoint
Désérialisation dangereuse	Suppression de l’endpoint
Chiffrement faible (MD5)	Remplacement par bcrypt
Path Traversal	Validation stricte des chemins
Secrets exposés	Variables d’environnement
Debug & logs	Mode debug désactivé
Docker	Image slim + utilisateur non-root

Dockerfile sécurisé
Image légère (python:3.11-slim)

Exécution avec un utilisateur non-root

Surface d’attaque réduite

Dockerfile sécurisé

<img width="1360" height="616" alt="image" src="https://github.com/user-attachments/assets/4e6d4a84-9e0d-43fd-b7aa-8f875498d8e4" />

requirements.txt sécurisé
Dépendances mises à jour

Suppression des versions vulnérables

<img width="1279" height="465" alt="image" src="https://github.com/user-attachments/assets/379ae288-56a3-4e1e-8979-3966b8b5d14c" />

app.py sécurisé
Entrées utilisateur validées

Secrets externalisés

Aucun code dangereux exécuté

Conforme aux règles Bandit

<img width="1167" height="969" alt="image" src="https://github.com/user-attachments/assets/5e252a40-61c3-4c47-8243-5061434b79fa" />

Analyse des fichiers — APRES sécurisation
.github/workflows/devsecops.yml

<img width="1562" height="939" alt="image" src="https://github.com/user-attachments/assets/3b12a022-f551-4225-b0e2-d2de4dfa014d" />


Pipeline après correction
Après application de toutes les corrections :

Aucune vulnérabilité CRITICAL / HIGH

Pipeline CI/CD validée avec succès

<img width="1892" height="868" alt="image" src="https://github.com/user-attachments/assets/a27b1407-88f1-494c-8bf9-5f11c23a2309" />


Résultat final
✔ Application sécurisée
✔ Pipeline CI/CD automatisée
✔ Blocage des failles critiques
✔ Conformité avec l’OWASP Top 10
✔ Démarche DevSecOps respectée

Conclusion DevSecOps
Ce projet démontre clairement l’importance de l’intégration de la sécurité dès les premières étapes du développement.
Grâce à l’approche DevSecOps, les vulnérabilités sont détectées automatiquement, corrigées efficacement et bloquées avant toute mise en production.

La pipeline CI/CD devient ainsi un élément clé garantissant la sécurité, la qualité et la fiabilité de l’application.

Auteur
Nom : Ayoub Faradi
