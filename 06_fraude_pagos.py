import pandas as pd

# 1. CARGA EL ARCHIVO
df = pd.read_csv("datos/fraude_pagos.csv")

# 2. OBLIGA A PYTHON A MOSTRAR LOS NOMBRES ANTES DE FALLAR
print("\n--- ¡ESTOS SON LOS NOMBRES REALES DE TU ARCHIVO! ---")
print(df.columns.tolist())

# 3. MIRA LAS PRIMERAS FILAS PARA VER QUÉ HAY DENTRO
print("\n--- VISTAZO DE LOS DATOS ---")
print(df.head(2))

# --- LA VERDAD BANCARIA (CORREGIDA) ---

# 1. Definimos los nombres que encontraste
col_pago = 'Payment_Method'
col_fraude = 'Fraudulent' # Reemplázalo por el nombre exacto de tu lista

# 2. Creamos el cruce de datos
# (Esto nos dirá cuántos fraudes hay por cada método)
tabla_verdad = pd.crosstab(df[col_pago], df[col_fraude])

print("--- CONTEO REAL DE TRANSACCIONES ---")
print(tabla_verdad)

# 3. Calculamos el riesgo (Promedio de robos)
riesgo = df.groupby(col_pago)[col_fraude].mean() * 100
print("\n--- % DE RIESGO POR MÉTODO ---")
print(riesgo.sort_values(ascending=False))

# --- INVESTIGACIÓN DE DISPOSITIVOS (EL SOSPECHOSO #2) ---

# 1. Buscamos el nombre real (¿Es 'Device_Used' o 'Device'?)
col_dispositivo = 'Device_Used' 

# 2. Porcentaje de Riesgo por Dispositivo
riesgo_dispositivo = df.groupby(col_dispositivo)['Fraudulent'].mean() * 100

print("\n--- % DE RIESGO POR DISPOSITIVO ---")
print(riesgo_dispositivo.sort_values(ascending=False))

# 3. Conteo real para ver si hay un "Líder" en robos
tabla_dispositivo = pd.crosstab(df[col_dispositivo], df['Fraudulent'])
print("\n--- TABLA DE CONTEO (DISPOSITIVOS) ---")
print(tabla_dispositivo)

# --- INVESTIGACIÓN DE DINERO (MONTO) ---

# 1. ¿Cuánto roban en promedio comparado con las compras legales?
# (Usa el nombre exacto de tu lista: 'Transaction_Amount' o 'Amount')
monto_promedio = df.groupby('Fraudulent')['Transaction_Amount'].mean()

print("\n--- COMPARATIVA DE DINERO (PROMEDIO) ---")
print("0 = Legal | 1 = ROBO")
print(monto_promedio)

# 2. El "Golpe" más grande y el más pequeño
print("\n--- EL ROBO MÁS GRANDE REGISTRADO ---")
print(df[df['Fraudulent'] == 1]['Transaction_Amount'].max())

print("\n--- EL ROBO MÁS PEQUEÑO ---")
print(df[df['Fraudulent'] == 1]['Transaction_Amount'].min())

# --- INVESTIGACIÓN DE CUENTAS (CORREGIDA) ---

# Usamos el nombre que encontraste: Account_Age
antiguedad_riesgo = df.groupby('Fraudulent')['Account_Age'].mean()

print("\n--- ANTIGÜEDAD PROMEDIO DE LA CUENTA ---")
print("0 = Cliente Fiel | 1 = FRAUDE")
print(antiguedad_riesgo)

# Un pequeño extra: ¿Cuál es la cuenta más nueva que robaron?
min_age = df[df['Fraudulent'] == 1]['Account_Age'].min()
print(f"\n🚨 El estafador atacó una cuenta de apenas {min_age} días/meses de antigüedad.")

import matplotlib.pyplot as plt

# 1. GRÁFICO DE BARRAS: Riesgo por Método de Pago
# (Usamos los datos que ya descubriste)
metodos = ['UPI', 'Credit Card', 'Net Banking', 'Debit Card']
riesgos = [5.14, 4.9, 4.9, 4.8]

plt.figure(figsize=(10, 6))
plt.bar(metodos, riesgos, color=['#e74c3c', '#3498db', '#3498db', '#3498db'])
plt.axhline(y=1, color='green', linestyle='--', label='Riesgo Normal (<1%)')
plt.title('Alerta Roja: Porcentaje de Fraude por Método de Pago', fontsize=14)
plt.ylabel('% de Riesgo (Frecuencia de Robo)')
plt.legend()
plt.savefig("01_riesgo_metodo.png")
plt.close()

# 2. GRÁFICO DE DISPOSITIVOS: Volumen de Robos
# (Móvil vs el resto)
dispositivos = ['Mobile', 'Desktop', 'Tablet']
robos = [806, 748, 729]

plt.figure(figsize=(8, 6))
plt.pie(robos, labels=dispositivos, autopct='%1.1f%%', colors=['#e67e22', '#95a5a6', '#bdc3c7'], explode=(0.1, 0, 0))
plt.title('Distribución de Robos por Dispositivo\n(Móvil es el principal punto de ataque)')
plt.savefig("02_volumen_dispositivo.png")
plt.close()

print("✅ ¡Gráficos estratégicos generados con éxito!")

# 3. HISTOGRAMA: ¿En qué montos se concentran los ladrones?

# Filtramos solo los datos donde hubo fraude (1)
datos_fraude = df[df['Fraudulent'] == 1]

plt.figure(figsize=(10, 6))
# Creamos el histograma del monto de la transacción
plt.hist(datos_fraude['Transaction_Amount'], bins=30, color='#c0392b', edgecolor='black', alpha=0.7)

# Añadimos una línea con el promedio de robo que calculamos antes ($3,118)
plt.axvline(3118, color='yellow', linestyle='dashed', linewidth=2, label='Promedio de Robo ($3,118)')

plt.title('Distribución de Montos en Transacciones Fraudulentas', fontsize=14)
plt.xlabel('Monto de la Transacción ($)')
plt.ylabel('Cantidad de Robos')
plt.legend()

# Guardamos el tercer tesoro
plt.savefig("03_distribucion_montos_robo.png")
plt.close()

print("✅ ¡Histograma de montos generado!")