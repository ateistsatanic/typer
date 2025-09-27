import time
import random
from pynput import keyboard, mouse
from pynput.keyboard import Key, Controller
from pynput.mouse import Button
import pyperclip
from pathlib import Path
import os
import threading
import sys
import pyperclipimg as pci
import win32gui
import win32con
import keyboard as kb_global

kb = Controller()
mouse_listener = None
keyboard_listener = None

running = False
mode = None
wpm = 193
words_list = []  # Основной список слов из messages.txt
words_list_2 = []  # Второй список слов
words_list_3 = []  # Третий список слов
photo_path = None

last_words = []

def on_mouse_click(x, y, button, pressed):
    """Обработка кликов мыши"""
    global running
    
    if not pressed:  # Обрабатываем только отпускание кнопки
        return
    
    if button == Button.x2:  # 5-я кнопка мыши (боковая вперед)
        if not running:
            print("Запуск (5-я кнопка мыши).")
            running = True
            thread = threading.Thread(target=worker, daemon=True)
            thread.start()
        else:
            print("Уже запущено.")
    
    elif button == Button.middle:  # 3-я кнопка мыши (колесо)
        print("Аварийный выход (3-я кнопка мыши).")
        os._exit(0)

def on_key_release(key):
    """Обработка отпускания клавиш"""
    global running
    
    try:
        # Проверяем Tab
        if key == Key.tab:
            if running:
                print("Остановка (Tab).")
                running = False
            else:
                print("Не запущено.")
    except AttributeError:
        pass

def calculate_char_delay(wpm):
    """Рассчитывает задержку между символами на основе WPM"""
    return 60.0 / (wpm * 5)

def type_text(text, wpm):
    """Печатает текст с естественной скоростью"""
    if not text:
        return
    
    char_delay = calculate_char_delay(wpm)
    
    for i, char in enumerate(text):
        kb.press(char)
        kb.release(char)
        
        if i < len(text) - 1:
            current_delay = char_delay * random.uniform(0.9, 1.1)
            time.sleep(max(0.001, current_delay))

def type_word(word, wpm):
    """Печатает слово и нажимает Enter"""
    type_text(word, wpm)
    time.sleep(0.02)
    kb.press(Key.enter)
    kb.release(Key.enter)

def type_words_separately(sentence, wpm):
    """Печатает каждое слово из предложения отдельным сообщением с возможными ошибками"""
    words = sentence.split()
    for word in words:
        if word.strip():  # Проверяем, что слово не пустое
            # 60% вероятность сделать ошибку в слове
            if random.random() < 0.60:
                word_with_errors = add_errors_to_word(word)
                type_word(word_with_errors, wpm)
                print(f"Печать с ошибкой: {word_with_errors} (оригинал: {word})")
            else:
                type_word(word, wpm)
            
            # Случайная пауза между словами
            time.sleep(random.uniform(0.06, 0.03))

def add_errors_to_word(word):
    """Добавляет ошибки в слово с различными типами опечаток (только русские буквы)"""
    print(f"  Обработка слова: '{word}'")
    
    if len(word) <= 1:
        print(f"  Слово слишком короткое, возвращаем оригинал")
        return word
    
    error_type = random.choice(['swap', 'extra', 'missing', 'wrong'])
    print(f"  Выбран тип ошибки: {error_type}")
    
    # Русские буквы для ошибок
    russian_letters = 'абвгджзыц'
    
    if error_type == 'swap' and len(word) >= 3:
        # Поменять две буквы местами
        pos = random.randint(0, len(word) - 2)
        chars = list(word)
        chars[pos], chars[pos + 1] = chars[pos + 1], chars[pos]
        result = ''.join(chars)
        print(f"  Swap: позиция {pos}, '{word}' -> '{result}'")
        return result
    
    elif error_type == 'extra' and len(word) >= 2:
        # Добавить лишнюю букву (русскую)
        pos = random.randint(0, len(word) - 1)
        extra_char = random.choice(russian_letters)
        result = word[:pos] + extra_char + word[pos:]
        print(f"  Extra: позиция {pos}, символ '{extra_char}', '{word}' -> '{result}'")
        return result
    
    elif error_type == 'missing' and len(word) >= 3:
        # Пропустить букву
        pos = random.randint(1, len(word) - 2)
        result = word[:pos] + word[pos + 1:]
        print(f"  Missing: позиция {pos}, '{word}' -> '{result}'")
        return result
    
    elif error_type == 'wrong' and len(word) >= 2:
        # Неправильная буква (русская)
        pos = random.randint(0, len(word) - 1)
        wrong_char = random.choice(russian_letters)
        result = word[:pos] + wrong_char + word[pos + 1:]
        print(f"  Wrong: позиция {pos}, символ '{wrong_char}', '{word}' -> '{result}'")
        return result
    
    # Если не удалось применить ошибку (слишком короткое слово), возвращаем оригинал
    print(f"  Не удалось применить ошибку, возвращаем оригинал")
    return word

