import asyncio
import logging
import time

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message, 
    CallbackQuery, 
    FSInputFile, 
    WebAppInfo, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)

from charts import create_crash_chart
from config import BOT_TOKEN

from keyboards import (
    main_menu,
    features_menu,
    back_to_features_button,
    demo_menu,
    risk_menu,
    price_menu,
    admin_contact_button,
    faq_menu,
    data_quality_menu,
)

from texts import (
    WELCOME_TEXT,
    FEATURES_TEXT,
    DEMO_TEXT,
    PRICE_TEXT,
    FAQ_TEXT,
    CONTACT_TEXT,
    RISK_TEXT,
)

from analytics import (
    calculate_statistics,
    get_recent_crash_history,
    get_statistical_analysis,
    get_historical_insights,
    get_refresh_status,
    get_data_quality
)


# =========================================================
# NGROK WEBAPP CONFIG
# =========================================================

# 🛑 මෙතැනට ඔයාට Ngrok එකෙන් ලැබුණු HTTPS Link එක Paste කරන්න:
WEBAPP_URL = "https://shaky-cranium-handwash.ngrok-free.dev"


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =========================================================
# BOT SETUP
# =========================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =========================================================
# COMMON ERROR TEXT
# =========================================================

ERROR_TEXT = """
⚠️ <b>Something went wrong.</b>

The requested information could not be loaded.

Please try again in a moment.

━━━━━━━━━━━━━━━━━━

ℹ️ If the problem continues,
please contact the administrator.
"""


# =========================================================
# START (WITH USER NAME GREETING)
# =========================================================

@dp.message(CommandStart())
async def start(message: Message):

    try:
        # User ගේ Telegram First Name එක ලබාගැනීම
        user_name = message.from_user.first_name if message.from_user and message.from_user.first_name else "Friend"

        # Personalized Welcome Text එක පිළියෙල කිරීම
        personalized_welcome = (
            f"👋 <b>ආයුබෝවන් {user_name}!</b>\n\n"
            f"{WELCOME_TEXT}"
        )

        await message.answer(
            personalized_welcome,
            parse_mode="HTML",
            reply_markup=main_menu()
        )

        # WebApp Dashboard Button එක යැවීම
        dashboard_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🚀 Open Live Analytics Dashboard",
                        web_app=WebAppInfo(url=WEBAPP_URL)
                    )
                ]
            ]
        )

        await message.answer(
            f"📊 <b>Welcome {user_name}! Live Aviator Dashboard</b>\n\n"
            "Dashboard එක Open කිරීමට පහත Button එක Click කරන්න:",
            parse_mode="HTML",
            reply_markup=dashboard_keyboard
        )

        logger.info(
            "User started bot | user_id=%s | name=%s",
            message.from_user.id,
            user_name
        )

    except Exception:

        logger.exception("❌ Error in /start")


# =========================================================
# DASHBOARD COMMAND
# =========================================================

@dp.message(Command("dashboard"))
async def dashboard_command(message: Message):
    try:
        dashboard_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🚀 Open Live Analytics Dashboard",
                        web_app=WebAppInfo(url=WEBAPP_URL)
                    )
                ]
            ]
        )

        await message.answer(
            "📊 <b>Live Aviator Dashboard</b>\n\n"
            "Dashboard එක Open කිරීමට පහත Button එක Click කරන්න:",
            parse_mode="HTML",
            reply_markup=dashboard_keyboard
        )

    except Exception:
        logger.exception("❌ Error in /dashboard command")


# =========================================================
# FEATURES
# =========================================================

@dp.callback_query(lambda c: c.data == "features")
async def features_callback(callback: CallbackQuery):

    try:

        await callback.answer("🚀 Opening features...")

        await callback.message.edit_text(
            FEATURES_TEXT,
            parse_mode="HTML",
            reply_markup=features_menu()
        )

    except Exception:

        logger.exception("❌ Error in Features")

        await callback.answer(
            "⚠️ Unable to open Features.",
            show_alert=True
        )


# =========================================================
# DATA ANALYTICS
# =========================================================

