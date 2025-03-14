import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
day_df = pd.read_csv("day.csv")

day_df['yr'] = day_df['yr'].map({0: 2011, 1: 2012})

drop_col = ['instant', 'season', 'holiday', 'weekday', 'workingday', 'windspeed', 'weathersit', 'casual', 'registered']

for i in day_df.columns:
  if i in drop_col:
    day_df.drop(labels=i, axis=1, inplace=True)

# Mengubah nama judul kolom
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'temp': 'temperature',
    'atemp': 'feeling_temperature',
    'hum': 'humidity',
    'cnt': 'count'
}, inplace=True)

day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})

def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df


min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()

def filter_data(df):
    """Filter berdasarkan tahun dengan opsi 'Semua Tahun'."""
    st.sidebar.header("Filter Data")
    year_options = ['Semua Tahun'] + list(df['year'].unique())
    year_selected = st.sidebar.selectbox("Pilih Tahun:", year_options)
    return df if year_selected == 'Semua Tahun' else df[df['year'] == year_selected]

def show_metrics(df):
    """Menampilkan metrik utama."""
    col1, col2 = st.columns(2)
    with col1:
        total_rentals = df['count'].sum()
        st.metric(label="Total Peminjaman", value=f"{total_rentals:,}")
    with col2:
        avg_rentals = round(df['count'].mean())
        st.metric(label="Rata-rata Peminjaman Harian", value=f"{avg_rentals:,}")

def plot_monthly_rentals(day_df):
    day_df['month'] = pd.Categorical(day_df['month'], categories=[
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ], ordered=True)

    monthly_counts = day_df.groupby(by=["month", "year"]).agg({
        "count": "sum"
    }).reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(
        data=monthly_counts,
        x="month",
        y="count",
        hue="year",
        palette="rocket",
        marker="o",
        ax=ax
    )

    ax.set_title("Jumlah Total Sepeda yang Disewakan Berdasarkan Bulan dan Tahun")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.legend(title="Tahun", loc="upper right")

    st.pyplot(fig)

def plot_scatter(day_df):
    fig, axes = plt.subplots(1, 3, figsize=(14, 6))

    # Scatter plot untuk 'temperature' vs 'count'
    sns.scatterplot(ax=axes[0], x='temperature', y='count', data=day_df, alpha=0.5)
    axes[0].set_title('Temperature vs Count')

    # Scatter plot untuk 'feeling_temperature' vs 'count'
    sns.scatterplot(ax=axes[1], x='feeling_temperature', y='count', data=day_df, alpha=0.5)
    axes[1].set_title('Feels Like Temperature vs Count')

    # Scatter plot untuk 'humidity' vs 'count'
    sns.scatterplot(ax=axes[2], x='humidity', y='count', data=day_df, alpha=0.5)
    axes[2].set_title('Humidity vs Count')

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

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center;'>" 
            "<b>🚲 Bike Sharing Dashboard</b><br>"
            "Created by <b>Muhammad Rivaro Farrelino Gozali</b><br>"
            "Powered by Streamlit & Data Science</div>", unsafe_allow_html=True)
