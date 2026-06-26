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

st.markdown("Completa los campos y verás los cálculos en tiempo real")

# --- Inicializar session state si no existe ---
if 'producto' not in st.session_state:
    st.session_state.producto = ""
if 'codigo_producto' not in st.session_state:
    st.session_state.codigo_producto = ""
if 'unidades' not in st.session_state:
    st.session_state.unidades = 1
if 'costo' not in st.session_state:
    st.session_state.costo = 0.0
if 'iva_choice' not in st.session_state:
    st.session_state.iva_choice = "21%"
if 'precio_venta' not in st.session_state:
    st.session_state.precio_venta = 0.0
if 'costo_envio' not in st.session_state:
    st.session_state.costo_envio = 0.0
if 'categoria_sel' not in st.session_state:
    st.session_state.categoria_sel = "Alimentos y Bebidas (11.8%)"
if 'impuestos_pct' not in st.session_state:
    st.session_state.impuestos_pct = 5.0
if 'cuotas_option' not in st.session_state:
    st.session_state.cuotas_option = "Sin cuotas (0%)"
if 'publicidad_pct' not in st.session_state:
    st.session_state.publicidad_pct = 5.0

# --- Inputs sin formulario (sin st.form) ---
# Primera fila: PRODUCTO, UNIDADES, CODIGO, CATEGORIA
st.subheader("Detalles del producto")
prod_col, unidades_col, codigo_col, cat_col = st.columns([3.2, 0.7, 1.2, 1.6])
with prod_col:
    producto = st.text_input("PRODUCTO", value=st.session_state.producto, placeholder="Nombre del producto", key="producto_input")
    st.session_state.producto = producto
with unidades_col:
    unidades = st.number_input("UNIDADES", min_value=1, value=st.session_state.unidades, step=1, key="unidades_input")
    st.session_state.unidades = unidades
with codigo_col:
    codigo_producto = st.text_input("CÓDIGO DE PRODUCTO", value=st.session_state.codigo_producto, placeholder="SKU / Código", key="codigo_input")
    st.session_state.codigo_producto = codigo_producto
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
    categoria_sel = st.selectbox("Categoría", options=categoria_display, index=categoria_display.index(st.session_state.categoria_sel) if st.session_state.categoria_sel in categoria_display else 0, key="categoria_input")
    st.session_state.categoria_sel = categoria_sel
    ml_pct = float(categoria_sel.split("(")[-1].replace("%)", "").replace("%", ""))

# Segunda fila: COSTO, IVA, PRECIO DE VENTA, COSTO DE ENVIO
st.markdown("### Costos y precio")
costo_col, iva_col, pv_col, envio_col = st.columns([1.2, 0.5, 1.2, 1.0])
with costo_col:
    costo = st.number_input("Costo sin IVA $", min_value=0.0, value=st.session_state.costo, format="%.2f", key="costo_input")
    st.session_state.costo = costo
with iva_col:
    iva_choice = st.selectbox("IVA", options=["10.5%", "21%"], index=0 if st.session_state.iva_choice == "10.5%" else 1, key="iva_input")
    st.session_state.iva_choice = iva_choice
    iva_pct = 10.5 if iva_choice == "10.5%" else 21.0
with pv_col:
    precio_venta = st.number_input("PV Final $", min_value=0.0, value=st.session_state.precio_venta, format="%.2f", key="pv_input")
    st.session_state.precio_venta = precio_venta
with envio_col:
    costo_envio = st.number_input("Valor Unitario Envio $", min_value=0.0, value=st.session_state.costo_envio, format="%.2f", key="envio_input")
    st.session_state.costo_envio = costo_envio

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
    impuestos_pct = st.number_input("Impuestos (%)", min_value=0.0, value=st.session_state.impuestos_pct, format="%.2f", key="impuestos_input")
    st.session_state.impuestos_pct = impuestos_pct
