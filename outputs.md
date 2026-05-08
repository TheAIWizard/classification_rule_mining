Voici la structuration de vos données sous forme de fiches de décision métier.

# RÈGLES CANDIDATES – VALIDATION MÉTIER

## 📋 TABLEAU DE SYNTHÈSE (OBLIGATOIRE EN PREMIER)

| Cluster | Activité | Code NAF | Impact base | Impact réel | Risque bruit | Décision | ✔ Retenir ? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CLUSTER_HOLDING_001 | Gestion de holdings | 70.10Y | élevé | élevé | élevé | SECURE | ☐ Oui ☐ Non |
| CLUSTER_IMMOBILIER_002 | Gestion/location immobilière | 68.20G | élevé | moyen | élevé | SECURE | ☐ Oui ☐ Non |
| CLUSTER_AUDIOVISUEL_003 | Production audiovisuelle | 59.11H | moyen | élevé | faible | INVESTIGATE | ☐ Oui ☐ Non |
| CLUSTER_BIEN_ETRE_004 | Soins bien-être/holistiques | 86.96Y | faible | moyen | élevé | INVESTIGATE | ☐ Oui ☐ Non |
| CLUSTER_INFORMATIQUE_005 | Développement informatique | 62.01Z | élevé | élevé | élevé | SECURE | ☐ Oui ☐ Non |
| CLUSTER_COMMERCE_ALIMENTAIRE_006 | Commerce détail alimentaire | 47.11G | moyen | élevé | moyen | INVESTIGATE | ☐ Oui ☐ Non |
| CLUSTER_CONSEIL_007 | Conseil/Expertise technique | 74.99Y | faible | faible | faible | LOW_PRIORITY | ☐ Oui ☐ Non |
| CLUSTER_NETTOYAGE_008 | Nettoyage et entretien | 81.22Y | moyen | faible | moyen | SECURE | ☐ Oui ☐ Non |
| CLUSTER_LOGISTIQUE_009 | Transport et logistique | 49.41H | élevé | élevé | élevé | SECURE | ☐ Oui ☐ Non |
| CLUSTER_INTERMEDIATION_010 | Intermédiation commerciale | 82.40 | moyen | élevé | élevé | INVESTIGATE | ☐ Oui ☐ Non |

---

## 🟦 DÉTAIL PAR CLUSTER

### CLUSTER_HOLDING_001 — Gestion de holdings et participations

**Code NAF :** 70.10Y  

---

### 📊 Impact sur la base d’apprentissage
- Volume total : 34 851
- Volume à corriger : 24 679
- Volume déjà correct : 10 172

---

### 🎯 Impact métier réel
57 % de corrections nécessaires

---

### ⚠️ Risque de bruit (effets de bord)
- Niveau : Élevé
- Causes principales :
  - overlap métier
  - confusion avec d’autres codes NAF (6630Y)

- 🔎 Exemples de cas problématiques (effets de bord potentiels) :
  - activités de holding de prise de participations de direction des filiales
  - siège social avant achat de fonds de commerce

👉 Ces exemples ne sont pas des erreurs certaines, mais des cas limites pouvant être affectés par la règle.

---

### 🎯 Décision recommandée (métier)
Sécuriser la règle avant déploiement en raison d'un risque majeur de confusion avec les services financiers (6630Y).

---

### 🎯 Activité métier (simplifiée)
Gestion de holdings et de participations financières.

---

### 🧠 Règle métier (simplifiée)
Identifier les sociétés dont l'activité principale est la gestion de participations et la direction de filiales.

---

### 🔎 Exemples représentatifs
- holding
- prise de participation
- siège social

---

### 🧩 Mots-clés essentiels
holding, prise de participation, siège social

---

### ⚠️ Points de vigilance
- risque de confusion avec le code 6630Y
- volume de correction très important (critique)

---

### ☑️ Décision finale
- [ ] RETENIR  
- [x] À MODIFIER  
- [ ] À REJETER  

---

### CLUSTER_IMMOBILIER_002 — Gestion et location de biens immobiliers

**Code NAF :** 68.20G  

---

### 📊 Impact sur la base d’apprentissage
- Volume total : 20 774
- Volume à corriger : 4 332
- Volume déjà correct : 16 442

---

### 🎯 Impact métier réel
21 % de corrections nécessaires

---

### ⚠️ Risque de bruit (effets de bord)
- Niveau : Élevé
- Causes principales :
  - forte dispersion métier
  - confusion avec gestion immobilière (6820H)

