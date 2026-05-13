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
            "NYKAA.NS": 4.85,
            "POWERINDIA.NS": 4.72,
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
            "RBLBANK.NS": 0.10,
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
            "PERSISTENT.NS": 0.02
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
            "POLICYBZR.NS": 1.36,
            "ASHOKLEY.NS": 1.35,
            "IPCALAB.NS": 1.32,
            "MAXHEALTH.NS": 1.31,
            "SUNDARMFIN.NS": 1.22,
            "PHOENIXLTD.NS": 1.14,
            "MUTHOOTFIN.NS": 1.11,
            "KARURVYSYA.NS": 1.09,
            "BEL.NS": 1.09,
            "JUBLFOOD.NS": 1.09,
            "JSWENERGY.NS": 1.02,
            "POLYCAB.NS": 1.02,
            "SAIL.NS": 1.02,
            "CANBK.NS": 0.98,
            "OIL.NS": 0.90,
            "BALKRISIND.NS": 0.83,
            "HINDPETRO.NS": 0.82,
            "PRESTIGE.NS": 0.82,
            "NAVINFLUOR.NS": 0.81,
            "VODAFONEIDEA.NS": 0.77,
            "BLUESTARCO.NS": 0.76,
            "INDHOTEL.NS": 0.75,
            "SCHAEFFLER.NS": 0.73,
            "DIXON.NS": 0.69,
            "TVSMOTOR.NS": 0.69,
            "MANKIND.NS": 0.65,
            "BHARTIHEXA.NS": 0.60,
            "CGPOWER.NS": 0.60,
            "BDL.NS": 0.49,
            "TRITURBINE.NS": 0.48,
            "360ONE.NS": 0.44,
            "NATIONALUM.NS": 0.43,
            "SUPREMEIND.NS": 0.43,
            "DABUR.NS": 0.39,
            "SWIGGY.NS": 0.38,
            "ASTRAL.NS": 0.37
        }
    },

    "Motilal Oswal Midcap Fund": {
        "nav": 103.52,
        "holdings": {
            "PAYTM.NS": 7.29,
            "KALYANKJIL.NS": 7.09,
            "ETERNAL.NS": 5.83,
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
            "IDFCFIRSTB.NS": 1.47,
            "AXISBANK.NS": 1.24,
            "AUBANK.NS": 1.01
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
st.markdown("### Real-Time Expected NAV Estimation")

current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
st.write(f"Last Updated: {current_time}")

# -----------------------------
# NAV CALCULATION
# -----------------------------

for fund_name, fund_data in funds.items():

    previous_nav = fund_data["nav"]
    holdings = fund_data["holdings"]

    weighted_return = 0
    stock_rows = []

    for ticker, weight in holdings.items():

        try:
            stock_data = data[ticker]

            latest_close = stock_data["Close"].iloc[-1]
            previous_close = stock_data["Close"].iloc[-2]

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

        top_positive = df.sort_values(
            by="Contribution",
            ascending=False
        ).head(5)

        top_negative = df.sort_values(
            by="Contribution",
            ascending=True
        ).head(5)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### Top Positive Contributors")
            st.dataframe(
                top_positive,
                use_container_width=True
            )

        with c2:
            st.markdown("#### Top Negative Contributors")
            st.dataframe(
                top_negative,
                use_container_width=True
            )

        st.markdown("#### Full Portfolio Movement")

        st.dataframe(
            df.sort_values(
                by="Contribution",
                ascending=False
            ),
            use_container_width=True,
            height=400
        )

st.markdown("---")

st.caption(
    "Live NAV estimation based on weighted portfolio stock movement."
)
