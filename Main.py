import streamlit as st



st.logo("HXBLogo.png", size="large")
main_page= st.Page("Spectra.py", title="ASCE 7-22 Seismic Parameters and Spectra", icon=":material/home:")
create_page = st.Page("Fpcalc.py", title="Fp Calculations", icon=":material/add_circle:")
pg = st.navigation([main_page,create_page])
st.set_page_config(page_title="ASCE722", page_icon=":material/edit:")
pg.run()
if 'sds' not in st.session_state:
    st.session_state['sds'] = 0.0
if 'mytitle' not in st.session_state:
    st.session_state['mytitle'] = ""
