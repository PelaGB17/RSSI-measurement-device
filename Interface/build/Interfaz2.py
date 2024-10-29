from pathlib import Path
import GPS as gps
import Main2 as main
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, StringVar, DoubleVar, IntVar

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/rssidev/Desktop/Interface/build/assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class FullScreenApp:
    def __init__(self, mainclass):
        self.mainclass = mainclass
        self.window = Tk()
        self.window.geometry("1920x1080")
        self.window.configure(bg="#9CC795")
        self.setup_canvas()
        self.setup_images()
        self.setup_buttons()
        self.setup_texts()
        self.setup_entries()
        self.window.resizable(False, False)
        self.window.mainloop()

    def setup_canvas(self):
        self.canvas = Canvas(
            self.window,
            bg="#9CC795",
            height=1080,
            width=1920,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

    def setup_images(self):
        self.im1 = PhotoImage(file=relative_to_assets("logo.png"))
        self.canvas.create_image(205.0, 82.0, image=self.im1)

        self.im2 = PhotoImage(file=relative_to_assets("rect1.png"))
        self.canvas.create_image(335.0, 600.0, image=self.im2)

        self.im3 = PhotoImage(file=relative_to_assets("rect2.png"))
        self.canvas.create_image(1280.0, 600.0, image=self.im3)

        self.char = PhotoImage(file=relative_to_assets("char.png"))
        for y in range(270, 930, 70):
            self.canvas.create_image(335.0, y, image=self.char)

        self.res = PhotoImage(file=relative_to_assets("res.png"))
        self.canvas.create_image(1280.0, 340.0, image=self.res)
        self.canvas.create_image(1280.0, 490.0, image=self.res)
        self.canvas.create_image(1280.0, 642.0, image=self.res)
        self.canvas.create_image(1280.0, 790.0, image=self.res)

    def setup_buttons(self):
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.stop,
            relief="flat"
        ).place(x=1150.0, y=940.0, width=260.0, height=80.0)

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.test,
            relief="flat"
        ).place(x=350.0, y=940.0, width=260.0, height=80.0)

        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.inicio,
            relief="flat"
        ).place(x=60.0, y=940.0, width=260.0, height=80.0)

    def setup_texts(self):
        self.canvas.create_text(
            209.0, 170.0, anchor="nw",
            text="Configuración:",
            fill="#000000",
            font=("Inter Bold", 40 * -1)
        )
        self.canvas.create_text(
            1210.0, 170.0, anchor="nw",
            text="Datos:",
            fill="#000000",
            font=("Inter Bold", 40 * -1)
        )
        config_labels = [
            ("Frecuencia (GHz)", 258.0), ("Ganancia receptor (dB)", 328.0), 
            ("Ganancia transmisor (dB)", 398.0), ("Latitud antena (º)", 468.0), 
            ("Longitud antena (º)", 538.0), ("Altura transmisor (m)", 608.0), 
            ("Altura receptor (m)", 678.0), ("Presión nivel del mar", 748.0), 
            ("Ganancia antena (dB)", 818.0), ("Nombre de la prueba", 888.0)
        ]
        for text, y in config_labels:
            self.canvas.create_text(80.0, y, anchor="nw", text=text, fill="#FFEAEC", font=("Inter Bold", 20 * -1))
        
        self.canvas.create_text(732.0, 320.0, anchor="nw", text="RSSI:", fill="#FFEAEC", font=("Inter Bold", 40 * -1))
        self.canvas.create_text(727.0, 470.0, anchor="nw", text="Lat:", fill="#FFEAEC", font=("Inter Bold", 40 * -1))
        self.canvas.create_text(727.0, 620.0, anchor="nw", text="Lon:", fill="#FFEAEC", font=("Inter Bold", 40 * -1))
        self.canvas.create_text(726.0, 770.0, anchor="nw", text="Alt:", fill="#FFEAEC", font=("Inter Bold", 40 * -1))

        self.rssi_text = self.canvas.create_text(1198.0, 320.0, anchor="nw", text="XX.XXX", tags="RSSI", fill="#FFEAEC", font=("Inter Bold", 40 * -1))
        self.latitude_text = self.canvas.create_text(1198.0, 470.0, anchor="nw", text="XX.XXX", tags="latitude", fill="#FFEAEC", font=("Inter Bold", 40 * -1))
        self.longitude_text = self.canvas.create_text(1191.0, 620.0, anchor="nw", text="-X.XXX", tags="longitude", fill="#FFEAEC", font=("Inter Bold", 40 * -1))
        self.altitude_text = self.canvas.create_text(1213.0, 770.0, anchor="nw", text="XXX.X", tags="altitude", fill="#FFEAEC", font=("Inter Bold", 40 * -1))

    def setup_entries(self):
        self.entry_image = PhotoImage(file=relative_to_assets("entry.png"))
        entries_positions = [
            (270.0, 255.0), (340.0, 325.0), (410.0, 395.0), (480.0, 465.0),
            (550.0, 535.0), (620.0, 605.0), (690.0, 675.0), (760.0, 745.0),
            (830.0, 815.0), (900.0, 885.0)
        ]
        self.entries = []
        for y, entry_y in entries_positions:
            self.canvas.create_image(465.0, y, image=self.entry_image)
            entry = Entry(self.window, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
            entry.place(x=340.0, y=entry_y, width=250.0, height=30.0)
            self.entries.append(entry)

    def inicio(self):
        try:
            self.freq = float(self.entries[0].get())  # Frecuencia en GHz
            self.g_rx = int(self.entries[1].get())
            self.g_tx = int(self.entries[2].get())
            self.lat = float(self.entries[3].get())
            self.lon = float(self.entries[4].get())
            self.h_tx = float(self.entries[5].get())
            self.h_rx = float(self.entries[6].get())
            self.pres = float(self.entries[7].get())
            self.g_ant = int(self.entries[8].get())
            self.name = self.entries[9].get()
            self.freq_Hz = self.freq * 1e9
            self.freq_MHz = self.freq * 1e3
            config = [self.lat, self.lon, self.pres, self.freq, self.g_rx, self.name]
            self.mainclass.create_info_file(freq_MHz=self.freq_MHz, g_tx=self.g_tx, g_ant=self.g_ant, h_tx=self.h_tx, g_rx=self.g_rx ,h_rx=self.h_rx, n_val=self.name)
            self.mainclass.main(config = config)
            print("Archivos creados")
        except Exception as e:
            print("Error al crear archivos:", e)

    def test(self):
        gps.getGPS()
        self.rssi = self.mainclass.read_RSSI()
        self.lat, self.lon, self.alt = gps.latitude(), gps.longitude(), gps.altitude()
        self.canvas.itemconfig(self.rssi_text, text=f"{self.rssi:.3f}")
        self.canvas.itemconfig(self.latitude_text, text=f"{self.lat:.3f}")
        self.canvas.itemconfig(self.longitude_text, text=f"{self.lon:.3f}")
        self.canvas.itemconfig(self.altitude_text, text=f"{self.alt:.1f}")
        print("Lat:", self.lat, "Lon:", self.lon, "Alt:", self.alt, "RSSI:", self.rssi)

    def stop(self):
        self.mainclass.stop_main_loop()
        print("Parar la prueba")

if __name__ == "__main__":
    app = FullScreenApp(main)
