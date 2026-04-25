import streamlit as st
import streamlit.components.v1 as components
import html

st.set_page_config(
    page_title="Generador Unicode Invisible",
    page_icon="🧩",
    layout="centered"
)

INVISIBLES = {
    "Zero Width Space — U+200B": "\u200B",
    "Zero Width Non-Joiner — U+200C": "\u200C",
    "Zero Width Joiner — U+200D": "\u200D",
    "Word Joiner — U+2060": "\u2060",
    "Invisible Separator — U+2063": "\u2063",
    "Non-Breaking Space — U+00A0": "\u00A0",
}

def agregar_invisibles(texto, invisible, cada_n=1, ignorar_espacios=True):
    resultado = []
    contador = 0

    for caracter in texto:
        resultado.append(caracter)

        if ignorar_espacios and caracter.isspace():
            continue

        contador += 1

        if contador % cada_n == 0:
            resultado.append(invisible)

    return "".join(resultado)

def boton_copiar(texto):
    texto_html = html.escape(texto)

    components.html(
        f"""
        <textarea id="textoCopiar" style="position:absolute; left:-9999px;">{texto_html}</textarea>

        <button 
            type="button"
            onclick="
                const textarea = document.getElementById('textoCopiar');
                textarea.focus();
                textarea.select();

                try {{
                    const ok = document.execCommand('copy');
                    const msg = document.getElementById('copy-msg');

                    if (ok) {{
                        msg.innerText = 'Texto copiado correctamente';
                        msg.style.color = '#16a34a';
                    }} else {{
                        msg.innerText = 'No se pudo copiar automáticamente';
                        msg.style.color = '#dc2626';
                    }}

                    setTimeout(() => msg.innerText = '', 2500);
                }} catch (err) {{
                    const msg = document.getElementById('copy-msg');
                    msg.innerText = 'Error al copiar';
                    msg.style.color = '#dc2626';
                }}
            "
            style="
                background: linear-gradient(135deg, #2563eb, #1d4ed8);
                color: white;
                border: none;
                padding: 0.65rem 1rem;
                border-radius: 10px;
                cursor: pointer;
                font-size: 15px;
                font-weight: 600;
                box-shadow: 0 4px 12px rgba(37,99,235,.25);
            "
        >
            Copiar texto generado
        </button>

        <span id="copy-msg" style="
            margin-left: 12px;
            font-weight: 600;
            font-size: 14px;
        "></span>
        """,
        height=80
    )

if "resultado" not in st.session_state:
    st.session_state.resultado = ""

if "texto_original" not in st.session_state:
    st.session_state.texto_original = ""

st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.1rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            color: #64748b;
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }

        .info-box {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 1rem;
            border-radius: 14px;
            margin-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Generador de texto con Unicode invisible</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Inserta caracteres invisibles dentro de un texto y copia el resultado sin perderlo.</div>',
    unsafe_allow_html=True
)

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    st.link_button(
        "Ir a QuillBot",
        "https://quillbot.com/es/detector-de-ia",
        use_container_width=True
    )

with col_btn2:
    st.link_button(
        "Ir a Phrasly",
        "https://phrasly.ai/es/ai-detector",
        use_container_width=True
    )

with st.container(border=True):
    texto = st.text_area(
        "Texto original",
        height=160,
        placeholder="Escribe o pega aquí tu texto...",
        key="texto_original"
    )

    col1, col2 = st.columns(2)

    with col1:
        opcion = st.selectbox(
            "Carácter invisible",
            list(INVISIBLES.keys())
        )

    with col2:
        cada_n = st.number_input(
            "Insertar cada cuántos caracteres",
            min_value=1,
            max_value=50,
            value=1,
            step=1
        )

    ignorar_espacios = st.checkbox(
        "No insertar invisibles después de espacios",
        value=True
    )

    generar = st.button(
        "Generar texto",
        type="primary",
        use_container_width=True
    )

if generar:
    if not texto.strip():
        st.warning("Ingresa un texto antes de generar.")
    else:
        invisible = INVISIBLES[opcion]
        st.session_state.resultado = agregar_invisibles(
            texto,
            invisible,
            cada_n,
            ignorar_espacios
        )

if st.session_state.resultado:
    st.divider()

    st.subheader("Texto generado")

    st.text_area(
        "Resultado",
        value=st.session_state.resultado,
        height=180,
        key="resultado_area"
    )

    boton_copiar(st.session_state.resultado)

    st.subheader("Vista visual")
    st.write(st.session_state.resultado)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.metric("Caracteres originales", len(st.session_state.texto_original))

    with col_b:
        st.metric("Caracteres generados", len(st.session_state.resultado))

    with col_c:
        st.metric(
            "Invisibles agregados",
            len(st.session_state.resultado) - len(st.session_state.texto_original)
        )

    with st.expander("Ver información técnica"):
        invisible_usado = INVISIBLES[opcion]

        st.code(
            f"""
Carácter seleccionado: {opcion}
Unicode real: {invisible_usado.encode("unicode_escape").decode()}
Longitud final: {len(st.session_state.resultado)}
            """.strip()
        )

    st.info(
        "Visualmente el texto puede parecer igual, pero internamente contiene caracteres Unicode invisibles."
    )
