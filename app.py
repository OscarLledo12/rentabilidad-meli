import streamlit as st

st.set_page_config(page_title="Calculadora de comisiones - Mercado Libre AR", layout="wide")

st.title("Calculadora de comisiones - Mercado Libre Argentina (ejemplo)")

st.markdown(
    """
    Esta aplicación calcula el desglose de comisiones y la ganancia neta a partir del Precio de Venta Final, Costo (con IVA) y Peso.
    - Las tasas por defecto son sólo ejemplos. Actualizá las tasas según las condiciones reales de Mercado Libre y Mercado Pago.
    - Si tenés dudas sobre las tasas actuales consultá la ayuda de Mercado Libre.
    """
)

# Inputs
with st.sidebar:
    st.header("Parámetros de la venta")
    precio_venta = st.number_input("Precio de Venta Final (ARS)", value=10000.0, min_value=0.0, step=100.0, format="%.2f")
    costo_con_iva = st.number_input("Costo con IVA (ARS)", value=6000.0, min_value=0.0, step=100.0, format="%.2f")
    peso_kg = st.number_input("Peso (kg)", value=1.0, min_value=0.0, step=0.1, format="%.3f")
    vendedor_paga_envio = st.checkbox("El vendedor paga el envío (incluir costo de envío)", value=True)

    st.markdown("### Tasas (editable)")
    preset = st.selectbox(
        "Preset de comisión Mercado Libre (ejemplo)",
        ("Ejemplo: 12% (genérica)", "Ejemplo: 15% (electrónica)", "Ejemplo: 18% (repuestos)", "Personalizar")
    )

    if preset == "Ejemplo: 12% (genérica)":
        ml_fee_pct = st.number_input("Comisión Mercado Libre (%)", value=12.0, min_value=0.0, format="%.2f")
    elif preset == "Ejemplo: 15% (electrónica)":
        ml_fee_pct = st.number_input("Comisión Mercado Libre (%)", value=15.0, min_value=0.0, format="%.2f")
    elif preset == "Ejemplo: 18% (repuestos)":
        ml_fee_pct = st.number_input("Comisión Mercado Libre (%)", value=18.0, min_value=0.0, format="%.2f")
    else:
        ml_fee_pct = st.number_input("Comisión Mercado Libre (%)", value=12.0, min_value=0.0, format="%.2f")

    iva_pct = st.number_input("IVA sobre la comisión (%)", value=21.0, min_value=0.0, format="%.2f")
    aplicar_iva_comision = st.checkbox("Aplicar IVA sobre la comisión de Mercado Libre", value=True)
    mp_fee_pct = st.number_input("Comisión Mercado Pago (%) (ejemplo)", value=7.5, min_value=0.0, format="%.2f")
    mp_fixed_fee = st.number_input("Comisión Mercado Pago fija por operación (ARS)", value=0.0, min_value=0.0, format="%.2f")

    st.markdown("### Envío (configurable)")
    shipping_rate_per_kg = st.number_input("Tarifa de envío por kg (ARS)", value=400.0, min_value=0.0, format="%.2f")
    shipping_fixed = st.number_input("Costo de envío fijo por paquete (ARS)", value=0.0, min_value=0.0, format="%.2f")

    st.markdown("### Cálculo de precio mínimo")
    desired_margin_pct = st.number_input("Margen deseado (%) sobre el precio de venta", value=15.0, min_value=0.0, format="%.2f")

