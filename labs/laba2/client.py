import socketio
import tkinter as tk
from threading import Thread

# Создаем клиент Socket.IO
sio = socketio.Client()

# Создаем окно tkinter
root = tk.Tk()
root.title("Чат клиент")

# Поле для отображения сообщений
chat_display = tk.Text(root, state='disabled', width=50, height=15)
chat_display.pack(pady=10)

# Поле для ввода сообщений
msg_entry = tk.Entry(root, width=50)
msg_entry.pack(pady=5)

# Кнопка для отправки сообщений
send_button = tk.Button(root, text="Отправить", width=10, command=lambda: send_message())
send_button.pack(pady=5)

# Флаг для отслеживания состояния окна
is_gui_running = True

# Функция для добавления текста в окно чата
def display_message(msg):
    if is_gui_running:  # Проверяем, существует ли интерфейс
        chat_display.config(state='normal')
        chat_display.insert(tk.END, msg + '\n')
        chat_display.config(state='disabled')
        chat_display.see(tk.END)  # Автопрокрутка к последнему сообщению

# Обработчики событий Socket.IO
@sio.event
def connect():
    display_message("Успешное подключение к серверу!")

@sio.event
def disconnect():
    display_message("Отключение от сервера.")

@sio.on('message')
def on_message(data):
    display_message(f"Получено сообщение: {data['msg']}")

# Функция для отправки сообщений
def send_message():
    msg = msg_entry.get()
    if msg:
        sio.emit('chat_message', {'msg': msg})
        display_message(f"Вы: {msg}")
        msg_entry.delete(0, tk.END)

# Подключение к серверу в отдельном потоке
def start_client():
    try:
        sio.connect('http://127.0.0.1:8080')
    except Exception as e:
        display_message(f"Ошибка подключения: {e}")

# Обработчик закрытия окна
def on_close():
    global is_gui_running
    is_gui_running = False  # Флаг для остановки обновлений интерфейса
    sio.disconnect()  # Корректное отключение клиента
    root.destroy()  # Закрытие окна

# Связываем обработчик закрытия окна
root.protocol("WM_DELETE_WINDOW", on_close)

# Запуск клиентского подключения в отдельном потоке, чтобы GUI не блокировался
client_thread = Thread(target=start_client)
client_thread.start()

# Запуск главного цикла интерфейса
root.mainloop()
