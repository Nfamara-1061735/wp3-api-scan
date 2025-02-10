WP3 WCAG samenvatting

# WCAG PP Louella:

Wat is WCAG:

-   Web Content Accessibility Guidelines
-   Web standaarden voor HTML, XML, CSS en WCAG
-   Maakt websites/apps toegankelijker
-   Verplicht voor publieke sector (vanaf juni 2025 ook voor commerciële sector)
-   **Wij gebruiken versie 2.2 AA (internationale standaard)**

WCAG:

-   Principes:
    -   Waarneembaar:
        -   Mensen kunnen inhoud zien/horen (ook met beperking)
        -   Methodes:
            -   Afbeeldingen hebben passende ALT tekst:
                -   Kort maar krachtig
                -   Vermijd herhaling
            -   Ondertitels bij filmpjes
            -   Genoeg contrast:
                -   WebAIM contrast checker
            -   Content kan worden vergroot (minimaal 200%)
    -   Bedienbaar:
        -   Bediening mogelijk met toetsenbord/andere hulpmiddelen (NIET alleen met muis)
        -   Methodes:
            -   Alles is te bereiken/bedienen met toetsenbord
            -   Geef passende titels/linkteksten
            -   Geef onderdelen waar het gebruik van een muis vereist is een alternatief
    -   Begrijpelijk:
        -   De informatie/bediening is begrijpelijk voor mensen/software
        -   Methodes:
            -   Taal van website is vastgelegd
            -   Goede opbouw (H1 t/m H6 tags, [semantics](https://www.w3schools.com/html/html5_semantic_elements.asp) etc.)
            -   Zichtbare labels/instructies bij formuliervelden
    -   Robuust:
        -   We website moet goed werken met verschillende browsers/apparaten/hulpmiddelen etc.
        -   Methodes:
            -   Alle UI-elementen hebben een duidelijke rol/naam/waarde:
                -   Naam: gebruik juiste HTML tag
                -   Rol: definieer de juiste ‘role’ in HTML
                -   Waarde: [ARIA](https://www.w3.org/TR/wai-aria-1.0/states_and_properties) word gebruik wanneer semantische HTML niet genoeg is
            -   Foutmeldingen/statusberichten kunnen door hulpmiddelen worden gepresenteerd

Testen van applicatie:

-   AXE DevTools
-   WAVE
-   Google Lighthouse

# Aantekeningen van Jorik:

Methodes om mensen met een beperking te helpen:

-   Blinden, slechtzienden en kleurenblinden:
    -   Ondersteuning voor voorleessoftware
    -   Goede structuur van content
    -   Vergroten van tekst
    -   Kleurcontrasten
    -   Audiodescriptie
-   Doven en slechthorenden:
    -   Ondertiteling bij video
    -   Begrijpelijke teksten
-   Motorische beperking:
    -   Toetsenbordtoegankelijkheid
-   Cognitieve beperking:
    -   Rustige lay-out
    -   Duidelijkheid
    -   Heldere navigatie

Extra tips:

-   HTML structuur is belangrijk (voor screenreader)
-   Voeg ALT tekst toe bij afbeeldingen
-   Tabellen zijn voor data, NIET voor lay-out

# W3 richtlijnen:

## Richtlijn 1: waarneembaar

-   Tekstalternatieven:
    -   Niet tekstuele onderdelen moeten een tekstueel alternatief/beschrijving bieden
    -   Bij decoratie/opmaak hoeft geen tekstueel alternatief te hebben
-   Aanpasbaar:
    -   Content moet op verschillende manieren worden gepresenteerd (bijv. met een eenvoudigere lay-out) zonder dat er informatie verloren gaat:
        -   Weergave is dus NIET beperkt tot maar één stand
        -   Het doel van elk invoerveld dat informatie verzamelt moet programmatisch worden bepaald
-   Onderscheidend:
    -   Maak het voor gebruikers makkelijker om content te zien of te horen door bijv. de voorgrond te scheiden van de achtergrond
    -   Kleur word NIET als enige visuele middel gebruikt om informatie over te dragen etc.
    -   Bij audio langer dan 3 seconden moeten de volgende functies beschikbaar zijn:
        -   Pauzeknop
        -   Volumeregelaar
    -   Visuele presentatie heeft minimaal een contrastverhouding van 4;5;1 behalve bij:
        -   Grote tekst:
            -   Minimaal 3;1;
        -   Toevallig (puur decoratief):
            -   Geen contrastvereiste
        -   Logo’s:
            -   Geen contrastvereiste
    -   De grootte van tekst kan tot 200% worden aangepast (zonder verlies van inhoud/functionaliteit)
    -   Inhoud kan worden gepresenteerd zonder verlies van informatie/functionaliteit en zonder dat er in twee dimensies hoeft te worden gescrolld:
        -   Verticaal:
            -   Breedte gelijk aan 320 CSS-pixels
        -   Horizontaal:
            -   Hoogte gelijk aan 256 CSS-pixels
    -   Niet-tekstueel contrast:
        -   UI:
            -   Minimaal 3;1
        -   Grafische objecten:
            -   Minimaal 3;1
    -   Tekstafstand:
        -   Regelhoogte: minimaal 1,5x lettergrootte
        -   Spatiëring na alinea’s: minimaal 2x lettergrootte
        -   Letterafstand: minimaal 0,12x lettergrootte
        -   Woordafstand: minimaal 0,16x lettergrootte
    -   Inhoud bij zweven/focus (met een muis hoveren): Er moet een alternatief mechanisme beschikbaar zijn om de informatie langer/definitief te laten zien

## Richtlijn 2: bedienbaar

Componenten van de UI/navigatie moeten bedienbaar zijn

-   Toetsenbord toegankelijk:
    -   Alle functionaliteiten kunnen worden bediend met een toetsenbordinterface
    -   ?
    -   Er moet een mechanisme zijn om sneltoetsen uit te schakelen, opnieuw te mappen of alleen actief te maken bij focus
-   Genoeg tijd:
    -   Gebruiker hebben voldoende tijd om inhoud te lezen/te gebruiken
    -   Tijdslimieten kunnen worden:
        -   Uitgeschakeld
        -   Aangepast
        -   Verlengd
        -   Uitzonderingen:
            -   Real-time event
            -   Essentieel tijdslimiet
            -   Limiet langer dan 20 uur
    -   Bewegende/geüpdatete onderdelen moeten kunnen worden gepauzeerd of worden gestopt
-   Ontwerp geen content waarvan bekend is dat deze aanvallen of fysieke reacties veroorzaakt:
    -   Geen elementen die vaker dan 3x per seconde knipperen of flits die lager is dan algemene flits/roodflitsdrempels
-   Bied manieren om gebruikers te helpen navigeren, inhoud te vinden en te bepalen waar ze zijn:
    -   Er is een mechanisme waarmee inhoud (die op meerdere pagina’s word herhaald) te omzeilen
    -   Pagina’s hebben een titel die het onderwerp/doel omschrijft
    -   Als er sequentieel kan worden genavigeerd krijgen componenten een focus in de volgorde waarmee de werking behouden blijft
    -   Het doel van elke link word bepaald a.d.h.v. de programmatisch bepaalde linktekst
    -   Er zijn meerdere manieren om een pagina binnen een set pagina’s te vinden
    -   Koppen/labels beschrijven het onderwerp/doel
    -   Elk UI onderdeel die met een toetsenbord kan worden bediend heeft een bedieningsmodus waarmee de indicator zichtbaar is
    -   Wanneer een component van de UI de focus krijgt, word het NIET volledig verborgen
-   Invoermodaliteiten:
    -   Maak het voor gebruiker eenvoudiger om functies te bedienen via verschillende invoermethoden (naast alleen het toetsenbord)
    -   Er moet een alternatief voor multipoint/pad-gebaseerde gebaren zijn
    -   Bij UI componenten met labels bevat de naam de tekst die visueel wordt weergegeven
    -   Functionaliteit die kan worden bediend door beweging van het apparaat/gebruiker kan ook worden bediend door componenten van de UI
    -   Voor functionaliteiten met een sleepbeweging is een alternatief

## Richtlijn 3: begrijpelijk

Informatie en bediening van de UI moet begrijpelijk zijn

-   Maak tekstinhoud leesbaar/begrijpelijk:
    -   De standaard menselijke taal kan van elke pagina programmatisch worden bepaald
-   Zorg dat pagina’s er voorspelbaar uitzien/werken:
    -   Wanneer een component focus krijgt, word er GEEN contextwijziging in gang gezet
    -   Als de instellingen van de UI veranderen, leidt dit NIET automatisch tot een contextwijziging
    -   Navigatiemechanismen die op meerdere schermen worden herhaald, staan op elke pagina in dezelfde volgorde
    -   Componenten met dezelfde functionaliteit binnen een set pagina’s worden consistent geïdentificeerd
-   Help gebruikers fouten te voorkomen/te corrigeren:
    -   Als er automatisch een invoerfout word gedetecteerd, word de fout geïdentificeerd en uitgelegd en worden er suggesties gedaan voor correcties
    -   Wanneer er input van de gebruiker word verwacht, worden labels/instructies getoond
    -   Bij het invoeren van financiële/juridische informatie moeten er de volgende opties zijn om fouten te voorkomen:
        -   Omkeerbaar: inzendingen zijn omkeerbaar
        -   Gecontroleerd: invoer word op fouten gecontroleerd en er is een optie om te corrigeren
        -   Bevestigd: er is een mechanisme waarmee de gebruiker informatie kan controleren, bevestigen en corrigeren
    -   Informatie die eerder al is ingevoerd word:
        -   Automatisch ingevuld of
        -   Beschikbaar voor de gebruiker om te selecteren
    -   Toegankelijke authenticatie (zie bron)

## Richtlijn 4: robuust

De inhoud moet robuust genoeg zijn om geïnterpreteerd te kunnen worden door een groot aantal gebruikersagenten, waaronder ondersteunende technologieën

-   Maximaliseer compatibiliteit met huidige/toekomstige gebruikersagenten
-   Voor alle componenten van de UI kunnen:
    -   de naam/rol programmatisch worden bepaald
    -   statussen, eigenschappen en waarden door de gebruiker worden ingesteld

# Bronnen:
- PowerPoint WP3 week 3.2
- Aantekeningen Jorik van presentatie vertegenwoordiger stichting accessibility week 3.1
- WCAG richtlijnen (https://www.w3.org/TR/WCAG22/)