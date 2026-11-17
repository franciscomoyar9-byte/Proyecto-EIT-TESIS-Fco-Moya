

import pandas as pd
datos = pd.read_csv(r"C:\Users\56940\EIT_TESISUI\ProcessedData_Subject03.csv")
print(datos.head())
print(datos.columns.tolist())
import matplotlib.pyplot as plt
#grafico curva presiones
plt.plot(datos["Time [s]"], datos["Pressure [cmH2O]"])
plt.xlabel("Tiempo (s)")
plt.ylabel("Presión (cmH2O)")
plt.title("Presión durante el registro")
plt.show()
#grafico areacion
plt.figure()
plt.plot(datos["Time (Aeration Data)_[s]"], datos["Global Aeration"])
plt.xlabel("Tiempo (s)")
plt.ylabel("Global Aeration")
plt.title("Aeración pulmonar global")
plt.show()
#ver si areacion cambia con presion
plt.figure()
plt.scatter(datos["Pressure [cmH2O]"], datos["Global Aeration"])
plt.xlabel("Presión (cmH2O)")
plt.ylabel("Global Aeration")
plt.title("Presión vs. aeración pulmonar")
plt.show()
print("Número de registros:", len(datos))
#continuacion analisis de datros
print("Resumen de variables:")
print(datos[[
    "Pressure [cmH2O]",
    "Flow [L/s]",
    "V_tidal [L]",
    "Global Aeration"
#HISTOGRAMA DE AIREACION GLOBAL
]].describe())
plt.figure()
plt.hist(datos["Global Aeration"].dropna(), bins=50)
plt.xlabel("Aeración pulmonar global")
plt.ylabel("Frecuencia")
plt.title("Distribución de la aeración pulmonar global")
plt.show()
#analisis de 0 en aireacion 
aeracion = datos["Global Aeration"]
print("Total de registros:", len(aeracion))
print("Registros iguales a cero:", (aeracion == 0).sum())
print("Porcentaje de ceros:", (aeracion == 0).mean() * 100)
print("Registros negativos:", (aeracion < 0).sum())
print("Valores faltantes:", aeracion.isna().sum())
#grafico de aireacion global a traves del tiempo
plt.figure(figsize=(12, 5))
plt.plot(datos["Time (Aeration Data)_[s]"],datos["Global Aeration"])
plt.xlabel("Tiempo (s)")
plt.ylabel("Aeración global")
plt.title("Aeración global durante todo el registro")
plt.grid(True)
plt.show()
#Analisis tiempo 
print("Tiempo de aeración:")
print(datos["Time (Aeration Data)_[s]"].describe())
columnas = ["Time (Aeration Data)_[s]", "Global Aeration"]
print("\nPrimeros 10 registros:")
print(datos[columnas].head(10))
print("\nÚltimos 10 registros:")
print(datos[columnas].tail(10))
#filas con tiempo y aireacion igual a 0
tiempo = datos["Time (Aeration Data)_[s]"] 
aeracion = datos["Global Aeration"] 
print("Tiempo igual a cero:", (tiempo == 0).sum()) 
print("Aeración igual a cero:", (aeracion == 0).sum()) 
print("Ambos iguales a cero:", ((tiempo == 0) & (aeracion == 0)).sum()) 
print("Tiempo distinto de cero:", (tiempo != 0).sum()) 
# Copia que conserve las filas donde el tiempo de aeración es distinto de cero para comparar dimensiones 
datos_aeracion = datos[datos["Time (Aeration Data)_[s]"] != 0].copy() 
print("Filas originales:", len(datos)) 
print("Filas con tiempo válido:", len(datos_aeracion)) 
columnas = ["Time (Aeration Data)_[s]", "Global Aeration"] 
print("\nPrimeros registros:") 
print(datos_aeracion[columnas].head()) 
print("\nÚltimos registros:") 
print(datos_aeracion[columnas].tail()) 
#nueva matriz de datos con tiempos sobre 0 
datos_eit = datos[datos["Time (Aeration Data)_[s]"] > 0].copy()
print("Registros EIT válidos:", len(datos_eit))
print("Tiempo inicial:", datos_eit["Time (Aeration Data)_[s]"].min())
print("Tiempo final:", datos_eit["Time (Aeration Data)_[s]"].max())
print("Aeración mínima:", datos_eit["Global Aeration"].min())
print("Aeración máxima:", datos_eit["Global Aeration"].max())
#nuevo grafico de aireacion global 
plt.figure(figsize=(12, 5))
plt.plot(
    datos_eit["Time (Aeration Data)_[s]"],
    datos_eit["Global Aeration"]
)
plt.xlabel("Tiempo (s)")
plt.ylabel("Aeración global")
plt.title("Señal EIT válida durante el registro")
plt.grid(True)
plt.tight_layout()
plt.show()
#cuantificacion de aireacion 
print("Estadísticas de la aeración EIT válida:")
print(datos_eit["Global Aeration"].describe())
print(datos_eit["Global Aeration"].describe())
import matplotlib.pyplot as plt
import pandas as pd
# 1. Cargar el archivo CSV
ruta_archivo = r"C:\Users\56940\EIT_TESISUI\ProcessedData_Subject03.csv"
datos = pd.read_csv(ruta_archivo)
# 2. Filtrar los datos para conservar solo aquellos con tiempo mayor a 0
eit = datos[datos["Time (Aeration Data)_[s]"] > 0].copy()
# 3. Configurar y generar la gráfica
plt.figure(figsize=(12, 5))
plt.plot(
    eit["Time (Aeration Data)_[s]"],
    eit["Global Aeration"],
    color="tab:blue",
    linewidth=1.5,)
