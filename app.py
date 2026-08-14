import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Live Midcap NAV Tracker",
    layout="wide"
)

st_autorefresh(interval=60000, key="refresh")

# =========================
# FUND DATA
# =========================

funds = {

    # Updated to HSBC Mutual Fund's Portfolio Statement
    # as on July 31, 2026 (equity holdings only; weights are "% to Net Assets").
    # Excludes Treps and Net Current Assets (cash-equivalent lines, not equities).
    # Entries listed at 0.00% in the statement are omitted (no impact on NAV calc).
    "HSBC Midcap Fund": {
        "nav": 540.16,
        "holdings": {
        "FEDERALBNK.NS": 4.91,   # The Federal Bank Limited
        "LENSKART.NS": 4.13,     # Lenskart Solutions Limited
        "NYKAA.NS": 4.04,        # FSN E-Commerce Ventures Limited
        "PIRAMALFIN.NS": 3.66,   # Piramal Finance Ltd
        "POLICYBZR.NS": 3.64,    # PB Fintech Limited
        "GVT&D.NS": 3.43,        # GE Vernova T&D India Limited
        "MEESHO.NS": 3.34,       # Meesho Limited
        "BHARATFORG.NS": 3.22,   # Bharat Forge Limited
        "CPPLUS.NS": 2.92,       # Aditya Infotech Limited
        "M&MFIN.NS": 2.88,       # Mahindra & Mahindra Financial Serv Ltd.
        "APARINDS.NS": 2.51,     # APAR INDUSTRIES LTD
        "JSWENERGY.NS": 2.51,    # JSW Energy Limited
        "RADICO.NS": 2.48,       # Radico Khaitan Limited
        "MANKIND.NS": 2.37,      # Mankind Pharma Limited
        "NAM-INDIA.NS": 2.36,    # Nippon Life India Asset Management Ltd
        "POWERINDIA.NS": 2.30,   # Hitachi Energy India Limited
        "THERMAX.NS": 2.29,      # Thermax Limited
        "NETWEB.NS": 2.03,       # Netweb Technologies India Limited
        "ATHERENERG.NS": 2.02,   # Ather Energy Limited
        "ABCAPITAL.NS": 1.90,    # Aditya Birla Capital Limited
        "AUBANK.NS": 1.89,       # AU Small Finance Bank Limited
        "PRESTIGE.NS": 1.89,     # Prestige Estates Projects Limited
        "COCHINSHIP.NS": 1.87,   # Cochin Shipyard Limited
        "DATAPATTNS.NS": 1.84,   # Data Patterns (India) Limited
        "IPCALAB.NS": 1.71,      # IPCA Laboratories Limited
        "CUB.NS": 1.63,          # City Union Bank Limited
        "THYROCARE.NS": 1.63,    # Thyrocare Technologies Limited
        "INDIANB.NS": 1.62,      # Indian Bank
        "GODFRYPHLP.NS": 1.52,   # Godfrey Phillips India Limited
        "ICICIAMC.NS": 1.48,     # ICICI Prudential AMC Ltd
        "LUPIN.NS": 1.42,        # Lupin Limited
        "INDUSINDBK.NS": 1.41,   # IndusInd Bank Limited
        "COFORGE.NS": 1.26,      # Coforge Limited
        "ASHOKLEY.NS": 1.24,     # Ashok Leyland Limited
        "SYNGENE.NS": 1.20,      # Syngene International Limited
        "ZYDUSLIFE.NS": 1.18,    # Zydus Lifesciences Limited
        "TDPOWERSYS.NS": 1.16,   # TD Power Systems Limited
        "POLYCAB.NS": 1.10,      # Polycab India Limited
        "NAVINFLUOR.NS": 1.09,   # Navin Fluorine International Limited
        "KEI.NS": 1.08,          # KEI Industries Limited
        "CGPOWER.NS": 1.02,      # CG Power And Industrial Solutions Ltd
        "MCX.NS": 0.96,          # Multi Commodity Exchange of India Ltd.
        "POLYMED.NS": 0.96,      # Poly Medicure Ltd
        "GROWW.NS": 0.90,        # Billionbrains Garage Ventures Ltd.
        "ATLANTAELE.NS": 0.89,   # Atlanta Electricals Limited
        "AVALON.NS": 0.89,       # AVALON TECHNOLOGIES LIMITED
        "TRITURBINE.NS": 0.72,   # TRIVENI TURBINE LTD.
        "KFINTECH.NS": 0.69,     # KFin Technologies Limited
        "KIRLOSENG.NS": 0.60,    # Kirloskar Oil Engines Ltd
        "TVSMOTOR.NS": 0.58,     # TVS Motor Company Limited
        "CREDITACC.NS": 0.39,    # Creditaccess Grameen Limited
        "BSE.NS": 0.32,          # BSE Ltd
        "JSWSTEEL.NS": 0.28,     # JSW Steel Limited
        "SAFARI.NS": 0.14,       # SAFARI INDUSTRIES (INDIA) LIMITED
        "HINDALCO.NS": 0.09,     # Hindalco Industries Limited
        "CRISIL.NS": 0.05,       # CRISIL Limited
        "IDFCFIRSTB.NS": 0.04,   # IDFC First Bank Limited
        "MUTHOOTFIN.NS": 0.03,   # Muthoot Finance Limited
        "MFSL.NS": 0.03,         # Max Financial Services Limited
        "MAZDOCK.NS": 0.03,      # Mazagon Dock Shipbuilders Limited
        "JKCEMENT.NS": 0.02,     # JK Cement Limited
        "DIXON.NS": 0.02,        # Dixon Technologies (India) Limited
        "SWIGGY.NS": 0.02,       # SWIGGY LIMITED
        "PERSISTENT.NS": 0.02,   # PERSISTENT SYSTEMS LTD
        "BHARTIHEXA.NS": 0.01,   # Bharti Hexacom Limited
        "KAYNES.NS": 0.01,       # Kaynes Technology India Ltd.
        "ACMESOLAR.NS": 0.01,    # ACME Solar Holdings Ltd.
        "SUNDARMFIN.NS": 0.01,   # Sundaram Finance Limited
        "ANTHEM.NS": 0.01,       # Anthem Biosciences Limited
        "MAXHEALTH.NS": 0.01,    # Max Healthcare Institute Limited
        "BIOCON.NS": 0.01,       # Biocon Limited
        "ETERNAL.NS": 0.01,      # Eternal Limited
        }
    },
           "ICICI Midcap Fund": {
        "nav": 393.47,
        # Updated to ICICI Prudential Midcap Fund's Monthly Portfolio
        # Statement as on July 31, 2026 (equity holdings only).
        "holdings": {
        "APARINDS.NS": 4.94,
        "HINDPETRO.NS": 4.77,
        "BSE.NS": 4.64,
        "MCX.NS": 4.33,
        "JINDALSTEL.NS": 3.86,
        "APLAPOLLO.NS": 3.29,
        "BHARATFORG.NS": 3.25,
        "MUTHOOTFIN.NS": 3.23,
        "PRESTIGE.NS": 2.88,
        "JSL.NS": 2.87,
        "POLICYBZR.NS": 2.84,
        "KEI.NS": 2.75,
        "UPL.NS": 2.63,
        "NAM-INDIA.NS": 2.40,
        "CUMMINSIND.NS": 2.06,
        "KPRMILL.NS": 2.02,
        "GODREJPROP.NS": 1.96,
        "GVT&D.NS": 1.95,
        "VAML.NS": 1.93,
        "POWERINDIA.NS": 1.87,
        "NAVINFLUOR.NS": 1.82,
        "SONACOMS.NS": 1.75,
        "UNOMINDA.NS": 1.73,
        "SRF.NS": 1.68,
        "ESCORTS.NS": 1.65,
        "360ONE.NS": 1.62,
        "BHARTIHEXA.NS": 1.52,
        "INDUSINDBK.NS": 1.46,
        "SCHAEFFLER.NS": 1.46,
        "DIXON.NS": 1.28,
        "MOTHERSON.NS": 1.22,
        "SAIL.NS": 1.16,
        "VEDL.NS": 1.12,
        "SUPREMEIND.NS": 1.12,
        "POLYCAB.NS": 1.10,
        "OBEROIRLTY.NS": 1.04,
        "FLUOROCHEM.NS": 1.04,
        "VOLTAS.NS": 0.98,
        "LENSKART.NS": 0.96,
        "NATIONALUM.NS": 0.90,
        "GRINDWELL.NS": 0.80,
        "ASTRAL.NS": 0.77,
        "BLUESTARCO.NS": 0.73,
        "COROMANDEL.NS": 0.71,
        "DEEPAKNTR.NS": 0.67,
        "AMBUJACEM.NS": 0.66,
        "BEML.NS": 0.61,
        "JYOTICNC.NS": 0.55,
        "PIIND.NS": 0.53,
        "CROMPTON.NS": 0.44,
        "SBICARD.NS": 0.43,
        "AARTIIND.NS": 0.43,
        "IRCTC.NS": 0.42,
        "IRB.NS": 0.35,
        "ATUL.NS": 0.35,
        "ENDURANCE.NS": 0.34,
        "PPLPHARMA.NS": 0.27,
        "SYNGENE.NS": 0.20,
        "RATNAMANI.NS": 0.18,
        "MRF.NS": 0.17,
        "HONAUT.NS": 0.16,
        "THERMAX.NS": 0.16,
        "BALKRISIND.NS": 0.14,
        "VISL.NS": 0.14,
        "INDIGO.NS": 0.13,
        "CARBORUNIV.NS": 0.12,
        "JKCEMENT.NS": 0.10,
        "HINDZINC.NS": 0.09,
        "ASTRAZEN.NS": 0.07,
        "ACC.NS": 0.04,
        "KAJARIACER.NS": 0.03,
        "CHEMPLASTS.NS": 0.02,
        "ASTEC.NS": 0.01,
        "CAMLINFINE.NS": 0.01,
        "GUJGASLTD.NS": 0.01,
        "CRISIL.NS": 0.0,
        }
    },

    # Updated to Edelweiss Mutual Fund's Portfolio Statement
    # as on July 31, 2026 (equity holdings only; weights are "% to Net Assets").
    # Excludes TREPS/Reverse Repo, Accrued Interest, and Net Receivables/
    # (Payables) lines (cash-equivalents, not equities).
    # "SPR Auto Technologies Ltd." (0.14%) is omitted - ticker could not be
    # confidently resolved on NSE. "Deepak Nitrite Ltd." (0.00%) is omitted
    # since it has no impact on the NAV calc.
    "Edelweiss Mid Cap Fund": {
        "nav": 130.74,
        "holdings": {
            "FEDERALBNK.NS": 4.00,   # The Federal Bank Ltd.
            "BSE.NS": 2.33,          # BSE Ltd.
            "MCX.NS": 2.26,          # Multi Commodity Exchange Of India Ltd.
            "MARICO.NS": 2.19,       # Marico Ltd.
            "PERSISTENT.NS": 2.15,   # Persistent Systems Ltd.
            "FORTIS.NS": 2.11,       # Fortis Healthcare Ltd.
            "COFORGE.NS": 2.01,      # Coforge Ltd.
            "SOLARINDS.NS": 2.01,    # Solar Industries India Ltd.
            "IDFCFIRSTB.NS": 1.80,   # IDFC First Bank Ltd.
            "RADICO.NS": 1.76,       # Radico Khaitan Ltd.
            "CREDITACC.NS": 1.73,    # Creditaccess Grameen Ltd.
            "IPCALAB.NS": 1.71,      # IPCA Laboratories Ltd.
            "CUB.NS": 1.67,          # City Union Bank Ltd.
            "BHARATFORG.NS": 1.60,   # Bharat Forge Ltd.
            "LTF.NS": 1.59,          # L&T Finance Ltd.
            "AUBANK.NS": 1.54,       # AU Small Finance Bank Ltd.
            "DIXON.NS": 1.51,        # Dixon Technologies (India) Ltd.
            "INDIANB.NS": 1.49,      # Indian Bank
            "TVSMOTOR.NS": 1.49,     # TVS Motor Company Ltd.
            "INDHOTEL.NS": 1.47,     # The Indian Hotels Company Ltd.
            "PHOENIXLTD.NS": 1.45,   # The Phoenix Mills Ltd.
            "UNOMINDA.NS": 1.43,     # UNO Minda Ltd.
            "KARURVYSYA.NS": 1.43,   # Karur Vysya Bank Ltd.
            "MAXHEALTH.NS": 1.41,    # Max Healthcare Institute Ltd.
            "OBEROIRLTY.NS": 1.34,   # Oberoi Realty Ltd.
            "BHEL.NS": 1.32,         # Bharat Heavy Electricals Ltd.
            "PRESTIGE.NS": 1.31,     # Prestige Estates Projects Ltd.
            "ASHOKLEY.NS": 1.30,     # Ashok Leyland Ltd.
            "APLAPOLLO.NS": 1.29,    # APL Apollo Tubes Ltd.
            "INDUSTOWER.NS": 1.26,   # Indus Towers Ltd.
            "HDFCAMC.NS": 1.25,      # HDFC Asset Management Company Ltd.
            "KEI.NS": 1.24,          # KEI Industries Ltd.
            "JSL.NS": 1.20,          # Jindal Stainless Ltd.
            "GVT&D.NS": 1.19,        # GE Vernova T&D India Limited
            "MFSL.NS": 1.18,         # Max Financial Services Ltd.
            "HINDPETRO.NS": 1.17,    # Hindustan Petroleum Corporation Ltd.
            "JSWENERGY.NS": 1.16,    # JSW Energy Ltd.
            "POLICYBZR.NS": 1.15,    # PB Fintech Ltd.
            "JKCEMENT.NS": 1.13,     # JK Cement Ltd.
            "SUNDARMFIN.NS": 1.10,   # Sundaram Finance Ltd.
            "AJANTPHARM.NS": 1.08,   # Ajanta Pharma Ltd.
            "PAGEIND.NS": 1.05,      # Page Industries Ltd.
            "MRF.NS": 1.01,          # MRF Ltd.
            "LUPIN.NS": 0.98,        # Lupin Ltd.
            "CHOLAFIN.NS": 0.97,     # Cholamandalam Investment & Finance Company Ltd.
            "TORNTPOWER.NS": 0.96,   # Torrent Power Ltd.
            "POLYCAB.NS": 0.96,      # Polycab India Ltd.
            "CUMMINSIND.NS": 0.93,   # Cummins India Ltd.
            "ENDURANCE.NS": 0.92,    # Endurance Technologies Ltd.
            "ATHERENERG.NS": 0.91,   # Ather Energy Ltd.
            "MANKIND.NS": 0.91,      # Mankind Pharma Ltd.
            "VMM.NS": 0.89,          # Vishal Mega Mart Ltd
            "BEL.NS": 0.89,          # Bharat Electronics Ltd.
            "JUBLFOOD.NS": 0.88,     # Jubilant Foodworks Ltd.
            "SUMICHEM.NS": 0.84,     # Sumitomo Chemical India Ltd.
            "NMDC.NS": 0.83,         # NMDC Ltd.
            "IDEA.NS": 0.83,         # Vodafone Idea Ltd.
            "LGEINDIA.NS": 0.82,     # LG Electronics India Ltd.
            "SAIL.NS": 0.80,         # Steel Authority of India Ltd.
            "TORNTPHARM.NS": 0.80,   # Torrent Pharmaceuticals Ltd.
            "GROWW.NS": 0.74,        # Billionbrains Garage Ventures Ltd.
            "COROMANDEL.NS": 0.68,   # Coromandel International Ltd.
            "360ONE.NS": 0.67,       # 360 One Wam Ltd.
            "ICICIAMC.NS": 0.67,     # ICICI Prudential Asset Mgmt Co Ltd.
            "SCHAEFFLER.NS": 0.65,   # Schaeffler India Ltd.
            "LAURUSLABS.NS": 0.64,   # Laurus Labs Ltd.
            "BLUESTARCO.NS": 0.63,   # Blue Star Ltd.
            "BIKAJI.NS": 0.59,       # Bikaji Foods International Ltd.
            "CRAFTSMAN.NS": 0.58,    # Craftsman Automation Ltd.
            "BHARTIHEXA.NS": 0.56,   # Bharti Hexacom Ltd.
            "THERMAX.NS": 0.53,      # Thermax Ltd.
            "SRF.NS": 0.49,          # SRF Ltd.
            "PNBHOUSING.NS": 0.47,   # PNB Housing Finance Ltd.
            "NYKAA.NS": 0.46,        # FSN E-Commerce Ventures Ltd.
            "EXIDEIND.NS": 0.46,     # Exide Industries Ltd.
            "TRITURBINE.NS": 0.45,   # Triveni Turbine Ltd.
            "FSL.NS": 0.43,          # Firstsource Solutions Ltd.
            "CEATLTD.NS": 0.42,      # CEAT Ltd.
            "OIL.NS": 0.41,          # Oil India Ltd.
            "BDL.NS": 0.41,          # Bharat Dynamics Ltd.
            "BERGEPAINT.NS": 0.39,   # Berger Paints (I) Ltd.
            "ITCHOTELS.NS": 0.39,    # ITC Hotels Ltd.
            "SUPREMEIND.NS": 0.35,   # Supreme Industries Ltd.
            "SWIGGY.NS": 0.34,       # Swiggy Ltd.
            "ELECON.NS": 0.34,       # Elecon Engineering Company Ltd.
            "LENSKART.NS": 0.30,     # Lenskart Solutions Ltd.
            "ASTRAL.NS": 0.30,       # Astral Ltd.
            "NETWEB.NS": 0.29,       # Netweb Technologies India Ltd.
            "NAVINFLUOR.NS": 0.27,   # Navin Fluorine International Ltd.
            "CGPOWER.NS": 0.26,      # CG Power and Industrial Solutions Ltd.
            "BALKRISIND.NS": 0.25,   # Balkrishna Industries Ltd.
            "COCHINSHIP.NS": 0.19,   # Cochin Shipyard Ltd.
        }
    },

    # Updated to HDFC Mutual Fund's Portfolio Statement
    # as on July 31, 2026 (equity holdings only; weights are "% to NAV").
    "HDFC Mid Cap Fund": {
        "nav": 237.08,
        "holdings": {
            "FEDERALBNK.NS": 4.36,
            "AUBANK.NS": 3.96,
            "MFSL.NS": 3.72,
            "BALKRISIND.NS": 3.37,
            "IPCALAB.NS": 3.01,
            "INDIANB.NS": 2.93,
            "FORTIS.NS": 2.91,
            "GLENMARK.NS": 2.85,
            "COFORGE.NS": 2.56,
            "MARICO.NS": 2.51,
            "M&MFIN.NS": 2.43,
            "VMM.NS": 2.30,
            "HINDPETRO.NS": 2.26,
            "CUMMINSIND.NS": 2.19,
            "AUROPHARMA.NS": 2.01,
            "UNITDSPR.NS": 1.98,
            "TATACOMM.NS": 1.86,
            "PERSISTENT.NS": 1.81,
            "ALKEM.NS": 1.73,
            "APOLLOTYRE.NS": 1.71,
            "MPHASIS.NS": 1.59,
            "DABUR.NS": 1.55,
            "JINDALSTEL.NS": 1.54,
            "POLICYBZR.NS": 1.49,
            "AIAENG.NS": 1.48,
            "UNIONBANK.NS": 1.47,
            "DELHIVERY.NS": 1.45,
            "GLAND.NS": 1.44,
            "BHARATFORG.NS": 1.35,
            "KARURVYSYA.NS": 1.28,
            "ETERNAL.NS": 1.24,
            "BOSCHLTD.NS": 1.22,
            "STARHEALTH.NS": 1.18,
            "INDUSINDBK.NS": 1.14,
            "NAM-INDIA.NS": 1.10,
            "COROMANDEL.NS": 1.09,
            "INDHOTEL.NS": 0.99,
            "ESCORTS.NS": 0.87,
            "GODREJCP.NS": 0.84,
            "REDINGTON.NS": 0.84,
            "ICICIGI.NS": 0.83,
            "HEXT.NS": 0.80,
            "IGL.NS": 0.74,
            "SONACOMS.NS": 0.74,
            "CROMPTON.NS": 0.71,
            "HAVELLS.NS": 0.70,
            "DIXON.NS": 0.69,
            "SUNDRMFAST.NS": 0.67,
            "CUB.NS": 0.65,
            "ACC.NS": 0.61,
            "SKFINDUS.NS": 0.61,
            "FLUOROCHEM.NS": 0.58,
            "TIMKEN.NS": 0.58,
            "SUPREMEIND.NS": 0.55,
            "ASTERDM.NS": 0.42,
            "ARVIND.NS": 0.40,
            "KEC.NS": 0.40,
            "AARTIIND.NS": 0.36,
            "OFSS.NS": 0.36,
            "VTL.NS": 0.35,
            "CHOLAHLDNG.NS": 0.33,
            "SKFINDIA.NS": 0.33,
            "VESUVIUS.NS": 0.30,
            "CIEINDIA.NS": 0.28,
            "EMAMILTD.NS": 0.28,
            "SYMPHONY.NS": 0.24,
            "BHARTIHEXA.NS": 0.21,
            "COLPAL.NS": 0.21,
            "FIVESTAR.NS": 0.20,
            "PETRONET.NS": 0.20,
            "GROWW.NS": 0.19,
            "NAVNETEDUL.NS": 0.18,
            "GREENLAM.NS": 0.15,
            "GREENPLY.NS": 0.15,
            "LGEINDIA.NS": 0.14,
            "KNRCON.NS": 0.12,
            "DHANUKA.NS": 0.10,
            "GREENPANEL.NS": 0.08,
            "JAGRAN.NS": 0.03,
        }
    },

    # Updated to Invesco Mutual Fund's Monthly Portfolio Statement
    # as on July 31, 2026 (equity holdings only; weights are "% to Net Assets").
    # Excludes TREPS/Reverse Repo and Net Receivables/(Payables) lines
    # (cash-equivalents, not equities).
    # "Manipal Health Enterprises Ltd" (0.51%) is omitted - it is an
    # unlisted company and has no resolvable NSE ticker.
    "Invesco India Midcap Fund": {
        "nav": 243.67,
        "holdings": {
            "PRESTIGE.NS": 7.16,     # Prestige Estates Projects Limited
            "FEDERALBNK.NS": 6.42,   # The Federal Bank Limited
            "MAXHEALTH.NS": 6.21,    # Max Healthcare Institute Limited
            "MEESHO.NS": 4.64,       # Meesho Ltd
            "MEDANTA.NS": 4.37,      # Global Health Limited
            "AUBANK.NS": 4.22,       # AU Small Finance Bank Limited
            "ETERNAL.NS": 4.18,      # Eternal Limited
            "INDUSINDBK.NS": 4.06,   # IndusInd Bank Limited
            "BSE.NS": 3.86,          # BSE Limited
            "LTF.NS": 3.81,          # L&T Finance Limited
            "INDIGO.NS": 3.76,       # InterGlobe Aviation Limited
            "MFSL.NS": 3.16,         # Max Financial Services Limited
            "SAILIFE.NS": 3.05,      # Sai Life Sciences Limited
            "JKCEMENT.NS": 2.93,     # JK Cement Limited
            "GLENMARK.NS": 2.83,     # Glenmark Pharmaceuticals Limited
            "ABB.NS": 2.55,          # ABB India Limited
            "SRF.NS": 2.51,          # SRF Limited
            "CPPLUS.NS": 2.33,       # Aditya Infotech Limited
            "NYKAA.NS": 2.28,        # FSN E-Commerce Ventures Limited
            "TORNTPOWER.NS": 2.23,   # Torrent Power Limited
            "TRENT.NS": 2.11,        # Trent Limited
            "SWIGGY.NS": 2.08,       # Swiggy Limited
            "AMBER.NS": 2.07,        # Amber Enterprises India Limited
            "DIXON.NS": 1.48,        # Dixon Technologies (India) Limited
            "ICICIGI.NS": 1.47,      # ICICI Lombard General Insurance Company Limited
            "BHARATFORG.NS": 1.27,   # Bharat Forge Limited
            "PHOENIXLTD.NS": 1.24,   # The Phoenix Mills Limited
            "KIMS.NS": 1.06,         # Krishna Institute Of Medical Sciences Limited
            "CORONA.NS": 1.00,       # Corona Remedies Limited
            "CRAFTSMAN.NS": 0.97,    # Craftsman Automation Limited
            "ETHOSLTD.NS": 0.92,     # Ethos Ltd.
            "DRAGARWQ.NS": 0.73,     # Dr Agarwals Health Care Limited
            "TIINDIA.NS": 0.68,      # Tube Investments Of India Limited
            "TIMKEN.NS": 0.58,       # Timken India Limited
            "BANSALWIRE.NS": 0.50,   # Bansal Wire Industries Limited
            "CARBORUNIV.NS": 0.45,   # Carborundum Universal Limited
            "WEWORK.NS": 0.44,       # Wework India Management Limited
            "MAXESTATES.NS": 0.36,   # Max Estates Limited
            "SONATSOFTW.NS": 0.33,   # Sonata Software Limited
            "VMM.NS": 0.19,          # Vishal Mega Mart Limited
        }
    },

    # Updated to Motilal Oswal Mutual Fund's Monthly Portfolio Statement
    # as on July 31, 2026 (equity holdings only; weights are "% to Net Assets").
    "Motilal Oswal Midcap Fund": {
        "nav": 121.33,
        "holdings": {
            "KALYANKJIL.NS": 8.87,   # Kalyan Jewellers India Limited
            "PAYTM.NS": 8.08,        # One 97 Communications Limited
            "ETERNAL.NS": 6.37,      # Eternal Limited
            "COFORGE.NS": 5.58,      # Coforge Limited
            "ABCAPITAL.NS": 5.20,    # Aditya Birla Capital Limited
            "KEI.NS": 4.81,          # KEI Industries Limited
            "PERSISTENT.NS": 4.75,   # Persistent Systems Ltd
            "GROWW.NS": 4.08,        # Billionbrains Garage Ventures Ltd (Groww)
            "SHRIRAMFIN.NS": 3.75,   # Shriram Finance Limited
            "DIXON.NS": 3.48,        # Dixon Technologies (India) Limited
            "MCX.NS": 2.90,          # Multi Commodity Exchange of India Limited
            "TIINDIA.NS": 2.83,      # Tube Investments Of India Limited
            "BSE.NS": 2.73,          # BSE Limited
            "STLTECH.NS": 2.66,      # Sterlite Technologies Limited
            "PRESTIGE.NS": 2.58,     # Prestige Estates Projects Limited
            "LTF.NS": 2.55,          # L&T Finance Limited
            "BHARTIHEXA.NS": 2.55,   # Bharti Hexacom Limited
            "SUZLON.NS": 2.34,       # Suzlon Energy Limited
            "IDFCFIRSTB.NS": 2.25,   # IDFC First Bank Limited
            "MAXHEALTH.NS": 2.20,    # Max Healthcare Institute Limited
            "POLICYBZR.NS": 2.16,    # PB Fintech Limited
            "PREMIERENE.NS": 2.15,   # Premier Energies Limited
            "MOTHERSON.NS": 2.09,    # Samvardhana Motherson International Limited
            "ICICIAMC.NS": 1.98,     # ICICI Prudential Asset Management Company Limited
            "BEL.NS": 1.90,          # Bharat Electronics Limited
            "INDIGO.NS": 1.83,       # InterGlobe Aviation Limited
            "WAAREEENER.NS": 1.63,   # Waaree Energies Limited
            "ADANIENT.NS": 0.91,     # Adani Enterprises Limited
            "PWL.NS": 0.60,          # PhysicsWallah Limited
            "AUBANK.NS": 0.06,       # AU Small Finance Bank Limited
        }
    },

    # Updated to WhiteOak Capital Mutual Fund's Portfolio Statement
    # as on July 31, 2026 (equity holdings only; weight used is the
    # combined "% to Net Assets" column, i.e. cash equity + any futures
    # overlay in the same stock).
    # Excludes: Bank Nifty Index (derivative, not a stock), REITs
    # (Nexus Select Trust, Embassy Office Parks REIT), InvITs (Vertis
    # Infrastructure Trust), Treasury Bills, and Reverse Repo/TREPS
    # (cash-equivalents, not equities).
    # The following holdings are omitted because their NSE ticker could
    # not be confidently resolved (avoiding the risk of mapping to the
    # wrong listed company): Omnitech Engineering Ltd (0.31%), Travel
    # Food Services Ltd (0.21%), Yash Highvoltage Ltd (0.19%), Epack
    # Prefab Technologies Ltd (0.16%), Onemi Technology Solutions Ltd
    # (0.14%), Indiqube Spaces Ltd (0.09%), Orkla India Ltd (0.09%),
    # EMA Partners India Ltd (0.04%), Bharat Bijlee Ltd (0.04%), Aye
    # Finance Ltd (0.04%), Carraro India Ltd (0.03%), Clean Max Enviro
    # Energy Solutions Ltd (0.01%, unlisted), Juniper Green Energy Ltd
    # (0.29%).
    "WhiteOak Capital Midcap Fund": {
        "nav": 23.66,
        "holdings": {
            "MFSL.NS": 3.11,          # Max Financial Services Limited
            "BHARTIHEXA.NS": 2.90,    # Bharti Hexacom Limited
            "FEDERALBNK.NS": 2.84,    # The Federal Bank Limited
            "COFORGE.NS": 2.72,       # Coforge Limited
            "LAURUSLABS.NS": 2.46,    # Laurus Labs Limited
            "FORTIS.NS": 2.30,        # Fortis Healthcare Limited
            "PERSISTENT.NS": 2.23,    # Persistent Systems Limited
            "POLICYBZR.NS": 2.16,     # PB Fintech Limited
            "PHOENIXLTD.NS": 2.12,    # The Phoenix Mills Limited
            "VMM.NS": 2.01,           # Vishal Mega Mart Limited
            "BHEL.NS": 1.81,          # Bharat Heavy Electricals Limited
            "NAUKRI.NS": 1.77,        # Info Edge Limited
            "OIL.NS": 1.74,           # Oil India Limited
            "INDUSINDBK.NS": 1.68,    # IndusInd Bank Limited
            "MARICO.NS": 1.67,        # Marico Limited
            "360ONE.NS": 1.58,        # 360 One WAM Limited
            "NAM-INDIA.NS": 1.56,     # Nippon Life India Asset Management Limited
            "BERGEPAINT.NS": 1.55,    # Berger Paints Limited
            "AIAENG.NS": 1.47,        # AIA Engineering Limited
            "SONACOMS.NS": 1.37,      # Sona BLW Precision Forgings Limited
            "KEI.NS": 1.37,           # KEI Industries Limited
            "ALKEM.NS": 1.34,         # Alkem Laboratories Limited
            "OFSS.NS": 1.33,          # Oracle Financial Services Software Limited
            "MUTHOOTFIN.NS": 1.32,    # Muthoot Finance Limited
            "NATIONALUM.NS": 1.28,    # National Aluminium Company Limited
            "RECLTD.NS": 1.25,        # REC Limited
            "IPCALAB.NS": 1.19,       # IPCA Laboratories Limited
            "TIINDIA.NS": 1.17,       # Tube Investments of India Limited
            "MAXHEALTH.NS": 1.16,     # Max Healthcare Institute Limited
            "MOTILALOFS.NS": 1.11,    # Motilal Oswal Financial Services Limited
            "ABCAPITAL.NS": 1.04,     # Aditya Birla Capital Limited
            "GODREJPROP.NS": 1.02,    # Godrej Properties Limited
            "BLUESTARCO.NS": 1.02,    # Blue Star Limited
            "NYKAA.NS": 1.01,         # FSN E-Commerce Ventures Limited
            "PAGEIND.NS": 0.98,       # Page Industries Limited
            "LENSKART.NS": 0.93,      # Lenskart Solutions Limited
            "JSWINFRA.NS": 0.91,      # JSW Infrastructure Ltd
            "AADHARHFC.NS": 0.90,     # Aadhar Housing Finance Limited
            "MANKIND.NS": 0.89,       # Mankind Pharma Limited
            "JSL.NS": 0.88,           # Jindal Stainless Limited
            "ABBOTINDIA.NS": 0.86,    # Abbott India Limited
            "GLAND.NS": 0.85,         # Gland Pharma Limited
            "POWERINDIA.NS": 0.83,    # Hitachi Energy India Limited
            "GVT&D.NS": 0.83,         # GE Vernova T&D India Limited
            "HEROMOTOCO.NS": 0.81,    # Hero MotoCorp Limited
            "COROMANDEL.NS": 0.81,    # Coromandel International Limited
            "CUMMINSIND.NS": 0.80,    # Cummins India Limited
            "NAVINFLUOR.NS": 0.77,    # Navin Fluorine International Limited
            "PETRONET.NS": 0.75,      # Petronet LNG Limited
            "BANKINDIA.NS": 0.74,     # Bank of India
            "MCX.NS": 0.74,           # Multi Commodity Exchange of India Limited
            "AJANTPHARM.NS": 0.74,    # Ajanta Pharma Limited
            "HINDPETRO.NS": 0.66,     # Hindustan Petroleum Corporation Limited
            "GODREJIND.NS": 0.66,     # Godrej Industries Limited
            "NH.NS": 0.65,            # Narayana Hrudayalaya Limited
            "THELEELA.NS": 0.65,         # Leela Palaces Hotels & Resorts Limited
            "COLPAL.NS": 0.62,        # Colgate Palmolive Limited
            "M&MFIN.NS": 0.59,        # Mahindra & Mahindra Financial Services Limited
            "FIVESTAR.NS": 0.59,      # Five Star Business Finance Limited
            "ATHERENERG.NS": 0.58,    # Ather Energy Limited
            "GROWW.NS": 0.58,         # Billionbrains Garage Ventures Ltd
            "AZAD.NS": 0.57,          # Azad Engineering Ltd
            "INDIASHLTR.NS": 0.57,    # India Shelter Finance Corporation Limited
            "CARERATING.NS": 0.55,    # CARE Ratings Limited
            "KRN.NS": 0.55,           # KRN Heat Exchanger And Refrigeration Limited
            "PAYTM.NS": 0.54,         # One 97 Communications Limited
            "SAILIFE.NS": 0.48,       # Sai Life Sciences Limited
            "NMDC.NS": 0.45,          # NMDC Limited
            "ACUTAAS.NS": 0.45,       # Acutaas Chemicals Limited
            "SUPREMEIND.NS": 0.43,    # Supreme Industries Limited
            "IIFL.NS": 0.43,          # IIFL Finance Limited
            "ABREL.NS": 0.42,         # Aditya Birla Real Estate Limited
            "AJAXENGG.NS": 0.42,      # Ajax Engineering Limited
            "CPPLUS.NS": 0.41,        # Aditya Infotech Limited
            "PNBHOUSING.NS": 0.41,    # PNB Housing Finance Limited
            "NEULANDLAB.NS": 0.41,    # Neuland Laboratories Limited
            "SOUTHBANK.NS": 0.40,     # The South Indian Bank Limited
            "POLYMED.NS": 0.39,       # Poly Medicure Limited
            "TDPOWERSYS.NS": 0.39,    # TD Power Systems Limited
            "DYNAMATECH.NS": 0.38,    # Dynamatic Technologies Limited
            "ENDURANCE.NS": 0.36,     # Endurance Technologies Limited
            "JSWCEMENT.NS": 0.36,     # JSW Cement Limited
            "MANORAMA.NS": 0.33,      # Manorama Industries Limited
            "CARTRADE.NS": 0.33,      # Cartrade Tech Limited
            "ANTHEM.NS": 0.31,        # Anthem Biosciences Limited
            "KIRLOSENG.NS": 0.31,     # Kirloskar Oil Engines Limited
            "EUREKAFORB.NS": 0.30,    # Eureka Forbes Ltd
            "TBOTEK.NS": 0.28,        # TBO Tek Limited
            "SHILPAMED.NS": 0.26,     # Shilpa Medicare Limited
            "IGIL.NS": 0.26,          # International Gemological Institute Limited
            "CHOLAHLDNG.NS": 0.25,    # Cholamandalam Financial Holdings Limited
            "REPCOHOME.NS": 0.25,     # Repco Home Finance Limited
            "METROBRAND.NS": 0.24,    # Metro Brands Limited
            "SOBHA.NS": 0.23,         # Sobha Limited
            "DOMS.NS": 0.22,          # Doms Industries Limited
            "GILLETTE.NS": 0.21,      # Gillette India Limited
            "AUBANK.NS": 0.18,        # AU Small Finance Bank Limited
            "INTELLECT.NS": 0.17,     # Intellect Design Arena Limited
            "LEMONTREE.NS": 0.17,     # Lemon Tree Hotels Limited
            "SAFARI.NS": 0.17,        # Safari Industries Limited
            "UJJIVANSFB.NS": 0.15,    # Ujjivan Small Finance Bank Limited
            "ICICIGI.NS": 0.15,       # ICICI Lombard General Insurance Company Limited
            "AVALON.NS": 0.15,        # Avalon Technologies Limited
            "3MINDIA.NS": 0.14,       # 3M India Limited
            "KIMS.NS": 0.13,          # Krishna Institute Of Medical Sciences Limited
            "SAGILITY.NS": 0.12,      # Sagility Limited
            "AETHER.NS": 0.11,        # Aether Industries Limited
            "PRUDENT.NS": 0.11,       # Prudent Corporate Advisory Services Limited
            "FINEORG.NS": 0.09,       # Fine Organic Industries Limited
            "XPROINDIA.NS": 0.08,     # Xpro India Limited
            "NEWGEN.NS": 0.08,        # Newgen Software Technologies Limited
            "BRIGADE.NS": 0.07,       # Brigade Enterprises Limited
            "ICICIPRULI.NS": 0.06,    # ICICI Prudential Life Insurance Company Limited
            "NSDL.NS": 0.06,          # National Securities Depository Limited
            "SJS.NS": 0.06,           # S.J.S. Enterprises Limited
            "KARURVYSYA.NS": 0.06,    # Karur Vysya Bank Limited
            "AWFIS.NS": 0.05,         # Awfis Space Solutions Limited
            "DIXON.NS": 0.04,         # Dixon Technologies Limited
            "INDIGOPNTS.NS": 0.03,    # Indigo Paints Limited
        }
    }
}

