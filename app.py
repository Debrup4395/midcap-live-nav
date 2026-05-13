import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Live Midcap NAV Tracker",
    layout="wide"
)

# AUTO REFRESH EVERY 5 MINUTES
st_autorefresh(interval=300000, key="refresh")

# -----------------------------
# FUND DATA
# -----------------------------

funds = {

    "HSBC Midcap Fund": {
        "nav": 482.33,
        "holdings": {
            "BSE.NS": 5.13,
            "POWERINDIA.NS": 4.72,
            "NYKAA.NS": 4.85,
            "FEDERALBNK.NS": 3.86,
            "PIRAMAL.NS": 3.51,
            "POLICYBZR.NS": 3.43,
            "BEL.NS": 3.01,
            "INDIANB.NS": 2.66,
            "BHEL.NS": 2.63,
            "POLYCAB.NS": 2.60,
            "LUPIN.NS": 2.12,
            "RADICO.NS": 2.03,
            "MCX.NS": 1.96,
            "NAM-INDIA.NS": 1.90,
            "OIL.NS": 1.45,
            "BHARATFORG.NS": 1.32,
            "ONGC.NS": 1.31,
            "JSWENERGY.NS": 1.06,
            "TATASTEEL.NS": 0.90,
            "SHRIRAMFIN.NS": 0.83,
            "DATAPATTNS.NS": 0.81,
            "KEI.NS": 0.77,
            "THERMAX.NS": 0.74,
            "BHARTIHEXA.NS": 0.74,
            "ABCAPITAL.NS": 0.74,
            "HINDALCO.NS": 0.72,
            "APLAPOLLO.NS": 0.65,
            "JSWSTEEL.NS": 0.60,
            "ECLERX.NS": 0.29,
            "RBLBANK.NS": 0.10
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
            "SRF.NS": 1.38,
            "JSL.NS": 1.38,
            "KEI.NS": 1.37,
            "MAXFIN.NS": 1.37,
            "POLICYBZR.NS": 1.36
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
            "POLICYBZR.NS": 1.45
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
            "SWIGGY.NS": 2.47,
            "ICICIGI.NS": 2.28,
            "NYKAA.NS": 2.26,
            "TORNTPOWER.NS": 2.02
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
            "TVSMOTOR.NS": 2.08
        }
    },

    "ICICI Prudential Midcap Fund": {
        "nav": 370.22,
        "holdings": {
            "MCX.NS": 4.88,
            "BSE.NS": 4.87,
            "JSL.NS": 4.51,
            "APARINDS.NS": 4.30,
            "MUTHOOTFIN.NS": 3.74,
            "APLAPOLLO.NS": 3.59,
            "JINDALSTEL.NS": 3.15,
            "HINDPETRO.NS": 3.14,
            "POLICYBZR.NS": 3.11,
            "UPL.NS": 2.94,
            "BHARATFORG.NS": 2.93,
            "KEI.NS": 2.69,
            "PRESTIGE.NS": 2.65,
            "NAM-INDIA.NS": 2.20,
            "CUMMINSIND.NS": 2.07,
            "POWERINDIA.NS": 2.05,
            "KPRMILL.NS": 1.90,
            "ESCORTS.NS": 1.82,
            "GODREJPROP.NS": 1.80,
            "NAVINFLUOR.NS": 1.72
        }
    }
}

# -----------------------------
# FETCH STOCK DATA
# -----------------------------

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
    st.error(f"Error fetching market data: {e}")
    st.stop()

# -----------------------------
# TITLE
# -----------------------------

st.title("📈 Live Midcap Fund NAV Tracker")

current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
st.write(f"Last Updated: {current_time}")

# -----------------------------
# NAV CALCULATION
# -----------------------------

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
