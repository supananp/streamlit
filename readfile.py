import streamlit as st
import pandas as pd

# อ่านไฟล์ Excel ที่อยู่ในโฟลเดอร์เดียวกัน
df = pd.read_excel(r'C:\streamlit\streamlit\ยอดจดทะเบียนรถรวม.xlsx')

# แสดงข้อมูล
st.write(df)
