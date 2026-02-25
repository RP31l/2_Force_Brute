import streamlit as st
from random import seed, randint
import anthropic

st.set_page_config(page_title="Force Brute IA", page_icon="🤖", layout="centered")

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
.result-box {
    background: linear-gradient(135deg, #0a2a0a, #0d3b0d);
    border: 2px solid #00ff88; border-radius: 8px;
    padding: 1.5rem; font-family: 'Share Tech Mono', monospace;
    font-size: 1rem; color: #00ff88; margin-top: 1rem;
    letter-spacing: 0.05em; line-height: 1.8; white-space: pre-wrap;
}
.candidate-box {
    background: #0d1b2a; border: 1px solid #1e3a5f; border-radius: 6px;
    padding: 0.6rem 1rem; font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem; color: #8a9ab0; margin-bottom: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

alp = "abcdefghijklmnopqrstuvwxyz"

def generer_indices(mot, cle_int):
    indices = list(range(len(mot)))
    seed(cle_int)
    i = len(indices) - 1
    while i > 0:
        j = randint(0, i)
        indices[i], indices[j] = indices[j], indices[i]
        i -= 1
    return indices

def dechiffrer(mot, cle):
    indices = generer_indices(mot, int(cle))
    res = [""] * len(mot)
    for i, l in enumerate(mot):
        if mot[indices[i]] == " ":
            res[i] = " "
        elif mot[indices[i]].lower() in alp:
            dec = int(cle[i % 8])
            idx = alp.index(mot[indices[i]].lower())
            nl = alp[(idx - dec) % 26]
            res[i] = nl
        else:
            res[i] = mot[indices[i]]
    return "".join(res)

def score_simple(texte):
    mots_fr = [
        "le","la","les","de","du","des","un","une","et","est","en","au","aux",
        "je","tu","il","elle","nous","vous","ils","elles","me","te","se","y",
        "que","qui","quoi","dont","ou","ne","pas","plus","jamais","rien","tout",
        "mon","ton","son","ma","ta","sa","notre","votre","leur","mes","tes","ses",
        "ce","cet","cette","ces","cela","ca","ici","la","voici","voila",
        "avec","pour","sans","sous","sur","dans","par","entre","vers","chez",
        "mais","ou","donc","or","ni","car","si","puis","alors","ainsi","donc",
        "bonjour","bonsoir","salut","merci","svp","stp","oui","non","peut","etre",
        "bien","mal","tres","assez","trop","peu","beaucoup","encore","toujours",
        "avoir","etre","faire","dire","aller","voir","savoir","pouvoir","vouloir",
        "venir","partir","prendre","donner","mettre","passer","tenir","rester",
        "manger","boire","dormir","parler","ecrire","lire","jouer","travailler",
        "aimer","vouloir","devoir","falloir","sembler","paraître","devenir",
        "maman","papa","frere","soeur","ami","amie","copain","copine","famille",
        "maison","ecole","classe","salle","chambre","cuisine","jardin","rue",
        "chat","chien","oiseau","poisson","lapin","cheval","vache","cochon",
        "jour","nuit","matin","soir","midi","heure","minute","seconde","semaine",
        "monde","pays","ville","village","mer","montagne","foret","riviere",
        "rouge","bleu","vert","jaune","noir","blanc","gris","rose","orange",
        "grand","petit","gros","mince","beau","bel","belle","bon","mauvais",
        "nouveau","vieux","jeune","vieux","premier","dernier","autre","même",
        "homme","femme","enfant","garcon","fille","bebe","adulte","personne",
        "eau","feu","air","terre","ciel","soleil","lune","etoile","nuage","pluie",
        "pain","lait","fromage","viande","fruit","legume","gateau","sucre","sel",
        "table","chaise","lit","porte","fenetre","mur","sol","plafond","escalier",
        "voiture","velo","bus","train","avion","bateau","moto","pied","main",
        "tete","bras","jambe","oeil","nez","bouche","oreille","dos","ventre",
        "livre","cahier","stylo","crayon","gomme","regle","cartable","sac",
        "telephone","ordinateur","television","radio","internet","message","photo",
        "sport","football","basket","tennis","natation","course","danse","musique",
        "france","paris","lyon","marseille","bordeaux","nice","nantes","strasbourg",
        "argent","euro","prix","achat","vente","magasin","marche","boutique",
        "temps","meteo","chaud","froid","beau","pluie","neige","vent","orage"
    ]
    score = 0
    for mot in texte.lower().split():
        if mot in mots_fr:
            score += 3
    for c in texte.lower():
        if c in "easitnrul":
            score += 0.1
    return round(score, 1)

# ── INTERFACE ────────────────────────────────────────────────────────────────
st.markdown("<h1>🤖 FORCE BRUTE IA</h1>", unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#8a9ab0;font-family:Share Tech Mono,monospace;font-size:0.85rem;letter-spacing:0.2em;">ANALYSE PAR INTELLIGENCE ARTIFICIELLE</p>', unsafe_allow_html=True)

api_key = st.secrets["ANTHROPIC_API_KEY"]
msg = st.text_input("Message chiffré à analyser", placeholder="Collez votre message chiffré ici...")

if st.button("🚀 LANCER L'ANALYSE IA"):
    if not msg:
        st.error("Entrez un message chiffré !")
    else:
        with st.spinner("Etape 1/2 — Test de toutes les cles..."):
            resultats = []
            for cle_int in range(10000):
                cle = str(cle_int).zfill(4) + str(cle_int).zfill(4)
                try:
                    res = dechiffrer(msg, cle)
                    s = score_simple(res)
                    resultats.append((s, cle, res))
                except:
                    pass
            resultats.sort(reverse=True)
            top20 = resultats[:20]

        st.markdown("<p style='color:#8a9ab0;font-size:0.85rem;'>10000 cles testees — top 20 envoyes a l'IA</p>", unsafe_allow_html=True)

        with st.expander("Voir les 20 candidats envoyes a l'IA"):
            for i, (score, cle, res) in enumerate(top20):
                st.markdown(f'<div class="candidate-box">#{i+1} Cle {cle} | Score {score} | {res}</div>', unsafe_allow_html=True)

        with st.spinner("Etape 2/2 — L'IA analyse les candidats..."):
            candidats_txt = "\n".join([f"#{i+1} Cle={cle} : {res}" for i, (s, cle, res) in enumerate(top20)])
            prompt = f"""Voici 20 tentatives de dechiffrement d'un message code.
Chaque ligne montre une cle et le resultat du dechiffrement.
Le message original est probablement en francais.

{candidats_txt}

Quel numero semble etre le vrai message dechiffre ?
Reponds avec : le numero, la cle, le message dechiffre, et explique pourquoi en 1-2 phrases."""

            try:
                client = anthropic.Anthropic(api_key=api_key)
                response = client.messages.create(
                    model="claude-opus-4-6",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                analyse = response.content[0].text
                st.markdown(f'<div class="result-box">ANALYSE DE L\'IA :\n\n{analyse}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erreur API : {e}")
