![alt text](https://raw.githubusercontent.com/ludvig03/Faktisk-Tiktok-scraper/main/static/TikTok_Scraper.png)

# Tiktok-scraper

Programvare for nedlastning av TikTok-data

## Du trenger for å kjøre:

    Dette verktøyet krever noen forkunnskaper om programmering. For å kjøre scraperen, må du installere følgende fra terminalen:

    1. [python3](https://www.python.org/downloads/)
    2. pip3 (Skal komme med python)
    3. [git](https://git-scm.com/downloads)


## Installasjon

Kjør denne her for å installere alle dependencies når du har lastet ned repoet:

```bash
pip3 install flask requests flask_cors selenium pandas flatten_json 
```

## Bruk
Dette programmet laster ned alle videoer med metadata og toppkommentarer til en eller flere TikTok-brukere.

For å kunne bruke programmet, må du kjøre python-skriptet kalt app.py. Dette skriptet spinner opp en lokal server der du får tilgang til programmets UI ved gå til port 5000 på localhost (127.0.0.1:5000).

I utgangspunktet henter programmet lenker til alle videoene en eller flere kontoer har lagt ut. Hvis du ønsker videofiler samt .csv-filer med videolenker, kommentardata og metadata, må du oppgi en API-nøkkel for API-et TikTok-Video-No-Watermark2, som du må kjøpe tilgang til selv på: https://rapidapi.com/yi005/api/tiktok-video-no-watermark2. 

Du kan spesifisere en eller flere brukere du vil hente data fra. Disse må oppgis som en liste med unike brukernavn (@brukernavn). Brukernavnene må være adskilt med komma eller semikolon. 

## Resultat

Når scrapingen av en eller flere TikTok-kontoer er ferdig vil du sitte igjen med en mappe i directoriet ditt som heter brukere. Her finner du en egen mappe for hver bruker du har scrapet.

Hver bruker har også to mapper, en med alle videofilene, og en med to .csv-filer. videos.csv inneholder et datasett med alle videoene til den brukeren, mens comments.csv inneholder et dataset med alle kommentarene som er hentet for den brukeren. 

Hver kommentar har sitt eget felt som identifiserer hvilken video kommentaren hører. Viktig: API-et vi bruker har bare "top layer comments". Det betyr at svarene på kommentarer ikke er med i datasettet.

## Feilsøking

Det hender at serveren returnerer 403 forbidden grunnet socket poolsene. Om det er tilfelle må du bare gå inn på denne addressen her: chrome://net-internals/#sockets og klikke på Flush socket pools. Dette skal løse problemet. 

Om serveren ikke er tilgjengelig på 127.0.0.1:5000, vil det stå printet i terminalen hvor serveren befinner seg. 