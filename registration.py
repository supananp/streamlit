import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# อ่านไฟล์ Excel
df = pd.read_excel('ยอดจดทะเบียนรถรวม.xlsx', engine='openpyxl')

# ฟังก์ชันสำหรับกราฟประเภทที่ 3 ถึง 6
def plot_engine_registration(engine_type, color, title):
    data_filtered = df[(df['Year'] >= 2561) & (df['Year'] <= 2567)]
    counts = data_filtered.groupby('Year')[engine_type].sum()

    fig, ax = plt.subplots(figsize=(4, 3))  # ปรับขนาดให้เล็กลง
    counts.plot(kind='bar', color=color, edgecolor='black', ax=ax)

    ax.set_title(title)
    ax.set_xlabel('ปี')
    ax.set_ylabel('จำนวนการจดทะเบียน')
    ax.tick_params(axis='x', rotation=0)  # หมุน labels บนแกน X
    ax.grid(False)  # ปิดการแสดงเส้นกริด
    plt.tight_layout()
    st.pyplot(fig)

# กราฟที่ 1 (Bar Chart)
def plot_bar_chart():
    # ตั้งค่าฟอนต์ Tahoma เพื่อรองรับภาษาไทย
    plt.rcParams['font.family'] = 'Tahoma'
    years = df['Year'].unique()
    car_types = df['Type'].unique()

    bar_width = 0.2
    n_car_types = len(car_types)

    fig, axes = plt.subplots(1, len(years), figsize=(15, 6), sharey=True)  # ขยายความกว้าง

    for i, year in enumerate(years):
        ax = axes[i]
        df_year = df[df['Year'] == year]
        r1 = np.arange(n_car_types)

        ax.bar(r1, df_year['ICEV'], color='#ff6361', width=bar_width, label='ICEV', alpha=0.8)
        ax.bar(r1 + bar_width, df_year['HEV'], color='#ffa600', width=bar_width, label='HEV', alpha=0.8)
        ax.bar(r1 + 2 * bar_width, df_year['PHEV'], color='#58508d', width=bar_width, label='PHEV', alpha=0.8)
        ax.bar(r1 + 3 * bar_width, df_year['BEV'], color='#003f5c', width=bar_width, label='BEV', alpha=0.8)

        ax.set_xticks([r + bar_width * 1.5 for r in range(n_car_types)])
        ax.set_xticklabels(car_types, rotation=45, ha='right')
        ax.set_title(f'Year {year}')

        if i == 0:
            ax.set_ylabel('จำนวนการจดทะเบียน')

    axes[0].legend()
    plt.tight_layout()
    st.pyplot(fig)

# กราฟที่ 2 (Trend Chart)
def plot_trend_chart():
    plt.rcParams['font.family'] = 'Tahoma'
    data_years = df[(df['Year'] >= 2561) & (df['Year'] <= 2567)]
    engine_types = ['ICEV', 'HEV', 'PHEV', 'BEV']
    colors = {'ICEV': '#ff6361', 'HEV': '#ffa600', 'PHEV': '#58508d', 'BEV': '#003f5c'}

    plot_data = {engine_type: [] for engine_type in engine_types}
    years = data_years['Year'].unique()

    for year in years:
        data_year = data_years[data_years['Year'] == year]
        for engine_type in engine_types:
            registrations = data_year[engine_type].sum()
            plot_data[engine_type].append(registrations)

    fig, ax = plt.subplots(figsize=(10, 6))  # ขนาดกราฟที่ 2
    for engine_type in engine_types:
        ax.plot(years, plot_data[engine_type], marker='o', label=engine_type, color=colors[engine_type])

    ax.set_xlabel('ปี', fontsize=14, labelpad=15)
    ax.set_ylabel('จำนวนที่จดทะเบียน', fontsize=14, labelpad=15)
    ax.set_title('แนวโน้มยอดจดทะเบียนรถแยกตามประเภทพลังงานในปี 2561 - 2567', fontsize=16, pad=20)
    ax.legend(fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)

# เรียกใช้ฟังก์ชันกราฟ
col1, col2, col3 = st.columns(3)

with col1:
    plot_bar_chart()  # กราฟที่ 1

with col2:
    plot_trend_chart()  # กราฟที่ 2


with col3:
    plot_engine_registration('ICEV', '#ff6361', 'ยอดการจดทะเบียนรถประเภท ICEV ตั้งแต่ปี 2561-2567')  # กราฟที่ 3


# แถวที่ 2
col4, col5, col6, col7 = st.columns(4)

with col4:
    plot_engine_registration('ICEV', '#ff6361', 'ยอดการจดทะเบียนรถประเภท ICEV ตั้งแต่ปี 2561-2567')  # กราฟที่ 3

with col5:
    plot_engine_registration('HEV', '#ffa600', 'ยอดการจดทะเบียนรถประเภท HEV ตั้งแต่ปี 2561-2567')  # กราฟที่ 4

with col6:
    plot_engine_registration('PHEV', '#58508d', 'ยอดการจดทะเบียนรถประเภท PHEV ตั้งแต่ปี 2561-2567')  # กราฟที่ 5

with col7:
    plot_engine_registration('BEV', '#003f5c', 'ยอดการจดทะเบียนรถประเภท BEV ตั้งแต่ปี 2561-2567')  # กราฟที่ 6




st.markdown(
    """
    <div style="background-color:#ffa600;padding:5px;">
        <h1 style="color:#58508d;text-align:center;">จำนวนการจดทะเบียนรถแยกตามประเภทของพลังงาน</h1>
    </div>
    """,
    unsafe_allow_html=True
)
