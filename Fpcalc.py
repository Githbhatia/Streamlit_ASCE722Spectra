import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import math

def persistent_toggle(label, key):
    state = st.toggle(label, value=st.session_state.checklist_items.get(key, False), key=key)
    st.session_state.checklist_items[key] = state
    return state

for k, v in st.session_state.items():
    st.session_state[k] = v
sds  = st.session_state['sds']
sds_latex = "S_{DS}"
sd1_latex = "S_{D1}"
st.subheader(":blue[ASCE7-22 Fp Calculation]")
st.write("USING THE DEFAULT OPTIONS WILL LEAD TO CONSERVATIVE RESULTS")
if not st.session_state.clicked:
    st.write (f"Please click on :red[RUN] button in the previous page to get Sds for this site")
    st.write (f"To proceed anyways, manually enter:red[${sds_latex}$]")

FP="F_{p}"
if st.session_state['myTitle'] == "":
    mysite = st.text_input("Title for report", placeholder="Enter title for report", key="title")
else:
    mysite = st.text_input("Title for report",st.session_state['myTitle'], key="title")
st.session_state['myTitle'] = st.session_state['title']
if sds <= 0.0:
    sds = st.number_input(f"Enter ${sds_latex}$", value= sds, format="%0.3f", min_value=0.0)
else:
    sds = st.number_input(f"${sds_latex}$, as obtained in previous page, can modify here", value= sds, format="%0.3f")
if sds <= 0.0:
    st.write(f":red[Enter a valid value for ${sds_latex}$]")
    st.stop()


df = pd.read_csv('ASCE722Ch13.csv')
df.set_index('Menuitems', inplace=True)
if st.session_state.selecteditem != "":
    _selecteditem = st.session_state.selecteditem
    selecteditem = st.selectbox("Select Nonstructural item (ASCE 7-22 Tables 13.5-1 and 13.6-1)",df.index, index = list(df.index).index(_selecteditem), key="nonstructural")
else:
    selecteditem = st.selectbox("Select Nonstructural item (ASCE 7-22 Tables 13.5-1 and 13.6-1)",df.index, index = 1, key="nonstructural")

st.session_state.selecteditem = st.session_state.nonstructural

car0 = df.loc[selecteditem].values[0]
car1 = df.loc[selecteditem].values[1]
rPO = df.loc[selecteditem].values[2]
omegaOP = df.loc[selecteditem].values[3]

sc1,sc2 =st.columns(2)
with sc1:
    I_p = "I_{p}"
    if st.session_state.selectedIp != 0.0:
        iP = float(st.selectbox(f"${I_p}$, Component Importance Factor",(1.0,1.5), index = list((1.0,1.5)).index(st.session_state.selectedIp), key="Ip"))   
    else:
        iP = float(st.selectbox(f"${I_p}$, Component Importance Factor",(1.0,1.5), index = 1, key="Ip"))
    st.session_state.selectedIp = iP
   

sc3,sc4 =st.columns(2)
with sc3:
    Z = "Z"
    # z = st.number_input(f"${Z}$, height above base",value= 90.0)
    if st.session_state.UserZvalues != "":
        zStr = st.text_input(f"${Z}$, height above base (multiple ok,separate with commas)",value= st.session_state.UserZvalues,  key="zvalues")

    else:
        zStr = st.text_input(f"${Z}$, height above base (multiple ok,separate with commas)",str("0, 15, 30, 45, 60, 75, 90, 100"),key="zvalues")

st.session_state.UserZvalues = st.session_state.zvalues


if st.session_state.UserZlabels != "":
    zLbl = st.text_input("Labels corresponding to Z values (Separate with commas,Optional)",st.session_state.UserZlabels, key="zLables")
else:
    zLbl = st.text_input("Labels corresponding to Z values (Separate with commas,Optional)",str("Grnd Level, Level 2, Level 3, Level 4, Level 5, Level 6, Mech Level, Roof"),key="zLables")
zLblist = [i.strip() for i in zLbl.split(",")]
st.session_state.UserZlabels = st.session_state.zLables

try:
    z =[float(i) for i in zStr.split(",")]
except ValueError:
    st.write(":red[Invalid input, Please enter numbers separated by commas]")
    st.stop()

if len(z) > len(zLblist):
    for i in range(len(z)-len(zLblist)):
        zLblist.append("")
if len(z) < len(zLblist):
    for i in range(len(zLblist)-len(z)):
        zLblist.pop()