def type_random_words_separately():
    """Печатает каждое слово отдельным сообщением с ошибками"""
    words = get_random_words()
    if words and words.strip():
        print(f"Печать слов отдельно: {words}")
        type_words_separately(words, wpm)


def simple_word_error(word):
    """Простая гарантированная ошибка в слове"""
    
    # Выбираем случайную позицию для ошибки
    pos = random.randint(0, len(word) - 1)
    
    # Простые типы ошибок
    error_type = random.choice(['double', 'remove', 'replace'])
    
    if error_type == 'double':
        # Дублируем букву
        return word[:pos] + word[pos] + word[pos:]
    
    elif error_type == 'remove':
        # Удаляем букву
        return word[:pos] + word[pos+1:]
    
    elif error_type == 'replace':
        # Заменяем букву на случайную
        new_char = random.choice('абвдеийклнопрстчш')
        return word[:pos] + new_char + word[pos+1:]
    

def add_errors_to_sentence(sentence):
    """Добавляет ошибки к словам в предложении с разной вероятностью"""
    words = sentence.split()
    result_words = []
    
    for i, word in enumerate(words):
        if i == 0:  # Первое слово - гарантированная ошибка
            messed_word = simple_word_error(word)
            result_words.append(messed_word)
            print(f"Гарантированная ошибка в первом слове: '{word}' -> '{messed_word}'")
        else:  # Остальные слова - 50% шанс
            if random.random() < 0.3:
                messed_word = simple_word_error(word)
                result_words.append(messed_word)
                print(f"Ошибка в слове {i+1}: '{word}' -> '{messed_word}'")
            else:
                result_words.append(word)
                print(f"Без ошибки в слове {i+1}: '{word}'")
    
    return " ".join(result_words)

def type_random_words():
    """Печатает сообщение целиком с ошибками"""
    words = get_random_words()
    if words and words.strip():
        print(f"Исходный текст: {words}")
        
        chance = random.random()
        if chance < 0.75:  # 60% шанс на ошибки
            print("Выпали ошибки! (60% шанс)")
            error_text = add_errors_to_sentence(words)
            print(f"Текст с ошибками: {error_text}")
            type_word(error_text, wpm)
        else:  # 40% шанс без ошибок
            print("Без ошибок (40% шанс)")
            type_word(words, wpm)

def get_random_words():
    """Возвращает случайное количество слов от 1 до 3"""
    global words_list, words_list_2, words_list_3, last_words
    
    # Определяем количество слов (1, 2 или 3)
    word_count = random.randint(1, 3)
    
    # 15% шанс на местоимение "ты"
    use_pronoun = random.random() < 0.1
    
    result_words = []
    words_list_4 = open('messages.txt' ,'r', encoding='utf-8').read().split('\n')
    if use_pronoun:
        # "ты" + случайное слово из основного списка
        if words_list:
            word = random.choice(words_list_4)
            result_words.append(word)
    
    else:
        # Обычный режим
        if word_count == 1 and words_list:
            result_words.append(random.choice(words_list_4))
        
        if word_count >= 2 and words_list_2:
            result_words.append(random.choice(words_list))
            result_words.append(random.choice(words_list_2))
        
        if word_count >= 3 and words_list_3:
            result_words.append(random.choice(words_list_3))
    
    # Если ничего не выбралось, используем слово из основного списка
    if not result_words and words_list:
        result_words.append(random.choice(words_list))
    
    final_text = " ".join(result_words)
    
    # Защита от повторов
    if final_text in last_words:
        # Если текст повторяется, генерируем заново
        return get_random_words()
    
    last_words.append(final_text)
    if len(last_words) > 5:
        last_words.pop(0)
    
    return final_text


