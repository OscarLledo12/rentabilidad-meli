import streamlit as st

st.set_page_config(page_title="Calculadora de Rentabilidad - Mercado Libre AR", layout="wide")

# --- Estilos personalizados (dark: fondo azul, detalles rosados) ---
st.markdown(
    """
    <style>
    /* Fondo principal */
    .stApp {
        background: linear-gradient(180deg, #041527 0%, #063045 100%);
        color: #e6f6ff;
    }

    /* Contenedor principal */
    .reportview-container .main .block-container{
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Sidebar */
    .css-1lcbmhc.e1fqkh3o2, .stSidebar {
        background: linear-gradient(180deg, #032230 0%, #042d3b 100%);
        padding: 1rem;
        border-radius: 10px;
    }

    /* Títulos y textos */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #f3f7fb;
    }
    .stText, .stMarkdown p, label {
        color: #dff2ff;
    }

    /* Inputs (cajas de texto / número / select) */
    input, textarea, select {
        background-color: #0b2633 !important;
        color: #e6f6ff !important;
        border: 1px solid rgba(255, 102, 178, 0.18) !important;
        border-radius: 6px;
    }

    /* Botones */
    .stButton>button, button[kind="primary"] {
        background: linear-gradient(90deg, #ff66b2 0%, #ff4fa6 100%);
        color: white;
        border: none;
        padding: 8px 14px;
        border-radius: 8px;
    }
    .stButton>button:hover {
        filter: brightness(0.95);
    }

    /* Metric style tweaks */
    .stMetric .value {
        color: #ffeef8 !important;
    }
    .stMetric .delta {
        color: #ffd2ea !important;
    }

    /* Table text color */
    .stTable td, .stTable th {
        color: #e9fbff !important;
    }

    /* Make containers a bit translucent */
    .stCard, .st-bk {
        background: rgba(2,18,26,0.30) !important;
        border-radius: 8px;
    }

    /* Improve spacing of columns on wide layout */
    .css-ffhzg2.e16nr0p31 { padding: 0.5rem 0; }

    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Calculadora de rentabilidad para ventas en Mercado Libre (Argentina)")
st.markdown(
    "Completa los campos del formulario y presiona Calcular. "
    "Los porcentajes seleccionados (comisión ML, impuestos, cuotas, publicidad) se utilizan en los cálculos pero no se muestran como montos en ARS por separado."
)

# --- Form -------------------------------------------------------
with st.form("ml_calc_form"):
    st.subheader("Detalles del producto")
    col1, col2 = st.columns([3, 1.2])
    with col1:
        producto = st.text_input("PRODUCTO", value="", placeholder="Nombre del producto")
        codigo_producto = st.text_input("CÓDIGO DE PRODUCTO", value="", placeholder="SKU / Código interno")
    with col2:
        unidades = st.number_input("UNIDADES a vender", min_value=1, value=1, step=1)

    st.markdown("### Costos y precio")
    colc1, colc2, colc3 = st.columns([1.2, 1.2, 1.2])
    with colc1:
        costo = st.number_input("COSTO (ARS)", min_value=0.0, value=1000.0, format="%.2f")
        iva_choice = st.selectbox("IVA", options=["10.5%", "21%"])
        iva_pct = 10.5 if iva_choice == "10.5%" else 21.0
        costo_con_iva = costo * (1 + iva_pct / 100.0)
        st.markdown(f"**COSTO FINAL CON IVA:** ARS {costo_con_iva:,.2f}")
    with colc2:
        precio_venta = st.number_input("PRECIO DE VENTA FINAL (PV Final) - por unidad (ARS)", min_value=0.0, value=20000.0, format="%.2f")
    with colc3:
        costo_envio = st.number_input("COSTO DE ENVÍO (ARS) por unidad (si aplica)", min_value=0.0, value=0.0, format="%.2f")

    st.markdown("### Categoría (determina % de comisión ML)")
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

    st.markdown("### Impuestos (se aplican sobre PV final)")
    impuestos_pct = st.number_input("IMPUESTOS (%) - ingresá un porcentaje", min_value=0.0, value=5.0, format="%.2f")

    st.markdown("### Financiamiento (CUOTAS) - % que se aplica sobre PV")
    cuotas_option = st.selectbox(
        "CUOTAS",
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

    st.markdown("### Publicidad / Promoción (ingresá %)")
    publicidad_pct = st.number_input("PUBLICIDAD (%) - ingresá un porcentaje", min_value=0.0, value=0.0, format="%.2f")

    submitted = st.form_submit_button("Calcular")

# --- Helper / mappings -----------------------------------------
def cargo_fijo_por_precio(pv):
    """
    Retorna cargo fijo por unidad según rangos indicados:
    - hasta 15.999 -> 1.255
    - 16.000 a 23.999 -> 2.500
    - 24.000 a 33.000 -> 3.030
    Si está fuera de rangos (por encima de 33.000) devuelve 0.0 (no definido).
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
    # Calculamos internamente las comisiones/montos pero NO los mostramos por separado en ARS
    ml_comision = precio_venta * (ml_pct / 100.0)          # usado internamente
    cuotas_comision = precio_venta * (cuotas_pct / 100.0) # usado internamente
    impuesto_monto = precio_venta * (impuestos_pct / 100.0) # usado internamente
    publicidad_monto = precio_venta * (publicidad_pct / 100.0) # usado internamente
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
    st.subheader("Porcentajes aplicados (se usan en el cálculo, no se muestran en ARS)")
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
    st.subheader("Resultados financieros (se muestran montos finales y ratios)")

    # Mostrar en un layout ancho y proporcionado
    top_col1, top_col2, top_col3 = st.columns([1.2, 1.2, 1])
    with top_col1:
        st.metric("PRECIO DE VENTA (por unidad)", f"ARS {precio_venta:,.2f}")
        st.metric("COSTO FINAL CON IVA (por unidad)", f"ARS {costo_con_iva:,.2f}")
    with top_col2:
        st.metric("Cargo fijo aplicado (por unidad)", f"ARS {cargo_fijo:,.2f}")
        st.metric("Costo de envío (por unidad)", f"ARS {costo_envio:,.2f}")
    with top_col3:
        st.metric("Ganancia neta por unidad (ARS)", f"ARS {profit_per_unit:,.2f}")
        st.metric("Markup (ganancia / costo) (%)", f"{markup_pct:.2f}%")
        st.metric("Margen sobre venta (%)", f"{margin_pct:.2f}%")

    st.write("---")
    st.subheader("Totales para la operación")
    st.write(f"- Ingreso bruto total (todas las unidades): ARS {revenue_total:,.2f}")
    st.write(f"- Costos + fees totales (todas las unidades): ARS {total_costs_total:,.2f}")
    st.write(f"- Ganancia neta total (todas las unidades): ARS {profit_total:,.2f}")

    st.write("---")
    st.subheader("Notas y supuestos")
    st.markdown(
        """
        - No se muestran montos en ARS desglosados para: comisiones ML, impuestos aplicados sobre PV, cargos por cuotas ni publicidad. Solo se muestran los porcentajes seleccionados.
        - Los porcentajes ingresados son aplicados sobre el PRECIO DE VENTA FINAL (PV) cuando corresponde (comisiones, cuotas, impuestos, publicidad).
        - El cargo fijo se aplica por unidad según la tabla proporcionada; si el PV está fuera de rango (> $33.000) el cargo fijo queda en $0 (no se muestra ninguna alerta).
        - El cálculo incorpora: costo con IVA, comisiones ML (según categoría), comisión por cuotas, impuestos (sobre PV), publicidad (sobre PV), cargo fijo y costo de envío.
        """
    )