with cuotas_col:
    cuotas_option = st.selectbox(
        "Cuotas",
        options=["Sin cuotas (0%)", "3 cuotas (8.40%)", "6 cuotas (12.30%)", "9 cuotas (15.70%)", "12 cuotas (19.20%)"],
        index=["Sin cuotas (0%)", "3 cuotas (8.40%)", "6 cuotas (12.30%)", "9 cuotas (15.70%)", "12 cuotas (19.20%)"].index(st.session_state.cuotas_option),
        key="cuotas_input"
    )
    st.session_state.cuotas_option = cuotas_option
    cuotas_pct_map = {
        "Sin cuotas (0%)": 0.0,
        "3 cuotas (8.40%)": 8.40,
        "6 cuotas (12.30%)": 12.30,
        "9 cuotas (15.70%)": 15.70,
        "12 cuotas (19.20%)": 19.20
    }
    cuotas_pct = cuotas_pct_map[cuotas_option]
with publicidad_col:
    publicidad_pct = st.number_input("Publicidad (%)", min_value=0.0, value=st.session_state.publicidad_pct, format="%.2f", key="publicidad_input")
    st.session_state.publicidad_pct = publicidad_pct

# --- Helper / mappings -----------------------------------------
def cargo_fijo_por_precio(pv):
    if pv <= 15999.0:
        return 1255.0
    if 16000.0 <= pv <= 23999.0:
        return 2500.0
    if 24000.0 <= pv <= 33000.0:
        return 3030.0
    return 0.0

# --- Cálculo en tiempo real ---
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

# Markup (%) = ganancia / costo_final_con_iva * 100
markup_pct = (profit_per_unit / costo_con_iva * 100.0) if costo_con_iva > 0 else 0.0

# Totales para N unidades
profit_total = profit_per_unit * unidades
revenue_total = precio_venta * unidades
total_costs_total = (costo_con_iva + total_fees_per_unit) * unidades

# --- Sección "Rentabilidades" con borde amarillo que integra los cálculos ---
st.markdown(
    """
    <div style="border: 4px solid #FFD700; border-radius: 10px; padding: 20px; background-color: rgba(255, 215, 0, 0.05);">
        <h2 style="color: #ffffff; text-align: center; margin-top: 0; margin-bottom: 20px;">Rentabilidades</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

# Mostrar: Ganancia Neta Unitaria $, Ganancia Neta % (según tu instrucción), Ganancia total $
# TODO dentro del contenedor con borde amarillo
st.markdown(
    f"""
    <div style="border: 4px solid #FFD700; border-radius: 10px; padding: 20px; background-color: rgba(255, 215, 0, 0.05);">
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
            <div style="text-align: center; padding: 15px; background-color: rgba(102, 51, 153, 0.3); border-radius: 8px;">
                <div style="color:#FFD700; font-weight:700; font-size:14px; margin-bottom: 10px;">Ganancia Neta Unitaria ($)</div>
                <div style="color:#FFD700; font-size:28px; font-weight:900;">${profit_per_unit:,.2f}</div>
            </div>
            <div style="text-align: center; padding: 15px; background-color: rgba(102, 51, 153, 0.3); border-radius: 8px;">
                <div style="color:#FFD700; font-weight:700; font-size:14px; margin-bottom: 10px;">Ganancia Neta (%)</div>
                <div style="color:#FFD700; font-size:28px; font-weight:900;">{markup_pct:.2f}%</div>
            </div>
            <div style="text-align: center; padding: 15px; background-color: rgba(102, 51, 153, 0.3); border-radius: 8px;">
                <div style="color:#FFD700; font-weight:700; font-size:14px; margin-bottom: 10px;">Ganancia total ($)</div>
                <div style="color:#FFD700; font-size:28px; font-weight:900;">${profit_total:,.2f}</div>
            </div>
        </div>
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
st.write(f"- Costos totales por vender (total unidades): ${total_costs_total:,.2f}")
st.write(f"- Ganancia neta total (todas las unidades): ${profit_total:,.2f}")
