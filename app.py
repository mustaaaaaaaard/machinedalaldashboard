import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Machine Dalal Market Insights", layout="wide")

# --- Sample Data ---
sales_data = pd.DataFrame({
    'Machine Type': ['Lathe', 'Lathe', 'Milling', 'Lathe', 'Milling'],
    'Brand': ['BrandA', 'BrandA', 'BrandB', 'BrandC', 'BrandB'],
    'Sale Price': [5000, 5200, 7000, 4800, 7100],
    'Sale Date': pd.to_datetime(['2025-04-01', '2025-04-15', '2025-03-20', '2025-05-01', '2025-05-10'])
})

current_listings = pd.DataFrame({
    'Machine Type': ['Lathe', 'Milling'],
    'Brand': ['BrandA', 'BrandB'],
    'Listing Price': [5100, 7200],
    'Location': ['Delhi', 'Mumbai']
})

# --- UI Layout ---
st.title("🛠️ Machine Dalal Market Insights Dashboard")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Filter Listings")
    machine_type = st.selectbox("Select Machine Type", current_listings['Machine Type'].unique())
    brand = st.selectbox("Select Brand", current_listings[current_listings['Machine Type'] == machine_type]['Brand'].unique())
with col2:
    st.subheader("Key Metrics")
    # Price Benchmarking
    relevant_sales = sales_data[(sales_data['Machine Type'] == machine_type) & (sales_data['Brand'] == brand)]
    avg_price = relevant_sales['Sale Price'].mean() if not relevant_sales.empty else None
    recent_sales = sales_data[(sales_data['Machine Type'] == machine_type) & (sales_data['Sale Date'] > pd.Timestamp('2025-04-01'))]
    demand = len(recent_sales)
    st.metric("Average Sale Price", f"₹{avg_price:.0f}" if avg_price else "N/A")
    st.metric("Recent Demand (Sales)", f"{demand}")

st.markdown("---")

st.subheader("📋 Current Listings")
filtered = current_listings[(current_listings['Machine Type'] == machine_type) & (current_listings['Brand'] == brand)]
st.dataframe(filtered if not filtered.empty else pd.DataFrame([{"No listings found": ""}]))

st.subheader("📈 Price Trend")
trend_data = sales_data[(sales_data['Machine Type'] == machine_type) & (sales_data['Brand'] == brand)]
if not trend_data.empty:
    fig, ax = plt.subplots()
    ax.plot(trend_data['Sale Date'], trend_data['Sale Price'], marker='o', color='blue')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sale Price')
    ax.set_title(f"{machine_type} ({brand}) Price Trend")
    st.pyplot(fig)
else:
    st.info("No price trend data available for this selection.")

st.subheader("🤖 AI Recommendation")
if not filtered.empty:
    st.success(f"Based on your interest in {machine_type} ({brand}), consider the listing in {filtered.iloc[0]['Location']}.")
else:
    st.warning("No active listings match your filters. Try another machine type or brand.")
