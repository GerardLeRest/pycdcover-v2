## Aperçu du logiciel

![Interface](ressources/interface.png)

## Exemple de jaquette maquette (1 CD)

Utilisé avec l’autorisation du groupe **CENT DÉTRESSES**.  
@CENT DÉTRESSES

![Jaquette_maquette](ressources/jaquette_maquette.png)

## Exemple de jaquette multi-albums

Les images ci-dessous servent uniquement de démonstration.  
Elles sont distribuées à titre non commercial et en basse résolution.

![Jaquette_multi-albums](ressources/jaquette-multi-albums.png)

# 1. Présentation

**PyCDCover** est un logiciel qui permet de créer une jaquette regroupant les différentes informations d’un album (auteur, titre, année, genre, image).

Le logiciel récupère automatiquement :

- les **tags** depuis les fichiers audio du CD,

- les **images d’albums** sur les sites iTunes ou MusicBrainz, à partir des tags (auteur – album).

Si aucune image n’est trouvée, elle est remplacée par une **image orange** portant le nom de l’artiste et de l’album.
Vous pouvez aussi **modifier librement les images** (bouton Changer) et **éditer/modifier les tags** à votre convenance.

---

## 2. Installation de l’environnement

## 2.1. GNU/Linux

### a) Installer Python et les outils nécessaires

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

### b) Téléchargement du programme
Ouvrez un terminal et placez-vous dans le répertoire de travail (~/Bureau par exemple):

```bash
git clone git@github.com:GerardLeRest/pycdcover-v2.git
cd pycdcover-v2
```

### c) Créer un environnement virtuel

```bash
python3 -m venv mon_env
```

### d) Activer l’environnement

```bash
source mon_env/bin/activate
```

### e) Installer les dépendances

```bash
pip install -r requirements.txt
```

Le fichier `requirements.txt` contient la liste des paquets nécessaires au projet.

### f) Lancement

Dans le répertoire du projet, exécutez :
```python
python3 Main.py
```

## 2.2. Sous Windows

### Téléchargement (version 9.0.0)

La dernière version stable de **PyCDCover** est disponible ici :
➡️ [Télécharger PyCDCover.exe — v9.0.0](https://github.com/gerardlerest/pycdcover/releases/tag/v9.0.0)

Cette version inclut toutes les dernières "optimisations majeures" du projet.

---

## 3. Fonctionnement du programme

1. Insérez le CD avec les fichiers correctement tagués.
2. Créez le **titre du CD** (1ʳᵉ icône à gauche).
3. **Récupérez les tags et les images** sur Internet via *MusicBrainz* (2ᵉ icône).
4. **Éditez ou modifiez les tags** si nécessaire (3ᵉ icône).
5. **Créez les images avant et arrière du CD** (4ᵉ icône).
6. **Générez le fichier PDF** découpable et imprimable.

---

## 5. Informations et Licences

**Informations sur le logiciel**

PyCDCover – Générateur de jaquettes de CD audio
Auteur : Gérard LE REST
Licence : GNU GPL v3
© Gérard LE REST
Email : gerard.lerest@orange.fr
"Créé le" 01-04-2010
Dernière mise à jour : 2025-10-18

**Licence** :

- **Licence libre : GNU GPL v3 (ou version ultérieure)**  
  Ce programme est un logiciel libre : vous pouvez le modifier et le redistribuer
  selon les termes de la Licence publique générale GNU (GPL-V3),
  version 3 ou toute version ultérieure.  
  Il est fourni sans aucune garantie,
  ni de valeur commerciale, ni d’adéquation à un usage particulier.  
  [Consulter la licence GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html)
