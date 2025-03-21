# 1b2 WP3 "Accessibility Hub"

Casus: [opdracht](CASUS.md)

## Installeren

### Stap 1: Installeer Python 3.12 (indien nog niet geïnstalleerd).

Ga naar de officiële Python-website en download de installer voor Python 3.12:
https://www.python.org/downloads/release/python-3120/

> [!warning]
> Zorg ervoor dat de optie **'Add Python to PATH'** is aangevinkt tijdens de installatie, zodat Python toegankelijk is via de terminal.

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
#Windows
.\.venv\Scripts\activate

#macOS/Linux:
source .venv/bin/activate
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
flask init-db-data 3
```

Dit commando genereert 100 keer zoveel dummy records als de standaarddatabase.

## Applicatie opstarten

Wanneer u zich in de virtuele omgeving bevindt, kunt u de applicatie starten met het volgende commando:

```shell
flask run
```
Open de browser en ga naar: http://127.0.0.1:5000 om de applicatie te openen.

Om de applicatie af te sluiten gebruik je `Ctrl+C`

En om je virtual environment te deactiveren gebruik je `deactivate`


## Homepage

Nu de applicatie is gestart bevind je je op de homepage. Op de homepagina heb je 3 opties:

![image](docs/images/ReadMe%20screenshots/homepage.png)

### Onderzoeksbureau

Deze pagina is bedoeld voor medewerkers van de organisaties. Hier staat de documentatie van de API waarmee de medewerkers onderzoeken kunnen aanmaken, bekijken en kunnen bewerken.

### Stichting accessibility

Deze pagina's zijn bedoeld voor de medewerkers van stichting Accessibility (de admins). Als je naar deze pagina gaat, zul je eerst moeten inloggen:

![image](docs/images/ReadMe%20screenshots/admin_login.png)

Nadat je in hebt gelogd kom je in het 'admin dashboard' terecht. Hier kunnen de admins CRUD-acties uitvoeren op de onderzoeksaanvragen, inschrijvingen en ervaringsdeskundigen. Dit kan op twee manieren:

#### Goed- of afkeuren
Het goed- of afkeuren van onderzoeksaanvragen, inschrijvingen en nieuwe ervaringsdeskundigen moet via het 'keuren'-scherm:

![image](docs/images/ReadMe%20screenshots/admin_dashboard_keuren.png)

Door op de 'details'-knop te drukken, word een kort overzicht van de gegevens van het onderzoek, inschrijving of ervaringsdeskundige getoond. Hier krijg je de optie om het gekozen object goed- of af te keuren:

![image](docs/images/ReadMe%20screenshots/admin_dashboard_keuren_details.png)

#### Overige CRUD-acties
Het uitvoeren van overige CRUD-acties zoals het aanpassen/verwijderen van gegevens moet via het 'beheren'-scherm:

![image](docs/images/ReadMe%20screenshots/admin_dashboard_beheren.png)

Door op de 'details'-knop te drukken, wordt een overzicht van alle beschikbare data van de ervaringsdeskundige, het onderzoek of de beheerder getoond. Hier kan je alle data aanpassen, waarna je door op de 'wijzigen opslaan'-knop te drukken de wijzigingen op kan slaan. Je kan ook het 'object' verwijderen door op de 'verwijderen'-knop te drukken.

![image](docs/images/ReadMe%20screenshots/admin_dashboard_beheren_details.png)

### Ervaringsdeskundige
