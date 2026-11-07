
import time
import sys
from pathlib import Path

import streamlit as st

# Project root
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.matching_engine import MatchingEngine


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ChronosMatch | Trading Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: #080e18;
    color: #e6edf3;
}

[data-testid="stHeader"] {
    background: #080e18;
}

[data-testid="stSidebar"] {
    background: #0d1725;
    border-right: 1px solid #243247;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #f1f5f9;
}

p {
    color: #a7b5c8;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #121f30, #101a29);
    border: 1px solid #26384e;
    border-radius: 12px;
    padding: 18px;
}

[data-testid="stMetricLabel"] {
    color: #9aacc2;
}

[data-testid="stMetricValue"] {
    color: #00d69a;
    font-weight: 700;
}

[data-testid="stDataFrame"] {
    border: 1px solid #26384e;
    border-radius: 10px;
}

[data-testid="stForm"] {
    background: #111d2c;
    border: 1px solid #26384e;
    border-radius: 14px;
    padding: 22px;
}

.stButton button,
.stFormSubmitButton button {
    background: #00a878;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    min-height: 42px;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background: #00c18a;
    color: white;
    border: none;
}

div[data-baseweb="input"] {
    background: #0d1725;
}

hr {
    border-color: #26384e;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "engine" not in st.session_state:
    st.session_state.engine = MatchingEngine()

if "next_order_id" not in st.session_state:
    st.session_state.next_order_id = 1

if "latency_history" not in st.session_state:
    st.session_state.latency_history = []

engine = st.session_state.engine


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def get_order_data(orders):
    return [
        {
            "Order ID": order.order_id,
            "Price": order.price,
            "Quantity": order.quantity,
        }
        for order in orders
    ]


def get_trade_data():
    return [
        {
            "Buy Order": trade.buy_order_id,
            "Sell Order": trade.sell_order_id,
            "Price": trade.price,
            "Quantity": trade.quantity,
        }
        for trade in reversed(engine.trade_history)
    ]


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div style="padding:15px 0 25px 0;">
        <h2 style="color:#00d69a; margin-bottom:0;">
            ⚡ ChronosMatch
        </h2>
        <p style="font-size:11px; letter-spacing:2px;">
            TRADING TERMINAL
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### MAIN MENU")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Place Order",
            "Order Book",
            "Trade History",
            "Analytics",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("##### SYSTEM STATUS")

    st.markdown("""
    <div style="
        background:#142638;
        padding:14px;
        border-radius:10px;
        border:1px solid #28445a;
    ">
        <span style="color:#00d69a;">●</span>
        <b style="color:white;"> Engine Online</b>
        <p style="font-size:11px; margin:8px 0 0 0;">
            Matching engine initialized
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.caption("CHRONOSMATCH")
    st.caption("Development Build")


# --------------------------------------------------
# COMMON HEADER
# --------------------------------------------------

st.markdown("""
<div style="
    background:linear-gradient(110deg,#13243a,#153449,#102b30);
    border:1px solid #29465b;
    border-radius:16px;
    padding:24px 28px;
    margin-bottom:24px;
">
    <div style="display:flex; justify-content:space-between;
                align-items:center; flex-wrap:wrap; gap:15px;">
        <div>
            <p style="color:#00d69a; font-size:11px;
                      letter-spacing:3px; font-weight:bold;">
                SMART ORDER MATCHING PLATFORM
            </p>
            <h1 style="color:white; margin:5px 0;">
                ChronosMatch
            </h1>
            <p style="margin:0;">
                Fast. Reliable. Intelligent Trading.
            </p>
        </div>

        <span style="font-size:55px; padding-right:15px;">
            📈
        </span>
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.subheader("Market Overview")
    st.caption("Your trading activity at a glance")

    best_bid = engine.get_best_bid()
    best_ask = engine.get_best_ask()
    spread = engine.get_spread()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "BEST BID",
        f"{best_bid:.2f}" if best_bid is not None else "—",
    )

    col2.metric(
        "BEST ASK",
        f"{best_ask:.2f}" if best_ask is not None else "—",
    )

    col3.metric(
        "SPREAD",
        f"{spread:.2f}" if spread is not None else "—",
    )

    col4.metric(
        "EXECUTED TRADES",
        len(engine.trade_history),
    )

    st.divider()

    # Chart and quick market information

    left, right = st.columns([2, 1])

    with left:

        st.subheader("📊 Execution Price Chart")
        st.caption("Based on actual executed trades")

        if engine.trade_history:

            prices = [
                trade.price
                for trade in engine.trade_history
            ]

            st.line_chart(
                prices,
                height=300,
            )

        else:
            st.info(
                "No executed trades yet. "
                "Place matching BUY and SELL orders to see the chart."
            )

    with right:

        st.subheader("Market Snapshot")

        st.metric(
            "Active Buy Orders",
            len(engine.buy_orders),
        )

        st.metric(
            "Active Sell Orders",
            len(engine.sell_orders),
        )

        st.metric(
            "Total Executed Trades",
            len(engine.trade_history),
        )

        last_latency = st.session_state.get("last_latency_ms")

        st.metric(
            "Last Order Latency",
            f"{last_latency:.4f} ms"
            if last_latency is not None else "—",
        )

    st.divider()

    # Order book preview

    st.subheader("📚 Market Depth")

    buy_col, sell_col = st.columns(2)

    with buy_col:

        st.markdown("🟢 **BUY ORDERS**")

        if engine.buy_orders:

            st.dataframe(
                get_order_data(engine.buy_orders),
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.info("No active buy orders.")

    with sell_col:

        st.markdown("🔴 **SELL ORDERS**")

        if engine.sell_orders:

            st.dataframe(
                get_order_data(engine.sell_orders),
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.info("No active sell orders.")

    st.divider()

    # Recent trades

    st.subheader("🧾 Recent Trades")

    if engine.trade_history:

        st.dataframe(
            get_trade_data()[:5],
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.info("No trades executed yet.")


# --------------------------------------------------
# PLACE ORDER
# --------------------------------------------------

elif page == "Place Order":

    st.subheader("⚡ Place a New Order")
    st.caption("Submit a BUY or SELL order to the matching engine")

    left, right = st.columns([1.3, 1])

    with left:

        with st.form("order_form", clear_on_submit=True):

            st.markdown("### Order Details")

            side = st.radio(
                "Select Order Type",
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

            submitted = st.form_submit_button(
                "PLACE ORDER",
                use_container_width=True,
            )

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

                    latency_ms = (
                        time.perf_counter() - start_time
                    ) * 1000

                    st.session_state.next_order_id += 1

                    st.session_state.last_latency_ms = latency_ms

                    st.session_state.latency_history.append({
                        "Order": order_id,
                        "Latency (ms)": latency_ms,
                    })

                    st.success(
                        f"{side} order #{order_id} submitted successfully!"
                    )

                    st.info(
                        f"Processing time: {latency_ms:.4f} ms"
                    )

                except ValueError as error:

                    st.error(str(error))

    with right:

        st.markdown("""
        <div style="
            background:linear-gradient(145deg,#14283a,#102b2b);
            border:1px solid #29465b;
            border-radius:14px;
            padding:22px;
        ">
            <h3 style="color:white;">Trading Guide</h3>
            <p>🟢 <b>BUY</b> — Place an order to buy.</p>
            <p>🔴 <b>SELL</b> — Place an order to sell.</p>
            <hr>
            <p style="font-size:13px;">
                Orders are automatically processed by the
                ChronosMatch matching engine.
            </p>
            <p style="font-size:13px;">
                Matching happens when BUY and SELL prices cross.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Current Market")

        st.metric(
            "Best Bid",
            f"{engine.get_best_bid():.2f}"
            if engine.get_best_bid() is not None else "—",
        )

        st.metric(
            "Best Ask",
            f"{engine.get_best_ask():.2f}"
            if engine.get_best_ask() is not None else "—",
        )


# --------------------------------------------------
# ORDER BOOK
# --------------------------------------------------

elif page == "Order Book":

    st.subheader("📚 Order Book")
    st.caption("All currently active buy and sell orders")

    buy_col, sell_col = st.columns(2)

    with buy_col:

        st.markdown("### 🟢 BUY SIDE")

        if engine.buy_orders:

            st.dataframe(
                get_order_data(engine.buy_orders),
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.info("No active buy orders.")

    with sell_col:

        st.markdown("### 🔴 SELL SIDE")

        if engine.sell_orders:

            st.dataframe(
                get_order_data(engine.sell_orders),
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.info("No active sell orders.")

    st.divider()

    st.subheader("Market Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Buy Orders", len(engine.buy_orders))
    col2.metric("Sell Orders", len(engine.sell_orders))
    col3.metric("Total Trades", len(engine.trade_history))


# --------------------------------------------------
# TRADE HISTORY
# --------------------------------------------------

elif page == "Trade History":

    st.subheader("🧾 Trade History")
    st.caption("A record of all successfully executed trades")

    if engine.trade_history:

        st.dataframe(
            get_trade_data(),
            use_container_width=True,
            hide_index=True,
        )

        prices = [
            trade.price
            for trade in engine.trade_history
        ]

        st.divider()

        st.subheader("Trade Price Movement")

        st.line_chart(
            prices,
            height=300,
        )

    else:

        st.info(
            "No trades executed yet. "
            "Place matching BUY and SELL orders to generate trade history."
        )


# --------------------------------------------------
# ANALYTICS
# --------------------------------------------------

elif page == "Analytics":

    st.subheader("⚡ Performance Analytics")
    st.caption("Order processing latency measurements")

    latencies = [
        item["Latency (ms)"]
        for item in st.session_state.latency_history
    ]

    if latencies:

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Measured Orders",
            len(latencies),
        )

        col2.metric(
            "Average Latency",
            f"{sum(latencies) / len(latencies):.4f} ms",
        )

        col3.metric(
            "Minimum Latency",
            f"{min(latencies):.4f} ms",
        )

        col4.metric(
            "Maximum Latency",
            f"{max(latencies):.4f} ms",
        )

        st.divider()

        st.subheader("Latency History")

        st.line_chart(
            latencies,
            height=300,
        )

    else:

        st.info(
            "No latency data available. "
            "Place some orders to collect performance measurements."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown("""
<div style="text-align:center; padding:10px;">
    <p style="color:#64748b; font-size:12px;">
        ⚡ CHRONOSMATCH &nbsp; | &nbsp;
        LOW-LATENCY ORDER MATCHING SYSTEM
    </p>
</div>
""", unsafe_allow_html=True)
