import pandas as pd
import numpy as np

# --- ثابت‌ها ---
g = 9.81  # m/s²
rho = 997  # kg/m³ (چگالی آب)
bar_to_Pa = 1e5  # 1 bar = 100000 Pa

# --- داده‌های دیتاست دوم ---
data_ds2 = {
    "Torque_Nm": [2.1, 2.0, 1.9, 1.7, 1.8, 1.7, 1.5, 1.5, 1.4, 1.2, 1.1, 1.0, 0.9],
    "Power_kW": [0.52, 0.50, 0.48, 0.46, 0.47, 0.45, 0.42, 0.42, 0.40, 0.38, 0.36, 0.33, 0.31],
    "Flow_Lmin": [254, 228, 197, 163, 177, 155, 127, 129, 99, 75, 50, 27, 2],
    "P_dis_bar": [0.06, 0.11, 0.18, 0.25, 0.21, 0.25, 0.29, 0.29, 0.32, 0.34, 0.35, 0.36, 0.36],
    "P_suc_bar": [-0.08, -0.07, -0.05, -0.04, -0.05, -0.04, -0.03, -0.03, -0.02, -0.02, -0.02, -0.01, -0.01]
}

df = pd.DataFrame(data_ds2)

# --- محاسبات ---
df["delta_P_Pa"] = (df["P_dis_bar"] - df["P_suc_bar"]) * bar_to_Pa
df["H"] = df["delta_P_Pa"] / (rho * g)
df["Q_m3s"] = df["Flow_Lmin"] / 1000 / 60
df["Q_m3h"] = df["Q_m3s"] * 3600
df["P_hyd_W"] = rho * g * df["Q_m3s"] * df["H"]
df["P_input_W"] = df["Power_kW"] * 1000
df["eta_hyd"] = df["P_hyd_W"] / df["P_input_W"]
df["eta_overall"] = df["eta_hyd"]

# نمایش جدول نهایی
print(df[["Flow_Lmin", "H", "P_hyd_W", "P_input_W", "eta_hyd", "eta_overall"]].round(3))