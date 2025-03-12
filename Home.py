import os
import json
import geemap
import ee
import tempfile

# Récupérer la chaîne JSON depuis la config var Heroku
json_key = os.environ.get("GCP_SERVICE_ACCOUNT_KEY")
if not json_key:
    raise Exception("La variable d'environnement GCP_SERVICE_ACCOUNT_KEY n'est pas définie.")

# Convertir la chaîne JSON en dict standard (optionnel, pour extraire l'email)
key_dict = json.loads(json_key)
service_account = key_dict["client_email"]

# Créer un fichier temporaire pour stocker la clé JSON
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as key_file:
    key_file.write(json_key)
    temp_key_path = key_file.name

# Authentifier Earth Engine en mode compte de service via geemap.ee_authenticate()
geemap.ee_authenticate(
    auth_mode="service_account",
    service_account=service_account,
    key_file=temp_key_path
)

# Initialiser Earth Engine (geemap.ee_authenticate() appelle ee.Initialize() en interne,
# mais vous pouvez l'appeler explicitement si besoin)
geemap.ee.Initialize()

# Exemple d'utilisation avec geemap (par exemple pour afficher une carte)
m = geemap.Map()
m.add_basemap("HYBRID")
m.to_streamlit()  # ou autre méthode d'affichage, selon votre application
