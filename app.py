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
# NOTE ON "nav": this is the fund's last known official per-unit NAV,
# used as the "Previous NAV" baseline the app grows from. The portfolio
# statements below only report holdings/weights, not per-unit NAV, so
# these figures are carried over unchanged from the last update. Swap
# them in if/when you have the actual Aug 31, 2026 (or later) NAV.

funds = {

    # Updated to HSBC Mutual Fund's Portfolio Statement
    # as on August 31, 2026 (equity holdings only; weights are "% to Net Assets").
    # Excludes Treps and Net Current Assets (cash-equivalent lines, not equities).
    # Entries listed at 0.00% in the statement are omitted (no impact on NAV calc):
    # Eternal Ltd, Biocon Ltd, Schaeffler India Ltd, Billionbrains Garage Ventures Ltd,
    # Abbott India Ltd, Gabriel India Ltd, BSE Ltd, NTPC Green Energy Ltd.
    # "Bosch Home Comfort India Limited" (0.08%) is omitted - ticker could not be
    # confidently resolved on NSE.
    "HSBC Midcap Fund": {
        "nav": 544.76,
        "holdings": {
        "LENSKART.NS": 4.81,     # Lenskart Solutions Limited
        "MEESHO.NS": 4.00,       # Meesho Limited
        "FEDERALBNK.NS": 3.96,   # The Federal Bank Limited
        "PIRAMALFIN.NS": 3.92,   # Piramal Finance Ltd
        "POLICYBZR.NS": 3.87,    # PB Fintech Limited
        "NYKAA.NS": 3.61,        # FSN E-Commerce Ventures Limited
        "ATHERENERG.NS": 3.57,   # Ather Energy Limited
        "APARINDS.NS": 3.38,     # APAR INDUSTRIES LTD
        "GVT&D.NS": 3.20,        # GE Vernova T&D India Limited
        "BHARATFORG.NS": 2.79,   # Bharat Forge Limited
        "RADICO.NS": 2.70,       # Radico Khaitan Limited
        "CPPLUS.NS": 2.64,       # Aditya Infotech Limited
        "M&MFIN.NS": 2.27,       # Mahindra & Mahindra Financial Serv Ltd.
        "POWERINDIA.NS": 2.19,   # Hitachi Energy India Limited
        "NAM-INDIA.NS": 2.16,    # Nippon Life India Asset Management Ltd
        "JSWENERGY.NS": 2.13,    # JSW Energy Limited
        "NETWEB.NS": 2.11,       # Netweb Technologies India Limited
        "MANKIND.NS": 2.10,      # Mankind Pharma Limited
        "NAVINFLUOR.NS": 2.06,   # Navin Fluorine International Limited
        "THYROCARE.NS": 1.99,    # Thyrocare Technologies Limited
        "ZYDUSLIFE.NS": 1.98,    # Zydus Lifesciences Limited
        "COFORGE.NS": 1.92,      # Coforge Limited
        "THERMAX.NS": 1.88,      # Thermax Limited
        "COCHINSHIP.NS": 1.80,   # Cochin Shipyard Limited
        "AUBANK.NS": 1.78,       # AU Small Finance Bank Limited
        "DATAPATTNS.NS": 1.77,   # Data Patterns (India) Limited
        "IPCALAB.NS": 1.75,      # IPCA Laboratories Limited
        "ABCAPITAL.NS": 1.74,    # Aditya Birla Capital Limited
        "PRESTIGE.NS": 1.73,     # Prestige Estates Projects Limited
        "KFINTECH.NS": 1.67,     # KFin Technologies Limited
        "ASHOKLEY.NS": 1.65,     # Ashok Leyland Limited
        "CUB.NS": 1.64,          # City Union Bank Limited
        "MCX.NS": 1.63,          # Multi Commodity Exchange of India Ltd.
        "INDIANB.NS": 1.57,      # Indian Bank
        "PAYTM.NS": 1.47,        # One 97 Communications Limited
        "SHADOWFAX.NS": 1.44,    # Shadowfax Technologies Limited
        "GODFRYPHLP.NS": 1.36,   # Godfrey Phillips India Limited
        "AVALON.NS": 1.34,       # AVALON TECHNOLOGIES LIMITED
        "INDUSINDBK.NS": 1.28,   # IndusInd Bank Limited
        "POLYMED.NS": 1.26,      # Poly Medicure Ltd
        "TDPOWERSYS.NS": 1.22,   # TD Power Systems Limited
        "LUPIN.NS": 1.17,        # Lupin Limited
        "CGPOWER.NS": 0.98,      # CG Power And Industrial Solutions Ltd
        "ATLANTAELE.NS": 0.96,   # Atlanta Electricals Limited
        "DHOOTTRANS.NS": 0.81,   # Dhoot Transmission Limited
        "TRITURBINE.NS": 0.73,   # TRIVENI TURBINE LTD.
        "KIRLOSENG.NS": 0.33,    # Kirloskar Oil Engines Ltd
        "TVSMOTOR.NS": 0.31,     # TVS Motor Company Limited
        "SAFARI.NS": 0.12,       # SAFARI INDUSTRIES (INDIA) LIMITED
        "SYNGENE.NS": 0.07,      # Syngene International Limited
        "CRISIL.NS": 0.05,       # CRISIL Limited
        "IDFCFIRSTB.NS": 0.03,   # IDFC First Bank Limited
        "MFSL.NS": 0.03,         # Max Financial Services Limited
        "MUTHOOTFIN.NS": 0.03,   # Muthoot Finance Limited
        "KEI.NS": 0.03,          # KEI Industries Limited
        "MAZDOCK.NS": 0.02,      # Mazagon Dock Shipbuilders Limited
        "DIXON.NS": 0.02,        # Dixon Technologies (India) Limited
        "JKCEMENT.NS": 0.02,     # JK Cement Limited
        "SWIGGY.NS": 0.02,       # SWIGGY LIMITED
        "CREDITACC.NS": 0.02,    # Creditaccess Grameen Limited
        "PERSISTENT.NS": 0.01,   # PERSISTENT SYSTEMS LTD
        "BHARTIHEXA.NS": 0.01,   # Bharti Hexacom Limited
        "ACMESOLAR.NS": 0.01,    # ACME Solar Holdings Ltd.
        "ANTHEM.NS": 0.01,       # Anthem Biosciences Limited
        "KAYNES.NS": 0.01,       # Kaynes Technology India Ltd.
        "MAXHEALTH.NS": 0.01,    # Max Healthcare Institute Limited
        }
    },

    # Updated to ICICI Prudential Mutual Fund's Portfolio Statement
    # as on August 31, 2026 (equity holdings only).
    # "Gujarat Gas Ltd" kept at 0.01%. "CRISIL Ltd" and "GSPL India Transco Ltd"
    # are marked as negligible (^, <0.01%) in the statement and are omitted
    # (no meaningful impact on NAV calc).
    "ICICI Midcap Fund": {
        "nav": 388.89,
        "holdings": {
        "APARINDS.NS": 5.77,     # Apar Industries Ltd.
        "MCX.NS": 5.30,          # Multi Commodity Exchange Of India Ltd.
        "HINDPETRO.NS": 4.50,    # Hindustan Petroleum Corporation Ltd.
        "JINDALSTEL.NS": 3.96,   # Jindal Steel Ltd.
        "BSE.NS": 3.95,          # BSE Ltd.
        "APLAPOLLO.NS": 3.80,    # APL Apollo Tubes Ltd.
        "POLICYBZR.NS": 3.14,    # PB Fintech Ltd.
        "KEI.NS": 2.99,          # KEI Industries Ltd.
        "BHARATFORG.NS": 2.94,   # Bharat Forge Ltd.
        "MUTHOOTFIN.NS": 2.92,   # Muthoot Finance Ltd.
        "PRESTIGE.NS": 2.76,     # Prestige Estates Projects Ltd.
        "JSL.NS": 2.60,          # Jindal Stainless Ltd.
        "UPL.NS": 2.32,          # UPL Ltd.
        "NAM-INDIA.NS": 2.29,    # Nippon Life India Asset Management Ltd
        "KPRMILL.NS": 2.15,      # K.P.R. Mill Ltd.
        "NAVINFLUOR.NS": 1.97,   # Navin Fluorine International Ltd.
        "GVT&D.NS": 1.90,        # Ge Vernova T&D India Ltd.
        "POWERINDIA.NS": 1.86,   # Hitachi Energy India Ltd.
        "CUMMINSIND.NS": 1.81,   # Cummins India Ltd.
        "GODREJPROP.NS": 1.77,   # Godrej Properties Ltd.
        "UNOMINDA.NS": 1.77,     # UNO Minda Ltd.
        "VAML.NS": 1.75,         # Vedanta Aluminium Metal Ltd.
        "SONACOMS.NS": 1.75,     # Sona Blw Precision Forgings Ltd.
        "360ONE.NS": 1.59,       # 360 One Wam Ltd.
        "SRF.NS": 1.56,          # SRF Ltd.
        "ESCORTS.NS": 1.51,      # Escorts Kubota Ltd
        "INDUSINDBK.NS": 1.39,   # IndusInd Bank Ltd.
        "BHARTIHEXA.NS": 1.38,   # Bharti Hexacom Ltd.
        "SCHAEFFLER.NS": 1.36,   # Schaeffler India Ltd.
        "MOTHERSON.NS": 1.31,    # Samvardhana Motherson International Ltd.
        "DIXON.NS": 1.28,        # Dixon Technologies (India) Ltd.
        "SAIL.NS": 1.27,         # Steel Authority Of India Ltd.
        "VEDL.NS": 1.12,         # Vedanta Ltd.
        "SUPREMEIND.NS": 1.09,   # Supreme Industries Ltd.
        "POLYCAB.NS": 1.08,      # Polycab India Ltd.
        "LENSKART.NS": 1.07,     # Lenskart Solutions Ltd.
        "FLUOROCHEM.NS": 1.06,   # Gujarat Fluorochemicals Ltd.
        "NATIONALUM.NS": 1.02,   # National Aluminium Company Ltd.
        "OBEROIRLTY.NS": 1.01,   # Oberoi Realty Ltd.
        "VOLTAS.NS": 0.84,       # Voltas Ltd.
        "ASTRAL.NS": 0.77,       # Astral Ltd.
        "GRINDWELL.NS": 0.72,    # Grindwell Norton Ltd.
        "DEEPAKNTR.NS": 0.66,    # Deepak Nitrite Ltd.
        "JYOTICNC.NS": 0.64,     # Jyoti CNC Automation Ltd
        "BEML.NS": 0.64,         # BEML Ltd.
        "BLUESTARCO.NS": 0.63,   # Blue Star Ltd.
        "DRREDDY.NS": 0.63,      # Dr. Reddy's Laboratories Ltd.
        "COROMANDEL.NS": 0.62,   # Coromandel International Ltd.
        "AMBUJACEM.NS": 0.58,    # Ambuja Cements Ltd.
        "AARTIIND.NS": 0.44,     # Aarti Industries Ltd.
        "PIIND.NS": 0.44,        # PI Industries Ltd.
        "SBICARD.NS": 0.40,      # SBI Cards & Payment Services Ltd.
        "IRCTC.NS": 0.39,        # Indian Railway Catering and Tourism Corp Ltd.
        "ENDURANCE.NS": 0.34,    # Endurance Technologies Ltd.
        "IRB.NS": 0.32,          # IRB Infrastructure Developers Ltd.
        "ATUL.NS": 0.31,         # Atul Ltd.
        "NYKAA.NS": 0.30,        # FSN E-Commerce Ventures Ltd.
        "PPLPHARMA.NS": 0.28,    # Piramal Pharma Ltd.
        "SYNGENE.NS": 0.20,      # Syngene International Ltd.
        "RATNAMANI.NS": 0.19,    # Ratnamani Metals & Tubes Ltd.
        "PREMIERENE.NS": 0.18,   # Premier Energies Ltd.
        "MRF.NS": 0.16,          # MRF Ltd.
        "VISL.NS": 0.15,         # Vedanta Iron And Steel Ltd.
        "HONAUT.NS": 0.14,       # Honeywell Automation India Ltd.
        "THERMAX.NS": 0.14,      # Thermax Ltd.
        "BALKRISIND.NS": 0.13,   # Balkrishna Industries Ltd.
        "INDIGO.NS": 0.12,       # Interglobe Aviation Ltd.
        "CARBORUNIV.NS": 0.12,   # Carborundum Universal Ltd.
        "CROMPTON.NS": 0.11,     # Crompton Greaves Consumer Electricals Ltd.
        "HINDZINC.NS": 0.09,     # Hindustan Zinc Ltd.
        "JKCEMENT.NS": 0.09,     # JK Cement Ltd.
        "ASTRAZEN.NS": 0.06,     # Astrazeneca Pharma India Ltd.
        "TIINDIA.NS": 0.05,      # Tube Investments of India Ltd.
        "ACC.NS": 0.04,          # ACC Ltd.
        "KAJARIACER.NS": 0.02,   # Kajaria Ceramics Ltd.
        "ASTEC.NS": 0.01,        # Astec LifeSciences Ltd.
        "CAMLINFINE.NS": 0.01,   # Camlin Fine Sciences Ltd.
        "CHEMPLASTS.NS": 0.01,   # Chemplast Sanmar Ltd
        "GUJGASLTD.BO": 0.01,    # Gujarat Gas Ltd
        }
    },

    # Updated to Edelweiss Mutual Fund's Portfolio Statement
    # as on August 31, 2026 (equity holdings only; weights are "% to Net Assets").
    # Excludes TREPS/Reverse Repo, Accrued Interest, and Net Receivables/
    # (Payables) lines (cash-equivalents, not equities).
    # "SPR Auto Technologies Ltd." (0.14%) is omitted - ticker could not be
    # confidently resolved on NSE. "Deepak Nitrite Ltd." (0.00%) is omitted
    # since it has no impact on the NAV calc.
    "Edelweiss Mid Cap Fund": {
        "nav": 128.54,
        "holdings": {
            "FEDERALBNK.NS": 3.73,   # The Federal Bank Ltd.
            "MCX.NS": 2.69,          # Multi Commodity Exchange Of India Ltd.
            "COFORGE.NS": 2.18,      # Coforge Ltd.
            "SOLARINDS.NS": 2.06,    # Solar Industries India Ltd.
            "PERSISTENT.NS": 2.04,   # Persistent Systems Ltd.
            "CUB.NS": 1.98,          # City Union Bank Ltd.
            "BSE.NS": 1.97,          # BSE Ltd.
            "MARICO.NS": 1.94,       # Marico Ltd.
            "FORTIS.NS": 1.91,       # Fortis Healthcare Ltd.
            "IPCALAB.NS": 1.82,      # IPCA Laboratories Ltd.
            "IDFCFIRSTB.NS": 1.72,   # IDFC First Bank Ltd.
            "RADICO.NS": 1.71,       # Radico Khaitan Ltd.
            "LTF.NS": 1.54,          # L&T Finance Ltd.
            "INDIANB.NS": 1.51,      # Indian Bank
            "DIXON.NS": 1.50,        # Dixon Technologies (India) Ltd.
            "AUBANK.NS": 1.50,       # AU Small Finance Bank Ltd.
            "APLAPOLLO.NS": 1.48,    # APL Apollo Tubes Ltd.
            "UNOMINDA.NS": 1.46,     # UNO Minda Ltd.
            "BHARATFORG.NS": 1.44,   # Bharat Forge Ltd.
            "TVSMOTOR.NS": 1.41,     # TVS Motor Company Ltd.
            "CREDITACC.NS": 1.40,    # Creditaccess Grameen Ltd.
            "INDHOTEL.NS": 1.38,     # The Indian Hotels Company Ltd.
            "PHOENIXLTD.NS": 1.37,   # The Phoenix Mills Ltd.
            "KARURVYSYA.NS": 1.36,   # Karur Vysya Bank Ltd.
            "BHEL.NS": 1.35,         # Bharat Heavy Electricals Ltd.
            "KEI.NS": 1.34,          # KEI Industries Ltd.
            "ASHOKLEY.NS": 1.29,     # Ashok Leyland Ltd.
            "OBEROIRLTY.NS": 1.28,   # Oberoi Realty Ltd.
            "POLICYBZR.NS": 1.26,    # PB Fintech Ltd.
            "MAXHEALTH.NS": 1.25,    # Max Healthcare Institute Ltd.
            "PRESTIGE.NS": 1.25,     # Prestige Estates Projects Ltd.
            "HDFCAMC.NS": 1.18,      # HDFC Asset Management Company Ltd.
            "INDUSTOWER.NS": 1.17,   # Indus Towers Ltd.
            "ATHERENERG.NS": 1.17,   # Ather Energy Ltd.
            "MFSL.NS": 1.16,         # Max Financial Services Ltd.
            "GVT&D.NS": 1.15,        # GE Vernova T&D India Limited
            "JSL.NS": 1.07,          # Jindal Stainless Ltd.
            "AJANTPHARM.NS": 1.05,   # Ajanta Pharma Ltd.
            "HINDPETRO.NS": 1.03,    # Hindustan Petroleum Corporation Ltd.
            "JSWENERGY.NS": 1.02,    # JSW Energy Ltd.
            "SUNDARMFIN.NS": 1.00,   # Sundaram Finance Ltd.
            "JKCEMENT.NS": 1.00,     # JK Cement Ltd.
            "MRF.NS": 0.95,          # MRF Ltd.
            "JUBLFOOD.NS": 0.93,     # Jubilant Foodworks Ltd.
            "POLYCAB.NS": 0.93,      # Polycab India Ltd.
            "CHOLAFIN.NS": 0.92,     # Cholamandalam Investment & Finance Company Ltd.
            "ENDURANCE.NS": 0.90,    # Endurance Technologies Ltd.
            "BEL.NS": 0.89,          # Bharat Electronics Ltd.
            "LGEINDIA.NS": 0.88,     # LG Electronics India Ltd.
            "PAGEIND.NS": 0.88,      # Page Industries Ltd.
            "VMM.NS": 0.87,          # Vishal Mega Mart Ltd
            "SAIL.NS": 0.86,         # Steel Authority of India Ltd.
            "IDEA.NS": 0.86,         # Vodafone Idea Ltd.
            "LUPIN.NS": 0.84,        # Lupin Ltd.
            "MANKIND.NS": 0.84,      # Mankind Pharma Ltd.
            "NMDC.NS": 0.81,         # NMDC Ltd.
            "CUMMINSIND.NS": 0.81,   # Cummins India Ltd.
            "SUMICHEM.NS": 0.80,     # Sumitomo Chemical India Ltd.
            "TORNTPOWER.NS": 0.78,   # Torrent Power Ltd.
            "TORNTPHARM.NS": 0.74,   # Torrent Pharmaceuticals Ltd.
            "360ONE.NS": 0.73,       # 360 One Wam Ltd.
            "EXIDEIND.NS": 0.72,     # Exide Industries Ltd.
            "GROWW.NS": 0.69,        # Billionbrains Garage Ventures Ltd.
            "NYKAA.NS": 0.68,        # FSN E-Commerce Ventures Ltd.
            "LAURUSLABS.NS": 0.63,   # Laurus Labs Ltd.
            "ICICIAMC.NS": 0.62,     # ICICI Prudential Asset Mgmt Co Ltd.
            "CRAFTSMAN.NS": 0.62,    # Craftsman Automation Ltd.
            "SCHAEFFLER.NS": 0.60,   # Schaeffler India Ltd.
            "COROMANDEL.NS": 0.58,   # Coromandel International Ltd.
            "BIKAJI.NS": 0.54,       # Bikaji Foods International Ltd.
            "BLUESTARCO.NS": 0.52,   # Blue Star Ltd.
            "BHARTIHEXA.NS": 0.51,   # Bharti Hexacom Ltd.
            "PNBHOUSING.NS": 0.48,   # PNB Housing Finance Ltd.
            "HEROMOTOCO.NS": 0.48,   # Hero MotoCorp Ltd.
            "NETWEB.NS": 0.47,       # Netweb Technologies India Ltd.
            "THERMAX.NS": 0.45,      # Thermax Ltd.
            "SRF.NS": 0.45,          # SRF Ltd.
            "TRITURBINE.NS": 0.41,   # Triveni Turbine Ltd.
            "OIL.NS": 0.41,          # Oil India Ltd.
            "CEATLTD.NS": 0.39,      # CEAT Ltd.
            "BDL.NS": 0.39,          # Bharat Dynamics Ltd.
            "ITCHOTELS.NS": 0.36,    # ITC Hotels Ltd.
            "BERGEPAINT.NS": 0.35,   # Berger Paints (I) Ltd.
            "FSL.NS": 0.35,          # Firstsource Solutions Ltd.
            "LENSKART.NS": 0.34,     # Lenskart Solutions Ltd.
            "SUPREMEIND.NS": 0.34,   # Supreme Industries Ltd.
            "SWIGGY.NS": 0.32,       # Swiggy Ltd.
            "ELECON.NS": 0.31,       # Elecon Engineering Company Ltd.
            "PINELABS.NS": 0.30,     # Pine Labs Ltd.
            "ASTRAL.NS": 0.30,       # Astral Ltd.
            "NAVINFLUOR.NS": 0.29,   # Navin Fluorine International Ltd.
            "SJS.NS": 0.29,          # S.J.S. Enterprises Ltd.
            "CGPOWER.NS": 0.26,      # CG Power and Industrial Solutions Ltd.
            "COCHINSHIP.NS": 0.19,   # Cochin Shipyard Ltd.
            "MEESHO.NS": 0.13,       # Meesho Ltd.
            "APARINDS.NS": 0.08,     # Apar Industries Ltd.
        }
    },

    # Updated to HDFC Mutual Fund's Portfolio Statement
    # as on August 31, 2026 (equity holdings only; weights are "% to NAV").
    # Two "SKF India" line items in the statement (Industrial - 0.65% and
    # Auto Components - 0.34%) refer to the same listed company and are
    # combined into one SKFINDIA.NS holding (0.99%).
    "HDFC Mid Cap Fund": {
        "nav": 231.07,
        "holdings": {
            "FEDERALBNK.NS": 4.21,
            "AUBANK.NS": 3.98,
            "MFSL.NS": 3.79,
            "IPCALAB.NS": 3.30,
            "GLENMARK.NS": 3.07,
            "INDIANB.NS": 3.06,
            "BALKRISIND.NS": 3.02,
            "COFORGE.NS": 2.86,
            "FORTIS.NS": 2.69,
            "VMM.NS": 2.31,
            "MARICO.NS": 2.29,
            "M&MFIN.NS": 2.28,
            "AUROPHARMA.NS": 2.12,
            "HINDPETRO.NS": 2.05,
            "UNITDSPR.NS": 1.93,
            "CUMMINSIND.NS": 1.92,
            "PERSISTENT.NS": 1.78,
            "TATACOMM.NS": 1.77,
            "APOLLOTYRE.NS": 1.70,
            "POLICYBZR.NS": 1.69,
            "GLAND.NS": 1.62,
            "JINDALSTEL.NS": 1.62,
            "ALKEM.NS": 1.61,
            "MPHASIS.NS": 1.61,
            "UNIONBANK.NS": 1.57,
            "DABUR.NS": 1.47,
            "BOSCHLTD.NS": 1.44,
            "AIAENG.NS": 1.33,
            "DELHIVERY.NS": 1.33,
            "ETERNAL.NS": 1.30,
            "KARURVYSYA.NS": 1.26,
            "BHARATFORG.NS": 1.25,
            "INDUSINDBK.NS": 1.11,
            "COROMANDEL.NS": 1.08,
            "NAM-INDIA.NS": 1.08,
            "STARHEALTH.NS": 1.08,
            "INDHOTEL.NS": 0.96,
            "REDINGTON.NS": 0.91,
            "HAVELLS.NS": 0.90,
            "ICICIGI.NS": 0.87,
            "ASTERDM.NS": 0.84,
            "ESCORTS.NS": 0.82,
            "GODREJCP.NS": 0.82,
            "SUNDRMFAST.NS": 0.80,
            "HEXT.NS": 0.76,
            "SONACOMS.NS": 0.76,
            "CUB.NS": 0.71,
            "DIXON.NS": 0.71,
            "IGL.NS": 0.71,
            "SKFINDIA.NS": 0.99,
            "CROMPTON.NS": 0.63,
            "FLUOROCHEM.NS": 0.60,
            "TIMKEN.NS": 0.57,
            "ACC.NS": 0.56,
            "SUPREMEIND.NS": 0.54,
            "ARVIND.NS": 0.42,
            "OFSS.NS": 0.39,
            "AARTIIND.NS": 0.37,
            "PETRONET.NS": 0.36,
            "VTL.NS": 0.33,
            "CHOLAHLDNG.NS": 0.31,
            "KEC.NS": 0.31,
            "VESUVIUS.NS": 0.27,
            "CIEINDIA.NS": 0.26,
            "SYMPHONY.NS": 0.20,
            "BHARTIHEXA.NS": 0.19,
            "COLPAL.NS": 0.19,
            "FIVESTAR.NS": 0.19,
            "GROWW.NS": 0.18,
            "NAVNETEDUL.NS": 0.17,
            "LGEINDIA.NS": 0.16,
            "GREENLAM.NS": 0.15,
            "GREENPLY.NS": 0.15,
            "EMAMILTD.NS": 0.10,
            "DHANUKA.NS": 0.09,
            "KNRCON.NS": 0.05,
            "GREENPANEL.NS": 0.04,
            "JAGRAN.NS": 0.02,
        }
    },

    # Updated to Invesco Mutual Fund's Monthly Portfolio Statement
    # as on August 31, 2026 (equity holdings only; weights are "% to Net Assets").
    # Excludes TREPS/Reverse Repo and Net Receivables/(Payables) lines
    # (cash-equivalents, not equities).
    # "Manipal Health Enterprises Ltd" (4.74%) is omitted - it is an
    # unlisted company and has no resolvable NSE ticker.
    "Invesco India Midcap Fund": {
        "nav": 244.20,
        "holdings": {
            "PRESTIGE.NS": 7.27,     # Prestige Estates Projects Limited
            "MAXHEALTH.NS": 6.50,    # Max Healthcare Institute Limited
            "FEDERALBNK.NS": 5.98,   # The Federal Bank Limited
            "MEESHO.NS": 4.84,       # Meesho Ltd
            "MEDANTA.NS": 4.26,      # Global Health Limited
            "ETERNAL.NS": 4.20,      # Eternal Limited
            "AUBANK.NS": 4.05,       # AU Small Finance Bank Limited
            "LTF.NS": 3.97,          # L&T Finance Limited
            "INDUSINDBK.NS": 3.92,   # IndusInd Bank Limited
            "BSE.NS": 3.22,          # BSE Limited
            "SAILIFE.NS": 3.14,      # Sai Life Sciences Limited
            "MFSL.NS": 3.07,         # Max Financial Services Limited
            "INDIGO.NS": 3.03,       # InterGlobe Aviation Limited
            "GLENMARK.NS": 2.91,     # Glenmark Pharmaceuticals Limited
            "ABB.NS": 2.86,          # ABB India Limited
            "JKCEMENT.NS": 2.56,     # JK Cement Limited
            "SRF.NS": 2.27,          # SRF Limited
            "CPPLUS.NS": 2.27,       # Aditya Infotech Limited
            "NYKAA.NS": 2.21,        # FSN E-Commerce Ventures Limited
            "AMBER.NS": 1.96,        # Amber Enterprises India Limited
            "BHARATFORG.NS": 1.85,   # Bharat Forge Limited
            "TRENT.NS": 1.77,        # Trent Limited
            "TORNTPOWER.NS": 1.77,   # Torrent Power Limited
            "SWIGGY.NS": 1.48,       # Swiggy Limited
            "DIXON.NS": 1.45,        # Dixon Technologies (India) Limited
            "TIINDIA.NS": 1.42,      # Tube Investments Of India Limited
            "ICICIGI.NS": 1.31,      # ICICI Lombard General Insurance Company Limited
            "PHOENIXLTD.NS": 1.15,   # The Phoenix Mills Limited
            "CRAFTSMAN.NS": 1.02,    # Craftsman Automation Limited
            "ETHOSLTD.NS": 0.96,     # Ethos Ltd.
            "KIMS.NS": 0.92,         # Krishna Institute Of Medical Sciences Limited
            "CORONA.NS": 0.90,       # Corona Remedies Limited
            "DRAGARWQ.NS": 0.73,     # Dr Agarwals Health Care Limited
            "TIMKEN.NS": 0.54,       # Timken India Limited
            "BANSALWIRE.NS": 0.47,   # Bansal Wire Industries Limited
            "MAXESTATES.NS": 0.43,   # Max Estates Limited
            "WEWORK.NS": 0.37,       # Wework India Management Limited
            "VMM.NS": 0.18,          # Vishal Mega Mart Limited
            "CARBORUNIV.NS": 0.09,   # Carborundum Universal Limited
            "SONATSOFTW.NS": 0.07,   # Sonata Software Limited
        }
    },

    # Updated to Motilal Oswal Mutual Fund's Monthly Portfolio Statement
    # as on August 31, 2026 (equity holdings only; weights are "% to Net Assets").
    "Motilal Oswal Midcap Fund": {
        "nav": 120.28,
        "holdings": {
            "PAYTM.NS": 9.07,        # One 97 Communications Limited
            "KALYANKJIL.NS": 8.13,   # Kalyan Jewellers India Limited
            "ETERNAL.NS": 6.46,      # Eternal Limited
            "COFORGE.NS": 5.79,      # Coforge Limited
            "KEI.NS": 5.16,          # KEI Industries Limited
            "ABCAPITAL.NS": 4.87,    # Aditya Birla Capital Limited
            "PERSISTENT.NS": 4.41,   # Persistent Systems Ltd
            "SHRIRAMFIN.NS": 3.66,   # Shriram Finance Limited
            "DIXON.NS": 3.44,        # Dixon Technologies (India) Limited
            "GROWW.NS": 3.43,        # Billionbrains Garage Ventures Ltd (Groww)
            "MCX.NS": 3.43,          # Multi Commodity Exchange of India Limited
            "STLTECH.NS": 3.30,      # Sterlite Technologies Limited
            "POLICYBZR.NS": 2.85,    # PB Fintech Limited
            "TIINDIA.NS": 2.67,      # Tube Investments Of India Limited
            "LTF.NS": 2.40,          # L&T Finance Limited
            "ICICIAMC.NS": 2.39,     # ICICI Prudential Asset Management Company Limited
            "PRESTIGE.NS": 2.37,     # Prestige Estates Projects Limited
            "BHARTIHEXA.NS": 2.27,   # Bharti Hexacom Limited
            "LENSKART.NS": 2.26,     # Lenskart Solutions Limited
            "MOTHERSON.NS": 2.21,    # Samvardhana Motherson International Limited
            "SUZLON.NS": 2.16,       # Suzlon Energy Limited
            "IDFCFIRSTB.NS": 2.13,   # IDFC First Bank Limited
            "PREMIERENE.NS": 2.03,   # Premier Energies Limited
            "BEL.NS": 1.90,          # Bharat Electronics Limited
            "BSE.NS": 1.76,          # BSE Limited
            "INDIGO.NS": 1.73,       # InterGlobe Aviation Limited
            "WAAREEENER.NS": 1.48,   # Waaree Energies Limited
            "MAXHEALTH.NS": 1.29,    # Max Healthcare Institute Limited
            "ADANIENT.NS": 0.81,     # Adani Enterprises Limited
            "PWL.NS": 0.52,          # PhysicsWallah Limited
        }
    },

    # Updated to WhiteOak Capital Mutual Fund's Portfolio Statement
    # as on August 31, 2026 (equity holdings only; weight used is the
    # combined "% to Net Assets" column, i.e. cash equity + any stock
    # futures overlay in the same stock, per the fund's own stated
    # methodology). Bank Nifty and NIFTY index futures are excluded (not
    # single stocks). REITs (Nexus Select Trust, Embassy Office Parks
    # REIT) and InvITs (Vertis Infrastructure Trust) are excluded.
    # The following holdings are omitted because their NSE ticker could
    # not be confidently resolved (avoiding the risk of mapping to the
    # wrong listed company): Juniper Green Energy Ltd (0.59%), Tenneco
    # Clean Air India Ltd (0.36%), Aye Finance Ltd (0.25%), Horizon
    # Industrial Parks Ltd (0.24%), Omnitech Engineering Ltd (0.24%),
    # Yash Highvoltage Ltd (0.21%), Travel Food Services Ltd (0.19%),
    # Epack Prefab Technologies Ltd (0.12%), Onemi Technology Solutions
    # Ltd (0.09%), Indiqube Spaces Ltd (0.09%), Orkla India Ltd (0.08%),
    # EMA Partners India Ltd (0.04%).
    "WhiteOak Capital Midcap Fund": {
        "nav": 23.57,
        "holdings": {
            "MFSL.NS": 3.11,           # Max Financial Services Limited
            "COFORGE.NS": 2.95,        # Coforge Limited (2.91 cash + 0.04 future)
            "BHARTIHEXA.NS": 2.72,     # Bharti Hexacom Limited
            "FEDERALBNK.NS": 2.66,     # The Federal Bank Limited
            "POLICYBZR.NS": 2.63,      # PB Fintech Limited
            "LAURUSLABS.NS": 2.35,     # Laurus Labs Limited (2.02 cash + 0.33 future)
            "PERSISTENT.NS": 2.29,     # Persistent Systems Limited (1.02 cash + 1.27 future)
            "VMM.NS": 2.04,            # Vishal Mega Mart Limited (1.93 cash + 0.11 future)
            "PHOENIXLTD.NS": 1.93,     # The Phoenix Mills Limited
            "MOTILALOFS.NS": 1.91,     # Motilal Oswal Financial Services Limited
            "BHEL.NS": 1.89,           # Bharat Heavy Electricals Limited
            "FORTIS.NS": 1.87,         # Fortis Healthcare Limited
            "NAUKRI.NS": 1.82,         # Info Edge (India) Limited
            "LENSKART.NS": 1.61,       # Lenskart Solutions Limited
            "BERGEPAINT.NS": 1.53,     # Berger Paints (I) Limited
            "INDUSINDBK.NS": 1.53,     # IndusInd Bank Limited
            "MARICO.NS": 1.52,         # Marico Limited
            "360ONE.NS": 1.48,         # 360 One WAM Limited
            "SONACOMS.NS": 1.46,       # Sona BLW Precision Forgings Limited
            "IPCALAB.NS": 1.37,        # IPCA Laboratories Limited
            "KEI.NS": 1.37,            # KEI Industries Limited (0.03 cash + 1.34 future)
            "NATIONALUM.NS": 1.27,     # National Aluminium Company Limited
            "AIAENG.NS": 1.24,         # AIA Engineering Limited
            "NAM-INDIA.NS": 1.29,      # Nippon Life India AMC Limited (0.03 cash + 1.26 future)
            "MUTHOOTFIN.NS": 1.15,     # Muthoot Finance Limited
            "ALKEM.NS": 1.13,          # Alkem Laboratories Limited
            "AJANTPHARM.NS": 1.12,     # Ajanta Pharma Limited
            "MAXHEALTH.NS": 1.06,      # Max Healthcare Institute Limited
            "TIINDIA.NS": 1.08,        # Tube Investments of India Limited (1.01 cash + 0.07 future)
            "OIL.NS": 1.67,            # Oil India Limited (0.67 cash + 1.00 future)
            "NYKAA.NS": 0.96,          # FSN E-Commerce Ventures Limited
            "MCX.NS": 0.95,            # Multi Commodity Exchange of India Limited
            "JSL.NS": 0.90,            # Jindal Stainless Limited
            "JSWINFRA.NS": 0.90,       # JSW Infrastructure Ltd
            "GLAND.NS": 0.89,          # Gland Pharma Limited
            "BANDHANBNK.NS": 0.89,     # Bandhan Bank Limited
            "M&MFIN.NS": 0.87,         # Mahindra & Mahindra Financial Services Limited
            "AADHARHFC.NS": 0.84,      # Aadhar Housing Finance Limited
            "NAVINFLUOR.NS": 0.80,     # Navin Fluorine International Limited
            "MANKIND.NS": 0.80,        # Mankind Pharma Limited
            "POWERINDIA.NS": 0.79,     # Hitachi Energy India Limited
            "PAGEIND.NS": 0.79,        # Page Industries Limited
            "RECLTD.NS": 0.79,         # REC Limited
            "GVT&D.NS": 0.77,          # GE Vernova T&D India Limited
            "HEROMOTOCO.NS": 0.74,     # Hero MotoCorp Limited
            "ABBOTINDIA.NS": 0.72,     # Abbott India Limited
            "ATHERENERG.NS": 0.72,     # Ather Energy Limited (0.70 cash + 0.02 future)
            "GODREJPROP.NS": 0.69,     # Godrej Properties Limited
            "BANKINDIA.NS": 0.69,      # Bank of India
            "COROMANDEL.NS": 0.67,     # Coromandel International Limited
            "KRN.NS": 0.66,            # KRN Heat Exchanger And Refrigeration Limited
            "AZAD.NS": 0.65,           # Azad Engineering Ltd
            "PAYTM.NS": 0.62,          # One 97 Communications Limited
            "PETRONET.NS": 0.73,       # Petronet LNG Limited (0.62 cash + 0.11 future)
            "CUMMINSIND.NS": 0.58,     # Cummins India Limited
            "THELEELA.NS": 0.57,       # Leela Palaces Hotels & Resorts Limited
            "NH.NS": 0.56,             # Narayana Hrudayalaya Limited
            "HINDPETRO.NS": 0.56,      # Hindustan Petroleum Corporation Limited
            "FIVESTAR.NS": 0.52,       # Five Star Business Finance Limited
            "GROWW.NS": 0.52,          # Billionbrains Garage Ventures Ltd
            "COLPAL.NS": 0.51,         # Colgate Palmolive (India) Limited
            "GODREJIND.NS": 0.51,      # Godrej Industries Limited
            "CARERATING.NS": 0.51,     # CARE Ratings Limited
            "PNBHOUSING.NS": 0.50,     # PNB Housing Finance Limited
            "SAILIFE.NS": 0.48,        # Sai Life Sciences Limited
            "TDPOWERSYS.NS": 0.48,     # TD Power Systems Limited
            "INDIASHLTR.NS": 0.46,     # India Shelter Finance Corporation Limited
            "ABCAPITAL.NS": 0.45,      # Aditya Birla Capital Limited
            "NEULANDLAB.NS": 0.45,     # Neuland Laboratories Limited
            "NMDC.NS": 0.43,           # NMDC Limited
            "IIFL.NS": 0.42,           # IIFL Finance Limited
            "ACUTAAS.NS": 0.41,        # Acutaas Chemicals Limited
            "SUPREMEIND.NS": 0.40,     # Supreme Industries Limited
            "DYNAMATECH.NS": 0.40,     # Dynamatic Technologies Limited
            "CPPLUS.NS": 0.39,         # Aditya Infotech Limited
            "AJAXENGG.NS": 0.37,       # Ajax Engineering Limited
            "SHILPAMED.NS": 0.37,      # Shilpa Medicare Limited
            "POLYMED.NS": 0.37,        # Poly Medicure Limited
            "ABREL.NS": 0.36,          # Aditya Birla Real Estate Limited
            "SOUTHBANK.NS": 0.36,      # The South Indian Bank Limited
            "MANORAMA.NS": 0.36,       # Manorama Industries Limited
            "ENDURANCE.NS": 0.34,      # Endurance Technologies Limited
            "CARTRADE.NS": 0.32,       # Cartrade Tech Limited
            "ANTHEM.NS": 0.31,         # Anthem Biosciences Limited
            "JSWCEMENT.NS": 0.31,      # JSW Cement Limited
            "AVALON.NS": 0.30,         # Avalon Technologies Limited
            "TBOTEK.NS": 0.28,         # TBO Tek Limited
            "KIRLOSENG.NS": 0.27,      # Kirloskar Oil Engines Limited
            "EUREKAFORB.NS": 0.26,     # Eureka Forbes Ltd
            "ELGIEQUIP.NS": 0.25,      # Elgi Equipments Limited
            "REDINGTON.NS": 0.24,      # Redington Limited
            "IGIL.NS": 0.22,           # International Gemological Institute Limited
            "CHOLAHLDNG.NS": 0.22,     # Cholamandalam Financial Holdings Limited
            "REPCOHOME.NS": 0.21,      # Repco Home Finance Limited
            "DOMS.NS": 0.20,           # Doms Industries Limited
            "SOBHA.NS": 0.19,          # Sobha Limited
            "METROBRAND.NS": 0.19,     # Metro Brands Limited
            "GILLETTE.NS": 0.18,       # Gillette India Limited
            "AUBANK.NS": 0.17,         # AU Small Finance Bank Limited
            "LEMONTREE.NS": 0.15,      # Lemon Tree Hotels Limited
            "INTELLECT.NS": 0.15,      # Intellect Design Arena Limited
            "SAFARI.NS": 0.15,         # Safari Industries (India) Limited
            "ICICIGI.NS": 0.13,        # ICICI Lombard General Insurance Company Limited
            "UJJIVANSFB.NS": 0.13,     # Ujjivan Small Finance Bank Limited
            "3MINDIA.NS": 0.13,        # 3M India Limited
            "SAGILITY.NS": 0.12,       # Sagility Limited
            "KIMS.NS": 0.11,           # Krishna Institute Of Medical Sciences Limited
            "PRUDENT.NS": 0.11,        # Prudent Corporate Advisory Services Limited
            "AETHER.NS": 0.11,         # Aether Industries Limited
            "FINEORG.NS": 0.09,        # Fine Organic Industries Limited
            "BRIGADE.NS": 0.07,        # Brigade Enterprises Limited
            "NEWGEN.NS": 0.07,         # Newgen Software Technologies Limited
            "XPROINDIA.NS": 0.06,      # Xpro India Limited
            "ICICIPRULI.NS": 0.06,     # ICICI Prudential Life Insurance Company Limited
            "NSDL.BO": 0.06,           # National Securities Depository Limited
            "KARURVYSYA.NS": 0.05,     # Karur Vysya Bank Limited
            "AWFIS.NS": 0.05,          # Awfis Space Solutions Limited
            "BLUESTARCO.NS": 0.82,     # Blue Star Limited (0.02 cash + 0.80 future)
            "OFSS.NS": 1.33,           # Oracle Financial Services Software Limited (0.01 cash + 1.32 future)
        }
    }
}

