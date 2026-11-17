
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