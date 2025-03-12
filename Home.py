import os
import json
import geemap
import ee
import tempfile

# Pour Python 3.11, utilisez tomllib (sinon installez tomli ou toml)
try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # Pour les versions antérieures

# Récupérer le contenu TOML depuis la variable d'environnement Heroku
toml_key = os.environ.get("GCP_SERVICE_ACCOUNT_KEY")
if not toml_key:
    raise Exception("La variable d'environnement GCP_SERVICE_ACCOUNT_KEY n'est pas définie.")

# Parser le TOML et extraire la section [gcp_service_account]
try:
    toml_dict = tomllib.loads(toml_key)
except Exception as e:
    raise Exception(f"Erreur de décodage TOML : {e}")

key_dict = toml_dict.get("gcp_service_account")
if not key_dict:
    raise Exception("La section 'gcp_service_account' n'a pas été trouvée dans le TOML.")

# Extraire l'email du compte de service
service_account = key_dict["client_email"]

# Convertir le dictionnaire en chaîne JSON
json_key = json.dumps(key_dict)

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

# Exemple d'utilisation avec geemap (affichage d'une carte)
m = geemap.Map()
m.add_basemap("HYBRID")
m.to_streamlit()
