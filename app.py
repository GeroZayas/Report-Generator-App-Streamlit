import streamlit as st
from docxtpl import DocxTemplate
import os
import sys
from pathlib import Path

# import time

st.set_page_config(page_title="Futur Idiomes - Report Generator", page_icon="📑")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def validate_input(input_value):
    if input_value in ["--", "NA"]:
        return True
    try:
        float(input_value)
        return True
    except ValueError:
        return False


def delete_temp_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def main():
    st.title("📑 Futur Idiomes - Report Generator (v0.5)")

    # Form inputs
    student = st.text_input("Student:")
    level = st.selectbox(
        "Level:",
        ["Young Learners", "Starters", "Movers", "Flyers", "KET", "PET", "FCE"],
    )
    teacher = st.text_input("Teacher:")
    period = st.selectbox(
        "Periodo:", ["1er Trimestre", "2ndo Trimestre", "3er Trimestre"]
    )
    # ========================================================================================
    # GENERAL MARKS

    st.markdown("### General Marks")
    col1, col2 = st.columns(2)

    with col1:
        asistencia = st.number_input("Asistencia:", min_value=1, max_value=10)
        asimilacion = st.number_input(
            "Asimilación de material nuevo:", min_value=1, max_value=10
        )
        aprendizaje = st.number_input("Aprendizaje/Deberes:", min_value=1, max_value=10)

    with col2:
        participacion = st.number_input(
            "Participación en clase/Interés:", min_value=1, max_value=10
        )
        comportamiento = st.number_input("Comportamiento:", min_value=1, max_value=10)
        progreso = st.number_input(
            "Progreso durante del trimestre:", min_value=1, max_value=10
        )
    # ========================================================================================

    # ========================================================================================
    # EXAM MARKS
    st.markdown("### Exam Marks")
    prueba = st.selectbox(
        "Prueba:", ["Trimestral", "Final", "Final (Simulación de examen FCE)"]
    )
    st.info("'--' -> no se evaluó en la prueba | 'NA' -> no asistió a la prueba")

    col3, col4 = st.columns(2)

    with col3:
        listening = st.number_input(
            "Listening:", value=0.0, step=1.0, format="%f", max_value=10.0
        )
        reading_use_language = st.number_input(
            "Reading and Use of Language:",
            value=0.0,
            step=1.0,
            format="%f",
            max_value=10.0,
        )
    with col4:
        writing = st.number_input(
            "Writing:", value=0.0, step=1.0, format="%f", max_value=10.0
        )
        speaking = st.number_input(
            "Speaking:", value=0.0, step=1.0, format="%f", max_value=10.0
        )
    # ========================================================================================

    st.markdown("### Comentario")
    comentario = st.text_area("Comentario:", height=100, max_chars=350)

    despedida = st.text_input("Despedida:", "¡Felices Vacaciones!")

    if st.button(
        "Generate Report", key="generate", help="Generate Report", type="primary"
    ):
        # Validate inputs
        general_marks_valid = all(
            validate_input(mark)
            for mark in [
                asistencia,
                asimilacion,
                aprendizaje,
                participacion,
                comportamiento,
                progreso,
            ]
        )
        exam_marks_valid = all(
            validate_input(mark)
            for mark in [listening, reading_use_language, writing, speaking]
        )

        if general_marks_valid and exam_marks_valid:
            output_path = generate_report(
                student,
                level,
                teacher,
                period,
                asistencia,
                asimilacion,
                aprendizaje,
                participacion,
                comportamiento,
                progreso,
                prueba,
                listening,
                reading_use_language,
                writing,
                speaking,
                comentario,
                despedida,
            )
            with open(output_path, "rb") as file:
                btn = st.download_button(
                    label="Download Report",
                    data=file,
                    file_name=f"{student}-{level}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    on_click=delete_temp_files,
                    args=(os.path.dirname(output_path),),
                )

        else:
            st.error("Please enter valid marks (numbers, '--', or 'NA')")

    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: green;
            color: white;
        }
        div.stButton > button[data-baseweb='button'] {
            background-color: blue;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("##### Made with ❤️ by [Gero Zayas](https://www.gerozayas.com)")


def generate_report(
    student,
    level,
    teacher,
    period,
    asistencia,
    asimilacion,
    aprendizaje,
    participacion,
    comportamiento,
    progreso,
    prueba,
    listening,
    reading_use_language,
    writing,
    speaking,
    comentario,
    despedida,
):
    document_path = resource_path(Path(__file__).parent / "./model.docx")
    doc = DocxTemplate(document_path)

    values = {
        "STUDENT": student,
        "LEVEL": level,
        "TEACHER": teacher,
        "PERIOD": period,
        "ASISTENCIA": asistencia,
        "ASIMILACION": asimilacion,
        "APRENDIZAJE": aprendizaje,
        "PARTICIPACION": participacion,
        "COMPORTAMIENTO": comportamiento,
        "PROGRESO": progreso,
        "PRUEBA": prueba,
        "LISTENING": listening,
        "READING_USE_LANGUAGE": reading_use_language,
        "WRITING": writing,
        "SPEAKING": speaking,
        "COMENTARIO": comentario,
        "DESPEDIDA": despedida,
    }

    try:
        result_total = (
            float(values["LISTENING"])
            + float(values["READING_USE_LANGUAGE"])
            + float(values["WRITING"])
            + float(values["SPEAKING"])
        ) / 4
        values["TOTAL"] = round(result_total, 1)
    except Exception:
        values["TOTAL"] = "..."

    doc.render(values)
    output_dir = os.path.join(os.getcwd(), "GENERATED_REPORTS")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(
        output_dir, f"{values['STUDENT']}-{values['LEVEL']}.docx"
    )
    doc.save(output_path)

    return output_path


if __name__ == "__main__":
    main()
