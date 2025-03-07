import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.ticker as ticker

st.title("Dashboard Analisis Data Penyewaan Sepeda")

# Membaca dataset
file_path = "combined_dataset.csv"
df = pd.read_csv(file_path)
df.rename(columns={"cnt": "total_rent"}, inplace=True)
df.rename(columns={"yr": "year"}, inplace=True)
df.rename(columns={"dteday": "dateday"}, inplace=True)
df.rename(columns={"mnth": "month"}, inplace=True)
df.rename(columns={"weekday": "day_of_week"}, inplace=True)
df.rename(columns={"weathersit": "weather_condition"}, inplace=True)
df.rename(columns={"casual": "casual_user"}, inplace=True)
df.rename(columns={"registered": "registered_user"}, inplace=True)
df.rename(columns={"instant": "index"}, inplace=True) #mengganti seluruh nama kolom yang ambigu
df["dateday"] = pd.to_datetime(df["dateday"])

def plot_rental_trends(df):
    avg_rentals = df.groupby("dateday")["total_rent"].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=avg_rentals.index, y=avg_rentals.values, marker="o", color="red", linewidth=2, ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda Harian")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.grid(True)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.0f}'.format(x)))  # Format Y-axis to avoid scientific notation
    st.pyplot(fig)

def plot_seasonal_rentals(df):
    avg_seasonal_rentals = df.groupby("season")["total_rent"].mean().sort_values()
    if not avg_seasonal_rentals.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=avg_seasonal_rentals.index, y=avg_seasonal_rentals.values, palette="viridis", ax=ax)
        ax.set_xlabel("Musim")
        ax.set_ylabel("Rata-rata Penyewaan Sepeda")
        ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.0f}'.format(x)))  # Format Y-axis to avoid scientific notation
        st.pyplot(fig)
    else:
        st.write("Tidak ada data untuk musim yang dipilih.")

def plot_weather_rentals(df):
    avg_weather_rentals = df.groupby("weather_condition")["total_rent"].mean().sort_index()
    if not avg_weather_rentals.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=avg_weather_rentals.index, y=avg_weather_rentals.values, palette="coolwarm", ax=ax)
        ax.set_xlabel("Kondisi Cuaca")
        ax.set_ylabel("Rata-rata Penyewaan Sepeda")
        ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.0f}'.format(x)))  # Format Y-axis to avoid scientific notation
        st.pyplot(fig)
    else:
        st.write("Tidak ada data untuk kondisi cuaca yang dipilih.")

def plot_temp_trends(df):
    avg_temp = df.groupby("dateday")["temp"].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=avg_temp.index, y=avg_temp.values, marker="o", color="blue", linewidth=2, ax=ax)
    ax.set_title("Rata-rata Suhu Harian")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Rata-rata Suhu")
    ax.grid(True)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.1f}'.format(x)))  # Format Y-axis to avoid scientific notation
    st.pyplot(fig)

# Sidebar untuk pemilihan filter
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [df["dateday"].min(), df["dateday"].max()])
season_filter = st.sidebar.multiselect("Pilih Musim", df["season"].unique(), default=df["season"].unique())

# Filter dataset
filtered_df = df[(df["dateday"] >= pd.to_datetime(date_range[0])) & (df["dateday"] <= pd.to_datetime(date_range[1]))]
filtered_df = filtered_df[filtered_df["season"].isin(season_filter)]

# Tampilkan hasil
st.write("### Rata-rata Penyewaan Sepeda Harian")
plot_rental_trends(filtered_df)

st.write("### Rata-rata Penyewaan Sepeda Berdasarkan Musim")
plot_seasonal_rentals(filtered_df)

st.write("### Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
plot_weather_rentals(filtered_df)

st.write("### Rata-rata Suhu Harian")
plot_temp_trends(filtered_df)
