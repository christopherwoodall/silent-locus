#!/usr/bin/env python3
"""
CRYPTOGRAPHER — EUROSWARM worker. Read-only local analysis.
Task 1: decode base64 blobs in corpora, language-detect DE/FR/EN.
Task 2: hex-decode "random" hex strings, test epoch nonces + tag tokens vs DE/FR wordlists.
Task 3: tag-grammar char/token distribution for non-English markers (incl. stripped-diacritic signal).
Task 4: webhook inbox bodies + beacon payloads language detection.

Output: JSON results under workers/cryptographer/out/*.json consumed by FINDINGS.md.
No network. No credential use. Agent/swarm scope only.
"""
import json, os, re, base64, binascii, hashlib
from collections import Counter, defaultdict

BASE = os.path.expanduser("~/workspace/silent-locus/data")
CORP = os.path.join(BASE, "2026-09-28-chinese-amap-fleet")
OUT = os.path.join(CORP, "german-french-swarm-hunt/workers/cryptographer/out")
os.makedirs(OUT, exist_ok=True)

EVENTS_FILES = [
    os.path.join(CORP, "events.jsonl"),
    os.path.join(BASE, "2026-10-01-oai-tag-sweep/events.jsonl"),
    os.path.join(BASE, "2026-05-12-webhook-deaddrops/events.jsonl"),
    os.path.join(BASE, "2025-12-04-urlquery-marker-sweep/events.jsonl"),
]
RAW_DIRS = [
    os.path.join(CORP, "raw"),
    os.path.join(BASE, "2025-12-04-urlquery-marker-sweep/raw"),
]

# ---------------------------------------------------------------- stopwords
DE_STOP = """der die das und in von zu mit den des auf für ist im dem nicht ein eine als auch es an werden aus er hat daß sie nach wird bei einer um am sind noch wie einem über einen man durch so zum können gegen vom ihr ihre ihrem ihren ihrer ihn ihnen ihn es uns euch wir unser unsere unseren unserem unserer uns euch ihnen ihnen denen dieser diese dieses diesen diesem diesem jedem jeder jedes jeden jede jenem jener jenes jenen jene alle aller allem allen alles andere anderen anderem anderen anderem anderem kein keine keinen keiner keinem keines mehr sehr schon nur auch nur noch wieder immer dann dort hier jetzt heute gestern morgen wo wohin woher warum weil wenn ob obschon obwohl denn sowie sondern aber oder bzw bis seit während vor hinter neben zwischen ohne statt anstatt trotz wegen statt zum zur vom beim vom auf beim im am ins ans aufs durch für gegen ohne um wieder gegen sein habe haben hatte hatten wurde wurden wird werde werden würden wäre wären sei seien bin bist ist sind war waren gewesen habe hast hat haben hatte hatten gehabt werde wird werden würde würden wurde wurden werden sein seine seiner seinem seinen seiner seine sein mein meine meiner meinem meinen meiner meine dein deine deiner deinem deinen deiner deine kein keine keiner keinem keinen keiner keine dies diese dieser diesem diesen diese jenes jene jener jenem jenen jene solch solche solcher solchem solchen solche welche welcher welchem welchen welche was wer wen wem wessen wo wohin woher wann wieviel wieviele selbst sich mich dich ihn es uns euch sie ihnen ihnen nein ja nicht kein nichts niemand niemandem niemanden niemands etwas alles alle jeder jedem jeden jede jedes allem allen alles anderem anderen anderem andere anderen viel viele vielem vielen viele wenig wenige wenigem wenigen wenige mehr weniger meist meisten sehr zu allzu ganz gar eben halt mal doch denn ja wohl etwa ungefähr circa bzw d.h z.B usw etc und oder aber denn sondern sowohl als auch entweder weder noch nicht nur sondern auch sowohl weder""".split()

FR_STOP = """le la les un une des du de d' l' et est en que qui dans ne pas se ce cette ces sur au aux il elle ils elles nous vous leur leurs on y a été être avoir fait faire dire peut plus comme par pour avec tout toute tous toutes autre autres entre sans sous vers chez pendant contre depuis jusqu jusque donc car ni ou où dont quand lorsque comme ainsi alors donc aussi bien très peu beaucoup trop assez moins autant aussi également même mêmes tel telle tels telles quel quelle quels quelles ceci cela ça celui celle ceux celles celui-ci celui-là mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs mien mienne miens miennes tien tienne tiens tiennes sien sienne siens siennes nôtre nôtres vôtre vôtres leur leurs ne pas plus jamais rien personne aucun aucune nul nulle jamais toujours souvent parfois déjà encore très trop peu assez beaucoup moins plus mieux pis meilleur meilleure meilleurs meilleures grand grande grands grandes petit petite petits petites nouveau nouvelle nouveaux nouvelles premier première premiers premières dernier dernière derniers dernières long longue longs longues haut haute hauts hautes bas basse basses jeune jeunes vieux vieille vieux vieilles bon bonne bons bonnes mauvais mauvaise mauvais mauvaises beau belle beaux belles joli jolie jolis jolies""".split()

