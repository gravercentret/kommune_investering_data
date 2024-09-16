import streamlit as st

# Side-titel
st.title("Sådan gjorde vi")

# Metode introduktion
st.header("Metode og tilgang")

st.write("""
I dette projekt har vi anvendt en kombination af kvantitative og kvalitative metoder 
for at sikre en grundig og objektiv analyse af data.
""")

# Fold-ud sektioner
with st.expander("Dataindsamling"):
    st.write("""
    Dataene til projektet blev indsamlet fra en række offentligt tilgængelige databaser, 
    herunder statistikker fra Danmarks Statistik og sundhedsdata fra de danske regioner.
    Derudover har vi gennemført interviews med eksperter inden for området for at få deres perspektiver.
    """)

with st.expander("Databehandling"):
    st.write("""
    Vi har renset og struktureret dataene, så de kunne analyseres. Dette inkluderede fjernelse af irrelevante oplysninger, 
    håndtering af manglende værdier og kodning af variabler.
    """)

with st.expander("Analysemetoder"):
    st.write("""
    De analyserede data er blevet bearbejdet ved hjælp af statistiske værktøjer, hvor vi har fokuseret på 
    at identificere tendenser og mønstre, der kunne belyse de problemstillinger, vi ønskede at undersøge.
    """)

# Liste med links til hjemmesider
st.header("Kilder og yderligere information")
st.write("Her er nogle af de kilder, vi har brugt i projektet:")

links = {
    "Danmarks Statistik": "https://www.dst.dk/",
    "Sundhedsdatastyrelsen": "https://www.sundhedsdatastyrelsen.dk/",
    "Regionernes hjemmesider": "https://www.regioner.dk/",
}

for name, url in links.items():
    st.write(f"[{name}]({url})")

# Footer
st.write("Har du spørgsmål til metoden, er du velkommen til at kontakte os.")