# 4. Personalizar ejes, etiquetas y diseño
plt.xlim(100, 110)
plt.xlabel("Tiempo (s)", fontsize=12)
plt.ylabel("Aeración global", fontsize=12)
plt.title("Morfología de la señal EIT: 10 segundos", fontsize=14, pad=10)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
# 5. Mostrar la visualización
plt.show()
#Suavizado con ventana movil de 30 segundos
eit["Aeracion_suavizada"] = eit["Global Aeration"].rolling(1500).mean()
plt.figure(figsize=(12, 5))
plt.plot(eit["Time (Aeration Data)_[s]"], eit["Global Aeration"], alpha=0.4)
plt.plot(eit["Time (Aeration Data)_[s]"], eit["Aeracion_suavizada"])
plt.xlim(100, 160)
plt.title("Señal EIT original y suavizada (ventana de 30 s)")
plt.grid()
plt.show()
#caracterizacion del sujeto y data frame
a = eit["Global Aeration"]
caracteristicas = pd.DataFrame([{
    "Sujeto": "03",
    "Media": a.mean(),
    "Desviacion_estandar": a.std(),
    "Minimo": a.min(),
    "Maximo": a.max(),
    "Amplitud": a.max() - a.min()
}])
print(caracteristicas)
caracteristicas.to_csv("caracteristicas_sujeto03.csv", index=False)
#Tendencias generales de aireacion durante el registro
from scipy.stats import linregress
t = eit["Time (Aeration Data)_[s]"]
a = eit["Global Aeration"]
ajuste = linregress(t, a)
print("Pendiente temporal:", ajuste.slope)
print("R²:", ajuste.rvalue**2)
#Incorporacion de la pendiente a la tabla
from scipy.stats import linregress
t = eit["Time (Aeration Data)_[s]"]
a = eit["Global Aeration"]
ajuste = linregress(t, a)
caracteristicas = pd.DataFrame([{
    "Sujeto": "03",
    "Media": a.mean(),
    "Desviacion_estandar": a.std(),
    "Minimo": a.min(),
    "Maximo": a.max(),
    "Amplitud": a.max() - a.min(),
    "Pendiente": ajuste.slope,
    "R2": ajuste.rvalue**2}])
print(caracteristicas)
caracteristicas.to_csv("caracteristicas_sujeto03.csv", index=False)
#deteccion de ciclos
from scipy.signal import find_peaks
s = eit[(eit["Time (Aeration Data)_[s]"] >= 100) &
        (eit["Time (Aeration Data)_[s]"] <= 110)]

p, _ = find_peaks(s["Global Aeration"], distance=75, prominence=1000)
plt.plot(s["Time (Aeration Data)_[s]"], s["Global Aeration"])
plt.plot(s["Time (Aeration Data)_[s]"].iloc[p], s["Global Aeration"].iloc[p], "ro")
plt.grid()
plt.show()
print("Picos detectados:", len(p))
#FRECUENCIA de ciclos detectados y variabilidad
if len(p) > 1:
    tiempos = s["Time (Aeration Data)_[s]"].iloc[p].to_numpy()
    intervalos = tiempos[1:] - tiempos[:-1]
    print("Intervalos entre picos (s):", intervalos)
    print("Frecuencia estimada (ciclos/min):", 60 / intervalos.mean())
    print("Variabilidad de intervalos (s):", intervalos.std())
#Comparar la señal de aeración global con el flujo respiratorio en el mismo segmento (100–110 s).
s = datos[(datos["Time [s]"] >= 100) &
          (datos["Time [s]"] <= 110)]
plt.figure(figsize=(12, 5))
plt.plot(s["Time [s]"], s["Flow [L/s]"])
plt.axhline(0, color="black", linewidth=0.8)
plt.xlabel("Tiempo (s)")
plt.ylabel("Flujo (L/s)")
plt.title("Flujo respiratorio entre 100 y 110 s")
plt.grid()
plt.show()
#superponer la señal de flujo y la aeración global en dos gráficos alineados temporalmente. Como tienen escalas y frecuencias de muestreo diferentes
s = datos[(datos["Time [s]"] >= 100) & (datos["Time [s]"] <= 110)]
e = eit[(eit["Time (Aeration Data)_[s]"] >= 100) & (eit["Time (Aeration Data)_[s]"] <= 110)]
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(10, 6))
ax[0].plot(s["Time [s]"], s["Flow [L/s]"])
ax[1].plot(e["Time (Aeration Data)_[s]"], e["Global Aeration"])
ax[0].set_ylabel("Flujo (L/s)")
ax[1].set_ylabel("Aeración global")
ax[1].set_xlabel("Tiempo (s)")
plt.tight_layout()
plt.show()

