from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# =========================================================
# MAIN MENU
# =========================================================

def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Explore Tool Features",
                    callback_data="features"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎥 Watch Demo",
                    callback_data="demo"
                ),
                InlineKeyboardButton(
                    text="💰 Pricing",
                    callback_data="price"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❓ FAQ",
                    callback_data="faq"
                ),
                InlineKeyboardButton(
                    text="📞 Contact Admin",
                    callback_data="contact"
                )
            ],
        ]
    )


# =========================================================
# FEATURES MENU
# =========================================================

def features_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📊 Data Analytics",
                    callback_data="data_analytics"
                ),
                InlineKeyboardButton(
                    text="📈 Statistics",
                    callback_data="statistics"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Crash History",
                    callback_data="crash_history"
                ),
                InlineKeyboardButton(
                    text="📉 Insights",
                    callback_data="historical_insights"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📈 Crash Chart",
                    callback_data="crash_chart"
                ),
                InlineKeyboardButton(
                    text="🧠 Risk Management",
                    callback_data="risk_management"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Live Data Status",
                    callback_data="refresh_status"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Data Quality Monitor",
                    callback_data="data_quality"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Main Menu",
                    callback_data="back_menu"
                )
            ],
        ]
    )


# =========================================================
# BACK BUTTONS
# =========================================================

def back_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏠 Main Menu",
                    callback_data="back_menu"
                )
            ]
        ]
    )


def back_to_features_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Features",
                    callback_data="back_features"
                ),
                InlineKeyboardButton(
                    text="🏠 Main Menu",
                    callback_data="back_menu"
                )
            ]
        ]
    )


# =========================================================
# RISK MENU
# =========================================================

def risk_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🟢 Low Risk",
                    callback_data="risk_low"
                ),
                InlineKeyboardButton(
                    text="🟡 Medium Risk",
                    callback_data="risk_medium"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔴 High Risk",
                    callback_data="risk_high"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Features",
                    callback_data="back_features"
                ),
                InlineKeyboardButton(
                    text="🏠 Main Menu",
                    callback_data="back_menu"
                )
            ],
        ]
    )


# =========================================================
# DEMO MENU
# =========================================================

def demo_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="▶️ Watch Demo Video",
                    url="https://t.me/smart_aviator_guide/7"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Main Menu",
                    callback_data="back_menu"
                )
            ],
        ]
    )


# =========================================================
# PRICE MENU
# =========================================================

def price_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔥 Get Lifetime Access — Rs. 5,000",
                    callback_data="contact"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎥 Watch Demo",
                    callback_data="demo"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Main Menu",
                    callback_data="back_menu"
                )
            ],
        ]
    )


# =========================================================
# CONTACT
# =========================================================

def admin_contact_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Chat with Admin",
                    url="https://t.me/Jasinda_W"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Main Menu",
                    callback_data="back_menu"
                )
            ],
        ]
    )


# =========================================================
# FAQ
# =========================================================

def faq_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔥 Get Lifetime Access — Rs. 5,000",
                    callback_data="contact"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎥 Watch Demo",
                    callback_data="demo"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Main Menu",
                    callback_data="back_menu"
                )
            ],
        ]
    )

def data_quality_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Refresh Quality",
                    callback_data="refresh_quality"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Back to Features",
                    callback_data="back_features"
                )
            ],
        ]
    )