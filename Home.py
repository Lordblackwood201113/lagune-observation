import streamlit as st
import geemap
import json
import os

# Récupérer le secret et le convertir en dict standard (si ce n'est pas déjà un dict)
key_dict = dict(st.secrets["gcp_service_account"])

# Définir le chemin du fichier de clé (il ne sera pas poussé dans le dépôt si vous l'ajoutez à .gitignore)
key_file_path = "private_key.json"

# Créer le fichier de clé s'il n'existe pas déjà
if not os.path.exists(key_file_path):
    with open(key_file_path, "w") as f:
        json.dump(key_dict, f)

# Utiliser geemap.ee_authenticate en mode service_account
geemap.ee.authenticate(
    auth_mode="service_account",
    service_account=key_dict["client_email"],
    key_file=key_file_path
)

# Initialiser Earth Engine (cette étape est effectuée automatiquement par ee_authenticate, 
# mais peut être appelée explicitement si besoin)
geemap.ee.Initialize()

# Vous pouvez maintenant continuer avec votre application Streamlit
st.write("Authentification Earth Engine réussie !")
m = geemap.Map()
m.add_basemap("HYBRID")
m.to_streamlit()
