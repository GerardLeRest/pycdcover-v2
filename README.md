<p align="center">
  🇬🇧 English | <a href="README.fr.md">🇫🇷 Français</a>
</p>

# PyCDCover

# 1. Presentation

**PyCDCover** is a software tool designed to create audio CD covers (sleeves) from album information (artist, title, year, genre, image).

The software automatically retrieves:

- **tags** from audio files;
- **album artworks** from *iTunes* based on tags (artist – album).

If no image is found, it is replaced with an **orange placeholder image** displaying the artist and album name.  
You can replace this image with one of your choice (preferably cropped).

Languages: French, English, Spanish, Breton

--- 

# 2. Illustrations

## 2.1 Example of a mock cover (1 CD)

Used with permission from the band **CENT DÉTRESSES**  
@CENT DÉTRESSES

<p align="center">
  <img src="ressources/jaquette_maquette.png" alt="mock cover">
</p>

## 2.2 Example of a multi-album cover

The images are sourced from Pixabay (Pixabay license).  
These are fictional albums.

<p align="center">
  <img src="ressources/jaquette-multi-albums.png" alt="multi-album cover">
</p>

## 2.3 Software preview

<p align="center">
  <img src="ressources/interface.png" alt="Interface">
</p>

---

# 3. Automatic Installation

## 3.1. Windows

The latest stable version of **PyCDCover** is available here:  
👉 https://github.com/GerardLeRest/pycdcover-v2/releases

Download PyCDCover.Setup-X.X.X.exe  
(where X.X.X corresponds to the version number, for example 2.2.1)

You can then proceed to section **5**.

---

## 3.2. GNU/Linux

➡️ **PyCDCover is available as an *AppImage***.

Download `PyCDCover-X.X.X-x86_64.AppImage`  
([Releases · GerardLeRest/pycdcover-v2 · GitHub](https://github.com/GerardLeRest/pycdcover-v2/releases))  
(where *X.X.X* represents the version number).

Make the file executable:

```bash
chmod +x PyCDCover-X.X.X-x86_64.AppImage
```

Run the program:

```bash
./PyCDCover-X.X.X-x86_64.AppImage
```

You can then proceed to section **5**.

---

# 4. Python Version — GNU/Linux

*(For users who want to run PyCDCover from the source code.)*

## 4.1 Install Python and required tools

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

## 4.2 Download the project

```bash
git clone git@github.com:GerardLeRest/pycdcover-v2.git
cd pycdcover-v2
```

## 4.3 Create a virtual environment

```bash
python3 -m venv my_env
```

### Activate the environment

```bash
source my_env/bin/activate
```

### Install dependencies

```bash
pip install reportlab PySide6 pillow requests mutagen music-tag
```

## 4.4 Run the application

```bash
python3 pycdcover.py
```

---

# 5. How the program works

## 5.1 Workflow with automatic image retrieval

1. Prepare a folder with your tagged music files. Do not use the CD drive directly as it may cause slowdowns or bugs. Copy your CD into a folder.

2. Create the **CD title** (first icon on the left).

3. **Retrieve tags** (second icon).

4. **Edit tags** if necessary (third icon).
   
   **Very important:**  
   check for any errors here.

5. **Download images automatically** via iTunes (fourth icon).

6. **Choose the cover color**

7. **Create front and back covers** (fifth icon).

8. **Generate the printable PDF**

---

## 5.2 Cover not found online

An orange placeholder image appears if an album image is not found online. iTunes may sometimes provide incorrect images. In case of an issue, follow this process:

Create title → retrieve MP3 tags → edit tags → download images → create covers → manually replace the image in folder (1) → create covers again → generate PDF

(1) ~/PyCDCover/miniatures is the thumbnails folder

Important note: follow this order to avoid returning to the previous configuration

---

## 5.3 Double albums

With a double album, duplicate images may appear on the front cover. To fix this:

Create title → retrieve MP3 → edit MP3 → download images → create covers → delete the unwanted image in folder (2) → create covers again → generate PDF

(2) ~/PyCDCover/miniatures is the thumbnails folder

Important note: follow this order to avoid returning to the previous configuration

---

# 6. Information and licenses

**PyCDCover – Audio CD Cover Generator**  
Author: Gérard LE REST  
License: GNU GPL v3  
© Gérard LE REST  
Email: ge.lerest@gmail.com  
Created: 01-04-2010  
Last update: 2026-01-15  

- [Official page](https://github.com/GerardLeRest/pycdcover-v2)
- [Documentation](https://doc.ubuntu-fr.org/pycdcover#liens)  
- [Website](https://gerardlerest.github.io/pycdcover/)

---

# 7. Licenses

## Image rights

PyCDCover uses Apple Inc.'s public API (iTunes Search API) to retrieve album artworks.

These images remain the property of their respective rights holders.  
They are stored locally and used for private purposes only.

This project is independent and not affiliated with or endorsed by Apple Inc.  
The user is solely responsible for the use of retrieved images.

## Free software license: GNU GPL v3 (or later)

This program is free software: you can modify and redistribute it under the terms of the GNU General Public License (GPL v3), or any later version.

It is provided **without any warranty**, express or implied.

👉 https://www.gnu.org/licenses/gpl-3.0.html

---

# 8. Project architecture

- PySide6: graphical user interface  
- ReportLab: PDF generation  
- Mutagen: MP3 tag reading  
- Requests: iTunes API  
- MVC architecture
