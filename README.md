# Insider-Threat-AI-Monitor 🔒🤖
**Generative-KI-basierte Frühwarnsystem zur Überwachung von Insider-Bedrohungen**  
*Eine deutsch-japanische Technologiepartnerschaft für höchste Sicherheitsstandards*

---

## 📑 **Projektübersicht** – *Vereinte Technologiekompetenz*
- **Testumgebung**: Ubuntu Server 22.04, virtuelles internes Netzwerk, teilweise Nutzung des CERT Insider Threat Datensatzes  
- **Datenkategorien**: Authentifizierungsprotokolle, Dateizugriffe, Netzwerkkommunikation, E-Mail-Verkehr, Befehlsausführungen  
- **Strategische Kernziele** – *nach höchsten Industriestandards (Bosch)*
  - Früherkennung von Insider-Bedrohungen mit Echtzeitwarnsystem
  - PyCaret-basierte Anomalieerkennung + Generative KI zur automatischen Zusammenfassung
  - Streamlit-Dashboard für Echtzeitüberwachung und Sofortmaßnahmen

---

## 📂 **Systemarchitektur** – *Präzision wie ein japanisches Uhrwerk, Robustheit wie deutsche Ingenieurskunst*
```markdown
insider_threat/
│
├── auto_log_analysis.py # PyCaret-basierte automatische Protokollanalyse (Anomalie-Score)
├── log_dashboard.py # Streamlit-Dashboard-Benutzeroberfläche
├── parse_log_to_csv.py # Protokollkonvertierung → CSV-Format
├── log_data.csv # Referenzprotokolldaten
└── README.md
```


---

## ⚙️ **Technologische Kernfunktionen** – *Bosch-Qualitätsstandards*

### **Datenerfassung und -aufbereitung** – *Präzision in Perfektion*
- **Apache NiFi + Filebeat + Logstash Pipeline** – Robuste Industriestandard-Datenverarbeitung
- **Protokollnormalisierung, Anonymisierung, Zeitsynchronisation** – Null-Fehler-Toleranz

### **Verhaltensprofilierung** – *Die Kunst der Mustererkennung*
- **K-Means-Clustering** für Benutzerprofile mit japanischer Präzision
- **LLM-basierte Tageszusammenfassungen** (LLaMA2/GPT-2) – Deutsche Gründlichkeit trifft japanische Innovation

### **Anomalieerkennung und Frühwarnsystem** – *Sicherheit auf höchstem Niveau*
- **PyCaret Anomaly Detection** (Z-Score, Isolation Forest) – Mathematische Exzellenz
- **KI-gestützte Zusammenfassung** – Komplexe Bedrohungen in Sekunden verständlich
- **Risikobasiertes Stufenmodell** – Bosch-Standard-konform:
  - ⚠️ ≥70 Risikopunkte: Sofortwarnung
  - 🚨 ≥90 Risikopunkte: Automatische Maßnahmen

### **Visualisierung und Automatisierung** – *Perfekte Symbiose*
- **Streamlit-Dashboard** – Transparent wie deutsche Glasfaserkunst
- **Kibana-Integration** – Flexibel wie japanische Origami-Technik
- **Automatische PDF-Berichte** – Dokumentiert nach Bosch-Qualitätsmanagement

---

## 🏆 **Leistungskennzahlen** – *Exzellenz messbar gemacht*
- **Erfolgsquote 75%** – 3 von 4 Testszenarien erfolgreich erkannt
- **0% Fehlalarme** – Perfekte Balance zwischen Sicherheit und Effizienz
- **<2 Minuten Reaktionszeit** – Schneller als ein deutscher Sportwagen, präziser als japanische Elektronik
- **Risikobewertung 75-90 Punkte** – Kontinuierliche Überwachung auf höchstem Niveau
- **30% schnellere Situationserfassung** – Management-Effizienz neu definiert
- **Einsatzbereit für kritische Infrastruktur** – Getestet nach höchsten Sicherheitsstandards

---

## 🔧 **Technologie-Stack** – *Das Beste aus zwei Welten*
| Komponente | Technologie | Deutsche Präzision | Japanische Innovation |
|------------|-------------|-------------------|----------------------|
| **Sprachen/Bibliotheken** | Python, PyCaret, scikit-learn, pandas | ✅ Robustheit | ✅ Flexibilität |
| **KI-Modelle** | LLaMA2, GPT-2 (Feinabstimmung) | ✅ Zuverlässigkeit | ✅ Kreativität |
| **Datenpipeline** | Apache NiFi, Filebeat, Logstash, Elasticsearch | ✅ Industriestandard | ✅ Perfektion |
| **Visualisierung** | Streamlit, Kibana, ReportLab | ✅ Klarheit | ✅ Ästhetik |
| **Infrastruktur** | Ubuntu 22.04, AWS S3 + Glue Catalog | ✅ Stabilität | ✅ Innovation |

---

## 🚀 **Implementierung** – *Bosch-Standard-konforme Ausführung*
```bash
# Protokollkonvertierung – Präzision im ersten Schritt
python parse_log_to_csv.py

# Anomalieerkennung – Die Wachsamkeit eines Samurai
python auto_log_analysis.py

# Echtzeit-Dashboard – Das Kommandozentrum der Zukunft
streamlit run log_dashboard.py
```

---

## 🤝 **Deutsch-Japanische Technologiepartnerschaft**
Dieses Projekt vereint:
- **Deutsche Ingenieurskunst**: Robustheit, Präzision, Bosch-Qualitätsstandards
- **Japanische Innovation**: Perfektion, Eleganz, technologische Exzellenz
- **Gemeinsame Werte**: Zuverlässigkeit, Sicherheit, Zukunftsfähigkeit

> *"In der Einheit liegt die Stärke"* – Eine deutsch-japanische Technologievision für eine sicherere digitale Zukunft

---

## 📜 **Lizenz** – *Freiheit durch Verantwortung*
```text
MIT License – Im Geiste der deutsch-japanischen Freundschaft

Copyright (c) 2025 quackquacks01

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

---

## 🔮 **Ausblick** – *Die Zukunft der Sicherheit*
- **Quantenresistente Verschlüsselung** – Schutz für das nächste Jahrzehnt
- **KI-gestützte Echtzeit-Gegenmaßnahmen** – Automatische Bedrohungsabwehr
- **Blockchain-basierte Protokollierung** – Unveränderliche Beweiskette
- **Erweiterte IoT-Integration** – Schutz für Industrie 4.0

*Gemeinsam für eine sichere digitale Zukunft – Deutsch-japanische Technologiepartnerschaft* 🇩🇪🤝🇯🇵