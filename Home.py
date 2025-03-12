import streamlit as st
import geemap
import json
import tempfile

def main():
    # Récupérer la clé sous forme de dictionnaire
    key_dict = st.secrets["gcp_service_account"]  # Ceci est un dict
    service_account = key_dict["client_email"]    # "xxx@xxx.iam.gserviceaccount.com"

    # Convertir le dict en chaîne JSON
    key_json_str = json.dumps(key_dict)

    # Créer un fichier temporaire pour y écrire le JSON
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write(key_json_str)
        temp_key_path = f.name  # Retenir le chemin du fichier créé

    # Authentification avec geemap
    geemap.ee_authenticate(
        auth_mode='service_account',
        service_account=service_account,
        key_file=temp_key_path
    )

    # Maintenant, Earth Engine est initialisé, on peut utiliser geemap
    m = geemap.Map()
    m.add_basemap("HYBRID")
    m.to_streamlit()

if __name__ == "__main__":
    main()
