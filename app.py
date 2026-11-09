import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import pytz
import concurrent.futures
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Live Midcap NAV Tracker",
    layout="wide"
)

REFRESH_SECONDS = 60

st_autorefresh(interval=REFRESH_SECONDS * 1000, key="refresh")

# =========================
# FUND DATA
# =========================
#
# NOTE ON "nav": last known official per-unit NAV, used as the
# "Previous NAV" baseline. Portfolio statements only report holdings/
# weights, so these NAVs are carried over unchanged. Swap them in when
# you have the latest NAV.
#
# All holdings below: portfolio statements as on September 30, 2026
# (equity holdings only; "% to Net Assets"). Cash/TREPS/T-bills/
# receivables, REITs/InvITs, unlisted names, and 0.00% / "^" lines are
# excluded. Names whose NSE ticker could not be confidently resolved
# are listed in the comment above each fund and omitted.

funds = {

    # HSBC Midcap Fund - 30-Sep-2026. 0.00% lines omitted (Eternal, Biocon,
    # Schaeffler, Billionbrains, Abbott, Gabriel, NTPC Green).
    "HSBC Midcap Fund": {
        "nav": 520.67,
        "holdings": {
            "LENSKART.NS": 5.08, "MEESHO.NS": 5.04, "FEDERALBNK.NS": 3.90,
            "CPPLUS.NS": 3.64, "PIRAMALFIN.NS": 3.56, "NYKAA.NS": 3.38,
            "APARINDS.NS": 3.16, "GVT&D.NS": 3.09, "ATHERENERG.NS": 3.03,
            "DHOOTTRANS.NS": 2.91, "RADICO.NS": 2.89, "ZYDUSLIFE.NS": 2.82,
            "BHARATFORG.NS": 2.61, "AUBANK.NS": 2.34, "POWERINDIA.NS": 2.28,
            "COFORGE.NS": 2.28, "MANKIND.NS": 2.22, "M&MFIN.NS": 2.03,
            "NAM-INDIA.NS": 2.01, "NAVINFLUOR.NS": 2.01, "NETWEB.NS": 1.89,
            "THYROCARE.NS": 1.80, "SHADOWFAX.NS": 1.77, "IPCALAB.NS": 1.75,
            "DATAPATTNS.NS": 1.71, "THERMAX.NS": 1.67, "ABCAPITAL.NS": 1.66,
            "CUB.NS": 1.66, "INDUSINDBK.NS": 1.64, "MCX.NS": 1.62,
            "COCHINSHIP.NS": 1.60, "ASHOKLEY.NS": 1.48, "AVALON.NS": 1.48,
            "KFINTECH.NS": 1.48, "PAYTM.NS": 1.47, "POLICYBZR.NS": 1.45,
            "INDIANB.NS": 1.44, "ACMESOLAR.NS": 1.33, "TDPOWERSYS.NS": 1.26,
            "GODFRYPHLP.NS": 1.25, "POLYMED.NS": 1.23, "LUPIN.NS": 1.11,
            "PRESTIGE.NS": 1.09, "JSWENERGY.NS": 0.95, "CGPOWER.NS": 0.93,
            "ATLANTAELE.NS": 0.87, "TRITURBINE.NS": 0.70, "KIRLOSENG.NS": 0.15,
            "SAFARI.NS": 0.12, "SYNGENE.NS": 0.06, "CRISIL.NS": 0.04,
            "IDFCFIRSTB.NS": 0.03, "MFSL.NS": 0.03, "MUTHOOTFIN.NS": 0.03,
            "JKCEMENT.NS": 0.02, "DIXON.NS": 0.02, "MAZDOCK.NS": 0.02,
            "KEI.NS": 0.02, "SWIGGY.NS": 0.01, "PERSISTENT.NS": 0.01,
            "BHARTIHEXA.NS": 0.01, "ANTHEM.NS": 0.01, "KAYNES.NS": 0.01,
            "TVSMOTOR.NS": 0.01, "MAXHEALTH.NS": 0.01,
        }
    },

    # ICICI Prudential Mid Cap Fund - 30-Sep-2026. CRISIL and GSPL India
    # Transco are "^" (<0.01%) and omitted.
    "ICICI Midcap Fund": {
        "nav": 370.23,
        "holdings": {
            "APARINDS.NS": 5.98, "HINDPETRO.NS": 5.43, "MCX.NS": 5.43,
            "JINDALSTEL.NS": 3.97, "APLAPOLLO.NS": 3.95, "BSE.NS": 3.93,
            "JSL.NS": 2.92, "BHARATFORG.NS": 2.84, "MUTHOOTFIN.NS": 2.83,
            "POLICYBZR.NS": 2.68, "PRESTIGE.NS": 2.68, "KEI.NS": 2.45,
            "UPL.NS": 2.35, "NAM-INDIA.NS": 2.21, "KPRMILL.NS": 2.13,
            "NAVINFLUOR.NS": 1.98, "GVT&D.NS": 1.89, "SONACOMS.NS": 1.88,
            "POWERINDIA.NS": 1.78, "CUMMINSIND.NS": 1.78, "VAML.NS": 1.75,
            "UNOMINDA.NS": 1.71, "SRF.NS": 1.59, "GODREJPROP.NS": 1.51,
            "360ONE.NS": 1.47, "ESCORTS.NS": 1.45, "SCHAEFFLER.NS": 1.39,
            "MOTHERSON.NS": 1.32, "INDUSINDBK.NS": 1.30, "FLUOROCHEM.NS": 1.28,
            "SAIL.NS": 1.24, "DIXON.NS": 1.19, "LENSKART.NS": 1.17,
            "SUPREMEIND.NS": 1.11, "VEDL.NS": 1.10, "OBEROIRLTY.NS": 1.01,
            "POLYCAB.NS": 0.97, "NATIONALUM.NS": 0.96, "BHARTIHEXA.NS": 0.83,
            "VOLTAS.NS": 0.79, "GRINDWELL.NS": 0.75, "ASTRAL.NS": 0.73,
            "DRREDDY.NS": 0.70, "JYOTICNC.NS": 0.70, "BEML.NS": 0.69,
            "BLUESTARCO.NS": 0.68, "DEEPAKNTR.NS": 0.61, "COROMANDEL.NS": 0.61,
            "AMBUJACEM.NS": 0.57, "ENDURANCE.NS": 0.47, "PIIND.NS": 0.45,
            "AARTIIND.NS": 0.42, "IRCTC.NS": 0.39, "SBICARD.NS": 0.38,
            "IRB.NS": 0.31, "ATUL.NS": 0.31, "NYKAA.NS": 0.29,
            "PPLPHARMA.NS": 0.28, "NEOGEN.NS": 0.22, "RATNAMANI.NS": 0.21,
            "SYNGENE.NS": 0.19, "PREMIERENE.NS": 0.16, "MRF.NS": 0.16,
            "CARBORUNIV.NS": 0.14, "HONAUT.NS": 0.14, "VISL.NS": 0.14,
            "CPPLUS.NS": 0.14, "THERMAX.NS": 0.13, "INDIGO.NS": 0.13,
            "BALKRISIND.NS": 0.12, "CROMPTON.NS": 0.11, "JKCEMENT.NS": 0.09,
            "HINDZINC.NS": 0.09, "ASTRAZEN.NS": 0.05, "TIINDIA.NS": 0.05,
            "ACC.NS": 0.04, "KAJARIACER.NS": 0.02, "ASTEC.NS": 0.02,
            "CAMLINFINE.NS": 0.01, "GUJGASLTD.BO": 0.01,
        }
    },

    # Edelweiss Mid Cap Fund - 30-Sep-2026.
    # Omitted (ticker not confidently resolved): SS Retail Ltd (0.33%),
    # SPR Auto Technologies (0.25%). Deepak Nitrite is ~0.00%.
    # NEW tickers worth a quick check: WELCORP, NTPCGREEN, SCHNEIDER,
    # URBANCO, ABSLAMC.
    "Edelweiss Mid Cap Fund": {
        "nav": 124.96,
        "holdings": {
            "FEDERALBNK.NS": 3.06, "MCX.NS": 2.70, "SOLARINDS.NS": 2.09,
            "CUB.NS": 2.02, "PERSISTENT.NS": 1.99, "COFORGE.NS": 1.98,
            "BSE.NS": 1.92, "MARICO.NS": 1.92, "IPCALAB.NS": 1.84,
            "RADICO.NS": 1.72, "IDFCFIRSTB.NS": 1.68, "FORTIS.NS": 1.67,
            "BHARATFORG.NS": 1.63, "INDUSTOWER.NS": 1.56, "INDHOTEL.NS": 1.53,
            "AUBANK.NS": 1.52, "APLAPOLLO.NS": 1.51, "ASHOKLEY.NS": 1.48,
            "PHOENIXLTD.NS": 1.44, "INDIANB.NS": 1.40, "UNOMINDA.NS": 1.38,
            "TVSMOTOR.NS": 1.38, "DIXON.NS": 1.37, "CREDITACC.NS": 1.35,
            "KARURVYSYA.NS": 1.32, "LTF.NS": 1.32, "BHEL.NS": 1.31,
            "OBEROIRLTY.NS": 1.25, "JSL.NS": 1.18, "PRESTIGE.NS": 1.17,
            "MAXHEALTH.NS": 1.16, "GVT&D.NS": 1.12, "AJANTPHARM.NS": 1.10,
            "KEI.NS": 1.08, "ATHERENERG.NS": 1.06, "NAUKRI.NS": 1.03,
            "JKCEMENT.NS": 1.03, "HINDPETRO.NS": 1.02, "JSWENERGY.NS": 1.00,
            "SUNDARMFIN.NS": 1.00, "NYKAA.NS": 0.98, "LGEINDIA.NS": 0.93,
            "MRF.NS": 0.92, "PAGEIND.NS": 0.92, "MFSL.NS": 0.91,
            "MANKIND.NS": 0.90, "HDFCAMC.NS": 0.89, "BEL.NS": 0.87,
            "ENDURANCE.NS": 0.86, "SAIL.NS": 0.83, "CHOLAFIN.NS": 0.83,
            "TORNTPOWER.NS": 0.82, "POLYCAB.NS": 0.82, "LUPIN.NS": 0.80,
            "MEESHO.NS": 0.79, "CUMMINSIND.NS": 0.78, "NMDC.NS": 0.73,
            "JUBLFOOD.NS": 0.73, "TORNTPHARM.NS": 0.72, "EXIDEIND.NS": 0.69,
            "SUMICHEM.NS": 0.69, "GROWW.NS": 0.68, "LAURUSLABS.NS": 0.67,
            "360ONE.NS": 0.66, "ICICIAMC.NS": 0.66, "VMM.NS": 0.65,
            "POLICYBZR.NS": 0.62, "SCHAEFFLER.NS": 0.61, "CRAFTSMAN.NS": 0.59,
            "LENSKART.NS": 0.59, "SWIGGY.NS": 0.58, "COROMANDEL.NS": 0.56,
            "BLUESTARCO.NS": 0.55, "PINELABS.NS": 0.55, "TBOTEK.NS": 0.51,
            "BERGEPAINT.NS": 0.51, "BHARTIHEXA.NS": 0.50, "CEATLTD.NS": 0.50,
            "PNBHOUSING.NS": 0.49, "HEROMOTOCO.NS": 0.47, "BIKAJI.NS": 0.46,
            "NETWEB.NS": 0.46, "SRF.NS": 0.45, "THERMAX.NS": 0.41,
            "TRITURBINE.NS": 0.40, "OIL.NS": 0.39, "ITCHOTELS.NS": 0.38,
            "ELECON.NS": 0.36, "BDL.NS": 0.35, "FSL.NS": 0.35,
            "SHADOWFAX.NS": 0.35, "WELCORP.NS": 0.34, "SUPREMEIND.NS": 0.34,
            "NTPCGREEN.NS": 0.33, "APARINDS.NS": 0.32, "SCHNEIDER.NS": 0.31,
            "NAVINFLUOR.NS": 0.29, "ABSLAMC.NS": 0.29, "URBANCO.NS": 0.29,
            "ASTRAL.NS": 0.28, "SJS.NS": 0.27, "CGPOWER.NS": 0.25,
            "COCHINSHIP.NS": 0.17,
        }
    },

    # HDFC Mid Cap Fund - 30-Sep-2026 ("% to NAV"). The two SKF India lines
    # (0.64 Industrial + 0.35) are combined into SKFINDIA.NS (0.99).
    "HDFC Mid Cap Fund": {
        "nav": 226.04,
        "holdings": {
            "FEDERALBNK.NS": 3.98, "AUBANK.NS": 3.94, "MFSL.NS": 3.52,
            "IPCALAB.NS": 3.43, "GLENMARK.NS": 3.07, "BALKRISIND.NS": 2.98,
            "INDIANB.NS": 2.92, "COFORGE.NS": 2.68, "FORTIS.NS": 2.40,
            "MARICO.NS": 2.37, "VMM.NS": 2.24, "AUROPHARMA.NS": 2.19,
            "M&MFIN.NS": 2.11, "HINDPETRO.NS": 2.09, "UNITDSPR.NS": 1.90,
            "CUMMINSIND.NS": 1.82, "TATACOMM.NS": 1.81, "PERSISTENT.NS": 1.78,
            "GLAND.NS": 1.73, "ALKEM.NS": 1.72, "APOLLOTYRE.NS": 1.66,
            "DABUR.NS": 1.66, "JINDALSTEL.NS": 1.64, "MPHASIS.NS": 1.55,
            "UNIONBANK.NS": 1.51, "BOSCHLTD.NS": 1.44, "ETERNAL.NS": 1.35,
            "AIAENG.NS": 1.29, "DELHIVERY.NS": 1.27, "KARURVYSYA.NS": 1.25,
            "BHARATFORG.NS": 1.22, "COROMANDEL.NS": 1.19, "REDINGTON.NS": 1.10,
            "STARHEALTH.NS": 1.08, "POLICYBZR.NS": 1.07, "INDUSINDBK.NS": 1.04,
            "NAM-INDIA.NS": 1.04, "INDHOTEL.NS": 1.01, "GODREJCP.NS": 0.98,
            "ICICIGI.NS": 0.95, "ASTERDM.NS": 0.90, "HAVELLS.NS": 0.84,
            "SONACOMS.NS": 0.82, "SUNDRMFAST.NS": 0.81, "ESCORTS.NS": 0.79,
            "HEXT.NS": 0.78, "CUB.NS": 0.74, "IGL.NS": 0.73,
            "DIXON.NS": 0.66, "SKFINDIA.NS": 0.99, "FLUOROCHEM.NS": 0.60,
            "TIMKEN.NS": 0.60, "CROMPTON.NS": 0.59, "ACC.NS": 0.56,
            "SUPREMEIND.NS": 0.56, "ARVIND.NS": 0.43, "AARTIIND.NS": 0.36,
            "OFSS.NS": 0.36, "PETRONET.NS": 0.36, "CHOLAHLDNG.NS": 0.31,
            "KEC.NS": 0.30, "VTL.NS": 0.30, "VESUVIUS.NS": 0.30,
            "CIEINDIA.NS": 0.27, "SYMPHONY.NS": 0.21, "FIVESTAR.NS": 0.20,
            "BHARTIHEXA.NS": 0.19, "GROWW.NS": 0.18, "COLPAL.NS": 0.18,
            "LGEINDIA.NS": 0.17, "GREENPLY.NS": 0.16, "NAVNETEDUL.NS": 0.16,
            "GREENLAM.NS": 0.13, "DHANUKA.NS": 0.10, "EMAMILTD.NS": 0.03,
            "JAGRAN.NS": 0.03, "GREENPANEL.NS": 0.02, "KNRCON.NS": 0.01,
        }
    },

    # Invesco India Midcap Fund - 30-Sep-2026. Omitted (unlisted):
    # Manipal Health Enterprises (4.44%), National Stock Exchange of India (0.12%).
    "Invesco India Midcap Fund": {
        "nav": 239.75,
        "holdings": {
            "PRESTIGE.NS": 7.33, "MAXHEALTH.NS": 7.21, "MEESHO.NS": 5.42,
            "FEDERALBNK.NS": 5.37, "ETERNAL.NS": 4.14, "MEDANTA.NS": 3.97,
            "LTF.NS": 3.91, "AUBANK.NS": 3.81, "INDUSINDBK.NS": 3.51,
            "SAILIFE.NS": 3.31, "MFSL.NS": 3.15, "BSE.NS": 3.06,
            "INDIGO.NS": 2.92, "JKCEMENT.NS": 2.90, "BHARATFORG.NS": 2.81,
            "GLENMARK.NS": 2.76, "ABB.NS": 2.56, "CPPLUS.NS": 2.47,
            "SRF.NS": 2.21, "NYKAA.NS": 2.04, "TORNTPOWER.NS": 1.83,
            "AMBER.NS": 1.73, "TRENT.NS": 1.63, "ICICIGI.NS": 1.52,
            "SWIGGY.NS": 1.32, "DIXON.NS": 1.29, "TIINDIA.NS": 1.23,
            "PHOENIXLTD.NS": 1.19, "GROWW.NS": 1.02, "CRAFTSMAN.NS": 0.96,
            "CORONA.NS": 0.93, "KIMS.NS": 0.92, "ETHOSLTD.NS": 0.84,
            "DRAGARWQ.NS": 0.68, "TIMKEN.NS": 0.54, "MAXESTATES.NS": 0.50,
            "BANSALWIRE.NS": 0.48, "WEWORK.NS": 0.37, "VMM.NS": 0.17,
            "CARBORUNIV.NS": 0.11, "SONATSOFTW.NS": 0.06,
        }
    },

    # Motilal Oswal Midcap Fund - ALREADY UPDATED (left unchanged).
    "Motilal Oswal Midcap Fund": {
        "nav": 119.01,
        "holdings": {
            "PAYTM.NS": 8.64,        # One 97 Communications Limited
            "KALYANKJIL.NS": 7.98,   # Kalyan Jewellers India Limited
            "ETERNAL.NS": 6.72,      # Eternal Limited
            "COFORGE.NS": 5.43,      # Coforge Limited
            "KEI.NS": 4.27,          # KEI Industries Limited
            "ABCAPITAL.NS": 4.64,    # Aditya Birla Capital Limited
            "PERSISTENT.NS": 4.43,   # Persistent Systems Ltd
            "SHRIRAMFIN.NS": 3.40,   # Shriram Finance Limited
            "DIXON.NS": 3.43,        # Dixon Technologies (India) Limited
            "GROWW.NS": 3.50,        # Billionbrains Garage Ventures Ltd (Groww)
            "MCX.NS": 3.74,          # Multi Commodity Exchange of India Limited
            "STLTECH.NS": 4.40,      # Sterlite Technologies Limited
            "POLICYBZR.NS": 1.72,    # PB Fintech Limited
            "TIINDIA.NS": 2.43,      # Tube Investments Of India Limited
            "LTF.NS": 2.11,          # L&T Finance Limited
            "ICICIAMC.NS": 2.60,     # ICICI Prudential Asset Management Company Limited
            "PRESTIGE.NS": 2.20,     # Prestige Estates Projects Limited
            "BHARTIHEXA.NS": 2.23,   # Bharti Hexacom Limited
            "LENSKART.NS": 2.94,     # Lenskart Solutions Limited
            "MOTHERSON.NS": 2.26,    # Samvardhana Motherson International Limited
            "SUZLON.NS": 1.91,       # Suzlon Energy Limited
            "IDFCFIRSTB.NS": 2.40,   # IDFC First Bank Limited
            "PREMIERENE.NS": 1.82,   # Premier Energies Limited
            "BEL.NS": 1.89,          # Bharat Electronics Limited
            "BSE.NS": 1.75,          # BSE Limited
            "INDIGO.NS": 1.75,       # InterGlobe Aviation Limited
            "WAAREEENER.NS": 1.43,   # Waaree Energies Limited
            "MAXHEALTH.NS": 1.33,    # Max Healthcare Institute Limited
            "ADANIENT.NS": 0.87,     # Adani Enterprises Limited
            "PWL.NS": 0.59,          # PhysicsWallah Limited
        }
    },

    # WhiteOak Capital Mid Cap Fund - 30-Sep-2026 (cash-equity "% to Net
    # Assets"; this month's statement shows no futures overlay column).
    # REITs/InvITs excluded. Omitted (ticker not confidently resolved):
    # Indo-MIM (0.65), Juniper Green Energy (0.61), Tenneco Clean Air (0.40),
    # Clean Max Enviro Energy (0.29), Omnitech Engineering (0.24), Yash
    # Highvoltage (0.23), Aye Finance (0.22), Horizon Industrial Parks (0.20),
    # Travel Food Services (0.17), Epack Prefab (0.13), Onemi Technology
    # (0.11), Indiqube Spaces (0.10), Orkla India (0.08), EMA Partners (0.04).
    # Blue Star is 0.00% and omitted.
    "WhiteOak Capital Midcap Fund": {
        "nav": 22.88,
        "holdings": {
            "BHARTIHEXA.NS": 2.78, "COFORGE.NS": 2.73, "FEDERALBNK.NS": 2.50,
            "MFSL.NS": 2.48, "LAURUSLABS.NS": 2.20, "MOTILALOFS.NS": 2.05,
            "VMM.NS": 1.96, "PHOENIXLTD.NS": 1.95, "NAUKRI.NS": 1.87,
            "BHEL.NS": 1.86, "LENSKART.NS": 1.66, "FORTIS.NS": 1.58,
            "360ONE.NS": 1.53, "MARICO.NS": 1.45, "BERGEPAINT.NS": 1.39,
            "IPCALAB.NS": 1.33, "AJANTPHARM.NS": 1.32, "SONACOMS.NS": 1.30,
            "BANDHANBNK.NS": 1.25, "KEI.NS": 1.22, "INDUSINDBK.NS": 1.20,
            "POLICYBZR.NS": 1.18, "NATIONALUM.NS": 1.12, "AIAENG.NS": 1.12,
            "MCX.NS": 1.07, "MUTHOOTFIN.NS": 1.05, "M&MFIN.NS": 1.03,
            "PERSISTENT.NS": 1.01, "JSL.NS": 0.95, "JSWINFRA.NS": 0.94,
            "GLAND.NS": 0.89, "TIINDIA.NS": 0.89, "NYKAA.NS": 0.87,
            "ALKEM.NS": 0.84, "MAXHEALTH.NS": 0.83, "AADHARHFC.NS": 0.83,
            "PAGEIND.NS": 0.80, "NAVINFLUOR.NS": 0.76, "ABBOTINDIA.NS": 0.75,
            "MEESHO.NS": 0.74, "GVT&D.NS": 0.73, "RECLTD.NS": 0.72,
            "POWERINDIA.NS": 0.72, "AZAD.NS": 0.67, "BANKINDIA.NS": 0.63,
            "OIL.NS": 0.62, "COROMANDEL.NS": 0.62, "PAYTM.NS": 0.60,
            "KRN.NS": 0.60, "MANKIND.NS": 0.58, "GODREJPROP.NS": 0.55,
            "CUMMINSIND.NS": 0.54, "THELEELA.NS": 0.54, "HINDPETRO.NS": 0.53,
            "NH.NS": 0.52, "FIVESTAR.NS": 0.50, "INDIASHLTR.NS": 0.50,
            "SAILIFE.NS": 0.50, "GROWW.NS": 0.49, "TDPOWERSYS.NS": 0.48,
            "PNBHOUSING.NS": 0.48, "COLPAL.NS": 0.47, "CARERATING.NS": 0.47,
            "GODREJIND.NS": 0.47, "DYNAMATECH.NS": 0.46, "ACUTAAS.NS": 0.42,
            "ABCAPITAL.NS": 0.42, "HEROMOTOCO.NS": 0.41, "NEULANDLAB.NS": 0.41,
            "SHILPAMED.NS": 0.41, "SUPREMEIND.NS": 0.39, "IIFL.NS": 0.38,
            "AJAXENGG.NS": 0.38, "CPPLUS.NS": 0.38, "SOUTHBANK.NS": 0.37,
            "NMDC.NS": 0.37, "MANORAMA.NS": 0.35, "UTIAMC.NS": 0.35,
            "POLYMED.NS": 0.35, "OFSS.NS": 0.34, "ENDURANCE.NS": 0.32,
            "CARTRADE.NS": 0.31, "ABREL.NS": 0.30, "ANTHEM.NS": 0.30,
            "KIRLOSENG.NS": 0.30, "AVALON.NS": 0.29, "JSWCEMENT.NS": 0.28,
            "NEOGEN.NS": 0.27, "TBOTEK.NS": 0.27, "GILLETTE.NS": 0.27,
            "REDINGTON.NS": 0.27, "ELGIEQUIP.NS": 0.24, "EUREKAFORB.NS": 0.22,
            "IGIL.NS": 0.21, "REPCOHOME.NS": 0.20, "SOBHA.NS": 0.19,
            "DOMS.NS": 0.19, "METROBRAND.NS": 0.17, "AUBANK.NS": 0.15,
            "LEMONTREE.NS": 0.15, "SAFARI.NS": 0.14, "CHOLAHLDNG.NS": 0.13,
            "ICICIGI.NS": 0.13, "INTELLECT.NS": 0.13, "UJJIVANSFB.NS": 0.13,
            "3MINDIA.NS": 0.12, "KIMS.NS": 0.11, "SAGILITY.NS": 0.11,
            "AETHER.NS": 0.11, "FINEORG.NS": 0.08, "BRIGADE.NS": 0.06,
            "NEWGEN.NS": 0.06, "XPROINDIA.NS": 0.06, "NSDL.BO": 0.05,
            "ICICIPRULI.NS": 0.05, "KARURVYSYA.NS": 0.05, "AWFIS.NS": 0.04,
            "PETRONET.NS": 0.04, "NAM-INDIA.NS": 0.02, "ATHERENERG.NS": 0.01,
        }
    }
}

