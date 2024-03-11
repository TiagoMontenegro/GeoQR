import tkinter as tk
from tkinter import filedialog
import pandas as pd
import folium
from folium.plugins import AntPath
from PIL import Image, ImageTk


def generate_map():
    file_path = filedialog.askopenfilename(title="Selecione o arquivo CSV!", filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)  # Read the CSV file

        # Getting the coordinates from the third column
        lat_long = df.iloc[:, 2].str.split(",", expand=True)
        lat_long[0] = lat_long[0].astype(float)
        lat_long[1] = lat_long[1].astype(float)

        # Create a base map
        m = folium.Map(location=[-9.67791, -35.72371], zoom_start=50,max_zoom=18) # max zoom in max_zoom=18

        # Add satellite tile layer
        folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google Satellite', name='Google Satellite').add_to(m)

        # Add markers and line
        locations = []
        for index, row in lat_long.iterrows():
            locations.append([row[0], row[1]])
            folium.Marker(
                location=[row[0], row[1]],
                popup=f"Data: {df.iloc[index,0]}, Local: {df.iloc[index,1]}"
            ).add_to(m)
        ant_path = AntPath(locations, color='red', weight=5, dash_array=[10, 20], delay=800, reverse=False, dash_offset='0%', icon='arrow', icon_size=0.8, rotate=True, repeat=True, offset=10).add_to(m)

        # Ask user for file name and location
        save_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])

        if save_path:
            # Save the map
            m.save(save_path)

            # Notify the user that the map is saved
            status_label.config(text="Mapa criado com sucesso!\nPode fechar o aplicativo.")

# Create the main window
root = tk.Tk()
root.title("Gerador de Mapa do GeoQR")
root.geometry("720x480")
#image = Image.open("C:/Users/tiago_luis/Desktop/LogoEMPAT.png")

# fatch Image from server for the background app
imagem_servidor = r"S:\US - INSP\Aplicativo de Ronda (GeoQR)\Não deletar\LogoEMPAT.png"
imagem = Image.open(imagem_servidor)


# Setting background image  
background_photo = ImageTk.PhotoImage(imagem)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add a button to generate the map
generate_button = tk.Button(root, text="Selecione o arquivo", command=generate_map,font=("Arial", 16), width=20, height=2)
generate_button.pack(pady=20)

# Add a status label to display messages
status_label = tk.Label(root, text="", fg="green",font=("Arial", 45))
status_label.pack()


# Start the GUI event loop
root.mainloop()


# Está interação do codigo só seleciona um arquivo por vez,
# alem do que necessita que crie um nome para o arquivo HTML.