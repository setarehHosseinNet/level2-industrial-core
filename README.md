# پروژه Heat Tracking System 🔥

این پروژه یک سیستم ردیابی ذوب (Heat Tracking) سطح ۲ صنعتی برای خطوط فولادسازی مانند ریخته‌گری پیوسته است. پروژه با زبان Python پیاده‌سازی شده و به‌صورت ماژولار شامل شبیه‌سازی تگ‌های صنعتی، ثبت اطلاعات، تحلیل کیفیت، محاسبه Setpoint، ذخیره در دیتابیس و نمایش زنده در داشبورد گرافیکی است.

---

## 🧱 ساختار پروژه

```
project-root/
├── core/                        # ماژول‌های اصلی پردازشی
│   ├── tracking.py              # ردیابی ذوب‌ها
│   ├── setpoint.py              # محاسبه دمای هدف
│   ├── quality.py               # ارزیابی کیفیت
│   └── __init__.py
├── db/                          # پایگاه داده
│   ├── database.py              # عملیات SQL
│   └── __init__.py
├── dcccom_simulator.py          # شبیه‌ساز تگ‌های DCCCOM
├── heat_tracking.db             # فایل SQLite
├── service_runner.py            # اجرای دائمی به‌عنوان سرویس
├── dashboard_live.py            # داشبورد گرافیکی زنده با Streamlit
├── main_static.py               # تست دستی/استاتیک ماژول‌ها
├── main_combined.py             # اجرای ترکیبی با شبیه‌سازی و تحلیل
├── heat_tracking.log            # فایل لاگ فعالیت سیستم
├── run_instructions.txt         # راهنمای اجرای سریع
└── README.md                    # این فایل
```

---

## ⚙️ پیش‌نیازها

* Python 3.9+
* Streamlit
* sqlite3
* کتابخانه `opcua` برای نسخه‌های آینده

نصب کتابخانه‌ها:

```bash
pip install streamlit pandas opcua
```

---

## 🚀 اجرای سریع

### اجرای تست استاتیک:

```bash
python main_static.py
```

### اجرای شبیه‌سازی داده‌ها و تحلیل:

```bash
python main_combined.py
```

### اجرای دائمی به‌عنوان سرویس:

```bash
nohup python service_runner.py & echo $! > service.pid
```

### اجرای داشبورد زنده:

```bash
streamlit run dashboard_live.py
```

---

## 📊 امکانات داشبورد

* نمایش زنده آخرین ذوب‌های ثبت‌شده
* مشاهده رویدادها و موقعیت‌ها
* بررسی فایل لاگ (heat\_tracking.log)
* به‌روزرسانی خودکار هر ۵ ثانیه
* کنترل راه‌اندازی / توقف سرویس در نوار کناری

---

## 🔒 امنیت و توسعه آینده

* معماری بروکری برای ارتباط بین سطوح Level2 و Level4
* پشتیبانی از OPC UA Client و Server
* شبیه‌سازی Tag‌ها از DCCOM و اتصال به PLC
* تحلیل آلارم‌ها، مدیریت کیفیت و گسترش MES

---

## 👨‍💻 توسعه‌دهنده

حسین ستاره – متخصص اتوماسیون صنعتی، سیستم‌های سطح ۲ و توسعه‌دهنده Python

[Github صفحه پروژه (به‌زودی)](https://github.com/setarehHosseinNet)

---

برای راهنمایی بیشتر یا توسعه ماژول‌های بعدی، با من در ارتباط باشید 🌐
