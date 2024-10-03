import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

customers_df = pd.read_csv('customers_data.csv')
seller_product_df = pd.read_csv('seller_product_data.csv')

sns.set(style='dark')

st.header('E-Commerce Analysis Dashboard', divider=True)

#1
st.subheader('State Demografi Pelanggan')
bystate_df = customers_df.groupby(by="customer_state").customer_id.nunique().sort_values(ascending=False).reset_index()
bystate_df.rename(columns={
    "customer_id": "Jumlah Pelanggan", "customer_state": "State"
}, inplace=True)
bystate_df

#2
st.subheader('Pengaruh State Penjual dengan Performa Penjualan')
state_performance = seller_product_df.groupby('seller_state').agg({
    'review_score': 'mean',
    'price': 'sum'
}).reset_index()
state_performance.columns = ['seller_state', 'avg_review_score', 'total_sales']

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(50, 80))

sns.barplot(x='avg_review_score', y='seller_state', hue='avg_review_score', 
            data=state_performance, palette='coolwarm', ax=ax[0])
ax[0].set_title('\nRata Rata Review Score berdasarkan Seller State\n', fontsize=75)
ax[0].set_xlabel('\nAverage Review Score\n', fontsize=50)
ax[0].set_ylabel('\nSeller State\n', fontsize=50)
ax[0].tick_params(axis='y', labelsize=50)
ax[0].tick_params(axis='x', labelsize=50)
ax[0].legend().remove()
for score in range(1, 6):
    ax[0].axvline(x=score, color='black', linestyle='--', linewidth=3)

sns.barplot(x='total_sales', y='seller_state', hue='avg_review_score',
            data=state_performance, palette='coolwarm', ax=ax[1])
ax[1].set_title('\nTotal Penjualan berdasarkan Seller State\n', fontsize=75)
ax[1].set_xlabel('\nTotal Sales (Million)\n', fontsize=50)
ax[1].set_ylabel('\nSeller State\n', fontsize=50)
ax[1].tick_params(axis='y', labelsize=50)
ax[1].tick_params(axis='x', labelsize=50)
ax[1].legend().remove()

st.pyplot(fig)

#3
st.subheader('Hubungan Antara Jumlah Pembeli dengan Skor Review')
review_count = seller_product_df.groupby('review_score')['customer_id'].nunique().reset_index()
review_count.columns = ['review_score', 'unique_customers']

fig, ax = plt.subplots(figsize=(35, 15))

sns.barplot(x='review_score', y='unique_customers', data=review_count, ax=ax)
ax.set_title('\nBanyak Unique Customers per Review Score\n', fontsize=50)
ax.set_xlabel('\nReview Score\n', fontsize=35)
ax.set_ylabel('\nNumber of Unique Customers\n', fontsize=35)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=35)
ax.legend().remove()

st.pyplot(fig)

#4
st.subheader('Kategori Produk Terbaik dan Terburuk')
sum_order_items_df = seller_product_df.groupby("product_category_name").order_item_id.sum().sort_values(ascending=False).reset_index()
sum_order_items_df.rename(columns={
    "order_item_id": "order_count"
}, inplace=True)

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(50, 60))

sns.barplot(x="order_count", y="product_category_name", hue="product_category_name",
            data=sum_order_items_df.head(3), palette='coolwarm', ax=ax[0])
ax[0].set_ylabel('\nProduct Category\n', fontsize=50)
ax[0].set_xlabel('\nTotal Order\n', fontsize=50)
ax[0].set_title('\nTop 3 Kategori Produk Terbaik\n', fontsize=75)
ax[0].tick_params(axis='x', labelsize=50)
ax[0].tick_params(axis='y', labelsize=50)
ax[0].legend().remove()

sns.barplot(x="order_count", y="product_category_name", hue="product_category_name",
            data=sum_order_items_df.sort_values(by="order_count", ascending=True).head(3), 
            palette='coolwarm', ax=ax[1])
ax[1].set_ylabel('\nProduct Category\n', fontsize=50)
ax[1].set_xlabel('\nTotal Order\n', fontsize=50)
ax[1].set_title('\nTop 3 Kategori Produk Terburuk\n', fontsize=75)
ax[1].tick_params(axis='x', labelsize=50)
ax[1].tick_params(axis='y', labelsize=50)
ax[1].legend().remove()

st.pyplot(fig)

#5
st.subheader('Perbandingan Pesanan Tepat Waktu dan Telat')
seller_product_df['delivery_status'] = seller_product_df['order_delivered_customer_date'] > seller_product_df['order_estimated_delivery_date']
delivery_status_count = seller_product_df['delivery_status'].value_counts().reset_index()
delivery_status_count.columns = ['Status', 'Count']

fig, ax = plt.subplots(figsize=(35, 15))

sns.barplot(x='Status', y='Count', hue='Status', data=delivery_status_count, 
            palette='coolwarm', ax=ax)
ax.set_title('\nPerbandingan Pesanan Tepat Waktu dan Telat\n', fontsize=50)
ax.set_xlabel('\nStatus Delivery\n', fontsize=35)
ax.set_ylabel('\nBanyak Delivery\n', fontsize=35)
ax.tick_params(axis='x', labelsize=35)
ax.set_xticks(ticks=[0, 1], labels=['Late', 'On Time'])
ax.tick_params(axis='y', labelsize=35)
ax.legend().remove()

st.pyplot(fig)