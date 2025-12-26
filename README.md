# RRK.ir Data Extractor

این پروژه برای استخراج داده از وب‌سایت [RRK.ir](https://rrk.ir/) با استفاده از **Selenium** و **requests** طراحی شده است.  
کد به گونه‌ای نوشته شده که بتواند محدوده‌ی تاریخ مشخص را ارسال کرده و داده‌های JSON مربوطه را دریافت کند.

## ویژگی‌ها

- اجرای خودکار مرورگر با Selenium  
- امکان تنظیم حالت **headless**  
- استخراج و تغییر تنظیمات body درخواست  
- ذخیره‌ی خروجی JSON در فایل `response.json`  

## پیش‌نیازها

- Python 3.10+  
- Google Chrome  
- Chromedriver متناسب با نسخه Chrome  

## نصب کتابخانه‌ها

```bash
pip install -r requirements.txt
