import time
import sys
from pathlib import Path

import streamlit as st

# Project root ko Python path mein add karna
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.matching_engine import MatchingEngine


st.set_page_config(
    page_title="ChronosMatch | Trading Terminal",
    page_icon="📈",
    layout="wide",
)


# Trading Terminal Styling
st.markdown("""
<style>
.stApp {
    background: #080d14;
    color: #e6edf3;
}

[data-testid="stHeader"] {
    background: #080d14;
}

[data-testid="stSidebar"] {
    background: #0d141e;
    border-right: 1px solid #202c3a;
}

.block-container {
    padding-top: 1.5rem;
    max-width: 1500px;
}

h1, h2, h3 {
    color: #f0f4f8;
    font-weight: 650;
}

[data-testid="stMetric"] {
    background: #111c28;
    border: 1px solid #263747;
    padding: 18px;
    border-radius: 10px;
}

[data-testid="stMetricLabel"] {
    color: #91a2b5;
}

[data-testid="stMetricValue"] {
    color: #00d69a;
    font-weight: 700;
}

[data-testid="stDataFrame"] {
    border: 1px solid #263747;
    border-radius: 10px;
}

[data-testid="stForm"] {
    background: #111c28;
    border: 1px solid #263747;
    padding: 20px;
    border-radius: 12px;
}

.stButton button,
.stFormSubmitButton button {
    background: #00a878;
    color: white;
    border: none;
    border-radius: 7px;
    font-weight: 650;
    min-height: 42px;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background: #00c18a;
    color: white;
}

[data-baseweb="input"],
[data-baseweb="select"] {
    background: #0d141e;
}

hr {
    border-color: #263747;
}

</style>
""", unsafe_allow_html=True)




# Engine ko session mein rakhna taaki UI refresh par data rahe
if "engine" not in st.session_state:
    st.session_state.engine = MatchingEngine()
    st.session_state.next_order_id = 1

engine = st.session_state.engine


with st.sidebar:
    st.markdown("# ⚡ ChronosMatch")
    st.caption("LOW-LATENCY TRADING")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Order Book",
            "Trade History",
            "Performance",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### System Status")
    st.success("Engine Initialized")
    st.caption("Development Build")


if page == "Order Book":
    st.title("📚 Order Book")
    st.caption("Active buy and sell orders")

    buy_tab, sell_tab = st.tabs(["BUY ORDERS", "SELL ORDERS"])

    with buy_tab:
        if engine.buy_orders:
            st.dataframe([
                {
                    "Order ID": order.order_id,
                    "Price": order.price,
                    "Quantity": order.quantity,
                }
                for order in engine.buy_orders
            ], use_container_width=True, hide_index=True)
        else:
            st.info("No active buy orders.")

    with sell_tab:
        if engine.sell_orders:
            st.dataframe([
                {
                    "Order ID": order.order_id,
                    "Price": order.price,
                    "Quantity": order.quantity,
                }
                for order in engine.sell_orders
            ], use_container_width=True, hide_index=True)
        else:
            st.info("No active sell orders.")

    st.stop()
