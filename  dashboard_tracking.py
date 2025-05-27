# فایل: dashboard_tracking.py
import streamlit as st
import sqlite3
import pandas as pd

# اتصال به دیتابیس
conn = sqlite3.connect("heat_tracking.db")

st.set_page_config(page_title="Heat Position Tracking", layout="wide")
st.title("📍 پایش موقعیت ذوب‌ها در ایستگاه‌های مختلف")

# استخراج آخرین وضعیت هر ذوب
query = """
SELECT heat_id, status, position, MAX(last_update) as last_update
FROM heats
GROUP BY heat_id
ORDER BY last_update DESC
"""
status_df = pd.read_sql_query(query, conn)

# نمایش به صورت جدول خلاصه
st.subheader("📦 موقعیت فعلی ذوب‌ها")
st.dataframe(status_df, use_container_width=True)

# فیلتر بر اساس موقعیت
positions = status_df["position"].dropna().unique().tolist()
selected_pos = st.selectbox("فیلتر بر اساس موقعیت (اختیاری):", ["همه"] + positions)

if selected_pos != "همه":
    filtered_df = status_df[status_df["position"] == selected_pos]
else:
    filtered_df = status_df

# نمایش شمارش موقعیت‌ها
st.subheader("📊 آمار موقعیت‌ها")
st.bar_chart(filtered_df["position"].value_counts())

conn.close()
