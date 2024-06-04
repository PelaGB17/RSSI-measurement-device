from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import GPS as gps
import Main as main


OUTPUT_PATH = Path(__file__).parent
print("Donde estás programando?")
print("1. TSK")
print("2. Portatil")
print("3. Raspberry")
ruta = input("Seleccione uno:")
if ruta == 1:
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\pelayo.garcia\Desktop\RSSI-measurement-device\Interface\build\assets\frame0")
elif ruta == 2:
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Vicente\Desktop\RSSI-measurement-device\Interface\build\assets\frame0")
elif ruta == 3:
    ASSETS_PATH = OUTPUT_PATH / Path(r"\home\pelayo\Desktop\RSSI-measurement-device\Interface\build\assets\frame0")
else:
    print("Error en la selección de dispositivo")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class FullScreenApp:

    def __init__(self):
        gps.inicializar_gps()

        self.window = Tk()

        self.window.geometry("1920x1080")
        self.window.configure(bg = "#9CC795")


        self.canvas = Canvas(
            self.window,
            bg = "#9CC795",
            height = 1080,
            width = 1920,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            205.0,
            82.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            335.0,
            600.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(
            1280.0,
            600.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets("image_4.png"))
        self.image_4 = self.canvas.create_image(
            1280.0,
            69.0,
            image=self.image_image_4
        )

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.inicio,
            relief="flat"
        )
        button_1.place(
            x=700.0,
            y=29.0,
            width=130.0,
            height=80.0
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.test,
            relief="flat"
        )
        button_2.place(
            x=205.0,
            y=940.0,
            width=260.0,
            height=80.0
        )

        self.image_char = PhotoImage(
            file=relative_to_assets("image_5.png"))
        
        self.char_1 = self.canvas.create_image(
            335.0,
            270.0,
            image=self.image_char
        )

        self.char_2 = self.canvas.create_image(
            335.0,
            340.0,
            image=self.image_char
        )

        self.char_3 = self.canvas.create_image(
            335.0,
            410.0,
            image=self.image_char
        )

        self.char_4 = self.canvas.create_image(
            335.0,
            480.0,
            image=self.image_char
        )

        self.char_5 = self.canvas.create_image(
            335.0,
            550.0,
            image=self.image_char
        )

        self.char_6 = self.canvas.create_image(
            335.0,
            620.0,
            image=self.image_char
        )
        
        self.char_7 = self.canvas.create_image(
            335.0,
            690.0,
            image=self.image_char
        )

        self.char_8 = self.canvas.create_image(
            335.0,
            760.0,
            image=self.image_char
        )

        self.char_9 = self.canvas.create_image(
            335.0,
            830.0,
            image=self.image_char
        )

        self.char_10 = self.canvas.create_image(
            335.0,
            900.0,
            image=self.image_char
        )

        self.canvas.create_text(
            209.0,
            170.0,
            anchor="nw",
            text="Configuración:",
            fill="#000000",
            font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
            1115.0,
            170.0,
            anchor="nw",
            text="Representación:",
            fill="#000000",
            font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
            80.0,
            888.0,
            anchor="nw",
            text="Nombre de la prueba",
            fill="#FFEAEC",
            font=("Inter Bold", 20 * -1)
        )

        self.canvas.create_text(
            80.0,
            818.0,
            anchor="nw",
            text="Ganancia antena (dB)",
            fill="#FFEAEC",
            font=("Inter Bold", 20 * -1)
        )

        self.canvas.create_text(
            80.0,
            748.0,
            anchor="nw",
            text="Presión nivel del mar",
            fill="#FFEAEC",
            font=("Inter Bold", 20 * -1)
        )

        self.canvas.create_text(
            80.0,
            678.0,
            anchor="nw",
            text="Altura receptor (m)",
            fill="#FFEAEC",
            font=("Inter Bold", 20 * -1)
        )

        self.canvas.create_text(
            80.0,
            608.0,
            anchor="nw",
            text="Altura transmisor (m)",
            fill="#FFEAEC",
            font=("Inter Bold", 20 * -1)
        )

        self.canvas.create_text(
            80.0,
            538.0,
            anchor="nw",
            text="Longitud antena (º)",
            fill="#FFEAEC",
            font=("Inter Bold", 20 * -1)
        )

        self.canvas.create_text(
            80.0,
            468.0,
            anchor="nw",
            text="Latitud antena (º)",
            fill="#FFEAEC",
            font=("Inter Bold", 20 * -1)
        )

        self.canvas.create_text(
            80.0,
            398.0,
            anchor="nw",
            text="Ganancia transmisor (dB)",
            fill="#FFEAEC",
            font=("Inter Bold", 20 * -1)
        )

        self.canvas.create_text(
            80.0,
            328.0,
            anchor="nw",
            text="Ganancia receptor (dB)",
            fill="#FFEAEC",
            font=("Inter Bold", 20 * -1)
        )

        self.canvas.create_text(
            80.0,
            258.0,
            anchor="nw",
            text="Frecuencia (GHz)",
            fill="#FFEAEC",
            font=("Inter Bold", 20 * -1)
        )

        self.image_test = PhotoImage(
            file=relative_to_assets("image_6.png"))
        self.test_bg = self.canvas.create_image(
            1347.0,
            69.0,
            image=self.image_test
        )

        self.entry_image = PhotoImage(
            file=relative_to_assets("entry.png"))
        self.entry_bg_1 = self.canvas.create_image(
            465.0,
            900.0,
            image=self.entry_image
        )
        self.entry_1 = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(
            x=340.0,
            y=885.0,
            width=250.0,
            height=30.0
        )

        self.entry_bg_2 = self.canvas.create_image(
            465.0,
            830.0,
            image=self.entry_image
        )
        self.entry_2 = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_2.place(
            x=340.0,
            y=815.0,
            width=250.0,
            height=30.0
        )

        self.entry_bg_3 = self.canvas.create_image(
            465.0,
            760.0,
            image=self.entry_image
        )
        self.entry_3 = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_3.place(
            x=340.0,
            y=745.0,
            width=250.0,
            height=30.0
        )

        self.entry_bg_4 = self.canvas.create_image(
            465.0,
            690.0,
            image=self.entry_image
        )
        self.entry_4 = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_4.place(
            x=340.0,
            y=675.0,
            width=250.0,
            height=30.0
        )

        self.entry_bg_5 = self.canvas.create_image(
            465.0,
            620.0,
            image=self.entry_image
        )
        self.entry_5 = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_5.place(
            x=340.0,
            y=605.0,
            width=250.0,
            height=30.0
        )

        self.entry_bg_6 = self.canvas.create_image(
            465.0,
            550.0,
            image=self.entry_image
        )
        self.entry_6 = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_6.place(
            x=340.0,
            y=535.0,
            width=250.0,
            height=30.0
        )

        self.entry_bg_7 = self.canvas.create_image(
            465.0,
            480.0,
            image=self.entry_image
        )
        self.entry_7 = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_7.place(
            x=340.0,
            y=465.0,
            width=250.0,
            height=30.0
        )

        self.entry_bg_8 = self.canvas.create_image(
            465.0,
            410.0,
            image=self.entry_image
        )
        self.entry_8 = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_8.place(
            x=340.0,
            y=395.0,
            width=250.0,
            height=30.0
        )

        self.entry_bg_9 = self.canvas.create_image(
            465.0,
            340.0,
            image=self.entry_image
        )
        self.entry_9 = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_9.place(
            x=340.0,
            y=325.0,
            width=250.0,
            height=30.0
        )

        self.entry_bg_10 = self.canvas.create_image(
            465.0,
            270.0,
            image=self.entry_image
        )
        self.entry_10 = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_10.place(
            x=340.0,
            y=255.0,
            width=250.0,
            height=30.0
        )

        self.canvas.create_text(
            867.0,
            49.0,
            anchor="nw",
            text="Lat:",
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
            967.0,
            49.0,
            anchor="nw",
            text="XX.XXX",
            tags = ("latitude"),
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
            1119.0,
            49.0,
            anchor="nw",
            text="º",
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
            1188.0,
            49.0,
            anchor="nw",
            text="Lon:",
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
            1288.0,
            49.0,
            anchor="nw",
            text="-X.XXX",
            tags = ("longitude"),
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
            1428.0,
            49.0,
            anchor="nw",
            text="º",
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
            1525.0,
            49.0,
            anchor="nw",
            text="Alt:",
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
            1625.0,
            49.0,
            anchor="nw",
            text="XXX.X",
            tags = ("altitude"),
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
            1755.0,
            49.0,
            anchor="nw",
            text="m",
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )
        self.window.resizable(False, False)
        self.window.mainloop()

    def inicio(self):
        self.freq = self.entry_1.get()  #Frecuencia en GHz
        self.g_rx = self.entry_2.get()
        self.g_tx = self.entry_3.get()
        self.lat = self.entry_4.get()
        self.lon = self.entry_5.get()
        self.h_tx = self.entry_6.get()
        self.h_rx = self.entry_7.get()
        self.pres = self.entry_8.get()
        self.g_ant = self.entry_9.get()
        self.name = self.entry_10.get()
        self.freq_Hz=float(self.freq*10**9)
        self.freq_MHz=float(self.freq*10**3)
        main.create_info_file(freq_MHz=self.freq, g_tx=self.g_tx, g_ant=self.g_ant, h_tx=self.h_tx, g_rx=self.g_rx ,h_rx=self.h_rx)
        main.main(lat_val=self.lat, lon_val=self.lon, p_val=self.pres, f_val=self.freq, g_val=self.g_rx, n_val=self.name)

    def test(self):
        try:
            datos_test = gps.obtener_datos_gps()
            self.set_longitude(datos_test['longitude'])
            self.set_latitude(datos_test['latitude'])
            self.set_altitude(datos_test['altitude'])
        except Exception as e:
            print(e)
            self.set_longitude("ERR")
            self.set_latitude("ERR")
            self.set_altitude("ERR")

    def set_longitude(self, longitude):
        item_id = self.canvas.find_withtag("longitude")
        self.canvas.itemconfig(item_id, text=longitude) 

    def set_latitude(self, latitude):
        item_id = self.canvas.find_withtag("latitude")
        self.canvas.itemconfig(item_id, text=latitude) 

    def set_altitude(self, altitude):
        item_id = self.canvas.find_withtag("altitude")
        self.canvas.itemconfig(item_id, text=altitude) 
    
if __name__ == '__main__':
    m=FullScreenApp()
