import os
import cv2
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# البيانات مدمجة مباشرة في السكربت
TOKEN = "8453371866:AAGbhkq5DUlBNJ2iu0IGYK8IdDqeTOr5lVc"
ALLOWED_USER_ID = 8453371866

def capture_image():
    """التقاط صورة من الكاميرا المحلية وحفظها مؤقتاً."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return None
        
    image_path = "temp_capture.jpg"
    cv2.imwrite(image_path, frame)
    return image_path

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("عذراً، غير مصرح لك باستخدام هذا البوت.")
        return
    await update.message.reply_text("البوت يعمل. أرسل الأمر /snap لالتقاط صورة.")

async def snap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("عذراً، غير مصرح لك باستخدام هذا البوت.")
        return
        
    await update.message.reply_text("جاري التقاط الصورة...")
    
    image_path = capture_image()
    
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, "rb") as photo:
                await update.message.reply_photo(photo=photo)
        finally:
            if os.path.exists(image_path):
                os.remove(image_path)
    else:
        await update.message.reply_text("حدث خطأ أثناء محاولة الوصول إلى الكاميرا.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("snap", snap))
    
    print("البوت يعمل الآن وجاهز...")
    app.run_polling()

if __name__ == "__main__":
    main()
