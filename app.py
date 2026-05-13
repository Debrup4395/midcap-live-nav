import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Live Midcap NAV Tracker",
    layout="wide"
)

st_autorefresh(interval=300000, key="refresh")

# =========================
# FUND DATA
# =========================

funds = {

    "HSBC Midcap Fund": {
        "nav": 482.33,
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

    "Edelweiss Mid Cap Fund": {
        "nav": 121.39,
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
        "nav": 216.62,
        "holdings": {
            "MAXFIN.NS": 4.37,
            "AUBANK.NS": 4.24,
            "FEDERALBNK.NS": 3.87,
            "GLENMARK.NS": 3.41,
            "INDIANB.NS": 3.31,
            "BALKRISIND.NS": 3.25,
            "FORTIS.NS": 3.16,
            "IPCALAB.NS": 2.92,
            "CUMMINSIND.NS": 2.50,
            "MARICO.NS": 2.48,
            "HINDPETRO.NS": 2.20,
            "M_MFIN.NS": 2.05,
            "COFORGE.NS": 1.97,
            "AUROPHARMA.NS": 1.96,
            "TATACOMM.NS": 1.86,
            "PERSISTENT.NS": 1.70,
            "DABUR.NS": 1.65,
            "MPHASIS.NS": 1.62,
            "DELHIVERY.NS": 1.55,
            "POLICYBZR.NS": 1.45,
            "BHARATFORG.NS": 1.28,
            "KARURVYSYA.NS": 1.23,
            "STARHEALTH.NS": 1.14,
            "NAM-INDIA.NS": 1.06,
            "INDUSINDBK.NS": 1.04,
            "ESCORTS.NS": 0.98,
            "INDHOTEL.NS": 0.95,
            "IGL.NS": 0.90,
            "GODREJCP.NS": 0.84,
            "CROMPTON.NS": 0.83,
            "TIMKEN.NS": 0.80,
            "CUB.NS": 0.73,
            "ACC.NS": 0.71,
            "REDINGTON.NS": 0.71,
            "SONACOMS.NS": 0.65,
            "SUPREMEIND.NS": 0.63,
            "DIXON.NS": 0.61
        }
    },

    "Invesco India Midcap Fund": {
        "nav": 218.21,
        "holdings": {
            "PRESTIGE.NS": 6.19,
            "BSE.NS": 5.88,
            "FEDERALBNK.NS": 5.44,
            "AUBANK.NS": 5.13,
            "ZOMATO.NS": 4.49,
            "MAXHEALTH.NS": 4.42,
            "GLOBALHEALTH.NS": 4.35,
            "INDIGO.NS": 4.14,
            "INDUSINDBK.NS": 4.02,
            "LTF.NS": 4.01,
            "GLENMARK.NS": 3.81,
            "MAXFIN.NS": 3.58,
            "JKCEMENT.NS": 3.50,
            "AMBER.NS": 2.79,
            "TRENT.NS": 2.70,
            "SRF.NS": 2.58,
            "ICICIGI.NS": 2.28,
            "NYKAA.NS": 2.26,
            "TORNTPOWER.NS": 2.02,
            "ABB.NS": 1.75,
            "DIXON.NS": 1.47,
            "PHOENIXLTD.NS": 1.45,
            "APARINDS.NS": 1.41
        }
    },

    "Motilal Oswal Midcap Fund": {
        "nav": 103.52,
        "holdings": {
            "ONE97.NS": 7.29,
            "KALYANKJIL.NS": 7.09,
            "ZOMATO.NS": 5.83,
            "COFORGE.NS": 5.58,
            "KEI.NS": 5.48,
            "PERSISTENT.NS": 5.41,
            "ABCAPITAL.NS": 5.17,
            "BHARTIARTL.NS": 5.01,
            "MCX.NS": 4.33,
            "BSE.NS": 3.83,
            "DIXON.NS": 3.54,
            "TIINDIA.NS": 3.51,
            "BHARTIHEXA.NS": 3.18,
            "SHRIRAMFIN.NS": 3.03,
            "PRESTIGE.NS": 2.91,
            "BEL.NS": 2.63,
            "LTF.NS": 2.61,
            "MAXHEALTH.NS": 2.23,
            "POLICYBZR.NS": 2.20,
            "TVSMOTOR.NS": 2.08,
            "HDFCAMC.NS": 1.96,
            "IDFCFIRSTB.NS": 1.47,
            "AXISBANK.NS": 1.24,
            "WAAREEENER.NS": 1.04,
            "AUBANK.NS": 1.01
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
        period="2d",
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

current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
st.write(f"Last Updated: {current_time}")

# =========================
# NAV CALCULATION
# =========================

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

st.markdown("---")

st.caption(
    "Live NAV estimation based on weighted portfolio stock movement."
)
