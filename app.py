import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# CONFIG PAGE
# ======================
st.set_page_config(
    page_title="Dashboard Analisis Data",
    layout="wide"
)

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    customers = pd.read_csv('customers_dataset.csv')
    orders = pd.read_csv('orders_dataset.csv')
    order_items = pd.read_csv('order_items_dataset.csv')
    products = pd.read_csv('products_dataset.csv')
    category = pd.read_csv('product_category_name_translation.csv')
    return customers, orders, order_items, products, category

customers, orders, order_items, products, category = load_data()

# ======================
# PREPROCESSING
# ======================
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

df = orders.merge(order_items, on='order_id')
df = df.merge(products, on='product_id')
df = df.merge(category, on='product_category_name', how='left')

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.title("⚙️ Filter Data")

min_date = df['order_purchase_timestamp'].min()
max_date = df['order_purchase_timestamp'].max()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    [min_date, max_date]
)

df = df[
    (df['order_purchase_timestamp'] >= pd.to_datetime(date_range[0])) &
    (df['order_purchase_timestamp'] <= pd.to_datetime(date_range[1]))
]

# ======================
# HEADER
# ======================
st.title("🚀 Dashboard Analisis E-Commerce")
st.markdown("Dashboard interaktif untuk analisis penjualan dan segmentasi pelanggan")

# ======================
# KPI
# ======================
total_revenue = df['price'].sum()
total_orders = df['order_id'].nunique()
total_customers = df['customer_id'].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("🛒 Total Orders", total_orders)
col3.metric("👥 Total Customers", total_customers)

st.markdown("---")

# ======================
# SALES TREND
# ======================
st.subheader("📈 Tren Penjualan Bulanan")

df['month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
monthly = df.groupby('month')['price'].sum().reset_index()

fig = px.line(monthly, x='month', y='price', markers=True)
st.plotly_chart(fig, use_container_width=True)

# ======================
# TOP CATEGORY
# ======================
st.subheader("🏆 Top 10 Kategori Produk")

top_cat = df.groupby('product_category_name_english')['price'] \
    .sum().sort_values(ascending=False).head(10).reset_index()

fig2 = px.bar(top_cat, x='product_category_name_english', y='price')
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ======================
# RFM ANALYSIS
# ======================
st.subheader("👥 Customer Segmentation (RFM Analysis)")

snapshot_date = df['order_purchase_timestamp'].max()

rfm = df.groupby('customer_id').agg({
    'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
    'order_id': 'nunique',
    'price': 'sum'
}).reset_index()

rfm.columns = ['customer_id', 'Recency', 'Frequency', 'Monetary']

# SCORING
rfm['R_score'] = pd.qcut(rfm['Recency'], 4, labels=[4,3,2,1])
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1,2,3,4])
rfm['M_score'] = pd.qcut(rfm['Monetary'], 4, labels=[1,2,3,4])

rfm['RFM_score'] = rfm[['R_score','F_score','M_score']].astype(int).sum(axis=1)

# SEGMENTASI
def segment(score):
    if score >= 10:
        return "Champions"
    elif score >= 8:
        return "Loyal Customers"
    elif score >= 6:
        return "Potential Loyalist"
    elif score >= 4:
        return "At Risk"
    else:
        return "Lost"

rfm['Segment'] = rfm['RFM_score'].apply(segment)

# ======================
# VISUALISASI RFM
# ======================
col1, col2 = st.columns(2)

seg_count = rfm['Segment'].value_counts().reset_index()
seg_count.columns = ['Segment', 'Count']

with col1:
    st.write("Distribusi Segmentasi")
    fig3 = px.pie(seg_count, names='Segment', values='Count')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.write("Perbandingan Segment")
    fig4 = px.bar(seg_count, x='Segment', y='Count')
    st.plotly_chart(fig4, use_container_width=True)

# ======================
# TABEL RFM
# ======================
st.subheader("📋 Data RFM (Sample)")
st.dataframe(rfm.sort_values(by='RFM_score', ascending=False).head(20))

st.markdown("---")
