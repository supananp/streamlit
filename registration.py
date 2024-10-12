import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# อ่านไฟล์ Excel
df = pd.read_excel('ยอดจดทะเบียนรถรวม.xlsx', engine='openpyxl')

# ฟังก์ชันสำหรับกราฟประเภทที่ 3 ถึง 6
def plot_engine_registration(engine_type, color, title):
    plt.rcParams['font.family'] = 'Noto Sans Thai'  # กำหนดฟอนต์ที่นี่
    data_filtered = df[(df['Year'] >= 2561) & (df['Year'] <= 2567)]
    counts = data_filtered.groupby('Year')[engine_type].sum()

    fig, ax = plt.subplots(figsize=(4, 3))  # ปรับขนาดให้เล็กลง
    counts.plot(kind='bar', color=color, edgecolor='black', ax=ax)

    ax.set_title(title, fontsize=14)  # ตั้งขนาดฟอนต์ของหัวตาราง
    ax.set_xlabel('ปี', fontsize=12)
    ax.set_ylabel('จำนวนการจดทะเบียน', fontsize=12)
    ax.tick_params(axis='x', rotation=0)  # หมุน labels บนแกน X
    ax.grid(False)  # ปิดการแสดงเส้นกริด
    plt.tight_layout()
    st.pyplot(fig)

# กราฟที่ 1 (Bar Chart)
def plot_bar_chart():
    plt.rcParams['font.family'] = 'Noto Sans Thai'  # กำหนดฟอนต์ที่นี่
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
        ax.set_xticklabels(car_types, rotation=45, ha='right', fontsize=12)  # ตั้งขนาดฟอนต์ของ labels
        ax.set_title(f'Year {year}', fontsize=14)  # ตั้งขนาดฟอนต์ของหัวตาราง

        if i == 0:
            ax.set_ylabel('จำนวนการจดทะเบียน', fontsize=12)

    axes[0].legend()
    plt.tight_layout()
    st.pyplot(fig)

# กราฟที่ 2 (Trend Chart)
def plot_trend_chart():
    plt.rcParams['font.family'] = 'Noto Sans Thai'  # กำหนดฟอนต์ที่นี่
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

# ฟังก์ชันสำหรับย่อขนาดตัวเลข
def format_number(value):
    if value >= 1_000_000:
        return f'{value / 1_000_000:.1f}M'  # เปลี่ยนเป็น "M" สำหรับล้าน
    elif value >= 1_000:
        return f'{value / 1_000:.1f}K'  # เปลี่ยนเป็น "K" สำหรับพัน
    else:
        return str(value)  # แสดงตามปกติถ้าน้อยกว่า 1,000

# ฟังก์ชันสำหรับสร้าง gauge chart พร้อมแสดงยอดรวมและเปอร์เซ็นต์ที่เหมาะสม
def plot_gauge_chart(value, total_sum, label, color):
    plt.rcParams['font.family'] = 'Noto Sans Thai'  # กำหนดฟอนต์ที่นี่
    fig, ax = plt.subplots(figsize=(3, 2), subplot_kw={'projection': 'polar'})  # ปรับขนาดให้เล็กลง

    # คำนวณมุมสำหรับกราฟ (0 ถึง 360 องศา)
    percentage = (value / total_sum) * 100  # คำนวณเป็นเปอร์เซ็นต์
    theta = (value / total_sum) * 2 * np.pi  # คำนวณมุมเป็นเรเดียน (จาก 0 ถึง 2π)

    # สร้าง gauge chart
    ax.barh(0, theta, color=color, height=1.0)  # วาดเส้นโค้งตามเปอร์เซ็นต์ที่คำนวณได้

    # ตั้งค่ากรอบและเส้นรอบวง
    ax.set_xlim(0, 2 * np.pi)  # แสดงมุม 0 ถึง 360 องศา (2π เรเดียน)
    ax.set_ylim(-1, 1)
    ax.set_theta_zero_location('N')  # ตั้งมุมเริ่มที่ตำแหน่ง 12 นาฬิกา
    ax.set_theta_direction(-1)  # หมุนตามเข็มนาฬิกา
    ax.set_axis_off()

    # แสดงค่าเปอร์เซ็นต์และปริมาณ
    ax.text(0, -0.5, f'{percentage:.1f}%', fontsize=12, ha='center', va='center')  # แสดงเปอร์เซ็นต์
    ax.text(0, -1, f'{value:,}', fontsize=10, ha='center', va='center')  # แสดงจำนวนรถ

    # ชื่อกราฟ
    plt.title(label, fontsize=14)
    st.pyplot(fig)

def plot_all_gauge_charts():
    data_years = df[(df['Year'] >= 2561) & (df['Year'] <= 2567)]
    total_registrations = {
        'ICEV': data_years['ICEV'].sum(),
        'HEV': data_years['HEV'].sum(),
        'PHEV': data_years['PHEV'].sum(),
        'BEV': data_years['BEV'].sum()
    }

    total_sum = sum(total_registrations.values())  # คำนวณยอดรวมทั้งหมด
    colors = {'ICEV': '#ff6361', 'HEV': '#ffa600', 'PHEV': '#58508d', 'BEV': '#003f5c'}

    cols = st.columns(len(total_registrations))
    for col, (engine_type, value) in zip(cols, total_registrations.items()):
        with col:
            # แสดงยอดรวมการจดทะเบียนรถแต่ละประเภทพร้อมย่อขนาดตัวเลข
            formatted_value = format_number(value)
            st.metric(label=f"ยอดรวม {engine_type}", value=formatted_value)
            plot_gauge_chart(value, total_sum, engine_type, colors[engine_type])  # ใช้ยอดรวมในการคำนวณเปอร์เซ็นต์

# แถว 1
col1, col2, col3 = st.columns(3)

with col1:
    plot_bar_chart()  # กราฟที่ 1

with col2:
    plot_all_gauge_charts()  # กราฟที่ 7

with col3:
    plot_trend_chart()  # กราฟที่ 2

# แถว 2
col4, col5 = st.columns(2)

with col4:
    plot_engine_registration('ICEV', '#ff6361', 'จำนวน ICEV')  # กราฟที่ 3

with col5:
    plot_engine_registration('HEV', '#ffa600', 'จำนวน HEV')  # กราฟที่ 4

# แถว 3
col6, col7 = st.columns(2)

with col6:
    plot_engine_registration('PHEV', '#58508d', 'จำนวน PHEV')  # กราฟที่ 5

with col7:
    plot_engine_registration('BEV', '#003f5c', 'จำนวน BEV')  # กราฟที่ 6


st.markdown(
    """
    <div style="background-color:#ffa600;padding:5px;">
        <h1 style="color:#58508d;text-align:center;">จำนวนการจดทะเบียนรถแยกตามประเภทของพลังงาน</h1>
    </div>
    """,
    unsafe_allow_html=True
) 
