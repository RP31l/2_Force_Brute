import streamlit as st
from random import seed, randint

st.set_page_config(page_title="Force Brute", page_icon="🔍", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Oxanium:wght@400;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Oxanium', sans-serif; background-color: #0a0a0f; color: #ffffff; }
.stApp { background: radial-gradient(ellipse at top, #0d1b2a 0%, #0a0a0f 70%); min-height: 100vh; }
h1 {
    font-family: 'Oxanium', sans-serif; font-weight: 800; font-size: 2.4rem; text-align: center;
    background: linear-gradient(90deg, #ff4444, #ff8800, #ff4444); background-size: 200%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
}
@keyframes shine { 0% { background-position: 0% } 100% { background-position: 200% } }
label { color: #ffffff !important; font-size: 0.85rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }
.stTextInput > div > div > input {
    background: #0d1b2a !important; border: 1px solid #ffffff !important;
    border-radius: 6px !important; color: #ffffff !important;
    font-family: 'Share Tech Mono', monospace !important;
}
.stButton > button {
    width: 100%; background: linear-gradient(135deg, #3a0a0a, #5a1a00);
    border: 1px solid #ff4444; color: #ff4444; font-family: 'Oxanium', sans-serif;
    font-weight: 700; font-size: 1rem; letter-spacing: 0.15em;
    padding: 0.75rem; border-radius: 6px; margin-top: 0.5rem;
}
.result-found {
    background: linear-gradient(135deg, #0a2a0a, #0d3b0d); border: 2px solid #00ff88;
    border-radius: 8px; padding: 1rem 1.5rem; font-family: 'Share Tech Mono', monospace;
    font-size: 1.1rem; color: #00ff88; margin-bottom: 0.5rem; letter-spacing: 0.1em;
}
.result-normal {
    background: #0d1b2a; border: 1px solid #1e3a5f; border-radius: 6px;
    padding: 0.6rem 1rem; font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem; color: #8a9ab0; margin-bottom: 0.3rem;
}
.score-badge {
    display: inline-block; background: #00ff8833; border: 1px solid #00ff88;
    border-radius: 4px; padding: 0.1rem 0.5rem; font-size: 0.75rem;
    color: #00ff88; margin-left: 0.5rem;
}
.bloc-info {
    background: #0d1b2a; border: 1px solid #00d4ff33; border-left: 4px solid #00d4ff;
    border-radius: 6px; padding: 0.8rem 1.2rem; font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem; color: #00d4ff; margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTES ────────────────────────────────────────────────────────────────
alp = "abcdefghijklmnopqrstuvwxyz "
ALP_IDX = {c: i for i, c in enumerate(alp)}
N_ALP = 27
TAILLE_BLOC = 500000
FREQ_FR = set("easitnrul")
VOYELLES = set("aeiouy")
MIN_VOYELLES = 0.20
MAX_VOYELLES = 0.65

mots_fr = set([
    # Articles et determinants
    "le","la","les","de","du","des","un","une","au","aux","l","d",
    # Pronoms
    "je","tu","il","elle","nous","vous","ils","elles","me","te","se","y","en",
    "moi","toi","lui","eux","leur","on","ce","cet","cette","ces","celui","celle",
    "ceux","celles","cela","ca","ceci","rien","tout","tous","toute","toutes",
    "quelque","quelques","chaque","autre","autres","meme","memes","tel","telle",
    # Verbes etre et avoir conjugues
    "suis","es","sommes","etes","sont","etais","etait","etions","etiez","etaient",
    "ai","as","avons","avez","ont","avais","avait","avions","aviez","avaient",
    "sera","serai","seras","serons","serez","seront","serais","serait","serions","seriez","seraient",
    "aura","aurai","auras","aurons","aurez","auront","aurais","aurait","aurions","auriez","auraient",
    "ete","eu","etant","ayant",
    # Verbes courants conjugues
    "fait","fais","faisons","faites","font","faisais","faisait","fera","ferai","feras","ferons","ferez","feront",
    "dit","dis","disons","dites","disent","disais","disait",
    "va","vais","allons","allez","vont","allais","allait","irai","iras","ira","irons","irez","iront",
    "vois","voit","voyons","voyez","voient","voyais","voyait","verra","verrai",
    "sais","sait","savons","savez","savent","savais","savait",
    "peux","peut","pouvons","pouvez","peuvent","pouvais","pouvait","pourra","pourrai",
    "veux","veut","voulons","voulez","veulent","voulais","voulait","voudra","voudrai",
    "viens","vient","venons","venez","viennent","venais","venait","viendra","viendrai",
    "prends","prend","prenons","prenez","prennent","prenais","prenait",
    "dois","doit","devons","devez","doivent","devais","devait","devra","devrai",
    "mets","met","mettons","mettez","mettent","mettais","mettait",
    "tiens","tient","tenons","tenez","tiennent","tenais","tenait",
    "reviens","revient","revenons","revenez","reviennent",
    "viens","vient","venons","venez","viennent",
    "mange","manges","mangeons","mangez","mangent","mangeais","mangeait",
    "bois","boit","buvons","buvez","boivent","buvais","buvait",
    "dors","dort","dormons","dormez","dorment","dormais","dormait",
    "parle","parles","parlons","parlez","parlent","parlais","parlait",
    "joue","joues","jouons","jouez","jouent","jouais","jouait",
    "aime","aimes","aimons","aimez","aiment","aimais","aimait",
    "pense","penses","pensons","pensez","pensent","pensais","pensait",
    "reste","restes","restons","restez","restent","restais","restait",
    "arrive","arrives","arrivons","arrivez","arrivent","arrivais","arrivait",
    "attends","attend","attendons","attendez","attendent","attendais","attendait",
    "connais","connait","connaissons","connaissez","connaissent",
    "crois","croit","croyons","croyez","croient","croyais","croyait",
    "donne","donnes","donnons","donnez","donnent","donnais","donnait",
    "habite","habites","habitons","habitez","habitent",
    "marche","marches","marchons","marchez","marchent",
    "monte","montes","montons","montez","montent",
    "ouvre","ouvres","ouvrons","ouvrez","ouvrent",
    "regarde","regardes","regardons","regardez","regardent",
    "rentre","rentres","rentrons","rentrez","rentrent",
    "sors","sort","sortons","sortez","sortent","sortais","sortait",
    "tombe","tombes","tombons","tombez","tombent",
    "travaille","travailles","travaillons","travaillez","travaillent",
    "trouve","trouves","trouvons","trouvez","trouvent",
    "viens","vient","venons","venez","viennent",
    "vis","vit","vivons","vivez","vivent","vivais","vivait",
    "appelle","appelles","appelons","appelez","appellent",
    "commence","commences","commencons","commencez","commencent",
    "comprends","comprend","comprenons","comprenez","comprennent",
    "couche","couches","couchons","couchez","couchent",
    "demande","demandes","demandons","demandez","demandent",
    "depasse","depasses","depassons","depassez","depassent",
    "ecris","ecrit","ecrivons","ecrivez","ecrivent",
    "envoie","envoies","envoyons","envoyez","envoient",
    "leve","leves","levons","levez","levent",
    "lis","lit","lisons","lisez","lisent",
    "passes","passons","passez","passent",
    "perds","perd","perdons","perdez","perdent",
    "pleure","pleures","pleurons","pleurez","pleurent",
    "poses","posons","posez","posent",
    "rappelle","rappelles","rappelons","rappelez","rappellent",
    "reponds","repond","repondons","repondez","repondent",
    "ris","rit","rions","riez","rient",
    "sens","sent","sentons","sentez","sentent",
    "sors","sort","sortons","sortez","sortent",
    "touches","touchons","touchez","touchent",
    "utilises","utilisons","utilisez","utilisent",
    "vois","voit","voyons","voyez","voient",
    # Prepositions et conjonctions
    "et","ou","mais","donc","or","ni","car","que","qui","quoi","dont","quand",
    "comme","si","parce","puisque","bien","mal","sans","sous","sur","dans",
    "par","entre","vers","chez","avec","pour","contre","avant","apres","depuis",
    "pendant","selon","malgre","sauf","lors","jusque","jusqu","afin","ainsi",
    "alors","aussi","autant","cependant","certes","deja","encore","enfin",
    "ensuite","environ","peu","pres","surtout","toujours","jamais","souvent",
    "parfois","rarement","vite","loin","près","ici","la","voici","voila",
    "quand","comment","pourquoi","combien","quel","quelle","quels","quelles",
    "non","oui","si","peut","etre","peut-etre","peut etre",
    # Negations
    "ne","pas","plus","point","guere","nullement","aucun","aucune","personne",
    # Adjectifs courants
    "grand","grande","grands","grandes","petit","petite","petits","petites",
    "gros","grosse","gros","grosses","mince","minces",
    "beau","belle","beaux","belles","joli","jolie","jolis","jolies",
    "laid","laide","laids","laides","fort","forte","forts","fortes",
    "faible","faibles","rapide","rapides","lent","lente","lents","lentes",
    "chaud","chaude","chauds","chaudes","froid","froide","froids","froides",
    "bon","bonne","bons","bonnes","mauvais","mauvaise","mauvaises",
    "vieux","vieille","vieux","vieilles","jeune","jeunes",
    "nouveau","nouvelle","nouveaux","nouvelles","ancien","ancienne","anciens","anciennes",
    "premier","premiere","premiers","premieres","dernier","derniere","derniers","dernieres",
    "prochain","prochaine","prochains","prochaines","seul","seule","seuls","seules",
    "meme","memes","autre","autres","certain","certaine","certains","certaines",
    "plusieurs","nombreux","nombreuse","nombreuses","divers","diverse","diverses",
    "different","differente","differents","differentes","pareil","pareille",
    "heureux","heureuse","heureux","heureuses","triste","tristes",
    "content","contente","contents","contentes","fache","fachee","faches","fachees",
    "fatigue","fatiguee","fatigues","fatiguees","malade","malades",
    "libre","libres","occupe","occupee","occupes","occupees",
    "possible","impossible","necessaire","important","importante",
    "difficile","difficiles","facile","faciles","utile","utiles",
    "vrai","vraie","vrais","vraies","faux","fausse","fausses",
    "long","longue","longs","longues","court","courte","courts","courtes",
    "haut","haute","hauts","hautes","bas","basse","basses",
    "plein","pleine","pleins","pleines","vide","vides",
    "ouvert","ouverte","ouverts","ouvertes","ferme","fermee","fermes","fermees",
    "chic","cool","super","sympa","nul","nulle","nuls","nulles",
    "bizarre","bizarres","chelou","chelous","marrant","marrante","marrants","marrantes",
    "gentil","gentille","gentils","gentilles","mechant","mechante","mechants","mechantes",
    "timide","timides","drole","droles","serieux","serieuse","serieuses",
    # Noms personnes et famille
    "homme","femme","enfant","garcon","fille","bebe","adulte","personne","gens",
    "maman","papa","mere","pere","frere","soeur","grand","mere","grand","pere",
    "grandmere","grandpere","oncle","tante","cousin","cousine","neveu","niece",
    "mari","femme","epoux","epouse","copain","copine","ami","amie","camarade",
    "collegue","voisin","voisine","patron","chef","eleve","etudiant","professeur",
    "medecin","docteur","infirmier","infirmiere","policier","pompier","soldat",
    "roi","reine","prince","princesse","president","ministre",
    "frere","frero","frerot","frer","freere","soeurette","mec","gars","meuf","bro",
    # Corps humain
    "tete","visage","front","yeux","oeil","nez","bouche","dent","dents","langue",
    "oreille","oreilles","joue","joues","menton","cou","epaule","epaules",
    "bras","coude","poignet","main","mains","doigt","doigts","pouce",
    "poitrine","dos","ventre","nombril","hanche","fesse","fesses",
    "jambe","jambes","genou","genoux","cheville","pied","pieds","orteil",
    "peau","muscle","os","sang","coeur","poumon","cerveau",
    # Maison et lieu
    "maison","appartement","immeuble","batiment","edifice","construction",
    "chambre","salon","cuisine","salle","bureau","couloir","escalier","cave",
    "grenier","garage","jardin","terrasse","balcon","toit","porte","fenetre",
    "mur","sol","plafond","meubles","table","chaise","canape","lit","armoire",
    "rue","avenue","boulevard","chemin","route","autoroute","pont","tunnel",
    "ville","village","quartier","banlieue","campagne","ferme","chateau",
    "ecole","college","lycee","universite","bibliotheque","musee","theatre",
    "cinema","restaurant","hotel","hopital","pharmacie","magasin","boutique",
    "supermarche","boulangerie","boucherie","epicerie","marche","banque","poste",
    "gare","aeroport","port","station","arret","metro","bus","tramway",
    "parc","jardin","foret","bois","montagne","colline","vallee","plaine",
    "mer","ocean","lac","riviere","fleuve","plage","ile","cote",
    # Animaux
    "chat","chien","cheval","vache","cochon","mouton","chevre","ane",
    "poule","coq","canard","oie","dinde","lapin","souris","rat",
    "oiseau","aigle","hibou","perroquet","moineau","pigeon","corbeau",
    "poisson","requin","dauphin","baleine","pieuvre","crabe","homard",
    "lion","tigre","elephant","girafe","zebre","singe","gorille","ours",
    "loup","renard","cerf","lapin","herisson","ecureuil","castor",
    "serpent","lezard","tortue","grenouille","insecte","abeille","papillon",
    # Nourriture
    "pain","baguette","croissant","brioche","gateau","tarte","biscuit","cookie",
    "lait","beurre","fromage","yaourt","creme","oeuf","oeufs",
    "viande","boeuf","poulet","porc","agneau","jambon","saucisse","saucisson",
    "poisson","thon","saumon","sardine","crevette","moule",
    "legume","carotte","pomme","terre","tomate","salade","haricot","petit","pois",
    "oignon","ail","poivron","aubergine","courgette","champignon","brocoli",
    "fruit","pomme","poire","banane","orange","citron","fraise","framboise",
    "cerise","peche","abricot","mangue","ananas","raisin","melon","pastèque",
    "riz","pates","nouilles","soupe","bouillon","salade","sandwich","pizza","burger",
    "sucre","sel","poivre","moutarde","mayonnaise","ketchup","sauce","huile","vinaigre",
    "eau","lait","jus","cafe","the","chocolat","coca","biere","vin","champagne",
    # Vetements
    "habit","vetement","vetements","tenue","costume","robe","jupe","pantalon",
    "jean","short","bermuda","legging","collant","slip","culotte","boxer",
    "chemise","chemisier","tshirt","pull","sweat","veste","manteau","blouson",
    "imperméable","parka","anorak","gilet","cardigan","blazer",
    "chaussure","chaussures","basket","botte","sandale","talon","mocassin",
    "chaussette","chaussettes","collants","sous","vetements",
    "chapeau","casquette","bonnet","echarpe","gant","gants","ceinture","sac",
    # Transports
    "voiture","auto","automobile","camion","camionnette","fourgon","van",
    "moto","scooter","velo","trottinette","skateboard","roller",
    "bus","autobus","autocar","metro","tramway","train","tgv","rer",
    "avion","helicoptere","drone","parachute","bateau","voilier","ferry",
    "taxi","uber","covoiturage","ambulance","pompier","police",
    # Technologie
    "telephone","portable","smartphone","tablette","ordinateur","laptop","pc","mac",
    "ecran","clavier","souris","imprimante","scanner","webcam","casque","enceinte",
    "internet","wifi","cable","chargeur","batterie","application","appli","logiciel",
    "reseau","serveur","cloud","email","mail","message","sms","appel","video",
    "facebook","instagram","snapchat","twitter","youtube","tiktok","whatsapp","discord",
    "google","amazon","apple","microsoft","samsung","netflix","spotify",
    "photo","selfie","video","film","serie","musique","podcast","stream","live",
    # Corps social
    "travail","boulot","taf","job","emploi","metier","carriere","salaire","argent",
    "euro","centime","billet","monnaie","banque","compte","virement","cheque",
    "famille","foyer","menage","couple","mariage","divorce","naissance","deces",
    "ami","amitie","amour","relation","rencontre","rendez","vous","sortie","soiree",
    "fete","anniversaire","noel","paques","vacances","conge","week","end","weekend",
    "sport","foot","football","basket","tennis","rugby","volley","natation","course",
    "velo","randonnee","musculation","yoga","danse","boxe","judo","karate","natation",
    "loisir","hobby","passion","cinema","theatre","concert","exposition","musee",
    # Temps
    "jour","nuit","matin","midi","apres","midi","soir","minuit",
    "heure","minute","seconde","moment","instant","fois","periode","epoque",
    "lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche",
    "janvier","fevrier","mars","avril","mai","juin","juillet","aout","septembre","octobre","novembre","decembre",
    "semaine","mois","annee","siecle","millenaire","hier","aujourd","hui","demain",
    "maintenant","bientot","tout","de","suite","depuis","pendant","avant","apres",
    "tot","tard","vite","longtemps","souvent","parfois","rarement","jamais",
    # Sentiments et etats
    "heureux","heureuse","triste","content","contente","fache","fachee",
    "amoureux","amoureuse","jaloux","jalouse","fier","fiere","honte","gene","genee",
    "peur","joie","colere","tristesse","bonheur","malheur","chance","malchance",
    "fatigue","fatiguee","malade","sain","saine","fort","forte","faible",
    "choque","surprise","etonne","etonnee","decu","decue","fier","fiere",
    "stress","stresse","stressee","calme","zen","detend","detente","relaxe",
    "ennuye","ennuyee","excite","excitee","curieux","curieuse","indifferent",
    "bored","excite","nerveux","nerveuse","anxieux","anxieuse","confiant","confiante",
    # Argot et SMS
    "t","c","g","j","v","n","l","m","y","k","r","z","s","a","e","i","o","u",
    "trop","super","hyper","mega","vachement","vraiment","carrément","franchement",
    "genre","style","espece","sorte","truc","machin","bidule","chose","affaire",
    "ouais","ouai","ouep","yep","yop","bah","beh","ben","bon","eh","ah","oh","ow",
    "wesh","wsh","yo","ayo","oye","hey","hé","allo","ola","coucou","salut",
    "ok","okay","nan","nope","si","oui","mouais","bof","pff","pfff","lol","mdr",
    "ptdr","xd","omg","wtf","omfg","wth","ngl","imo","tbh","fr","frr","bruh",
    "stp","svp","jsp","jpp","jvs","pk","pcq","pck","pr","ns","vs","qd","dc",
    "mtn","mntnt","mm","ms","mc","mec","gars","meuf","nana","keuf","keum",
    "bro","frero","frer","frere","freere","soeur","soeurette","sis","daronne","daron",
    "poto","pote","copain","copine","ami","amie","bg","bg","bb","babe","cheri","cherie",
    "nul","nulle","ouf","chelou","zarbi","bizarre","louche","weird","random",
    "cool","swag","classe","stylé","stylée","hype","tendance","viral","buzz",
    "chiant","chiante","relou","reloud","lourd","lourde","saoul","saoule",
    "grave","clairement","exactement","absolument","totalement","completement",
    "carrément","franchement","serieusement","serieux","serieuse","honnetement",
    "bisou","bisous","bise","bises","kiss","câlin","calin","amour","love",
    "enerve","enervee","soule","soulee","agace","agacee","irrite","irritee",
    "perdu","perdue","perdu","confus","confuse","perturbe","perturbee","perplexe",
    "manger","bouffer","crever","creve","dormir","pioncer","sortir","kiffer",
    "aimer","adorer","detester","hair","apprécier","apprecier","preferer",
    "parler","causer","tchatcher","discuter","expliquer","raconter","dire","crier","chuchoter",
    "ecouter","entendre","regarder","voir","observer","fixer","scruter",
    "toucher","sentir","gouter","respirer","bouger","marcher","courir","sauter",
    "tomber","glisser","nager","voler","grimper","descendre","monter","entrer","sortir",
    # France et lieux
    "france","paris","lyon","marseille","bordeaux","toulouse","nice","nantes",
    "strasbourg","montpellier","lille","rennes","reims","toulon","grenoble",
    "dijon","angers","nimes","villeurbanne","saint","etienne","le","havre",
    "europe","monde","afrique","asie","amerique","australie","antartique",
    "espagne","italie","allemagne","angleterre","portugal","belgique","suisse",
    "maroc","algerie","tunisie","senegal","cameroun","cote","ivoire",
    # Divers
    "chose","truc","machin","bidule","affaire","histoire","exemple","raison",
    "probleme","solution","question","reponse","idee","projet","plan","but",
    "droit","gauche","haut","bas","devant","derriere","milieu","centre","cote",
    "numero","chiffre","lettre","mot","phrase","texte","livre","page","chapitre",
    "couleur","rouge","bleu","vert","jaune","noir","blanc","gris","rose","violet",
    "orange","marron","beige","turquoise","or","argent","bronze",
    "taille","poids","hauteur","largeur","longueur","distance","vitesse","temperature",
    "bruit","son","musique","chanson","melodie","rythme","parole","lyrique",
    "lumiere","ombre","couleur","image","photo","dessin","peinture","sculpture",
    # Verbes conjugues supplementaires
    "mange","manges","mangeons","mangez","mangent","mangé",
    "parle","parles","parlons","parlez","parlent","parlé",
    "joue","joues","jouons","jouez","jouent","joué",
    "aime","aimes","aimons","aimez","aiment","aimé",
    "fais","fait","faisons","faites","font","faisais","faisait",
    "vais","vas","va","allons","allez","vont","allait","allais",
    "suis","es","sommes","etes","sont","etait","etais","etaient",
    "ai","as","avons","avez","ont","avait","avais","avaient",
    "peux","peut","pouvons","pouvez","peuvent","pouvais",
    "veux","veut","voulons","voulez","veulent","voulais",
    "dois","doit","devons","devez","doivent","devais",
    "sais","sait","savons","savez","savent","savais",
    "viens","vient","venons","venez","viennent","venais",
    "dis","dit","disons","dites","disent","disais",
    "prends","prend","prenons","prenez","prennent","prenais",
    "mets","met","mettons","mettez","mettent","mettais",
    "vois","voit","voyons","voyez","voient","voyais",
    "ris","rit","rions","riez","rient","pleure","pleures","pleurent",
    "cours","court","courons","courez","courent","marchons",
    "dors","dort","dormons","dormez","dorment","dormais",
    "ecris","ecrit","ecrivons","ecrivez","ecrivent",
    "lis","lit","lisons","lisez","lisent","lisais",
    "bois","boit","buvons","buvez","boivent","buvais",
    "sors","sort","sortons","sortez","sortent","sortais",
    "rentre","rentres","rentrons","rentrez","rentrent",
    "reste","restes","restons","restez","restent",
    "passe","passes","passons","passez","passent",
    "regarde","regardes","regardons","regardez","regardent",
    "ecoute","ecoutes","ecoutons","ecoutez","ecoutent",
    "appelle","appelles","appelons","appelez","appellent",
    "travaille","travailles","travaillons","travaillez","travaillent",
    "chante","chantes","chantons","chantez","chantent",
    "danse","danses","dansons","dansez","dansent",
    "cherche","cherches","cherchons","cherchez","cherchent",
    "trouve","trouves","trouvons","trouvez","trouvent",
    "pense","penses","pensons","pensez","pensent",
    "crois","croit","croyons","croyez","croient",
    "connais","connait","connaissons","connaissez","connaissent",
    "comprends","comprend","comprenons","comprenez","comprennent",
    "apprends","apprend","apprenons","apprenez","apprennent",
    "oublie","oublies","oublions","oubliez","oublient",
    "demande","demandes","demandons","demandez","demandent",
    "repond","reponds","repondons","repondez","repondent",
    "aide","aides","aidons","aidez","aident",
    "achete","achetes","achetons","achetez","achetent",
    "reviens","revient","revenons","revenez","reviennent",
    "attends","attend","attendons","attendez","attendent",
    # Formes passées et futures
    "suis","etais","serai","serais","sera","serons","serez","seront",
    "avais","aurai","aurais","aura","aurons","aurez","auront",
    "allait","irai","irais","ira","irons","irez","iront",
    "faisait","ferai","ferais","fera","ferons","ferez","feront",
    "disait","dirai","dirais","dira","dirons","direz","diront",
    "voyait","verrai","verrais","verra","verrons","verrez","verront",
    "savait","saurai","saurais","saura","saurons","saurez","sauront",
    "pouvait","pourrai","pourrais","pourra","pourrons","pourrez","pourront",
    "voulait","voudrai","voudrais","voudra","voudrons","voudrez","voudront",
    "devait","devrai","devrais","devra","devrons","devrez","devront",
    "prenait","prendrai","prendras","prendra","prendrons","prendrez","prendront",
    "venait","viendrai","viendras","viendra","viendrons","viendrez","viendront",
    # Expressions et mots liaisons
    "donc","alors","ensuite","enfin","bref","quand","meme","surtout",
    "pourtant","cependant","neanmoins","toutefois","sinon","autrement",
    "voila","voici","tiens","attention","zut","mince","super","genial",
    "parfait","exactement","evidemment","certainement","absolument","totalement",
    "normalement","generalement","habituellement","specialement","rapidement",
    "lentement","doucement","fortement","faiblement","clairement","simplement",
    "ensemble","seul","seule","seuls","seules","ensemble","partout","nulle",
    "ailleurs","autour","dedans","dehors","dessus","dessous","devant","derriere",
    # Mots de politesse et salutations
    "bonjour","bonsoir","bonne","nuit","salut","coucou","hello","allo","bye",
    "merci","beaucoup","sil","vous","plait","pardon","excuse","desole","desolee",
    "bienvenue","felicitations","bravo","courage","bonne","chance","bonne","journee",
    "sante","cheers","tchin","bisous","bises","grosses","bisous","gros","câlins",
    # Interjections et onomatopées
    "ah","oh","eh","euh","hein","ben","bah","bof","pfff","ouah","wow","super",
    "aie","ouch","zut","mince","flute","merde","putain","bordel","nom","sacre",
    "chut","stop","allez","hop","et","voila","la","ca","y","est",
    # Formes verbales courtes
    "est","sont","ont","vas","fut","put","dut","vit","dit","fit","dit","ait",
    "bel","beau","belle","bon","bonne","mal","mauvais","mauvaise","nul","nulle",
    "bete","betes","idiot","idiote","naze","nazes","con","conne","connard",
    "gros","grosse","gras","grasse","mou","molle","dur","dure","sec","seche",
    # Prenoms francais communs
    "romain","thomas","nicolas","antoine","julien","maxime","alexandre","clement",
    "pierre","paul","jean","louis","hugo","lucas","theo","leo","noah","adam","enzo",
    "marie","sophie","emma","lea","camille","manon","chloe","sarah","lucie","jade",
    "alice","julie","laura","pauline","anais","marine","clara","elodie","melissa",
    "kevin","jordan","dylan","ryan","mathieu","sebastien","francois","guillaume",
    "mama","papa","tata","tonton","papy","mamie","papi","meme","doudou","cheri","cherie"
])

# ── FONCTIONS ─────────────────────────────────────────────────────────────────
def generer_indices(n, cle_int):
    indices = list(range(n))
    seed(cle_int)
    i = n - 1
    while i > 0:
        j = randint(0, i)
        indices[i], indices[j] = indices[j], indices[i]
        i -= 1
    return indices

def preparer_message(msg):
    msg_idx = []
    msg_in_alp = []
    for c in msg.lower():
        if c in ALP_IDX:
            msg_idx.append(ALP_IDX[c])
            msg_in_alp.append(True)
        else:
            msg_idx.append(-1)
            msg_in_alp.append(False)
    return msg_idx, msg_in_alp

def ratio_voyelles_ok(texte):
    lettres = [c for c in texte if c in alp and c != " "]
    if len(lettres) == 0:
        return True
    voyelles = sum(1 for c in lettres if c in VOYELLES)
    ratio = voyelles / len(lettres)
    return MIN_VOYELLES <= ratio <= MAX_VOYELLES

# Seuls ces petits mots sont acceptes — les autres sont ignores
PETITS_MOTS_VALIDES = {"le","la","les","de","du","des","un","une","et","en","au","a",
    "je","tu","il","on","ce","ca","si","ou","ni","ne","se","me","te","ma","ta","sa",
    "ok","yo","ah","eh","oh","oui","non","oui","nan","bah","ben","bon","ya","va"}

def score_francais(texte):
    score = 0
    mots = texte.split()
    nb_mots = len(mots) if mots else 1
    nb_mots_reconnus_longs = 0   # mots de 4+ lettres reconnus
    nb_mots_longs_inconnus = 0   # mots de 4+ lettres non reconnus
    nb_parasites = 0             # petits mots non valides

    for mot in mots:
        if len(mot) >= 4 and mot in mots_fr:
            score += 15 + len(mot) * 0.5
            nb_mots_reconnus_longs += 1
        elif len(mot) == 3 and mot in mots_fr:
            score += 8
            nb_mots_reconnus_longs += 1
        elif len(mot) >= 4:
            nb_mots_longs_inconnus += 1
        elif len(mot) <= 3 and mot in PETITS_MOTS_VALIDES:
            score += 2
        else:
            nb_parasites += 1

    # Penalite forte pour les parasites
    score -= nb_parasites * 4

    # Penalite pour mots longs inconnus
    score -= nb_mots_longs_inconnus * 3

    # Gros bonus si plusieurs vrais mots longs reconnus
    if nb_mots_reconnus_longs >= 3:
        score += 40
    elif nb_mots_reconnus_longs >= 2:
        score += 20
    elif nb_mots_reconnus_longs >= 1:
        score += 5

    # Penaliser suites de 3+ consonnes
    consonnes = set("bcdfghjklmnpqrstvwxyz")
    suite = 0
    for c in texte:
        if c in consonnes:
            suite += 1
            if suite >= 3:
                score -= 2
        else:
            suite = 0

    # Penaliser mots sans voyelle de 4+ lettres
    for mot in mots:
        if len(mot) >= 4 and not any(v in mot for v in "aeiouy"):
            score -= 5

    return round(score, 1)

def afficher_barre_globale(placeholder, nb_blocs):
    pct = len(st.session_state.blocs_testes) / nb_blocs * 100 if nb_blocs > 0 else 0
    segments = ""
    for b in range(nb_blocs):
        couleur = "#00ff88" if b in st.session_state.blocs_testes else "#ff4444"
        segments += f'<span style="display:inline-block;width:{100/nb_blocs:.2f}%;height:16px;background:{couleur};" title="Bloc {b}"></span>'
    html = f"""<div style="margin:1rem 0;">
        <p style="color:#8a9ab0;font-family:Share Tech Mono,monospace;font-size:0.8rem;margin-bottom:0.3rem;">
        PROGRESSION — {pct:.1f}% ({len(st.session_state.blocs_testes)}/{nb_blocs} blocs)</p>
        <div style="width:100%;display:flex;border-radius:4px;overflow:hidden;border:1px solid #1e3a5f;">{segments}</div>
        <div style="display:flex;gap:1rem;margin-top:0.3rem;">
        <span style="color:#00ff88;font-family:Share Tech Mono,monospace;font-size:0.75rem;">■ Teste</span>
        <span style="color:#ff4444;font-family:Share Tech Mono,monospace;font-size:0.75rem;">■ Non teste</span>
        </div></div>"""
    placeholder.markdown(html, unsafe_allow_html=True)

def analyser_avec_progression(debut, msg, nb, taille_cle):
    max_cle = 10 ** taille_cle
    fin = min(debut + TAILLE_BLOC, max_cle)
    n = len(msg)
    msg_idx, msg_in_alp = preparer_message(msg)
    resultats = []
    barre = st.progress(0)
    info = st.empty()
    total = max(1, fin - max(1, debut))
    fmt = f"0{taille_cle}d"
    for idx, cle_int in enumerate(range(max(1, debut), fin)):
        cle = format(cle_int, fmt)
        dec = [int(cle[i % taille_cle]) for i in range(n)]
        indices = generer_indices(n, cle_int)
        res = [None] * n
        for i in range(n):
            src = indices[i]
            if msg_in_alp[src]:
                res[i] = alp[(msg_idx[src] - dec[i]) % N_ALP]
            else:
                res[i] = msg[src]
        texte = "".join(res)
        if not ratio_voyelles_ok(texte):
            continue
        s = score_francais(texte)
        resultats.append((s, cle, texte))
        # Garder seulement le top 50 en temps reel pour economiser la memoire
        if len(resultats) > 50:
            resultats.sort(reverse=True)
            resultats = resultats[:50]
        if idx % 25000 == 0:
            pct = idx / total
            barre.progress(min(pct, 1.0))
            info.markdown(f"<p style='color:#8a9ab0;font-size:0.8rem;font-family:Share Tech Mono,monospace;'>Cle {cle} — {pct*100:.1f}% — {len(resultats)} resultats</p>", unsafe_allow_html=True)
    barre.progress(1.0)
    info.empty()
    resultats.sort(reverse=True)
    return resultats[:nb]

def afficher_resultats(top):
    if top:
        st.markdown("<p style='color:#00ff88;font-weight:700;letter-spacing:0.2em;'>🏆 MEILLEURS RÉSULTATS :</p>", unsafe_allow_html=True)
        for i, (score, cle, res) in enumerate(top):
            if i == 0:
                st.markdown(f'<div class="result-found">🥇 Clé : <b>{cle}</b> <span class="score-badge">Score {score}</span><br>{res}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="result-normal">#{i+1} Clé : {cle} | Score {score} | {res}</div>', unsafe_allow_html=True)
    else:
        st.warning("Rien trouvé dans ce bloc. Essayez le suivant !")

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "bloc_debut" not in st.session_state:
    st.session_state.bloc_debut = 1
if "classement_global" not in st.session_state:
    st.session_state.classement_global = []
if "blocs_testes" not in st.session_state:
    st.session_state.blocs_testes = set()
if "auto" not in st.session_state:
    st.session_state.auto = False

# ── INTERFACE ────────────────────────────────────────────────────────────────
st.markdown("<h1>🔍 FORCE BRUTE</h1>", unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#8a9ab0;font-family:Share Tech Mono,monospace;font-size:0.85rem;letter-spacing:0.2em;">DETECTION AUTOMATIQUE DE CLE</p>', unsafe_allow_html=True)

taille_cle = st.select_slider("Taille de la clé utilisée pour chiffrer", options=[4, 6, 8, 10, 12], value=8)
max_cle = 10 ** taille_cle
nb_blocs = max(1, max_cle // TAILLE_BLOC)

barre_globale_placeholder = st.empty()
afficher_barre_globale(barre_globale_placeholder, nb_blocs)

msg = st.text_input("Message chiffré à analyser", placeholder="Collez votre message chiffré ici...")
nb = st.slider("Nombre de meilleurs résultats à afficher", min_value=3, max_value=20, value=5)
cle_depart_str = st.text_input("Clé de départ", value=str(st.session_state.bloc_debut).zfill(taille_cle), max_chars=taille_cle, placeholder=f"ex: {'0'*(taille_cle-1)}1")

if len(cle_depart_str) == taille_cle and cle_depart_str.isdigit():
    debut = int(cle_depart_str)
else:
    debut = 1

fin = debut + TAILLE_BLOC
bloc = debut // TAILLE_BLOC

st.markdown(f'<div class="bloc-info">🔢 Bloc {bloc}/{nb_blocs-1} — Clés : <b>{debut:0{taille_cle}d}</b> à <b>{min(fin-1, max_cle-1):0{taille_cle}d}</b> — {bloc/nb_blocs*100:.1f}% exploré</div>', unsafe_allow_html=True)
st.info(f"⚠️ Vérifiez que la taille de clé ({taille_cle} chiffres) correspond bien à la clé utilisée pour chiffrer le message !")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚀 ANALYSER CE BLOC"):
        if not msg:
            st.error("Entrez un message chiffré !")
        else:
            st.session_state.auto = False
            st.session_state.bloc_debut = debut
            top = analyser_avec_progression(debut, msg, nb, taille_cle)
            st.session_state.blocs_testes.add(debut // TAILLE_BLOC)
            afficher_barre_globale(barre_globale_placeholder, nb_blocs)
            st.success("✅ Bloc testé !")
            afficher_resultats(top)

with col2:
    if st.button("⏭️ BLOC SUIVANT"):
        if not msg:
            st.error("Entrez un message chiffré !")
        else:
            st.session_state.auto = False
            prochain = debut + TAILLE_BLOC
            st.session_state.bloc_debut = prochain
            top = analyser_avec_progression(prochain, msg, nb, taille_cle)
            st.session_state.blocs_testes.add(prochain // TAILLE_BLOC)
            afficher_barre_globale(barre_globale_placeholder, nb_blocs)
            st.success(f"✅ Bloc {prochain // TAILLE_BLOC} testé !")
            afficher_resultats(top)

with col3:
    label_auto = "⛔ STOP AUTO" if st.session_state.auto else "🤖 AUTO"
    if st.button(label_auto):
        if not msg:
            st.error("Entrez un message chiffré !")
        else:
            st.session_state.auto = not st.session_state.auto
            st.rerun()

if st.session_state.auto and msg:
    st.warning("⚙️ Mode automatique actif — cliquez STOP AUTO pour arrêter")
    classement_placeholder = st.empty()
    bloc_auto = debut
    while bloc_auto < max_cle:
        top = analyser_avec_progression(bloc_auto, msg, nb, taille_cle)
        st.session_state.blocs_testes.add(bloc_auto // TAILLE_BLOC)
        afficher_barre_globale(barre_globale_placeholder, nb_blocs)
        if top:
            st.session_state.classement_global.extend(top)
            st.session_state.classement_global.sort(reverse=True)
            st.session_state.classement_global = st.session_state.classement_global[:20]
        with classement_placeholder.container():
            st.markdown("<p style='color:#00ff88;font-weight:700;letter-spacing:0.2em;'>🏆 CLASSEMENT EN COURS :</p>", unsafe_allow_html=True)
            for i, (score, cle, res) in enumerate(st.session_state.classement_global[:nb]):
                if i == 0:
                    st.markdown(f'<div class="result-found">🥇 Clé : <b>{cle}</b> <span class="score-badge">Score {score}</span><br>{res}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-normal">#{i+1} Clé : {cle} | Score {score} | {res}</div>', unsafe_allow_html=True)
        bloc_auto += TAILLE_BLOC
        st.session_state.bloc_debut = bloc_auto

if not st.session_state.auto and st.session_state.classement_global:
    st.markdown("<p style='color:#00ff88;font-weight:700;letter-spacing:0.2em;'>🏆 CLASSEMENT FINAL :</p>", unsafe_allow_html=True)
    for i, (score, cle, res) in enumerate(st.session_state.classement_global[:nb]):
        if i == 0:
            st.markdown(f'<div class="result-found">🥇 Clé : <b>{cle}</b> <span class="score-badge">Score {score}</span><br>{res}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-normal">#{i+1} Clé : {cle} | Score {score} | {res}</div>', unsafe_allow_html=True)
    if st.button("🗑️ Effacer le classement"):
        st.session_state.classement_global = []
        st.session_state.blocs_testes = set()
