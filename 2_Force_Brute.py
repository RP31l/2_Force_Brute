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
    background: linear-gradient(135deg, #0a2a0a, #0d3b0d);
    border: 2px solid #00ff88; border-radius: 8px;
    padding: 1rem 1.5rem; font-family: 'Share Tech Mono', monospace;
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

alp = "abcdefghijklmnopqrstuvwxyz "
TAILLE_BLOC = 1000000
NB_BLOCS = 100

mots_fr = set([
    "le","la","les","de","du","des","un","une","et","est","en","au","aux",
    "je","tu","il","elle","nous","vous","ils","elles","me","te","se","y",
    "que","qui","quoi","dont","ou","ne","pas","plus","jamais","rien","tout",
    "mon","ton","son","ma","ta","sa","notre","votre","leur","mes","tes","ses",
    "ce","cet","cette","ces","cela","ca","ici","voici","voila",
    "avec","pour","sans","sous","sur","dans","par","entre","vers","chez",
    "mais","donc","or","ni","car","si","puis","alors","ainsi",
    "bonjour","bonsoir","salut","merci","oui","non","bien","mal","tres",
    "avoir","etre","faire","dire","aller","voir","savoir","pouvoir","vouloir",
    "venir","partir","prendre","donner","mettre","passer","tenir","rester",
    "manger","boire","dormir","parler","ecrire","lire","jouer","travailler",
    "maman","papa","frere","soeur","ami","amie","copain","copine","famille",
    "maison","ecole","classe","salle","chambre","cuisine","jardin","rue",
    "chat","chien","oiseau","poisson","lapin","cheval","vache","cochon",
    "jour","nuit","matin","soir","midi","heure","minute","seconde","semaine",
    "monde","pays","ville","village","mer","montagne","foret","riviere",
    "rouge","bleu","vert","jaune","noir","blanc","gris","rose","orange",
    "grand","petit","gros","mince","beau","bon","mauvais","nouveau","vieux",
    "homme","femme","enfant","garcon","fille","bebe","adulte","personne",
    "eau","feu","air","terre","ciel","soleil","lune","etoile","nuage","pluie",
    "pain","lait","fromage","viande","fruit","legume","gateau","sucre","sel",
    "table","chaise","lit","porte","fenetre","mur","sol","plafond","escalier",
    "voiture","velo","bus","train","avion","bateau","moto","main","tete",
    "bras","jambe","oeil","nez","bouche","oreille","dos","ventre",
    "livre","cahier","stylo","crayon","gomme","regle","cartable","sac",
    "telephone","ordinateur","television","radio","internet","message","photo",
    "sport","football","basket","tennis","natation","course","danse","musique",
    "france","paris","lyon","marseille","bordeaux","nice","nantes","strasbourg",
    "argent","euro","prix","achat","vente","magasin","marche","boutique",
    "temps","meteo","chaud","froid","neige","vent","orage","aimer","devoir"
])

def generer_indices(n, cle_int):
    indices = list(range(n))
    seed(cle_int)
    i = n - 1
    while i > 0:
        j = randint(0, i)
        indices[i], indices[j] = indices[j], indices[i]
        i -= 1
    return indices

def dechiffrer(mot, cle):
    indices = generer_indices(len(mot), int(cle))
    res = [""] * len(mot)
    for i in range(len(mot)):
        c = mot[indices[i]].lower()
        if c in alp:
            dec = int(cle[i % 8])
            idx = alp.index(c)
            res[i] = alp[(idx - dec) % 27]
        else:
            res[i] = mot[indices[i]]
    return "".join(res)

def score_francais(texte):
    score = 0
    for mot in texte.lower().split():
        if mot in mots_fr:
            score += 3
    for c in texte.lower():
        if c in "easitnrul":
            score += 0.1
    return round(score, 1)

# Précalcul des décalages pour accélérer
def precalcul_decalages(cle, n):
    return [int(cle[i % 8]) for i in range(n)]

def analyser_bloc_rapide(debut, msg, nb):
    fin = min(debut + TAILLE_BLOC, 100000000)
    n = len(msg)
    resultats = []
    for cle_int in range(max(1, debut), fin):
        cle = str(cle_int).zfill(8)
        # Précalcul des indices une seule fois par clé
        indices = generer_indices(n, cle_int)
        res = [""] * n
        valide = True
        for i in range(n):
            c = msg[indices[i]].lower()
            if c in alp:
                dec = int(cle[i % 8])
                idx = alp.index(c)
                res[i] = alp[(idx - dec) % 27]
            else:
                res[i] = msg[indices[i]]
        texte = "".join(res)
        s = score_francais(texte)
        if s > 0:
            resultats.append((s, cle, texte))
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

# ── INTERFACE ────────────────────────────────────────────────────────────────
st.markdown("<h1>🔍 FORCE BRUTE</h1>", unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#8a9ab0;font-family:Share Tech Mono,monospace;font-size:0.85rem;letter-spacing:0.2em;">DETECTION AUTOMATIQUE DE CLE</p>', unsafe_allow_html=True)

msg = st.text_input("Message chiffré à analyser", placeholder="Collez votre message chiffré ici...")
nb = st.slider("Nombre de meilleurs résultats à afficher", min_value=3, max_value=20, value=5)
cle_depart_str = st.text_input("Clé de départ (8 chiffres)", value=str(st.session_state.bloc_debut).zfill(8), max_chars=8, placeholder="ex: 00000001")

if len(cle_depart_str) == 8 and cle_depart_str.isdigit():
    debut = int(cle_depart_str)
else:
    debut = 1

fin = debut + TAILLE_BLOC
bloc = debut // TAILLE_BLOC

st.markdown(f'<div class="bloc-info">🔢 Bloc {bloc}/{NB_BLOCS-1} — Clés : <b>{debut:08d}</b> à <b>{fin-1:08d}</b> — {bloc/10:.1f}% exploré</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 ANALYSER CE BLOC"):
        if not msg:
            st.error("Entrez un message chiffré !")
        else:
            st.session_state.bloc_debut = debut
            with st.spinner(f"Test des clés {debut:08d} à {fin-1:08d}..."):
                top = analyser_bloc_rapide(debut, msg, nb)
            st.markdown(f"<p style='color:#8a9ab0;font-size:0.85rem;'>✅ 100 000 clés testées</p>", unsafe_allow_html=True)
            afficher_resultats(top)

with col2:
    if st.button("⏭️ BLOC SUIVANT"):
        if not msg:
            st.error("Entrez un message chiffré !")
        else:
            prochain = debut + TAILLE_BLOC
            st.session_state.bloc_debut = prochain
            with st.spinner(f"Test des clés {prochain:08d} à {prochain+TAILLE_BLOC-1:08d}..."):
                top = analyser_bloc_rapide(prochain, msg, nb)
            st.markdown(f"<p style='color:#8a9ab0;font-size:0.85rem;'>✅ Bloc {prochain // TAILLE_BLOC} testé</p>", unsafe_allow_html=True)
            afficher_resultats(top)
