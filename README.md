# Aperçu du logiciel

![Interface](ressources/interface.png)

## Exemple de jaquette maquette (1 CD)

Utilisé avec l’autorisation du groupe **CENT DÉTRESSES**.  
@CENT DÉTRESSES

![Jaquette_maquette](ressources/jaquette_maquette.png)

## Exemple de jaquette multi-albums

Les images ci-dessous servent uniquement de démonstration.  
Elles sont distribuées à titre non commercial et en basse résolution.

![Jaquette_multi-albums](ressources/jaquette-multi-albums.png)

---

# 1. Présentation

**PyCDCover** est un logiciel permettant de créer une jaquette regroupant les informations d’un album (auteur, titre, année, genre, image).

Le logiciel récupère automatiquement :

- les **tags** depuis les fichiers audio du CD ;
- les **images d’albums** sur iTunes ou MusicBrainz, à partir des tags (artiste – album).

Si aucune image n’est trouvée, elle est remplacée par une **image orange** portant le nom de l’artiste et de l’album.  
Vous pouvez remplacer cette image par celle de votre choix (cadrée de préférence).

---

# 2. Installations automatiques

## 2.1. Sous Windows

La dernière version stable de **PyCDCover** est disponible ici :  
[Télécharger PyCDCover.Setup.exe et installer-le

(https://github.com/gerardlerest/pycdcover/releases/tag/v2.0.0)

Vous pouvez ensuite passer à la section 4.]

---

## 2.2. Sous GNU/Linux

➡️ **PyCDCover est disponible au format *AppImage***.

Installation : Télécharger PyCDCover_2.0.0_x86_64.AppImage (ou X.X.X représente le numéro de version. Se rendre dans le dossier de cette image et rendez le fichier exécutable

```bash
chmod +x PyCDCover_2.0.0_x86_64.AppImage
```

Lancement :

```bash
./PyCDCover_2.0.0_x86_64.AppImage
```

Vous pouvez ensuite passer à la section 4.

---

# 3. Utilisation Python — GNU/Linux

*(Pour les utilisateurs souhaitant lancer PyCDCover depuis les sources.)*

## 3.1. Installer Python et les outils nécessaires

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

## 3.2. Télécharger le programme

```bash
git clone git@github.com:GerardLeRest/pycdcover-v2.git
cd pycdcover-v2
```

## 3.3. Créer un environnement

```
### Activer l’environnement

```bash
source mon_env/bin/activate
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

## 3.4. Lancement

```bash
python3 Main.py
```

---

# 4. Fonctionnement du programme

## 4.1. Fonctionnement avec recherche automatique des images

1. Insérez le CD contenant les fichiers correctement tagués.  
2. Créez le **titre du CD** (1ʳᵉ icône à gauche).  
3. **Récupérez les tags et les images** via MusicBrainz ou Itunes (2ᵉ icône).  
4. **Éditez les tags** si nécessaire (3ᵉ icône).  **TRES IMPORTANT***: C'est ici que vous couperez les titres trop longs selon vos souhaits
5. **Créez les images avant et arrière** (4ᵉ icône).  
6. **Générez le PDF** découpable et imprimable.

---

## 4.2. Jaquette non référencée sur le web

Si une mauvaise image apparaît, voici la procédure :

1. Trouvez la bonne pochette sur Internet (512×512 recommandé).  
2. Enregistrez-la dans le dossier **thumbnails**,  
   → avec **exactement le même nom** que l’image incorrecte.  
3. Sélectionnez les albums modifiés
4. Recréez la face avant et la face arrière.  
5. Générez le PDF final.

**Remarque importante :**  
Ne cliquez pas sur “Récupérer les images”. Cela réinstallerait l’ancienne pochette.

---

# 5. Informations et licences

**PyCDCover – Générateur de jaquettes de CD audio**  
Auteur : Gérard LE REST  
Licence : GNU GPL v3  
© Gérard LE REST  
Email : gerard.lerest@orange.fr  
Créé le : 01-04-2010  
Dernière mise à jour : 2025-10-18  

---

## Licence

**Licence libre : GNU GPL v3 (ou version ultérieure)**  

Ce programme est un logiciel libre : vous pouvez le modifier et le redistribuer selon les termes de la Licence publique générale GNU (GPL v3), version 3 ou toute version ultérieure.  

Il est fourni sans aucune garantie — ni implicite ni explicite — concernant une valeur commerciale ou une adéquation à un usage particulier.  

[Consulter la licence GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html)
