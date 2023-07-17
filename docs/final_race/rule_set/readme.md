# Organisatorisches

## Ziel
Ihr Roboter schafft es in einem generischen Labyrinth in begrenzter Zeit ins Ziel zu kommen

## Anforderung
* Schreiben und Trainieren Sie einen selbstlernenden Agenten, den Sie später auf Ihren Roboter exportieren   
=> _Beinhaltet: Verfahren, Policy, …_
* ~~Bauen Sie Ihren Roboter so, dass sich alle notwendigen Sensoren und Aktoren an den richtigen Stellen befinden~~

## Aufgabe
* Bilden Sie hierzu selbstorganisierte Teams (2-3er Gruppen)
* Setzen Sie die Aufgabenstellung mit der Programmiersprache Python und den LEGO Mindstorms EV3 Bauteilen um

---
---
---

# ⚠️ Regelwerk ⚠️

## Aufbau der Rennstrecke
* das Labyrinth bzw. die Rennstrecke besteht aus Ordnern und Karton-Elementen
* jedes Team hat die Möglichkeit, gemeinsam Teilelemente der Strecke zu gestalten   
  => _dazu erhält jedes Team 4 Ordner und 2 Karton-Elementen_
* auf der Rennstrecke vergibt die Rennleitung (Dozent) verschiedene Checkpoints 
* die finale Rennstrecke wird durch den Dozenten abgenommen



## Finales Rennen

### Regeln
* die Fahrtzeit beginnt, sobald der Roboter die Startlinie überfahren hat
* die Fahrtzeit endet, sobald der Roboter komplett die Ziellinie überquert hat
* die Fahrtzeit ist eine reine Nettozeit, d.h. darauf werden anschließend noch die Strafzeiten addiert
* **Strafzeiten**:  
  => _Strafzeiten sind pro Vergehen zu addieren!_    
  | Strafzeit | Vergehen |
  | --------- | -------- |
  | 00:05:00 | Umgebung (Wände) länger als 3 Sekunden am Stück berühren |
  | 00:15:00 | Umgebung (Wände) umfahren / beschädigen |
  | 00:10:00 | leichtes händisches Eingreifen (_z.B. Drehung um weniger als 22,5°_) |
  | 00:30:00 | schweres händisches Eingreifen (_z.B. Drehung um mehr als 22,5°_) |
  | 00:15:00 | Robotor vom Checkpoint starten lassen |
  | 00:30:00 | Robotor vom Start neustarten lassen |
  | 01:00:00 | Robotor vom Start neustarten lassen und die bisherige Nettozeit verwerfen |
  |  | |
  | ~~15:00:00~~ **undefined** | maximale Zeit auf der Rennstrecke (_time undefined_) |

### Vorgehen & Ablauf
* 3 verschiedene Roboter mit denen jeweils maximal 3 Durchläufe absolviert werden dürfen
  * bester Durchlauf (_enthält bereits die aufaddierten Strafzeiten_) der drei Versuche pro Roboter werden gezählt
  * die drei Bestzeiten werden dann zwischen den Gruppen verglichen
  * die Durchschnittszeit der drei Bestzeiten ermittelt das Gesamtsieger-Team   
  => $$ f(x) = \frac {\sum\limits_1^n \min_{\{t\}} Einzelzeiten}{n} ; n = 3 $$

### Beispiel
* **Einzelzeiten**:
  * Roboter 1:
    - [x] 00:35:12
    - [ ] 00:39:55
    - [ ] 00:37:05
  * Roboter 2:
    - [ ] 00:36:42
    - [ ] 00:34:22
    - [x] 00:33:08
  * Roboter 3:
    - [x] 00:34:04
    - [ ] 00:36:64
    - [ ] 00:35:91
* **Durchschnittszeit**:   
  => (00:35:12 + 00:33:08 + 00:34:04) / 3 = 01:42:24 / 3 = **00:34:08**

### Bestenliste
[🥳 Highscore List 🏆](highscore_list.md)