import streamlit as st
import streamlit.components.v1 as components
import json
import random
import unicodedata
import re

st.set_page_config(
    page_title="Normalizador Unicode",
    page_icon="🧩",
    layout="centered"
)

WORD_JOINER = "\u2060"

UNICODES_COMPATIBLES = {
    "Non-Breaking Space — U+00A0": "\u00A0",
    "Thin Space — U+2009": "\u2009",
    "Hair Space — U+200A": "\u200A",
    "Word Joiner — U+2060": "\u2060",
}

UNICODES_DETECTABLES = {
    "Zero Width Space — U+200B": "\u200B",
    "Zero Width Non-Joiner — U+200C": "\u200C",
    "Zero Width Joiner — U+200D": "\u200D",
    "Invisible Separator — U+2063": "\u2063",
}

TODOS_UNICODES = {
    **UNICODES_COMPATIBLES,
    **UNICODES_DETECTABLES
}


def agregar_word_joiner_por_palabra(texto):
    partes = re.split(r"(\s+)", texto)
    resultado = []

    for parte in partes:
        if parte.isspace():
            resultado.append(parte)
        elif parte:
            resultado.append(parte + WORD_JOINER)

    return "".join(resultado)


def insertar_unicode_fijo(texto, caracter, cada_n=5, ignorar_espacios=True):
    resultado = []
    contador = 0

    for c in texto:
        resultado.append(c)

        if ignorar_espacios and c.isspace():
            continue

        contador += 1

        if contador % cada_n == 0:
            resultado.append(caracter)

    return "".join(resultado)


def insertar_unicode_solo_en_espacios(texto, caracteres, probabilidad=0.12):
    partes = re.split(r"(\s+)", texto)
    resultado = []

    for parte in partes:
        if parte.isspace():
            if "\n" in parte or "\r" in parte or "\t" in parte:
                resultado.append(parte)
            else:
                if random.random() < probabilidad:
                    resultado.append(random.choice(caracteres))
                else:
                    resultado.append(parte)
        else:
            resultado.append(parte)

    return "".join(resultado)


def limpiar_unicode_invisible(texto):
    invisibles = [
        "\u200B",
        "\u200C",
        "\u200D",
        "\u2060",
        "\u2063",
        "\uFEFF",
        "\u2009",
        "\u200A",
    ]

    for c in invisibles:
        texto = texto.replace(c, "")

    texto = texto.replace("\u00A0", " ")
    return texto


def analizar_unicode(texto):
    conteo = {}

    codigos_detectados = [
        "U+200B",
        "U+200C",
        "U+200D",
        "U+2060",
        "U+2063",
        "U+00A0",
        "U+2009",
        "U+200A",
        "U+FEFF",
    ]

    for c in texto:
        codigo = f"U+{ord(c):04X}"
        nombre = unicodedata.name(c, "SIN NOMBRE")
        clave = f"{codigo} — {nombre}"

        if codigo in codigos_detectados:
            conteo[clave] = conteo.get(clave, 0) + 1

    return conteo


def boton_copiar(texto):
    texto_json = json.dumps(texto)

    components.html(
        f"""
        <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
            <button
                type="button"
                onclick='copiarTexto()'
                style="
                    background: linear-gradient(135deg, #2563eb, #1d4ed8);
                    color: white;
                    border: none;
                    padding: 0.70rem 1rem;
                    border-radius: 10px;
                    cursor: pointer;
                    font-size: 15px;
                    font-weight: 700;
                    box-shadow: 0 4px 12px rgba(37,99,235,.25);
                "
            >
                Copiar texto generado
            </button>

            <span id="copy-msg" style="
                font-weight: 700;
                font-size: 14px;
            "></span>
        </div>

        <script>
            async function copiarTexto() {{
                const texto = {texto_json};
                const msg = document.getElementById("copy-msg");

                try {{
                    if (navigator.clipboard && window.isSecureContext) {{
                        await navigator.clipboard.writeText(texto);
                    }} else {{
                        const textarea = document.createElement("textarea");
                        textarea.value = texto;
                        textarea.style.position = "fixed";
                        textarea.style.left = "-9999px";
                        textarea.style.top = "-9999px";
                        document.body.appendChild(textarea);
                        textarea.focus();
                        textarea.select();
                        document.execCommand("copy");
                        document.body.removeChild(textarea);
                    }}

                    msg.innerText = "Texto copiado correctamente";
                    msg.style.color = "#16a34a";

                    setTimeout(() => {{
                        msg.innerText = "";
                    }}, 2500);

                }} catch (error) {{
                    msg.innerText = "No se pudo copiar automáticamente";
                    msg.style.color = "#dc2626";
                }}
            }}
        </script>
        """,
        height=85
    )


if "resultado" not in st.session_state:
    st.session_state.resultado = ""

if "texto_original" not in st.session_state:
    st.session_state.texto_original = ""


st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.2rem;
            font-weight: 850;
            margin-bottom: 0.2rem;
            line-height: 1.1;
        }

        .subtitle {
            color: #64748b;
            font-size: 1rem;
            margin-bottom: 1.4rem;
        }

        .warning-box {
            background: #fff7ed;
            border: 1px solid #fed7aa;
            color: #9a3412;
            padding: 1rem;
            border-radius: 14px;
            margin-bottom: 1rem;
            font-size: 0.95rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Normalizador y generador Unicode</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Procesa texto Unicode modificando espacios o agregando Word Joiner por palabra.</div>',
    unsafe_allow_html=True
)

