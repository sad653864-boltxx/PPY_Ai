import flet as ft
from google import genai
import base64

# ==========================================
# 🔑 الـ API Key الخاص بك مدمج بالكامل
# ==========================================
GEMINI_API_KEY = "AIzaSyDn59xB8JBBMaA3l51joeW7K9zSHRy0vQk"

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception:
    client = None

# قاعدة بيانات مؤقتة لتجربة الحسابات
registered_users = {"adamtony@gmail.com": "123456"}

def main(page: ft.Page):
    page.title = "PPY Ai"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0A0512"
    page.padding = 10

    # القائمة المنسدلة للغات والأوضاع
    selected_mode = "Main AI"
    selected_lang = "English"

    # منطقة الرسائل
    chat_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    # خانات الإدخال والتنبيهات
    entry = ft.TextField(
        hint_text="Type a message or prompt...",
        border_color="#8A2BE2",
        fill_color="#1F1135",
        expand=True,
        multiline=True,
        max_lines=3,
    )

    # دالة إرسال الرسائل وتفاعل الذكاء الاصطناعي
    def send_click(e):
        user_text = entry.value.strip()
        if not user_text:
            return

        # إضافة رسالة المستخدم
        chat_list.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(user_text, color=ft.Colors.WHITE),
                        bgcolor="#8A2BE2",
                        padding=10,
                        border_radius=10,
                        max_width=300,
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        )
        entry.value = ""
        page.update()

        # استجابة الذكاء الاصطناعي
        if client:
            try:
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=f"Answer as AI in {selected_lang}: {user_text}",
                )
                ai_text = response.text
            except Exception as ex:
                ai_text = f"Error: {str(ex)}"
        else:
            ai_text = "Connection Error."

        # إضافة رسالة الذكاء الاصطناعي مع زر القراءة
        chat_list.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.VOLUME_UP_ROUNDED,
                                    icon_color="#A855F7",
                                    icon_size=20,
                                    tooltip="Read Aloud",
                                ),
                                ft.Text(ai_text, color=ft.Colors.WHITE),
                            ]
                        ),
                        bgcolor="#1F1135",
                        padding=10,
                        border_radius=10,
                        border=ft.border.all(1, "#8A2BE2"),
                        max_width=320,
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            )
        )
        page.update()

    # شريط التحكم والإدخال السفلي
    input_row = ft.Row(
        [
            ft.IconButton(icon=ft.Icons.ADD_A_PHOTO, icon_color="#8A2BE2", tooltip="Attach Photo"),
            entry,
            ft.IconButton(icon=ft.Icons.MIC, icon_color="#8A2BE2", tooltip="Voice Input"),
            ft.IconButton(icon=ft.Icons.SEND, icon_color="#8A2BE2", on_click=send_click),
        ]
    )

    # بناء الصفحة الرئيسية للتطبيق
    page.add(
        ft.AppBar(
            title=ft.Text("PPY Ai", color="#A855F7", weight=ft.FontWeight.BOLD),
            bgcolor="#120822",
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Main AI"),
                        ft.PopupMenuItem(text="Coding"),
                        ft.PopupMenuItem(text="Free Games"),
                    ]
                )
            ],
        ),
        chat_list,
        input_row,
    )

    # حوار تسجيل الدخول / إنشاء حساب (Sign In & Sign Up)
    in_email = ft.TextField(label="Google Email (@gmail.com)", border_color="#8A2BE2")
    in_pass = ft.TextField(label="Password", password=True, can_reveal_password=True, border_color="#8A2BE2")
    error_lbl = ft.Text("", color=ft.Colors.RED_400)

    def handle_signin(e):
        email = in_email.value.strip().lower()
        password = in_pass.value.strip()

        if email in registered_users:
            if registered_users[email] == password:
                login_dialog.open = False
                page.update()
            else:
                error_lbl.value = "This password is incorrect."
                page.update()
            return

        # تسجيل حساب جديد في حال عدم وجوده
        if email and password:
            registered_users[email] = password
            login_dialog.open = False
            page.update()
        else:
            error_lbl.value = "This email is already in use or invalid."
            page.update()

    login_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Welcome to PPY Ai", color="#A855F7"),
        content=ft.Column([in_email, in_pass, error_lbl], tight=True, spacing=10),
        actions=[
            ft.ElevatedButton("Sign In / Sign Up", bgcolor="#8A2BE2", color=ft.Colors.WHITE, on_click=handle_signin)
        ],
    )

    page.dialog = login_dialog
    login_dialog.open = True
    page.update()

# تشغيل التطبيق
if __name__ == "__main__":
    ft.app(target=main)