with sc4:
    H = "H"
    if st.session_state["UserHvalues"] != 0.0:
        h = st.number_input(f"${H}$, Average roof height of structure in ft",value= st.session_state["UserHvalues"], key="H")
    else:
        h = st.number_input(f"${H}$, Average roof height of structure in ft",value= 100.0, key="H")
    st.session_state.UserHvalues = st.session_state.H
    if h < max(z):
        st.write(":red[H is < highest value of z, Please correct]")
        st.stop()

st.divider()
knownstsys = persistent_toggle("Structural System Selection (Unknown system assumed if not enabled)", key="structuralselect")
if knownstsys:
    dfs = pd.read_csv('ASCE722StructuralSystems.csv')
    dfs.set_index('StructuralSystem', inplace=True)
    if st.session_state.selecteditemStructSys != "":
        _selecteditem = st.session_state.selecteditemStructSys
        selecteditem = st.selectbox("Select Structural System of the Building (ASCE 7-22 Table 12.2-1):",dfs.index, index = list(dfs.index).index(_selecteditem), key="structural") 
        st.session_state.selecteditemStructSys = st.session_state.structural
    else:   
        selecteditem = st.selectbox("Select Structural System of the Building (ASCE 7-22 Table 12.2-1):",dfs.index, index = 49, key="structural")
        st.session_state.selecteditemStructSys = st.session_state.structural
    
    
    r = dfs.loc[selecteditem].values[0]
    oM = dfs.loc[selecteditem].values[1]
I_e = "I_{e}"
if st.session_state["selectedIe"] != 0.0:
    ie = float(st.selectbox(f"${I_e}$, Importance Factor for Building",(1.0,1.25,1.5), index = list((1.0,1.25,1.5)).index(st.session_state["selectedIe"]), key="Ie"))
else:
    ie = float(st.selectbox(f"${I_e}$, Importance Factor for Building",(1.0,1.25,1.5), index = 2, key="Ie"))
st.session_state["selectedIe"] = st.session_state.Ie
st.write(f"Selected Structural System: {selecteditem}")
if knownstsys:
    c1,c2 = st.columns(2)
    with c1:
        R= "R"
        st.write(f"${R}$, Response modification Value = "+ str(round(r,2)))
    with c2:
        Om = "\\Omega_{o}"
        st.write(f"${Om}$ = " + str(round(oM,2)))

    rU = max((1.1*(r/(ie*oM)))**0.5, 1.3)
else:
    rU = 1.3
st.write(":red[ASCE 7-22 Equation 13.3-6:]")
st.latex(r'''\color{red} R_{\mu} = \left[ \frac{1.1 R}{I_{e}\Omega_{o}} \right]^{1/2} \ge 1.3''')
Ru = "R_{\\mu}"
st.write(f"${Ru}$ = " +str(round(rU,3)) + " (1.0 used for z = 0.0 per ASCE 7-22 13.3.1.2)")

st.divider()
knownperiod = persistent_toggle("Period Known (if not enabled, period is calculated based on Height H)", key="periodselect")
# st.write(st.session_state)
if knownperiod:
    Ta = "T_{a}"
    if st.session_state.selecteditemTa != 0.0:
        tA = st.number_input(f"${Ta}$, Lowest fundamental period of structure:",value= st.session_state.selecteditemTa, key="Ta")
    else:
        tA = st.number_input(f"${Ta}$, Lowest fundamental period of structure:",value= 0.5, key="Ta")
    st.session_state.selecteditemTa = st.session_state.Ta
else:
    tA = 0.02*h**0.75
    Ta = "T_{a} = C_t H^x = "
    st.write(f"Per ASCE 7-22 Eq 12.8-8 (for \"all other structural systems\"):" )
    st.write(f"${Ta}$ " +str(round(tA,3))+ " secs")
st.divider()

def getHf(zhratio):
    a1 = min(1/tA,2.5)
    a2 = max((1-(0.4/tA)**2),0.0)
    hF = 1+ a1*zhratio + a2*zhratio**10 
    # print ("Hf = " + str(hF))   
    return(hF)

zhlist = np.concatenate((np.array([0.0,0.001]),np.arange(0.002, 1.001, 0.001)),axis=0)

zh = [None]*len(z);hF = [None]*len(z);fP = [None]*len(z)
fPMax = 1.6*sds*iP
fPMin = 0.3*sds*iP
fPMaxstr = "1.6 S_{DS} I_p W_p"
fPMinstr = "0.3 S_{DS} I_p W_p"
for i in range(len(z)):
    zh[i] =z[i]/h
    hF[i] = getHf(zh[i])
