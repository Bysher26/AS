import streamlit as st
import pandas as pd
import re
from dosage_calculator import DosageCalculator
from translations import get_translation, LANGUAGES

st.set_page_config(
    page_title="Medical Dosage Calculator",
    page_icon="💊",
    layout="wide"
)

if 'language' not in st.session_state:
    st.session_state.language = 'en'

def main():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(get_translation("title", st.session_state.language))
        st.markdown(get_translation("subtitle", st.session_state.language))
    with col2:
        language = st.selectbox(
            "Language",
            options=['en', 'ar'],
            format_func=lambda x: "🇺🇸 EN" if x == 'en' else "🇸🇦 AR",
            index=0 if st.session_state.language == 'en' else 1,
            key="language_selector",
            label_visibility="collapsed",
        )

    if language != st.session_state.language:
        st.session_state.language = language
        st.rerun()

    col1, col2, col3 = st.columns(3)
    with col1:
        weight_col1, weight_col2 = st.columns([2, 1])
        with weight_col1:
            weight = st.number_input(get_translation("weight", st.session_state.language), min_value=0.1, max_value=300.0, value=70.0, step=0.1, format="%.1f")
        with weight_col2:
            weight_unit = st.selectbox(get_translation("weight_unit", st.session_state.language), options=['kg', 'lbs'], index=0, key="weight_unit_selector")

    with col2:
        age_col1, age_col2 = st.columns([2, 1])
        with age_col1:
            if st.session_state.get("age_unit_selector", "years") == 'years':
                age = st.number_input(label=get_translation("age", st.session_state.language), min_value=0, max_value=120, value=30, step=1, key="age_input")
            else:
                age = st.number_input(label=get_translation("age", st.session_state.language), min_value=0, max_value=1440, value=360, step=1, key="age_input")
        with age_col2:
            age_unit = st.selectbox("", options=['years', 'months'], index=0 if st.session_state.get("age_unit_selector", "years") == 'years' else 1, key="age_unit_selector")

    with col3:
        st.write("")
        calculate_button = st.button(get_translation("calculate", st.session_state.language), type="primary")

    weight_kg = weight if weight_unit == 'kg' else weight * 0.453592
    age_years = age if age_unit == 'years' else age / 12

    if weight_kg <= 0:
        st.error(get_translation("weight_error", st.session_state.language))
        return

    if age < 0:
        st.error(get_translation("age_error", st.session_state.language))
        return

    calculator = DosageCalculator(weight_kg, age_years)

    if calculate_button or weight_kg > 0:
        st.markdown("---")
        st.subheader(get_translation("patient_info", st.session_state.language))
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.metric(get_translation("weight", st.session_state.language), f"{weight_kg:.1f} kg")
        with info_col2:
            age_display = f"{age} " + get_translation(age_unit, st.session_state.language)
            st.metric(get_translation("age", st.session_state.language), age_display)
        st.markdown("---")

        display_medication_category("airway_defib", calculator.get_airway_defib_medications())
        display_medication_category("intubation", calculator.get_intubation_medications())
        display_medication_category("emergencies", calculator.get_emergency_medications())
        display_medication_category("inotropes", calculator.get_inotropes())
        display_medication_category("sedation", calculator.get_sedation_paralysis())
        display_medication_category("antihypertensives", calculator.get_antihypertensives())
        display_medication_category("antiarrhythmics", calculator.get_antiarrhythmics())
        display_medication_category("others", calculator.get_others())

def display_medication_category(category_key, medications):
    if not medications:
        return
    st.subheader(get_translation(category_key, st.session_state.language))
    if category_key in ['inotropes', 'sedation', 'antihypertensives', 'antiarrhythmics', 'others']:
        display_infusion_medications(medications)
    elif category_key == 'airway_defib':
        for med in medications:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(f"**{med['name']}**")
            with col2:
                st.write(f"{med['dosage']} - {med['route']}")
            st.markdown("---")
    else:
        for med in medications:
            col1, col2, col3 = st.columns([2, 2, 3])
            with col1:
                st.write(med['name'])
            with col2:
                st.write(med['dosage'])
            with col3:
                st.write(med['route'])
        st.markdown("---")

def display_infusion_medications(medications):
    for i, med in enumerate(medications):
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                st.write(f"**{med['name']}**")
                st.caption(f"Weight: {med['dosage']}")

            with col2:
                route = med['route']
                match = re.search(r'(\d+\.?\d*)-(\d+\.?\d*)', route)
                unit_match = re.search(r'(mcg/kg/h|mcg/kg/min|mg/kg/h|units/kg/h)', route)

                if match and unit_match:
                    min_dose = float(match.group(1))
                    max_dose = float(match.group(2))
                    unit = unit_match.group(1)

                    # Generate clean step intervals
                    if max_dose <= 1:
                        step = 0.1
                    elif max_dose <= 10:
                        step = 0.5
                    else:
                        step = 1
                    options = [round(min_dose + i * step, 2) for i in range(int((max_dose - min_dose) / step) + 1)]

                    st.write(f"Range: {options[0]} – {options[-1]} {unit}")
                    selected_dose = st.selectbox(
                        "Select rate:",
                        options=options,
                        index=len(options)//2,
                        key=f"dose_{i}_{med['name']}"
                    )

                    with col3:
                        weight_kg = float(med['dosage'].split()[0])
                        total_dose = selected_dose * weight_kg

                        if unit == 'mcg/kg/min':
                            dose_mcg_per_hr = total_dose * 60
                            dose_mg_per_hr = dose_mcg_per_hr / 1000
                        elif unit == 'mcg/kg/h':
                            dose_mg_per_hr = total_dose / 1000
                        elif unit == 'mg/kg/h':
                            dose_mg_per_hr = total_dose
                        elif unit == 'units/kg/h':
                            dose_mg_per_hr = total_dose
                        else:
                            dose_mg_per_hr = None

                        # Determine volume (default 50 mL unless adrenaline)
                        volume_ml = 20 if 'adrenaline' in med['name'].lower() else 50

                        if dose_mg_per_hr is not None:
                            concentration = med.get('concentration', dose_mg_per_hr / volume_ml)
                            infusion_rate_ml_hr = dose_mg_per_hr / concentration
                            st.metric("Infusion Rate", f"{infusion_rate_ml_hr:.1f} mL/h")
                            st.caption(f"Add **{dose_mg_per_hr:.2f} mg** to {volume_ml} mL NS")
                        else:
                            st.write("Unsupported unit")
                else:
                    st.write(route)

if __name__ == "__main__":
    main()
