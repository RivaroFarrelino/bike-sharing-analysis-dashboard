import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

main_df = pd.read_csv("main_data.csv")

main_df['yr'] = main_df['yr_hour'].map({0: 2011, 1: 2012})
month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
             7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
main_df['mnth'] = main_df['mnth_hour'].map(month_map)

def filter_data(df):
    """Fungsi untuk menampilkan filter di sidebar."""
    st.sidebar.header("Filter Data")
    year_selected = st.sidebar.selectbox("Pilih Tahun:", df['yr'].unique())
    return df[df['yr'] == year_selected]

def show_metrics(df):
    """Fungsi untuk menampilkan statistik utama."""
    col1, col2 = st.columns(2)
    with col1:
        total_rentals = df['cnt_day'].sum()
        st.metric(label="Total Peminjaman", value=f"{total_rentals:,}")
    with col2:
        avg_rentals = round(df['cnt_day'].mean(), 2)
        st.metric(label="Rata-rata Peminjaman Harian", value=f"{avg_rentals:,}")

def plot_monthly_trend(df):
    """Fungsi untuk menampilkan tren peminjaman sepeda per bulan."""
    st.subheader("📈 Tren Peminjaman Sepeda per Bulan")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df, x='mnth', y='cnt_day', ci=None, palette='viridis')
    plt.xticks(rotation=45)
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Peminjaman")
    plt.title("Total Peminjaman Sepeda per Bulan")
    st.pyplot(fig)

def plot_humidity_vs_rentals(df):
    """Fungsi untuk menampilkan scatter plot antara kelembaban dan peminjaman."""
    st.subheader("🌦️ Pengaruh Kelembaban terhadap Peminjaman")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x='hum_day', y='cnt_day', alpha=0.5, color='blue')
    plt.xlabel("Kelembaban")
    plt.ylabel("Jumlah Peminjaman")
    st.pyplot(fig)

def plot_windspeed_vs_rentals(df):
    """Fungsi untuk menampilkan scatter plot antara kecepatan angin dan peminjaman."""
    st.subheader("💨 Pengaruh Kecepatan Angin terhadap Peminjaman")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x='windspeed_day', y='cnt_day', alpha=0.5, color='red')
    plt.xlabel("Kecepatan Angin")
    plt.ylabel("Jumlah Peminjaman")
    st.pyplot(fig)

def plot_hourly_trend(df):
    """Fungsi untuk menampilkan tren peminjaman per jam."""
    st.subheader("🕒 Tren Peminjaman Sepeda per Jam")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, x='hr', y='cnt_hour', ci=None, marker='o', color='green')
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Peminjaman")
    plt.title("Rata-rata Peminjaman Sepeda per Jam")
    st.pyplot(fig)

st.title("🚲 Bike Sharing Dashboard")
st.markdown("Menampilkan analisis tren peminjaman sepeda berdasarkan dataset.")

filtered_data = filter_data(main_df)

show_metrics(filtered_data)

plot_monthly_trend(filtered_data)
plot_humidity_vs_rentals(filtered_data)
plot_windspeed_vs_rentals(filtered_data)
plot_hourly_trend(filtered_data)

st.markdown("---")
st.markdown("<div style='text-align: center;'>" 
            "<b>🚲 Bike Sharing Dashboard</b><br>"
            "Created by <b>Muhammad Rivaro Farrelino Gozali</b><br>"
            "Powered by Streamlit & Data Science</div>", unsafe_allow_html=True)