from scipy.signal import butter, sosfiltfilt
import matplotlib.pyplot as plt
# 1. Extraer las señales
tiempo = eit["Time (Aeration Data)_[s]"].to_numpy()
aeracion = eit["Global Aeration"].to_numpy()
# 2. Aplicar filtro pasa-bajos
filtro = butter(4, 20, fs=50, btype="lowpass", output="sos")
aeracion_filtrada = sosfiltfilt(filtro, aeracion)
# 3. Seleccionar el intervalo de 100 a 110 segundos
intervalo = (tiempo >= 100) & (tiempo <= 110)
# 4. Graficar la comparación
plt.plot(tiempo[intervalo], aeracion[intervalo], label="Original")
plt.plot(tiempo[intervalo], aeracion_filtrada[intervalo], label="Filtrada")
plt.xlabel("Tiempo (s)")
plt.ylabel("Aeración global")
plt.title("Comparación de señales")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
#FILTRO 5 Hz
from scipy.signal import butter, sosfiltfilt
import matplotlib.pyplot as plt
tiempo = eit["Time (Aeration Data)_[s]"].to_numpy()
senal = eit["Global Aeration"].to_numpy()
# Comparar filtros de 20 Hz y 5 Hz
filtro_20 = butter(4, 20, fs=50, btype="lowpass", output="sos")
filtro_5 = butter(4, 5, fs=50, btype="lowpass", output="sos")
senal_20 = sosfiltfilt(filtro_20, senal)
senal_5 = sosfiltfilt(filtro_5, senal)
# Seleccionar el mismo intervalo
m = (tiempo >= 100) & (tiempo <= 110)
plt.figure(figsize=(10, 5))
plt.plot(tiempo[m], senal[m], label="Original", alpha=0.6)
plt.plot(tiempo[m], senal_20[m], label="Filtro 20 Hz")
plt.plot(tiempo[m], senal_5[m], label="Filtro 5 Hz")
plt.xlabel("Tiempo (s)")
plt.ylabel("Aeración global")
plt.title("Comparación de filtros")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
#CUANTIFICAR EL EFECTO DEL FILTRADO
import numpy as np
for nombre, filtrada in [
    ("20 Hz", senal_20),
    ("5 Hz", senal_5)
]:
    diferencia = np.sqrt(np.mean((senal - filtrada) ** 2))
    print(f"{nombre}: diferencia RMS = {diferencia:.2f}")

#Comparar maximos y minimos
import matplotlib.pyplot as plt
m = (tiempo >= 100) & (tiempo <= 110)
plt.figure(figsize=(10, 5))
plt.plot(tiempo[m], senal[m], label="Original", alpha=0.5)
plt.plot(tiempo[m], senal_5[m], label="Filtrada a 5 Hz")
plt.xlabel("Tiempo (s)")
plt.ylabel("Aeración global")
plt.title("Efecto del filtro sobre los ciclos respiratorios")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Comprar flujo resp con areacion global
import matplotlib.pyplot as plt
# Seleccionar el intervalo
m_flujo = datos["Time [s]"].between(100, 110)
m_eit = eit["Time (Aeration Data)_[s]"].between(100, 110)
# Graficar ambas señales
fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
ax[0].plot(datos.loc[m_flujo, "Time [s]"],
           datos.loc[m_flujo, "Flow [L/s]"])
ax[0].set_ylabel("Flujo (L/s)")
ax[0].set_title("Flujo respiratorio")
ax[1].plot(eit.loc[m_eit, "Time (Aeration Data)_[s]"],
           eit.loc[m_eit, "Global Aeration"])
ax[1].set_ylabel("Aeración global")
ax[1].set_xlabel("Tiempo (s)")
ax[1].set_title("Señal EIT")
plt.tight_layout()
plt.show()

#comprobar si picos de aireacion coinciden con flujo respiratorio
f = datos[datos["Time [s]"].between(100, 110)]
fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
ax[0].plot(f["Time [s]"], f["Flow [L/s]"])
ax[1].plot(s["Time (Aeration Data)_[s]"], s["Global Aeration"])
ax[1].plot(s["Time (Aeration Data)_[s]"].iloc[p],
            s["Global Aeration"].iloc[p], "ro")
ax[0].set_xlim(100, 110)
plt.tight_layout()
plt.show()
print("Picos de aireación:", s["Time (Aeration Data)_[s]"].iloc[p].to_numpy())
s = eit[eit["Time (Aeration Data)_[s]"].between(100, 110)]
p, _ = find_peaks(s["Global Aeration"], distance=75, prominence=1000)

print("Picos de aireación:",
      s["Time (Aeration Data)_[s]"].iloc[p].to_numpy())

plt.plot(s["Time (Aeration Data)_[s]"], s["Global Aeration"])
plt.plot(s["Time (Aeration Data)_[s]"].iloc[p],
         s["Global Aeration"].iloc[p], "ro")
plt.xlim(100, 110)
plt.grid()
plt.show()