
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#set style seaborn
sns.set(style='dark')
# Title for the Streamlit App
st.title('Bike Sharing Rental Analysis')

# Load the dataset
hour_df = pd.read_csv('E:\Project 1 Bangkit\hour.csv')
hour_df.head()

def create_month_rent_df(df):
    month_df = df.groupby(by='mnth').agg({
        'cnt': 'sum'
    }).reset_index()
    
    month_df['mnth'] = month_df['mnth'].astype(int)
    month_df = month_df.sort_values(by='mnth')
    return month_df

hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

min_date = pd.to_datetime(hour_df['dteday']).dt.date.min()
max_date = pd.to_datetime(hour_df['dteday']).dt.date.max()
with st.sidebar:
    st.subheader('DATA HOUR')
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )
    #menampilkan jumlah penyewa sepeda berdasarkan casual, registered, dan cnt
    def create_hour_cnt_df(df):
        hour_cnt_rent_df = df.groupby(by='dteday').agg({
            'cnt': 'sum'
            }).reset_index()
        return hour_cnt_rent_df
    hour_cnt_rent_df = create_hour_cnt_df(hour_df)

    def create_hour_casual_df(df):
        hour_casual_rent_df = df.groupby(by='dteday').agg({
            'casual': 'sum'
            }).reset_index()
        return hour_casual_rent_df
    hour_casual_rent_df = create_hour_casual_df(hour_df)

    def create_hour_registered_df(df):
        hour_registered_rent_df = df.groupby(by='dteday').agg({
            'registered': 'sum'
            }).reset_index()
        return hour_registered_rent_df
    hour_registered_rent_df = create_hour_registered_df(hour_df)

    #membuat main
    main_df = hour_df[(hour_df['dteday'] >= str(start_date)) & 
                 (hour_df['dteday'] <= str(end_date))]
    month_df = create_month_rent_df(main_df)

    #menampilkan jumlah berdasarkan jenis
    st.subheader('Jumlah Penyewa Sepeda Berdasarkan Jenis')
    hour_rent_casual = hour_casual_rent_df['casual'].sum()
    st.metric('Casual User', value=hour_rent_casual)
    
    hour_rent_registered = hour_registered_rent_df['registered'].sum()
    st.metric('Registered User', value=hour_rent_registered)
    
    hour_rent_total = hour_cnt_rent_df['cnt'].sum()
    st.metric('Casual & Registered User', value=hour_rent_total)

 #menampilkan data bulanan pengguna sepeda   
st.subheader('Jumlah Penyewa Setiap Bulan')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    month_df['mnth'],  
    month_df['cnt'],
    marker='o', 
    linewidth=2,
    color='tab:blue'
)

for index, row in month_df.iterrows():
    ax.text(row['mnth'], row['cnt'] + 1, str(row['cnt']), ha='center', va='bottom', fontsize=18)

ax.set_xticks(month_df['mnth']) 
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

#menampilkan jumlah pengguna berdasarkan season
st.subheader('Jumlah Penyewa Sepeda Berdasarkan Season')
colors = sns.color_palette("Set2")
byseason_df = hour_df.groupby(by="season").instant.nunique().reset_index()
byseason_df.rename(columns={
    "instant": "customer_count"
}, inplace=True)

# Plotting
plt.figure(figsize=(10, 5))
ax = sns.barplot(
    y="customer_count",
    x="season",
    data=byseason_df.sort_values(by="customer_count", ascending=False),
    palette=colors
)

for p in ax.patches:
    ax.text(
        p.get_x() + p.get_width() / 2,  
        p.get_height() + 1,  
        f'{int(p.get_height())}',  
        ha='center',  
        va='bottom',  
        fontsize=12  
    )

handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors[:4]]
labels = ['Spring', 'Summer', 'Fall', 'Winter']
plt.legend(handles=handles, labels=labels, title="Season", loc="upper right")

plt.ylabel('Jumlah pengguna sepeda')
plt.xlabel('Season')
plt.tick_params(axis='x', labelsize=12)
st.pyplot(plt)

#menampilkan jumlah pengguna berdasarkan jam
st.subheader('Jumlah Penyewa Sepeda Setiap Jam')
plt.figure(figsize=(10, 6))
ax = sns.barplot(
    x='hr',
    y='cnt',
    data=hour_df,
    palette='viridis' 
)
plt.xlabel('Jam', fontsize=14)
plt.ylabel('Jumlah Pengguna Sepeda', fontsize=14)
st.pyplot(plt)

#menampilkan jumlah penyewa sepeda berdasarkan weathersit
st.subheader('Jumlah Penyewa Sepeda Berdasarkan Kondisi Cuaca')
colors = sns.color_palette("Set2")
plt.figure(figsize=(10, 6))
sns.barplot(
    x='weathersit',
    y='cnt',
    data=hour_df,
    palette=colors
)

handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors[:4]]
labels = ['Clear/few Clouds', 'Mist + Cloudy/broken cloudy', 'Light snow/rain', 'Heavy rain/thunderstorm']
plt.legend(handles=handles, labels=labels, title="Cuaca", loc="upper right")

plt.xlabel('Kondisi Cuaca', fontsize=14)
plt.ylabel('Jumlah Pengguna Sepeda', fontsize=14)
st.pyplot(plt)

#menampilkan jumlah pengguna sepeda berdasarkan workingday, holiday, dan weekday
st.subheader('Jumlah Penyewa Sepeda Berdasarkan Workingday, Holiday, & Hari dalam Seminggu')
colors1 = sns.color_palette("Set2")
colors2 = sns.color_palette("Set1")
colors3 = sns.color_palette("Paired")

# Create subplots
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 10))

# Plot for workingday
sns.barplot(
    x='workingday',
    y='cnt',
    data=hour_df,
    palette=colors1,
    ax=axes[0]
)
axes[0].set_title('Jumlah Pengguna Sepeda berdasarkan Workingday')
axes[0].set_xlabel('Workingday')
axes[0].set_ylabel('Jumlah Pengguna Sepeda')
handles1 = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors1[:2]]
labels1 = ['Weekend', 'Workingday']
axes[0].legend(handles=handles1, labels=labels1, title='Keterangan')

# Plot for holiday
sns.barplot(
    x='holiday',
    y='cnt',
    data=hour_df,
    palette=colors2,
    ax=axes[1]
)
axes[1].set_title('Jumlah Pengguna Sepeda berdasarkan Holiday')
axes[1].set_xlabel('Holiday')
axes[1].set_ylabel('Jumlah Pengguna Sepeda')
handles2 = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors2[:2]]
labels2 = ['Bukan Holiday', 'Holiday']
axes[1].legend(handles=handles2, labels=labels2, title='Keterangan')

# Plot for weekday
ax = sns.barplot(
    x='weekday',
    y='cnt',
    data=hour_df,
    palette=colors3,
    ax=axes[2]
)
axes[2].set_title('Jumlah Pengguna Sepeda berdasarkan Hari dalam Seminggu')
axes[2].set_xlabel('Hari dalam Seminggu')
axes[2].set_ylabel('Jumlah Pengguna Sepeda')

for p in ax.patches:
    ax.text(
        p.get_x() + p.get_width() / 2,  
        p.get_height() + 1, 
        f'{int(p.get_height())}',  
        ha='center',  
        va='bottom',  
        fontsize=14 
    )

handles3 = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors3[:7]]
labels3 = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
axes[2].legend(handles=handles3, labels=labels3, title='Hari')

plt.tight_layout()
st.pyplot(fig)

# Additional Insights
st.subheader('Conclusion')
st.write('1. Bagaimana demografi pengguna sepeda yang kita miliki berdasarkan season?')
st.write('Berdasarkan hasil visualisasi data, demografi pengguna yang kita miliki tersebar cukup merata walaupun berbeda-beda musim dengan jumlah pengguna diatas 4000 pada keempat musim. Tetapi, musim paling banyak jumlah penyewa sepeda jatuh kepada musim fall. Dan jumlah penyewa sepeda terendah ditempati pada musim winter.')
st.write('2. Apakah setiap jam dapat mempengaruhi performa jumlah pengguna sepeda?')
st.write('Berdasarkan hasil dari visualisasi data tersebut, diketahui bahwa jumlah penyewa sepeda terbanyak ditempati pada jam 17 atau 5 sore, sedangkan jumlah penyewa sepeda terendah jatuh pada jam 4 pagi.')
st.write('3. Bagaimana peran dari weathersit terhadap jumlah pengguna sepeda (berdasarkan pengguna casual sekaligus registered)?')
st.write('Berdasarkan hasil dari data tersebut, diektahui bahwa posisi pertama dalam penyewa sepeda terbanyak jatuh kepada cuaca 1 (Clear, Few clouds, Partly cloudy, Partly cloudy). Dan jumlah penyewa sepeda terendah pada cuaca 4 (Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog).')
st.write('4. Tunjukkan performa penggunaan sepeda berdasarkan holiday, workingday, dan weekday. Bagaimana kondisi yang terlihat?')
st.write('Berdasarkan hasil dari visualisasi data tersebut, diketahui bahwa untuk jumlah pengguna sepeda berdasarkan workingday, hari kerja lebih unggul dibanding bukan hari kerja. Kemudian berdasarkan holiday (hari libur), diketahui bahwa penyewa sepeda tertinggi rata-rata pada hari bukan holiday dibandingkan dengan holiday. Terakhir berdasarkan weekday, Hari kamis dan Jumat menempati posisi yang sama dan urutan pertama dan hari dengan jumlah penyewa terkecil ditempati oleh hari minggu.')

# Note: Ensure that the dataset and column names match the ones in your notebook for accurate visualization.
