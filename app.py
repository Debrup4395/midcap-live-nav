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

    "HSBC Midcap Fund": {
        "nav": 530.65,
        "holdings": {
        "NYKAA.NS": 4.67,
        "FEDERALBNK.NS": 4.21,
        "GVT&D.NS": 3.99,
        "LENSKART.NS": 3.84,
        "POLICYBZR.NS": 3.76,
        "PIRAMALFIN.NS": 3.66,
        "CPPLUS.NS": 3.54,
        "GROWW.NS": 3.28,
        "BHARATFORG.NS": 3.19,
        "MEESHO.NS": 2.87,
        "THERMAX.NS": 2.78,
        "APARINDS.NS": 2.55,
        "POWERINDIA.NS": 2.53,
        "MANKIND.NS": 2.47,
        "NAM-INDIA.NS": 2.39,
        "RADICO.NS": 2.29,
        "NETWEB.NS": 2.06,
        "JSWENERGY.NS": 2.06,
        "LUPIN.NS": 1.94,
        "INDIANB.NS": 1.93,
        "AUBANK.NS": 1.90,
        "M&MFIN.NS": 1.82,
        "ICICIAMC.NS": 1.77,
        "ATHERENERG.NS": 1.73,
        "IPCALAB.NS": 1.69,
        "CUB.NS": 1.67,
        "MCX.NS": 1.63,
        "ABCAPITAL.NS": 1.63,
        "DATAPATTNS.NS": 1.62,
        "GODFRYPHLP.NS": 1.57,
        "THYROCARE.NS": 1.56,
        "TDPOWERSYS.NS": 1.45,
        "BHEL.NS": 1.42,
        "SYNGENE.NS": 1.39,
        "COCHINSHIP.NS": 1.25,
        "POLYCAB.NS": 1.22,
        "KEI.NS": 1.19,
        "NAVINFLUOR.NS": 1.12,
        "ATLANTAELE.NS": 1.07,
        "AVALON.NS": 1.04,
        "BSE.NS": 0.96,
        "KIRLOSENG.NS": 0.96,
        "POLYMED.NS": 0.85,
        "TRITURBINE.NS": 0.67,
        "JINDALSTEL.NS": 0.59,
        "NTPCGREEN.NS": 0.53,
        "JSWSTEEL.NS": 0.51,
        "NATIONALUM.NS": 0.48,
        "TVSMOTOR.NS": 0.48,
        "SCHAEFFLER.NS": 0.41,
        "SAFARI.NS": 0.40,
        "CREDITACC.NS": 0.37,
        "KAYNES.NS": 0.33,
        "CGPOWER.NS": 0.33,
        "ACMESOLAR.NS": 0.33,
        "ANTHEM.NS": 0.32,
        "BHARTIHEXA.NS": 0.10,
        "HINDALCO.NS": 0.09,
        "BOSCHLTD.NS": 0.07,
        "OIL.NS": 0.07,
        "TATASTEEL.NS": 0.05,
        "CRISIL.NS": 0.04,
        "COFORGE.NS": 0.04,
        "IDFCFIRSTB.NS": 0.04,
        "MFSL.NS": 0.03,
        "MUTHOOTFIN.NS": 0.03,
        "MAZDOCK.NS": 0.03,
        "JKCEMENT.NS": 0.02,
        "DIXON.NS": 0.02,
        "SWIGGY.NS": 0.02,
        "HINDPETRO.NS": 0.01,
        "PERSISTENT.NS": 0.01,
        "SUNDARMFIN.NS": 0.01,
        "MAXHEALTH.NS": 0.01,
        "BIOCON.NS": 0.01,
        "APLAPOLLO.NS": 0.01
        }
    },
           "ICICI Midcap Fund": {
        "nav": 387.83,
        "holdings": {
        "APARINDS.NS": 5.48,
        "BSE.NS": 4.99,
        "MCX.NS": 4.48,
        "JINDALSTEL.NS": 3.77,
        "HINDPETRO.NS": 3.66,
        "APLAPOLLO.NS": 3.28,
        "BHARATFORG.NS": 3.21,
        "MUTHOOTFIN.NS": 3.15,
        "KEI.NS": 3.02,
        "POLICYBZR.NS": 2.92,
        "PRESTIGE.NS": 2.83,
        "JSL.NS": 2.74,
        "UPL.NS": 2.52,
        "NAM-INDIA.NS": 2.44,
        "KPRMILL.NS": 2.30,
        "GVT&D.NS": 2.26,
        "CUMMINSIND.NS": 2.15,
        "POWERINDIA.NS": 2.06,
        "VAML.NS": 1.93,
        "NAVINFLUOR.NS": 1.87,
        "SRF.NS": 1.78,
        "GODREJPROP.NS": 1.76,
        "UNOMINDA.NS": 1.61,
        "ESCORTS.NS": 1.59,
        "360ONE.NS": 1.55,
        "SCHAEFFLER.NS": 1.52,
        "SONACOMS.NS": 1.43,
        "BHARTIHEXA.NS": 1.42,
        "INDUSINDBK.NS": 1.35,
        "POLYCAB.NS": 1.22,
        "MOTHERSON.NS": 1.22,
        "VEDL.NS": 1.21,
        "DIXON.NS": 1.10,
        "SUPREMEIND.NS": 1.03,
        "OBEROIRLTY.NS": 1.02,
        "VOLTAS.NS": 0.96,
        "FLUOROCHEM.NS": 0.90,
        "LENSKART.NS": 0.89,
        "NATIONALUM.NS": 0.89,
        "GRINDWELL.NS": 0.83,
        "SAIL.NS": 0.76,
        "ASTRAL.NS": 0.72,
        "BLUESTARCO.NS": 0.72,
        "COROMANDEL.NS": 0.70,
        "AMBUJACEM.NS": 0.65,
        "DEEPAKNTR.NS": 0.63,
        "BEML.NS": 0.62,
        "JYOTICNC.NS": 0.53,
        "PIIND.NS": 0.50,
        "CROMPTON.NS": 0.47,
        "BANDHANBNK.NS": 0.46,
        "IRCTC.NS": 0.43,
        "AARTIIND.NS": 0.41,
        "SBICARD.NS": 0.39,
        "IRB.NS": 0.38,
        "ATUL.NS": 0.34,
        "ENDURANCE.NS": 0.34,
        "PPLPHARMA.NS": 0.23,
        "SYNGENE.NS": 0.23,
        "KIMS.NS": 0.21,
        "RATNAMANI.NS": 0.20,
        "THERMAX.NS": 0.19,
        "VEDPOWER.NS": 0.17,
        "HONAUT.NS": 0.17,
        "VISL.NS": 0.15,
        "CARBORUNIV.NS": 0.14,
        "INDIGO.NS": 0.14,
        "BALKRISIND.NS": 0.13,
        "JKCEMENT.NS": 0.10,
        "RAINBOW.NS": 0.09,
        "HINDZINC.NS": 0.09,
        "ASTRAZEN.NS": 0.07,
        "CHEMPLASTS.NS": 0.05,
        "ACC.NS": 0.04,
        "KAJARIACER.NS": 0.03,
        "ASTRAMICRO.NS": 0.02,
        "ASTEC.NS": 0.02,
        "GUJENERGY.NS": 0.01,
        "CAMLINFINE.NS": 0.01,
        "CRISIL.NS": 0.0,
        }
    },

    "Edelweiss Mid Cap Fund": {
        "nav": 129.55,
        "holdings": {
            "FEDERALBNK.NS": 3.87,
            "BSE.NS": 2.61,
            "FORTIS.NS": 2.25,
            "MARICO.NS": 2.22,
            "SOLARINDS.NS": 2.15,
            "MCX.NS": 2.14,
            "BHEL.NS": 1.88,
            "IDFCFIRSTB.NS": 1.78,
            "CUB.NS": 1.78,
            "IPCALAB.NS": 1.76,
            "CREDITACC.NS": 1.71,
            "RADICO.NS": 1.68,
            "LTF.NS": 1.67,
            "BHARATFORG.NS": 1.64,
            "AUBANK.NS": 1.60,
            "COFORGE.NS": 1.60,
            "INDIANB.NS": 1.54,
            "JSWENERGY.NS": 1.53,
            "MAXHEALTH.NS": 1.52,
            "NMDC.NS": 1.48,
            "CUMMINSIND.NS": 1.47,
            "GVT&D.NS": 1.43,
            "KEI.NS": 1.42,
            "UNOMINDA.NS": 1.39,
            "HDFCAMC.NS": 1.34,
            "APLAPOLLO.NS": 1.33,
            "INDUSTOWER.NS": 1.33,
            "MFSL.NS": 1.31,
            "KARURVYSYA.NS": 1.30,
            "ASHOKLEY.NS": 1.29,
            "TORNTPOWER.NS": 1.29,
            "HINDPETRO.NS": 1.25,
            "PERSISTENT.NS": 1.24,
            "POLICYBZR.NS": 1.23,
            "POLYCAB.NS": 1.20,
            "PHOENIXLTD.NS": 1.20,
            "JKCEMENT.NS": 1.19,
            "JSL.NS": 1.19,
            "LUPIN.NS": 1.14,
            "PAGEIND.NS": 1.14,
            "AJANTPHARM.NS": 1.12,
            "SUNDARMFIN.NS": 1.12,
            "INDHOTEL.NS": 1.05,
            "VMM.NS": 1.04,
            "SRF.NS": 1.03,
            "BEL.NS": 1.00,
            "CHOLAFIN.NS": 0.99,
            "MANKIND.NS": 0.99,
            "IDEA.NS": 0.97,
            "ENDURANCE.NS": 0.94,
            "LGEINDIA.NS": 0.90,
            "JUBLFOOD.NS": 0.88,
            "PRESTIGE.NS": 0.86,
            "SAIL.NS": 0.86,
            "GROWW.NS": 0.81,
            "TVSMOTOR.NS": 0.80,
            "BALKRISIND.NS": 0.78,
            "ICICIAMC.NS": 0.75,
            "POWERINDIA.NS": 0.75,
            "JBCHEPHARM.NS": 0.74,
            "SUMICHEM.NS": 0.73,
            "SCHAEFFLER.NS": 0.71,
            "DIXON.NS": 0.69,
            "ATHERENERG.NS": 0.68,
            "THERMAX.NS": 0.67,
            "CGPOWER.NS": 0.65,
            "BLUESTARCO.NS": 0.64,
            "BIKAJI.NS": 0.63,
            "CRAFTSMAN.NS": 0.58,
            "LAURUSLABS.NS": 0.56,
            "TRITURBINE.NS": 0.55,
            "BHARTIHEXA.NS": 0.55,
            "COROMANDEL.NS": 0.53,
            "BDL.NS": 0.47,
            "NYKAA.NS": 0.46,
            "ELECON.NS": 0.45,
            "360ONE.NS": 0.44,
            "BERGEPAINT.NS": 0.40,
            "OIL.NS": 0.39,
            "FSL.NS": 0.34,
            "SUPREMEIND.NS": 0.33,
            "NETWEB.NS": 0.31,
            "PNBHOUSING.NS": 0.30,
            "SWIGGY.NS": 0.30,
            "NAVINFLUOR.NS": 0.29,
            "ASTRAL.NS": 0.29,
            "ITCHOTELS.NS": 0.27,
            "OBEROIRLTY.NS": 0.24,
            "MUTHOOTFIN.NS": 0.18,
            "MRF.NS": 0.07,
            "CEATLTD.NS": 0.0,
            "DEEPAKNTR.NS": 0.0,
        }
    },

    "HDFC Mid Cap Fund": {
        "nav": 235.90,
        "holdings": {
            "FEDERALBNK.NS": 4.18,
            "MFSL.NS": 4.10,
            "AUBANK.NS": 4.08,
            "BALKRISIND.NS": 3.10,
            "FORTIS.NS": 3.07,
            "IPCALAB.NS": 3.05,
            "INDIANB.NS": 2.98,
            "GLENMARK.NS": 2.93,
            "VMM.NS": 2.64,
            "CUMMINSIND.NS": 2.52,
            "MARICO.NS": 2.51,
            "COFORGE.NS": 2.27,
            "HINDPETRO.NS": 2.27,
            "TATACOMM.NS": 2.18,
            "AUROPHARMA.NS": 2.09,
            "M&MFIN.NS": 2.07,
            "APOLLOTYRE.NS": 1.79,
            "ALKEM.NS": 1.75,
            "AIAENG.NS": 1.68,
            "UNITDSPR.NS": 1.60,
            "DABUR.NS": 1.56,
            "GLAND.NS": 1.56,
            "JINDALSTEL.NS": 1.55,
            "UNIONBANK.NS": 1.54,
            "POLICYBZR.NS": 1.53,
            "DELHIVERY.NS": 1.48,
            "MPHASIS.NS": 1.46,
            "PERSISTENT.NS": 1.44,
            "BHARATFORG.NS": 1.37,
            "BOSCHLTD.NS": 1.24,
            "STARHEALTH.NS": 1.20,
            "KARURVYSYA.NS": 1.17,
            "NAM-INDIA.NS": 1.14,
            "COROMANDEL.NS": 1.06,
            "ETERNAL.NS": 1.05,
            "INDHOTEL.NS": 1.00,
            "INDUSINDBK.NS": 0.99,
            "ESCORTS.NS": 0.84,
            "IGL.NS": 0.84,
            "GODREJCP.NS": 0.83,
            "CROMPTON.NS": 0.78,
            "REDINGTON.NS": 0.78,
            "HEXT.NS": 0.76,
            "TIMKEN.NS": 0.76,
            "CUB.NS": 0.69,
            "SKFINDUS.NS": 0.67,
            "SUNDRMFAST.NS": 0.67,
            "ACC.NS": 0.62,
            "SONACOMS.NS": 0.62,
            "DIXON.NS": 0.61,
            "FLUOROCHEM.NS": 0.54,
            "SUPREMEIND.NS": 0.52,
            "ARVIND.NS": 0.47,
            "KEC.NS": 0.47,
            "ICICIGI.NS": 0.45,
            "VTL.NS": 0.39,
            "SKFINDIA.NS": 0.39,
            "ASTERDM.NS": 0.39,
            "CHOLAHLDNG.NS": 0.37,
            "OFSS.NS": 0.36,
            "AARTIIND.NS": 0.35,
            "VESUVIUS.NS": 0.33,
            "EMAMILTD.NS": 0.30,
            "SYMPHONY.NS": 0.25,
            "NAVNETEDUL.NS": 0.22,
            "GROWW.NS": 0.20,
            "BHARTIHEXA.NS": 0.20,
            "FIVESTAR.NS": 0.19,
            "GREENLAM.NS": 0.16,
            "GREENPLY.NS": 0.16,
            "COLPAL.NS": 0.16,
            "LGEINDIA.NS": 0.15,
            "KNRCON.NS": 0.14,
            "DHANUKA.NS": 0.11,
            "GREENPANEL.NS": 0.08,
            "JAGRAN.NS": 0.04,
        }
    },

    "Invesco India Midcap Fund": {
        "nav": 243.34,
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
            "CPPLUS.NS": 2.37,
            "SWIGGY.NS": 2.24,
            "NYKAA.NS": 2.13,
            "TORNTPOWER.NS": 1.93,
            "ICICIGI.NS": 1.92,
            "CHOLAHLDNG.NS": 1.45,
            "DIXON.NS": 1.44,
            "APARINDS.NS": 1.42,
            "PHOENIXLTD.NS": 1.38,
            "KIMS.NS": 1.19,
            "CRAFTSMAN.NS": 1.06,
            "ETHOSLTD.NS": 1.01,
            "CORONA.NS": 0.95,
            "DRAGARWQ.NS": 0.88,
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
        "nav": 118.06,
        "holdings": {
            "PAYTM.NS": 7.34,
            "KALYANKJIL.NS": 6.34,
            "COFORGE.NS": 6.04,
            "ETERNAL.NS": 5.96,
            "KEI.NS": 5.61,
            "ABCAPITAL.NS": 5.49,
            "PERSISTENT.NS": 4.59,
            "GROWW.NS": 4.56,
            "SHRIRAMFIN.NS": 3.78,
            "BSE.NS": 3.61,
            "MCX.NS": 3.48,
            "TIINDIA.NS": 3.44,
            "DIXON.NS": 3.26,
            "PRESTIGE.NS": 3.10,
            "BHARTIHEXA.NS": 2.97,
            "MAXHEALTH.NS": 2.80,
            "LTF.NS": 2.77,
            "SUZLON.NS": 2.47,
            "POLICYBZR.NS": 2.35,
            "ICICIAMC.NS": 2.25,
            "IDFCFIRSTB.NS": 2.25,
            "BEL.NS": 2.21,
            "MOTHERSON.NS": 2.20,
            "PREMIERENE.NS": 2.19,
            "WAAREEENER.NS": 1.91,
            "INDIGO.NS": 1.68,
            "AUBANK.NS": 0.99,
            "STLTECH.NS": 0.91,
            "PWL.NS": 0.57,
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