# =========================
# FETCH DATA (fast_info primary + batched-download fallback)
# =========================
#
# WHY THE OLD VERSION COULD SHOW WRONG PRICES / WRONG % CHANGE:
# Both the "previous close" and the "latest close" used as a stand-in
# for the live price came from the SAME single batched yf.download()
# daily-bar table, via close.iloc[-2] / close.iloc[-1]. That sounds
# internally consistent, but early in the trading session Yahoo's
# daily bar for TODAY often doesn't exist yet in that download
# response. When that happens, iloc[-1] silently becomes YESTERDAY's
# close (not live) and iloc[-2] becomes the close from TWO days ago --
# both numbers are stale, and the resulting "% change" can be wrong,
# sometimes even the wrong direction.
#
# FIX: for each ticker, pull BOTH previous close and live price from a
# single fast_info snapshot -- fast_info.previous_close is Yahoo's own
# live "last completed session" reference price and fast_info.last_price
# is the true current quote, so the two numbers can never desync from
# each other the way two daily bars pulled at different times could.
# The batched daily-bar download is kept as a fallback (and still
# powers the "skipped holdings" diagnostics), used only for tickers
# where fast_info comes back empty.
#
# Because this file spans ~150 unique tickers across 6 funds, fast_info
# calls are cached per-ticker for the same duration as the fallback
# batch (ttl=300s) so a 60s auto-refresh doesn't re-hit Yahoo for every
# single symbol on every rerun.

