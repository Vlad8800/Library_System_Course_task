import tkinter as tk
from tkinter import messagebox
import mysql.connector
from database import get_db_connection
from reader_window import show_reader_window
from register_window import show_register_window
from guest_window import show_guest_window


def show_help():
    messagebox.showinfo(
        "Допомога (F1)",
        "• Enter – увійти\n"
        "• Esc – закрити\n"
        "• F1 – довідка"
    )


def get_reader_id_from_user_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT reader_id FROM Readers WHERE user_id=%s", (user_id,))
        row = cursor.fetchone()
        return row[0] if row else None
    except:
        return None
    finally:
        cursor.close()
        conn.close()


def show_login_window():
    login_window = tk.Toplevel()     
    login_window.title("Вхід в систему")
    login_window.geometry("340x360")
    login_window.configure(bg="#F8F9FA")

    login_window.grab_set()
    login_window.focus_force()

    login_window.bind("<Escape>", lambda e: login_window.destroy())
    login_window.bind("<F1>", lambda e: show_help())

    frame = tk.Frame(login_window, bg="#F8F9FA")
    frame.pack(expand=True)

    tk.Label(frame, text="Логін:", bg="#F8F9FA",
             font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky="e")

    entry_login = tk.Entry(frame, font=("Arial", 11))
    entry_login.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(frame, text="Пароль:", bg="#F8F9FA",
             font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=10, sticky="e")

    entry_password = tk.Entry(frame, show="*", font=("Arial", 11))
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    def forgot_password():
        login = entry_login.get()

        if not login:
            messagebox.showerror("Помилка", "Введіть логін!")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM Users WHERE login=%s", (login,))
            row = cursor.fetchone()
            if row:
                messagebox.showinfo("Ваш пароль", f"Ваш пароль: {row[0]}")
            else:
                messagebox.showerror("Помилка", "Користувача не знайдено.")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))
        finally:
            cursor.close()
            conn.close()

    def login_user():
        login = entry_login.get()
        password = entry_password.get()

        if not login or not password:
            messagebox.showerror("Помилка", "Заповніть всі поля!")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, password, role FROM Users WHERE login=%s",
                (login,)
            )
            row = cursor.fetchone()

            if not row:
                messagebox.showerror("Помилка", "Невірний логін")
                return

            user_id, db_password, role = row

            if db_password != password:
                messagebox.showerror("Помилка", "Невірний пароль")
                return

            if role == "Guest":
                messagebox.showwarning(
                    "Очікує підтвердження",
                    "Ваш обліковий запис ще не підтверджено адміністратором.\n"
                    "Спробуйте пізніше."
                )
                return 
            login_window.destroy()

            if role == "Reader":
                reader_id = get_reader_id_from_user_id(user_id)
                show_reader_window(reader_id)

            elif role == "Admin":
                from admin_window import show_admin_window
                show_admin_window(user_id)

            elif role == "Writer":
                from writer_window import show_writer_window
                show_writer_window(user_id)

            elif role == "Operator":
                from operator_window import show_operator_window
                show_operator_window(user_id)

            elif role == "Librarian":
                from librarian_window import show_librarian_window
                show_librarian_window(user_id)

        except Exception as e:
            messagebox.showerror("Помилка", str(e))
        finally:
            cursor.close()
            conn.close()

    login_btn = tk.Button(frame, text="Увійти", command=login_user,
                          font=("Arial", 12), bg="green", fg="white", width=20)
    login_btn.grid(row=2, column=0, columnspan=2, pady=10)

    tk.Button(frame, text="Забув пароль", command=forgot_password,
              font=("Arial", 10)).grid(row=3, column=0, columnspan=2, pady=5)

    def go_register():
        login_window.destroy()
        show_register_window()

    tk.Label(frame, text="Ще не маєте акаунту?", bg="#F8F9FA",
             font=("Arial", 10)).grid(row=4, column=0, columnspan=2)

    tk.Button(frame, text="Зареєструватися", command=go_register,
              font=("Arial", 10)).grid(row=5, column=0, columnspan=2, pady=5)

    def go_guest():
        login_window.destroy()
        show_guest_window()

    tk.Button(frame, text="Увійти як гість", command=go_guest,
              font=("Arial", 10)).grid(row=6, column=0, columnspan=2, pady=10)

    entry_login.bind("<Return>", lambda e: login_user())
    entry_password.bind("<Return>", lambda e: login_user())
    login_btn.focus_set()
    login_window.mainloop()
