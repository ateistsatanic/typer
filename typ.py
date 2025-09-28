from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
import time
import random
import threading

class SimpleTyper:
    def __init__(self):
        self.running = False
        self.wpm = 193
        self.text_to_type = ""
    
    def calculate_char_delay(self, wpm):
        """Рассчитывает задержку между символами"""
        return 60.0 / (wpm * 5)
    
    def type_text(self):
        """Эмуляция печати текста"""
        if not self.text_to_type:
            return
        
        char_delay = self.calculate_char_delay(self.wpm)
        
        # Эмуляция печати
        for i, char in enumerate(self.text_to_type):
            if not self.running:
                break
            time.sleep(max(0.001, char_delay * random.uniform(0.9, 1.1)))
    
    def start_typing(self):
        """Запускает печать"""
        self.running = True
        self.type_text()
        self.running = False
    
    def stop_typing(self):
        """Останавливает печать"""
        self.running = False

class AndroidOverlay(FloatLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app
        
        # Прозрачный фон поверх всего
        self.size_hint = (None, None)
        self.size = (300, 100)
        self.pos_hint = {'top': 0.95, 'right': 0.98}
        
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 0.9)  # Полупрозрачный черный
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
        # Контейнер для контролов
        controls_layout = BoxLayout(orientation='horizontal', padding=10)
        
        self.status_label = Label(
            text='Печатаем...',
            color=(1, 1, 1, 1),
            size_hint_x=0.6
        )
        
        self.stop_btn = Button(
            text='⏹️ СТОП',
            background_color=(0.8, 0, 0, 1),
            size_hint_x=0.4
        )
        self.stop_btn.bind(on_press=self.stop_typing)
        
        controls_layout.add_widget(self.status_label)
        controls_layout.add_widget(self.stop_btn)
        self.add_widget(controls_layout)
        
        # Обновляем позицию прямоугольника при изменении размера
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def stop_typing(self, instance):
        self.main_app.stop_typing()

class TyperApp(App):
    def build(self):
        self.typer = SimpleTyper()
        self.typing_thread = None
        self.overlay = None
        
        # Главный layout
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Заголовок
        title = Label(
            text='ПРОСТОЙ ТАЙПЕР\n(Android Overlay)',
            font_size='24sp',
            bold=True,
            halign='center',
            size_hint_y=0.15
        )
        
        # Поле для WPM
        wpm_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        wpm_layout.add_widget(Label(text='Скорость (WPM):', size_hint_x=0.5))
        self.wpm_input = TextInput(
            text='193',
            multiline=False,
            input_filter='int',
            size_hint_x=0.5
        )
        wpm_layout.add_widget(self.wpm_input)
        
        # Поле для текста
        text_layout = BoxLayout(orientation='vertical', size_hint_y=0.6)
        text_layout.add_widget(Label(text='Текст для печати:', size_hint_y=0.1))
        self.text_input = TextInput(
            text='Привет! Это тестовый текст для тайпера.',
            multiline=True,
            size_hint_y=0.9
        )
        text_layout.add_widget(self.text_input)
        
        # Кнопка старт
        self.start_btn = Button(
            text='🚀 НАЧАТЬ ПЕЧАТАТЬ',
            size_hint_y=0.15,
            background_color=(0, 0.7, 0, 1)
        )
        self.start_btn.bind(on_press=self.start_typing)
        
        # Добавляем все в главный layout
        self.main_layout.add_widget(title)
        self.main_layout.add_widget(wpm_layout)
        self.main_layout.add_widget(text_layout)
        self.main_layout.add_widget(self.start_btn)
        
        return self.main_layout
    
    def start_typing(self, instance):
        """Запускает процесс печати"""
        try:
            # Получаем параметры
            wpm = max(40, min(int(self.wpm_input.text), 300))
            text = self.text_input.text.strip()
            
            if not text:
                return
            
            # Устанавливаем параметры
            self.typer.wpm = wpm
            self.typer.text_to_type = text
            
            # Блокируем UI
            self.start_btn.disabled = True
            self.wpm_input.disabled = True
            self.text_input.disabled = True
            
            # Создаем оверлей
            self.create_overlay()
            
            # Запускаем в отдельном потоке
            self.typing_thread = threading.Thread(target=self.typer.start_typing, daemon=True)
            self.typing_thread.start()
            
            # Проверяем завершение
            Clock.schedule_interval(self.check_typing, 0.1)
            
        except Exception as e:
            print(f'Ошибка: {e}')
    
    def create_overlay(self):
        """Создает overlay"""
        if not self.overlay:
            self.overlay = AndroidOverlay(self)
            Window.add_widget(self.overlay)
    
    def remove_overlay(self):
        """Убирает overlay"""
        if self.overlay:
            Window.remove_widget(self.overlay)
            self.overlay = None
    
    def stop_typing(self, instance=None):
        """Останавливает печать"""
        self.typer.stop_typing()
        self.reset_ui()
    
    def check_typing(self, dt):
        """Проверяет статус печати"""
        if not self.typer.running and self.overlay:
            self.overlay.status_label.text = 'Завершено!'
            Clock.schedule_once(lambda dt: self.reset_ui(), 1.0)
            return False
        return True
    
    def reset_ui(self):
        """Восстанавливает UI"""
        self.remove_overlay()
        self.start_btn.disabled = False
        self.wpm_input.disabled = False
        self.text_input.disabled = False
        Clock.unschedule(self.check_typing)

if __name__ == '__main__':
    TyperApp().run()