# Calculations
def calculate_breakdown(precio, costo, peso, vendedor_paga_envio,
                        ml_fee_pct, iva_pct, aplicar_iva_comision,
                        mp_fee_pct, mp_fixed_fee,
                        shipping_rate_per_kg, shipping_fixed,
                        desired_margin_pct):
    # Shipping
    shipping_cost = 0.0
    if vendedor_paga_envio:
        shipping_cost = shipping_rate_per_kg * peso + shipping_fixed

    # Comisiones variables (proporcionales al precio de venta)
    ml_commission = precio * (ml_fee_pct / 100.0)
    iva_on_ml_commission = ml_commission * (iva_pct / 100.0) if aplicar_iva_comision else 0.0
    mp_commission = precio * (mp_fee_pct / 100.0) + mp_fixed_fee

    # Totales
    total_costs = costo + ml_commission + iva_on_ml_commission + mp_commission + shipping_cost
    profit = precio - total_costs
    margin_pct = (profit / precio * 100.0) if precio > 0 else 0.0

    # Price minimum for desired margin:
    # We solve precio such that profit/precio = desired_margin_pct/100
    # profit = precio - (costo + shipping + mp_fixed_fee) - precio*(ml_fee + mp_fee + iva_ml_on_mlfee)
    # => precio*(1 - total_var_rate - desired_margin) = costo + shipping + mp_fixed_fee
    ml_fee_rate = ml_fee_pct / 100.0
    mp_fee_rate = mp_fee_pct / 100.0
    iva_on_ml_rate = (ml_fee_pct * iva_pct) / 10000.0 if aplicar_iva_comision else 0.0
    total_var_rate = ml_fee_rate + mp_fee_rate + iva_on_ml_rate

    denom = 1.0 - total_var_rate - (desired_margin_pct / 100.0)
    price_for_desired_margin = None
    if denom > 0:
        price_for_desired_margin = (costo + shipping_cost + mp_fixed_fee) / denom
    else:
        price_for_desired_margin = None  # imposible con esas tasas/margen

    return {
        "precio": precio,
        "costo_con_iva": costo,
        "peso_kg": peso,
        "shipping_cost": shipping_cost,
        "ml_commission": ml_commission,
        "iva_on_ml_commission": iva_on_ml_commission,
        "mp_commission": mp_commission,
        "total_costs": total_costs,
        "profit": profit,
        "margin_pct": margin_pct,
        "price_for_desired_margin": price_for_desired_margin,
        "total_var_rate": total_var_rate
    }

res = calculate_breakdown(
    precio_venta, costo_con_iva, peso_kg, vendedor_paga_envio,
    ml_fee_pct, iva_pct, aplicar_iva_comision,
    mp_fee_pct, mp_fixed_fee,
    shipping_rate_per_kg, shipping_fixed,
    desired_margin_pct
)

# Display results
st.subheader("Desglose y resultados")
col1, col2, col3 = st.columns(3)

col1.metric("Precio de venta (ARS)", f"{res['precio']:,.2f}")
col1.metric("Costo con IVA (ARS)", f"{res['costo_con_iva']:,.2f}")
col1.metric("Peso (kg)", f"{res['peso_kg']:.3f}")

col2.metric("Comisión ML (ARS)", f"{res['ml_commission']:,.2f}")
col2.metric("IVA sobre comisión ML (ARS)", f"{res['iva_on_ml_commission']:,.2f}")
col2.metric("Comisión MP (ARS)", f"{res['mp_commission']:,.2f}")

col3.metric("Costo de envío (ARS)", f"{res['shipping_cost']:,.2f}")
col3.metric("Costos totales (ARS)", f"{res['total_costs']:,.2f}")
col3.metric("Ganancia neta (ARS)", f"{res['profit']:,.2f}")

st.write("---")
st.markdown("### Resumen detallado")
st.table({
    "Concepto": [
        "Precio de venta",
        "Costo con IVA",
        "Comisión Mercado Libre",
        "IVA sobre comisión ML",
        "Comisión Mercado Pago (incl. fija)",
        "Costo envío (si aplica)",
        "Costos totales",
        "Ganancia neta",
        "Margen sobre venta (%)"
    ],
    "ARS": [
        f"{res['precio']:,.2f}",
        f"{res['costo_con_iva']:,.2f}",
        f"{res['ml_commission']:,.2f}",
        f"{res['iva_on_ml_commission']:,.2f}",
        f"{res['mp_commission']:,.2f}",
        f"{res['shipping_cost']:,.2f}",
        f"{res['total_costs']:,.2f}",
        f"{res['profit']:,.2f}",
        f"{res['margin_pct']:.2f}%"
    ]
})

st.write("---")
st.subheader("Cálculo de precio mínimo para margen deseado")
if res["price_for_desired_margin"] is None:
    st.error("No es posible alcanzar el margen deseado con las tasas y costos actuales (denominador ≤ 0). Reducí el margen deseado o las comisiones.")
else:
    st.success(f"Precio mínimo aproximado para {desired_margin_pct:.2f}% de margen: ARS {res['price_for_desired_margin']:,.2f}")

st.markdown(
    """
    Notas:
    - Este cálculo aplica las comisiones proporcionales sobre el Precio de Venta Final.
    - La IVA sobre la comisión se aplica sólo si se activa la opción (checkbox).
    - Ajustá las tasas según la categoría y plan de publicación de Mercado Libre y la condición de Mercado Pago.
    - No incluye retenciones impositivas adicionales, costos fijos operativos, ni costos logísticos internos.
    """
)

st.markdown("#### Enlaces útiles (actualizá según fuente oficial):")
st.markdown("- [Ayuda Mercado Libre Argentina](https://www.mercadolibre.com.ar/ayuda)")
st.markdown("- Revisá la sección de tarifas/comisiones en tu cuenta de Mercado Libre / Mercado Pago para valores exactos.")
