import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1. Carga y limpieza de datos (simulando el archivo Excel)
# ------------------------------------------------------------
# Dado que el contenido se proporcionó en el mensaje, lo recreamos manualmente.
# En la práctica se usaría: df = pd.read_excel('Acusaciones de acoso o intimidacion.xlsx', sheet_name='Total', skiprows=3)

# Datos extraídos de la tabla (excluyendo filas vacías y notas)
data = {
    'Estado': ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
               'Delaware', 'Distrito de Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois',
               'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
               'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
               'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
               'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
               'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'Virginia Occidental',
               'Wisconsin', 'Wyoming'],
    'Total_acusaciones': [1434,58,2780,1222,18197,1162,1017,258,116,149,1550,824,1168,19687,2279,1310,2046,
                          885,448,581,514,1842,5081,5881,731,3424,954,1217,1252,685,5613,1255,10791,2291,227,
                          2782,1295,2612,4460,2016,988,268,5703,3931,2111,1106,1574,3041,1116,2996,264],
    'Escuelas': [1400,503,1977,1092,10138,1868,1238,235,221,3952,2407,290,720,4081,1879,1365,1356,1407,1367,
                 589,1434,1873,3616,2170,978,2372,825,1064,658,483,2577,880,4916,2618,481,3631,1815,1283,3027,
                 308,1236,688,1818,8616,1009,306,1971,2305,720,2232,365],
    'Porcentaje_reporta': [100.0,100.0,99.6965,99.8168,99.6449,89.6146,100.0,100.0,48.8688,100.0,100.0,100.0,
                           100.0,99.70595,100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0,99.97235,99.81567,
                           100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0,99.85761,100.0,100.0,100.0,100.0,
                           100.0,100.0,100.0,95.63107,100.0,100.0,100.0,94.84638,100.0,100.0,100.0,100.0,100.0,
                           100.0]
}

df = pd.DataFrame(data)

# Verificar que no hay nulos
print(df.isnull().sum())

# ------------------------------------------------------------
# 2. Separar predictores y objetivo
# ------------------------------------------------------------
X = df[['Escuelas', 'Porcentaje_reporta']]
y = df['Total_acusaciones']

# ------------------------------------------------------------
# 3. División entrenamiento (70%) y prueba (30%)
# ------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ------------------------------------------------------------
# 4. Escalado de características (StandardScaler)
# ------------------------------------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ------------------------------------------------------------
# 5. Modelo de regresión lineal
# ------------------------------------------------------------
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# ------------------------------------------------------------
# 6. Evaluación en test
# ------------------------------------------------------------
y_pred = model.predict(X_test_scaled)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

print("\n--- Resultados en conjunto de prueba ---")
print(f"R²: {r2:.4f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAE: {mae:.2f}")

# Coeficientes (en escala original para interpretación)
coef_df = pd.DataFrame({
    'Variable': ['Intercepto', 'Escuelas', 'Porcentaje_reporta'],
    'Coeficiente': [model.intercept_, model.coef_[0], model.coef_[1]]
})
print("\nCoeficientes del modelo (sobre características estandarizadas):")
print(coef_df)

# ------------------------------------------------------------
# 7. Diagramas de diagnóstico
# ------------------------------------------------------------

# 7.1 Reales vs Predichos
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.6, edgecolors='k', linewidth=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Valores Reales')
plt.ylabel('Valores Predichos')
plt.title('Valores Reales vs Predichos')
plt.tight_layout()
plt.savefig('diagrama_reales_vs_predichos.png')

# 7.2 Residuales vs Predichos
plt.figure(figsize=(8, 6))
residuals = y_test - y_pred
plt.scatter(y_pred, residuals, alpha=0.6, edgecolors='k', linewidth=0.5)
plt.axhline(y=0, color='r', linestyle='--', lw=2)
plt.xlabel('Valores Predichos')
plt.ylabel('Residuales')
plt.title('Residuales vs Valores Predichos')
plt.tight_layout()
plt.savefig('diagrama_residuales.png')

# 7.3 Histograma de residuales
plt.figure(figsize=(8, 6))
plt.hist(residuals, bins=15, edgecolor='black', alpha=0.7)
plt.xlabel('Residual')
plt.ylabel('Frecuencia')
plt.title('Distribución de Residuales')
plt.tight_layout()
plt.savefig('diagrama_histograma_residuales.png')

# 7.4 Coeficientes del modelo
plt.figure(figsize=(8, 6))
variables = ['Escuelas', 'Porcentaje_reporta']
coeficientes = [model.coef_[0], model.coef_[1]]
plt.bar(variables, coeficientes, color=['steelblue', 'coral'], edgecolor='black')
plt.axhline(y=0, color='gray', linestyle='--', lw=1)
plt.ylabel('Coeficiente')
plt.title('Coeficientes del Modelo')
plt.tight_layout()
plt.savefig('diagrama_coeficientes.png')

# ------------------------------------------------------------
# 8. Validación cruzada (5 folds) en entrenamiento
# ------------------------------------------------------------
kfold = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=kfold, scoring='r2')
print(f"\nValidación cruzada (5 folds) R²: media = {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# ------------------------------------------------------------
# 9. Diagrama de validación cruzada
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
fold_labels = [f'Fold {i+1}' for i in range(len(cv_scores))]
plt.bar(fold_labels, cv_scores, color='steelblue', edgecolor='black')
plt.axhline(y=cv_scores.mean(), color='red', linestyle='--', lw=2, label=f'Media = {cv_scores.mean():.4f}')
plt.ylabel('R²')
plt.title('Puntuaciones R² por Fold en Validación Cruzada')
plt.legend()
plt.tight_layout()
plt.savefig('diagrama_validacion_cruzada.png')

# ------------------------------------------------------------
# 10. (Opcional) Regresión simple solo con 'Escuelas' para comparar
# ------------------------------------------------------------
X_simple = df[['Escuelas']]
X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(X_simple, y, test_size=0.3, random_state=42)
scaler_s = StandardScaler()
X_train_s_scaled = scaler_s.fit_transform(X_train_s)
X_test_s_scaled = scaler_s.transform(X_test_s)
model_simple = LinearRegression()
model_simple.fit(X_train_s_scaled, y_train_s)
y_pred_s = model_simple.predict(X_test_s_scaled)
r2_s = r2_score(y_test_s, y_pred_s)
print(f"\nModelo solo con 'Escuelas' - R² en test: {r2_s:.4f}")

# ------------------------------------------------------------
# 11. Diagrama comparativo de modelos
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
modelos = ['Completo\n(Escuelas + %reporta)', 'Simple\n(solo Escuelas)']
r2_valores = [r2, r2_s]
colores = ['steelblue', 'coral']
plt.bar(modelos, r2_valores, color=colores, edgecolor='black')
plt.ylabel('R²')
plt.title('Comparación de R² entre Modelos')
plt.tight_layout()
plt.savefig('diagrama_comparacion_modelos.png')

plt.show()
