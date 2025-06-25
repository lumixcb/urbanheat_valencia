# 🌡️ UrbanHeat – Predicción de islas de calor urbanas en València

UrbanHeat es una aplicación que predice zonas con mayor riesgo térmico en la ciudad de València, combinando datos de temperatura, vegetación y otros factores urbanos.

## 📁 Estructura del proyecto

urbanheat_valencia/
├── app/ # Aplicación principal en Streamlit
├── data/
│ ├── raw/ # Datos originales sin procesar
│ └── processed/ # Datos limpios y listos para modelar
├── models/ # Modelos entrenados
├── notebooks/ # Notebooks de análisis y predicción
├── media/ # Imágenes, capturas o recursos visuales
├── requirements.txt # Librerías necesarias
└── README.md # Descripción general del proyecto


## 📊 Datasets utilizados

- **Temperatura València 2018–2022** (Opendata València)
- **Cartografía Base Vegetación** (Opendata València)
- [Posible integración] Datos urbanos o socioeconómicos adicionales

## 🎯 Objetivo

Aplicar técnicas de Machine Learning para detectar y visualizar zonas urbanas con riesgo térmico elevado, con el fin de:

- Identificar patrones espaciales
- Proponer estrategias de mitigación
- Ayudar en decisiones de planificación urbana