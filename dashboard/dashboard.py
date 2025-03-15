import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
day_df = pd.read_csv("dashboard/day.csv")

day_df["yr"] = day_df["yr"].map({0: 2011, 1: 2012})

drop_col = [
    "instant",
    "season",
    "holiday",
    "weekday",
    "workingday",
    "windspeed",
    "weathersit",
    "casual",
    "registered",
]

for i in day_df.columns:
    if i in drop_col:
        day_df.drop(labels=i, axis=1, inplace=True)

# Mengubah nama judul kolom
day_df.rename(
    columns={
        "dteday": "dateday",
        "yr": "year",
        "mnth": "month",
        "temp": "temperature",
        "atemp": "feeling_temperature",
        "hum": "humidity",
        "cnt": "count",
    },
    inplace=True,
)

day_df["month"] = day_df["month"].map(
    {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }
)


def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by="dateday").agg({"count": "sum"}).reset_index()
    return daily_rent_df


def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by="month").agg({"count": "sum"})
    ordered_months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df


min_date = pd.to_datetime(day_df["dateday"]).dt.date.min()
max_date = pd.to_datetime(day_df["dateday"]).dt.date.max()


def filter_data(df):
    """Filter berdasarkan tahun dengan opsi 'Semua Tahun'."""
    st.sidebar.header("Filter Data")
    year_options = ["Semua Tahun"] + list(df["year"].unique())
    year_selected = st.sidebar.selectbox("Pilih Tahun:", year_options)
    return df if year_selected == "Semua Tahun" else df[df["year"] == year_selected]


def show_metrics(df):
    """Menampilkan metrik utama."""
    col1, col2 = st.columns(2)
    with col1:
        total_rentals = df["count"].sum()
        st.metric(label="Total Peminjaman", value=f"{total_rentals:,}")
    with col2:
        avg_rentals = round(df["count"].mean())
        st.metric(label="Rata-rata Peminjaman Harian", value=f"{avg_rentals:,}")