- 🔎 Exemples de cas problématiques (effets de bord potentiels) :
  - gestion immobilière (6820H)
  - location saisonnière

👉 Ces exemples ne sont pas des erreurs certaines, mais des cas limites pouvant être affectés par la règle.

---

### 🎯 Décision recommandée (métier)
Sécuriser la distinction entre la propriété/location (6820G) et la prestation de services de gestion (6820H).

---

### 🎯 Activité métier (simplifiée)
Gestion et location de biens immobiliers.

---

### 🧠 Règle métier (simplifiée)
Identifier les activités de location (meublée ou non) et de détention d'actifs immobiliers.

---

### 🔎 Exemples représentatifs
- location meublée
- lmnp
- gestion immobilière

---

### 🧩 Mots-clés essentiels
location meublée, lmnp, gestion immobilière

---

### ⚠️ Points de vigilance
- le terme "gestion immobilière" doit être strictement encadré pour ne pas basculer vers le 6820H.

---

### ☑️ Décision finale
- [ ] RETENIR  
- [x] À MODIFIER  
- [ ] À REJETER  

---

### CLUSTER_AUDIOVISUEL_003 — Production et réalisation audiovisuelle

**Code NAF :** 59.11H  

---

### 📊 Impact sur la base d’apprentissage
- Volume total : 1 895
- Volume à corriger : 1 883
- Volume déjà correct : 12

---

### 🎯 Impact métier réel
99 % de corrections nécessaires

---

### ⚠️ Risque de bruit (effets de bord)
- Niveau : Faible
- Causes principales :
  - dispersion vers 5912Y

- 🔎 Exemples de cas problématiques (effets de bord potentiels) :
  - post-production de films (5912Y)

👉 Ces exemples ne sont pas des erreurs certaines, mais des cas limites pouvant être affectés par la règle.

---

### 🎯 Décision recommandée (métier)
Investiguer pour valider la séparation entre la réalisation (5911H) et la post-production (5912Y).

---

### 🎯 Activité métier (simplifiée)
Production et réalisation de contenus audiovisuels et digitaux.

---

### 🧠 Règle métier (simplifiée)
Cibler la création et la réalisation de contenus audiovisuels.

---

### 🔎 Exemples représentatifs
- réalisation audiovisuelle
- montage vidéo
- production de films

---

### 🧩 Mots-clés essentiels
réalisation audiovisuelle, montage vidéo, production de films

---

### ⚠️ Points de vigilance
- risque de confusion avec les activités de post-production.

---

### ☑️ Décision finale
- [x] RETENIR  
- [ ] À MODIFIER  
- [ ] À REJETER  

---

### CLUSTER_BIEN_ETRE_004 — Services de soins de bien-être

**Code NAF :** 86.96Y  

---

### 📊 Impact sur la base d’apprentissage
- Volume total : 728
- Volume à corriger : 508
- Volume déjà correct : 220

---

### 🎯 Impact métier réel
30 % de corrections nécessaires

---

### ⚠️ Risque de bruit (effets de bord)
- Niveau : Élevé
- Causes principales :
  - forte dispersion vers 9623Y

- 🔎 Exemples de cas problématiques (effets de bord potentiels) :
  - massage bien-être (9623Y)

👉 Ces exemples ne sont pas des erreurs certaines, mais des cas limites pouvant être affectés par la règle.

---

### 🎯 Décision recommandée (métier)
Investiguer pour mieux différencier les pratiques holistiques des services de massage/esthétique.

---

### 🎯 Activité métier (simplifiée)
Services de soins de bien-être et pratiques holistiques.

---

### 🧠 Règle métier (simplifiée)
Identifier les activités de soins holistiques et de thérapies alternatives.

---

### 🔎 Exemples représentatifs
- réflexologie
- naturopathie

---

### 🧩 Mots-clés essentiels
réflexologie, naturopathie

---

### ⚠️ Points de vigilance
- confusion fréquente avec le secteur du massage et de l'esthétique (9623Y).

---

### ☑️ Décision finale
- [ ] RETENIR  
- [x] À MODIFIER  
- [ ] À REJETER  

---

### CLUSTER_INFORMATIQUE_005 — Développement informatique

**Code NAF :** 62.01Z  

---

### 📊 Impact sur la base d’apprentissage
- Volume total : 9 758
- Volume à corriger : 9 758
- Volume déjà correct : 0

---

### 🎯 Impact métier réel
100 % de corrections nécessaires

---

