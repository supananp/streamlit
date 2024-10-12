import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.font_manager as fm

# โหลดฟอนต์ภาษาไทย เช่น TH Sarabun New
font_path = '/usr/share/fonts/truetype/thai/THSarabunNew.ttf'
fontprop = fm.FontProperties(fname=font_path)

# อ่านไฟล์ Excel
df = pd.read_excel('ยอดจดทะเบียนรถรวม.xlsx', engine='openpyxl')

# ฟังก์ชันสำหรับกราฟประเภทที่ 3 ถึง 6
def plot_engine_registration(engine_type, color, title):
    data_filtered = df[(df['Year'] >= 2561) & (df['Year'] <= 2567)]
    counts = data_filtered.groupby('Year')[engine_type].sum()

    fig, ax = plt.subplots(figsize=(4, 3))
    counts.plot(kind='bar', color=color, edgecolor='black', ax=ax)

    ax.set_title(title, fontproperties=fontprop)
    ax.set_xlabel('ปี', fontproperties=fontprop)
    ax.set_ylabel('จำนวนการจดทะเบียน', fontproperties=fontprop)
    ax.tick_params(axis='x', rotation=0)
    ax.grid(False)
    plt.tight_layout()
    st.pyplot(fig)

# กราฟที่ 1 (Bar Chart)
def plot_bar_chart():
    plt.rcParams['font.family'] = fontprop.get_name()  # ใช้ฟอนต์ TH Sarabun New
    years = df['Year'].unique()
    car_types = df['Type'].unique()

    bar_width = 0.2
    n_car_types = len(car_types)

    fig, axes = plt.subplots(1, len(years), figsize=(15, 6), sharey=True)

    for i, year in enumerate(years):
        ax = axes[i]
        df_year = df[df['Year'] == year]
        r1 = np.arange(n_car_types)

        ax.bar(r1, df_year['ICEV'], color='#ff6361', width=bar_width, label='ICEV', alpha=0.8)
        ax.bar(r1 + bar_width, df_year['HEV'], color='#ffa600', width=bar_width, label='HEV', alpha=0.8)
        ax.bar(r1 + 2 * bar_width, df_year['PHEV'], color='#58508d', width=bar_width, label='PHEV', alpha=0.8)
        ax.bar(r1 + 3 * bar_width, df_year['BEV'], color='#003f5c', width=bar_width, label='BEV', alpha=0.8)

        ax.set_xticks([r + bar_width * 1.5 for r in range(n_car_types)])
        ax.set_xticklabels(car_types, rotation=45, ha='right', fontproperties=fontprop)
        ax.set_title(f'ปี {year}', fontproperties=fontprop)

        if i == 0:
            ax.set_ylabel('จำนวนการจดทะเบียน', fontproperties=fontprop)

    axes[0].legend(prop=fontprop)
    plt.tight_layout()
    st.pyplot(fig)

# กราฟที่ 2 (Trend Chart)
def plot_trend_chart():
    plt.rcParams['font.family'] = fontprop.get_name()
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

    fig, ax = plt.subplots(figsize=(10, 6))
    for engine_type in engine_types:
        ax.plot(years, plot_data[engine_type], marker='o', label=engine_type, color=colors[engine_type])

    ax.set_xlabel('ปี', fontsize=14, labelpad=15, fontproperties=fontprop)
    ax.set_ylabel('จำนวนที่จดทะเบียน', fontsize=14, labelpad=15, fontproperties=fontprop)
    ax.set_title('แนวโน้มยอดจดทะเบียนรถแยกตามประเภทพลังงานในปี 2561 - 2567', fontsize=16, pad=20, fontproperties=fontprop)
    ax.legend(prop=fontprop, fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)

# ฟังก์ชันสร้าง gauge chart
def plot_gauge_chart(value, total_sum, label, color):
    fig, ax = plt.subplots(figsize=(3, 2), subplot_kw={'projection': 'polar'})
    percentage = (value / total_sum) * 100
    theta = (value / total_sum) * 2 * np.pi

    ax.barh(0, theta, color=color, height=1.0)
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1, 1)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_axis_off()

    ax.text(0, -0.5, f'{percentage:.1f}%', fontsize=12, ha='center', va='center', fontproperties=fontprop)
    ax.text(0, -1, f'{value:,}', fontsize=10, ha='center', va='center', fontproperties=fontprop)
    plt.title(label, fontsize=14, fontproperties=fontprop)
    st.pyplot(fig)

# เรียกใช้ฟังก์ชันแสดงกราฟ
col1, col2, col3 = st.columns(3)
with col1:
    plot_bar_chart()
with col2:
    plot_trend_chart()





st.markdown(
    """
    <div style="background-color:#ffa600;padding:5px;">
        <h1 style="color:#58508d;text-align:center;">จำนวนการจดทะเบียนรถแยกตามประเภทของพลังงาน</h1>
    </div>
    """,
    unsafe_allow_html=True
)