EN_STOP = """the of and to in is that it was for on are as with his they be at one have this from or had by hot word but what some we can out other were which do their time if will how said an each tell does set three want air well also play small end put home read hand port large spell add even land here must big high such follow act why ask men change went light kind off need house picture try again animal point mother world near build self earth father any new work part take get place made live where after back little only round man year came show every good me give our under name very through just form sentence great think say help low line differ turn cause much mean before move right boy old too same she all there when up use your how said an each she which do their time will way about many then them would write like so these her long make thing see him two has look more day could go come did number sound no most people my over know water than call first who may down side been now find any new take get place made where after back little only round man year came show every good give our under while number no way could people than first water been call who oil sit now find long down day did get come made may part over such because turn here why ask went men read need land different home move try kind hand picture again change play spell air away old each tell does set three want well also small end put read port large""".split()

def lang_score(text):
    """Returns (verdict, detail dict). Simple stopword-density scoring."""
    words = re.findall(r"[a-zàâäçèéêëîïôöùûüÿßæœ']+", text.lower())
    if not words:
        return ("empty", {})
    n = len(words)
    hits = {}
    for lang, sw in (("de", DE_STOP), ("fr", FR_STOP), ("en", EN_STOP)):
        c = sum(1 for w in words if w in set(sw))
        hits[lang] = c
    best = max(hits, key=lambda k: hits[k])
    second = sorted(hits.values())[-2]
    dens = hits[best] / n
    # require >=3 stopword hits and density edge to call it
    if hits[best] >= 3 and hits[best] >= 2 * max(second, 1) and dens >= 0.02:
        verdict = best
    elif hits[best] >= 3:
        verdict = "mixed/" + best
    else:
        verdict = "undetermined"
    return (verdict, {"hits": hits, "n_words": n, "density": round(dens, 4)})

# ---------------------------------------------------------------- wordlists
# Common words (len>=4) + task/agent vocab. All lowercase.
DE_WORDS = set("""haben wurde wurden werden würde wäre wären zwischen
arbeiten arbeit arbeiter aufgabe aufgaben beauftragt sammeln sammle sammlung
daten datensatz karte karten ort orte standort adresse adressen
suchbegriff suche suchen suchanfrage forschung forschen analyse analysieren
bericht berichte nachricht nachrichten meldung ergebnis ergebnisse
agent agenten bot bots programm programme skript aufzeichnung
webseite seiten inhalte inhalt text texte bild bilder datei dateien
herunterladen laden abrufen zugriff zugreifen anfrage anfragen antwort
server dienst dienste schnittstelle benutzer konto konten anmeldung
passwort schlüssel token sitzung ablauf zeitstempel protokoll
verzeichnis liste listen tabelle tabellen zeile spalte spalten
netzwerk verbindung anfrage fehler fehlerhaft erfolg erfolgreich
starten starten stoppen anhalten fortsetzen wiederholen versuch
nummer zahlen wert werte name namen titel beschreibung
stadt städte land länder region bezirk straße platz
preis preise angebot angebote produkt produkte laden geschäft
wetter klima temperatur prognose verkehr fahrt route routen
fahrplan abfahrt ankunft bahnhof flughafen hotel restaurant
telefon nummer email adresse öffnen schließen klicken klick
formular eingabe ausgabe eingabefeld schaltfläche link links
seite seiten kopf fuß menü navigation suche filter sortieren
deutsch deutschland berlin münchen hamburg köln frankfurt stuttgart
düsseldorf leipzig dresden hannover nürnberg bremen essen dortmund
frankreich paris lyon marseille österreich wien schweiz zürich
januar februar märz april mai juni juli august september oktober november dezember
montag dienstag mittwoch donnerstag freitag samstag sonntag
heute gestern morgen woche monat jahr stunde minute sekunde
sprachmodell modell modelle anweisung anweisungen eingabeaufforderung
zusammenfassen extrahieren vergleichen prüfen validieren
sicher speichern laden speichern dateiname pfad ordner
automatisierung workflow pipeline aufgabenliste checkliste
geheim verschlüsselt entschlüsseln kodiert dekodiert base
proxy relay tunnel vpn tor knoten punkt endpunkt
scannen scan crawlen crawler spinne ernte ernten
überwachen beobachtung alarm warnung benachrichtigung
katalog index indizieren abfrage abfragen datenbank
browser fenster registerkarte iframe skript laufzeit
ausführen ausführung befehl befehle terminal konsole
schadcode angriff verwundbarkeit ausnutzen payload nutzlast
ziel ziele kampagne operation mission einsatz test tests
beacon leuchtfeuer rufzeichen ruf signal signale puls
herzschlag takt intervall warte verzögerung schlafen
verschleierung tarnung versteckt heimlich leise lautlos
umgehung tarnkappe wechsel rotation wechselnd zufällig
prüfen validierung verifizierung authentifizierung
""".replace("ä","a").replace("ö","o").replace("ü","u").replace("ß","ss").split())
# also add the umlaut-bearing forms for folded matching
DE_WORDS |= set("""für über straße städte münchen köln düsseldorf nürnberg
größe grüße süd nörd österreich zürich täter""".split())

