import streamlit as st
import geemap.foliumap as geemap
import json
import ee

service_account = "test-789@ee-learn2014.iam.gserviceaccount.com"

# key_dict est un dict (St.secrets renvoie un dict)
key_dict = dict(st.secrets["gcp_service_account"])

# On convertit ce dict en chaîne JSON
json_str = json.dumps(key_dict)

credentials = ee.ServiceAccountCredentials(
    service_account=service_account, 
    key_data=json_str  # On passe la chaîne JSON
)

geemap.Initialize(credentials)



st.set_page_config(layout="wide", page_title = "Water Observation", page_icon= "🌍")

st.sidebar.image("Logo.jpg")

st.sidebar.title("Contact")

st.sidebar.info(
    """
    [LinkedIn] https://www.linkedin.com/in/yao-franck-daniel-yao/ |
     
    [Email] gle.yao@inphb.ci |
     
    [GitHub] https://github.com/Lordblackwood201113 |
     
    | [Téléphone](+33 0744943191) | 
    """
)

st.logo("Logo.jpg", size = "medium")


#------- HEADER -------------
with st.container() :
    st.subheader("OBSERVATION DE LA LAGUNE EBRIE 2015 - 2024")
    
# Affichage de quelques métriques (valeurs statiques ici)
total1, total2, total3 = st.columns(3, gap='small')
with total1:
    st.info('Surface lagune 2015')
    st.metric(label="Surface lagune (m^2)", value=868.9111)

with total2:
    st.info('Surface lagune 2024')
    st.metric(label="Surface lagune (m^2)", value=596.3545)

with total3:
    st.info('Surface Remblai')
    st.metric(label="Surfacer Remblais (m^2)", value=270.7267)


#center=[5.27719337, -3.98766093], zoom=14
m = geemap.Map(center=[5.27719337, -3.98766093], zoom=14)
m.add_basemap("HYBRID")

def maskL8sr(image):
    """
    Applique un masque pour éliminer les nuages et les ombres de nuages
    en utilisant la bande QA_PIXEL.
    Les bits 3 (ombre de nuage) et 5 (nuage) doivent être à 0.
    """
    qa = image.select('QA_PIXEL')
    cloudShadowBitMask = 1 << 3  # Bit 3 : ombre de nuage
    cloudsBitMask = 1 << 5       # Bit 5 : nuage
    mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
    return image.updateMask(mask)

# Charger la collection Landsat 9 Collection 2 Tier 1 Level 2
collection_2015 = (geemap.ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
              .filterDate("2015-01-01", "2015-12-31")
              .map(maskL8sr))

# Créer une image composite (médiane) sur l'ensemble de la collection
composite_image_2015 = collection_2015.median()

# Afficher les informations de l'image composite dans la console
#print(composite_image.getInfo())

# Paramètres de visualisation
visParams = {
    'min': 7000,
    'max': 15000,
    'bands': ['SR_B4', 'SR_B3', 'SR_B2']
}

# Charger la collection Landsat 9 Collection 2 Tier 1 Level 2
collection_2024 = (geemap.ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')
              .filterDate("2024-01-01", "2024-12-31")
              .map(maskL8sr))

# Créer une image composite (médiane) sur l'ensemble de la collection
composite_image_2024 = collection_2024.median()

image_2015 = geemap.ee_tile_layer(composite_image_2015, visParams, "Image 2015")

image_2024 = geemap.ee_tile_layer(composite_image_2024, visParams, "Image 2024")




# Centrer la carte sur l'image composite (le centre est défini automatiquement)
#m.addLayer(composite_image, visParams, 'Composite Image 2024')

m.split_map(left_layer=image_2015, right_layer="HYBRID")

remblais = "Remblais.shp"
remblais = geemap.shp_to_ee(remblais)
m.addLayer(remblais, {}, "remblais", shown=False)

m.add_text(text = "2015", fontsize= 30, fontcolor="red", bold=True, position = "bottomleft")


m.add_text(text = "2024", fontsize= 30, fontcolor="red", bold=True, position = "bottomright")

m.to_streamlit(height=500)

