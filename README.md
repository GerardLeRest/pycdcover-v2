# 1. Présentation

**PyCDCover** est un logiciel qui permet de créer une jaquette regroupant les différentes  
informations d’un album (auteur, titre, année, genre, image).

Le logiciel récupère automatiquement :

- les **tags** depuis les fichiers audio du CD,
- les **images d’albums** sur le site *MusicBrainz*, à partir des tags (auteur – album).

Si aucune image n’est trouvée, elle est remplacée par une **image orange** portant le nom de l’artiste et de l’album.  
Vous pouvez aussi **modifier librement les images** (bouton *Changer*) et **éditer les tags** à votre convenance.

---

## 2. Installation de l’environnement

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

Le fichier `requirements.txt` contient la liste des paquets nécessaires au projet.

---

## 3. Lancement

Dans le répertoire du projet, exécutez :

```python
python3 Fenetre.py
```

---

## 4. Fonctionnement

1. Insérer le CD avec les fichiers correctement tagués.
2. Créer le **titre du CD** (1ʳᵉ icône à gauche).
3. **Récupérer les tags et les images** sur Internet via *MusicBrainz* (2ᵉ icône).
4. **Éditer ou modifier les tags** si nécessaire (3ᵉ icône).
5. **Créer les images avant et arrière du CD** (4ᵉ icône).
6. **Générer le fichier PDF** découpable et imprimable.

---

## 5. Installation du projet

Ouvrir un terminal et se placer dans le répertoire de travail :

```bash
git clone git@github.com:GerardLeRest/pycdcover.git
cd pycdcover
```

Puis suivre les instructions ci-dessus.

---

## Information et Licence

**informations sur le logiciel**

PyCDCover – Générateur de jaquettes de CD audio
Auteur : Gérard LE REST
Licence : GNU GPL v3
© Gérard LE REST
email: gerard.lerest@orange.fr
Créé en : 01-04-2010
Dernière mise à jour : 2025-10-18

**Licence : GNU GPL v3 (ou version ultérieure)**

Ce programme est un logiciel libre : vous pouvez le modifier et le redistribuer
selon les termes de la Licence publique générale GNU (GPL-V3),
version 3 ou toute version ultérieure.

Il est fourni sans aucune garantie,
ni de valeur commerciale, ni d’adéquation à un usage particulier.
Pour plus d’informations, consultez la licence GPL-V3.

[Licence publique générale GNU v3 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.html)