# Hf = "H_{f}"
# st.write(f"${Hf}$ = " +str(round(hF,3)))
    if z[i] == 0.0:
        fP[i] = 0.4*sds*iP*(hF[i]/1.0)*(car0/rPO)
    else:
        fP[i] = 0.4*sds*iP*(hF[i]/rU)*(car1/rPO)

    fP[i] = min(max(fP[i],fPMin),fPMax)


Wp = "W_{p}"
st.write(":red[ASCE 7-22 Equation 13.3-1:]")
st.latex(r'''\color{red} F_{p} = 0.4 S_{DS} I_{p} \left( \frac{H_{f}}{R_{\mu}} \right) \left( \frac{C_{AR}}{R_{po}} \right) W_{p}''')
c1,c2 = st.columns(2)
with c1:
    tfPmin=str(round(fPMin,3))
    st.write(f":red[Minimum ${FP}$ = ${fPMinstr}$ = {tfPmin} ${Wp}$]")
with c2:
    tfmax=str(round(fPMax,3))
    st.write(f":red[Maximum ${FP}$ = ${fPMaxstr}$ = {tfmax} ${Wp}$]")
c1,c2 = st.columns(2)
with c1:
    CAR0 = "C_{AR}"
    if math.isnan(car0):
        st.write(f"${CAR0}$ supported at or below grade plane = N/A" )
    else:
        st.write(f"${CAR0}$ supported at or below grade plane = " + str(car0))
with c2:
    CAR1 = "C_{AR}"
    st.write(f"${CAR1}$ above grade plane,supported by structure = " + str(car1))   
Rpo = "R_{PO}"
st.write(f"${Rpo}$ = " + str(rPO))
Omop = "\\Omega_{op}"
st.write(f" ${Omop}$ to be used for concrete or masonry post-installed anchors = " + str(round(omegaOP,3)) )

fPlist = []
for i in range(len(zhlist)):
    hFL = getHf(zhlist[i])
    if zhlist[i] == 0.0:
        fPlist.append(min(max(0.4*sds*iP*(hFL/1.0)*(car0/rPO),fPMin),fPMax))
    else:
        fPlist.append(min(max(0.4*sds*iP*(hFL/rU)*(car1/rPO),fPMin),fPMax))
st.write(f":blue[Governing ${FP}$:]")
dfsfP=pd.DataFrame({"Location":zLblist,"Z":z,"Z/H": zh,"Hf": hF, "Fp/Wp": fP})
st.dataframe(dfsfP, hide_index=True)

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)
ax.plot(fPlist, zhlist, label="Calculated Fp", color='Red', linewidth=1.0)
for i in range(len(z)):
    ax.plot(fP[i], zh[i], marker='o', label="Governing Fp", color='Black', linestyle='--', linewidth=2.0)
    axmin,axmax = ax.get_xlim()
    arrowlength = (axmax - axmin)/20
    if z[i] >0.85* h:
        ax.annotate(f"{round(fP[i],3)} at " + str(z[i]) + " ("+ zLblist[i] + ")", ha = 'right', xy=(fP[i], zh[i]), xytext=(fP[i]-arrowlength, zh[i]+0.005), arrowprops=dict(facecolor='black', shrink=0.05))
    else:       
        ax.annotate(f"{round(fP[i],3)} at " + str(z[i]) + " ("+ zLblist[i] + ")", xy=(fP[i], zh[i]), xytext=(fP[i]+arrowlength, zh[i]+0.005), arrowprops=dict(facecolor='black', shrink=0.05))
ax.grid()
ax.set_xlabel("Fp/Wp")
ax.set_ylabel("Z/H")
ax.set_title("Variation of Fp with Z/H")
info = (mysite[:100] + '..') if len(mysite) > 100 else mysite
ax.text(0.99, 0.08, info, horizontalalignment='right', verticalalignment='top', fontsize=10, color ='Black',transform=ax.transAxes)
ax.text(0.99, 0.05, "Sds = "+str(round(sds,3)), horizontalalignment='right', verticalalignment='top', fontsize=10, color ='Black',transform=ax.transAxes)
info = (st.session_state['nonstructural'][:150] + '..') if len(st.session_state['nonstructural']) > 150 else st.session_state['nonstructural']
ax.text(0.99, 0.02, info, horizontalalignment='right', verticalalignment='top', fontsize=6, color ='Black',transform=ax.transAxes)
st.pyplot(fig)
