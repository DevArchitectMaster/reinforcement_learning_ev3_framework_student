# Submission at the end of term

## Prüfungsleistung: Portfolioprüfung

* Entwicklung und Umsetzung des Projektes
* schriftliche Dokumentation
* Abschlusspräsentation und Vorstellung des Prototypen


## Abgabe

> * **Entwicklung und Umsetzung des Projektes bzw. Prototyp**  
    \> Programmcode als gepackte ZIP-Datei

> * **schriftliche wissenschaftliche Ausarbeitung & Reflexion**<sup>†</sup>  
    \> Umfang 40.000 - 45.000 Zeichen (mit Leerzeichen) pro Person in [IEEE-Vorlagen-Format](http://www.ieee.org/conferences/publishing/templates.html)  
       => _80.000 - 90.000 Zeichen (mit Leerzeichen) gemeinsam als 2er Gruppe_   
    \> RL-Inhalte, UML-Diagramme, Projektplan & -ablauf, Reflexion  

> * **Demonstrationsvideo**

> * **Abschlusspräsentation und Vorstellung des Prototypen**  
\> als PDF-Datei

          - Inhalte:
            - Wie haben Sie Ihren Reward gestaltet?
            - Welche Agents haben Sie ausprobiert und verwendet? Warum?
            - Wie verarbeiten Sie Ihre Inputs vor (Unterschied Simulation und reale Welt) und wie gestalten Sie ihre Outputs?

### <sup>†</sup>schriftliche wissenschaftliche Ausarbeitung & Reflexion

* **Einleitung**
  * Motivation
  * Ziel
  * Forschungsfrage(n)
  * Abgrenzung verwandte Arbeiten (_Related Work_)
  * Überblick

* **Grundlagen**
  * Verwendete RL-Algorithmen<sup>1</sup>
  * Roboter<sup>1</sup>
  * Sensoren<sup>1</sup>
  * Aktoren<sup>1</sup>
  * Simulation der realen Welt für Trainingszwecke
    > Wie kann die reale Welt simuliert werden?  
    > Pro, Con & Limitierungen<sup>1</sup>

* **methodisches Vorgehen**
  * Observations<sup>1</sup> und deren Datenverarbeitung (_mit UML-Zustandsdiagramm_)
  * Actions<sup>1</sup> (_mit UML-Zustandsdiagramm_)
  * States<sup>1</sup> (_mit UML-Zustandsdiagramm_)
  * Value Function<sup>1</sup>
  * Reward(-Function)<sup>1</sup>  (_mit UML-Klassen-, Sequenz- und Aktivitätsdiagramm_)
    > Ansätze: Was, warum und wie?
  * Trainingskonzept<sup>1</sup>
    > Begründung der Wahl des Konzeptes und des Environments
  * Transfer (_Anpassungen der Datenverarbeitung_)<sup>1</sup>
    > Aufgetretene Probleme?  
    > Angewandte Lösungen?
  * Bewertung & Vergleich von Agents bzw. gelernten Q-Tables<sup>1</sup>

* **Experimente**
  * Trainingsverlauf und dessen Auswertung
  * Bewertung von Agents (_Simulation & reale Welt_)
    > Welche sind gut bzw. besser als andere?
  * Diskussion (_Interpretation & Begründung_) der vorliegenden Ergebnisse
  * nächsten Schritte und deren Hypothesen

* **Reflexion**
  > _Wird **inhaltlich** nicht bewertet!_
  * _Was lief schief? Was würden Sie beim nächsten Projekt/Durchgang anders machen und warum?_
  * _Was lief gut?_
  * persönliches Fazit des Projektes (_**nicht** inhaltlich!_)

* **Fazit**
  * _Forschungsfrage beantwortet?_
  * _Wurde das Ziel erreicht?_
  * _Gab es Probleme? Wie wurden diese gelöst?_

* **Ausblick**
  * _Was könnte man noch machen, wenn Sie mehr Zeit hätten?_
  * _Was machen andere noch, was Sie nicht geschafft haben?_

> __Bitte denken Sie bei der Abgabe noch mit dran, dass Sie ein weiteres Dokument mit abgeben, aus dem hervorgeht, wer welches Kapitel der schriftlichen Ausarbeitung verfasst hat!__

<sup>1</sup> _mit korrekten Quellenangaben_


## Eingriffsmöglichkeiten

> * Welche Kombination aus  
>   * **Agent**,  
>   * **Hyperparametern** und  
>   * **Environment**  
> 
>   liefert eine gute Performance?

### Roboter - Stellschrauben

* Wie können die „rohen“ Messwerte der Sensoren verarbeitet werden, z.B. Fehlerkorrekturen?
* Wie kann mit der Ungenauigkeit von Motoren umgegangen werden?
* Wie kann aus den Sensorwerten ein Zustand (_State_) erzeugt werden, mit welchen „gute“ Aktionen gewählt werden müssen?
* Welche Aktionen (_Actions_) können ausgeführt werden?

### Simulations - Stellschrauben

* Wie kann die Performance von Agents in unterschiedlichen Simulationen bewertet werden?
* Environment
  * Wie kann die Reward-Function (_sim_world>envs>pygame_0>ev3_sim_pygame_2d_V2.py: evaluate()_) gestaltet werden, sodass der Agent das gewünschte Verhalten lernt?
* Agent
  * Feature Selection => Merkmalsauswahl => Irrelevante & Redundante Merkmale
  * Wie können States aus Sensorwerten erzeugt werden?
  * Welche Aktionen können ausgeführt werden?
  * Wie können die Sensoren und Motoren bzw. deren Ungenauigkeit simuliert werden?
