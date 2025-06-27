import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide", page_title="E-Commerce Sales Dashboard")
st.title("E-Commerce Sales Dashboard - Olist Brazil")

# --- Load Data ---
df = pd.read_csv("sales_review_data.csv")
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# --- SIDEBAR FILTER ---
st.sidebar.header("🔍 Filter Data")

# Filter Kategori Produk
kategori = st.sidebar.multiselect(
    "Pilih Kategori Produk:",
    options=df['product_category_name'].dropna().unique(),
    default=df['product_category_name'].dropna().unique()
)

# Filter Kota Customer
kota = st.sidebar.multiselect(
    "Pilih Kota Customer:",
    options=df['customer_city'].dropna().unique(),
    default=df['customer_city'].dropna().unique()
)

# Filter Tanggal
st.sidebar.subheader("📆 Filter Tanggal Pembelian")
start_date = st.sidebar.date_input("Tanggal Mulai", value=df['order_purchase_timestamp'].min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", value=df['order_purchase_timestamp'].max().date())

if start_date > end_date:
    st.sidebar.error("❌ Tanggal akhir harus setelah tanggal mulai.")

# Filter dataframe akhir
filtered_df = df[
    (df['product_category_name'].isin(kategori)) &
    (df['customer_city'].isin(kota)) &
    (df['order_purchase_timestamp'].dt.date >= start_date) &
    (df['order_purchase_timestamp'].dt.date <= end_date)
]

# --- Visualisasi Pertanyaan Bisnis 1 ---
st.markdown("## 📈 Ringkasan")
col1, col2, col3 = st.columns(3)
col1.metric("Total Order", f"{filtered_df['order_id'].nunique()}")
col2.metric("Total Revenue", f"R$ {filtered_df['total_revenue'].sum():,.0f}")
col3.metric("Jumlah Customer", f"{filtered_df['customer_id'].nunique()}")

# Jumlah Pesanan Terbanyak
# TOP 10 KATEGORI - ORDER COUNT
st.markdown("### 🛒 Top 10 Produk Berdasarkan Jumlah Pesanan")
order_counts = filtered_df['product_category_name'].value_counts().head(10).reset_index()
order_counts.columns = ['product_category_name', 'order_count']

fig1, ax1 = plt.subplots(figsize=(10,6))
sns.barplot(data=order_counts, x='order_count', y='product_category_name', palette='Blues_r', ax=ax1)
ax1.set_title('Top 10 Kategori Produk Berdasarkan Jumlah Pesanan')
ax1.set_xlabel('Jumlah Pesanan')
ax1.set_ylabel('Kategori Produk')
st.pyplot(fig1)

# Total Revenue Tertinggi
# TOP 10 KATEGORI - TOTAL REVENUE
st.markdown("### 💰 Top 10 Produk Berdasarkan Total Revenue")
revenue_by_category = (
    filtered_df.groupby('product_category_name')['total_revenue']
    .sum().sort_values(ascending=False).head(10).reset_index()
)

fig2, ax2 = plt.subplots(figsize=(10,6))
sns.barplot(data=revenue_by_category, x='total_revenue', y='product_category_name', palette='Greens_r', ax=ax2)
ax2.set_title('Top 10 Kategori Produk Berdasarkan Total Revenue')
ax2.set_xlabel('Total Revenue (BRL)')
ax2.set_ylabel('Kategori Produk')
st.pyplot(fig2)

# --- Visualisasi Pertanyaan Bisnis 2 ---
st.markdown("## ⏱️Durasi Pengiriman dan Review Score")

# Korelasi Pearson
corr = filtered_df[['delivery_duration', 'review_score']].corr().iloc[0,1]
st.write(f"**Korelasi (Pearson):** {corr:.2f} ➝ {'Negatif' if corr < 0 else 'Positif'}")

# Rata-rata Durasi per Skor Review
avg_duration = filtered_df.groupby('review_score')['delivery_duration'].mean().reset_index()
fig3, ax3 = plt.subplots(figsize=(8,5))
sns.barplot(data=avg_duration, x='review_score', y='delivery_duration', palette='OrRd', ax=ax3)
ax3.set_title('Rata-rata Durasi Pengiriman per Skor Review')
ax3.set_xlabel('Skor Review (1-5)')
ax3.set_ylabel('Rata-rata Durasi Pengiriman (hari)')
st.pyplot(fig3)

# Scatterplot Durasi vs Review Score
fig4, ax4 = plt.subplots(figsize=(8,5))
sns.scatterplot(data=filtered_df, x='delivery_duration', y='review_score', alpha=0.3, ax=ax4)
ax4.set_title('Scatter Plot: Durasi Pengiriman vs Review Score')
ax4.set_xlabel('Durasi Pengiriman (hari)')
ax4.set_ylabel('Review Score')
st.pyplot(fig4)

# Footer
st.markdown("---")
st.caption("Dashboard by Andi Amalia - Final Submission Dicoding Data Analyst")