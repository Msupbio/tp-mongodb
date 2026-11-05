# connexion.py : ouvre la connexion à MongoDB, partagée par tous les scripts du TP
# Le lien Atlas complet contient ton mot de passe : il n'est JAMAIS écrit dans le code ni dans OneDrive.
# 1re fois : on te demande le mot de passe, puis le lien complet est rangé dans
# C:\Users\admin\.mongodb-atlas\uri.txt (hors OneDrive, comme .mysql-local) ; ensuite plus rien à taper.
import os                                      # os = chemins et variables d'environnement
from pathlib import Path                       # Path = manipuler un chemin de fichier
from urllib.parse import quote_plus            # encode les caractères spéciaux du mot de passe (@, :, /…)

URI_FILE = Path.home() / ".mongodb-atlas" / "uri.txt"   # fichier local, jamais synchronisé ni publié
URI_MODELE = None                              # lien demandé au 1er lancement (rien de personnel dans le code)

def get_uri():
    if os.environ.get("MONGODB_URI") and "<db_" not in os.environ["MONGODB_URI"]:
        return os.environ["MONGODB_URI"]       # lien complet donné à la main : prioritaire
    if URI_FILE.exists():                      # lien déjà enregistré : on le relit
        return URI_FILE.read_text(encoding="utf-8").strip()
    from getpass import getpass                # getpass = saisie masquée (rien ne s'affiche)
    uri = os.environ.get("MONGODB_URI") or URI_MODELE or input("Lien Atlas (Connect > Drivers) : ").strip()
    if "<db_username>" in uri:
        uri = uri.replace("<db_username>", quote_plus(input("Utilisateur Atlas : ").strip()))
    uri = uri.replace("<db_password>", quote_plus(getpass("Mot de passe de l'utilisateur Atlas : ")))
    return uri

def get_client():
    """Renvoie un client MongoDB (connexion au serveur)."""
    if os.environ.get("MONGOMOCK") == "1":     # mode test hors ligne : fausse base en mémoire
        import mongomock                       # mongomock imite pymongo sans serveur
        return mongomock.MongoClient()
    from pymongo import MongoClient            # MongoClient = l'objet qui parle au serveur
    from pymongo.server_api import ServerApi   # ServerApi('1') = version stable de l'API (code du prof)
    uri = get_uri()
    client = MongoClient(uri, server_api=ServerApi("1"))
    client.admin.command("ping")               # ping = test de connexion ; échoue si mot de passe faux
    print("Pinged your deployment. You successfully connected to MongoDB!")
    if not URI_FILE.exists():                  # on n'enregistre qu'un lien qui a marché
        URI_FILE.parent.mkdir(exist_ok=True)
        URI_FILE.write_text(uri, encoding="utf-8")
        print(f"Lien enregistré dans {URI_FILE} : tu n'auras plus à le taper.")
    return client
