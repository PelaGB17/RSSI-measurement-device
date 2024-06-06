import numpy as np
import matplotlib.pyplot as plt
import argparse

def representa_medidas(data, config, ruta_guardado):
    # ------------------------- DATOS DE ENTRADA ------------------------------
    # Carga del fichero de medidas y de los datos de configuración de la medida.
    C = np.loadtxt(data)
    A = np.genfromtxt(config, comments="%", skip_header=6)
    pol = 'Circ'

    # ----------------------- FIN DATOS DE ENTRADA ----------------------------

    freq = A[0];        # frecuencia (MHz)

    allowed_freq = [2.3e3, 2.4e3, 5e3, 5.1e3]
    if freq not in allowed_freq:
        raise ValueError('Error. /n Frequency must be 2.3e3, 2.4e3, 5e3 or 5.1e3')

    G_t = A[1];     # ganancia en el USRP transmisor
    G_r = A[4];     # ganancia en el USRP receptor
    antenas = A[2]; # ganancia de las antenas transmisora y receptora (antenas iguales, con la misma ganancia)
    h_t = A[3];     # altura de la antena transmisora
    h_r = A[5];     # altura de la antena receptora


    # Atenuación de los cables coaxiales.
    # Cables negros cortos
    if freq == 2.3e3 or freq == 2.4e3:
        L_coax = 1.2;
    else:
        L_coax = 2.1;

    # Potencia transmitida por el USRP en función del valor configurado para
    # la ganancia, según datos recabados de la calibración.

    Pmed_1_2G3 = [-52.1, -42, -32, -21.9, -11.9, -1.8, 7.6];      # B210, 2.4 GHz
    Pmed_1_5G = [-53.8, -43.6, -33.6, -23.7, -13.7, -3.7, 6.1];   # B210, 5 GHz
    Pmed_2_2G3 = [-51.2, -41.1, -31, -20.9, -10.9, -1.0, 8.6];    # B200mini, 2.4 GHz
    Pmed_2_5G = [-54.3, -44.3, -34.3, -24.4, -14.4, -4.3, 5.7];   # B200mini, 5 GHz
    Ganancia_tx = list(range(20, 81, 10))

    for i in Ganancia_tx:
        if freq in [2.3e3, 2.4e3]:
            if G_t == i:
                col = Ganancia_tx.index(G_t)
                P_t = Pmed_2_2G3[col]
        else:
            if G_t == i:
                col = Ganancia_tx.index(G_t)
                P_t = Pmed_2_5G[col]

    # Ganancia de los amplificadores externos.
    ampli_externo = 0

    # Factor de calibración del dispositivo USRP (relación entre la medida del
    # USRP (dB) y la potencia recibida (dBm)), según datos recabados de la
    # calibración.

    Ganancia_rx = [
        [10.91, -5.89, -14.8, -26.30],
        [14.17, -0.23, -10.77, -18.02],
        [9.93, -7.09, -16.6, -26.05],
        [15.38, -0.25, -8.9, -17.5]
    ]

    if G_r == 0:
        if freq == 2.3e3 or freq == 2.4e3:
            cal_off = Ganancia_rx[2][0]
        else:
            cal_off = Ganancia_rx[3][0]
    elif G_r == 20:
        if freq == 2.3e3 or freq == 2.4e3:
            cal_off = Ganancia_rx[2][1]
        else:
            cal_off = Ganancia_rx[3][1]
    elif G_r == 30:
        if freq == 2.3e3 or freq == 2.4e3:
            cal_off = Ganancia_rx[2][2]
        else:
            cal_off = Ganancia_rx[3][2]
    else:
        if freq == 2.3e3 or freq == 2.4e3:
            cal_off = Ganancia_rx[2][3]
        else:
            cal_off = Ganancia_rx[3][3]

    # Representación de modelos y medidas.

    R = np.arange(0.5, 100.5, 0.5)  # distancia (metros)
    Lbf = 32.45 + 20 * np.log10(R * 1e-3) + 20 * np.log10(freq)                     # pérdidas en espacio libre
    Lb = 120 + 40 * np.log10(R * 1e-3) - 20 * np.log10(h_t) - 20 * np.log10(h_r)    # pérdidas en tierra plana
    P_r1 = P_t + 2 * antenas - 2 * L_coax - Lbf + ampli_externo                     # potencia recibida en espacio libre
    P_r2 = P_t + 2 * antenas - 2 * L_coax - Lb + ampli_externo                      # potencia recibida en tierra plana


    #  modelo 2 rayos ----------------------------------------------------------
    lambda_val = 3e8 / (freq * 1e6)  # Hz
    rho = -1

    H = 0  # altura del transmisor

    d1 = np.sqrt(R ** 2 + (H - h_t + h_r) ** 2)  # Camino recorrido por el rayo directo
    l1 = np.sqrt(R ** 2 + (H + h_t + h_r) ** 2)  # Camino recorrido por el rayo reflejado
    delta_phi_1 = 2 * np.pi * (l1 - d1) / lambda_val  # Diferencia de fase como consecuencia de la diferencia de caminos
    Lb_2rays = Lbf - 20 * np.log10(abs(1 + abs(rho) * np.exp(1j * np.angle(rho)) * np.exp(1j * delta_phi_1)))
    Pr_2rays = P_t + 2 * antenas - 2 * L_coax - Lb_2rays + ampli_externo


    index = np.where(P_r2 >= P_r1)[0][-1]
    PIRE = P_t + antenas - L_coax
    print("PIRE:",PIRE,"dBm")

    # Potencia medida
    dist_USRP = C[:, 1]
    P_in_USRP = C[:, 0] + cal_off

    # Representación de la potencia medida y comparación con los modelos
    plt.figure()
    plt.plot(R, P_r1, label="Free Space Propagation Model", linewidth=1.25, color=[0, 0.4470, 0.7410])
    plt.plot(R, Pr_2rays, label="Two-ray Model $//rho = -1$", linewidth=1.25, color=[0.9290, 0.6940, 0.1250])
    plt.plot(dist_USRP, P_in_USRP, '.', label="Measurements", markersize=15, color=[0.6350, 0.0780, 0.1840])
    plt.xlabel("Distance (m)")
    plt.ylabel("RSSI value (dBm)")

    plt.legend(loc='best')

    plt.title(f"Frequency: {freq * 1e-3} GHz; Pol: {pol}")
    plt.xlim([0, 70])
    plt.ylim([-100, -20])
    plt.grid(True)
    plt.show()
    plt.savefig(ruta_guardado)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Representa Medidas script.')
    parser.add_argument('-d', '--data', type=str, default='D:/OneDrive - Universidad de Oviedo/Clase/4_2/TFG/Archivos/All_Files/Medidas/17a_prueba/procesado.txt', help='Data file path')
    parser.add_argument('-c', '--config', type=str, default='D:/OneDrive - Universidad de Oviedo/Clase/4_2/TFG/Archivos/All_Files/Scripts/Herramientas/data_f24v.txt', help='Config file path')
    args = parser.parse_args()
    representa_medidas(args.data, args.config)