FR_WORDS = set("""avoir être faire dire pouvoir vouloir devoir savoir
tâche taches mission missions travail travaux
collecter collecte collecteuse collecteur données base carte cartes
lieu lieux adresse adresses emplacement recherche rechercher
requête analyse analyser rapport rapports message messages
résultat résultats agent agents robot robots programme programmes
script page pages site sites contenu texte image images fichier
télécharger charger récupérer accès demande demandes réponse
serveur service services utilisateur compte comptes connexion
motdepasse clé jeton session horodatage journal répertoire
liste listes tableau tableaux ligne colonne colonnes réseau
erreur échec succès démarrer arrêter continuer répéter essai
numéro valeur valeurs nom noms titre description ville villes
pays région rue place prix offre offres produit produits
météo climat température prévision trafic trajet itinéraire
horaire départ arrivée gare aéroport hôtel restaurant
téléphone courriel ouvrir fermer cliquer formulaire saisie
sortie bouton lien liens en-tête pied menu navigation filtre
trier allemagne france paris lyon marseille berlin
janvier février mars avril juin juillet août septembre octobre novembre décembre
lundi mardi mercredi jeudi vendredi samedi dimanche
aujourd'hui hier demain semaine mois année heure minute seconde
modèle modèles instruction instructions résumé résumer extraire
comparer vérifier valider enregistrer charger nomfichier dossier
automatisation flux pipeline secrète chiffré décoder encodé
proxy relais tunnel noeud point extrémité balayer analyse
crawler moisson moissonner surveiller observation alerte avertissement
notification catalogue index indexer base données navigateur
fenêtre onglet exécuter exécution commande commandes terminal
console charge utile cible cibles campagne opération essai tests
balise battement coeur intervalle attendre délai dormir
dissimulation caché furtif silencieux contournement rotation aléatoire
vérification authentification français française langue langues
parler écrit écrire lire lecture traduire traduction mot mots
phrase phrases document documents source sources cible cibles
""".replace("é","e").replace("è","e").replace("ê","e").replace("à","a").replace("ç","c").replace("ù","u").replace("î","i").replace("ï","i").replace("ô","o").replace("û","u").split())
FR_WORDS |= set("""tâche données été être où ça""".split())

# ASCII-folded German/French task words (stripped-diacritic markers)
FOLDED_DE = """fuer ueber aendern strasse muenchen koeln zuerich duesseldorf nuernberg
grosse gruesse sued nord taeter oesterreich aufgaben sammeln daten
karte standort suche forschung analyse bericht nachricht ergebnis
beacon nutzlast tarnung verschleierung abrufen zugriff anfrage""".split()
FOLDED_FR = """tache donnees etre cafe eleve francais francaise recherche collecte
adresse donnees resultat rapport message analyse""".split()

B64_RE = re.compile(r"[A-Za-z0-9+/=_-]{100,}")
B64_URLISH = re.compile(r"(?:[A-Za-z0-9_-]{60,}={0,2})")

def try_b64(s):
    s = s.strip().strip('"').strip("'")
    # strip URL-safe to standard for decode attempt
    for variant in (s, s.replace("-", "+").replace("_", "/")):
        pad = "=" * (-len(variant) % 4)
        try:
            raw = base64.b64decode(variant + pad, validate=False)
        except (binascii.Error, ValueError):
            continue
        if len(raw) < 30:
            continue
        # STRICT: valid UTF-8 only (latin-1 fallback fabricates words from binary)
        try:
            txt = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        print_ratio = sum(1 for c in txt if c.isprintable() or c in "\n\r\t") / max(len(txt), 1)
        if print_ratio > 0.90:
            return txt
    return None

def iter_event_strings():
    """Yield (corpus_name, event_idx, field_path, string_value) for all string fields."""
    for ef in EVENTS_FILES:
        cname = os.path.basename(os.path.dirname(ef))
        try:
            f = open(ef, encoding="utf-8", errors="replace")
        except FileNotFoundError:
            continue
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            stack = [("", d)]
            while stack:
                path, v = stack.pop()
                if isinstance(v, str):
                    yield (cname, i, path, v)
                elif isinstance(v, dict):
                    for k, vv in v.items():
                        stack.append((path + "/" + str(k), vv))
                elif isinstance(v, list):
                    for j, vv in enumerate(v):
                        stack.append((f"{path}[{j}]", vv))
        f.close()

def iter_raw_files():
    for rd in RAW_DIRS:
        if not os.path.isdir(rd):
            continue
        for root, _ds, files in os.walk(rd):
            for fn in files:
                if fn.endswith((".json", ".jsonl", ".txt", ".html")):
                    yield os.path.join(root, fn)