### ⚠️ Risque de bruit (effets de bord)
- Niveau : Élevé
- Causes principales :
  - bruit sémantique massif (terme "code")

- 🔎 Exemples de cas problématiques (effets de bord potentiels) :
  - code APE (6820G)
  - code monétaire

👉 Ces exemples ne sont pas des erreurs certaines, mais des cas limites pouvant être affectés par la règle.

---

### 🎯 Décision recommandée (métier)
Sécuriser impérativement par un filtrage strict des termes non informatiques.

---

### 🎯 Activité métier (simplifiée)
Développement de solutions informatiques et programmation.

---

### 🧠 Règle métier (simplifiée)
Identifier les activités de programmation et de création de logiciels/sites.

---

### 🔎 Exemples représentatifs
- développement logiciel
- création de sites internet
- code

---

### 🧩 Mots-clés essentiels
développement logiciel, création de sites internet

---

### ⚠️ Points de vigilance
- Le mot "code" est trop générique et pollue le cluster (risque de capturer des termes administratifs ou monétaires).

---

### ☑️ Décision finale
- [ ] RETENIR  
- [x] À MODIFIER  
- [ ] À REJETER  

---

### CLUSTER_COMMERCE_ALIMENTAIRE_006 — Commerce de détail alimentaire

**Code NAF :** 47.11G  

---

### 📊 Impact sur la base d’apprentissage
- Volume total : 1 328
- Volume à corriger : 1 323
- Volume déjà correct : 5

---

### 🎯 Impact métier réel
99 % de corrections nécessaires

---

### ⚠️ Risque de bruit (effets de bord)
- Niveau : Moyen
- Causes principales :
  - dispersion vers 4722Y/4725Y

- 🔎 Exemples de cas problématiques (effets de bord potentiels) :
  - épicerie fine (4725Y)
  - alimentation générale (4722Y)

👉 Ces exemples ne sont pas des erreurs certaines, mais des cas limites pouvant être affectés par la règle.

---

### 🎯 Décision recommandée (métier)
Investiguer pour éviter que la règle ne capture des spécialités plus fines (épicerie fine, etc.).

---

### 🎯 Activité métier (simplifiée)
Commerce de détail alimentaire et épicerie.

---

### 🧠 Règle métier (simplifiée)
Identifier le commerce de détail d'alimentation de base ou générale.

---

### 🔎 Exemples représentatifs
- épicerie fine
- commerce alimentaire
- alimentation générale

---

### 🧩 Mots-clés essentiels
épicerie fine, commerce alimentaire, alimentation générale

---

### ⚠️ Points de vigilance
- forte probabilité de capturer des codes de spécialités (4722Y, 4725Y).

---

### ☑️ Décision finale
- [ ] RETENIR  
- [x] À MODIFIER  
- [ ] À REJETER  

---

### CLUSTER_CONSEIL_007 — Conseil et expertise technique

**Code NAF :** 74.99Y  

---

### 📊 Impact sur la base d’apprentissage
- Volume total : 37
- Volume à corriger : 36
- Volume déjà correct : 1

---

### 🎯 Impact métier réel
97 % de corrections nécessaires

---

### ⚠️ Risque de bruit (effets de bord)
- Niveau : Faible
- Causes principales :
  - dispersion vers 7020Y/7112Y

- 🔎 Exemples de cas problématiques (effets de bord potentiels) :
  - conseil en stratégie (7020Y)

👉 Ces exemples ne sont pas des erreurs certaines, mais des cas limites pouvant être affectés par la règle.

---

### 🎯 Décision recommandée (métier)
Priorité basse en raison du volume très faible.

---

### 🎯 Activité métier (simplifiée)
Conseil, ingénierie et expertise technique spécialisée.

---

### 🧠 Règle métier (simplifiée)
Identifier les activités d'expertise technique ou de conseil spécialisé.

---

### 🔎 Exemples représentatifs
- conseil en stratégie RSE
- décarbonation
- expertise agricole

---

### 🧩 Mots-clés essentiels
conseil en stratégie RSE, décarbonation, expertise agricole

---

### ⚠️ Points de vigilance
- faible volume ; risque de confusion avec le conseil de direction (7020Y).

---

### ☑️ Décision finale
- [ ] RETENIR  
- [ ] À MODIFIER  
- [x] À REJETER  

---

### CLUSTER_NETTOYAGE_008 — Nettoyage et entretien

**Code NAF :** 81.22Y  

---

### 📊 Impact sur la base d’apprentissage
- Volume total : 1 485
- Volume à corriger : 203
- Volume déjà correct : 1 282

