# Process Mining eines Kreditantragsprozesses

In diesem Projekt analysiere ich die Event-Logs eines Kreditantragsprozesses mit Process-Mining-Methoden. Ziel ist es nachzuvollziehen, wie Anträge tatsächlich bearbeitet werden und wo Zeit und Kunden verloren gehen. Im zweiten Teil soll ein lokal laufendes Sprachmodell Fragen zum Prozess beantworten können, ohne dass die Daten den Rechner verlassen.

Das Projekt ist noch in Arbeit (begonnen im Oktober 2026).

## Stand

Abgeschlossen:
- Laden und Prüfen des Event-Logs, Speicherung als Parquet (`src/load.py`)
- Datenexploration: Aktivitäten, Ausgänge der Anträge, erste Hypothesen (`notebooks/01_datenexploration.ipynb`)

Geplant:
- Process Discovery (Directly-Follows-Graph, Varianten, Inductive Miner)
- Durchlaufzeiten, Wartezeiten und Nacharbeit
- Assistent auf Basis eines lokalen LLM (Ollama), der vordefinierte Analysefunktionen aufruft
- Dashboard mit Streamlit
- optional: Conformance Checking gegen einen selbst modellierten Soll-Prozess in BPMN

## Daten

Verwendet wird der Datensatz der [BPI Challenge 2017](https://doi.org/10.4121/uuid:5f3067df-f10b-45da-b98b-86ae4c7a310b). Er enthält Kreditanträge eines niederländischen Finanzinstituts aus dem Zeitraum Januar 2016 bis Februar 2017: 31.509 Anträge mit insgesamt 1.202.267 Events und 26 verschiedenen Aktivitäten. Die Aktivitäten sind nach Präfix gruppiert in Antragsstatus (`A_`), Angebote (`O_`) und Arbeitsschritte (`W_`).

Beim Laden prüft `src/load.py`, ob die Anzahl der Events und Anträge mit der Datensatzbeschreibung übereinstimmt.

## Erste Ergebnisse

Von den Anträgen werden 55 % bewilligt, 12 % von der Bank abgelehnt und 33 % abgebrochen. Dass jeder dritte Antrag abgebrochen wird, hat mich überrascht, deshalb habe ich mir diese Fälle genauer angesehen.

Meine erste Vermutung war, dass Kunden das Angebot aktiv ablehnen. Das bestätigen die Daten nicht. 76 % der Abbrüche werden von einem System-User gebucht, und zwischen dem letzten versendeten Angebot und dem Abbruch liegen im Median 30,7 Tage. Die Hälfte aller Fälle liegt zwischen 30,5 und 30,8 Tagen. Nur bei 9 % der abgebrochenen Anträge hatte der Kunde überhaupt ein Angebot zurückgeschickt.

Das spricht für eine automatische Stornierung, wenn sich der Kunde rund 30 Tage nach dem Angebot nicht meldet. Diese Regel leite ich aus den Daten ab, dokumentiert ist sie nicht. Als Nächstes möchte ich untersuchen, ob die Nachfass-Anrufe (`W_Call after offers`) vor Ablauf dieser Frist stattfinden und ob sie einen Abbruch verhindern.

Die Herleitung steht in `notebooks/01_datenexploration.ipynb`.

## Geplanter Assistent

Das Sprachmodell soll keine Zahlen selbst berechnen und keinen Code erzeugen. Stattdessen wählt es aus festgelegten Analysefunktionen die passende aus (Tool Calling), Python berechnet das Ergebnis, und das Modell formuliert daraus die Antwort. So bleiben die Zahlen nachvollziehbar. Das Modell läuft lokal über Ollama, weil Prozessdaten von Banken und Versicherungen in der Regel nicht an externe Dienste übermittelt werden dürfen.

## Installation

Benötigt werden Anaconda oder Miniconda sowie die Datei `BPI Challenge 2017.xes.gz` aus der oben verlinkten Quelle. Die Datei gehört nach `data/raw/`.

```bash
git clone https://github.com/matteo-went/process-mining-assistant.git
cd process-mining-assistant
conda create -n pm python=3.11 -y && conda activate pm
pip install -r requirements.txt
python src/load.py
```

Anschließend können die Notebooks im Ordner `notebooks/` ausgeführt werden.

## Quelle

van Dongen, B. F. (2017). BPI Challenge 2017 [Data set]. 4TU.ResearchData. https://doi.org/10.4121/uuid:5f3067df-f10b-45da-b98b-86ae4c7a310b

## Hinweise

Bei der Umsetzung habe ich Claude Code als KI-Unterstützung genutzt. Analyse, Interpretation und Designentscheidungen stammen von mir.

Lizenz: AGPL-3.0 (siehe `LICENSE`), da das Projekt auf PM4Py aufbaut.
