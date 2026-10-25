# Process Mining eines Kreditantragsprozesses mit lokalem KI-Assistenten

Aus den Event-Logs einer Bank rekonstruiere ich, wie Kreditanträge tatsächlich bearbeitet werden, wo Zeit und Kunden verloren gehen, und baue einen KI-Assistenten, der Fragen zum Prozess beantwortet, **komplett lokal**, sodass die Prozessdaten den Rechner nie verlassen.

> **Status: Work in progress** (begonnen im Oktober 2026)

| Schritt | Inhalt | Stand |
|---|---|---|
| Setup | Daten laden, prüfen, als Parquet speichern ([`src/load.py`](src/load.py)) | ✅ |
| Datenexploration | Aktivitäten, Antragsausgänge, erste Hypothesen ([Notebook 01](notebooks/01_datenexploration.ipynb)) | ✅ |
| Process Discovery | Prozessgraph, Varianten, Inductive Miner | 🔄 als Nächstes |
| Performance & Engpässe | Durchlaufzeiten, Wartezeiten, Nacharbeit | ⏳ geplant |
| KI-Assistent | Lokales LLM (Ollama) mit Tool Calling auf vordefinierte Analysefunktionen | ⏳ geplant |
| Dashboard | Streamlit-App mit Kennzahlen und Chat | ⏳ geplant |
| Conformance Checking | Abgleich mit einem selbst modellierten Soll-Prozess (BPMN) | ⏳ optional |

## Daten

[BPI Challenge 2017](https://doi.org/10.4121/uuid:5f3067df-f10b-45da-b98b-86ae4c7a310b): reale Kreditanträge eines niederländischen Finanzinstituts, Januar 2016 bis Februar 2017.

| | |
|---|---|
| Anträge (Cases) | 31.509 |
| Events | 1.202.267 |
| Aktivitäten | 26, in drei Gruppen: `A_` Antragsstatus, `O_` Angebote, `W_` Arbeitsschritte |

Die Integrität der Datei wird über die MD5-Prüfsumme der offiziellen Quelle sowie über automatische Plausibilitätsprüfungen beim Laden sichergestellt.

## Erste Erkenntnisse

**Wie enden die Anträge?** 55 % werden bewilligt, 12 % von der Bank abgelehnt, und **33 % abgebrochen**.

**Warum wird jeder dritte Antrag abgebrochen?** Die naheliegende Vermutung, dass Kunden aktiv absagen, halten die Daten nicht:
- 76 % der Abbrüche werden vom System gebucht, nicht von Mitarbeitenden.
- Zwischen dem letzten Angebot und dem Abbruch liegen im Median 30,7 Tage; die Hälfte aller Fälle liegt zwischen 30,5 und 30,8 Tagen.
- Nur bei 9 % der abgebrochenen Anträge hatte der Kunde überhaupt ein Angebot zurückgeschickt.

Das deutet auf eine **automatische Stornierung nach rund 30 Tagen ohne Kundenreaktion** hin (aus den Daten erschlossen, nicht dokumentiert). Die Bank verliert diese Kunden also nicht durch Ablehnung, sondern durch Funkstille. Ob die bestehenden Nachfass-Anrufe rechtzeitig kommen und wirken, untersuche ich im nächsten Schritt.

Details und Herleitung: [Notebook 01](notebooks/01_datenexploration.ipynb)

## Geplante Architektur des Assistenten

Das Sprachmodell rechnet nicht selbst und erzeugt keinen Code. Es wählt aus einem festen Satz geprüfter Analysefunktionen (Tool Calling) aus. Python liefert die Zahlen, das Modell formuliert die Antwort. Das macht die Antworten nachvollziehbar und verhindert erfundene Kennzahlen. Das Modell läuft lokal über [Ollama](https://ollama.com), weil Prozessdaten von Banken und Versicherungen in der Regel nicht an externe Cloud-Dienste gehen dürfen.

## Projektstruktur

```
data/raw/          Original-Log (nicht im Repo, siehe Installation)
data/processed/    aufbereitete Daten als Parquet (nicht im Repo)
notebooks/         Analysen, nummeriert in Arbeitsreihenfolge
src/               wiederverwendbarer Code (Laden, später Analysefunktionen und Assistent)
app/               Streamlit-Dashboard (geplant)
reports/figures/   Grafiken
```

## Installation

Voraussetzungen: [Anaconda/Miniconda](https://www.anaconda.com) und die Datei `BPI Challenge 2017.xes.gz` von der [Datenquelle](https://doi.org/10.4121/uuid:5f3067df-f10b-45da-b98b-86ae4c7a310b) in `data/raw/`.

```bash
git clone https://github.com/matteo-went/process-mining-assistant.git && cd process-mining-assistant
conda create -n pm python=3.11 -y && conda activate pm
pip install -r requirements.txt
python src/load.py
```

Danach lassen sich die Notebooks in `notebooks/` ausführen.

## Quelle

van Dongen, B. F. (2017). *BPI Challenge 2017* [Data set]. 4TU.ResearchData. https://doi.org/10.4121/uuid:5f3067df-f10b-45da-b98b-86ae4c7a310b

## Hinweise

Entwickelt mit KI-Unterstützung (Claude Code). Analyse, Interpretation und Designentscheidungen stammen von mir.

Lizenz: [AGPL-3.0](LICENSE), passend zur verwendeten Bibliothek [PM4Py](https://processintelligence.solutions/pm4py).
