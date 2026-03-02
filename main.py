import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ======================
# 🔐 التوكن (حطه هنا مباشرة لو ما تستخدم Environment Variables)
# ======================
TOKEN = os.getenv("TOKEN") or "حط_توكن_البوت_هنا"

DATA = "points.json"


# ======================
# 📦 تحميل البيانات بأمان
# ======================
def load():
    if os.path.exists(DATA):
        try:
            with open(DATA, "r") as f:
                return json.load(f)
        except:
            return {"users": {}, "teams": {}}
    return {"users": {}, "teams": {}}


def save(data):
    with open(DATA, "w") as f:
        json.dump(data, f, indent=4)


data = load()


# ======================
# ➕ إضافة نقاط
# ======================
async def dxp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text("استخدم: /dxp اسم عدد")

    user = context.args[0]

    try:
        amount = int(context.args[1])
    except:
        return await update.message.reply_text("❌ لازم الرقم يكون عدد صحيح")

    data["users"][user] = data["users"].get(user, 0) + amount
    save(data)

    await update.message.reply_text("✅ تمت إضافة النقاط")


# ======================
# ➖ خصم نقاط
# ======================
async def rep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text("استخدم: /rep اسم عدد")

    user = context.args[0]

    try:
        amount = int(context.args[1])
    except:
        return await update.message.reply_text("❌ لازم الرقم يكون عدد صحيح")

    data["users"][user] = data["users"].get(user, 0) - amount
    save(data)

    await update.message.reply_text("❌ تم خصم النقاط")


# ======================
# 🏆 أعلى 10
# ======================
async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not data["users"]:
        return await update.message.reply_text("❌ ما فيه أي نقاط حالياً")

    sorted_users = sorted(data["users"].items(), key=lambda x: x[1], reverse=True)[:10]

    text = "🏆 أفضل 10 أعضاء:\n"
    for i, (u, p) in enumerate(sorted_users, 1):
        text += f"{i}- {u} | {p}\n"

    await update.message.reply_text(text)


# ======================
# 🚀 تشغيل البوت
# ======================
if not TOKEN:
    raise ValueError("❌ TOKEN غير موجود!")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("dxp", dxp))
app.add_handler(CommandHandler("rep", rep))
app.add_handler(CommandHandler("top", top))

print("🔥 البوت شغال الآن...")
app.run_polling()