# =========================
# FETCH LIVE DATA
# =========================
#
# 3-tier design (all tiers fetched concurrently, quote lookup does no I/O):
#   Tier 1 (.NS only):    NSE's own quote API (previousClose / lastPrice).
#   Tier 2 (.NS + .BO):   Yahoo chart API meta block (chartPreviousClose /
#                         regularMarketPrice). Deliberately NOT yfinance
#                         fast_info (client-side-derived previousClose).
#   Tier 3 (last resort): batched daily + intraday candle history, with the
#                         "is last daily bar today's session" test done by
#                         comparing yfinance's own daily vs intraday bar dates.
# A ticker with no fresh data falls back to its last known good quote in
# st.session_state.

NSE_REQUEST_TIMEOUT = 5
NSE_BATCH_TIMEOUT = 35
YF_BATCH_TIMEOUT = 30
STALE_DATA_MAX_DAYS = 4

if "last_good_quotes" not in st.session_state:
    # {ticker: (previous_close, latest_close, as_of_date, source)}
    st.session_state["last_good_quotes"] = {}

if "nse_session" not in st.session_state:
    st.session_state["nse_session"] = None

all_tickers = []
for fund in funds.values():
    all_tickers.extend(list(fund["holdings"].keys()))
all_tickers = sorted(set(all_tickers))

