**Oplossingsrichting:**

Webapplicatie en API

**Eindproduct** (webapplicatie met 3 componenten):

1.  Een component voor **ervaringsdeskundigen** waar zij hun profiel kunnen inzien/aanpassen + aanmelden voor onderzoeken
2.  Een component voor **beheerders**, bevat er 2:
    1.  Schermen voor beheer van ervaringsdeskundigen, organisaties en onderzoeken en een dashboard waarin alle acties zichtbaar zijn.
    2.  Real-time browser pagina moet live worden bijgewerkt, bijvoorbeeld als een organisatie een nieuw onderzoek aanbied (Workshop van Mark in 1e week feb)
3.  API waarin bedrijven onderzoeken kunnen aanmaken en ervaringsdeskundigen kunnen ophalen (meer functies mag, hoeft niet).

**Functionele requirements:**

1.  Applicatie is toegankelijk voor mensen met een beperking, specifiek de pagina’s voor ervaringsdeskundigen. Moet voldoen aan WCAG 2.2 – AA richtlijnen.
2.  Applicatie moet er verzorgd uitzien, bootstrap gebruiken voor professioneel uiterlijk.
3.  Informatiebeveiliging, applicatie moet veilig zijn. De gegevens van de gebruikers moeten zijn afgeschermd voor toegang door onbevoegden. Ervaringsdeskundigen mogen niet elkaars gegevens kunnen inzien door te rommelen met URL’s. LETOP: dit gaat gecontroleerd worden tijdens de beoordeling.

**Portal ervaringsdeskundigen:**

-   Ervaringsdeskundige moet zich kunnen registreren, hieronder de minimale attributen en beperkingenlijst die hierbij nodig zijn:

    ![](media/705bb0b8ca7f7f47eac4370c133dfb37.png)

    **Auditieve beperkingen**

    Doof

    Slechthorend

    Doofblind

    **Visuele beperkingen**

    Blind

    Slechtziend

    Kleurenblind

    Doofblind

    **Motorische / lichamelijke beperkingen**

    Amputatie en mismaaktheid

    Artritus

    Fibromyalgie

    Reuma

    Verminderde handvaardigheid

    Spierdystrofie

    RSI

    Tremor en Spasmen

    Quadriplegie of tetraplegie

    **Cognitieve / neurologische beperkingen**

    ADHD

    Autisme

    Dyslexie

    Dyscalculie

    Leerstoornis

    Geheugen beperking

    Multiple Sclerose

    Epilepsie

    Migraine

-   Profiel moet in geval van voogd of ervaringsdeskundige met toezichthouder ook de contactgegevens van deze persoon bevatten, deze zijn verplicht bij een ervaringsdeskundige onder de 18. JavaScript gebruiken om juiste velden te tonen.
-   Tijdens registratie moet akkoord worden gegevens op algemene voorwaarden, hiervan moet je ook een link met pdf geven.
-   Hierna afwachten goedkeuring door beheerder, tot dan niet mogelijk in te loggen.
-   Na goedkeuring kan ervaringsdeskundige zich aanmelden voor onderzoeken (moet wel telkens goedgekeurd/afgekeurd worden door beheerder).
-   Ook moet het hierna mogelijk zijn profielgegevens toe te voegen en wijzigen (dit kan zonder goedkeuring beheerder).
-   Na authenticatie moet een lijst getoond worden met alle aanvragen van organisaties die qua filters (beperking, leeftijd en beschikbaarheid) van toepassing zijn op de persoon en goedgekeurd door beheerder.
-   Ervaringsdeskundige moet details van aanvraag kunnen inzien en aanmeldoptie hebben via een knop.
-   Ervaringsdeskundige moet verschillende overzichten met onderzoeken kunnen inzien:
    -   Onderzoeken waarop de ervaringsdeskundige is ingeschreven in afwachting van goedkeuring door een beheerder.
    -   Onderzoeken waarvan de inschrijving is afgekeurd door een beheerder.
    -   Onderzoeken waarvan de inschrijving is goedgekeurd door een beheerder

**Portal beheerders:**

-   Beheerders kunnen zich aanmelden op de site, registratie is er niet.
-   Het portal van de beheerder toont op het startscherm de volgende informatie (LETOP: moet live zijn zoals in Mark zijn Workshop w1 feb, hiervoor moet JavaScript en REST backend URL’s gebruikt worden:
    -   Goed te keuren onderzoeksaanvragen
    -   Goed te keuren inschrijvingen door ervaringsdeskundigen op onderzoeken
    -   Goed te keuren nieuw geregistreerde ervaringsdeskundigen
-   Beheerder kan hier goedkeuren/afkeuren, dit moet worden bijgehouden zodat we precies kunnen zien welke beheerder iets heeft goed- of afgekeurd.
-   Reden van afkeuring is niet nodig (gaat buiten systeem om).
-   Er moet CRU(D) functionaliteit zijn om beheerders, onderzoeken en ervaringsdeskundigen te kunnen inzien, wijzigen en verwijderen via webpagina's (Liefst met een zoekveld in eventuele lijsten om snel een specifiek item te kunnen vinden).

**API voor organisaties:**

-   Organisaties maken gebruik van REST API om hun zaken te beheren. Authenticatie met een API-key is vereist!
-   Organisatie mag zijn eigen gegevens wijzigen.
-   Via REST API moet organisatie nieuw onderzoek kunnen aanmaken en beperkt kunnen wijzigen (titel, datum, omschrijving en beloning). Opgeven als gesloten moet ook kunnen.
-   Mogen details van onderzoek opvragen. Via deze details mogen zij de lijst met de profielinhoud van ingeschreven ervaringsdeskundigen te zien waarvan een beheerder de inschrijving heeft goedgekeurd.

**Technische requirements:**

-   WCAG 2.2 – AA
-   3 essentiële JavaScript toepassingen:
    -   Niet tonen van informatie die niet van belang is: Bijvoorbeeld, pas als een ervaringsdeskundige aangeeft een voogd of toezichthouder te hebben of jonger dan 18 jaar te zijn, moeten de velden voor de contactgegevens van de voogd of toezichthouder worden getoond.
    -   Er moet een mogelijkheid komen om dynamisch de voorgrond- (letter) en achtergrondkleur te kunnen kiezen. Dit is een belangrijk onderdeel van de WCAG standaard. Je mag deze voorkeur in een cookie of in de database opslaan.
    -   Invoer in formulieren moet worden gecontroleerd op geldigheid vóór het versturen. Bij problemen moet duidelijk worden aangegeven welk veld niet correct is ingevuld én moet er een foutmelding met uitleg worden getoond.
