# فایل: dashboard_live.py
import streamlit as st
import pandas as pd
import sqlite3
import time
import os
import signal

st.set_page_config(page_title="Live Heat Monitor", layout="wide")
st.title("📡 مانیتور زنده وضعیت ذوب‌ها")


# تابع برای واکشی داده از دیتابیس
def fetch_data():
    conn = sqlite3.connect("heat_tracking.db")
    df = pd.read_sql_query("""
        SELECT h.heat_id, h.start_time, h.status,
               e.event_type, e.position, e.timestamp
        FROM heats h
        LEFT JOIN events e ON h.heat_id = e.heat_id
        ORDER BY h.start_time DESC, e.timestamp DESC
        LIMIT 100
    """, conn)
    conn.close()
    return df

# تابع برای خواندن لاگ فایل
def read_logs(log_path="heat_tracking.log", num_lines=50):
    if not os.path.exists(log_path):
        return ["📭 لاگی پیدا نشد"]
    with open(log_path, "r") as f:
        lines = f.readlines()[-num_lines:]
    return lines

placeholder = st.empty()
st.sidebar.title("📄 لاگ‌ فایل")
st.sidebar.markdown("آخرین ۵۰ خط لاگ:")
st.sidebar.code("\n".join(read_logs()), language="bash")

# اجرای رفرش زنده هر 5 ثانیه
while True:
    with placeholder.container():
        data = fetch_data()
        st.dataframe(data, use_container_width=True)
        st.toast("🔄 بروز شد", icon="🔁")
    time.sleep(5)
# دکمه‌های راه‌اندازی و توقف سرویس
with st.sidebar:
    st.subheader("🛠 کنترل سرویس")
    if st.button("▶️ راه‌اندازی سرویس"):
        if not os.path.exists("service.pid"):
            os.system("nohup python service_runner.py & echo $! > service.pid")
            st.success("سرویس راه‌اندازی شد")
        else:
            st.warning("سرویس در حال اجراست")

    if st.button("⛔ توقف سرویس"):
        if os.path.exists("service.pid"):
            with open("service.pid", "r") as f:
                pid = int(f.read())
            try:
                os.kill(pid, signal.SIGTERM)
                os.remove("service.pid")
                st.success("سرویس متوقف شد")
            except Exception as e:
                st.error(f"خطا در توقف: {e}")
        else:
            st.info("سرویس فعال نیست")

# تابع برای واکشی داده از دیتابیس
def fetch_data():
    conn = sqlite3.connect("heat_tracking.db")
    df = pd.read_sql_query("""
        SELECT h.heat_id, h.start_time, h.status,
               e.event_type, e.position, e.timestamp
        FROM heats h
        LEFT JOIN events e ON h.heat_id = e.heat_id
        ORDER BY h.start_time DESC, e.timestamp DESC
        LIMIT 100
    """, conn)
    conn.close()
    return df

placeholder = st.empty()

# اجرای رفرش زنده هر 5 ثانیه
while True:
    with placeholder.container():
        data = fetch_data()

        # آخرین ذوب فعال
        latest_heat = data.iloc[0]["heat_id"] if not data.empty else "-"
        st.subheader(f"🔥 آخرین ذوب فعال: {latest_heat}")

        # آلارم‌ها
        if "Alarm" in data["event_type"].values:
            st.error("🚨 آلارم فعال شناسایی شد!", icon="⚠️")

        # جدول کامل داده‌ها
        st.dataframe(data, use_container_width=True)
        st.toast("🔄 بروز شد", icon="🔁")
    time.sleep(5)