# NSE's quote API only serves .NS listings; .BO tickers go to Tier 2.
nse_eligible_symbols = [t[:-3] for t in all_tickers if t.endswith(".NS")]

NSE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/get-quotes/equity",
}

YF_CHART_URL = "https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"

YF_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json,text/plain,*/*",
}


def get_nse_session():
    """Reuse one requests.Session across reruns so we don't re-negotiate
    NSE's anti-bot cookies on every refresh."""
    session = st.session_state.get("nse_session")
    if session is None:
        session = requests.Session()
        session.headers.update(NSE_HEADERS)
        try:
            session.get("https://www.nseindia.com", timeout=NSE_REQUEST_TIMEOUT)
        except Exception:
            pass
        st.session_state["nse_session"] = session
    return session


def _fetch_one_nse(symbol, session):
    """Single-symbol NSE fetch (thread pool). `symbol` has no .NS suffix."""
    url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
    try:
        resp = session.get(url, timeout=NSE_REQUEST_TIMEOUT)
        if resp.status_code != 200:
            resp = session.get(url, timeout=NSE_REQUEST_TIMEOUT)
        if resp.status_code != 200:
            return symbol, None, None, f"HTTP {resp.status_code}"
        data = resp.json()
        price_info = data.get("priceInfo", {})
        live_price = price_info.get("lastPrice")
        prev_close = price_info.get("previousClose")
        if live_price and prev_close:
            return symbol, float(prev_close), float(live_price), None
        return symbol, None, None, "missing priceInfo fields (likely bot-blocked page)"
    except ValueError:
        return symbol, None, None, "non-JSON response (likely bot-block HTML page)"
    except requests.exceptions.Timeout:
        return symbol, None, None, "timeout"
    except Exception as e:
        return symbol, None, None, f"{type(e).__name__}"


@st.cache_data(ttl=REFRESH_SECONDS, show_spinner=False)
def fetch_nse_batch(symbols):
    """PRIMARY source (.NS only), concurrent, one overall timeout."""
    session = get_nse_session()
    results = {}
    errors = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        futures = {ex.submit(_fetch_one_nse, s, session): s for s in symbols}
        try:
            for fut in concurrent.futures.as_completed(futures, timeout=NSE_BATCH_TIMEOUT):
                s = futures[fut]
                try:
                    _, prev_close, live_price, err = fut.result()
                except Exception as e:
                    prev_close, live_price, err = None, None, str(e)
                results[s] = (prev_close, live_price)
                if err:
                    errors[s] = err
        except concurrent.futures.TimeoutError:
            for fut, s in futures.items():
                if s not in results:
                    results[s] = (None, None)
                    errors[s] = "timeout (overall NSE batch)"

    return results, errors


def _fetch_one_yf_chart(ticker):
    """TIER 2 -- Yahoo chart-API meta block. `ticker` includes .NS/.BO."""
    try:
        resp = requests.get(
            YF_CHART_URL.format(ticker=ticker),
            params={"range": "1d", "interval": "1m"},
            headers=YF_HEADERS,
            timeout=NSE_REQUEST_TIMEOUT,
        )
        if resp.status_code != 200:
            return ticker, None, None, f"HTTP {resp.status_code}"

        payload = resp.json()
        result = (payload.get("chart", {}).get("result") or [None])[0]
        if not result:
            err = payload.get("chart", {}).get("error")
            return ticker, None, None, f"no result ({err})"

        meta = result.get("meta", {})
        prev_close = meta.get("chartPreviousClose") or meta.get("previousClose")
        live_price = meta.get("regularMarketPrice")

        if live_price is None:
            try:
                closes = result["indicators"]["quote"][0]["close"]
                for c in reversed(closes):
                    if c is not None:
                        live_price = c
                        break
            except Exception:
                pass

        if prev_close and live_price:
            return ticker, float(prev_close), float(live_price), None
        return ticker, None, None, "missing chart meta fields"

    except ValueError:
        return ticker, None, None, "non-JSON response"
    except requests.exceptions.Timeout:
        return ticker, None, None, "timeout"
    except Exception as e:
        return ticker, None, None, f"{type(e).__name__}"


@st.cache_data(ttl=REFRESH_SECONDS, show_spinner=False)
def fetch_yf_chart_batch(tickers):
    """TIER 2 (secondary) source, concurrent, one overall timeout."""
    results = {}
    errors = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        futures = {ex.submit(_fetch_one_yf_chart, t): t for t in tickers}
        try:
            for fut in concurrent.futures.as_completed(futures, timeout=YF_BATCH_TIMEOUT):
                t = futures[fut]
                try:
                    _, prev_close, live_price, err = fut.result()
                except Exception as e:
                    prev_close, live_price, err = None, None, str(e)
                results[t] = (prev_close, live_price)
                if err:
                    errors[t] = err
        except concurrent.futures.TimeoutError:
            for fut, t in futures.items():
                if t not in results:
                    results[t] = (None, None)
                    errors[t] = "timeout (overall Yahoo chart batch)"

    return results, errors


def _download_with_timeout(kwargs, timeout_seconds):
    """Runs yf.download() in a worker thread with a hard timeout."""
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            future = ex.submit(lambda: yf.download(**kwargs))
            return future.result(timeout=timeout_seconds)
    except concurrent.futures.TimeoutError:
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=REFRESH_SECONDS, show_spinner=False)
def fetch_daily_batch(tickers):
    """TIER 3 previous-close source: batched recent daily bars."""
    return _download_with_timeout(
        dict(
            tickers=tickers,
            period="10d",
            interval="1d",
            group_by="ticker",
            threads=True,
            progress=False,
            auto_adjust=False,
        ),
        YF_BATCH_TIMEOUT,
    )


@st.cache_data(ttl=REFRESH_SECONDS, show_spinner=False)
def fetch_intraday_batch(tickers):
    """TIER 3 live-price source: batched 1-minute intraday bars."""
    return _download_with_timeout(
        dict(
            tickers=tickers,
            period="1d",
            interval="1m",
            group_by="ticker",
            threads=True,
            progress=False,
            auto_adjust=False,
        ),
        YF_BATCH_TIMEOUT,
    )


def _extract_close_series(ticker, batch_data, n_tickers):
    if batch_data is None or batch_data.empty:
        return None
    try:
        if n_tickers == 1:
            if "Close" not in batch_data.columns:
                return None
            return batch_data["Close"].dropna()
        if ticker not in batch_data.columns.get_level_values(0):
            return None
        return batch_data[ticker]["Close"].dropna()
    except Exception:
        return None


def get_prev_close_from_daily(ticker, daily_batch, intraday_batch, n_tickers, today_date):
    """Tier-3 previous close: compare the daily batch's own last bar date
    with the intraday batch's own last bar date (same source)."""
    daily_hist = _extract_close_series(ticker, daily_batch, n_tickers)
    if daily_hist is None or daily_hist.empty:
        return None

    last_daily_date = pd.Timestamp(daily_hist.index[-1]).date()

    if (today_date - last_daily_date).days > STALE_DATA_MAX_DAYS:
        return None

    intraday_hist = _extract_close_series(ticker, intraday_batch, n_tickers)
    intraday_last_date = None
    if intraday_hist is not None and len(intraday_hist) >= 1:
        intraday_last_date = pd.Timestamp(intraday_hist.index[-1]).date()

    if intraday_last_date is not None and last_daily_date == intraday_last_date:
        if len(daily_hist) >= 2:
            return float(daily_hist.iloc[-2])
        return None

    return float(daily_hist.iloc[-1])


def get_live_price_from_intraday(ticker, intraday_batch, daily_batch, n_tickers):
    """Tier-3 live price = latest 1-minute close, else last daily close."""
    hist = _extract_close_series(ticker, intraday_batch, n_tickers)
    if hist is not None and len(hist) >= 1:
        return float(hist.iloc[-1])
    hist = _extract_close_series(ticker, daily_batch, n_tickers)
    if hist is not None and len(hist) >= 1:
        return float(hist.iloc[-1])
    return None


india = pytz.timezone("Asia/Kolkata")
now_india = datetime.now(india)
today_india_date = now_india.date()

# --- Fetch all tiers ONCE, up front. Building quote_map does NO network I/O.

nse_results, nse_errors = fetch_nse_batch(tuple(nse_eligible_symbols))

need_tier2 = any(
    t.endswith(".NS")
    and (
        nse_results.get(t[:-3], (None, None))[0] is None
        or nse_results.get(t[:-3], (None, None))[1] is None
    )
    or not t.endswith(".NS")
    for t in all_tickers
)

yf_chart_results, yf_chart_errors = (
    fetch_yf_chart_batch(tuple(all_tickers)) if need_tier2 else ({}, {})
)


def _tier2_ok(t):
    p, l = yf_chart_results.get(t, (None, None))
    return p is not None and l is not None


need_tier3 = any(
    not (t.endswith(".NS") and nse_results.get(t[:-3], (None, None))[0] is not None
         and nse_results.get(t[:-3], (None, None))[1] is not None)
    and not _tier2_ok(t)
    for t in all_tickers
)

daily_batch = fetch_daily_batch(tuple(all_tickers)) if need_tier3 else None
intraday_batch = fetch_intraday_batch(tuple(all_tickers)) if need_tier3 else None
n_tickers = len(all_tickers)

quote_map = {}

# Fetch the cache dict HERE (not at the top of the script). A slow fetch
# can be interrupted by the 60s autorefresh rerun, and Streamlit may have
# reset session_state by the time this point is reached.
good_quotes = st.session_state.setdefault("last_good_quotes", {})

for ticker in all_tickers:

    prev_close, live_price, source = None, None, None

    if ticker.endswith(".NS"):
        prev_close, live_price = nse_results.get(ticker[:-3], (None, None))
        if prev_close is not None and live_price is not None:
            source = "NSE"

    if prev_close is None or live_price is None:
        q_prev, q_live = yf_chart_results.get(ticker, (None, None))
        if q_prev is not None and q_live is not None:
            prev_close, live_price = q_prev, q_live
            source = "yahoo-chart"

    if prev_close is None or live_price is None:
        fb_prev = get_prev_close_from_daily(
            ticker, daily_batch, intraday_batch, n_tickers, today_india_date
        )
        fb_live = get_live_price_from_intraday(
            ticker, intraday_batch, daily_batch, n_tickers
        )
        if fb_prev is not None and fb_live is not None:
            prev_close, live_price = fb_prev, fb_live
            source = "yfinance-daily-derived"

    if prev_close is not None and live_price is not None and prev_close != 0:
        quote_map[ticker] = (prev_close, live_price, today_india_date, source)
        good_quotes[ticker] = (
            prev_close, live_price, today_india_date, source
        )
    else:
        cached = good_quotes.get(ticker)
        if cached is not None:
            if len(cached) == 3:
                cached = (cached[0], cached[1], cached[2], "cached")
            quote_map[ticker] = cached

fetch_failed = len(quote_map) == 0

if fetch_failed:
    st.warning(
        "⚠️ Couldn't reach any price source this refresh "
        "(NSE, Yahoo chart API, and Yahoo daily bars all failed). "
        "Showing last known values where available.",
        icon="⚠️",
    )

# =========================
# TITLE
# =========================

st.title("📈 Live Midcap Fund NAV Tracker")

current_time = now_india.strftime("%d-%m-%Y %I:%M:%S %p")

st.write(f"Last Updated: {current_time}")

# =========================
# NAV CALCULATION
# =========================

fund_performance = []
stale_this_cycle = set()
source_counts = {}

for fund_name, fund_data in funds.items():

    previous_nav = fund_data["nav"]
    holdings = fund_data["holdings"]

    weighted_return = 0.0
    stock_rows = []
    skipped = []

    for ticker, weight in holdings.items():

        quote = quote_map.get(ticker)

        if quote is None:
            skipped.append((ticker, weight, "No fresh or cached price available yet"))
            continue

        previous_close, latest_close, as_of_date, source = quote

        if source not in ("NSE", "yahoo-chart"):
            stale_this_cycle.add(ticker)

        source_counts[source] = source_counts.get(source, 0) + 1

        change_percent = (
            (latest_close - previous_close) / previous_close
        ) * 100

        contribution = (weight / 100) * change_percent
        weighted_return += contribution

        stock_rows.append({
            "Stock": ticker,
            "Weight %": round(weight, 2),
            "Price Change %": round(change_percent, 2),
            "Contribution": round(contribution, 3),
            "Source": source,
        })

    expected_nav = previous_nav * (
        1 + weighted_return / 100
    )

    nav_change = (
        (expected_nav - previous_nav)
        / previous_nav
    ) * 100

    fund_performance.append({
        "Fund": fund_name,
        "Return": nav_change
    })

    st.markdown("---")

    st.subheader(fund_name)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Previous NAV",
        f"₹{previous_nav:.2f}"
    )

    col2.metric(
        "Expected NAV",
        f"₹{expected_nav:.2f}",
        f"{nav_change:.2f}%"
    )

    col3.metric(
        "Portfolio Move",
        f"{weighted_return:.2f}%"
    )

    total_weight = sum(h["Weight %"] for h in stock_rows)
    st.caption(
        f"{len(stock_rows)}/{len(holdings)} holdings priced "
        f"(covers {total_weight:.2f}% of {sum(holdings.values()):.2f}% total weight)"
    )

    df = pd.DataFrame(stock_rows)

    if not df.empty:

        df = df.sort_values(
            by="Weight %",
            ascending=False
        )

        st.dataframe(
            df,
            width="stretch",
            height=400
        )

    if skipped:
        with st.expander(f"⚠️ {len(skipped)} holding(s) skipped in {fund_name}"):
            skipped_df = pd.DataFrame(
                skipped, columns=["Stock", "Weight %", "Reason"]
            ).sort_values(by="Weight %", ascending=False)
            st.dataframe(
                skipped_df,
                width="stretch"
            )

# =====================================================
# DATA FRESHNESS / SOURCE NOTICE
# =====================================================

st.markdown("---")

with st.expander("🛠️ Debug: price source breakdown", expanded=False):
    if source_counts:
        st.dataframe(
            pd.DataFrame(
                [{"Source": s, "Tickers": c} for s, c in source_counts.items()]
            ).sort_values(by="Tickers", ascending=False),
            width="stretch"
        )
        st.caption(
            "'NSE' and 'yahoo-chart' are authoritative, exchange/vendor-"
            "stated quotes. 'yfinance-daily-derived' means both of those "
            "failed for that ticker and it fell back to candle-derived "
            "data -- the least reliable tier, worth checking individually "
            "if a ticker still looks off. 'cached' means no source "
            "responded this cycle and last-known-good was reused."
        )
    if nse_errors:
        n_fail = len(nse_errors)
        n_total = len(nse_eligible_symbols)
        st.caption(
            f"NSE failed for {n_fail}/{n_total} symbols this cycle "
            "(common on Streamlit Community Cloud, which NSE tends to "
            "bot-block -- the app then runs on the Yahoo chart tier)."
        )

if stale_this_cycle:
    sample = ", ".join(sorted(stale_this_cycle)[:8])
    more = f" +{len(stale_this_cycle) - 8} more" if len(stale_this_cycle) > 8 else ""
    st.info(
        f"ℹ️ {len(stale_this_cycle)} ticker(s) are on the last-resort "
        f"candle-derived tier or a cached value this refresh: {sample}{more}"
    )

# =====================================================
# BEST & WORST FUND
# =====================================================

st.markdown("---")

if len(fund_performance) > 0:

    performance_df = pd.DataFrame(fund_performance)

    best_fund = performance_df.loc[
        performance_df["Return"].idxmax()
    ]

    worst_fund = performance_df.loc[
        performance_df["Return"].idxmin()
    ]

    st.subheader("🏆 Fund Performance Today")

    c1, c2 = st.columns(2)

    c1.metric(
        "Best Fund of the Day",
        best_fund["Fund"],
        f"{best_fund['Return']:.2f}%"
    )

    c2.metric(
        "Worst Fund of the Day",
        worst_fund["Fund"],
        f"{worst_fund['Return']:.2f}%"
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Live NAV estimation based on weighted portfolio stock movement."
)
