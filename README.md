# 1b2 WP3 "Accessibility Hub"

Casus: [opdracht](CASUS.md)

## Installeren

### Stap 1: Installeer Python 3.12 (indien nog niet geïnstalleerd).

Ga naar de officiële Python-website en download de installer voor Python 3.12:
https://www.python.org/downloads/release/python-3120/

Let op: Zorg ervoor dat de optie **'Add Python to PATH'** is aangevinkt tijdens de installatie, zodat Python
toegankelijk is via de terminal.

### Stap 2: Maak een locale kloon van de repository.

Clone de repository naar uw lokale machine door het volgende commando uit te voeren:

```shell
git clone https://github.com/Rac-Software-Development/wp3-2025-rest-1-b2.git
```

### Stap 3: Navigeer naar de repository-map.

Navigeer naar de map van de gekloonde repository:

```shell
cd wp3-2025-rest-1-b2
```

### Stap 4: Maak een virtuele omgeving aan.

Maak een virtuele omgeving aan om de benodigde Python-pakketten geïsoleerd te installeren:

```shell
python -m venv .venv
```

### Stap 5: Activeer de virtuele omgeving.

Activeer de virtuele omgeving die zojuist is aangemaakt:

```shell
.\.venv\Scripts\activate
```

### Stap 6: Installeer de vereiste pakketten.

Installeer de benodigde Python-pakketten door het onderstaande commando uit te voeren:

```shell
pip install -r requirements.txt
```

### Stap 7: Genereer de database

Om de SQLite-database aan te maken, kunt u het volgende commando uitvoeren:

```shell
flask init-db
```

Als u een database met dummydata wilt genereren, kunt u het volgende commando gebruiken:

```shell
flask init-db-data [factor]
```

Waarbij `[factor]` een **optionele** vermenigvuldigingsfactor is voor het aantal dummy records. Laat de parameter weg om
de standaardwaarde te gebruiken.
**Voorbeeld zonder factor:**

```shell
flask init-db-data
```

Dit commando maakt tussen de 10 en 25 dummy gebruikers en 5 tot 15 dummy bedrijven aan.
**Voorbeeld met factor:**

```shell
flask init-db-data 100
```

Dit commando genereert 100 keer zoveel dummy records als de standaarddatabase.

## Applicatie opstarten

Wanneer u zich in de virtuele omgeving bevindt, kunt u de applicatie starten met het volgende commando:

```shell
flask run
```