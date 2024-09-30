import streamlit as st

# Side-titel
st.title("Mulige historier")

# Overordnede afsnit
st.header("Mulige vinkler på historier")

st.write(
    """
Her er nogle forslag til journalistiske vinkler, som kan udforskes baseret på kommunernes investeringer:
"""
)

st.write(
    """
- **Kommunens investeringer i usunde virksomheder:** Selv om mange kommuner har vedtaget sundhedspolitikker, 
  investerer de muligvis i virksomheder, der fremmer usunde produkter eller praksisser.
"""
)

st.write(
    """
- **Kommuners politiske holdninger kontra deres investeringer:** Nogle kommuner støtter officielt fredsprocessen mellem Israel og Palæstina, 
  men investerer alligevel i virksomheder, der er på FN's eksklusionsliste for overtrædelser af menneskerettigheder eller etiske retningslinjer.
"""
)

# Fold-ud sektioner med eksempler fra kommuner
st.header("Eksempler fra kommuner")

with st.expander("Eksempel fra Tønder Kommune"):
    st.write(
        """
    Tønder Kommune har en sundhedspolitik, der sigter mod at forbedre borgernes sundhed, men samtidig har de investeringer i virksomheder, 
    der producerer tobak og alkohol. Hvilken påvirkning har dette på kommunens troværdighed og sundhedsmål?
    """
    )

with st.expander("Eksempel fra Næstved Kommune"):
    st.write(
        """
    Næstved Kommune har offentligt støttet fredsprocessen mellem Israel og Palæstina. Samtidig har de investeringer i selskaber, 
    som er inkluderet på FN's eksklusionsliste på grund af deres aktiviteter i de besatte områder. Hvordan harmonerer dette med kommunens politiske udmeldinger?
    """
    )

# Footer
st.write(
    "Disse eksempler kan være udgangspunkt for videre research og journalistiske undersøgelser."
)
