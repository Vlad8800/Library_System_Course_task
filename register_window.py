import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
from database import get_db_connection
from utils import get_reading_rooms
import login_window


def show_register_window():
    window = tk.Toplevel()
    window.title("Реєстрація нового користувача")
    window.geometry("650x750")
    window.configure(bg="#f4f6fb")

    tk.Label(
        window,
        text=" РЕЄСТРАЦІЯ КОРИСТУВАЧА",
        font=("Arial", 22, "bold"),
        fg="#1f3b6f",
        bg="#f4f6fb"
    ).pack(pady=15)

    tk.Label(
        window,
        text="Ваш запит буде надіслано адміністратору для підтвердження.",
        font=("Arial", 11),
        fg="#445",
        bg="#f4f6fb"
    ).pack()

    content = tk.Frame(window, bg="#f4f6fb", padx=30, pady=20)
    content.pack(fill="both", expand=True)

    content.grid_columnconfigure(0, weight=0)
    content.grid_columnconfigure(1, weight=1)
    content.grid_columnconfigure(2, weight=0)

    tk.Label(content, text="Логін:", font=("Arial", 13, "bold"), bg="#f4f6fb",
             anchor="e").grid(row=0, column=0, pady=10, sticky="e")
    login_entry = tk.Entry(content, width=40, font=("Arial", 13))
    login_entry.grid(row=0, column=1, sticky="w")

    tk.Label(content, text="Пароль:", font=("Arial", 13, "bold"), bg="#f4f6fb",
             anchor="e").grid(row=1, column=0, pady=10, sticky="e")
    password_entry = tk.Entry(content, width=40, font=("Arial", 13), show="*")
    password_entry.grid(row=1, column=1, sticky="w")

    def toggle_password():
        if password_entry.cget("show") == "*":
            password_entry.config(show="")
            toggle_btn.config(text="Сховати")
        else:
            password_entry.config(show="*")
            toggle_btn.config(text=" Показати")

    toggle_btn = tk.Button(content, text=" Показати", command=toggle_password)
    toggle_btn.grid(row=1, column=2, padx=10)

    password_warning = tk.Label(
        content,
        text="Пароль має бути не менше 4 символів",
        fg="red",
        bg="#f4f6fb",
        font=("Arial", 9)
    )
    password_warning.grid(row=2, column=1, sticky="w")
    password_warning.grid_remove()

    tk.Label(content, text="Бажана роль:", font=("Arial", 13, "bold"),
             bg="#f4f6fb").grid(row=3, column=0, pady=10, sticky="e")

    role_var = tk.StringVar()
    role_combo = ttk.Combobox(
        content,
        textvariable=role_var,
        state="readonly",
        values=["Reader", "Librarian", "Writer"],
        width=30,
        font=("Arial", 12)
    )
    role_combo.grid(row=3, column=1, sticky="w")

    reader_frame = tk.LabelFrame(
        content,
        text="Дані читача (Reader)",
        bg="#f4f6fb",
        padx=20,
        pady=15,
        font=("Arial", 11, "bold")
    )
    reader_frame.grid(row=5, column=0, columnspan=3, sticky="ew", pady=15)
    reader_frame.grid_columnconfigure(1, weight=1)
    reader_frame.grid_remove()

    tk.Label(reader_frame, text="ПІБ:", bg="#f4f6fb", font=("Arial", 12)).grid(row=0, column=0, sticky="e")
    reader_name_entry = tk.Entry(reader_frame, width=45, font=("Arial", 12))
    reader_name_entry.grid(row=0, column=1, sticky="w")

    tk.Label(reader_frame, text="Адреса:", bg="#f4f6fb", font=("Arial", 12)).grid(row=1, column=0, sticky="e")
    reader_address_entry = tk.Entry(reader_frame, width=45, font=("Arial", 12))
    reader_address_entry.grid(row=1, column=1, sticky="w")

    tk.Label(reader_frame, text="Тип читача:", bg="#f4f6fb", font=("Arial", 12)).grid(row=2, column=0, sticky="e")
    reader_type_var = tk.StringVar()
    reader_type_combo = ttk.Combobox(
        reader_frame,
        textvariable=reader_type_var,
        values=["Студент", "Викладач", "Науковець", "Інше"],
        width=30,
        state="readonly"
    )
    reader_type_combo.grid(row=2, column=1, sticky="w")

    
    student_frame = tk.Frame(reader_frame, bg="#f4f6fb")
    tk.Label(student_frame, text="Університет:", bg="#f4f6fb").grid(row=0, column=0, sticky="e")
    univ_entry = tk.Entry(student_frame, width=45)
    univ_entry.grid(row=0, column=1, sticky="w")

    tk.Label(student_frame, text="Факультет:", bg="#f4f6fb").grid(row=1, column=0, sticky="e")
    faculty_entry = tk.Entry(student_frame, width=45)
    faculty_entry.grid(row=1, column=1, sticky="w")

    student_frame.grid(row=3, column=0, columnspan=2, pady=5)
    student_frame.grid_remove()


    tk.Label(reader_frame, text="Організація:", bg="#f4f6fb").grid(row=4, column=0, sticky="e")
    scient_org_entry = tk.Entry(reader_frame, width=45)
    scient_org_entry.grid(row=4, column=1, sticky="w")
    scient_org_entry.grid_remove()


    librarian_frame = tk.LabelFrame(
        content, text="Дані бібліотекаря (Librarian)",
        bg="#f4f6fb", padx=20, pady=15,
        font=("Arial", 11, "bold")
    )
    librarian_frame.grid(row=6, column=0, columnspan=3, sticky="ew")
    librarian_frame.grid_remove()

    tk.Label(librarian_frame, text="Імʼя:", bg="#f4f6fb", font=("Arial", 12)).grid(row=0, column=0, sticky="e")
    librarian_name_entry = tk.Entry(librarian_frame, width=45, font=("Arial", 12))
    librarian_name_entry.grid(row=0, column=1, sticky="w")

    tk.Label(librarian_frame, text="Читальний зал:", bg="#f4f6fb", font=("Arial", 12)).grid(row=1, column=0, sticky="e")
    reading_room_var = tk.StringVar()
    reading_room_combo = ttk.Combobox(librarian_frame, textvariable=reading_room_var, width=35, state="readonly")
    reading_room_combo.grid(row=1, column=1, sticky="w")

    room_id_map = {}
    try:
        rooms = get_reading_rooms()
        values = []
        for r_id, r_name in rooms:
            label = f"{r_id}: {r_name}"
            values.append(label)
            room_id_map[label] = r_id
        reading_room_combo["values"] = values
    except:
        pass


    writer_frame = tk.LabelFrame(
        content, text="Дані автора (Writer)",
        bg="#f4f6fb", padx=20, pady=15,
        font=("Arial", 11, "bold")
    )
    writer_frame.grid(row=7, column=0, columnspan=3, sticky="ew")
    writer_frame.grid_remove()

    tk.Label(writer_frame, text="Імʼя:", bg="#f4f6fb").grid(row=0, column=0, sticky="e")
    author_name_entry = tk.Entry(writer_frame, width=45)
    author_name_entry.grid(row=0, column=1, sticky="w")

    tk.Label(writer_frame, text="Прізвище:", bg="#f4f6fb").grid(row=1, column=0, sticky="e")
    author_surname_entry = tk.Entry(writer_frame, width=45)
    author_surname_entry.grid(row=1, column=1, sticky="w")

    tk.Label(writer_frame, text="Країна:", bg="#f4f6fb").grid(row=2, column=0, sticky="e")
    author_country_entry = tk.Entry(writer_frame, width=45)
    author_country_entry.grid(row=2, column=1, sticky="w")

    tk.Label(writer_frame, text="Дата народження:", bg="#f4f6fb").grid(row=3, column=0, sticky="e")
    author_birth_date = DateEntry(writer_frame, width=20, date_pattern="yyyy-mm-dd")
    author_birth_date.grid(row=3, column=1, sticky="w")

    def switch_role(*_):
        reader_frame.grid_remove()
        librarian_frame.grid_remove()
        writer_frame.grid_remove()

        role = role_var.get()
        if role == "Reader":
            reader_frame.grid()
        elif role == "Librarian":
            librarian_frame.grid()
        elif role == "Writer":
            writer_frame.grid()

    role_combo.bind("<<ComboboxSelected>>", switch_role)

    def switch_reader_type(*_):
        student_frame.grid_remove()
        scient_org_entry.grid_remove()

        r = reader_type_var.get()
        if r == "Студент":
            student_frame.grid()
        elif r == "Науковець":
            scient_org_entry.grid()

    reader_type_combo.bind("<<ComboboxSelected>>", switch_reader_type)

    def validate():
        login = login_entry.get().strip()
        password = password_entry.get().strip()

        if not login or not password:
            messagebox.showerror("Помилка", "Логін і пароль обовʼязкові!")
            return False

        if len(password) < 4:
            password_warning.grid()
            return False

        if not role_var.get():
            messagebox.showerror("Помилка", "Оберіть роль!")
            return False

        if role_var.get() == "Reader":
            if not reader_name_entry.get().strip():
                messagebox.showerror("Помилка", "Для Reader потрібно ввести ПІБ!")
                return False

        if role_var.get() == "Librarian":
            if not librarian_name_entry.get().strip():
                messagebox.showerror("Помилка", "Введіть імʼя бібліотекаря!")
                return False

            if not reading_room_var.get():
                messagebox.showerror("Помилка", "Оберіть читальний зал!")
                return False

        if role_var.get() == "Writer":
            if not author_name_entry.get().strip() or not author_surname_entry.get().strip():
                messagebox.showerror("Помилка", "Заповніть імʼя та прізвище автора!")
                return False

        return True

    def submit():
        if not validate():
            return

        login = login_entry.get().strip()
        password = password_entry.get().strip()
        role = role_var.get()

        data = {
            "requested_role": role,
            "status": "pending"
        }

        if role == "Reader":
            data.update({
                "name": reader_name_entry.get().strip(),
                "address": reader_address_entry.get().strip(),
                "reader_type": reader_type_var.get(),
                "university": univ_entry.get().strip() or None,
                "faculty": faculty_entry.get().strip() or None,
                "organization": scient_org_entry.get().strip() or None
            })

        elif role == "Librarian":
            data.update({
                "name": librarian_name_entry.get().strip(),
                "reading_room_id": room_id_map.get(reading_room_var.get())
            })

        elif role == "Writer":
            data.update({
                "name": author_name_entry.get().strip(),
                "surname": author_surname_entry.get().strip(),
                "country": author_country_entry.get().strip(),
                "birth_date": author_birth_date.get_date().strftime("%Y-%m-%d")
            })

        data_json = json.dumps(data, ensure_ascii=False)

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Users WHERE login=%s", (login,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Помилка", "Такий логін вже існує!")
                return

            cursor.execute(
                "INSERT INTO Users (login, password, role, usercol) VALUES (%s, %s, 'Guest', %s)",
                (login, password, data_json)
            )

            conn.commit()

            messagebox.showinfo(
                "Успіх!",
                "Ваш запит на реєстрацію відправлено.\n"
                "Очікуйте підтвердження адміністратора."
            )

            window.destroy()
            login_window.show_login_window()

        except Exception as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Помилка", f"Помилка при створенні запиту:\n{e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    btn_frame = tk.Frame(window, bg="#f4f6fb")
    btn_frame.pack(pady=20)

    tk.Button(
        btn_frame,
        text=" Надіслати запит",
        bg="#28a745",
        fg="white",
        font=("Arial", 13, "bold"),
        padx=20, pady=7,
        command=submit
    ).pack(side="left", padx=10)

    tk.Button(
        btn_frame,
        text=" Назад",
        bg="#dc3545",
        fg="white",
        font=("Arial", 12),
        padx=20, pady=7,
        command=lambda: [window.destroy(), login_window.show_login_window()]
    ).pack(side="left", padx=10)

    login_entry.focus_set()
