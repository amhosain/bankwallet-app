from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
import json
import os

COLORS = {
    'primary': '#1a237e',
    'secondary': '#0d47a1',
    'accent': '#ff6f00',
    'success': '#2e7d32',
    'danger': '#c62828',
    'gold': '#ffd700',
    'white': '#ffffff',
    'background': '#e8eaf6'
}

class BankWalletApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_file = "bank_wallet.json"
        self.data = {}
        self.password = ""

    def build(self):
        Window.clearcolor = get_color_from_hex(COLORS['background'])
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(LoanScreen(name='loan'))
        sm.add_widget(IbanScreen(name='iban'))
        sm.add_widget(CurrencyScreen(name='currency'))
        sm.add_widget(ChecksScreen(name='checks'))
        sm.add_widget(CustomersScreen(name='customers'))
        sm.add_widget(ReportScreen(name='report'))
        return sm

    def authenticate(self, password):
        if not os.path.exists(self.data_file):
            self.password = password
            self.data = {"customers": [], "checks": [], "loans": []}
            self.save_data()
            return True
        self.password = password
        return self.load_data()

    def save_data(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False

    def load_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return True
        except:
            return False

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        header = BoxLayout(size_hint_y=0.3)
        with header.canvas.before:
            Color(*get_color_from_hex(COLORS['primary']))
            RoundedRectangle(pos=header.pos, size=header.size, radius=[20])
        title = Label(text='🏦 کیف پول بانکی', font_size='28sp',
                      color=get_color_from_hex(COLORS['white']), bold=True)
        header.add_widget(title)
        layout.add_widget(header)

        form = BoxLayout(orientation='vertical', spacing=15, size_hint_y=0.5)
        self.password_input = TextInput(hint_text='🔐 رمز عبور', password=True,
                                         font_size='18sp', size_hint_y=None, height=50,
                                         multiline=False)
        form.add_widget(self.password_input)

        login_btn = Button(text='✅ ورود', font_size='20sp', size_hint_y=None,
                           height=55, background_color=get_color_from_hex(COLORS['secondary']),
                           color=get_color_from_hex(COLORS['white']), bold=True)
        login_btn.bind(on_press=self.login)
        form.add_widget(login_btn)

        self.error_label = Label(text='', color=get_color_from_hex(COLORS['danger']),
                                  font_size='16sp')
        form.add_widget(self.error_label)

        layout.add_widget(form)
        self.add_widget(layout)

    def login(self, instance):
        password = self.password_input.text
        app = App.get_running_app()
        if app.authenticate(password):
            self.manager.current = 'main'
        else:
            self.error_label.text = '❌ رمز اشتباه است!'

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        header = BoxLayout(size_hint_y=0.15, padding=15)
        with header.canvas.before:
            Color(*get_color_from_hex(COLORS['primary']))
            RoundedRectangle(pos=header.pos, size=header.size, radius=[15])
        title = Label(text='🏦 کیف پول بانکی', font_size='24sp',
                      color=get_color_from_hex(COLORS['white']), bold=True)
        header.add_widget(title)
        layout.add_widget(header)

        info_box = BoxLayout(size_hint_y=0.15, spacing=10, padding=10)
        with info_box.canvas.before:
            Color(*get_color_from_hex(COLORS['gold']), 0.2)
            RoundedRectangle(pos=info_box.pos, size=info_box.size, radius=[10])
        info_label = Label(text='👥 0 مشتری | 💳 0 چک', font_size='16sp',
                           color=get_color_from_hex(COLORS['primary']))
        info_box.add_widget(info_label)
        layout.add_widget(info_box)

        menu = GridLayout(cols=2, spacing=15, size_hint_y=0.6, padding=10)
        buttons = [
            ('📊 وام', 'loan', COLORS['secondary']),
            ('🏦 شبا', 'iban', COLORS['success']),
            ('💱 ارز', 'currency', COLORS['accent']),
            ('📝 چک', 'checks', COLORS['primary']),
            ('👥 مشتری', 'customers', COLORS['secondary']),
            ('📊 گزارش', 'report', COLORS['gold'])
        ]
        for text, screen, color in buttons:
            btn = Button(text=text, font_size='18sp', size_hint_y=None, height=70,
                         background_color=get_color_from_hex(color),
                         color=get_color_from_hex(COLORS['white']), bold=True)
            btn.bind(on_press=lambda x, s=screen: setattr(self.manager, 'current', s))
            menu.add_widget(btn)
        layout.add_widget(menu)

        logout_btn = Button(text='🚪 خروج', font_size='18sp', size_hint_y=0.08,
                            background_color=get_color_from_hex(COLORS['danger']),
                            color=get_color_from_hex(COLORS['white']), bold=True)
        logout_btn.bind(on_press=lambda x: App.get_running_app().stop())
        layout.add_widget(logout_btn)

        self.add_widget(layout)

class LoanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        layout.add_widget(Label(text='📊 ماشین‌حساب وام', font_size='24sp',
                                 color=get_color_from_hex(COLORS['primary']), bold=True))
        layout.add_widget(Label(text='🔧 در حال توسعه...', font_size='18sp'))
        back_btn = Button(text='🔙 بازگشت', size_hint_y=0.1,
                          background_color=get_color_from_hex(COLORS['primary']),
                          color=get_color_from_hex(COLORS['white']))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back_btn)
        self.add_widget(layout)

class IbanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        layout.add_widget(Label(text='🏦 تأیید شبا و کارت', font_size='24sp',
                                 color=get_color_from_hex(COLORS['primary']), bold=True))
        layout.add_widget(Label(text='🔧 در حال توسعه...', font_size='18sp'))
        back_btn = Button(text='🔙 بازگشت', size_hint_y=0.1,
                          background_color=get_color_from_hex(COLORS['primary']),
                          color=get_color_from_hex(COLORS['white']))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back_btn)
        self.add_widget(layout)

class CurrencyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        layout.add_widget(Label(text='💱 مبدل ارز و طلا', font_size='24sp',
                                 color=get_color_from_hex(COLORS['primary']), bold=True))
        layout.add_widget(Label(text='🔧 در حال توسعه...', font_size='18sp'))
        back_btn = Button(text='🔙 بازگشت', size_hint_y=0.1,
                          background_color=get_color_from_hex(COLORS['primary']),
                          color=get_color_from_hex(COLORS['white']))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back_btn)
        self.add_widget(layout)

class ChecksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        layout.add_widget(Label(text='📝 مدیریت چک‌ها', font_size='24sp',
                                 color=get_color_from_hex(COLORS['primary']), bold=True))
        layout.add_widget(Label(text='🔧 در حال توسعه...', font_size='18sp'))
        back_btn = Button(text='🔙 بازگشت', size_hint_y=0.1,
                          background_color=get_color_from_hex(COLORS['primary']),
                          color=get_color_from_hex(COLORS['white']))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back_btn)
        self.add_widget(layout)

class CustomersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        layout.add_widget(Label(text='👥 مدیریت مشتریان', font_size='24sp',
                                 color=get_color_from_hex(COLORS['primary']), bold=True))
        layout.add_widget(Label(text='🔧 در حال توسعه...', font_size='18sp'))
        back_btn = Button(text='🔙 بازگشت', size_hint_y=0.1,
                          background_color=get_color_from_hex(COLORS['primary']),
                          color=get_color_from_hex(COLORS['white']))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back_btn)
        self.add_widget(layout)

class ReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        layout.add_widget(Label(text='📊 گزارش‌ها', font_size='24sp',
                                 color=get_color_from_hex(COLORS['primary']), bold=True))
        layout.add_widget(Label(text='🔧 در حال توسعه...', font_size='18sp'))
        back_btn = Button(text='🔙 بازگشت', size_hint_y=0.1,
                          background_color=get_color_from_hex(COLORS['primary']),
                          color=get_color_from_hex(COLORS['white']))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back_btn)
        self.add_widget(layout)

if __name__ == '__main__':
    BankWalletApp().run()