# =========================
# FETCH LIVE DATA
# =========================
#
# WHY PRICES WERE STILL WRONG:
#
# The whole app was built on ONE batched yf.download(period="10d",
# interval="1d") call, then "previous_close = iloc[-2], live_price =
# iloc[-1]" off those DAILY bars. Daily bars are not a live quote --
# during market hours, .NS/.BO daily candles are frequently not
# updated intraday, so iloc[-1] can silently be an OLD close instead
# of the current traded price, and iloc[-2] shifts along with it. That
# is the exact bug already found and fixed in the sister Invesco and
# Motilal trackers: no true live-price source was ever being queried
# here, only end-of-day candles.
#
# FIX -- same 3-tier design proven on those trackers, generalised to
# ~150 tickers across 7 funds and to both .NS and .BO tickers:
#
#   Tier 1 (primary, .NS only):  NSE's own quote API -- previousClose
#                                and lastPrice straight from the
#                                exchange, authoritative, not derived.
#   Tier 2 (secondary, .NS + .BO): Yahoo's CHART API meta block
#                                (chartPreviousClose / regularMarket-
#                                Price) -- values Yahoo states
#                                directly. Deliberately NOT yfinance's
#                                fast_info, whose previousClose is
#                                derived client-side from grouped
#                                hourly bars and was the exact cause of
#                                wrong previous-closes on the sister
#                                Invesco tracker (e.g. FEDERALBNK
#                                334.50 shown vs. the real 332.75).
#   Tier 3 (last resort):       batched daily + intraday candle
#                                history, with the "is the last daily
#                                bar today's in-progress session"
#                                question answered by comparing
#                                yfinance's OWN daily-bar date against
#                                yfinance's OWN intraday-bar date (same
#                                source/normalisation), never against a
#                                separately-computed Python-clock date.
#
# All three tiers are fetched CONCURRENTLY across every ticker, each
# bounded by its own hard timeout, and the quote lookup used by the
# per-fund loop below does ZERO network I/O -- it only reads a
# pre-built quote_map. A ticker with no fresh/trustworthy data this
# cycle falls back to its last known good quote in st.session_state,
# same as before.

