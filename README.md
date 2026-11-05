# TP MongoDB (Nowledgeable « 16. MongoDB », cours du 05/11/2026)

Lien : https://nowledgeable.com/student/session/a605391e-f319-4424-a957-970c04a1cc6b/do

| Fichier | Exercice |
|---|---|
| `connexion.py` | connexion Atlas (code du prof : `MongoClient` + `ping`) |
| `lab1_ecommerce.py` | 1. Discovering MongoDB : users / products / orders, requêtes, update, delete |
| `lab2_modeling.py` | 2. NoSQL Modeling : posts avec commentaires et likes imbriqués, 5 requêtes |
| `api_manga.py` | 5. Mini exercise : API Flask `POST /items`, `GET /items/<id>`, `GET /items`, `GET /search` |

## Lancer sur ton cluster Atlas (PowerShell)
1. Atlas > ton cluster > **Connect** > **Drivers** > copie le lien `mongodb+srv://...` (remplace `<db_password>`).
2. Dans Atlas > **Network Access**, autorise ton adresse IP (bouton « Add current IP »).
3. Dans PowerShell, dans ce dossier (le lien reste dans cette fenêtre seulement, jamais dans un fichier) :

```powershell
$env:MONGODB_URI = "mongodb+srv://..."
python lab1_ecommerce.py
python lab2_modeling.py
python api_manga.py      # puis http://127.0.0.1:5000/search?keyword=ninja&genre=action
```

Test sans serveur (fausse base en mémoire) : `$env:MONGOMOCK = "1"` avant les commandes (testé le 05/11/2026 : tout passe).
