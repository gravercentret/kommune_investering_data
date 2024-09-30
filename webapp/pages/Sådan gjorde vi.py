import streamlit as st

# Side-titel
st.title("Sådan gjorde vi")

# Metode introduktion
st.header("Metode og tilgang")

st.markdown(
    """
Læs mere om reglerne på området osv...
"""
)

# Fold-ud sektioner
with st.expander("Reglerne på området:"):
    st.markdown(
        """
    Det er tilladt for kommuner og regioner at investere direkte i stats- eller realkreditobligationer eller obligationer, der frembyder en tilsvarende sikkerhed.
    Men kommuner og regioner må ikke anbringe midler direkte i aktier.
    Dog kan de anbringe midler i investeringsforeninger, der investerer i aktier og dermed eje andele af disse aktier og få del i såvel udbytte som evt. kursstigninger.
    Det følger af kommunalfuldmagtsreglerne (de uskrevne regler om kommunernes opgavevaretagelse), at kommuner som udgangspunkt ikke må drive erhvervsvirksomhed, herunder handel, håndværk, industri og finansiel virksomhed, medmindre der er lovhjemmel til det.
    Forbuddet mod at drive kommunal erhvervsvirksomhed er for det første begrundet i, at kommunerne har til opgave at udføre opgaver, der kommer almenvellet til gode. For det andet er det begrundet i et ønske om at undgå konkurrenceforvridning i forhold til den private sektor.
    **Kilde: Indenrigs- og Sundhedsministeriet**

    """
    )

with st.expander("Databehandling"):
    st.write(
        """
    Vi har renset og struktureret dataene, så de kunne analyseres. Dette inkluderede fjernelse af irrelevante oplysninger, 
    håndtering af manglende værdier og kodning af variabler.
    """
    )

with st.expander("Analysemetoder"):
    st.write(
        """
    De analyserede data er blevet bearbejdet ved hjælp af statistiske værktøjer, hvor vi har fokuseret på 
    at identificere tendenser og mønstre, der kunne belyse de problemstillinger, vi ønskede at undersøge.
    """
    )

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
