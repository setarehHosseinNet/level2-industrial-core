# فایل: dashboard.py
import streamlit as st
import sqlite3
import pandas as pd

# اتصال به دیتابیس
conn = sqlite3.connect("heat_tracking.db")

st.set_page_config(page_title="Heat Tracker Dashboard", layout="wide")
st.title("🔥 داشبورد پایش ذوب‌ها (Level 2)")

# نمایش جدول ذوب‌ها
st.subheader("📋 لیست ذوب‌ها")
heats_df = pd.read_sql_query("SELECT * FROM heats ORDER BY start_time DESC", conn)
st.dataframe(heats_df, use_container_width=True)

# انتخاب یک ذوب خاص
selected_heat = st.selectbox("ذوب را انتخاب کنید:", heats_df["heat_id"])

# نمایش رویدادهای مرتبط
st.subheader("📌 رویدادهای ثبت‌شده برای ذوب انتخاب‌شده")
events_df = pd.read_sql_query(
    f"SELECT * FROM events WHERE heat_id = '{selected_heat}' ORDER BY timestamp", conn
)
st.dataframe(events_df, use_container_width=True)

# نمودار دما در طول زمان (اگر مقدار دما ثبت شده باشد)
temp_events = events_df[events_df["event_type"] == "Temperature"]
if not temp_events.empty:
    temp_events["timestamp"] = pd.to_datetime(temp_events["timestamp"])
    temp_events["value"] = pd.to_numeric(temp_events["position"], errors="coerce")
    st.line_chart(temp_events.set_index("timestamp")["value"])

conn.close()
