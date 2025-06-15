import streamlit as st
import random
from math import sqrt

st.set_page_config(page_title="Damage Calculators", layout="centered")

st.title("⚔️ Damage Calculators")

tab1, tab2, tab3 = st.tabs(["Ranged Attack", "Physical Attack", "Rules"])

with tab1:
    st.header("Ranged Attack Damage Calculator")
    WeaponA = st.number_input("Weapon Attack", min_value=0, value=10, key="ranged_attack")
    attack_type = st.selectbox("Attack Type", ["Normal", "Holy", "Unholy"], key="ranged_atk_type")
    defense_type = st.selectbox("Defense Type", ["Normal", "Holy", "Unholy"], key="ranged_def_type")
    WeaponM = st.number_input("Proficiency Multiplier(%)",
                              min_value=-100, max_value=100, value=0, step=10, key="ranged_mult")
    modifier = st.number_input("Modifier", value=0, key="ranged_mod")
    defence = st.number_input("Defense(%)", min_value=-100, max_value=100, value=0, step=10, key="ranged_def")

    distance1 = st.number_input("X Distance", value=0, key="x_dist")
    distance2 = st.number_input("Y Distance", value=0, key="y_dist")
    distance3 = sqrt((distance1 ** 2) + (distance2 ** 2))

    miss_threshold = max(1, min(20, int(round((distance3 / 1.25) + 1))))
    distance_penalty = max(0.5, 1 - (distance3 / 20))

    defence /= 100
    WeaponM /= 100

    if st.button("Calculate Ranged Damage"):
        D20 = random.randint(1, 20)

        effectiveness = 1.5 if (attack_type, defense_type) in [("Holy", "Unholy"), ("Unholy", "Holy")] else 1.0

        if D20 == 20:
            damage = ((WeaponA * (1 + WeaponM)) * 2) * (1 - defence) * effectiveness * distance_penalty + modifier
            st.success("CRITICAL HIT!")
        elif D20 == 1:
            damage = ((WeaponA * (1 + WeaponM)) / 2) * (1 - defence) * effectiveness * distance_penalty + modifier
            st.warning("GLANCING BLOW!")
        else:
            damage = (((WeaponA * (1 + WeaponM)) * (0.8 + (D20 - 10) / 50)) *
                      (1 - defence) * effectiveness * distance_penalty + modifier)

        st.write(f"**Miss Threshold = {miss_threshold}**")
        st.write(f"**D20 Roll = {D20}**")

        if D20 < miss_threshold:
            st.error("MISS")
        else:
            st.write(f"**Damage = {round(damage, 2)}**")


with tab2:
    st.header("Physical Attack Damage Calculator")
    WeaponA = st.number_input("Weapon Attack", min_value=0, value=10, key="phys_attack")
    attack_type = st.selectbox("Attack Type", ["Normal", "Holy", "Unholy"], key="phys_atk_type")
    defense_type = st.selectbox("Defense Type", ["Normal", "Holy", "Unholy"], key="phys_def_type")
    WeaponM = st.number_input("Proficiency Multiplier(%)",
                              min_value=-100, max_value=100, value=0, step=10, key="phys_mult")
    modifier = st.number_input("Modifier", value=0, key="phys_mod")
    defence = st.number_input("Defense(%)", min_value=-100, max_value=100, value=0, step=10, key="phys_def")

    defence /= 100
    WeaponM /= 100

    if st.button("Calculate Physical Damage"):
        D20 = random.randint(1, 20)
        st.write(f"**D20 Roll = {D20}**")

        effectiveness = 1.5 if (attack_type, defense_type) in [("Holy", "Unholy"), ("Unholy", "Holy")] else 1.0

        if D20 == 20:
            damage = ((WeaponA * (1 + WeaponM)) * 2) * (1 - defence) * effectiveness + modifier
            st.success("CRITICAL HIT!")
        elif D20 == 1:
            damage = ((WeaponA * (1 + WeaponM)) / 2) * (1 - defence) * effectiveness + modifier
            st.warning("GLANCING BLOW!")
        else:
            damage = ((WeaponA * (1 + WeaponM)) * (0.8 + (D20 - 10) / 50)) * (1 - defence) * effectiveness + modifier

        st.write(f"**Damage = {round(damage, 2)}**")

with tab3:
    st.title("Rules")
    stat_option = st.selectbox('Stats', ["Select", "Physical Attack", "Ranged Attack", "Health", "Defence"])

    if stat_option == "Physical Attack":
        st.write("The Attack (ATK) stat represents a character's "
                 "offensive power, determining how much damage "
                 "dealt with melee strikes. Eg: swords, knives, clubs. ")

        st.write("damage = ((physicalA * (1 + WeaponM)) * (0.8 + (D20 - 10) / 50))"
                 " * (1 - defence) * effectiveness + modifier")

    elif stat_option == "Ranged Attack":
        st.write("Ranged Attack represents a character’s ability to hit targets with ranged weapons "
                 "(e.g., bows, crossbows, throwing weapons) and is influenced by the distance between "
                 "the attacker and the target.")

        st.markdown(
            "<p style='font-size:13px;'>"
            "damage = (((RangedA * (1 + WeaponM)) * (0.8 + (D20 - 10) / 50)) * "
            "(1 - defence) * effectiveness * distance_penalty + modifier)"
            "</p>",
            unsafe_allow_html=True
        )

        st.image("ranged_example_final.png")

        st.write("the miss threshold is calculated using the 2 distances, "
                 "and it increases the likely hood of missing with distance")
        st.write("miss threshold = distance3 / 1.25")
        st.write("if the D20 roll < the miss threshold, an attack will miss ")

        st.write("the distance penalty is also calculated using distance, "
                 "and decreases the final damage output with distance")
        st.write("distance penalty = 1 - (distance3 / 20)")

    elif stat_option == "Health":
        st.write("The Health (HP) stat represents a character’s total life force. "
                 "When HP reaches 0, the character is dead. HP is reduced when taking "
                 "damage and can be restored through  spells, potions. ")

    elif stat_option == "Defence":
        st.write("The Defense (DEF) stat represents a character’s ability to reduce incoming damage. "
                 "A higher DEF value means the character takes less damage from physical attacks."
                 "for example, a charactor with 50% defence will take 50% less damage.")
