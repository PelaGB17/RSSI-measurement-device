
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
import GPS as gps
import Main as main

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/rssidev/Desktop/Interface/build/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class FullScreenApp:
            
    def __init__(self, mainclass):    
        window = Tk()
        window.geometry("1920x1080")
        window.configure(bg = "#9CC795")
        self.mainclass = mainclass


        self.canvas = Canvas(
            window,
            bg = "#9CC795",
            height = 1080,
            width = 1920,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.im1 = PhotoImage(
            file=relative_to_assets("logo.png"))
        self.image_1 = self.canvas.create_image(
            205.0,
            82.0,
            image=self.im1
        )

        self.im2 = PhotoImage(
            file=relative_to_assets("rect1.png"))
        self.image_2 = self.canvas.create_image(
            335.0,
            600.0,
            image=self.im2
        )

        self.im3 = PhotoImage(
            file=relative_to_assets("rect2.png"))
        self.image_3 = self.canvas.create_image(
            1280.0,
            600.0,
            image=self.im3
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.stop,
            relief="flat"
        )
        self.button_1.place(
            x=1150.0,
            y=940.0,
            width=260.0,
            height=80.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.test,
            relief="flat"
        )
        button_2.place(
            x=350.0,
            y=940.0,
            width=260.0,
            height=80.0
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.inicio,
            relief="flat"
        )
        self.button_3.place(
            x=60.0,
            y=940.0,
            width=260.0,
            height=80.0
        )

        self.char = PhotoImage(
            file=relative_to_assets("char.png"))
        self.image_4 = self.canvas.create_image(
            335.0,
            270.0,
            image=self.char
        )

        self.image_5 = self.canvas.create_image(
            335.0,
            340.0,
            image=self.char
        )

        self.image_6 = self.canvas.create_image(
            335.0,
            410.0,
            image=self.char
        )

        self.image_7 = self.canvas.create_image(
            335.0,
            480.0,
            image=self.char
        )

        self.image_8 = self.canvas.create_image(
            335.0,
            550.0,
            image=self.char
        )

        self.image_9 = self.canvas.create_image(
            335.0,
            620.0,
            image=self.char
        )

        self.image_10 = self.canvas.create_image(
            335.0,
            690.0,
            image=self.char
        )

        self.image_11 = self.canvas.create_image(
            335.0,
            760.0,
            image=self.char
        )

        self.image_12 = self.canvas.create_image(
            335.0,
            830.0,
            image=self.char
        )

        self.image_13 = self.canvas.create_image(
            335.0,
            830.0,
            image=self.char
        )

        self.image_14 = self.canvas.create_image(
            335.0,
            900.0,
            image=self.char
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
            1210.0,
            170.0,
            anchor="nw",
            text="Datos:",
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

        self.entry_image = PhotoImage(
            file=relative_to_assets("entry.png"))
        
        self.entry_bg_10 = self.canvas.create_image(
            465.0,
            270.0,
            image=self.entry_image
        )
        self.entry_10 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_10.place(
            x=340.0,
            y=255.0,
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
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_9.place(
            x=340.0,
            y=325.0,
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
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_8.place(
            x=340.0,
            y=395.0,
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
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_7.place(
            x=340.0,
            y=465.0,
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
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_6.place(
            x=340.0,
            y=535.0,
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
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_5.place(
            x=340.0,
            y=605.0,
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
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_4.place(
            x=340.0,
            y=675.0,
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
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_3.place(
            x=340.0,
            y=745.0,
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
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_2.place(
            x=340.0,
            y=815.0,
            width=250.0,
            height=30.0
        )

        self.entry_bg_1 = self.canvas.create_image(
            465.0,
            900.0,
            image=self.entry_image
        )
        self.entry_1 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(
            x=340.0,
            y=885.0,
            width=250.0,
            height=30.0
        )

        self.res = PhotoImage(
            file=relative_to_assets("res.png"))
        self.image_15 = self.canvas.create_image(
            1280.0,
            340.0,
            image=self.res
        )

        self.canvas.create_text(
            732.0,
            320.0,
            anchor="nw",
            text="RSSI:",
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
            1198.0,
            320.0,
            anchor="nw",
            text="XX.XXX",
            tags = ("RSSI"),
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.image_16 = self.canvas.create_image(
            1280.0,
            490.0,
            image=self.res
        )

        self.canvas.create_text(
            727.0,
            470.0,
            anchor="nw",
            text="Lat:",
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
            1198.0,
            470.0,
            anchor="nw",
            text="XX.XXX",
            tags = ("latitude"),
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.image_17 = self.canvas.create_image(
            1280.0,
            642.0,
            image=self.res
        )

        self.canvas.create_text(
            727.0,
            620.0,
            anchor="nw",
            text="Lon:",
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
            1191.0,
            620.0,
            anchor="nw",
            tags = ("longitude"),
            text="-X.XXX",
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.image_18 = self.canvas.create_image(
            1280.0,
            790.0,
            image=self.res
        )

        self.canvas.create_text(
            726.0,
            770.0,
            anchor="nw",
            text="Alt:",
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
            1213.0,
            770.0,
            anchor="nw",
            tags = ("altitude"),
            text="XXX.X",
            fill="#FFEAEC",
            font=("Inter Bold", 40 * -1)
        )
        
        window.resizable(False, False)
        window.mainloop()

    def inicio(self):
        self.freq = float(self.entry_10.get())  #Frecuencia en GHz
        self.g_rx = int(self.entry_9.get())
        self.g_tx = int(self.entry_8.get())
        self.lat = float(self.entry_7.get())
        self.lon = float(self.entry_6.get())
        self.h_tx = float(self.entry_5.get())
        self.h_rx = float(self.entry_4.get())
        self.pres = float(self.entry_3.get())
        self.g_ant = int(self.entry_2.get())
        self.name = self.entry_1.get()
        self.freq_Hz=self.freq*1000000000
        self.freq_MHz=self.freq*1000
        self.mainclass.create_info_file(freq_MHz=self.freq_MHz, g_tx=self.g_tx, g_ant=self.g_ant, h_tx=self.h_tx, g_rx=self.g_rx ,h_rx=self.h_rx, n_val=self.name)
        self.mainclass.main(lat_val=self.lat, lon_val=self.lon, p_val=self.pres, f_val=self.freq, g_val=self.g_rx, n_val=self.name)

    def test(self):
        try:
            datos_test = gps.obtener_datos_gps()
            RSSI = self.mainclass.nivel_de_senal()
            self.set_longitude(str(datos_test['longitude'])+" º")
            self.set_latitude(str(datos_test['latitude'])+" º")
            alt = str(datos_test['altitude'])
            alt = alt.replace("(","")
            alt = alt.replace(")","")
            alt = alt.replace(",","")
            self.set_altitude(alt+" m")
            self.set_RSSI(str(RSSI)+"dBm")
        except Exception as e:
            print(e)
            self.set_longitude("ERR")
            self.set_latitude("ERR")
            self.set_altitude("ERR")
            self.set_RSSI("ERR")

    def stop(self):
        self.mainclass.status = False
    
    def set_RSSI(self, RSSI):
        item_id = self.canvas.find_withtag("RSSI")
        self.canvas.itemconfig(item_id, text=RSSI) 

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
