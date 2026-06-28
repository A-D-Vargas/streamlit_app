import streamlit as st
import plotly.express as px

# ── BLOQUE DE TÍTULO ──────────────────────────────────────────
# st.title() muestra el título principal de la app
st.title("Dashboard de Desarrollo Mundial")

# st.markdown() acepta texto con formato; lo usamos para el subtítulo
st.markdown("Explorá la relación entre **riqueza**, **salud** y **población** por país.")

# st.divider() dibuja una línea horizontal como separador visual
st.divider()

# ── CARGA DE DATOS ────────────────────────────────────────────
# Cargamos el dataset Gapminder directamente desde Plotly
# Es un DataFrame con columnas: country, continent, year,
# lifeExp (expectativa de vida), pop (población), gdpPercap (PBI per cápita)
df = px.data.gapminder()

# ── SLIDER ───────────────────────────────────────────────────
# st.slider() crea un control deslizante interactivo
# Parámetros: etiqueta, valor mínimo, valor máximo, valor inicial, paso
anio = st.slider("Seleccioná el año:", 1952, 2007, 2007, step=5)

# Filtramos el dataset para quedarnos solo con el año elegido
# Este filtrado se recalcula automáticamente cada vez que el slider cambia
df_anio = df[df["year"] == anio]

# ── MÉTRICA RÁPIDA ────────────────────────────────────────────
# st.metric() muestra un número destacado con etiqueta
# Lo usamos para mostrar cuántos países hay en el año seleccionado
st.metric("Países en el análisis", df_anio["country"].nunique())

st.divider()

# ── GRÁFICO 1: dispersión ─────────────────────────────────────
# px.scatter() genera un gráfico de dispersión interactivo en una línea
# x: PBI per cápita (riqueza)  y: expectativa de vida (salud)
# size: tamaño del punto según población  color: continente
# hover_name: qué aparece al pasar el cursor sobre un punto
fig1 = px.scatter(
    df_anio,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,                        # escala logarítmica en X (el PBI tiene mucha variación)
    title=f"Riqueza vs. Expectativa de vida — {anio}",
    labels={"gdpPercap": "PBI per cápita (USD)", "lifeExp": "Expectativa de vida (años)"}
)

# st.plotly_chart() renderiza el gráfico de Plotly en la app
# use_container_width=True hace que ocupe todo el ancho disponible
st.plotly_chart(fig1, use_container_width=True)

# ── GRÁFICO 2: barras por continente ─────────────────────────
# px.bar() genera un gráfico de barras interactivo en una línea
# Agrupamos por continente y calculamos el promedio de expectativa de vida
df_cont = df_anio.groupby("continent", as_index=False)["lifeExp"].mean().round(1)

fig2 = px.bar(
    df_cont,
    x="continent",
    y="lifeExp",
    color="continent",
    title=f"Expectativa de vida promedio por continente — {anio}",
    labels={"lifeExp": "Expectativa de vida promedio (años)", "continent": "Continente"},
    text="lifeExp"                      # muestra el valor encima de cada barra
)

st.plotly_chart(fig2, use_container_width=True)

# ── NOTA AL PIE ───────────────────────────────────────────────
# st.caption() muestra texto pequeño, ideal para fuentes o aclaraciones
st.caption("Fuente: Gapminder Dataset — disponible en Plotly Express (px.data.gapminder())") 