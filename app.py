import streamlit as st

st.set_page_config(page_title="Calculadora de Rentabilidad", layout="wide")

# --- Estilos personalizados (dark: fondo azul, detalles rosados, texto blanco, botón rosado fuerte con texto negro) ---
st.markdown(
    """
    <style>
    /* Fondo principal y texto blanco */
    .stApp {
        background: linear-gradient(180deg, #041527 0%, #063045 100%);
        color: #ffffff;
    }

    /* Contenedor principal ancho */
    .reportview-container .main .block-container{
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Forzar texto blanco en la mayoría de elementos */
    h1, h2, h3, h4, h5, h6, label, .stText, .stMarkdown p, .stMetric, .stTable td, .stTable th, .css-1dq8tca p {
        color: #ffffff !important;
    }

    /* Sidebar */
    .css-1lcbmhc.e1fqkh3o2, .stSidebar {
        background: linear-gradient(180deg, #032230 0%, #042d3b 100%);
        padding: 1rem;
        border-radius: 10px;
        color: #ffffff;
    }

    /* Inputs (cajas de texto / número / select) */
    input, textarea, select {
        background-color: #0b2633 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 102, 178, 0.18) !important;
        border-radius: 6px;
    }

    /* Placeholders y labels en inputs */
    ::placeholder {
        color: #bcd9e6 !important;
        opacity: 1;
    }

    /* Botón Calcular: rosado fuerte con texto negro para contraste */
    .stButton>button, button[kind="primary"] {
        background: linear-gradient(90deg, #ff007f 0%, #ff2d95 100%);
        color: #000000 !important;
        border: none;
        padding: 10px 18px;
        border-radius: 10px;
        font-weight: 700;
        box-shadow: 0 6px 18px rgba(255,45,149,0.18);
    }
    .stButton>button:hover {
        filter: brightness(0.95);
    }

    /* Métricas: asegurar contraste (valores y labels en blanco) */
    .stMetric .value {
        color: #ffffff !important;
    }
    .stMetric .label {
        color: #ffffff !important;
    }
    .stMetric .delta {
        color: #ffffff !important;
    }

    /* Tablas */
    .stTable td, .stTable th {
        color: #ffffff !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# --- Título e instrucción simple ---
st.title("Calculadora de Rentabilidad")
st.markdown("Completa los campos y presiona Calcular al final")

# --- Form -------------------------------------------------------
with st.form("ml_calc_form"):
    # Primera fila: PRODUCTO, UNIDADES, CODIGO, CATEGORIA
    st.subheader("Detalles del producto")
    prod_col, unidades_col, codigo_col, cat_col = st.columns([3.2, 0.7, 1.2, 1.6])
    with prod_col:
        producto = st.text_input("PRODUCTO", value="", placeholder="Nombre del producto")
    with unidades_col:
        unidades = st.number_input("UNIDADES", min_value=1, value=1, step=1)
    with codigo_col:
        codigo_producto = st.text_input("CÓDIGO DE PRODUCTO", value="", placeholder="SKU / Código")
    with cat_col:
        category_options = [
            ("Alimentos y Bebidas", 11.8),
            ("Supermercado", 11.8),
            ("Celulares y Telefonía", 13.0),
            ("Bebés", 13.5),
            ("Accesorios para Vehículos", 14.0),
            ("Belleza y Cuidado Personal", 14.0),
            ("Consolas y Videojuegos", 14.0),
            ("Computación / Electrónica / Audio y Video", 15.0),
            ("Electrodomésticos", 15.0),
            ("Herramientas", 15.0),
            ("Indumentaria y Calzado", 15.0),
            ("Deportes y Fitness", 15.0),
            ("Hogar, Muebles y Jardín", 15.0),
            ("Juegos y Juguetes", 15.0),
            ("Servicios", 15.0)
        ]
        categoria_display = [f"{name} ({pct:.1f}%)" for name, pct in category_options]
        categoria_sel = st.selectbox("Categoría", options=categoria_display)
        ml_pct = float(categoria_sel.split("(")[-1].replace("%)", "").replace("%", ""))

    # Segunda fila: COSTO, IVA, PRECIO DE VENTA, COSTO DE ENVIO
    st.markdown("### Costos y precio")
    costo_col, iva_col, pv_col, envio_col = st.columns([1.2, 0.5, 1.2, 1.0])
    with costo_col:
        costo = st.number_input("COSTO ($)", min_value=0.0, value=1000.0, format="%.2f")
    with iva_col:
        iva_choice = st.selectbox("IVA", options=["10.5%", "21%"])
        iva_pct = 10.5 if iva_choice == "10.5%" else 21.0
    with pv_col:
        precio_venta = st.number_input("PRECIO DE VENTA FINAL (PV Final) ($)", min_value=0.0, value=20000.0, format="%.2f")
    with envio_col:
        costo_envio = st.number_input("COSTO DE ENVÍO ($) por unidad", min_value=0.0, value=0.0, format="%.2f")

    # Mostrar costo final con IVA (calculado) en un texto claro
    costo_con_iva = costo * (1 + iva_pct / 100.0)
    st.markdown(f"**COSTO FINAL CON IVA ($):** ${costo_con_iva:,.2f}")

    # Tercera fila: IMPUESTOS, CUOTAS, PUBLICIDAD
    st.markdown("### Ajustes adicionales")
    impuestos_col, cuotas_col, publicidad_col = st.columns([1, 1, 1])
    with impuestos_col:
        impuestos_pct = st.number_input("Impuestos (%)", min_value=0.0, value=5.0, format="%.2f")
    with cuotas_col:
        cuotas_option = st.selectbox(
            "Cuotas",
            options=["Sin cuotas (0%)", "3 cuotas (8.40%)", "6 cuotas (12.30%)", "9 cuotas (15.70%)", "12 cuotas (19.20%)"]
        )
        cuotas_pct_map = {
            "Sin cuotas (0%)": 0.0,
            "3 cuotas (8.40%)": 8.40,
            "6 cuotas (12.30%)": 12.30,
            "9 cuotas (15.70%)": 15.70,
            "12 cuotas (19.20%)": 19.20
        }
        cuotas_pct = cuotas_pct_map[cuotas_option]
    with publicidad_col:
        publicidad_pct = st.number_input("Publicidad (%)", min_value=0.0, value=0.0, format="%.2f")

    # Botón calcular (estilizado por CSS arriba)
    submitted = st.form_submit_button("Calcular")

# --- Helper / mappings -----------------------------------------
def cargo_fijo_por_precio(pv):
    if pv <= 15999.0:
        return 1255.0
    if 16000.0 <= pv <= 23999.0:
        return 2500.0
    if 24000.0 <= pv <= 33000.0:
        return 3030.0
    return 0.0

# --- Cálculo ----------------------------------------------------
if submitted:
    # Calculos internos (no se muestran montos desglosados)
    ml_comision = precio_venta * (ml_pct / 100.0)
    cuotas_comision = precio_venta * (cuotas_pct / 100.0)
    impuesto_monto = precio_venta * (impuestos_pct / 100.0)
    publicidad_monto = precio_venta * (publicidad_pct / 100.0)
    cargo_fijo = cargo_fijo_por_precio(precio_venta)

    total_fees_per_unit = (
        ml_comision
        + cuotas_comision
        + impuesto_monto
        + publicidad_monto
        + cargo_fijo
        + costo_envio
    )

    # Ganancia neta por unidad
    profit_per_unit = precio_venta - costo_con_iva - total_fees_per_unit

    # Márgenes:
    # Markup = ganancia / costo_final_con_iva * 100 (se muestra como "Markup")
    markup_pct = (profit_per_unit / costo_con_iva * 100.0) if costo_con_iva > 0 else 0.0

    # Ganancia Neta % (ganancia / precio)
    ganancia_neta_pct = (profit_per_unit / precio_venta * 100.0) if precio_venta > 0 else 0.0

    # Margen sobre venta = Ganancia neta / Costo final con IVA (según tu instrucción)
    margen_sobre_venta_pct = (profit_per_unit / costo_con_iva * 100.0) if costo_con_iva > 0 else 0.0

    # Totales para N unidades
    profit_total = profit_per_unit * unidades
    revenue_total = precio_venta * unidades
    total_costs_total = (costo_con_iva + total_fees_per_unit) * unidades

    # --- Sección "Rentabilidades" --------------------------------
    st.subheader("Rentabilidades")

    # Mostrar en orden: Ganancia Neta $, Ganancia Neta %, Margen sobre venta (%) (según fórmula solicitada), Ganancia total $
    r_col1, r_col2, r_col3, r_col4 = st.columns([1.1, 1.0, 1.0, 1.2])
    with r_col1:
        st.metric("Ganancia Neta ($)", f"${profit_per_unit:,.2f}")
    with r_col2:
        st.metric("Ganancia Neta (%)", f"{ganancia_neta_pct:.2f}%")
    with r_col3:
        st.metric("Margen sobre venta (%)", f"{margen_sobre_venta_pct:.2f}%")
    with r_col4:
        st.metric("Ganancia total ($)", f"${profit_total:,.2f}")

    st.write("---")

    # Porcentajes aplicados (se usan en el cálculo)
    st.subheader("Porcentajes aplicados (se usan en el cálculo)")
    p1, p2, p3 = st.columns(3)
    with p1:
        st.write(f"- Comisión ML aplicada: {ml_pct:.2f}%")
        st.write(f"- IVA aplicado al costo: {iva_pct:.2f}%")
    with p2:
        st.write(f"- Impuestos aplicados sobre PV final: {impuestos_pct:.2f}%")
        st.write(f"- Cuotas seleccionadas: {cuotas_pct:.2f}%")
    with p3:
        st.write(f"- Publicidad aplicada: {publicidad_pct:.2f}%")
        st.write(f"- Unidades: {unidades}")

    st.write("---")
    # Totales para la operación (después de rentabilidades)
    st.subheader("Totales para la operación")
    st.write(f"- Ingreso bruto total (todas las unidades): ${revenue_total:,.2f}")
    st.write(f"- Costos + fees totales (todas las unidades): ${total_costs_total:,.2f}")
    st.write(f"- Ganancia neta total (todas las unidades): ${profit_total:,.2f}")

    st.write("---")
    st.subheader("Notas y supuestos")
    st.markdown(
        """
        - "Margen sobre venta (%)" se calcula como Ganancia neta dividido por Costo final con IVA, tal como solicitaste.
        - No se muestran montos en ARS desglosados para: comisiones ML, impuestos aplicados sobre PV, cargos por cuotas ni publicidad. Solo se muestran los porcentajes seleccionados.
        - Los porcentajes ingresados son aplicados sobre el PRECIO DE VENTA FINAL (PV) cuando corresponde (comisiones, cuotas, impuestos, publicidad).
        - El cargo fijo se aplica por unidad según la tabla proporcionada; si el PV está fuera de rango (> $33.000) el cargo fijo queda en $0 (se muestra sin alertas).
        """
    )
