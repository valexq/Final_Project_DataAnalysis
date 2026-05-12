# Proyecto de Analítica de Datos y Modelo Predictivo sobre Cambio Climático

Proyecto integrador orientado al desarrollo de una solución completa de análisis de datos, inteligencia de negocios y aprendizaje computacional, utilizando indicadores climáticos globales como caso de estudio.

El proyecto implementa un flujo de trabajo end-to-end que incluye procesos ETL, análisis exploratorio de datos (EDA), visualización de información, generación de dashboards y construcción de modelos predictivos supervisados.

---

# 1. Descripción del Proyecto

Este proyecto tiene como objetivo analizar indicadores relacionados con el cambio climático en múltiples países entre los años 2000 y 2023, utilizando técnicas de analítica de datos y aprendizaje automático para extraer patrones, generar conocimiento útil y construir modelos predictivos.

El dataset incluye variables como:

- Temperatura promedio
- Emisiones de CO₂
- Nivel del mar
- Precipitaciones
- Participación de energías renovables
- Área forestal
- Eventos climáticos extremos

A partir de estos datos se desarrolló una solución analítica completa que permite:

- Procesar y transformar datos mediante pipelines ETL.
- Analizar tendencias y correlaciones climáticas.
- Generar visualizaciones y dashboards interactivos.
- Construir modelos predictivos supervisados.
- Formular conclusiones y recomendaciones basadas en evidencia.

---

# 2. Objetivos

## Objetivo General

Desarrollar un proyecto integral de análisis de datos y aprendizaje computacional aplicado al estudio del cambio climático, incorporando procesos ETL, inteligencia de negocios y modelado predictivo.

## Objetivos Específicos

- Identificar y transformar fuentes de datos relevantes.
- Realizar limpieza y análisis exploratorio de datos.
- Diseñar visualizaciones y dashboards para apoyar la toma de decisiones.
- Implementar modelos de aprendizaje supervisado.
- Evaluar el rendimiento de los modelos mediante métricas apropiadas.
- Generar conclusiones y recomendaciones estratégicas.

---

# 3. Relación con los Resultados de Aprendizaje

## Inteligencia de Negocios (BI)

- Definición de reglas de negocio para el tratamiento de datos.
- Diseño de un modelo de datos para explotación analítica.
- Creación de dashboards interactivos para visualización de insights.

## Analítica de Datos (AD)

- Implementación del proceso ETL.
- Limpieza y transformación de datos.
- Análisis exploratorio y visualización de patrones.

## Aprendizaje Computacional (AC)

- Implementación de modelos supervisados.
- Evaluación mediante métricas de desempeño.
- Aplicación de técnicas de Machine Learning.

---

# 4. Tecnologías Utilizadas

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.11 |
| Manipulación de datos | pandas, numpy |
| Visualización | matplotlib, seaborn, plotly |
| Machine Learning | scikit-learn |
| Notebooks | Jupyter Notebook |
| Persistencia | CSV, Parquet |
| Testing | pytest |

---

# 5. Arquitectura del Proyecto

```text
climate_analytics_project/
│
├── data/
│   ├── raw/              # Datos originales
│   ├── cleaned/          # Datos limpios
│   ├── processed/        # Datos transformados
│   └── external/         # Datos externos de apoyo
│
├── notebooks/            # Notebooks del análisis
│
├── reports/
│   ├── figures/          # Gráficas exportadas
│   ├── tables/           # Tablas y métricas
│   └── final_report/     # Informe final
│
├── src/                  # Código fuente reutilizable
│
├── tests/                # Pruebas unitarias
│
├── requirements.txt
├── environment.yml
└── README.md