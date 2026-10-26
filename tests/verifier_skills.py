"""Vérifie les skills : front matter valide (name = nom du dossier, description non vide) et absence de
chemin ou d'adresse personnels. Usage : python3 tests/verifier_skills.py"""
import os, re, sys

RACINE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'skills')
INTERDITS = [r'C:\\Users\\[A-Za-z]+', r'/home/[a-z]+/', r'\b100\.\d+\.\d+\.\d+\b', r'[\w.+-]+@[\w-]+\.(fr|com)\b']
erreurs, n = [], 0
for nom in sorted(os.listdir(RACINE)):
    d = os.path.join(RACINE, nom)
    f = os.path.join(d, 'SKILL.md')
    if not os.path.isfile(f):
        erreurs.append(f'{nom}: SKILL.md absent'); continue
    n += 1
    texte = open(f, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n', texte, re.S)
    if not m:
        erreurs.append(f'{nom}: front matter absent'); continue
    champs = dict(re.findall(r'^([a-z-]+):\s*(.*)$', m.group(1), re.M))
    if champs.get('name', '').strip() != nom:
        erreurs.append(f'{nom}: name « {champs.get("name")} » différent du dossier')
    if not (champs.get('description', '').strip() or 'description:' in m.group(1)):
        erreurs.append(f'{nom}: description vide')
    for racine, _, fichiers in os.walk(d):
        for x in fichiers:
            if x.endswith(('.md', '.py', '.mjs', '.ps1', '.sh', '.css', '.json')):
                t = open(os.path.join(racine, x), encoding='utf-8', errors='replace').read()
                for p in INTERDITS:
                    for hit in re.finditer(p, t):
                        if hit.group(0) in ('@media',): continue
                        erreurs.append(f'{os.path.relpath(os.path.join(racine, x), RACINE)}: motif personnel « {hit.group(0)} »')
print(f'{n} skills contrôlés')
for e in erreurs: print('ERREUR', e)
sys.exit(1 if erreurs else 0)