@dp.callback_query(lambda c: c.data == "data_analytics")
async def data_analytics_callback(callback: CallbackQuery):

    try:

        await callback.answer("📊 Analyzing crash data...")

        stats = calculate_statistics()

        text = f"""
📊 <b>DATA ANALYTICS</b>

━━━━━━━━━━━━━━━━━━

🎯 <b>Total Rounds</b>
{stats["total_rounds"]}

📈 <b>Average Crash</b>
{stats["average"]:.2f}x

━━━━━━━━━━━━━━━━━━

🔵 <b>Below 2x</b>
{stats["below_2"]:.2f}%

🟢 <b>2x – 5x</b>
{stats["between_2_5"]:.2f}%

🟡 <b>5x – 10x</b>
{stats["between_5_10"]:.2f}%

🔴 <b>10x+</b>
{stats["above_10"]:.2f}%

━━━━━━━━━━━━━━━━━━

📂 <b>Source</b>
Latest Aviator CSV

ℹ️ Historical data only.
"""

        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=back_to_features_button()
        )

    except Exception:

        logger.exception("❌ Error in Data Analytics")

        await callback.message.edit_text(
            ERROR_TEXT,
            parse_mode="HTML",
            reply_markup=back_to_features_button()
        )


# =========================================================
# CRASH HISTORY
# =========================================================

@dp.callback_query(lambda c: c.data == "crash_history")
async def crash_history_callback(callback: CallbackQuery):

    try:

        await callback.answer("📋 Loading latest history...")

        history = get_recent_crash_history(10)

        if not history:

            text = """
📋 <b>CRASH HISTORY</b>

━━━━━━━━━━━━━━━━━━

❌ <b>No data found</b>

No crash history records are
currently available.

Please check your CSV file.

━━━━━━━━━━━━━━━━━━
"""

        else:

            rows = []

            for item in history:

                rows.append(
                    f"#{item['round']}   {item['crash']}   {item['time']}"
                )

            history_text = "\n".join(rows)

            text = f"""
📋 <b>CRASH HISTORY</b>

━━━━━━━━━━━━━━━━━━

<b>Round      Crash      Time</b>

{history_text}

━━━━━━━━━━━━━━━━━━

📊 Latest 10 rounds
"""

        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=back_to_features_button()
        )

    except Exception:

        logger.exception("❌ Error in Crash History")

        await callback.message.edit_text(
            ERROR_TEXT,
            parse_mode="HTML",
            reply_markup=back_to_features_button()
        )


# =========================================================
# STATISTICAL ANALYSIS
# =========================================================

@dp.callback_query(lambda c: c.data == "statistics")
async def statistics_callback(callback: CallbackQuery):

    try:

        await callback.answer("📈 Calculating statistics...")

        stats = get_statistical_analysis()

        text = f"""
📈 <b>STATISTICAL ANALYSIS</b>

━━━━━━━━━━━━━━━━━━

🎯 <b>Total Rounds</b>
{stats["total"]}

📊 <b>Average</b>
{stats["average"]:.2f}x

📌 <b>Median</b>
{stats["median"]:.2f}x

⬇️ <b>Minimum</b>
{stats["minimum"]:.2f}x

⬆️ <b>Maximum</b>
{stats["maximum"]:.2f}x

📐 <b>Standard Deviation</b>
{stats["std_dev"]:.2f}

━━━━━━━━━━━━━━━━━━

📌 <b>Run Analysis</b>

🔵 Longest &lt;2x Run
{stats["longest_low_run"]} rounds

🔴 Longest ≥10x Run
{stats["longest_high_run"]} rounds

━━━━━━━━━━━━━━━━━━

⚠️ Historical statistics do not
guarantee future crash results.
"""

        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=back_to_features_button()
        )

    except Exception:

        logger.exception("❌ Error in Statistical Analysis")

        await callback.message.edit_text(
            ERROR_TEXT,
            parse_mode="HTML",
            reply_markup=back_to_features_button()
        )


# =========================================================
# RISK MANAGEMENT
# =========================================================

@dp.callback_query(lambda c: c.data == "risk_management")
async def risk_management_callback(callback: CallbackQuery):

    try:

        await callback.answer("🧠 Opening risk information...")

        await callback.message.edit_text(
            RISK_TEXT,
            parse_mode="HTML",
            reply_markup=risk_menu()
        )

    except Exception:

        logger.exception("❌ Error in Risk Management")

        await callback.answer(
            "⚠️ Unable to open Risk Management.",
            show_alert=True
        )


# =========================================================
# LOW RISK
# =========================================================

@dp.callback_query(lambda c: c.data == "risk_low")
async def risk_low_callback(callback: CallbackQuery):

    try:

        await callback.answer("🟢 Loading information...")

        text = """
🟢 <b>LOW RISK</b>

━━━━━━━━━━━━━━━━━━

Suggested maximum session exposure:

💰 <b>2% of bankroll</b>

Example:

Bankroll: Rs. 10,000

Reference exposure:
Rs. 200

━━━━━━━━━━━━━━━━━━

⚠️ This is a general
risk-management guideline.

It is NOT a prediction,
strategy, or guarantee of profit.

Never risk money you cannot
afford to lose.
"""

        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=back_to_features_button()
        )

    except Exception:

        logger.exception("❌ Error in Low Risk")


