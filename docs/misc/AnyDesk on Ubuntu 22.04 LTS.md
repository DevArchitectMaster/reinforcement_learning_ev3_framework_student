# Install AnyDsk on 22.04

1. root rechte erhalten
    ```bash
    sudo su
    ```

1.  AnyDesk Installieren mit rootrechten
    
    
    3. add repository key to Trusted software providers list
	```bash 
	wget -qO - https://keys.anydesk.com/repos/DEB-GPG-KEY | apt-key add -
	```	
    4. add the repository:
	```bash 
	echo "deb http://deb.anydesk.com/ all main" > /etc/apt/sources.list.d/anydesk-stable.list
	```
	
    5. update apt cache:
	```bash 
	apt update
	```
	
    6. install anydesk:
	```bash
	apt install anydesk
	```
- nachdem das installiert wurde kann AnyDesk ausgeführt werden allerdings erscheint ein Fehler
	```bash
	anydesk
	anydesk: error while loading shared libraries: libpangox-1.0.so.0: cannot open shared object file: No such file or directory
	```
2. fehler beim ausführen beheben

	1. download fehlende pakete
	```bash
	wget http://ftp.us.debian.org/debian/pool/main/p/pangox-compat/libpangox-1.0-0_0.0.2-5.1_amd64.deb
	 ```
	2. instalieren der pakete
	```bash
	apt install ./libpangox-1.0-0_0.0.2-5.1_amd64.deb
	 ```
3. konfigurieren des bildschirm deamons
	
	1. datei öffnen
	```bash
	nano /etc/gdm3/custom.conf
	 ```
	2. den deamon bereich bearbeiten indem die folgenden Variablen unter deamon gesetzt werden
	```bash
	...
	[deamon]
	AutomaticLoginEnable=true
	AutomaticLogin=$USERNAME
	WaylandEnable=false
	...
	```
4. vm neu starten 
	```bash
	sudo reboot
	 ```
5. konfigurieren von anydesk 
	1. root rechte nach neustart erhalten
    ```bash
    sudo su
    ```
	2. erhalten der anydesk id 
	```bash
	anydesk --get-id
	```
	output merken und später in anydesk eingeben:
	```bash
	123 456 789
	```
	
	3. festlegen des anydesk passworts
	```bash
	echo "MyPassword" | anydesk --set-password
	```
ID in AnyDesk eingeben 
FERTIG!	
	