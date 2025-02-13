
import numpy as np
import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim
import urllib.request as ur
import json as js
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

        
def onclick():

    global address, lat,longt, textout, riskct, sitecl

    if swv != 0.0:
        try:
            shearwavevel = float(swv)
        except ValueError:
            st.write("Invalid Shear Wave Velocity:"+ "Enter shear wave velocity in ft/sec and try again")
            return
        if shearwavevel==0:
            st.write("Invalid Shear Wave Velocity:"+ "Enter a non-zero shear wave velocity in ft/sec and try again")
            return
        shearwavevellimits = [('F',0.0),('E',500.0),('DE',700.0),('D',1000.0),('CD',1450.0),('C',2100.0),('BC',3000.0),('B',5000.0),('A',1000000.0)]
        centershearwave = [('E',500.0),('DE',600.0),('D',849.0),('CD',1200.0),('C',1732.0),('BC',2500.0),('B',3536.0),('A',1000000.0)]
        index = 0
        for a, b in shearwavevellimits:
            if shearwavevel <= b:
                sitecl = a
                break
        prev =0
        for a, b in centershearwave:
            if shearwavevel > b:
                sitecll = a
                prev = b
        if shearwavevel <= 500.0:
            sitecll = "E"
                
        for a, b in centershearwave:
            if shearwavevel <= b:
                siteclu = a
                siteclBMultp = (shearwavevel - prev)/(b- prev)
                break
                
        if estimatedswv==1:
            for a, b in shearwavevellimits:
                if shearwavevel/1.3 <= b:
                    sitecll = a
                    break
            for a, b in shearwavevellimits:
                if shearwavevel*1.3 <= b:
                    siteclu = a
                    break
        placeholdersc.selectbox("Site Class",siteClassList,index = siteClassList.index(sitecl), key="replaced")    
    elif siteclass=="Default":
        sitecl = "CD"
        siteclu = "C"
        sitecll = "D"
    else:
        sitecl = siteclass
    if sitecl == 'F': 
        st.write("Invalid Shear Wave Velocity:" + "Site Class F, Requires site response analysis studies")
        return(0)
    
    #print(sitecll+" "+siteclu)
    #print(siteclBMultp)

    
    ctx = ssl.create_default_context(cafile=certifi.where())
    #ctx = ssl._create_unverified_context()
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = Nominatim(user_agent="ASCE722Spectra", scheme='https')
    sitetitle = mysite
    riskct = riskc
    address = addressg

    if address =="":
        lat = latitude
        longt = longitude
        location = geolocator.reverse(str(lat) + " ," + str(longt))
        address = str(location.address)
        st.write("Using "+ address)

    else:
        location = geolocator.geocode(address)
        if (location != None):
            lat = str(location.latitude)
            longt = str(location.longitude)
            address = str(location.address)
            st.write("Using "+ str(lat) + ", " + str(longt))
        else:
            st.write("Invalid Address:" + "Invalid address, revise address and try again")
            return()
    
    df = pd.DataFrame({"lat":[float(lat)], "lon":[float(longt)]})
    st.map(df)      


    url = 'https://earthquake.usgs.gov/ws/designmaps/asce7-22.json?latitude='+ str(lat) + '&longitude=' + str(longt) +'&riskCategory='+ riskct +'&siteClass=' + sitecl + '&title=Example'
    
    if  swv != 0.0 or siteclass=="Default":
        urll = 'https://earthquake.usgs.gov/ws/designmaps/asce7-22.json?latitude='+ str(lat) + '&longitude=' + str(longt) +'&riskCategory='+ riskct +'&siteClass=' + sitecll + '&title=Example'
        urlu = 'https://earthquake.usgs.gov/ws/designmaps/asce7-22.json?latitude='+ str(lat) + '&longitude=' + str(longt) +'&riskCategory='+ riskct +'&siteClass=' + siteclu + '&title=Example'
        

    try:
        response = ur.urlopen(url)
        if swv != 0.0 or siteclass=="Default":
            responsel = ur.urlopen(urll)
            responseu = ur.urlopen(urlu)
    except ur.URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            return()
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            return()

    

    rdata = js.loads(response.read())
    if swv != 0.0 or siteclass=="Default":           
        rdatal = js.loads(responsel.read())
        rdatau = js.loads(responseu.read())

    # if self.SaveJson.get() == 1:
    #     with open("ASCE722.json", "w") as write_file:
    #         js.dump(rdata, write_file)
    #     if str(self.entry_SWVel.get()) != "" or str(self.SelectedSiteClass.get())=="Default":
    #         with open("ASCE722_lowerbound.json", "w") as write_file:
    #             js.dump(rdatal, write_file)
    #         with open("ASCE722_upperbound.json", "w") as write_file:
    #             js.dump(rdatau, write_file)

    output = 'Output for Latitude = ' + str(lat) + ' Longitude = ' + str(longt)
    t = rdata["response"]["data"]["multiPeriodDesignSpectrum"]["periods"]
    s = rdata["response"]["data"]["multiPeriodDesignSpectrum"]["ordinates"]

    t2 = rdata["response"]["data"]["twoPeriodDesignSpectrum"]["periods"]
    s2 = rdata["response"]["data"]["twoPeriodDesignSpectrum"]["ordinates"]
        
    tmce = rdata["response"]["data"]["multiPeriodMCErSpectrum"]["periods"]
    smce = rdata["response"]["data"]["multiPeriodMCErSpectrum"]["ordinates"]



    tmce2 = rdata["response"]["data"]["twoPeriodMCErSpectrum"]["periods"]
    smce2 = rdata["response"]["data"]["twoPeriodMCErSpectrum"]["ordinates"]

    if swv != 0.0 or siteclass=="Default":    
        tl = rdatal["response"]["data"]["multiPeriodDesignSpectrum"]["periods"]
        sl = rdatal["response"]["data"]["multiPeriodDesignSpectrum"]["ordinates"]
        
        tu = rdatau["response"]["data"]["multiPeriodDesignSpectrum"]["periods"]
        su = rdatau["response"]["data"]["multiPeriodDesignSpectrum"]["ordinates"]

        tmcel = rdatal["response"]["data"]["multiPeriodMCErSpectrum"]["periods"]
        smcel = rdatal["response"]["data"]["multiPeriodMCErSpectrum"]["ordinates"]

        tmceu = rdatau["response"]["data"]["multiPeriodMCErSpectrum"]["periods"]
        smceu = rdatau["response"]["data"]["multiPeriodMCErSpectrum"]["ordinates"]

    fig = plt.figure(figsize=(10, 10))
    ax = fig.subplots(2,1)
    ax[0].set_xlabel('Period')
    ax[0].set_title(sitetitle + " Design Spectrum")

    ax[1].set_xlabel('Period')
    ax[1].set_title(sitetitle + " MCE Spectrum")

    if (estimatedswv and swv != 0.0):

        sg = [max(sl,s,su) for sl,s,su in zip(sl,s,su)]
        ax[0].plot(t, sl, label="Multiperiod Des Spec lower bound SC= "+ sitecll, color='Red', linewidth=1.0)
        ax[0].plot(t, s, label="Multiperiod Des Spec SC= " + sitecl, color='Blue', linewidth=1.0)
        ax[0].plot(t, su, label="Multiperiod Des Spec upper bound SC= "+ siteclu, color='Green', linewidth=1.0)
        ax[0].plot(t, sg, label="Govering Multiperiod Des Spec", color='Black', linestyle='--', linewidth=2.0)
        ax[0].set_xlim([0, 5])
        ax[0].legend()  
        ax[0].grid()
        smcel = rdatal["response"]["data"]["multiPeriodMCErSpectrum"]["ordinates"]
        smceu = rdatau["response"]["data"]["multiPeriodMCErSpectrum"]["ordinates"]
        smceg = [max(smcel,smce,smceu) for smcel,smce,smceu in zip(smcel,smce,smceu)]
        ax[1].plot(tmce, smcel, label="MCE Multiperiod lower bound SC= "+ sitecll, color='Red', linewidth=1.0)
        ax[1].plot(tmce, smce, label="MCE Multiperiod Spec SC= " + sitecl, color='Blue', linewidth=1.0)
        ax[1].plot(tmce, smceu, label="MCE Multiperiod upper bound SC= "+ siteclu, color='Green', linewidth=1.0)
        ax[1].plot(tmce, smceg, label="Govering MCE Multiperiod", color='Black', linestyle='--', linewidth=2.0)
        ax[1].set_xlim([0, 5])
        ax[1].legend() 
        ax[1].grid()
        
        
        sds = 0.9 * max(sg[t.index(0.2):t.index(5.0)])
        sd1min = sg[t.index(1.0)]
        sd1 = 0.0
        if shearwavevel > 1450:
            for i in range(t.index(1.0), t.index(2.0)+1):
                sd1 = max(0.9*sg[i]*t[i], sd1)
            sd1=max(sd1,sd1min)
        elif shearwavevel <= 1450:
            for i in range(t.index(1.0), t.index(5.0)+1):
                sd1 = max(0.9*sg[i]*t[i], sd1)
            sd1=max(sd1,sd1min)

        st.subheader("ASCE7-22 Seismic Parameter Output")
        st.write("Based on est. shear wave velocity per ASCE 7-22 Section 20.3 and 21.4")
        df = pd.DataFrame(
        {'Parameter':["sms","sm1","sds","sd1","pga"],'Values':[str(round(sds*1.5,3)),str(round(sd1*1.5,3)),str(round(sds,3)),str(round(sd1,3)),str(round(sg[0],3))]}
        )
        df.set_index('Parameter', inplace=True)
        st.dataframe(df)
        textout = mywritefileEstSV(t, sg, tmce, smceg, sds, sd1, sitecl)
       
    elif siteclass=="Default":   

        sg = [max(sl,s,su) for sl,s,su in zip(sl,s,su)]
        ax[0].plot(t, sl, label="Multiperiod Des Spec lower bound SC= "+ sitecll, color='Red', linewidth=1.0)
        ax[0].plot(t, s, label="Multiperiod Des Spec SC= " + sitecl, color='Blue', linewidth=1.0)
        ax[0].plot(t, su, label="Multiperiod Des Spec upper bound SC= "+ siteclu, color='Green', linewidth=1.0)
        ax[0].plot(t, sg, label="Govering Multiperiod Des Spec", color='Black', linestyle='--', linewidth=2.0)
        ax[0].set_xlim([0, 5])
        ax[0].legend()  
        ax[0].grid()
        smcel = rdatal["response"]["data"]["multiPeriodMCErSpectrum"]["ordinates"]
        smceu = rdatau["response"]["data"]["multiPeriodMCErSpectrum"]["ordinates"]
        smceg = [max(smcel,smce,smceu) for smcel,smce,smceu in zip(smcel,smce,smceu)]
        ax[1].plot(tmce, smcel, label="MCE Multiperiod lower bound SC= "+ sitecll, color='Red', linewidth=1.0)
        ax[1].plot(tmce, smce, label="MCE Multiperiod Spec SC= " + sitecl, color='Blue', linewidth=1.0)
        ax[1].plot(tmce, smceu, label="MCE Multiperiod upper bound SC= "+ siteclu, color='Green', linewidth=1.0)
        ax[1].plot(tmce, smceg, label="Govering MCE Multiperiod", color='Black', linestyle='--', linewidth=2.0)
        ax[1].set_xlim([0, 5])
        ax[1].legend() 
        ax[1].grid()
 

        sds = 0.9 * max(sg[t.index(0.2):t.index(5.0)])
        sd1 = sg[t.index(1.0)]
        st.subheader("ASCE7-22 Seismic Parameter Output")
        st.write("Default = Max of Site Class C, CD, D")
        df = pd.DataFrame(
        {'Parameter':["sms","sm1","sds","sd1","pga"],'Values':[str(round(sds*1.5,3)),str(round(sd1*1.5,3)),str(round(sds,3)),str(round(sd1,3)),str(round(sg[0],3))]}
        )
        df.set_index('Parameter', inplace=True)
        st.dataframe(df)
        textout = mywritefileEstSV(t, sg, tmce, smceg, sds, sd1, sitecl)

    elif  swv != 0.0:
        sexp = np.array(su)*siteclBMultp + np.array(sl)*(1-siteclBMultp)
        sexpmce = np.array(smceu)*siteclBMultp + np.array(smcel)*(1-siteclBMultp)
        ax[0].plot(t, s, label="Multiperiod Design Spectrum for " + sitecl, color='Red', linewidth=1.0)
        ax[0].plot(t2, s2, label="2-Period Design Spectrum for " + sitecl, color='Green', linewidth=1.0)
        #ax[0].plot(tl, sl, label="Lower Bound Design Spectrum for" + sitecll, color='black', linewidth=0.1)
        ax[0].plot(tl, sexp, label="Interpolated Spectrum for " + str(round(shearwavevel,0)) + " ft/s", color='black', linestyle='--', linewidth=1.0)
        ax[0].set_xlim([0, 5])
        ax[0].legend()
        ax[0].grid()
        ax[1].plot(tmce, smce, label="MCE Multiperiod Spectrum", color='Blue', linewidth=1.0)
        ax[1].plot(tmce2, smce2, label="MCE 2-Period  Spectrum", color='Green', linewidth=1.0)
        ax[1].plot(tmcel, sexpmce, label="Interpolated mCE Spectrum for " + str(round(shearwavevel,0)) + " ft/s", color='black', linestyle='--', linewidth=1.0)
        ax[1].set_xlim([0, 5])
        ax[1].legend()
        ax[1].grid()
        p = rdata["response"]["data"].items()
        st.subheader("ASCE7-22 Seismic Parameter Output")
        df = pd.DataFrame(p)
        df = df[0:11]
        df.columns = ['Parameter','Values']
        df['Values'] = df['Values'].astype(str)
        df.set_index('Parameter', inplace=True)
        st.dataframe(df)
        textout = mywritefileest(rdata, sitecl, sexp)
    else:
        ax[0].plot(t, s, label="Multiperiod Design Spectrum for" + sitecl, color='Red', linewidth=1.0)
        ax[0].plot(t2, s2, label="2-Period Design Spectrum for" + sitecl, color='Green', linewidth=1.0)
        ax[0].set_xlim([0, 5])
        ax[0].legend()
        ax[0].grid()
        ax[1].plot(tmce, smce, label="MCE Multiperiod Spectrum", color='Blue', linewidth=1.0)
        ax[1].plot(tmce2, smce2, label="MCE 2-Period  Spectrum", color='Green', linewidth=1.0)
        ax[1].set_xlim([0, 5])
        ax[1].legend()
        ax[1].grid()
        p = rdata["response"]["data"].items()
        st.subheader("ASCE7-22 Seismic Parameter Output")
        df = pd.DataFrame(p)
        df = df[0:11]
        df.columns = ['Parameter','Values']
        df['Values'] = df['Values'].astype(str)
        df.set_index('Parameter', inplace=True)
        st.dataframe(df)
        textout = mywritefile(rdata, sitecl)

    st.pyplot(fig)

    return()