# =========================================================
# MEDIUM RISK
# =========================================================

@dp.callback_query(lambda c: c.data == "risk_medium")
async def risk_medium_callback(callback: CallbackQuery):

    try:

        await callback.answer("🟡 Loading information...")

        text = """
🟡 <b>MEDIUM RISK</b>

━━━━━━━━━━━━━━━━━━

Suggested maximum session exposure:

💰 <b>5% of bankroll</b>

Example:

Bankroll: Rs. 10,000

Reference exposure:
Rs. 500

━━━━━━━━━━━━━━━━━━

⚠️ This is a general
risk-management guideline.

It is NOT a prediction,
strategy, or guarantee of profit.

Never risk money you cannot
afford to lose.
"""

        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=back_to_features_button()
        )

    except Exception:

        logger.exception("❌ Error in Medium Risk")


# =========================================================
# HIGH RISK
# =========================================================

@dp.callback_query(lambda c: c.data == "risk_high")
async def risk_high_callback(callback: CallbackQuery):

    try:

        await callback.answer("🔴 Loading information...")

        text = """
🔴 <b>HIGH RISK</b>

━━━━━━━━━━━━━━━━━━

Suggested maximum session exposure:

💰 <b>10% of bankroll</b>

Example:

Bankroll: Rs. 10,000

Reference exposure:
Rs. 1,000

━━━━━━━━━━━━━━━━━━

⚠️ Higher exposure means
higher potential loss.

This is NOT a prediction,
strategy, or guarantee of profit.

Never risk money you cannot
afford to lose.
"""

        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=back_to_features_button()
        )

    except Exception:

        logger.exception("❌ Error in High Risk")


# =========================================================
# HISTORICAL INSIGHTS
# =========================================================

@dp.callback_query(lambda c: c.data == "historical_insights")
async def historical_callback(callback: CallbackQuery):

    try:

        await callback.answer("📉 Analyzing historical trends...")

        data = get_historical_insights()

        if data is None:

            text = """
📉 <b>HISTORICAL INSIGHTS</b>

━━━━━━━━━━━━━━━━━━

❌ <b>No CSV data found</b>

Historical analysis is unavailable
until crash-history data is available.
"""

        else:

            text = f"""
📉 <b>HISTORICAL INSIGHTS</b>

━━━━━━━━━━━━━━━━━━

📊 <b>Last 20 Average</b>
{data["average20"]:.2f}x

📊 <b>Last 50 Average</b>
{data["average50"]:.2f}x

📊 <b>Overall Average</b>
{data["overall_average"]:.2f}x

━━━━━━━━━━━━━━━━━━

🔥 <b>Highest Crash</b>
{data["highest"]:.2f}x

💥 <b>Lowest Crash</b>
{data["lowest"]:.2f}x

━━━━━━━━━━━━━━━━━━

📈 <b>Historical Trend</b>
{data["trend"]}

━━━━━━━━━━━━━━━━━━

ℹ️ This describes historical data
and does not predict future rounds.
"""

        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=back_to_features_button()
        )

    except Exception:

        logger.exception("❌ Error in Historical Insights")

        await callback.message.edit_text(
            ERROR_TEXT,
            parse_mode="HTML",
            reply_markup=back_to_features_button()
        )


# =========================================================
# CRASH CHART
# =========================================================

@dp.callback_query(lambda c: c.data == "crash_chart")
async def crash_chart_callback(callback: CallbackQuery):

    try:

        await callback.answer("📈 Generating crash chart...")

        chart_file = create_crash_chart(100)

        if chart_file is None:

            await callback.message.edit_text(
                """
📈 <b>CRASH TREND CHART</b>

━━━━━━━━━━━━━━━━━━

❌ No CSV data available.

Please check your crash-history
data source and try again.
""",
                parse_mode="HTML",
                reply_markup=back_to_features_button()
            )

            return

        photo = FSInputFile(chart_file)

        await callback.message.answer_photo(
            photo=photo,
            caption=(
                "📈 <b>Crash Trend</b>\n\n"
                "Latest 100 historical rounds\n\n"
                "ℹ️ Historical data only."
            ),
            parse_mode="HTML"
        )

    except Exception:

        logger.exception("❌ Error in Crash Chart")

        await callback.message.answer(
            ERROR_TEXT,
            parse_mode="HTML"
        )


# =========================
# DATA QUALITY MONITOR
# =========================