def plot_monthly_rentals(day_df):
    day_df["year"] = day_df["year"].replace({0: 2011, 1: 2012})

    day_df["month"] = pd.Categorical(
        day_df["month"],
        categories=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        ordered=True,
    )

    monthly_counts = (
        day_df.groupby(by=["month", "year"]).agg({"count": "sum"}).reset_index()
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.lineplot(
        data=monthly_counts,
        x="month",
        y="count",
        hue="year",
        palette={2011: "red", 2012: "blue"},
        marker="o",
        ax=ax,
    )

    for year in monthly_counts["year"].unique():
        subset = monthly_counts[monthly_counts["year"] == year]
    
        if not subset.empty and subset["count"].sum() > 0:
            max_row = subset.loc[subset["count"].idxmax()]
            ax.text(
                max_row["month"], max_row["count"] + 5000,
                f'{max_row["count"]:,}',
                ha="center", fontsize=11, fontweight="bold", color="black"
            )

    ax.set_title("Jumlah total sepeda yang disewakan berdasarkan Bulan dan tahun")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.legend(title="Tahun", loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    st.pyplot(fig)


def plot_scatter(day_df):
    fig, axes = plt.subplots(1, 3, figsize=(14, 6))

    # Scatter plot untuk 'temperature' vs 'count'
    sns.scatterplot(ax=axes[0], x="temperature", y="count", data=day_df, alpha=0.5)
    axes[0].set_title("Temperature vs Count")

    # Scatter plot untuk 'feeling_temperature' vs 'count'
    sns.scatterplot(
        ax=axes[1], x="feeling_temperature", y="count", data=day_df, alpha=0.5
    )
    axes[1].set_title("Feels Like Temperature vs Count")

    # Scatter plot untuk 'humidity' vs 'count'
    sns.scatterplot(ax=axes[2], x="humidity", y="count", data=day_df, alpha=0.5)
    axes[2].set_title("Humidity vs Count")

    plt.tight_layout()
    st.pyplot(fig)


# Tampilan utama dashboard
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Menampilkan analisis tren peminjaman sepeda berdasarkan dataset.")

# Filter data berdasarkan tahun
filtered_data = filter_data(day_df)

# Menampilkan metrik
show_metrics(filtered_data)

# Menampilkan visualisasi berdasarkan urutan pertanyaan bisnis
st.subheader("Tren Peminjaman Sepeda")
plot_monthly_rentals(filtered_data)

st.subheader("Dampak Temperatur & Kelembaban pada Peminjaman Sepeda")
plot_scatter(filtered_data)

st.markdown("---")
st.markdown("### **Kesimpulan dan Rekomendasi**")

st.markdown("""
#### **Conclusion Pertanyaan 1:**  
Berdasarkan analisis datasets bike sharing, ditemukan bahwa tren peminjaman sepeda pada tahun 2011 dan 2012 menunjukkan adanya perbedaan pola musiman. Pada tahun **2011**, jumlah penyewaan tertinggi terjadi pada bulan **Juni**, dengan jumlah peminjaman mencpai sekitar **143.512 unit sepeda**. Sementara itu, jumlah peminjaman terendah terjadi pada bulan **Januari**  

Di sisi lain, pada tahun **2012**, puncak peminjaman bergeser ke bulan **September**, dengan jumlah penyewaan sepeda mencapai **218.573 unit**. Namun, titik terendah tetap berada di bulan **Januari**, dgn jumlah penyewaan yang mirip dgn tahun sebelumnya. Selain itu, total peminjaman sepeda secara keseluruhan pada tahun **2012 lebih tinggi dibandingkan dgn tahun 2011**. Hal ini menunjukkan adanya peningkatan minat masyarakat dalam menggunakan layanan penyewaan sepeda, yang mungkin disebabkan oleh faktor eksternal seperti peningkatan fasilitas infrastruktur, promosi layanan, atau perubahan kebiasaan pengguna.  

**Rekomendasi:**  
1. **Meningkatkan Stok Sepeda pada Musim Ramai**  
   - Karena puncak penyewaan terjadi di bulan Juni (2011) dan September (2012), penyedia layanan sebaiknya meningkatkan ketersediaan sepeda pada bulan-bulan ini untuk mengantisipasi lonjakan permintaan.  
2. **Menyediakan Promosi atau Insentif di Bulan Januari**  
   - Mengingat bulan Januari memiliki jumlah peminjaman yang paling rendah, strategi promosi seperti diskon atau layanan tambahan dapat diterapkan untuk meningkatkan minat pengguna selama musim dingin.  

---

#### **Conclusion Pertanyaan 2:**  
Hasil analisis menunjukkan bahwa **humidity (kelembaban udara) memiliki korelasi negatif dgn jumlah penyewaan sepeda**. Artinya, semakin tinggi tingkat kelembaban, semakin sedikit jumlah peminjaman sepeda. Namun, korelasi ini relatif kecil sehingga dampaknya tidak terlalu signifikan. Sebagai contoh, pada kelembaban tinggi di atas 80%, rata-rata jumlah peminjaman sepeda berada di kisaran 3.500 - 4.500 unit per hari.  
Sebaliknya, saat kelembaban berada di sekitar 40-50%, rata-rata peminjaman meningkat hingga lebih dari 5.500 unit per hari.  

Di sisi lainnya, **temperature dan feeling_temperature memiliki korelasi positif terhadap jumlah peminjaman sepeda**. Ketika suhu meningkat, jumlah pengguna juga meningkat.  

**Rekomendasi:**  
1. **Memprioritaskan Perawatan Sepeda pada Musim Lembab**  
   - Karena kelembaban tinggi sedikit menurunkan jumlah peminjaman, penyedia layanan dapat mengantisipasi dengan merawat sepeda agar tetap dalam kondisi optimal dan memberikan informasi kepada pengguna terkait kenyamanan berkendara saat kelembaban tinggi.  
2. **Memanfaatkan Suhu Hangat untuk Kampanye Peningkatan Penggunaan Sepeda**  
   - Mengingat suhu yang lebih tinggi berkorelasi dengan meningkatnya jumlah peminjaman, kampanye atau promosi dapat difokuskan pada musim dengan suhu lebih tinggi untuk mendorong lebih banyak pengguna menggunakan layanan sepeda.  
""")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>"
    "<b>🚲 Bike Sharing Dashboard</b><br>"
    "Created by <b>Muhammad Rivaro Farrelino Gozali</b><br>"
    "Powered by Streamlit & Data Science</div>",
    unsafe_allow_html=True,
)
