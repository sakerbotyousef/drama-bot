from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from datetime import datetime, timedelta
import random

# ========== الإعدادات تبعك جاهزة ==========
TOKEN = "8938677238:AAFiWvjznRjQaH3zCC7wgbvWpCk3oZ5SIXs"
REQUIRED_CHANNEL = "@sada313syria"  # قناتك
DEVELOPER_USERNAME = "𝒮𝒜𝒦𝐸𝑅 - تواصل عبر @sada313syria" 
# ============================================

ANGRY_WORDS = [
    'كذاب', 'حمار', 'غبي', 'ولي', 'انقلع', 'تفو', 'حيوان', 'خرا', 'تافه',
    'كلخرا', 'كل خرا', 'كل زق', 'بكرهكن', 'بكرهكم', 'باي', 'ليش ستلمتوني', 
    'ليش استلمتوني', 'الكل عليي', 'الكل علي', 'زعلان', 'زعلانة', 'مكتئب', 
    'مكتئبة', 'قمنقلع', 'قم انقلع', 'خصبقا', 'خلص بقا', 'خلص بقى',
    'اكرهكم', 'اكرهكن', 'سخيف', 'سخيفة', 'انقبر', 'انقلعي', 'بلا حكي'
]

FUNNY_REPLIES = [
    "شباب صلو عالنبي 😂 الخناق بيجيب التجاعيد وانتو لسا صغار",
    "ستوب ستوب ✋ اللي بخانق هلق بدنا نبعته على جروب محبي القطط لمدة ساعة",
    "يا جماعة وحدو الله 🤲 اللي بعصب بنقص عمره، واللي بيضحك بطول عمره",
    "خلص بكفي 😅 ترا الأدمن عم يراقب وعم ياكل بوشار ومبسوط عالدراما",
    "يارباه مستطيل خلص روقو شبكن 😘",
    "بدنا نررررروء بدنا نهدى شو🌝🌚🤣",
    "لك روقووو يا جماعة الدنيا ما مستاهلة 🤣 كباية ليمون ونحنا منرجع حبايب؟",
    "وحدوووه 😇 اللي بيعصب بنقص من رصيد ضحكته بالجنة",
    "خيو هدّي أعصابك، فاينل ما بدنا نخسرك ع مسبة 😂💔",
    "خلصووو دراما 📢 فيكن تتهاوشو بس بعد ما تشربو مي باردة اتفقنا؟"
]

MEMES = [
    "https://i.imgur.com/4M7IWwP.jpeg",
    "https://i.imgur.com/8QfYKuB.jpeg"
]

last_angry_time = {}
angry_count = {}

async def is_user_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"خطأ: تأكد انو البوت أدمن بقناة {REQUIRED_CHANNEL}")
        return False

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    if await is_admin(update, context):
        return

    chat_id = update.effective_chat.id
    text = update.message.text
    text_lower = text.lower()
    
    word_found = any(word in text_lower for word in ANGRY_WORDS)
    has_many_exclamation = text.count('!') >= 3
    has_many_question = text.count('؟') >= 3
    is_all_caps = text.isupper() and len(text) > 8
    has_repeated_chars = any(text.count(c * 4) > 0 for c in text)
    
    is_angry = word_found or has_many_exclamation or has_many_question or is_all_caps or has_repeated_chars
    
    if not is_angry:
        angry_count[chat_id] = 0
        return

    now = datetime.now()
    if chat_id in last_angry_time and now - last_angry_time[chat_id] > timedelta(minutes=2):
        angry_count[chat_id] = 0
    
    last_angry_time[chat_id] = now
    angry_count[chat_id] = angry_count.get(chat_id, 0) + 1

    if angry_count[chat_id] == 2:
        reply = random.choice(FUNNY_REPLIES)
        await update.message.reply_text(reply)

    elif angry_count[chat_id] >= 3:
        meme = random.choice(MEMES)
        await update.message.reply_photo(photo=meme, caption="يا جماعة الخناق وصل ليفل الوحش 😂")
        await context.bot.send_poll(
            chat_id=chat_id,
            question="مين معه حق برأيكم؟ 😂",
            options=["الأول", "التاني", "تنيناتكم غلط", "خلص بوسوا بعض"],
            is_anonymous=False
        )
        angry_count[chat_id] = 0

async def add_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not await is_admin(update, context):
        await update.message.reply_text("بس المشرفين بيقدروا يستخدموا هاد الأمر")
        return
    
    if not await is_user_subscribed(user_id, context):
        await update.message.reply_text(f"عذراً 😅\nلازم تشترك بقناتنا أول {REQUIRED_CHANNEL}\nبعدين بتحسن تضيف كلمات وتتحكم بالبوت")
        return
        
    if not context.args:
        await update.message.reply_text("استخدم: /addword كلمة_جديدة")
        return
    
    new_word = ' '.join(context.args).lower()
    if new_word not in ANGRY_WORDS:
        ANGRY_WORDS.append(new_word)
        await update.message.reply_text(f"تم إضافة '{new_word}' لقائمة كلمات الخناق ✅")
    else:
        await update.message.reply_text("هاي الكلمة موجودة أصلاً")

async def add_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not await is_admin(update, context):
        await update.message.reply_text("بس المشرفين بيقدروا يستخدموا هاد الأمر")
        return
        
    if not await is_user_subscribed(user_id, context):
        await update.message.reply_text(f"عذراً 😅\nلازم تشترك بقناتنا أول {REQUIRED_CHANNEL}\nبعدين بتحسن تضيف ردود وتتحكم بالبوت")
        return
        
    if not context.args:
        await update.message.reply_text("استخدم: /addreply الرد الجديد")
        return
    
    new_reply = ' '.join(context.args)
    if new_reply not in FUNNY_REPLIES:
        FUNNY_REPLIES.append(new_reply)
        await update.message.reply_text(f"تم إضافة الرد ✅\n{new_reply}")
    else:
        await update.message.reply_text("هاد الرد موجود أصلاً")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"أنا بوت كاتم الزعل 😇\n"
        f"مهمتي أخلي قروبكم رايق وبلا دراما.\n\n"
        f"🔧 للتحكم بالبوت: لازم تكون أدمن + مشترك بقناتنا {REQUIRED_CHANNEL}\n\n"
        f"برمجة و تطوير: {DEVELOPER_USERNAME}"
    )

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addword", add_word))
app.add_handler(CommandHandler("addreply", add_reply))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("بوت كاتم الزعل شغال...")
app.run_polling()
