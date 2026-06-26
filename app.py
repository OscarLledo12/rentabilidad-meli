import streamlit as st

st.set_page_config(page_title="Calculadora de Rentabilidad", layout="wide")

# --- Estilos personalizados (dark: fondo azul, detalles rosados, todo en blanco) ---
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
    h1, h2, h3, h4, h5, h6, label, .stText, .stMarkdown p, .stMetric, .stTable td, .stTable th {
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

    /* Labels dentro de inputs */
    .st-b5 { color: #ffffff !important; }

    /* Botones: rosado con letras azules */
    .stButton>button, button[kind="primary"] {
        background: linear-gradient(90deg, #ff7fbf 0%, #ff66b2 100%);
        color: #063045 !important;
        border: none;
        padding: 8px 14px;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton>button:hover {
        filter: brightness(0.95);
    }

    /* Métricas y valores */
    .stMetric .value {
        color: #ffffff !important;
    }
    .stMetric .delta {
        color: #ffffff !important;
    }

    /* Tablas */
    .stTable td, .stTable th {
        color: #ffffff !important;
    }

    /* Asegurar placeholders y textos de inputs en blanco */
    ::placeholder {
        color: #bcd9e6 !important;
        opacity: 1;
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
    st.subheader("Detalles del producto")
    col1, col2 = st.columns([3, 1])
    with col1:
        producto = st.text_input("PRODUCTO", value="", placeholder="Nombre del producto")
        codigo_producto = st.text_input("CÓDIGO DE PRODUCTO", value="", placeholder="SKU / Código interno")
    with col2:
        unidades = st.number_input("UNIDADES a vender", min_value=1, value=1, step=1)

    st.markdown("### Costos y precio")
    colc1, colc2, colc3 = st.columns([1.2, 1.2, 1.2])
    with colc1:
        costo = st.number_input("COSTO ($)", min_value=0.0, value=1000.0, format="%.2f")
        iva_choice = st.selectbox("IVA", options=["10.5%", "21%"])
        iva_pct = 10.5 if iva_choice == "10.5%" else 21.0
        costo_con_iva = costo * (1 + iva_pct / 100.0)
        st.markdown(f"**COSTO FINAL CON IVA ($):** ${costo_con_iva:,.2f}")
    with colc2:
        precio_venta = st.number_input("PRECIO DE VENTA FINAL (PV Final) ($) - por unidad", min_value=0.0, value=20000.0, format="%.2f")
    with colc3:
        costo_envio = st.number_input("COSTO DE ENVÍO ($) por unidad (si aplica)", min_value=0.0, value=0.0, format="%.2f")

    st.markdown("### Categoría")
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

    st.markdown("### Impuestos")
    impuestos_pct = st.number_input("IMPUESTOS (%) - ingresá un porcentaje", min_value=0.0, value=5.0, format="%.2f")

    st.markdown("### Cuotas")
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

    st.markdown("### Publicidad %")
    publicidad_pct = st.number_input("Publicidad (%) - ingresá un porcentaje", min_value=0.0, value=0.0, format="%.2f")

    submitted = st.form_submit_button("Calcular")

# --- Helper / mappings -----------------------------------------
def cargo_fijo_por_precio(pv):
    """
    Retorna cargo fijo por unidad según rangos indicados:
    - hasta 15.999 -> 1.255
    - 16.000 a 23.999 -> 2.500
    - 24.000 a 33.000 -> 3.030
    Si está fuera de rangos (por encima de 33.000) devuelve 0.0 (se muestra $0 sin alertas).
    """
    if pv <= 15999.0:
        return 1255.0
    if 16000.0 <= pv <= 23999.0:
        return 2500.0
    if 24000.0 <= pv <= 33000.0:
        return 3030.0
    return 0.0

# --- Cálculo ----------------------------------------------------
if submitted:
    # Calculamos internamente las comisiones/montos (no se muestran por separado en ARS)
    ml_comision = precio_venta * (ml_pct / 100.0)
    cuotas_comision = precio_venta * (cuotas_pct / 100.0)
    impuesto_monto = precio_venta * (impuestos_pct / 100.0)
    publicidad_monto = precio_venta * (publicidad_pct / 100.0)
    cargo_fijo = cargo_fijo_por_precio(precio_venta)

    # Total fees / cargos por unidad (incluye comisiones, impuestos, publicidad, cargo fijo y envío)
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
    markup_pct = (profit_per_unit / costo_con_iva * 100.0) if costo_con_iva > 0 else 0.0
    margin_pct = (profit_per_unit / precio_venta * 100.0) if precio_venta > 0 else 0.0

    # Totales para N unidades
    profit_total = profit_per_unit * unidades
    revenue_total = precio_venta * unidades
    total_costs_total = (costo_con_iva + total_fees_per_unit) * unidades

    # --- Resultados (sin mostrar montos individuales de comisiones/impuestos/publicidad) ---
    st.subheader("Porcentajes aplicados (se usan en el cálculo)")
    pct_col1, pct_col2, pct_col3 = st.columns(3)
    with pct_col1:
        st.write(f"- Comisión ML aplicada: {ml_pct:.2f}%")
        st.write(f"- IVA aplicado al costo: {iva_pct:.2f}%")
    with pct_col2:
        st.write(f"- Impuestos aplicados sobre PV final: {impuestos_pct:.2f}%")
        st.write(f"- Cuotas seleccionadas: {cuotas_pct:.2f}%")
    with pct_col3:
        st.write(f"- Publicidad aplicada: {publicidad_pct:.2f}%")
        st.write(f"- Unidades: {unidades}")

    st.write("---")
    st.subheader("Resultados financieros")

    # Mostrar en un layout ancho y proporcionado, con formato moneda $
    top_col1, top_col2, top_col3 = st.columns([1.2, 1.2, 1])
    with top_col1:
        st.metric("PRECIO DE VENTA (por unidad) $", f"${precio_venta:,.2f}")
        st.metric("COSTO FINAL CON IVA (por unidad) $", f"${costo_con_iva:,.2f}")
    with top_col2:
        st.metric("Cargo fijo (por unidad) $", f"${cargo_fijo:,.2f}")
        st.metric("Costo de envío (por unidad) $", f"${costo_envio:,.2f}")
    with top_col3:
        st.metric("Ganancia neta por unidad ($)", f"${profit_per_unit:,.2f}")
        st.metric("Markup (ganancia / costo) (%)", f"{markup_pct:.2f}%")
        st.metric("Margen sobre venta (%)", f"{margin_pct:.2f}%")

    st.write("---")
    st.subheader("Totales para la operación")
    st.write(f"- Ingreso bruto total (todas las unidades): ${revenue_total:,.2f}")
    st.write(f"- Costos + fees totales (todas las unidades): ${total_costs_total:,.2f}")
    st.write(f"- Ganancia neta total (todas las unidades): ${profit_total:,.2f}")

    st.write("---")
    st.subheader("Notas y supuestos")
    st.markdown(
        """
        - No se muestran montos en ARS desglosados para: comisiones ML, impuestos aplicados sobre PV, cargos por cuotas ni publicidad. Solo se muestran los porcentajes seleccionados.
        - Los porcentajes ingresados son aplicados sobre el PRECIO DE VENTA FINAL (PV) cuando corresponde (comisiones, cuotas, impuestos, publicidad).
        - El cargo fijo se aplica por unidad según la tabla proporcionada; si el PV está fuera de rango (> $33.000) el cargo fijo queda en $0 (se muestra sin alertas).
        - El cálculo incorpora: costo con IVA, comisiones ML (según categoría), comisión por cuotas, impuestos (sobre PV), publicidad (sobre PV), cargo fijo y costo de envío.
        """
    )
