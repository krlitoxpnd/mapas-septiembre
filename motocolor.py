import pandas as pd
import folium
import os

# 1. Configuración del nombre del archivo
archivo = 'motochorros.xlsx' 

if not os.path.exists(archivo):
    archivo = 'motochorros.csv'

if not os.path.exists(archivo):
    print("Error: No encuentro el archivo 'motochorros' en la carpeta.")
else:
    # 2. Leer los datos
    if archivo.endswith('.csv'):
        df = pd.read_csv(archivo, encoding='latin-1', sep=None, engine='python')
    else:
        df = pd.read_excel(archivo)

    # 3. Diccionario de colores por Comisaría
    # Puedes cambiar los colores a tu gusto
    colores_comisarias = {
        'PRIMERA': 'red',
        'SEGUNDA': 'blue',
        'TERCERA': 'green',
        'CUARTA': 'purple',
        'QUINTA': 'orange',
        'SEXTA': 'darkred',
        'SEPTIMA': 'darkblue',
        'OCTAVA': 'cadetblue',
        'NONA': 'darkgreen',
        'DECIMA': 'pink',
        'ONCEAVA': 'beige',
        'DOCEAVA': 'black',
        'DECIMOTERCERA': 'lightgray',
        'DECIMOCUARTA': 'darkpurple',
        'DECIMOQUINTA': 'lightblue',
        'DECIMOSEXTA': 'lightgreen'
    }

    # 4. Función para corregir coordenadas
    def corregir_puntos(valor):
        try:
            v_str = str(int(valor))
            if len(v_str) > 5:
                return float(v_str[:3] + '.' + v_str[3:])
            return float(valor)
        except:
            return None

    df['lat_ok'] = df['latitud'].apply(corregir_puntos)
    df['lon_ok'] = df['longitud'].apply(corregir_puntos)
    df = df.dropna(subset=['lat_ok', 'lon_ok'])

    # 5. Crear el mapa
    mapa = folium.Map(location=[-38.0055, -57.5542], zoom_start=12)

    # 6. BUCLE con distinción de colores
    for index, row in df.iterrows():
        nombre_comisaria = str(row['COMISARIA ']).upper()
        
        # Lógica para encontrar qué color corresponde
        color_punto = 'gray' # Color por defecto
        for clave, color in colores_comisarias.items():
            if clave in nombre_comisaria:
                color_punto = color
                break

        texto = f"""
        <div style="font-family: sans-serif; font-size: 11px; width: 180px;">
            <b>Comisaría:</b> {row['COMISARIA ']}<br>
            <b>Fecha:</b> {row['FECHA']}<br>
            <b>Delito:</b> {row['tipodelito']}<br>
            <b>Lugar:</b> {row['CALLE']} {row['Nro']}
        </div>
        """
        
        folium.CircleMarker(
            location=[row['lat_ok'], row['lon_ok']],
            radius=6,
            color=color_punto,     # Color del borde según comisaría
            fill=True,
            fill_color=color_punto, # Color de relleno según comisaría
            fill_opacity=0.7,
            popup=folium.Popup(texto, max_width=250),
            tooltip=f"Jurisdicción: {row['COMISARIA ']}"
        ).add_to(mapa)

    # 7. Guardar el archivo
    mapa.save('mapa_comisarias_motochorros.html')
    print("¡Éxito! Mapa generado: 'mapa_comisarias_motochorros.html' con distinción por colores.")