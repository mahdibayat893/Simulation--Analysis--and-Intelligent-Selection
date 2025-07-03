import pandas as pd
import numpy as np

g = 9.81
rho = 997
psi_to_pa = 6894.76
V_line = 460
PF = 0.875
eta_motor = 0.90
pipe_diameter_inch = 6
pipe_diameter_m = pipe_diameter_inch * 0.0254
pipe_area = np.pi * (pipe_diameter_m / 2) ** 2

data = {
    "Q_gpm": [0, 500, 800, 1000, 1100, 1200, 1400, 1500],
    "P_suc_psi": [0.65, 0.25, -0.35, -0.92, -1.24, -1.62, -2.42, -2.89],
    "P_dis_psi": [53.3, 48.3, 42.3, 36.9, 33.0, 27.8, 15.3, 7.3],
    "I_amp": [18.0, 26.2, 31.0, 33.9, 35.2, 36.3, 38.0, 39.0]
}
df = pd.DataFrame(data)

df["P_suc_Pa"] = df["P_suc_psi"] * psi_to_pa
df["P_dis_Pa"] = df["P_dis_psi"] * psi_to_pa

df["H"] = (df["P_dis_Pa"] - df["P_suc_Pa"]) / (rho * g)

df["Q_m3s"] = df["Q_gpm"] * 0.00378541 / 60

df["P_hyd_W"] = rho * g * df["Q_m3s"] * df["H"]

df["P_input_W"] = (np.sqrt(3) * V_line * df["I_amp"] * PF) / eta_motor

df["eta_overall"] = df["P_hyd_W"] / df["P_input_W"]

df[["Q_gpm", "H", "P_hyd_W", "P_input_W", "eta_overall"]].round(3)
