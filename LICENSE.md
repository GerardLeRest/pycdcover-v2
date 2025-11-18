# PyCDCover

**PyCDCover** est un logiciel libre permettant de **générer automatiquement des jaquettes de CD audio** à partir des informations (tags) de vos fichiers musicaux.

Le programme crée la **face avant** et la **face arrière** de la jaquette, prêtes à être imprimées, en récupérant automatiquement :

- les **tags** (artiste, album, année, genre, titre des morceaux),
- les **images d’albums** depuis *MusicBrainz*,
- ou, si aucune image n’est trouvée, une **image orange** portant le nom de l’artiste et de l’album.

Vous pouvez ensuite :

- **modifier librement les images** (bouton *Changer*),
- **éditer les tags** directement depuis le programme,
- et **générer un PDF final** découpable et imprimable.

---

## ⚙️ 1. Installation de l’environnement

### a) Installer Python et les outils nécessaires

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

### b) Créer un environnement virtuel

```bash
python3 -m venv mon_env
```

### c) Activer l’environnement

```bash
source mon_env/bin/activate
```

### d) Installer les dépendances

```bash
pip install -r requirements.txt
```

> Le fichier `requirements.txt` contient la liste complète des paquets nécessaires au projet.

---

## ▶️ 2. Lancement du programme

Depuis le répertoire du projet, exécutez :

```bash
python3 Fenetre.py
```

ou, si le fichier est exécutable :

```bash
./Fenetre.py
```

---

## 💿 3. Utilisation

1. Insérez le CD contenant vos fichiers audio correctement **tagués**.  
2. Cliquez sur la **1ʳᵉ icône** pour créer le **titre du CD**.  
3. Cliquez sur la **2ᵉ icône** pour **récupérer les tags et les images** sur *MusicBrainz*.  
4. Utilisez la **3ᵉ icône** pour **éditer les tags** ou changer les images.  
5. Cliquez sur la **4ᵉ icône** pour **créer les faces avant et arrière**.  
6. Enfin, générez le **PDF imprimable**.

---

## 💾 4. Installation du projet

Ouvrir un terminal et saisir :

```bash
git clone https://github.com/GerardLeRest/pycdcover.git
cd pycdcover
```

Puis suivre les instructions d’installation ci-dessus.

---

## 🧱 5. Informations techniques

- **Nom :** PyCDCover – Générateur de jaquettes de CD audio  
- **Auteur :** Gérard LE REST  
- **Licence :** GNU GPL v3  
- **Créé le :** 01/04/2010  
- **Dernière mise à jour :** 29/10/2025  
- **Contact :** gerard.lerest@orange.fr

---

## 🪪 6. Licence

**Licence libre : GNU GPL v3 (ou version ultérieure)**  

Ce programme est un logiciel libre : vous pouvez le redistribuer et/ou le modifier selon les termes de la [Licence publique générale GNU, version 3](https://www.gnu.org/licenses/gpl-3.0.html), ou toute version ultérieure.  

Il est distribué **sans aucune garantie**, y compris sans garantie de valeur commerciale ou d’adéquation à un usage particulier.

---

## 🖼️ 7. Exemples de jaquettes

*(Ajouter ici deux captures d’écran : une “Maquette” et une “MultiCD”)*

---

## 🐧 8. Exécution sous Ubuntu

Après installation, le programme peut être lancé directement dans un terminal :

```bash
./Lancement_av_ar.py
```

ou installé comme commande système :

```bash
sudo cp Lancement_av_ar.py /usr/local/bin/pycdcover
```

Ensuite, vous pouvez simplement exécuter :

```bash
pycdcover
```

---

## 🪟 9. Exécution sous Windows

### a) Version exécutable (recommandée)

Une version Windows prête à l’emploi sera fournie : **`PyCDCover.exe`**.  
Elle permet de lancer le programme directement par double-clic, sans installation de Python.

Le programme crée automatiquement le dossier de travail :

```
C:\Users\<votre_nom>\PyCDCover\
```

et y enregistre les images et le fichier PDF générés.

> 💡 **Conseil :** placez `PyCDCover.exe` sur votre Bureau ou dans un dossier dédié à vos albums.

---

### b) Version Python (pour les utilisateurs avancés)

1. Ouvrez **PowerShell** ou l’invite de commande.  
2. Placez-vous dans le dossier du projet :  
   
   ```powershell
   cd C:\Users\<votre_nom>\Documents\PyCDCover
   ```
3. Créez un environnement virtuel :
   
   ```powershell
   python -m venv mon_env
   ```
4. Activez-le :
   
   ```powershell
   mon_env\Scripts\activate
   ```
5. Installez les dépendances :
   
   ```powershell
   pip install -r requirements.txt
   ```
6. Lancez le programme :
   
   ```powershell
   python Fenetre.py
   ```

---

## 🎯 10. À venir

- Génération d’un exécutable `.exe` stable pour Windows  
- Modernisation de l’interface graphique (PySide)  
- Publication des vidéos de démonstration :
  - 🎬 *Jaquette Maquette*
  - 🎬 *Jaquette MultiCD*

---

© **Gérard LE REST**, 2010–2025 — *Projet libre sous licence GNU GPL v3*