NSE_REQUEST_TIMEOUT = 5     # per-request timeout, seconds
NSE_BATCH_TIMEOUT = 35      # hard ceiling for ALL NSE requests combined (~150 tickers)
YF_BATCH_TIMEOUT = 30       # hard ceiling for each batched Yahoo call
STALE_DATA_MAX_DAYS = 4     # Tier-3 candle data older than this is treated as a failed fetch

if "last_good_quotes" not in st.session_state:
    # {ticker: (previous_close, latest_close, as_of_date, source)}
    st.session_state["last_good_quotes"] = {}

if "nse_session" not in st.session_state:
    st.session_state["nse_session"] = None

all_tickers = []
for fund in funds.values():
    all_tickers.extend(list(fund["holdings"].keys()))
all_tickers = sorted(set(all_tickers))

# NSE's quote API only serves NSE (.NS) listings, so only that subset
# is eligible for Tier 1. .BO-only tickers (GUJGASLTD, NSDL) go
# straight to Tier 2, which handles both exchanges fine.
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
    """Single-symbol NSE fetch. Called from a thread pool, never
    directly from the main loop. `symbol` has no .NS suffix."""
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
    """PRIMARY source (.NS only). Fetches all eligible symbols
    concurrently, bounded by ONE overall timeout."""
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
    """TIER 2 -- Yahoo's chart-API meta block. `ticker` includes its
    .NS/.BO suffix, matching what's used everywhere else.

    Deliberately NOT yfinance's fast_info: fast_info.previousClose is
    derived client-side from grouped hourly bars and was proven to
    return the wrong session's close for NSE tickers (see FEDERALBNK
    on the Invesco tracker: showed 334.50, real value 332.75). The
    chart endpoint's `meta.chartPreviousClose` and
    `meta.regularMarketPrice` are values Yahoo computes and states
    directly, with no client-side reconciliation."""
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
            # Market closed / field absent -> last non-null 1-minute
            # close from the SAME payload (no cross-source mixing).
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
    """TIER 2 (secondary) source, used when NSE fails or for .BO
    tickers NSE can't serve at all. Fetches all tickers concurrently,
    bounded by ONE overall timeout."""
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
    """Runs a yf.download() call in a worker thread with a hard
    timeout, since yfinance itself sets none."""
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
    """TIER 3 (last-resort) previous-close source: ONE batched,
    threaded call for ALL tickers' recent daily bars."""
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
    """TIER 3 live-price source: ONE batched, threaded call for ALL
    tickers' 1-minute intraday bars."""
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
    """Tier-3 previous close, derived the same day-matched way as the
    fixed Motilal/Invesco trackers: compare the daily batch's OWN last
    bar date against the intraday batch's OWN last bar date (same
    source/normalisation), rather than against a separately-computed
    Python-clock date, since those two can silently disagree."""
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
        # Last daily row is today's in-progress session -> drop it.
        if len(daily_hist) >= 2:
            return float(daily_hist.iloc[-2])
        return None

    return float(daily_hist.iloc[-1])


def get_live_price_from_intraday(ticker, intraday_batch, daily_batch, n_tickers):
    """Tier-3 live price = most recent 1-minute close. Falls back to
    the daily batch's last close if intraday data is unavailable (e.g.
    market closed)."""
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

# --- Fetch all three tiers ONCE, up front, each bounded by its own
# --- hard timeout. Building quote_map below does NO network I/O.

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
        st.session_state["last_good_quotes"][ticker] = (
            prev_close, live_price, today_india_date, source
        )
    else:
        cached = st.session_state["last_good_quotes"].get(ticker)
        if cached is not None:
            # cached may be a 3-tuple from an older session (pre-source
            # tracking); normalise to 4-tuple defensively.
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
