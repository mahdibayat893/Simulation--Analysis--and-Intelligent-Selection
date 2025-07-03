# کد کامل برای محاسبه و برازش 4 پارامتر عملکردی پمپ سانتریفیوژ در سرعت 1750 rpm

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

# --- مشخصات ثابت ---
g = 9.81
rho = 997
psi_to_pa = 6894.76
V_line = 460
PF = 0.875
eta_motor = 0.90
N_rpm = 1750

# --- داده‌های اولیه ---
data = {
    "Q_gpm": [0, 500, 800, 1000, 1100, 1200, 1400, 1500],
    "P_suc_psi": [0.65, 0.25, -0.35, -0.92, -1.24, -1.62, -2.42, -2.89],
    "P_dis_psi": [53.3, 48.3, 42.3, 36.9, 33.0, 27.8, 15.3, 7.3],
    "I_amp": [18.0, 26.2, 31.0, 33.9, 35.2, 36.3, 38.0, 39.0]
}
df = pd.DataFrame(data)

# --- محاسبات ---
df["P_suc_Pa"] = df["P_suc_psi"] * psi_to_pa
df["P_dis_Pa"] = df["P_dis_psi"] * psi_to_pa
df["H"] = (df["P_dis_Pa"] - df["P_suc_Pa"]) / (rho * g)
df["Q_m3s"] = df["Q_gpm"] * 0.00378541 / 60
df["Q_m3h"] = df["Q_m3s"] * 3600
df["P_hyd_W"] = rho * g * df["Q_m3s"] * df["H"]
df["P_input_W"] = (np.sqrt(3) * V_line * df["I_amp"] * PF) / eta_motor
df["eta_overall"] = df["P_hyd_W"] / df["P_input_W"]
df["Ns"] = N_rpm * np.sqrt(df["Q_m3s"]) / (df["H"] ** 0.75)

# --- تعریف متغیرهای مستقل و نقاط برازش ---
x = df["Q_m3h"].values
x_fit = np.linspace(min(x), max(x), 100)

# --- 1. Head ---
y_H = df["H"].values
p_H = Polynomial.fit(x, y_H, deg=2)
y_fit_H = p_H(x_fit)

plt.figure(figsize=(8, 5))
plt.plot(x, y_H, 'bo', label='Measured Head')
plt.plot(x_fit, y_fit_H, 'b-', label='Fitted Curve')
plt.xlabel("Flow rate (m³/h)")
plt.ylabel("Head (m)")
plt.title("Head vs Flow Rate with Curve Fit")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# --- 2. Hydraulic Power ---
y_P = df["P_hyd_W"].values / 1000
p_P = Polynomial.fit(x, y_P, deg=2)
y_fit_P = p_P(x_fit)

plt.figure(figsize=(8, 5))
plt.plot(x, y_P, 'go', label='Measured Power')
plt.plot(x_fit, y_fit_P, 'g-', label='Fitted Curve')
plt.xlabel("Flow rate (m³/h)")
plt.ylabel("Hydraulic Power (kW)")
plt.title("Hydraulic Power vs Flow Rate with Curve Fit")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# --- 3. Efficiency ---
y_eta = df["eta_overall"].values * 100
p_eta = Polynomial.fit(x, y_eta, deg=2)
y_fit_eta = p_eta(x_fit)

plt.figure(figsize=(8, 5))
plt.plot(x, y_eta, 'ro', label='Measured Efficiency')
plt.plot(x_fit, y_fit_eta, 'r-', label='Fitted Curve')
plt.xlabel("Flow rate (m³/h)")
plt.ylabel("Efficiency (%)")
plt.title("Efficiency vs Flow Rate with Curve Fit")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# --- 4. Specific Speed ---
y_Ns = df["Ns"].values
p_Ns = Polynomial.fit(x, y_Ns, deg=2)
y_fit_Ns = p_Ns(x_fit)

plt.figure(figsize=(8, 5))
plt.plot(x, y_Ns, 'mo', label='Measured Ns')
plt.plot(x_fit, y_fit_Ns, 'm-', label='Fitted Curve')
plt.xlabel("Flow rate (m³/h)")
plt.ylabel("Specific Speed (Ns)")
plt.title("Specific Speed vs Flow Rate with Curve Fit")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# --- خروجی ضرایب ---
{
    "Head Coefficients": p_H.convert().coef.round(4),
    "Power Coefficients": p_P.convert().coef.round(4),
    "Efficiency Coefficients": p_eta.convert().coef.round(4),
    "Specific Speed Coefficients": p_Ns.convert().coef.round(4)
}