if page == "Trade History":
    st.title("🧾 Trade History")
    st.caption("Record of executed trades")

    if engine.trade_history:
        st.dataframe(
            [
                {
                    "Buy Order": trade.buy_order_id,
                    "Sell Order": trade.sell_order_id,
                    "Price": trade.price,
                    "Quantity": trade.quantity,
                }
                for trade in reversed(engine.trade_history)
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No trades executed yet.")

    st.stop()


if page == "Performance":
    st.title("⚡ Performance")
    st.caption("Order processing measurements")

    latencies = [
        item["Latency (ms)"]
        for item in st.session_state.get("latency_history", [])
    ]

    if latencies:
        col1, col2, col3 = st.columns(3)
        col1.metric("Measured Orders", len(latencies))
        col2.metric(
            "Average Processing Time",
            f"{sum(latencies) / len(latencies):.4f} ms",
        )
        col3.metric("Maximum Processing Time", f"{max(latencies):.4f} ms")

        st.line_chart(latencies)
    else:
        st.info("Place orders on the Dashboard to collect measurements.")

    st.stop()    

# Header
st.title("📈 ChronosMatch")
st.caption("LOW-LATENCY ORDER MATCHING • TRADING TERMINAL")
st.divider()


# Top metrics
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "BEST BID",
    f"{engine.get_best_bid():.2f}"
    if engine.get_best_bid() is not None else "—",
)

c2.metric(
    "BEST ASK",
    f"{engine.get_best_ask():.2f}"
    if engine.get_best_ask() is not None else "—",
)

c3.metric(
    "SPREAD",
    f"{engine.get_spread():.2f}"
    if engine.get_spread() is not None else "—",
)

c4.metric("EXECUTED TRADES", len(engine.trade_history))

c5, = st.columns(1)

last_latency = st.session_state.get("last_latency_ms")

c5.metric(
    "LAST ORDER LATENCY",
    f"{last_latency:.4f} ms"
    if last_latency is not None else "—",
)
st.divider()


# Main layout
left, right = st.columns([1, 1.6], gap="large")


with left:
    st.subheader("⚡ Place Order")

    with st.form("order_form", clear_on_submit=True):
        side = st.radio(
            "Order Side",
            ["BUY", "SELL"],
            horizontal=True,
        )

        price = st.number_input(
            "Price",
            min_value=0.01,
            value=100.0,
            step=1.0,
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            step=1,
        )

        submitted = st.form_submit_button("PLACE ORDER")

        if submitted:
            order_id = st.session_state.next_order_id

            try:
               start_time = time.perf_counter()

               engine.add_order(
                               order_id,
                               side,
                               price,
                               quantity,
                            )

               latency_ms = (time.perf_counter() - start_time) * 1000

               st.session_state.next_order_id += 1
               st.session_state.last_latency_ms = latency_ms
               if "latency_history" not in st.session_state:
                   st.session_state.latency_history = []

               st.session_state.latency_history.append({
                        "Order": order_id,
                        "Latency (ms)": latency_ms,
})

               st.success(
                  f"{side} order #{order_id} submitted! "
                  f"Processing time: {latency_ms:.4f} ms"
                )
               st.rerun()

            except ValueError as error:
                st.error(str(error))


with right:
    st.subheader("📚 Order Book")

    buy_tab, sell_tab = st.tabs(["🟢 BUY ORDERS", "🔴 SELL ORDERS"])

    with buy_tab:
        if engine.buy_orders:
            st.dataframe(
                [
                    {
                        "Order ID": order.order_id,
                        "Price": order.price,
                        "Quantity": order.quantity,
                    }
                    for order in engine.buy_orders
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No active buy orders.")

    with sell_tab:
        if engine.sell_orders:
            st.dataframe(
                [
                    {
                        "Order ID": order.order_id,
                        "Price": order.price,
                        "Quantity": order.quantity,
                    }
                    for order in engine.sell_orders
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No active sell orders.")


st.divider()
st.subheader("🧾 Trade History")

if engine.trade_history:
    st.dataframe(
        [
            {
                "Buy Order": trade.buy_order_id,
                "Sell Order": trade.sell_order_id,
                "Price": trade.price,
                "Quantity": trade.quantity,
            }
            for trade in reversed(engine.trade_history)
        ],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No trades yet. Place a matching BUY and SELL order to see trades here.")

st.caption("ChronosMatch • Development build")
st.divider()
st.subheader("⚡ Latency Monitoring")

latency_history = st.session_state.get("latency_history", [])

if latency_history:
    latency_data = latency_history[-50:]

    st.line_chart(
        {
            str(item["Order"]): item["Latency (ms)"]
            for item in latency_data
        }
    )

    latencies = [
        item["Latency (ms)"]
        for item in latency_history
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric("Measured Orders", len(latencies))
    col2.metric("Average Latency", f"{sum(latencies) / len(latencies):.4f} ms")
    col3.metric("Maximum Latency", f"{max(latencies):.4f} ms")
else:
    st.info("Place some orders to start collecting latency measurements.")