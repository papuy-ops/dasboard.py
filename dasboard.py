# Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Data Wrangling
# Load Dataset
day_df = pd.read_csv('/content/day.csv')
print(day_df.head(5))

# Merge Dataset
main_data = day_df
print(main_data)
main_data.to_csv("main_data.csv", index=False)

# Assessing Data
# Melihat informasi kolom
print(main_data.info())

# Melihat jumlah missing value di setiap kolom
print(day_df.isnull().sum())

# Memeriksa data duplikat
data_duplicated_day = day_df.duplicated().sum()
print("Jumlah data Duplikat dari Data Day CSV sebanyak : ", data_duplicated_day)

# Menampilkan statistik deskriptif
print(day_df.describe())

# Cleaning Data
# Convert tipe data kolom 'dteday' menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
print("Tipe data pada day_df setelah perubahan:")
print(day_df.info())

# Mengubah value kolom 'season' agar lebih deskriptif
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season_name'] = day_df['season'].map(season_mapping)
print(day_df.head())

# Menormalisasi kolom 'temp', 'atemp', 'hum', dan 'windspeed'
day_df['temp'] = day_df['temp'] * 41
day_df['atemp'] = day_df['atemp'] * 50
day_df['hum'] = day_df['hum'] * 100
day_df['windspeed'] = day_df['windspeed'] * 67
print(day_df.head())

# Menyimpan dataset yang sudah clean
day_df.to_csv("clean_day_bike_data.csv", index=False)

# Exploratory Data Analysis (EDA)
# Deskripsi lengkap dataset
print(day_df.describe(include="all"))

# Jumlah Penggunaan Sepeda Tiap Musim
season_avg_df = day_df.groupby('season_name')['cnt'].sum().reset_index()
season_avg_df.columns = ['Musim', 'Total Penggunaan Sepeda']
print(season_avg_df)

# Jumlah Penyewaan Sepeda Berdasarkan Kategori Suhu
day_df['temp_bin'], bins = pd.cut(day_df['temp'], bins=5, labels=['Sangat Dingin', 'Dingin', 'Sedang', 'Hangat', 'Panas'], retbins=True)
temp_avg_df = day_df.groupby('temp_bin')['cnt'].sum().reset_index()
temp_avg_df.columns = ['Kategori Suhu', 'Total Penyewaan Sepeda']
print(temp_avg_df)

# Perbandingan Penyewaan Berdasarkan Hari Kerja vs Hari Libur
working_day_df = day_df[day_df['workingday'] == 1]
holiday_df = day_df[day_df['workingday'] == 0]

working_day_season_avg_df = working_day_df.groupby('season_name')['cnt'].sum().reset_index()
holiday_season_avg_df = holiday_df.groupby('season_name')['cnt'].sum().reset_index()

working_day_season_avg_df.columns = ['Musim', 'Total Penyewaan (Hari Kerja)']
holiday_season_avg_df.columns = ['Musim', 'Total Penyewaan (Hari Libur)']

season_comparison_df = pd.merge(working_day_season_avg_df, holiday_season_avg_df, on='Musim')
print(season_comparison_df)

# Visualization & Explanatory Analysis
# Pengaruh Hari Libur terhadap Penjualan
season_avg = day_df.groupby('season_name')['cnt'].mean()
season_avg.plot(kind='bar', title='Pengaruh Hari Libur terhadap Penjualan')
plt.xlabel('Musim')
plt.ylabel('Penjualan (cnt)')
plt.show()

# Hubungan Hari dalam Minggu dengan Kinerja Penjualan
temp_avg = day_df.groupby('temp_bin')['cnt'].mean()
categories = day_df['temp_bin'].cat.categories
temp_ranges = [f"{bins[i]:.2f} - {bins[i+1]:.2f}" for i in range(len(bins)-1)]
average_counts = temp_avg.values

plt.figure(figsize=(10, 6))
bars = plt.bar(categories, average_counts, color='skyblue', alpha=0.7, edgecolor='black')

for i, bar in enumerate(bars):
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, y + 1, temp_ranges[i], ha='center', color='black')

plt.xlabel('Kategori Suhu', fontsize=12)
plt.ylabel('Rata-rata Penyewaan Sepeda (cnt)', fontsize=12)
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Kategori Suhu dan Kisaran Suhu', fontsize=16)
plt.grid(axis='y')
plt.show()

