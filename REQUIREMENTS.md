# Software Engineer Web API Aufgabe

## Globomantics Datenmanagement

### Globomantics heutiges Setup

Unsere Kunden können heute ihre Ortsnetzstationen über unsere Web-App pflegen.
Eine Station hat eine Adresse und besteht aus >=1 Trafo. Jeder Trafo hat >=1
Niederspannungsverteiler, welcher wiederum 1-20 Abgänge haben können.
Globomantic stellt verschiedene Messgeräte her, die in einer Station
installiert werden können, um Strom und Spannung zu messen. Jedes Messgerät hat
eine eigene Konfiguration und wird einer Stationskomponente (Trafo,
Niederspannungsverteiler oder Abgang) zugeordnet.

Messgeräte führen minütliche Messungen durch, die an die Globomantic Plattform
geschickt werden, wo sie validiert und aufbereitet werden. Dabei erhalten wir
Daten aus 10.000 Stationen bzw. von 100.000 Messgeräte.

In der Zukunft wollen wir weitere Messgeräte in die Globomantic Plattform
einbinden, eigene und von anderen Herstellern. Es sollen auch weitere
Komponenten des Niederspannungsnetzes in unserer Plattform gepflegt werden
können (z.B. Smart Meter, Kabellängen, Netztopologie). Diese Daten sollen
sowohl via API und Web-App in die Globomantic Systeme einspielbar sein.

### Aufgaben

1. Erstelle eine API zum Verwalten der Ortsnetzstationen und Messdaten von
   Globomantic. Es sollte möglich sein Ortnetzstationen und ihre Komponenten
über die API anzulegen, zu verändern und zu löschen. Zudem sollte die API die
Messdaten der verschiedenen Messgeräte entgegennehmen und speichern. Es sollte
auch möglich sein, die Messdaten einer Station für einen bestimmten Zeitbereich
abzufragen.
2. Wir würdest dein gewähltes Datenmodell erweitern, um die oben beschriebenen
   zukünftigen Daten zu integrieren?

### Randbedingungen

Du kannst eine der folgenden Programmiersprachen verwenden, um die Aufgabe zu
erledigen: Go, Python oder Kotlin. Wenn du möchtest, kannst du vorhandene
Frameworks oder Libraries verwenden, um die Aufgabe zu lösen. Kennzeichne gern
deinen Einsatz von Generative AI.

### Evaluierung

Deine Lösung sollte deine Fähigkeiten demonstrieren guten production-level code
zu schreiben mit allem, was dazugehört und uns zeigen, wie du Software
konzeptionierst und an Problemstellungen herangehst.
