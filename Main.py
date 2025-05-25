import streamlit as st

if 'sds' not in st.session_state:
    st.session_state['sds'] = 0.0
if 'mytitle' not in st.session_state:
    st.session_state['myTitle'] = ""
if "selecteditem" not in st.session_state:
    st.session_state.selecteditem = ""
if "selectedIp" not in st.session_state:
    st.session_state.selectedIp = 0.0
if "UserZvalues" not in st.session_state:
    st.session_state.UserZvalues = ""
if "UserZlabels" not in st.session_state:
    st.session_state.UserZlabels = ""
if "UserHvalues" not in st.session_state:
    st.session_state.UserHvalues = 0.0
if "selectedIe" not in st.session_state:
    st.session_state.selectedIe = 0.0
if "selecteditemStructSys" not in st.session_state:
    st.session_state.selecteditemStructSys = ""
if "selecteditemTa" not in st.session_state:
    st.session_state.selecteditemTa = 0.0
if 'checklist_items' not in st.session_state:
    st.session_state.checklist_items = {}


st.logo("HXBLogo.png", size="large")
main_page= st.Page("Spectra.py", title="ASCE 7-22 Seismic Parameters and Spectra", icon=":material/home:")
create_page = st.Page("Fpcalc.py", title="Fp Calculations", icon=":material/add_circle:")
pg = st.navigation([main_page,create_page])
st.set_page_config(page_title="ASCE722", page_icon=":material/edit:")
pg.run()
