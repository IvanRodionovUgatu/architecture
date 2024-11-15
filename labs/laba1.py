import ipaddress
import tkinter as tk
from tkinter import messagebox

from getmac import get_mac_address


def calculate_network_parameters() -> None:
    try:
        # Получение IP-адресов из полей ввода
        start_ip = start_ip_entry.get()
        end_ip = end_ip_entry.get()

        # Получение байтов адресов
        begin = ipaddress.IPv4Address(start_ip).packed
        end = ipaddress.IPv4Address(end_ip).packed

        # Вычисление маски
        mask = bytearray(4)
        edge = False
        for i in range(4):
            for b in [128, 64, 32, 16, 8, 4, 2, 1]:
                if not edge and (begin[i] & b) == (end[i] & b):
                    mask[i] |= b
                else:
                    edge = True
                    mask[i] &= ~b

        # Преобразование маски в строку для вывода
        network_mask = ipaddress.IPv4Address(bytes(mask))

        # Расчет адреса сети
        network = ipaddress.IPv4Network(f'{start_ip}/{network_mask}', strict=False)
        network_address = network.network_address
        broadcast_address = network.broadcast_address

        # Получение MAC-адреса устройства
        mac_address = get_mac_address()

        # Вывод результата
        result_label.config(
            text=f'Адрес сети: {network_address}\n'
            f'Broadcast адрес: {broadcast_address}\n'
            f'MAC-адрес устройства: {mac_address}\n'
            f'Маска сети: {network_mask}'
        )
    except ValueError:
        messagebox.showerror('Ошибка', 'Введите корректные IP-адреса.')


# Создание главного окна


root = tk.Tk()
root.title('Network Calculator')

# Метки и поля ввода для начального и конечного IP-адресов
tk.Label(root, text='Начальный IP-адрес:').grid(row=0, column=0, padx=10, pady=5)
start_ip_entry = tk.Entry(root)
start_ip_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text='Конечный IP-адрес:').grid(row=1, column=0, padx=10, pady=5)
end_ip_entry = tk.Entry(root)
end_ip_entry.grid(row=1, column=1, padx=10, pady=5)

# Кнопка для запуска расчета
calculate_button = tk.Button(root, text='Рассчитать', command=calculate_network_parameters)
calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

# Метка для отображения результата
result_label = tk.Label(root, text='', justify='left')
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Запуск основного цикла приложения
root.mainloop()