all_tickers = []

for fund in funds.values():
    all_tickers.extend(list(fund["holdings"].keys()))

all_tickers = list(set(all_tickers))


@st.cache_data(ttl=300)
def fetch_data(tickers):
    """Fallback-only daily bar data, used solely when fast_info fails
    for a given ticker (and to power the 'skipped holdings' diagnostics
    for symbols that fail on both sources)."""
    data = yf.download(
        tickers=tickers,
        period="10d",
        interval="1d",
        auto_adjust=True,
        progress=False,
        group_by="ticker",
        threads=False
    )

    return data


@st.cache_data(ttl=300)
def get_quote(ticker):
    """Primary source: previous close AND live price from the SAME
    live-quote snapshot, so they can never desync from each other."""
    try:
        fi = yf.Ticker(ticker).fast_info
        live_price = fi.get("last_price") or fi.get("lastPrice")
        prev_close = (
            fi.get("previous_close")
            or fi.get("previousClose")
            or fi.get("regular_market_previous_close")
        )
        if live_price and prev_close:
            return float(prev_close), float(live_price)
    except Exception:
        pass
    return None, None


try:
    data = fetch_data(all_tickers)

except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

# =========================
# TITLE
# =========================

st.title("📈 Live Midcap Fund NAV Tracker")