@dp.callback_query(lambda c: c.data == "data_quality")
async def data_quality_callback(callback: CallbackQuery):

    await callback.answer("🔍 Loading data quality...")

    try:

        data = get_data_quality()

        total = data["total_rows"]
        valid = data["valid_rows"]
        invalid = data["invalid_rows"]
        duplicates = data["duplicate_rows"]

        if total > 0:
            quality = (valid / total) * 100
        else:
            quality = 0

        if quality >= 99:
            quality_status = "🟢 Excellent"
        elif quality >= 95:
            quality_status = "🟡 Good"
        elif quality >= 90:
            quality_status = "🟠 Needs Attention"
        else:
            quality_status = "🔴 Poor"

        text = f"""
🔍 <b>DATA QUALITY MONITOR</b>

━━━━━━━━━━━━━━━━━━

📊 <b>DATA SUMMARY</b>

📁 Total Records:
<b>{total}</b>

✅ Valid Records:
<b>{valid}</b>

⚠️ Invalid Records:
<b>{invalid}</b>

🔁 Duplicate Records:
<b>{duplicates}</b>

━━━━━━━━━━━━━━━━━━

🎯 <b>DATA QUALITY</b>

<b>{quality:.2f}%</b>

Status:
<b>{quality_status}</b>

━━━━━━━━━━━━━━━━━━

ℹ️ <b>VALIDATION RULES</b>

✅ Valid numeric crash values
✅ Positive crash values
✅ NaN / Infinity rejected
✅ Duplicate rounds filtered
✅ Empty values rejected

━━━━━━━━━━━━━━━━━━

🔄 <b>Last Check:</b>
{time.strftime("%H:%M:%S")}

━━━━━━━━━━━━━━━━━━

ℹ️ Data quality is based on
the latest available CSV file.
"""

        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=data_quality_menu()
        )

    except Exception as error:

        error_text = str(error)

        if "message is not modified" in error_text.lower():
            return

        print(f"❌ Data Quality Error: {error}")

        try:

            await callback.message.edit_text(
                """
❌ <b>DATA QUALITY ERROR</b>

━━━━━━━━━━━━━━━━━━

Unable to refresh the data quality
information.

Please check the CSV file and try again.

━━━━━━━━━━━━━━━━━━
""",
                parse_mode="HTML",
                reply_markup=data_quality_menu()
            )

        except Exception as edit_error:

            print(f"❌ Telegram Edit Error: {edit_error}")


# =========================================================
# REFRESH DATA QUALITY
# =========================================================

@dp.callback_query(lambda c: c.data == "refresh_quality")
async def refresh_quality_callback(callback: CallbackQuery):

    try:

        await callback.answer("🔄 Checking latest CSV data...")

        data = get_data_quality()

        total = data["total_rows"]
        valid = data["valid_rows"]
        invalid = data["invalid_rows"]
        duplicates = data["duplicate_rows"]

        if total > 0:
            quality = (valid / total) * 100
        else:
            quality = 0

        if quality >= 99:
            quality_status = "🟢 Excellent"
        elif quality >= 95:
            quality_status = "🟡 Good"
        elif quality >= 90:
            quality_status = "🟠 Needs Attention"
        else:
            quality_status = "🔴 Poor"

        issues = []

        if invalid > 0:
            issues.append(f"• {invalid} invalid record(s)")

        if duplicates > 0:
            issues.append(f"• {duplicates} duplicate record(s)")

        if not issues:
            issues.append("• No data quality issues detected")

        issue_text = "\n".join(issues)

        text = f"""
🔍 <b>DATA QUALITY MONITOR</b>

━━━━━━━━━━━━━━━━━━

📊 <b>DATA SUMMARY</b>

📁 Total Records
<b>{total}</b>

✅ Valid Records
<b>{valid}</b>

⚠️ Invalid Records
<b>{invalid}</b>

🔁 Duplicate Records
<b>{duplicates}</b>

━━━━━━━━━━━━━━━━━━

🎯 <b>QUALITY SCORE</b>

<b>{quality:.2f}%</b>

Status:
<b>{quality_status}</b>

━━━━━━━━━━━━━━━━━━

⚠️ <b>ISSUES FOUND</b>

{issue_text}

━━━━━━━━━━━━━━━━━━

🧪 <b>VALIDATION CHECKS</b>

✅ Numeric crash values
✅ Positive values
✅ Empty values
✅ Duplicate rounds
✅ Invalid records

━━━━━━━━━━━━━━━━━━

🔄 <b>Last Check</b>

{time.strftime("%H:%M:%S")}

━━━━━━━━━━━━━━━━━━

ℹ️ Analysis is based on the
latest available Aviator CSV.
"""

        try:

            await callback.message.edit_text(
                text,
                parse_mode="HTML",
                reply_markup=data_quality_menu()
            )

        except Exception as edit_error:

            if "message is not modified" in str(edit_error).lower():

                await callback.answer("✅ Data is already up to date.")

                return

            raise

    except Exception:

        logger.exception("❌ Error refreshing Data Quality")

        try:

            await callback.answer(
                "❌ Unable to refresh data quality.",
                show_alert=True
            )

        except Exception:

            pass


