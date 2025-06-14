
Streamlit version. 
Get the Multi-period response spectrum for a site for use with ASCE 7-22. Free to use. Data source is USGS (ASCE 7-22 Database) and OpenStreetMaps. 

Authors do not assume any responsibility or liability for its accuracy. Use of the output of this program does not imply approval by the governing building code bodies responsible for building code approval and interpretation for the building site described by latitude/longitude location.

Written by HXB

Accepts both late long pair or an address.

2/17/2024 Accepts an estimated shear wave velocity and computes the governing spectra based an upper bound, lower bound and estimated site class. Extensive revisions to code to write the governing spectra to file. 2/18/2024 Revised to compute sds and sd1 per ASCE 7-22 Section 21.4 where the shear wave velocity is estimated. 3/27/2024 Added option to lookup local variation of SDS and SD1 around site. 11/1/2024 Added default siteclass and interpolated spectra based on measured shear wave velocity.

2/15/2025 Enabled parameters in url - add to url as 
/?title=your title&address=your address&lat=xx.x&long=xx.x&riskcat=II&shearwavevelo=1200

2/16/2025 Better trapping of geocoding errors - will continue even if lat/long pair provided and geocoder is unavailable.

5/16/2025 A new section to automate FP calculation via ASCE 7-22 is now provided.

5/17/2025 Allow user to specify multiple z values with labels - error checking included.

5/18/2025 Cached URL calls, so the URL calls are not repeated when Fp calcs are run  also cached the normatin calls as well.

5/20/2025 Various aesthetic improvements (equations/code references) and error checking ( zmax <= H) etc.

5/23/2025 Converted to a multi- page app to separate Fp calculations from spectra calculations. URL parameters are stored in session variables for persistance over pages

5/24/2025 Further added code for persistance in user options on the Fp page, not perfect but close.

6/15/2025 Improved code for maps - switched to pydeck.  Now has labels for markers and tooltip popups.

Try out at: https://jmtwtc7pdpdfhpzgnwfdt6.streamlit.app/
