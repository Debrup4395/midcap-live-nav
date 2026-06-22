import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Live Midcap NAV Tracker",
    layout="wide"
)

st_autorefresh(interval=10000, key="refresh")

# =========================
# FUND DATA
# =========================

funds = {

    "HSBC Midcap Fund": {
        "nav": 526.49,
        "holdings": {
        "BSE.NS": 5.13,
        "GVT&D.NS": 4.94,
        "NYKAA.NS": 4.85,
        "POWERINDIA.NS": 4.72,
        "GROWW.NS": 3.88,
        "FEDERALBNK.NS": 3.86,
        "PIRAMAL.NS": 3.51,
        "POLICYBZR.NS": 3.43,
        "LENSKART.NS": 3.23,
        "BEL.NS": 3.01,
        "CPPLUS.NS": 2.99,
        "INDIANB.NS": 2.66,
        "BHEL.NS": 2.63,
        "POLYCAB.NS": 2.60,
        "ICICIAMC.NS": 2.22,
        "LUPIN.NS": 2.12,
        "RADICO.NS": 2.03,
        "MCX.NS": 1.96,
        "NAM-INDIA.NS": 1.90,
        "NETWEB.NS": 1.87,
        "GODFRYPHLP.NS": 1.86,
        "CUB.NS": 1.86,
        "APARINDS.NS": 1.85,
        "KIRLOSENG.NS": 1.69,
        "TDPOWERSYS.NS": 1.61,
        "OIL.NS": 1.45,
        "NTPCGREEN.NS": 1.45,
        "BHARATFORG.NS": 1.32,
        "ONGC.NS": 1.31,
        "THYROCARE.NS": 1.31,
        "IPCALAB.NS": 1.12,
        "NATIONALUM.NS": 1.06,
        "JSWENERGY.NS": 1.06,
        "ATHERENERG.NS": 1.45,
        "ATLANTAELE.NS": 0.98,
        "KAYNES.NS": 0.98,
        "MANKIND.NS": 0.95,
        "TATASTEEL.NS": 0.90,
        "SAFARI.NS": 0.85,
        "SHRIRAMFIN.NS": 0.83,
        "DATAPATTNS.NS": 0.81,
        "KEI.NS": 0.77,
        "THERMAX.NS": 0.74,
        "BHARTIHEXA.NS": 0.74,
        "ABCAPITAL.NS": 0.74,
        "HINDALCO.NS": 0.72,
        "AVALON.NS": 0.70,
        "ANTHEM.NS": 0.67,
        "APLAPOLLO.NS": 0.65,
        "JSWSTEEL.NS": 0.60,
        "SCHAEFFLER.NS": 0.47,
        "SYNGENE.NS": 0.46,
        "JINDALSTEL.NS": 0.46,
        "ECLERX.NS": 0.29,
        "GABRIEL.NS": 0.14,
        "RBLBANK.NS": 0.10,
        "BOSCHLTD.NS": 0.09,
        "CRISIL.NS": 0.05,
        "CUMMINSIND.NS": 0.05,
        "MUTHOOTFIN.NS": 0.04,
        "MAXFIN.NS": 0.04,
        "IDFCFIRSTB.NS": 0.04,
        "COFORGE.NS": 0.04,
        "MAZDOCK.NS": 0.03,
        "JKCEMENT.NS": 0.03,
        "KPITTECH.NS": 0.03,
        "DIXON.NS": 0.02,
        "SWIGGY.NS": 0.02,
        "INDHOTEL.NS": 0.02,
        "GLOBALHEALTH.NS": 0.02,
        "PERSISTENT.NS": 0.02,
        "SUNDARMFIN.NS": 0.01,
        "MSUMI.NS": 0.01,
        "DIVISLAB.NS": 0.01,
        "INDIGO.NS": 0.01,
        "MAXHEALTH.NS": 0.01,
        "CGPOWER.NS": 0.01,
        "BIOCON.NS": 0.01,
        "ASHOKLEY.NS": 0.01
        }
    },
           "ICICI Midcap Fund": {
        "nav": 388.22,
        "holdings": {
        "MCX.NS": 4.70,
        "BSE.NS": 5.39,
        "JINDALSTEL.NS": 4.32,
        "APARINDS.NS": 4.61,
        "MUTHOOTFIN.NS": 3.54,
        "APLAPOLLO.NS": 3.38,
        "JSL.NS": 2.73,
        "HINDPETRO.NS": 3.68,
        "POLICYBZR.NS": 3.08,
        "UPL.NS": 2.87,
        "BHARATFORG.NS": 2.95,
        "KEI.NS": 2.96,
        "PRESTIGE.NS": 2.49,
        "NAM-INDIA.NS": 2.32,
        "GVT&D.NS": 2.37,
        "CUMMINSIND.NS": 2.25,
        "POWERINDIA.NS": 2.05,
        "KPRMILL.NS": 1.90,
        "ESCORTS.NS": 1.82,
        "GODREJPROP.NS": 1.68,
        "NAVINFLUOR.NS": 1.75,
        "SRF.NS": 1.78,
        "SCHAEFFLER.NS": 1.55,
        "360ONE.NS": 1.61,
        "BHARTIHEXA.NS": 1.51,
        "SONACOMS.NS": 1.45,
        "INDUSINDBK.NS": 1.39,
        "SUPREMEIND.NS": 1.23,
        "VEDL.NS": 1.22,
        "NAUKRI.NS": 1.13,
        "VOLTAS.NS": 1.12,
        "DIXON.NS": 1.05,
        "MOTHERSON.NS": 1.03,
        "POLYCAB.NS": 1.03,
        "OBEROIRLTY.NS": 1.00,
        "ASTRAL.NS": 0.86,
        "BLUESTARCO.NS": 0.82,
        "NATIONALUM.NS": 0.74,
        "DEEPAKNTR.NS": 0.73,
        "SAIL.NS": 0.72,
        "COROMANDEL.NS": 0.72,
        "AMBUJACEM.NS": 0.72,
        "LENSKART.NS": 0.68,
        "UNOMINDA.NS": 0.68,
        "BEML.NS": 0.66,
        "GRINDWELL.NS": 0.63,
        "PIIND.NS": 0.62,
        "SUNDRMFAST.NS": 0.54,
        "JYOTICNC.NS": 0.54,
        "CROMPTON.NS": 0.49,
        "IRCTC.NS": 0.48,
        "AARTIIND.NS": 0.47,
        "BANDHANBNK.NS": 0.46,
        "SBICARD.NS": 0.44,
        "IRB.NS": 0.40,
        "FLUOROCHEM.NS": 0.37,
        "ATUL.NS": 0.37,
        "ACC.NS": 0.26,
        "SYNGENE.NS": 0.26,
        "PPLPHARMA.NS": 0.23,
        "RATNAMANI.NS": 0.21,
        "ENDURANCE.NS": 0.18,
        "KIMS.NS": 0.18,
        "THERMAX.NS": 0.16,
        "HONAUT.NS": 0.14,
        "CARBORUNIV.NS": 0.11,
        "TORNTPOWER.NS": 0.11,
        "INDIGO.NS": 0.11,
        "JKCEMENT.NS": 0.10,
        "HINDZINC.NS": 0.10,
        "RAINBOW.NS": 0.08,
        "ASTRAZEN.NS": 0.07,
        "CHEMPLASTS.NS": 0.06,
        "VTL.NS": 0.05,
        "KAJARIACER.NS": 0.03,
        "JSWENERGY.NS": 0.02,
        "GUJGASLTD.NS": 0.02,
        "ASTEC.NS": 0.02,
        "ASTRAMICRO.NS": 0.02,
        "CAMLINFINE.NS": 0.01,
        "CRISIL.NS": 0.01,
        }
    },

    "Edelweiss Mid Cap Fund": {
        "nav": 126.67,
        "holdings": {
            "MCX.NS": 3.15,
            "FEDERALBNK.NS": 2.88,
            "BSE.NS": 2.65,
            "AUBANK.NS": 2.22,
            "MARICO.NS": 2.15,
            "FORTIS.NS": 2.08,
            "SOLARINDS.NS": 1.86,
            "BHEL.NS": 1.73,
            "INDIANB.NS": 1.73,
            "TORNTPOWER.NS": 1.73,
            "IDFCFIRSTB.NS": 1.68,
            "NMDC.NS": 1.65,
            "APLAPOLLO.NS": 1.58,
            "JKCEMENT.NS": 1.54,
            "RADICO.NS": 1.53,
            "PERSISTENT.NS": 1.53,
            "LTF.NS": 1.52,
            "BHARATFORG.NS": 1.51,
            "UNOMINDA.NS": 1.49,
            "CUB.NS": 1.49,
            "CUMMINSIND.NS": 1.48,
            "COFORGE.NS": 1.46,
            "INDUSTOWER.NS": 1.45,
            "LUPIN.NS": 1.45,
            "HDFCAMC.NS": 1.43,
            "GVT&D.NS": 1.40,
            "SRF.NS": 1.38,
            "JSL.NS": 1.38,
            "KEI.NS": 1.37,
            "MAXFIN.NS": 1.37,
            "POLICYBZR.NS": 1.36,
            "ASHOKLEY.NS": 1.35,
            "IPCALAB.NS": 1.32,
            "MAXHEALTH.NS": 1.31,
            "CREDITACC.NS": 1.23,
            "SUNDARMFIN.NS": 1.22,
            "PHOENIXLTD.NS": 1.14,
            "VMM.NS": 1.13,
            "MUTHOOTFIN.NS": 1.11,
            "KARURVYSYA.NS": 1.09,
            "BEL.NS": 1.09,
            "JUBLFOOD.NS": 1.09,
            "PAGEIND.NS": 1.09,
            "GROWW.NS": 1.08,
            "JSWENERGY.NS": 1.02,
            "POLYCAB.NS": 1.02,
            "SAIL.NS": 1.02,
            "CANBK.NS": 0.98,
            "LGEINDIA.NS": 0.97,
            "OIL.NS": 0.90,
            "ENDURANCE.NS": 0.86,
            "BALKRISIND.NS": 0.83,
            "HINDPETRO.NS": 0.82,
            "PRESTIGE.NS": 0.82,
            "NAVINFLUOR.NS": 0.81,
            "VODAFONEIDEA.NS": 0.77,
            "BLUESTARCO.NS": 0.76,
            "INDHOTEL.NS": 0.75,
            "SCHAEFFLER.NS": 0.73,
            "AJANTAPHARM.NS": 0.70,
            "DIXON.NS": 0.69,
            "TVSMOTOR.NS": 0.69,
            "BIKAJI.NS": 0.72,
            "MANKIND.NS": 0.65,
            "ATHERENERG.NS": 0.62,
            "CHOLAFIN.NS": 0.60,
            "BHARTIHEXA.NS": 0.61,
            "ICICIAMC.NS": 0.60,
            "CGPOWER.NS": 0.60,
            "SUMICHEM.NS": 0.53,
            "CRAFTSMAN.NS": 0.50,
            "BDL.NS": 0.49,
            "TRITURBINE.NS": 0.48,
            "M_MFIN.NS": 0.47,
            "360ONE.NS": 0.44,
            "NATIONALUM.NS": 0.43,
            "SUPREMEIND.NS": 0.43,
            "DABUR.NS": 0.39,
            "ASTRAL.NS": 0.37,
            "FSL.NS": 0.35,
            "ITCHOTELS.NS": 0.26,
            "OBEROIRLTY.NS": 0.24,
            "CEATLTD.NS": 0.24,
            "HEROMOTOCO.NS": 0.15,
            "KFINTECH.NS": 0.01,
        }
    },
   
    "HDFC Mid Cap Fund": {
        "nav": 226.50,
        "holdings": {
            "MFSL.NS": 4.49,
            "AUBANK.NS": 4.01,
            "FEDERALBNK.NS": 3.79,
            "GLENMARK.NS": 3.13,  
            "INDIANB.NS": 3.15,
            "BALKRISIND.NS": 3.25,
            "FORTIS.NS": 3.09,
            "IPCALAB.NS": 2.83,
            "VMM.NS": 2.83,
            "CUMMINSIND.NS": 2.72,
            "MARICO.NS": 2.55,
            "HINDPETRO.NS": 2.25,
            "M&MFIN.NS": 1.99,
            "COFORGE.NS": 2.28,
            "AUROPHARMA.NS": 1.96,
            "JINDALSTEL.NS": 1.82,
            "TATACOMM.NS": 2.25,
            "APOLLOTYRE.NS": 1.70,
            "ALKEM.NS": 1.79,
            "PERSISTENT.NS": 1.79,
            "UNIONBANK.NS": 1.70,
            "DABUR.NS": 1.68,
            "MPHASIS.NS": 1.62,
            "DELHIVERY.NS": 1.55,
            "UNITDSPR.NS": 1.53,
            "POLICYBZR.NS": 1.59,
            "BOSCHLTD.NS": 1.41,
            "AIAENG.NS": 1.39,
            "BHARATFORG.NS": 1.28,
            "KARURVYSYA.NS": 1.23,
            "GLAND.NS": 1.17,
            "STARHEALTH.NS": 1.14,
            "NAM-INDIA.NS": 1.06,
            "ETERNAL.NS": 1.04,
            "INDUSINDBK.NS": 1.04,
            "COROMANDEL.NS": 1.03,
            "ESCORTS.NS": 0.98,
            "INDHOTEL.NS": 0.95,
            "IGL.NS": 0.90,
            "GODREJCP.NS": 0.84,
            "CROMPTON.NS": 0.83,
            "TIMKEN.NS": 0.80,
            "CUB.NS": 0.73,
            "ACC.NS": 0.71,
            "REDINGTON.NS": 0.71,
            "HEXT.NS": 0.70,
            "SONACOMS.NS": 0.65,
            "SUNDRMFAST.NS": 0.64,
            "SUPREMEIND.NS": 0.63,
            "DIXON.NS": 0.61,
            "SKFINDUS.NS": 0.55,
            "FLUOROCHEM.NS": 0.53,
            "KEC.NS": 0.53,
            "SKFINDIA.NS": 0.43,
            "AARTIIND.NS": 0.41,
            "VTL.NS": 0.40,
            "VESUVIUS.NS": 0.40,
            "CHOLAHLDNG.NS": 0.37,
            "EMAMILTD.NS": 0.35,
            "OFSS.NS": 0.35,
            "ARVIND.NS": 0.34,
            "SYMPHONY.NS": 0.33,
            "CEATLTD.NS": 0.29,
            "ASTERDM.NS": 0.27,
            "ICICIGI.NS": 0.24,
            "NAVNETEDUL.NS": 0.24,
            "GROWW.NS": 0.23,
            "GREENLAM.NS": 0.23,
            "BHARTIHEXA.NS": 0.22,
            "FIVESTAR.NS": 0.20,
            "COLPAL.NS": 0.18,
            "LGEINDIA.NS": 0.17,
            "GREENPLY.NS": 0.15,
            "KNRCON.NS": 0.14,
            "DHANUKA.NS": 0.12,
            "GREENPANEL.NS": 0.10,
            "JAGRAN.NS": 0.04,
        }
    },

    "Invesco India Midcap Fund": {
        "nav": 234.86,
        "holdings": {
            "BSE.NS": 6.05,
            "PRESTIGE.NS": 5.85,
            "FEDERALBNK.NS": 5.20,
            "AUBANK.NS": 4.72,
            "ETERNAL.NS": 4.48,
            "MEDANTA.NS": 4.39,
            "INDIGO.NS": 4.22,
            "MAXHEALTH.NS": 4.08,
            "LTF.NS": 3.90,
            "INDUSINDBK.NS": 3.81,
            "MFSL.NS": 3.59,
            "GLENMARK.NS": 3.42,
            "JKCEMENT.NS": 3.25,
            "SAILIFE.NS": 3.20,
            "SRF.NS": 3.09,
            "TRENT.NS": 2.61,
            "AMBER.NS": 2.51,
            "ABB.NS": 2.49,
            "HEXT.NS": 2.37,
            "ADITYAINFO.NS": 2.37,
            "SWIGGY.NS": 2.24,
            "NYKAA.NS": 2.13,
            "TORNTPOWER.NS": 1.93,
            "ICICIGI.NS": 1.92,
            "CHOLAHLDNG.NS": 1.45,
            "DIXON.NS": 1.44,
            "APARINDS.NS": 1.42,
            "PHOENIXLTD.NS": 1.38,
            "KIMS.NS": 1.19,
            "CRAFSMAN.NS": 1.06,
            "ETHOSLTD.NS": 1.01,
            "CORONA.NS": 0.95,
            "DRAGARWAL.NS": 0.88,
            "TIMKEN.NS": 0.80,
            "BANSALWIRE.NS": 0.60,
            "CARBORUNIV.NS": 0.51,
            "MAXESTATES.NS": 0.48,
            "WEWORK.NS": 0.42,
            "SOBHA.NS": 0.42,
            "SONATSOFTW.NS": 0.32,
            "VMM.NS": 0.26,
            "TIINDIA.NS": 0.17,
        }
    },

    "Motilal Oswal Midcap Fund": {
        "nav": 109.03,
        "holdings": {
            "PAYTM.NS": 7.29,
            "COFORGE.NS": 6.12,
            "KALYANKJIL.NS": 5.98,
            "KEI.NS": 5.82,
            "ETERNAL.NS": 5.80,
            "PERSISTENT.NS": 5.74,
            "ABCAPITAL.NS": 5.23,
            "GROWW.NS": 4.29,
            "MCX.NS": 4.22,
            "BSE.NS": 3.98,
            "TIINDIA.NS": 3.66,
            "DIXON.NS": 3.58,
            "SHRIRAMFIN.NS": 3.24,
            "BHARTIHEXA.NS": 3.08,
            "PRESTIGE.NS": 2.81,
            "LTF.NS": 2.63,
            "POLICYBZR.NS": 2.52,
            "ICICIAMC.NS": 2.48,
            "MAXHEALTH.NS": 2.46,
            "BEL.NS": 2.26,
            "PREMIERENE.NS": 2.13,
            "SUZLON.NS": 2.01,
            "WAAREEENER.NS": 1.98,
            "MOTHERSON.NS": 1.63,
            "IDFCFIRSTB.NS": 1.47,
            "AUBANK.NS": 0.96

        }
    }
}

