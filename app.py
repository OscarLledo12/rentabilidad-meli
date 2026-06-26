import streamlit as st

st.set_page_config(page_title="Calculadora de Rentabilidad", layout="wide")

# --- Estilos personalizados (fondo lila, detalles rosados, texto blanco) ---
st.markdown(
    """
    <style>
    /* Fondo principal lila y texto blanco */
    .stApp {
        background: linear-gradient(180deg, #663399 0%, #9933cc 100%);
        color: #ffffff;
    }

    /* Contenedor principal ancho */
    .reportview-container .main .block-container{
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Forzar texto blanco en la mayoría de elementos */
    h1, h2, h3, h4, h5, h6, label, .stText, .stMarkdown p, .stMetric, .stTable td, .stTable th {
        color: #ffffff !important;
    }

    /* Sidebar */
    .css-1lcbmhc.e1fqkh3o2, .stSidebar {
        background: linear-gradient(180deg, #5522aa 0%, #7722cc 100%);
        padding: 1rem;
        border-radius: 10px;
        color: #ffffff;
    }

    /* Inputs (cajas de texto / número / select) */
    input, textarea, select {
        background-color: #4a1f66 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 102, 178, 0.18) !important;
        border-radius: 6px;
    }

    /* Placeholders y labels en inputs */
    ::placeholder {
        color: #d4b5e6 !important;
        opacity: 1;
    }

    /* Botón Calcular: Verde fuerte con texto negro - GRANDE Y CENTRADO */
    .stButton {
        display: flex;
        justify-content: center !important;
        width: 100% !important;
    }

    .stButton > button {
        background-color: #00CC00 !important;
        background-image: none !important;
        color: #000000 !important;
        border: 4px solid #000000 !important;
        padding: 20px 60px !important;
        border-radius: 15px !important;
        font-weight: 900 !important;
        font-size: 24px !important;
        box-shadow: 0 12px 28px rgba(0, 204, 0, 0.4) !important;
        width: auto !important;
        min-width: 300px !important;
        display: inline-block !important;
    }
    
    .stButton > button:hover {
        background-color: #00AA00 !important;
        color: #000000 !important;
        border: 4px solid #000000 !important;
        filter: brightness(1.1) !important;
        box-shadow: 0 14px 32px rgba(0, 204, 0, 0.5) !important;
    }

    .stButton > button:active {
        background-color: #008800 !important;
        color: #000000 !important;
        filter: brightness(0.95) !important;
    }

    /* Asegurar que el texto del botón sea negro */
    .stButton > button > p {
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 24px !important;
    }

    .stButton > button > span {
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 24px !important;
    }

    /* Métricas: asegurar contraste (valores y labels en blanco por defecto) */
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

# --- Título ---
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

    # Mostrar costo final con IVA (calculado) - etiqueta personalizada en blanco
    costo_con_iva = costo * (1 + iva_pct / 100.0)
    st.markdown(
        f"<div style='color:#ffffff; font-weight:700;'>Costo final c/iva: <span style=\"color:#ffffff\">${costo_con_iva:,.2f}</span></div>",
        unsafe_allow_html=True,
    )

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

    # Botón calcular - GRANDE, CENTRADO Y VERDE
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("CALCULAR")

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
    # Cálculos internos (no se muestran montos desglosados)
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

    # Ganancia neta por unidad ($)
    profit_per_unit = precio_venta - costo_con_iva - total_fees_per_unit

    # Markup (%) = ganancia / costo_final_con_iva * 100  (se muestra como markup)
    markup_pct = (profit_per_unit / costo_con_iva * 100.0) if costo_con_iva > 0 else 0.0

    # Totales para N unidades
    profit_total = profit_per_unit * unidades
    revenue_total = precio_venta * unidades
    total_costs_total = (costo_con_iva + total_fees_per_unit) * unidades

    # --- Sección "Rentabilidades" --------------------------------
    st.subheader("Rentabilidades")

    # Mostrar: Ganancia Neta Unitaria $, Ganancia Neta % (según tu instrucción), Ganancia total $
    r_col1, r_col2, r_col3 = st.columns([1.2, 1.0, 1.2])

    # Use inline HTML to render these rentabilidad results in yellow
    r_col1.markdown(
        f"""
        <div style="color:#FFD700; font-weight:700; padding:4px;">
          <div style="font-size:14px;">Ganancia Neta Unitaria ($)</div>
          <div style="font-size:22px; font-weight:800;">${profit_per_unit:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    r_col2.markdown(
        f"""
        <div style="color:#FFD700; font-weight:700; padding:4px;">
          <div style="font-size:14px;">Ganancia Neta (%)</div>
          <div style="font-size:22px; font-weight:800;">{markup_pct:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    r_col3.markdown(
        f"""
        <div style="color:#FFD700; font-weight:700; padding:4px;">
          <div style="font-size:14px;">Ganancia total ($)</div>
          <div style="font-size:22px; font-weight:800;">${profit_total:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