def send_photo_with_text():
    global photo_path, wpm
    if not photo_path:
        print("Путь до фото не указан.")
        return
        
    photo_file = Path(photo_path)
    if not photo_file.is_file():
        photo_file = Path(os.getcwd()) / photo_file.name
        if not photo_file.is_file():
            print(f"Фото {photo_path} не найдено.")
            return

    try:
        # Копируем фото
        pci.copy(photo_file)
        # Минимальная задержка для гарантии копирования
        time.sleep(0.05)
        
        # Вставляем фото
        with kb.pressed(Key.ctrl):
            kb.press('v')
            kb.release('v')
        
        # Минимальная задержка перед текстом
        time.sleep(0.05)
        
        # Печатаем текст
        word = get_random_words()
        if word and word.strip():
            type_word(word, wpm)
            
    except Exception as e:
        print(f"Ошибка: {e}")

def worker():
    global running, mode
    while running:
        try:
            if mode == 1:
                type_random_words()  # Сообщение целиком с ошибками
            elif mode == 2:
                send_photo_with_text()
            elif mode == 3:
                type_random_words_separately()  # Каждое слово отдельно с ошибками
            
            # Пауза между сообщениями
            time.sleep(0.001)
        except Exception as e:
            print(f"Ошибка в worker: {e}")
            time.sleep(1)

def load_word_list(filename):
    """Загружает список слов из файла"""
    try:
        if not os.path.exists(filename):
            print(f"Файл {filename} не существует")
            return []
            
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        words = [line.strip() for line in content.split("\n") if line.strip()]
        print(f"Загружено {len(words)} слов из {filename}")
        return words
        
    except Exception as e:
        print(f"Ошибка чтения {filename}: {e}")
        return []

def main():
    global mode, wpm, words_list, words_list_2, words_list_3, photo_path
    global mouse_listener, keyboard_listener
    
    print("=" * 50)
    print("АВТОТАЙПЕР v2.0")
    print("=" * 50)
    
    choice = input("Выберите режим:\n1 - автотайпер из текстовых файлов\n2 - отправка фото и текста\n3 - отправка слов по отдельности\nВведите 1, 2 или 3: ").strip()
    
    if choice == '1':
        mode = 1
        print("Режим: автотайпер (предложения)")
        
    elif choice == '2':
        mode = 2
        print("Режим: отправка фото + текст")
        photo_path = input("Введите полный путь до фото файла: ").strip()
        
    elif choice == '3':
        mode = 3
        print("Режим: отправка слов по отдельности")
        
    else:
        print("Неверный выбор.")
        return
    
    # Загружаем слова из всех файлов
    words_list = load_word_list("messages1.txt")
    words_list_2 = load_word_list("messages2.txt")
    words_list_3 = load_word_list("messages3.txt")
    words_list_4 = load_word_list("messages.txt")
    
    # Проверяем, что есть хотя бы один файл с словами
    if not any([words_list, words_list_2, words_list_3]):
        print("Ошибка: нет загруженных слов! Создайте файлы:")
        print("- messages.txt (обязательный)")
        print("- messages2.txt (опциональный)")
        print("- messages3.txt (опциональный)")
        return

    # Настройка скорости
    try:
        wpm_input = input("Введите скорость печати (40-300, по умолчанию 193): ").strip()
        if wpm_input:
            wpm = max(40, min(int(wpm_input), 300))
        print(f"Скорость печати: {wpm} WPM")
    except:
        wpm = 193
        print("Установлена скорость по умолчанию: 193 WPM")

    # Скрытие консоли
    try:
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    except:
        print("Не удалось скрыть окно (возможно, не Windows)")

    # Запуск слушателей мыши и клавиатуры
    mouse_listener = mouse.Listener(on_click=on_mouse_click)
    keyboard_listener = keyboard.Listener(on_release=on_key_release)
    
    mouse_listener.start()
    keyboard_listener.start()

    print("\n" + "=" * 50)
    print("СКРИПТ ЗАПУЩЕН!")
    print("Управление:")
    print("5-я кнопка мыши (боковая вперед) - Старт")
    print("Tab - Стоп") 
    print("3-я кнопка мыши (колесо) - Аварийный выход")
    print("=" * 50)
    print("Перед началом убедитесь, что:")
    print("1. Активно окно чата/сообщений")
    print("2. Курсор находится в поле ввода")
    print("3. Раскладка клавиатуры - английская")
    print("=" * 50)

    # Ожидание завершения потоков
    try:
        mouse_listener.join()
        keyboard_listener.join()
    except KeyboardInterrupt:
        print("\nЗавершение работы...")
    finally:
        if mouse_listener:
            mouse_listener.stop()
        if keyboard_listener:
            keyboard_listener.stop()

if __name__ == "__main__":
    main()