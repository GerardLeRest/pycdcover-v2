<p align="center">
  <a href="README-fr.md">🇫🇷 Français</a> | English
</p>

# PyCDCover: Automatic CD Cover and Booklet Creator

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)

**PyCDCover** is a **free and open-source software** designed to **automatically generate audio CD covers and booklets** (single or multi-album) from the information contained in your music files.

The software automates the entire process:

- **Tag extraction** directly from audio files (artist, title, year, genre);
- **Automatic album artwork download** from the *iTunes* API based on the Artist - Album pair.

If no image is found online, it is automatically replaced with a generic orange cover containing the artist and album name. Since the server may sometimes return incorrect images, you are always free to manually replace any image with one of your choice.

**Languages:** French, English, Spanish, Breton  
**Operating Systems:** GNU/Linux, Windows

---

# 2. Illustrations

## 2.1 Example of a demo cover (1 CD)

Used with permission from the band **CENT DÉTRESSES**  
@CENT DÉTRESSES

<p align="center">
  <img src="ressources/jaquette_maquette.png" alt="Demo CD cover">
</p>

## 2.2 Example of a multi-album cover

Images are taken from Pixabay (Pixabay license).  
These are fictional albums.

<p align="center">
  <img src="ressources/jaquette-multi-albums.png" alt="Multi-album CD cover">
</p>

## 2.3 Software preview

<p align="center">
  <img src="ressources/interface.png" alt="PyCDCover software interface">
</p>

---

# 3. Installation

## 3.1. Windows

The latest stable version of **PyCDCover** is available here:  
👉 https://github.com/GerardLeRest/pycdcover-v2/releases

Download `PyCDCover.Setup-X.X.X.exe`  
(where X.X.X corresponds to the version number, for example 2.2.1)

You can then proceed to section **5**.

---

## 3.2. GNU/Linux

➡️ **PyCDCover is available as an AppImage package**.

Download `PyCDCover-X.X.X-x86_64.AppImage`  
([Releases · GerardLeRest/pycdcover-v2 · GitHub](https://github.com/GerardLeRest/pycdcover-v2/releases))

(where *X.X.X* represents the version number).

Make the file executable:

```bash
chmod +x PyCDCover-X.X.X-x86_64.AppImage
```

Launch the program:

```bash
./PyCDCover-X.X.X-x86_64.AppImage
```

You can then proceed to section **5**.

---

# 4. Python Version — GNU/Linux

*(For users who want to run PyCDCover from source.)*

## 4.1. Install Python and required tools

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

## 4.2. Download the program

```bash
git clone git@github.com:GerardLeRest/pycdcover-v2.git
cd pycdcover-v2
```

## 4.3. Create a virtual environment

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

## 4.4. Launch

```bash
python3 pycdcover.py
```

---

# 5. How the program works

## 5.1. Automatic image search mode

1. Prepare your folder with properly tagged music files. Do not use the CD drive directly because it may cause slowdowns or bugs. Copy your CD contents into a folder first.

2. Create the **CD title** (1st icon on the left).

3. **Retrieve the tags** (2nd icon).

4. **Edit the tags** if necessary (3rd icon).
   
   **Very important:**  
   Check for possible errors here.

5. **Automatically download images** through iTunes (4th icon). Images provided by the server may sometimes be incorrect.

6. **Choose the cover color**

7. **Create the front and back covers** (5th icon).

8. **Generate the printable PDF**.

## 5.2. Cover not found or incorrectly referenced online

An orange image (with artist + album name) appears if an album cover was not found online. iTunes may also provide incorrect images. In all cases, if an image is incorrect, follow these steps:

Create title → retrieve MP3 tags → edit MP3 tags → download images → create both covers → manually replace the desired image in folder (1) → recreate both covers → generate PDF

(1) `~/PyCDCover/miniatures` is the thumbnails folder.

Important note: Follow the order above to avoid returning to the previous configuration.

## 5.3 Double albums

With a double album, if no action is taken, two identical images may appear on the front cover. Here is how to solve the issue easily:

Create title → retrieve MP3 tags → edit MP3 tags → download images → create both covers → delete the desired image in folder (2) → recreate both covers → generate PDF

(2) `~/PyCDCover/miniatures` is the thumbnails folder.

Important note: Follow the order above to avoid returning to the previous configuration.

---

# 6. Project Information

**PyCDCover – Audio CD Cover Generator**  
Author: Gérard LE REST  
License: GNU GPL v3  
© Gérard LE REST  
Email: ge.lerest@gmail.com  
Created on: 2010-04-01  
Last updated: 2026-01-15  

- [Official page](https://github.com/GerardLeRest/pycdcover-v2)
- [Documentation](https://doc.ubuntu-fr.org/pycdcover#liens)
- [Website](https://gerardlerest.github.io/pycdcover/)
- [LinuxFr journal](https://linuxfr.org/users/clisam/journaux/pycdcover-createur-automatique-de-jaquettes-pochettes-cd)

---

# 7. License and Image Rights

**Image rights**

PyCDCover uses Apple Inc.'s public API (iTunes Search API) to automatically retrieve album artwork.

These images remain the property of their respective copyright holders.  
They are stored locally between sessions and are intended for private use only.

This project is independent and is neither affiliated with nor endorsed by Apple Inc.  
The user is solely responsible for how the retrieved images are used.

**Free Software License: GNU GPL v3 (or later)**

This program is free software: you can modify and redistribute it under the terms of the GNU General Public License (GPL v3), version 3 or any later version.

It is provided **without any warranty**, either expressed or implied,  
including any warranty of merchantability or fitness for a particular purpose.

👉 [Read the GNU GPL v3 license](https://www.gnu.org/licenses/gpl-3.0.html)

---

# 8. Project Architecture

- PySide6: graphical interface
- ReportLab: PDF generation
- Mutagen: MP3 tag reading
- Requests: iTunes API
- Architecture: MVC model (business logic / interface / controller separation)