# =========================
# FETCH DATA
# =========================

all_tickers = []

for fund in funds.values():
    all_tickers.extend(list(fund["holdings"].keys()))

all_tickers = list(set(all_tickers))

@st.cache_data(ttl=300)
def fetch_data(tickers):

    data = yf.download(
        tickers=tickers,
        period="5d",
        interval="1d",
        auto_adjust=True,
        progress=False,
        group_by="ticker",
        threads=True
    )

    return data

try:
    data = fetch_data(all_tickers)

except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

# =========================
# TITLE
# =========================

st.title("📈 Live Midcap Fund NAV Tracker")

from datetime import datetime
import pytz

india = pytz.timezone("Asia/Kolkata")

current_time = datetime.now(india).strftime("%d-%m-%Y %I:%M:%S %p")

st.write(f"Last Updated: {current_time}")
# =========================
# NAV CALCULATION
# =========================
fund_performance = []
for fund_name, fund_data in funds.items():

    previous_nav = fund_data["nav"]
    holdings = fund_data["holdings"]

    weighted_return = 0.0
    stock_rows = []

    for ticker, weight in holdings.items():

        try:

            stock_data = data[ticker]

            latest_close = float(
                stock_data["Close"].iloc[-1]
            )

            previous_close = float(
                stock_data["Close"].iloc[-2]
            )

            if previous_close == 0:
                continue

            change_percent = (
                (latest_close - previous_close)
                / previous_close
            ) * 100

            if pd.isna(change_percent):
                continue

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

        except:
            continue
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
    df = pd.DataFrame(stock_rows)

    if not df.empty:

        df = df.sort_values(
            by="Weight %",
            ascending=False
        )

        st.dataframe(
            df,
            use_container_width=True,
            height=400
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