col_link1, col_link2 = st.columns(2)

with col_link1:
    st.link_button(
        "Ir a QuillBot",
        "https://quillbot.com/es/detector-de-ia",
        use_container_width=True
    )

with col_link2:
    st.link_button(
        "Ir a Phrasly",
        "https://phrasly.ai/es/ai-detector",
        use_container_width=True
    )


with st.container(border=True):
    texto = st.text_area(
        "Texto original",
        height=170,
        placeholder="Escribe o pega aquí tu texto...",
        key="texto_original"
    )

    modo = st.radio(
        "Modo de procesamiento",
        [
            "Agregar Word Joiner por palabra",
            "Reemplazar solo espacios entre palabras",
            "Inserción fija cada N caracteres",
            "Limpiar Unicode invisible"
        ]
    )

    if modo == "Agregar Word Joiner por palabra":
        st.caption(
            "Agrega U+2060 al final de cada palabra. Mantiene los espacios originales."
        )

    elif modo == "Reemplazar solo espacios entre palabras":
        caracteres_seleccionados = st.multiselect(
            "Caracteres a usar en espacios",
            list(UNICODES_COMPATIBLES.keys()),
            default=[
                "Non-Breaking Space — U+00A0",
                "Thin Space — U+2009"
            ]
        )

        probabilidad = st.slider(
            "Probabilidad de reemplazar espacios",
            min_value=1,
            max_value=100,
            value=15,
            step=1
        )

        st.caption(
            "Este modo no modifica letras internas, solo algunos espacios normales entre palabras."
        )

    elif modo == "Inserción fija cada N caracteres":
        col1, col2 = st.columns(2)

        with col1:
            opcion = st.selectbox(
                "Carácter Unicode",
                list(TODOS_UNICODES.keys())
            )

        with col2:
            cada_n = st.number_input(
                "Insertar cada cuántos caracteres",
                min_value=1,
                max_value=100,
                value=8,
                step=1
            )

        ignorar_espacios = st.checkbox(
            "No insertar después de espacios",
            value=True
        )

        st.warning(
            "Este modo puede afectar correctores ortográficos porque inserta caracteres dentro del texto."
        )

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        generar = st.button(
            "Procesar texto",
            type="primary",
            use_container_width=True
        )

    with col_btn2:
        limpiar = st.button(
            "Limpiar resultado",
            use_container_width=True
        )


if limpiar:
    st.session_state.resultado = ""


if generar:
    if not texto.strip():
        st.warning("Ingresa un texto antes de procesar.")
    else:
        if modo == "Agregar Word Joiner por palabra":
            st.session_state.resultado = agregar_word_joiner_por_palabra(texto)

        elif modo == "Reemplazar solo espacios entre palabras":
            if not caracteres_seleccionados:
                st.warning("Selecciona al menos un carácter Unicode.")
            else:
                caracteres = [
                    UNICODES_COMPATIBLES[x]
                    for x in caracteres_seleccionados
                ]

                st.session_state.resultado = insertar_unicode_solo_en_espacios(
                    texto=texto,
                    caracteres=caracteres,
                    probabilidad=probabilidad / 100
                )

        elif modo == "Inserción fija cada N caracteres":
            caracter = TODOS_UNICODES[opcion]

            st.session_state.resultado = insertar_unicode_fijo(
                texto=texto,
                caracter=caracter,
                cada_n=cada_n,
                ignorar_espacios=ignorar_espacios
            )

        elif modo == "Limpiar Unicode invisible":
            st.session_state.resultado = limpiar_unicode_invisible(texto)


if st.session_state.resultado:
    st.divider()

    st.subheader("Resultado")

    st.text_area(
        "Texto procesado",
        value=st.session_state.resultado,
        height=190,
        key="resultado_area"
    )

    boton_copiar(st.session_state.resultado)

    st.subheader("Vista renderizada")
    st.write(st.session_state.resultado)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.metric(
            "Caracteres originales",
            len(st.session_state.texto_original)
        )

    with col_b:
        st.metric(
            "Caracteres resultado",
            len(st.session_state.resultado)
        )

    with col_c:
        diferencia = len(st.session_state.resultado) - len(st.session_state.texto_original)
        st.metric(
            "Diferencia",
            diferencia
        )

    with st.expander("Análisis Unicode"):
        conteo = analizar_unicode(st.session_state.resultado)

        if conteo:
            for clave, cantidad in conteo.items():
                st.write(f"**{clave}:** {cantidad}")
        else:
            st.success(
                "No se encontraron caracteres Unicode invisibles o especiales conocidos."
            )

    with st.expander("Texto limpio equivalente"):
        texto_limpio = limpiar_unicode_invisible(st.session_state.resultado)

        st.text_area(
            "Texto sin Unicode invisible",
            value=texto_limpio,
            height=140
        )

    st.info(
        "El modo Word Joiner por palabra agrega U+2060 al final de cada palabra sin eliminar los espacios."
    )
