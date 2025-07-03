import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

# --- تعریف متغیر مستقل ---
x = df["Q_m3h"].values
x_fit = np.linspace(min(x), max(x), 100)

# --- تابع کمکی برای رسم هر نمودار ---
def plot_fit(y_data, ylabel, color, label, title):
    p = Polynomial.fit(x, y_data, deg=2)
    y_fit = p(x_fit)
    plt.figure(figsize=(8, 5))
    plt.plot(x, y_data, 'o', color=color, label="Measured")
    plt.plot(x_fit, y_fit, '-', color=color, label="Fitted Curve")
    plt.xlabel("Flow rate (m³/h)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return p.convert().coef.round(4)

# --- 1. هد پمپ ---
coef_H = plot_fit(df["H"].values, "Head (m)", "blue", "Head", "Head vs Flow Rate")

# --- 2. توان هیدرولیکی ---
coef_P = plot_fit(df["P_hyd_W"].values / 1000, "Hydraulic Power (kW)", "green", "Power", "Hydraulic Power vs Flow Rate")

# --- 3. بازده کلی ---
coef_eta = plot_fit(df["eta_overall"].values * 100, "Efficiency (%)", "red", "Efficiency", "Efficiency vs Flow Rate")

# --- 4. سرعت مخصوص ---
N_rpm = 1100
df["Ns"] = N_rpm * np.sqrt(df["Q_m3s"]) / (df["H"] ** 0.75)
coef_Ns = plot_fit(df["Ns"].values, "Specific Speed (Ns)", "purple", "Ns", "Specific Speed vs Flow Rate")

# --- نمایش ضرایب نهایی ---
print("Head Coefficients:", coef_H)
print("Power Coefficients:", coef_P)
print("Efficiency Coefficients:", coef_eta)
print("Specific Speed Coefficients:", coef_Ns)