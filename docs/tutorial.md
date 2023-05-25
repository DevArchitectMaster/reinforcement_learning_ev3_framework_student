# Cheatsheet: small introduction tutorial for a better start

## Überblick

### wichtige Dateien

```simulation/sim_world/``` | ```robot/ev3/``` | Hinweis
-------- | -------- | --------
```../main_sim.py```   | ```main_robot_micpy.py```   | <ul> <li>Einstiegspunkt für die eigene Implementierung</li> <li>hier sollten Sie <ul> <li>Sensorwerte vorverarbeiten,</li> <li>Actions definieren,</li> <li>...</li> </ul> </li> <li>...</li> </ul>
```/envs/car_0/ev3_sim_car.py```   | ```ev3_robot_car.py```   | <ul> <li>Definition des Autos   (_kann beim Verständnis weiterhelfen_) </li> <li>gemeinsame Bestandteile:</li> <ul> <li>```MotorTank```</li> <ul> <li>```__init__()```</li> <li>```drive()```</li> </ul> <li>```SensorUltrasonic```</li> <ul> <li>```__init__()```</li> <li>```read()```</li> </ul> <li>```SensorInfrared```</li> <ul> <li>```__init__()```</li> <li>```read()```</li> </ul> <li>```EV3Car``` *bzw.* ```SimCar```</li> <ul> <li>```__init__()```</li> <li>```init_robot_input_and_output()```</li> <li>```observe()```</li> <li>```action()```</li> <li>~~_weitere Hilfsmethoden nur für die Simulation_~~</li> </ul> <li>~~```_BlueprintDistanceMeasure```~~</li> </ul> </ul>

---

## Simulation

### wichtige Dateien

> ```simulation/sim_world/```

* ```envs/``` => [Gym Envs](https://www.gymlibrary.dev/content/environment_creation/)

  * ```car_0/``` => ...

    * ```ev3_sim_car.py``` => virtuelles Auto - Definition (_siehe oben_)

  * ```pygame_0/``` => ...

    * ```ev3_sim_pygame_2d_V2.py``` => Simulationsumgebung in ```PyGame```

  * ```simulation_env.py``` => benutzerdefinierte Umgebung

* ```maps/open_world``` => offene Trainingskarten

* ```maps/race_tracks``` => Trainingskarten mit definiertem Start und Ziel

* ```../main_sim.py``` => Main (_siehe oben_)

---

## EV3

### wichtige Dateien

> ```robot/ev3/```

* ```main_robot_micpy.py``` => Main (_siehe oben_)

* ```ev3_robot_car.py``` => reales Auto - Definition (_siehe oben_)

* ```policy.json``` => State-Action-Zuordnungstabelle

---

## Reinforcement Learning Agenten (Alogrithmen)

### wichtige Dateien

> ```simulation/reinforcement_agents/```

* ```agents/``` => alle zur Verfügung stehenden RL Agenten

  * ... => ...

* ```utils/``` => Ansammlung an Hilfsmethoden

  * ... => ...

---