def contourf(lat, longt, riskct):
    sitecl = siteclass
    nlong = 7
    nlat= 7
    gridspacing = 0.5/60.0
    lat = float(lat)
    longt = float(longt)
    latgrid = np.arange(lat+(nlat//2)*gridspacing, lat-((nlat//2)+0.9)*gridspacing, -gridspacing)
    longgrid = np.arange(longt-(nlong//2)*gridspacing, longt+((nlong//2)+0.9)*gridspacing, gridspacing)
    xLong,xLat = np.meshgrid(longgrid,latgrid)
    ZSDS=np.zeros((nlong,nlat)); ZSD1=np.zeros((nlong,nlat))
    st.write("Grid Used:")
    df = pd.DataFrame({"lat":xLat.flatten(), "lon":xLong.flatten()})
    st.map(df)  
    mesg = st.empty()

    for i in range(nlong):
        for j in range(nlat):
            mesg.write("Getting gird " + str(i) + ", " + str(j))
            url = 'https://earthquake.usgs.gov/ws/designmaps/asce7-22.json?latitude='+ str(xLat[i,j]) + '&longitude=' + str(xLong[i,j]) +'&riskCategory='+ riskct +'&siteClass=' + sitecl + '&title=Example'
            try:
                response = ur.urlopen(url)

            except ur.URLError as e:
                if hasattr(e, 'reason'):
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                    return()
                elif hasattr(e, 'code'):
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)
                    return() 
            rdata = js.loads(response.read())
            ZSDS[i,j] = rdata["response"]["data"]["sds"]
            ZSD1[i,j] = rdata["response"]["data"]["sd1"]
    mesg.write("Completed")
    #print(ZSDS, ZSD1)
    fig = plt.figure(figsize=(10, 20))
    ax = fig.add_subplot(211)
    CS = ax.contour(xLong,xLat,ZSDS) 
    ax.set_title('Local Variation of SDS around site')
    ax.text(longt,lat , '. Site '+ str(ZSDS[nlong//2, nlat//2]), fontsize = 10)
    ax.clabel(CS, inline=True, fontsize=10)
    ax = fig.add_subplot(212)
    CS2 = ax.contour(xLong,xLat,ZSD1) 
    ax.set_title('Variation of SD1 around site')
    ax.text(longt, lat, '. Site '+ str(ZSD1[nlong//2, nlat//2]), fontsize = 10)
    ax.clabel(CS2, inline=True, fontsize=10)

    st.pyplot(fig)



def mywritefileEstSV(t, sg, tmce, smceg, sds, sd1, sitecl):
    sitetitle = mysite
    riskct = riskc

    textout = ""

    textout += "Data source is USGS (ASCE 722 Database) and OpenStreetMaps.\nAuthors do not assume any responsibility or liability for its accuracy.\n"
    textout += "Use of the output of this program does not imply approval by the governing building code bodies responsible for building code approval and interpretation for the building site described by latitude/longitude location.\n"
    textout += "Written by HXB\n \n \n"
    textout += sitetitle + "\n" + address + "\n"
    textout += "The location is " + str(lat) + ", " + str(longt) +  " and Risk Category "+ riskct + "\n"
    if (estimatedswv and swv == 0.0):
        textout += "Site Class based on an estimated shear wave velocity of " + str(swv) + "ft/s\n"
        textout += "Lower bound and upper bound site class considered in computation per ASCE 7-22 Section 20.3 and 21.4" + "\n"
    else:
        textout += "Default Site Class based on max of Site Class C, CD, D\n"
    textout += "sms from governing design spectra = " + str(round(sds*1.5, 3)) + "\n"
    textout += "sm1 from governing design spectra = " + str(round(sd1*1.5, 3)) + "\n"
    textout += "sds from governing design spectra = " + str(round(sds, 3)) + "\n"
    textout += "sd1 from governing design spectra = " + str(round(sd1, 3)) + "\n"
    textout += "pga from governing design spectra = " + str(round(sg[0], 3)) + "\n"
    textout += "Governing MultiPeriodDesignSpectrum\n"
    index = len(t)
    j = 0
    while j < index:
        textout += str(t[j])+ ", " + str(sg[j])+"\n"
        j+= 1
    textout += "Governing MultiPeriodMCErSpectrum\n"
    index = len(tmce)
    j = 0
    while j < index:
        textout += str(tmce[j])+ ", " + str(smceg[j])+"\n"
        j+= 1
    return(textout)




def mywritefile( ldata, sitecl):
    sitetitle = mysite
    riskct = riskc

    textout = ""
    index = 0
    p = ldata["response"]["data"]
    t = ldata["response"]["data"]["multiPeriodDesignSpectrum"]["periods"]
    s = ldata["response"]["data"]["multiPeriodDesignSpectrum"]["ordinates"]
    tmce = ldata["response"]["data"]["multiPeriodMCErSpectrum"]["periods"]
    smce = ldata["response"]["data"]["multiPeriodMCErSpectrum"]["ordinates"]
    textout += "Data source is USGS (ASCE 722 Database) and OpenStreetMaps.\nAuthors do not assume any responsibility or liability for its accuracy.\n"
    textout += "Use of the output of this program does not imply approval by the governing building code bodies responsible for building code approval and interpretation for the building site described by latitude/longitude location.\n"
    textout += "Written by HXB\n \n \n"
    textout += sitetitle + "\n" + address + "\n"
    textout += "The location is " + str(lat) + ", " + str(longt) + " with Site Class " + sitecl + " and Risk Category "+ riskct + "\n"
    if swv != 0.0:
        textout += "Site Class based on a shear wave velocity of " + str(swv) + "ft/s\n"
    textout += "pga from design spectra = " + str(round(s[0], 3)) + "\n"
    for key, value in p.items():
        if index <= 11:
            textout += str(key)+ ", " + str(value)+"\n"  
        index += 1
    
    textout += "MultiPeriodDesignSpectrum\n"
    index = len(t)
    j = 0
    while j < index:
        textout += str(t[j])+ ", " + str(s[j])+"\n"
        j+= 1
    textout += "MultiPeriodMCErSpectrum\n"
    index = len(tmce)
    j = 0
    while j < index:
        textout += str(tmce[j])+ ", " + str(smce[j])+"\n"
        j+= 1
    return(textout)


def mywritefileest(ldata, sitecl, sexp):
    sitetitle = mysite
    riskct = riskc

    textout = ""
    index = 0
    p = ldata["response"]["data"]
    t = ldata["response"]["data"]["multiPeriodDesignSpectrum"]["periods"]
    s = ldata["response"]["data"]["multiPeriodDesignSpectrum"]["ordinates"]
    tmce = ldata["response"]["data"]["multiPeriodMCErSpectrum"]["periods"]
    smce = ldata["response"]["data"]["multiPeriodMCErSpectrum"]["ordinates"]
    textout += "Data source is USGS (ASCE 722 Database) and OpenStreetMaps.\nAuthors do not assume any responsibility or liability for its accuracy.\n"
    textout += "Use of the output of this program does not imply approval by the governing building code bodies responsible for building code approval and interpretation for the building site described by latitude/longitude location.\n"
    textout += "Written by HXB\n \n \n"
    textout += sitetitle + "\n" + address + "\n"
    textout += "The location is " + str(lat) + ", " + str(longt) + " with Site Class " + sitecl + " and Risk Category "+ riskct + "\n"
    if swv != 0.0 :
        textout += "Site Class based on a shear wave velocity of " + str(swv) + "ft/s\n"
    textout += "pga from design spectra = " + str(round(s[0], 3)) + "\n"
    for key, value in p.items():
        if index <= 11:
            textout += str(key)+ ", " + str(value)+"\n"     
        index += 1
    
    textout += "MultiPeriodDesignSpectrum\n"
    index = len(t)
    j = 0
    while j < index:
        textout += str(t[j])+ ", " + str(s[j])+"\n"
        j+= 1

    textout += "Interpolated MultiPeriodDesignSpectrum\n"
    index = len(t)
    j = 0
    while j < index:
        textout += str(t[j])+ ", " + str(sexp[j])+"\n"
        j+= 1
    textout += "MultiPeriodMCErSpectrum\n"
    index = len(tmce)
    j = 0
    while j < index:
        textout += str(tmce[j])+ ", " + str(smce[j])+"\n"
        j+= 1
    return(textout)


global rr


rr=0
st.subheader("ASCE7-22 Seismic Parameter Input")

mysite = st.text_input("Title for report","My Site")
st.write("Either enter Shear Wave Velocity or pick Site Class" )
st.write("(Shear Wave Velocity will be used when entered)")

t1, t2 = st.tabs(["Shear Wave Velocity", "Site Class"])
with t1:
    swv= st.number_input("Shear Wave Velocity (ft/s)",0.0)
    estimatedswv= st.checkbox("Estimated Shear Wave Velocity?")

with t2:
    placeholdersc = st.empty()
    siteClassList=["A","B","BC","C","CD","D","DE","E", "Default"]
    siteclass = placeholdersc.selectbox("Site Class",siteClassList,index = 4,key="original")
st.divider()

RiskCategoryList=["I","II","III","IV"]
riskc = st.selectbox("Risk Category",RiskCategoryList, index = 3)

st.divider()
st.write("Either provide Address or Lat/Long Pair (leave Address blank)")

tab1, tab2 = st.tabs(["Address", "Lat/Long"])

with tab1:
    addressg = st.text_input("Address", "", placeholder="123, streat name, city, CA")

with tab2:
    latitude= st.number_input("Latitude",38)
    longitude= st.number_input("Longitude",-121)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button('Run', on_click=click_button)

if st.session_state.clicked:
    onclick()
    st.subheader("Download output file")
    sfile= st.checkbox("Save output file")
    if sfile:
        st.download_button("Save output file", textout, file_name="respspectra.txt",)


if st.session_state.clicked:
    st.subheader("ASCE7-22 Local Variation")
    st.write("Computed for selected site class only,\n Will take some time depending on latency of USGS website,\n Select to start")
    locvart= st.checkbox("Check Local Variation of SDS and SD1")
    if locvart==1:
        contourf(lat, longt, riskct)