---

### 🎯 Impact métier réel
14 % de corrections nécessaires

---

### ⚠️ Risque de bruit (effets de bord)
- Niveau : Moyen
- Causes principales :
  - confusion avec entretien véhicules (9531G)

- 🔎 Exemples de cas problématiques (effets de bord potentiels) :
  - entretien véhicules (9531G)

👉 Ces exemples ne sont pas des erreurs certaines, mais des cas limites pouvant être affectés par la règle.

---

### 🎯 Décision recommandée (métier)
Sécuriser la règle en isolant les activités de nettoyage industriel/bâtiment des services automobiles.

---

### 🎯 Activité métier (simplifiée)
Services de nettoyage et entretien de bâtiments ou véhicules.

---

### 🧠 Règle métier (simplifiée)
Cibler les prestations de nettoyage de locaux ou de surfaces.

---

### 🔎 Exemples représentatifs
- nettoyage après travaux
- nettoyage industriel
- entretien véhicules

---

### 🧩 Mots-clés essentiels
nettoyage après travaux, nettoyage industriel, entretien véhicules

---

### ⚠️ Points de vigilance
- risque de capturer l'entretien de véhicules (9531G).

---

### ☑️ Décision finale
- [ ] RETENIR  
- [x] À MODIFIER  
- [ ] À REJETER  

---

### CLUSTER_LOGISTIQUE_009 — Transport et logistique

**Code NAF :** 49.41H  

---

### 📊 Impact sur la base d’apprentissage
- Volume total : 4 232
- Volume à corriger : 4 213
- Volume déjà correct : 19

---

### 🎯 Impact métier réel
99 % de corrections nécessaires

---

### ⚠️ Risque de bruit (effets de bord)
- Niveau : Élevé
- Causes principales :
  - confusion majeure avec 7020Y et 4941G

- 🔎 Exemples de cas problématiques (effets de bord potentiels) :
  - logistique (7020Y)
  - transport routier de personnes (4941G)

👉 Ces exemples ne sont pas des erreurs certaines, mais des cas limites pouvant être affectés par la règle.

---

### 🎯 Décision recommandée (métier)
Sécuriser impérativement avant déploiement : risque de confusion critique avec les holdings (7020Y).

---

### 🎯 Activité métier (simplifiée)
Transport, logistique et entreposage de marchandises.

---

### 🧠 Règle métier (simplifiée)
Identifier le transport routier de marchandises et les services de stockage.

---

### 🔎 Exemples représentatifs
- transport routier
- logistique
- entreposage

---

### 🧩 Mots-clés essentiels
transport routier, logistique, entreposage

---

### ⚠️ Points de vigilance
- Risque énorme de confusion avec les holdings (7020Y).
- Risque de confusion avec le transport de personnes (4941G).

---

### ☑️ Décision finale
- [ ] RETENIR  
- [x] À MODIFIER  
- [ ] À REJETER  

---

### CLUSTER_INTERMEDIATION_010 — Intermédiation commerciale

**Code NAF :** 82.40  

---

### 📊 Impact sur la base d’apprentissage
- Volume total : 2 038
- Volume à corriger : 2 038
- Volume déjà correct : 0

---

### 🎯 Impact métier réel
100 % de corrections nécessaires

---

### ⚠️ Risque de bruit (effets de bord)
- Niveau : Élevé
- Causes principales :
  - dispersion vers 7020Y et 4619H

- 🔎 Exemples de cas problématiques (effets de bord potentiels) :
  - mise en relation (7020Y)
  - intermédiaire de vente (4619H)

👉 Ces exemples ne sont pas des erreurs certaines, mais des cas limites pouvant être affectés par la règle.

---

### 🎯 Décision recommandée (métier)
Investiguer pour différencier l'apport d'affaires du conseil ou du commerce de gros.

---

### 🎯 Activité métier (simplifiée)
Intermédiation commerciale et apport d'affaires.

---

### 🧠 Règle métier (simplifiée)
Identifier les activités de mise en relation commerciale.

---

### 🔎 Exemples représentatifs
- apporteur d'affaires
- mise en relation
- intermédiaire de vente

---

### 🧩 Mots-clés essentiels
apporteur d'affaires, mise en relation, intermédiaire de vente

---

### ⚠️ Points de vigilance
- forte dispersion vers les services de conseil (7020Y) et le commerce de gros (4619H).

---

### ☑️ Décision finale
- [ ] RETENIR  
- [x] À MODIFIER  
- [ ] À REJETER