india = pytz.timezone("Asia/Kolkata")

current_time = datetime.now(india).strftime("%d-%m-%Y %I:%M:%S %p")

st.write(f"Last Updated: {current_time}")

# =========================
# HELPER: SAFE PRICE EXTRACTION (fallback path only)
# =========================

def get_close_series(data, ticker, all_tickers):
    """
    Fallback-only helper. Return the Close price series for a ticker,
    handling both the multi-ticker (MultiIndex) and single-ticker
    column layouts that yf.download can return. Only used when
    fast_info didn't return a usable quote for this ticker.
    """
    if len(all_tickers) == 1:
        if "Close" not in data.columns:
            raise KeyError(f"No Close column for {ticker}")
        return data["Close"].dropna()

    if ticker not in data.columns.get_level_values(0):
        raise KeyError(f"{ticker} not present in downloaded data")

    close = data[ticker]["Close"].dropna()
    return close


# =========================
# NAV CALCULATION
# =========================
fund_performance = []
for fund_name, fund_data in funds.items():

    previous_nav = fund_data["nav"]
    holdings = fund_data["holdings"]

    weighted_return = 0.0
    stock_rows = []
    skipped = []

    for ticker, weight in holdings.items():

        try:
            # PRIMARY: single consistent snapshot from fast_info
            previous_close, latest_close = get_quote(ticker)

            if previous_close is None or latest_close is None:
                # FALLBACK: last COMPLETE daily bar pair from the
                # batched download, only used if fast_info failed
                close = get_close_series(data, ticker, all_tickers)

                if len(close) < 2:
                    skipped.append((ticker, weight, "Insufficient price history (newly listed / no prior close)"))
                    continue

                latest_close = float(close.iloc[-1])
                previous_close = float(close.iloc[-2])

            if previous_close == 0 or pd.isna(previous_close) or pd.isna(latest_close):
                skipped.append((ticker, weight, "Invalid/zero close price"))
                continue

            change_percent = (
                (latest_close - previous_close)
                / previous_close
            ) * 100

            contribution = (
                weight / 100
            ) * change_percent

            weighted_return += contribution

            stock_rows.append({
                "Stock": ticker,
                "Weight %": round(weight, 2),
                "Price Change %": round(change_percent, 2),
                "Contribution": round(contribution, 3)
            })

        except KeyError:
            skipped.append((ticker, weight, "Ticker not found in yfinance data (check symbol / possibly delisted)"))
        except IndexError:
            skipped.append((ticker, weight, "Not enough trading days available (likely a recent listing)"))
        except Exception as e:
            skipped.append((ticker, weight, f"Unexpected error: {e}"))

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
