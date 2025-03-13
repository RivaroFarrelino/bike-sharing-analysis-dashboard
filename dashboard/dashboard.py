import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
main_df = pd.read_csv("main_data.csv")

# Mapping values
main_df['yr'] = main_df['yr_hour'].map({0: 2011, 1: 2012})
month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
             7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
main_df['mnth'] = main_df['mnth_hour'].map(month_map)

# Buat kategori kelembaban
bins_hum = [0, 0.3, 0.6, 1]
labels_hum = ["Rendah", "Sedang", "Tinggi"]
main_df["hum_category"] = pd.cut(main_df["hum_day"], bins=bins_hum, labels=labels_hum)

# Buat kategori kecepatan angin
bins_wind = [0, 0.2, 0.4, 1]
labels_wind = ["Rendah", "Sedang", "Tinggi"]
main_df["wind_category"] = pd.cut(main_df["windspeed_day"], bins=bins_wind, labels=labels_wind)

def filter_data(df):
    """Filter berdasarkan tahun dengan opsi 'Semua Tahun'."""
    st.sidebar.header("Filter Data")
    year_options = ['Semua Tahun'] + list(df['yr'].unique())
    year_selected = st.sidebar.selectbox("Pilih Tahun:", year_options)
    return df if year_selected == 'Semua Tahun' else df[df['yr'] == year_selected]

def show_metrics(df):
    """Menampilkan metrik utama."""
    col1, col2 = st.columns(2)
    with col1:
        total_rentals = df['cnt_day'].sum()
        st.metric(label="Total Peminjaman", value=f"{total_rentals:,}")
    with col2:
        avg_rentals = round(df['cnt_day'].mean(), 2)
        st.metric(label="Rata-rata Peminjaman Harian", value=f"{avg_rentals:,}")

def plot_trend(df):
    """Tren peminjaman per tahun dan per bulan."""
    st.subheader("📈 Tren Peminjaman Sepeda per Tahun & Bulan")
    yearly_trend = df.groupby("yr")["cnt_day"].sum().reset_index()
    monthly_trend = df.groupby("mnth")["cnt_day"].sum().reset_index()

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    
    sns.barplot(x="yr", y="cnt_day", data=yearly_trend, ax=ax[0], palette="Blues")
    ax[0].set_xlabel("Tahun")
    ax[0].set_ylabel("Total Peminjaman Sepeda")
    ax[0].set_title("Tren Peminjaman Sepeda per Tahun")

    sns.barplot(x="mnth", y="cnt_day", data=monthly_trend, ax=ax[1], palette="Greens")
    ax[1].set_xlabel("Bulan")
    ax[1].set_ylabel("Total Peminjaman Sepeda")
    ax[1].set_title("Tren Peminjaman Sepeda per Bulan")

    plt.tight_layout()
    st.pyplot(fig)

def plot_humidity_vs_rentals(df):
    """Pengaruh kelembaban terhadap peminjaman."""
    st.subheader("🌦️ Pengaruh Kelembaban terhadap Peminjaman")
    
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(x=df["hum_category"], y=df["cnt_day"], palette='Blues')
    plt.xlabel("Kategori Kelembaban")
    plt.ylabel("Rata-rata Peminjaman Sepeda")
    plt.title("Pengaruh Kelembaban terhadap Peminjaman Sepeda")
    
    st.pyplot(fig)

def plot_windspeed_vs_rentals(df):
    """Pengaruh kecepatan angin terhadap peminjaman."""
    st.subheader("💨 Pengaruh Kecepatan Angin terhadap Peminjaman")

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(x=df["wind_category"], y=df["cnt_day"], palette='Reds')
    plt.xlabel("Kategori Kecepatan Angin")
    plt.ylabel("Rata-rata Peminjaman Sepeda")
    plt.title("Pengaruh Kecepatan Angin terhadap Peminjaman Sepeda")

    st.pyplot(fig)

def plot_hourly_trend(df):
    """Tren peminjaman per jam."""
    st.subheader("🕒 Tren Peminjaman Sepeda per Jam")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x='hr', y='cnt_hour', ci=None, marker='o', color='green')
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Peminjaman")
    plt.title("Rata-rata Peminjaman Sepeda per Jam")
    st.pyplot(fig)

# Tampilan utama dashboard
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Menampilkan analisis tren peminjaman sepeda berdasarkan dataset.")

# Filter data berdasarkan tahun
filtered_data = filter_data(main_df)

# Menampilkan metrik
show_metrics(filtered_data)

# Menampilkan visualisasi berdasarkan urutan pertanyaan bisnis
plot_trend(filtered_data)
plot_humidity_vs_rentals(filtered_data)
plot_windspeed_vs_rentals(filtered_data)
plot_hourly_trend(filtered_data)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center;'>" 
            "<b>🚲 Bike Sharing Dashboard</b><br>"
            "Created by <b>Muhammad Rivaro Farrelino Gozali</b><br>"
            "Powered by Streamlit & Data Science</div>", unsafe_allow_html=True)
