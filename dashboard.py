import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("sales_review_data.csv")

df = load_data()

# Title
st.title("E-Commerce Sales Dashboard (Brazilian Olist)")

# Sidebar Filter
st.sidebar.header("🔍 Filter Data")
kategori = st.sidebar.multiselect("Pilih Kategori Produk:", options=df['product_category_name'].unique(), default=df['product_category_name'].unique())
kota = st.sidebar.multiselect("Pilih Kota Customer:", options=df['customer_city'].unique(), default=df['customer_city'].unique())

# Filter data
filtered_df = df[(df['product_category_name'].isin(kategori)) & (df['customer_city'].isin(kota))]

# METRICS
st.markdown("## 📈 Ringkasan")
col1, col2, col3 = st.columns(3)
col1.metric("Total Order", f"{filtered_df['order_id'].nunique()}")
col2.metric("Total Revenue", f"R$ {filtered_df['total_revenue'].sum():,.0f}")
col3.metric("Jumlah Customer", f"{filtered_df['customer_id'].nunique()}")

# TOP 10 KATEGORI - ORDER COUNT
st.markdown("### 🛒 Top 10 Produk Berdasarkan Jumlah Pesanan")
top_orders = filtered_df['product_category_name'].value_counts().head(10)
st.bar_chart(top_orders)

# TOP 10 KATEGORI - TOTAL REVENUE
st.markdown("### 💰 Top 10 Produk Berdasarkan Total Revenue")
top_revenue = (
    filtered_df.groupby('product_category_name')['total_revenue']
    .sum().sort_values(ascending=False).head(10)
)
st.bar_chart(top_revenue)

# ANALISIS KORELASI DURASI & RATING
st.markdown("### ⏱️Korelasi Durasi Pengiriman & Review Score")
corr = filtered_df[['delivery_duration', 'review_score']].corr().iloc[0,1]
st.write(f"**Korelasi (Pearson):** {corr:.2f} ➝ {'Negatif' if corr < 0 else 'Positif'}")

fig, ax = plt.subplots()
sns.barplot(data=filtered_df.groupby('review_score')['delivery_duration'].mean().reset_index(),
            x='review_score', y='delivery_duration', palette='OrRd', ax=ax)
ax.set_title("Rata-rata Durasi Pengiriman per Review Score")
st.pyplot(fig)
