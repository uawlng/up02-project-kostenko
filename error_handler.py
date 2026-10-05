from tkinter import messagebox


def safe_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except FileNotFoundError as e:
        messagebox.showerror("Ошибка БД", f"Файл не найден:\n{e}")
    except ConnectionError as e:
        messagebox.showerror("Ошибка соединения", f"Нет подключения:\n{e}")
    except ValueError as e:
        messagebox.showwarning("Некорректные данные", str(e))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Непредвиденная ошибка:\n{e}")
    return None


def validate_positive_int(value, field_name="Значение"):
    try:
        number = int(value)
        if number <= 0:
            return (False, f"{field_name} должно быть больше нуля")
        return (True, number)
    except ValueError:
        return (False, f"{field_name} должно быть целым числом")