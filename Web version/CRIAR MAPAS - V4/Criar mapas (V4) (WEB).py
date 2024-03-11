from flask import Flask, render_template, request, send_file
import os
import pandas as pd
import folium
from folium.plugins import AntPath
import tempfile
import zipfile

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "arquivos[]" not in request.files:
        return "Nenhum arquivo enviado", 400

    files = request.files.getlist("arquivos[]")
    map_paths = []

    for file in files:
        df = pd.read_csv(file)
        lat_long = df.iloc[:, 2].str.split(",", expand=True)
        lat_long[0] = lat_long[0].astype(float)
        lat_long[1] = lat_long[1].astype(float)

        m = folium.Map(location=[-9.678815, -35.723539], zoom_start=50, max_zoom=18)
        folium.TileLayer(
            "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google Satellite",
            name="Google Satellite",
        ).add_to(m)

        locations = []
        for index, row in lat_long.iterrows():
            locations.append([row[0], row[1]])
            folium.Marker(
                location=[row[0], row[1]],
                popup=f"Data: {df.iloc[index, 0]}, Local: {df.iloc[index, 1]}",
            ).add_to(m)

        ant_path = AntPath(
            locations,
            color="red",
            weight=5,
            dash_array=[10, 20],
            delay=800,
            reverse=False,
            dash_offset="0%",
            icon="arrow",
            icon_size=0.8,
            rotate=True,
            repeat=True,
            offset=10,
        ).add_to(m)

        base_filename = os.path.splitext(file.filename)[0]
        save_path = os.path.join(tempfile.gettempdir(), f"{base_filename}.html")
        m.save(save_path)
        map_paths.append(save_path)

    zip_path = os.path.join(tempfile.gettempdir(), "mapas_criados.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for map_path in map_paths:
            zipf.write(map_path, os.path.basename(map_path))

    return send_file(zip_path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True)
