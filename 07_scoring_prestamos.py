import pandas as pd 

# 1. CARGA (En tu carpeta de 'datos' impecable 📂)
df = pd.read_csv("datos/prestamos_banco.csv")

# --- DETECTOR DE HUECOS BANCARIOS ---

# 2. ¿Cuántos nulos hay por columna?
print("--- CONTEO DE NULOS POR COLUMNA ---")
print(df.isnull().sum())

# 3. ¿Qué porcentaje del banco está "vacío"?
print("\n--- PORCENTAJE DE DATOS FALTANTES ---")
print((df.isnull().sum() / len(df)) * 100)

# --- LIMPIEZA PROFUNDA BANCARIA (VERSION FINAL) ---

# 1. Columnas de Dinero -> Usamos MEDIANA
df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].median())
df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].median())

# 2. Columnas de Texto/Categoría -> Usamos MODA (El valor más frecuente)
# Creamos una lista de las columnas que queremos limpiar con moda
columnas_moda = ['Credit_History', 'Self_Employed', 'Dependents', 'Gender', 'Married']

for col in columnas_moda:
    df[col] = df[col].fillna(df[col].mode()[0])

# 3. VERIFICACIÓN FINAL
print("--- RADIOGRAFÍA POST-LIMPIEZA ---")
print(df.isnull().sum())

# --- DUELO DE EDUCACIÓN VS PRÉSTAMO ---
# (Loan_Status: Y = Sí, N = No)
duelo_educacion = pd.crosstab(df['Education'], df['Loan_Status'], normalize='index') * 100

print("\n--- % DE APROBACIÓN POR NIVEL EDUCATIVO ---")
print(duelo_educacion)

# --- DUELO DE ESTADO CIVIL VS PRÉSTAMO ---

# Analizamos si estar casado (Married: Yes/No) influye en la aprobación
duelo_civil = pd.crosstab(df['Married'], df['Loan_Status'], normalize='index') * 100

print("\n--- % DE APROBACIÓN: ¿CASADOS O SOLTEROS? ---")
print(duelo_civil)

# Y un dato extra: ¿El Género influye en la decisión?
duelo_genero = pd.crosstab(df['Gender'], df['Loan_Status'], normalize='index') * 100
print("\n--- % DE APROBACIÓN POR GÉNERO ---")
print(duelo_genero)

# --- EL DUELO DEFINITIVO: HISTORIAL CREDITICIO ---
# 1.0 = Tiene historial (buen pagador) | 0.0 = No tiene o es mal pagador

duelo_historial = pd.crosstab(df['Credit_History'], df['Loan_Status'], normalize='index') * 100

print("\n--- % EL PODER DEL HISTORIAL CREDITICIO ---")
print(duelo_historial)

# Extra: ¿Cuánto dinero piden en promedio los que son aprobados?
monto_aprobado = df.groupby('Loan_Status')['LoanAmount'].mean()
print("\n--- MONTO PROMEDIO SOLICITADO (000's) ---")
print(monto_aprobado)

# --- INVESTIGACIÓN DE INGRESOS (SALARIO) ---

# 1. ¿Cuánto ganan en promedio los aprobados vs los rechazados?
salario_promedio = df.groupby('Loan_Status')['ApplicantIncome'].mean()

print("\n--- SALARIO PROMEDIO DEL SOLICITANTE ---")
print(salario_promedio)

# 2. El "Filtro de Oro": Salario vs Historial
# Vamos a ver si tener buen salario compensa no tener historial
filtro_vip = df.groupby(['Credit_History', 'Loan_Status'])['ApplicantIncome'].mean()
print("\n--- SALARIO PROMEDIO POR HISTORIAL Y ESTADO ---")
print(filtro_vip)

import matplotlib.pyplot as plt

# 1. Creamos la tabla de aprobación por zona
zona_aprobacion = pd.crosstab(df['Property_Area'], df['Loan_Status'], normalize='index') * 100

# 1. Creamos la gráfica
zona_aprobacion.plot(kind='bar', stacked=True, color=['#e74c3c', '#2ecc71'], figsize=(10, 6))
plt.title('¿Influye dónde vives en la aprobación del crédito?', fontsize=14)

# 2. EL GUARDADO (El que va a GitHub)
plt.savefig("01_aprobacion_por_zona.png")

# 3. EL SILENCIADOR (Sustituye a plt.show)
plt.close() 

print("✅ Gráfico guardado en silencio. ¡Sigamos con la IA!")

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 1. Seleccionamos las pistas clave que encontramos hoy
columnas_clave = ['Credit_History', 'Education', 'Married', 'Property_Area', 'LoanAmount', 'ApplicantIncome']
X = df[columnas_clave]
y = df['Loan_Status']

# 2. El TRADUCTOR UNIVERSAL (Convertimos todo a ceros y unos)
X = pd.get_dummies(X, drop_first=True)

# 3. DIVIDIMOS (80% Estudio / 20% Examen)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. ENTRENAMOS AL "COMITÉ DE CRÉDITO" (100 Árboles)
modelo_prestamos = RandomForestClassifier(n_estimators=100, random_state=42)
modelo_prestamos.fit(X_train, y_train)

# 5. EL VEREDICTO FINAL
print("\n--- REPORTE DE PRECISIÓN BANCARIA ---")
predicciones = modelo_prestamos.predict(X_test)
print(classification_report(y_test, predicciones))

# --- ¿QUÉ "MIRA" EL BANCO PARA DARTE EL CRÉDITO? ---

# 1. Extraemos la importancia de las columnas
importancia = pd.Series(modelo_prestamos.feature_importances_, index=X.columns)

# 2. Creamos el gráfico (Con el truco de los nombres completos)
plt.figure(figsize=(10, 6))
importancia.sort_values(ascending=True).plot(kind='barh', color='#2ecc71')

plt.title('Pistas Críticas para la Aprobación de Préstamos', fontsize=14)
plt.xlabel('Nivel de Importancia (Peso en la Decisión)')

# Ajustamos para que no se corten los nombres
plt.tight_layout()

# 3. Guardamos la Evidencia #2
plt.savefig("02_importancia_pistas_prestamo.png")
plt.close()

print("✅ ¡Gráfico de Pistas Bancarias guardado con éxito!")