# =========================================================
# AUTO REFRESH STATUS
# =========================================================

@dp.callback_query(lambda c: c.data == "refresh_status")
async def refresh_status_callback(callback: CallbackQuery):

    try:

        await callback.answer("🔄 Checking live data status...")

        data = get_refresh_status()

        text = f"""
🔄 <b>LIVE DATA STATUS</b>

━━━━━━━━━━━━━━━━━━

🟢 <b>Status</b>
{data["status"]}

🕐 <b>Last Updated</b>
{data["last_updated"]}

📊 <b>Total Rounds</b>
{data["total_rounds"]}

🆕 <b>New Rounds</b>
+{data["new_rounds"]}

📁 <b>Source</b>
{data["file_name"]}

━━━━━━━━━━━━━━━━━━

ℹ️ The system checks the CSV
for updated crash-history data.
"""

        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=back_to_features_button()
        )

    except Exception:

        logger.exception("❌ Error in Live Data Status")

        await callback.message.edit_text(
            ERROR_TEXT,
            parse_mode="HTML",
            reply_markup=back_to_features_button()
        )


# =========================================================
# DEMO
# =========================================================

@dp.callback_query(lambda c: c.data == "demo")
async def demo_callback(callback: CallbackQuery):

    try:

        await callback.answer("🎥 Opening demo...")

        await callback.message.edit_text(
            DEMO_TEXT,
            parse_mode="HTML",
            reply_markup=demo_menu()
        )

    except Exception:

        logger.exception("❌ Error in Demo")


# =========================================================
# PRICING
# =========================================================

@dp.callback_query(lambda c: c.data == "price")
async def price_callback(callback: CallbackQuery):

    try:

        await callback.answer("💰 Opening pricing...")

        await callback.message.edit_text(
            PRICE_TEXT,
            parse_mode="HTML",
            reply_markup=price_menu()
        )

    except Exception:

        logger.exception("❌ Error in Pricing")


# =========================================================
# FAQ
# =========================================================

@dp.callback_query(lambda c: c.data == "faq")
async def faq_callback(callback: CallbackQuery):

    try:

        await callback.answer("❓ Opening FAQ...")

        await callback.message.edit_text(
            FAQ_TEXT,
            parse_mode="HTML",
            reply_markup=faq_menu()
        )

    except Exception:

        logger.exception("❌ Error in FAQ")


# =========================================================
# CONTACT
# =========================================================

@dp.callback_query(lambda c: c.data == "contact")
async def contact_callback(callback: CallbackQuery):

    try:

        await callback.answer("📞 Opening contact...")

        await callback.message.edit_text(
            CONTACT_TEXT,
            parse_mode="HTML",
            reply_markup=admin_contact_button()
        )

    except Exception:

        logger.exception("❌ Error in Contact")


# =========================================================
# BACK TO MAIN MENU
# =========================================================

@dp.callback_query(lambda c: c.data == "back_menu")
async def back_menu_callback(callback: CallbackQuery):

    try:

        await callback.answer("🏠 Main Menu")

        await callback.message.edit_text(
            WELCOME_TEXT,
            parse_mode="HTML",
            reply_markup=main_menu()
        )

    except Exception:

        logger.exception("❌ Error in Back to Menu")

        await callback.answer(
            "⚠️ Unable to return to menu.",
            show_alert=True
        )


# =========================================================
# BACK TO FEATURES
# =========================================================

@dp.callback_query(lambda c: c.data == "back_features")
async def back_features_callback(callback: CallbackQuery):

    try:

        await callback.answer("⬅️ Features")

        await callback.message.edit_text(
            FEATURES_TEXT,
            parse_mode="HTML",
            reply_markup=features_menu()
        )

    except Exception:

        logger.exception("❌ Error in Back to Features")

        await callback.answer(
            "⚠️ Unable to return to Features.",
            show_alert=True
        )


# =========================================================
# RUN BOT
# =========================================================

async def main():

    logger.info("======================================")
    logger.info("🤖 My Aviator Helper")
    logger.info("🚀 Bot is starting...")
    logger.info("======================================")

    await dp.start_polling(bot)


if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        logger.info("🛑 Bot stopped by user.")

    except Exception:

        logger.exception("❌ Fatal bot error.")