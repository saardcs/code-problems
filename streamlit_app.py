import streamlit as st
import random
import math

st.title("Combinations & Password Generator Practice")

# Define character pools
char_pools = {
    'lowercase': 26,
    'uppercase': 26,
    'numbers': 10
}

def readable_chars(char_types):
    names = {
        'lowercase': 'a–z (lowercase)',
        'uppercase': 'A–Z (uppercase)',
        'numbers': '0–9 (numbers)'
    }
    return ", ".join([names[c] for c in char_types])

# Generate a problem
def generate_problem():
    char_types = random.sample(list(char_pools.keys()), k=random.randint(1, 3))
    allow_repeat = random.choice([True, False])
    code_length = random.randint(3, 5)

    total_chars = sum([char_pools[c] for c in char_types])

    if allow_repeat:
        formula_parts = [str(total_chars)] * code_length
        total_combinations = total_chars ** code_length
    else:
        formula_parts = [str(total_chars - i) for i in range(code_length)]
        total_combinations = math.prod([int(x) for x in formula_parts])

    return {
        "char_types": char_types,
        "allow_repeat": allow_repeat,
        "code_length": code_length,
        "formula_parts": formula_parts,
        "total_combinations": total_combinations
    }

# Store problems
if "problems" not in st.session_state:
    st.session_state.problems = [generate_problem() for _ in range(5)]

for idx, problem in enumerate(st.session_state.problems):
    st.subheader(f"Problem {idx + 1}")

    st.markdown(f"**Code Length:** {problem['code_length']} characters")
    st.markdown(f"**Character Types:** {readable_chars(problem['char_types'])}")
    st.markdown(f"**Repetition Allowed:** {'Yes' if problem['allow_repeat'] else 'No'}")

    correct_formula = " × ".join(problem["formula_parts"])
    correct_total = str(problem["total_combinations"])

    # User Inputs
    user_formula = st.text_input(
        f"👉 Enter the multiplication steps (e.g., 62 × 61 × 60):",
        key=f"formula_{idx}"
    )
    user_total = st.text_input(
        "👉 Enter the total number of combinations:",
        key=f"total_{idx}"
    )

    # Normalize formula input
    def normalize_formula(input_str):
        return input_str.replace("*", "×").replace("x", "×").replace(" ", "")

    if user_formula and user_total:
        normalized_input = normalize_formula(user_formula)
        normalized_answer = correct_formula.replace(" ", "")

        if normalized_input == normalized_answer and user_total == correct_total:
            st.success("✅ Correct!")
        else:
            st.error("❌ Incorrect.")
            with st.expander("Show correct calculation"):
                st.markdown(f"**Correct formula:** {correct_formula}")
                st.markdown(f"**Correct total:** {correct_total}")

# Button to regenerate problems
if st.button("🔁 Generate New Problems"):
    st.session_state.problems = [generate_problem() for _ in range(5)]
    st.rerun()
