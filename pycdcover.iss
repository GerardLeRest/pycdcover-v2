; ---------------------------------------------
; Script d'installation pour PyCDCover
; ---------------------------------------------

[Setup]
AppName=PyCDCover
AppVersion=2.0
AppPublisher=Gérard Le Rest
DefaultDirName={pf}\PyCDCover
DefaultGroupName=PyCDCover
OutputBaseFilename=PyCDCover-Setup
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes

; Icône utilisée pour l'installeur (mettre ton icone.ico à côté du .iss)
SetupIconFile=icone.ico

; Icône affichée dans "Programmes et fonctionnalités"
UninstallDisplayIcon={app}\Main.exe

[Files]
; Exécutable principal généré par PyInstaller
Source: "dist\Main.exe"; DestDir: "{app}"; Flags: ignoreversion

; Dossier ressources complet (icônes, polices, images, modèles)
Source: "ressources\*"; DestDir: "{app}\ressources"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Raccourci dans le menu Démarrer
Name: "{group}\PyCDCover"; Filename: "{app}\Main.exe"

; Raccourci sur le bureau (option proposée)
Name: "{commondesktop}\PyCDCover"; Filename: "{app}\Main.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Créer un raccourci sur le bureau"; Flags: unchecked

[Run]
; Lancer l'application juste après installation
Filename: "{app}\Main.exe"; Description: "Lancer PyCDCover"; Flags: nowait postinstall skipifsilent
