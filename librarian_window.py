import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from tkcalendar import DateEntry
from datetime import date, timedelta
import mysql.connector
from database import get_db_connection
import json
import login_window
import csv


# ====================== ДОПОМІЖНІ ФУНКЦІЇ ======================

def show_help():
    messagebox.showinfo(
        "Допомога (F1)",
        "Основні гарячі клавіші:\n\n"
        "• Enter: Підтвердити дію, знайти, видати книгу.\n"
        "• Esc: Скасувати дію, закрити поточне вікно (з підтвердженням).\n"
        "• Tab: Перехід до наступного поля.\n"
        "• Shift+Tab: Повернення до попереднього поля.\n"
        "• F1: Виклик цієї довідки."
    )


def setup_keyboard_bindings(window, is_main_window=False):
    """Налаштовує глобальні прив'язки клавіш для вікна"""

    def on_f1(event):
        show_help_window()
        return "break"

    def on_escape(event):
        if isinstance(window, tk.Toplevel):
            window.destroy()
        else:
            if messagebox.askyesno(
                "Підтвердження",
                "Вийти з облікового запису та повернутися до вікна входу?"
            ):
                window.destroy()
                login_window.show_login_window()
        return "break"

    def on_tab(event):
        try:
            event.widget.tk_focusNext().focus()
        except Exception:
            pass
        return "break"

    def on_shift_tab(event):
        try:
            event.widget.tk_focusPrev().focus()
        except Exception:
            pass
        return "break"

    def on_enter(event):
        # Якщо фокус у полі вводу — не чіпаємо Enter
        if isinstance(event.widget, (tk.Entry, ttk.Combobox, tk.Text, tk.Spinbox)):
            return

        # Якщо кнопка в фокусі — натискаємо її
        focus_widget = window.focus_get()
        if isinstance(focus_widget, tk.Button) and focus_widget['state'] == 'normal':
            focus_widget.invoke()
            return "break"

        # Інакше шукаємо "головну" кнопку (OK/Зберегти/Видати)
        for widget in window.winfo_children():
            if isinstance(widget, tk.Button) and widget['state'] == 'normal':
                text_lower = widget['text'].lower()
                if any(keyword in text_lower for keyword in
                       ['ок', 'зберегти', 'так', 'підтвердити', 'додати', 'виконати', 'видати']):
                    widget.invoke()
                    return "break"
        return "break"

    def ignore_unbound_keys(event):
        allowed_keys = [
            'BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down',
            'Home', 'End', 'Insert', 'Page_Up', 'Page_Down'
        ]

        if isinstance(event.widget, (tk.Entry, ttk.Combobox, tk.Text, tk.Spinbox)):
            return

        if event.keysym.startswith('Control') or event.keysym.startswith('Alt'):
            return

        if event.keysym not in allowed_keys:
            return "break"

    window.bind('<F1>', on_f1)
    window.bind('<Escape>', on_escape)
    window.bind('<Tab>', on_tab)
    window.bind('<Shift-Tab>', on_shift_tab)
    window.bind('<Return>', on_enter)
    window.bind('<Key>', ignore_unbound_keys)

    def bind_recursive(widget):
        for child in widget.winfo_children():
            if not isinstance(child, tk.Menu):
                child.bind('<F1>', on_f1)
                child.bind('<Escape>', on_escape)
                child.bind('<Tab>', on_tab)
                child.bind('<Shift-Tab>', on_shift_tab)
                child.bind('<Return>', on_enter)
                child.bind('<Key>', ignore_unbound_keys)
                bind_recursive(child)

    bind_recursive(window)


def show_help_window():
    """Окреме вікно довідки"""
    help_window = tk.Toplevel()
    help_window.title("Довідка")
    help_window.state('zoomed')

    setup_keyboard_bindings(help_window)

    title_label = tk.Label(
        help_window,
        text=" Довідка по клавіатурним комбінаціям",
        font=("Arial", 16, "bold"),
        fg="darkblue"
    )
    title_label.pack(pady=20)

    help_text = """
 ОСНОВНІ КЛАВІШІ УПРАВЛІННЯ:

F1 - Відкрити довідку
ESC - Відміна / Повернення назад / Вихід
TAB - Перехід до наступного поля
Shift + TAB - Повернення до попереднього поля
Enter - Підтвердження / Виконання дії

 ПРИКЛАДИ ВИКОРИСТАННЯ:

• Натисніть TAB для швидкого переміщення між полями форми
• Натисніть ESC для скасування дії або закриття вікна
• Натисніть Enter для підтвердження введених даних
• Використовуйте F1 для отримання довідки у будь-який момент

 ПОРАДИ:

• Більшість кнопок можна активувати клавішею Enter
• Вікна пошуку підтримують швидку навігацію клавішами
• Завжди можна повернутися назад клавішею ESC
    """

    text_widget = tk.Text(
        help_window,
        wrap="word",
        font=("Arial", 12),
        padx=20,
        pady=20,
        bg="#f9f9f9"
    )
    text_widget.insert("1.0", help_text)
    text_widget.config(state="disabled")
    text_widget.pack(fill="both", expand=True, padx=20, pady=10)

    close_btn = tk.Button(
        help_window,
        text="Закрити (ESC)",
        command=help_window.destroy,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=10,
        pady=5
    )
    close_btn.pack(pady=20)

    close_btn.focus_set()


def go_to_login(window_to_close):
    if messagebox.askyesno(
        "Підтвердження виходу",
        "Ви дійсно хочете вийти та повернутися до вікна входу?"
    ):
        from login_window import show_login_window
        window_to_close.destroy()
        show_login_window()


def get_librarian_details_by_user(user_info):
    """
    Повертає (librarian_id, reading_room_id, name) за user_id або login.
    ВАЖЛИВО: librarian_id == user_id (FK).
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    librarian_id_to_find = None

    if isinstance(user_info, int):
        librarian_id_to_find = user_info
    else:
        try:
            cursor.execute(
                "SELECT user_id FROM Users WHERE login = %s AND role = 'librarian'",
                (user_info,)
            )
            result = cursor.fetchone()
            if result:
                librarian_id_to_find = result['user_id']
            else:
                conn.close()
                return None, None, None
        except Exception as e:
            print(f"Помилка пошуку user_id за логіном: {e}")
            conn.close()
            return None, None, None

    if not librarian_id_to_find:
        return None, None, None

    try:
        query = "SELECT librarian_id, reading_room_id, name FROM Librarians WHERE librarian_id = %s"
        cursor.execute(query, (librarian_id_to_find,))
        result = cursor.fetchone()
        conn.close()
        if result:
            user_name = result['name']
            if not isinstance(user_name, str) or user_name.isnumeric():
                user_name = f"Бібліотекар {result['librarian_id']}"
            return result['librarian_id'], result['reading_room_id'], user_name
        else:
            return None, None, None
    except Exception as e:
        print(f"Помилка отримання даних з Librarians: {e}")
        conn.close()
        return None, None, None


def fetch_all_readers(search_query=None):
    """Повертає список (reader_id, login) усіх читачів, з опціональним пошуком."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT user_id, login FROM Users WHERE role = 'reader'"
        params = []
        if search_query:
            query += " AND login LIKE %s"
            params.append(f"%{search_query}%")
        query += " ORDER BY login"
        cursor.execute(query, params)
        readers = cursor.fetchall()
        conn.close()
        return [(reader['user_id'], reader['login']) for reader in readers]
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося завантажити список читачів: {e}")
        return []


def fetch_available_books(room_id, search_query=None):
    """Книги, доступні у конкретному залі (з урахуванням вже виданих примірників)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Додамо відлагоджувальну інформацію
        print(f"Пошук книг для залу: {room_id}, пошук: {search_query}")
        
        query = """
            SELECT 
                b.book_id, 
                b.title, 
                b.access_type,
                b.quantity,
                (SELECT COUNT(*) FROM IssuedBooks ib 
                 WHERE ib.book_id = b.book_id AND ib.returned = FALSE) as borrowed_count,
                (b.quantity - (SELECT COUNT(*) FROM IssuedBooks ib 
                              WHERE ib.book_id = b.book_id AND ib.returned = FALSE)) AS available_quantity
            FROM Books b
            JOIN Placements p ON b.book_id = p.book_id
            WHERE p.room_id = %s 
        """
        params = [room_id]
        if search_query:
            query += " AND b.title LIKE %s"
            params.append(f"%{search_query}%")
        query += " ORDER BY b.title"

        cursor.execute(query, params)
        books = cursor.fetchall()
        conn.close()
        
        # Додамо відлагоджувальну інформацію
        print(f"Знайдено книг: {len(books)}")
        for book in books:
            print(f"  Книга: {book['title']}, доступно: {book['available_quantity']}")
            
        return books
    except Exception as e:
        print(f"Помилка завантаження книг: {e}")
        messagebox.showerror("Помилка", f"Не вдалося завантажити список книг: {e}")
        return []


def log_library_visit(reader_id, librarian_id, room_id, purpose):
    """Логування відвідування бібліотеки (таблиця LibraryVisits)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO LibraryVisits (reader_id, visit_date, librarian_id, room_id, visit_purpose)
            VALUES (%s, %s, %s, %s, %s)
        """, (reader_id, date.today(), librarian_id, room_id, purpose))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Помилка при логуванні відвідування: {e}")


def issue_book_by_librarian(librarian_id, room_id, reader_id, book_id, reading_place, return_date):
    """
    Видача книги бібліотекарем:
      - перевірка, чи вже є активна видача цієї книги цьому читачу;
      - перевірка доступної кількості;
      - вставка в IssuedBooks;
      - log_library_visit(..., 'Взяття книги')
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1) Чи читач вже має цю книгу?
        cursor.execute(
            "SELECT 1 FROM IssuedBooks WHERE reader_id = %s AND book_id = %s AND returned = FALSE",
            (reader_id, book_id)
        )
        if cursor.fetchone():
            messagebox.showinfo("Увага", "Читач вже має активний примірник цієї книги.")
            conn.close()
            return False

        # 2) Чи є доступні примірники?
        cursor.execute("""
            SELECT b.quantity - (
                SELECT COUNT(*) FROM IssuedBooks ib 
                WHERE ib.book_id = b.book_id AND ib.returned = FALSE
            ) AS available 
            FROM Books b 
            WHERE b.book_id = %s
        """, (book_id,))
        result = cursor.fetchone()
        
        if not result or result[0] <= 0:
            messagebox.showinfo("Увага", "Немає доступних примірників. Оновіть список.")
            conn.close()
            return False

        # 3) Запис у IssuedBooks
        cursor.execute("""
            INSERT INTO IssuedBooks 
            (reader_id, book_id, issue_date, return_date, reading_place, room_id, librarian_id, returned)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (reader_id, book_id, date.today(), return_date, reading_place, room_id, librarian_id, False))

        # 4) Лог відвідування
        log_library_visit(reader_id, librarian_id, room_id, 'Взяття книги')

        conn.commit()
        messagebox.showinfo("Успіх", "Книгу успішно видано читачу. Відвідування зафіксовано.")
        return True
        
    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        if err.errno == 1452:
            messagebox.showerror(
                "Помилка зв'язку БД",
                f"Не вдалося видати книгу.\nПомилка FOREIGN KEY.\nДеталі: {err}"
            )
        else:
            messagebox.showerror("Помилка бази даних", f"Не вдалося видати книгу: {err}")
        return False
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Несподівана помилка", f"Сталася помилка: {e}")
        return False
    finally:
        if conn:
            conn.close()


def create_modern_button(parent, text, command,
                         bg_color="#4A90E2", hover_color="#357ABD",
                         text_color="white", width=30, font_size=11):
    """Сучасна кнопка з hover-ефектом"""
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg_color,
        fg=text_color,
        font=("Segoe UI", font_size, "bold"),
        width=width,
        height=2,
        relief="flat",
        cursor="hand2",
        activebackground=hover_color,
        activeforeground=text_color,
        borderwidth=0
    )

    def on_enter(e):
        button.config(bg=hover_color, relief="raised")

    def on_leave(e):
        button.config(bg=bg_color, relief="flat")

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    return button


def get_books():
    """Список усіх книг (book_id, title)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT book_id, title FROM Books ORDER BY title")
    books = cursor.fetchall()
    conn.close()
    return books


def get_reading_rooms():
    """Список читальних залів"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT room_id, name FROM ReadingRooms ORDER BY name")
    rooms = cursor.fetchall()
    conn.close()
    return rooms


def get_publishers():
    """Список видавництв"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT publisher_id, name FROM Publishers ORDER BY name")
    publishers = cursor.fetchall()
    conn.close()
    return publishers


# ====================== РЕДАГУВАННЯ КНИГ ======================

def show_edit_book_window_librarian():
    """Вікно редагування книги для бібліотекаря"""
    edit_window = tk.Toplevel()
    edit_window.title("Редагування книги")
    edit_window.state('zoomed')

    setup_keyboard_bindings(edit_window)

    label_font = ("Arial", 12, "bold")
    entry_font = ("Arial", 12)

    style = ttk.Style()
    style.configure("Large.TCombobox", font=entry_font, padding=5)

    books = get_books()
    book_dict = {f"{title} (ID: {book_id})": book_id for book_id, title in books}
    rooms = get_reading_rooms()
    room_dict = {f"{name} (ID: {room_id})": room_id for room_id, name in rooms}
    publishers = get_publishers()
    publisher_dict = {name: publisher_id for publisher_id, name in publishers}

    tk.Label(
        edit_window,
        text="Редагування книги",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    main_frame = tk.Frame(edit_window, padx=20, pady=10)
    main_frame.pack(expand=True, fill='x', padx=50)
    main_frame.grid_columnconfigure(1, weight=1)

    tk.Label(main_frame, text="Оберіть книгу:", font=label_font).grid(row=0, column=0, sticky="w", pady=8)
    book_combobox = ttk.Combobox(
        main_frame,
        values=list(book_dict.keys()),
        state="readonly",
        style="Large.TCombobox"
    )
    book_combobox.grid(row=0, column=1, pady=8, padx=10, sticky="ew")

    tk.Label(main_frame, text="Тип доступу:", font=label_font).grid(row=1, column=0, sticky="w", pady=8)
    access_type_var = tk.StringVar()
    access_type_combobox = ttk.Combobox(
        main_frame,
        textvariable=access_type_var,
        state='readonly',
        style="Large.TCombobox"
    )
    access_type_combobox['values'] = ["У читальній залі і вдома", "Тільки в читальній залі"]
    access_type_combobox.grid(row=1, column=1, pady=8, padx=10, sticky="ew")

    tk.Label(main_frame, text="Видавництво:", font=label_font).grid(row=2, column=0, sticky="w", pady=8)
    publisher_combobox = ttk.Combobox(
        main_frame,
        values=list(publisher_dict.keys()),
        state="readonly",
        style="Large.TCombobox"
    )
    publisher_combobox.grid(row=2, column=1, pady=8, padx=10, sticky="ew")

    tk.Label(main_frame, text="Оберіть зал:", font=label_font).grid(row=3, column=0, sticky="w", pady=8)
    room_combobox = ttk.Combobox(
        main_frame,
        values=list(room_dict.keys()),
        state="readonly",
        style="Large.TCombobox"
    )
    room_combobox.grid(row=3, column=1, pady=8, padx=10, sticky="ew")

    tk.Label(main_frame, text="Полиця:", font=label_font).grid(row=4, column=0, sticky="w", pady=8)
    shelf_entry = tk.Entry(main_frame, font=entry_font)
    shelf_entry.grid(row=4, column=1, pady=8, padx=10, sticky="ew")

    tk.Label(main_frame, text="Ряд:", font=label_font).grid(row=5, column=0, sticky="w", pady=8)
    row_entry = tk.Entry(main_frame, font=entry_font)
    row_entry.grid(row=5, column=1, pady=8, padx=10, sticky="ew")

    tk.Label(main_frame, text="Кількість примірників:", font=label_font).grid(row=6, column=0, sticky="w", pady=8)
    quantity_entry = tk.Entry(main_frame, font=entry_font)
    quantity_entry.grid(row=6, column=1, pady=8, padx=10, sticky="ew")

    def load_book_info(event):
        selected_key = book_combobox.get()
        if not selected_key:
            return
        book_id = book_dict[selected_key]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT access_type, quantity, publisher_id FROM Books WHERE book_id = %s", (book_id,))
        result = cursor.fetchone()
        if result:
            access_type_combobox.set(result[0])
            quantity_entry.delete(0, tk.END)
            quantity_entry.insert(0, result[1])
            pub_id = result[2]
            for name, pid in publisher_dict.items():
                if pid == pub_id:
                    publisher_combobox.set(name)
                    break
        else:
            access_type_combobox.set("")
            quantity_entry.delete(0, tk.END)
            publisher_combobox.set("")

        cursor.execute("SELECT room_id, shelf, `row` FROM Placements WHERE book_id = %s LIMIT 1", (book_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            room_id = result[0]
            shelf = result[1]
            row_val = result[2]
            for name, rid in room_dict.items():
                if rid == room_id:
                    room_combobox.set(name)
                    break
            shelf_entry.delete(0, tk.END)
            shelf_entry.insert(0, shelf)
            row_entry.delete(0, tk.END)
            row_entry.insert(0, row_val)
        else:
            room_combobox.set("")
            shelf_entry.delete(0, tk.END)
            row_entry.delete(0, tk.END)

    book_combobox.bind("<<ComboboxSelected>>", load_book_info)

    def update_book():
        selected_book = book_combobox.get()
        if not selected_book:
            messagebox.showerror("Помилка", "Оберіть книгу.")
            return

        book_id = book_dict[selected_book]
        access_type = access_type_var.get()
        selected_publisher = publisher_combobox.get()
        selected_room = room_combobox.get()
        shelf = shelf_entry.get()
        row_val = row_entry.get()
        quantity = quantity_entry.get()

        if not all([selected_room, access_type, shelf, row_val, quantity, selected_publisher]):
            messagebox.showerror("Помилка", "Усі поля мають бути заповнені.")
            return

        try:
            quantity = int(quantity)
            if quantity < 0:
                messagebox.showerror("Помилка", "Кількість не може бути менше нуля.")
                return
        except ValueError:
            messagebox.showerror("Помилка", "Кількість повинна бути числом.")
            return

        publisher_id = publisher_dict[selected_publisher]
        room_id = room_dict[selected_room]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE Books SET access_type = %s, quantity = %s, publisher_id = %s WHERE book_id = %s",
                (access_type, quantity, publisher_id, book_id)
            )

            cursor.execute("DELETE FROM Placements WHERE book_id = %s", (book_id,))

            cursor.execute(
                "INSERT INTO Placements (book_id, room_id, shelf, `row`) VALUES (%s, %s, %s, %s)",
                (book_id, room_id, shelf, row_val)
            )

            conn.commit()
            messagebox.showinfo("Успіх", "Інформацію про книгу успішно оновлено!")
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка при оновленні: {str(e)}")
        finally:
            conn.close()

    button_frame = tk.Frame(edit_window)
    button_frame.pack(pady=20)

    update_btn = tk.Button(
        button_frame,
        text="Оновити книгу ",
        command=update_book,
        bg="green",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=10,
        pady=5
    )
    update_btn.pack(side="left", padx=10)

    close_btn = tk.Button(
        button_frame,
        text="Скасувати ",
        command=edit_window.destroy,
        bg="red",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=10,
        pady=5
    )
    close_btn.pack(side="left", padx=10)

    book_combobox.focus_set()


# ====================== СПИСОК ПРОСТРОЧЕНИХ ======================

def fetch_overdue_books(librarian_id=None):
    """Прострочені книги (опціонально по конкретному бібліотекарю)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT ib.issue_id, r.reader_id, r.user_name as reader_name, b.book_id,
                   b.title as book_title, ib.issue_date, ib.return_date,
                   DATEDIFF(CURDATE(), ib.return_date) as days_overdue, ib.reading_place
            FROM IssuedBooks ib
            JOIN Readers r ON ib.reader_id = r.reader_id
            JOIN Books b ON ib.book_id = b.book_id
            WHERE ib.returned = FALSE AND ib.return_date < CURDATE()
        """
        params = []
        if librarian_id:
            query += " AND ib.librarian_id = %s"
            params.append(librarian_id)
        query += " ORDER BY days_overdue DESC"
        cursor.execute(query, params)
        overdue_books = cursor.fetchall()
        conn.close()
        return overdue_books
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося завантажити список прострочених книг: {e}")
        return []


def find_who_has_book():
    """Модальне вікно: хто тримає обрану книгу."""
    search_window = tk.Toplevel()
    search_window.title("Хто взяв книгу")
    search_window.state('zoomed')
    setup_keyboard_bindings(search_window)

    label_font = ("Arial", 14)
    combo_font = ("Arial", 12)
    text_font = ("Arial", 12)
    button_font = ("Arial", 12, "bold")

    main_frame = tk.Frame(search_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    content_frame = tk.Frame(main_frame)
    content_frame.pack(expand=True, fill='x', padx=50)

    books = get_books()
    book_map = {f"{title} (ID: {book_id})": book_id for book_id, title in books}

    tk.Label(content_frame, text="Оберіть книгу:", font=label_font).pack(pady=10)

    style = ttk.Style()
    style.configure("Large.TCombobox", font=combo_font, padding=5)
    book_combo = ttk.Combobox(
        content_frame,
        values=list(book_map.keys()),
        state="readonly",
        style="Large.TCombobox"
    )
    book_combo.pack(pady=5, fill='x', padx=20)

    result_box = tk.Text(content_frame, width=55, height=15, font=text_font)
    result_box.pack(pady=10, fill='both', expand=True, padx=20)

    def search_book():
        selected_book = book_combo.get()
        if not selected_book:
            messagebox.showerror("Помилка", "Оберіть книгу зі списку!")
            return
        book_id = book_map[selected_book]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.user_name, b.title, ib.issue_date, ib.return_date
            FROM IssuedBooks ib
            JOIN Readers r ON ib.reader_id = r.reader_id
            JOIN Books b ON ib.book_id = b.book_id
            WHERE b.book_id = %s
        """, (book_id,))
        results = cursor.fetchall()
        conn.close()
        result_box.delete(1.0, tk.END)
        if results:
            for user_name, title, issue_date, return_date in results:
                if return_date is None:
                    status = "книга зараз у користувача"
                else:
                    if return_date >= date.today():
                        status = f"книга буде повернена {return_date}"
                    else:
                        status = f"мав повернути {return_date}"

                if issue_date == return_date and return_date < date.today():
                    status = f"мав повернути {return_date} (видача в залі)"
                elif issue_date == return_date and return_date == date.today():
                    status = "книга зараз у користувача (в залі до кінця дня)"

                result_box.insert(
                    tk.END,
                    f"• {user_name} — '{title}' (взято {issue_date}) — {status}\n"
                )
        else:
            result_box.insert(
                tk.END,
                "Цю книгу зараз ніхто не тримає, або її ще не видавали.\n"
            )

    button_frame = tk.Frame(content_frame)
    button_frame.pack(pady=20)

    search_btn = tk.Button(
        button_frame,
        text="Перевірити (Enter)",
        command=search_book,
        font=button_font,
        bg="#3498DB",
        fg="white",
        padx=10,
        pady=5
    )
    search_btn.pack(side=tk.LEFT, padx=10)

    close_btn = tk.Button(
        button_frame,
        text="Закрити",
        command=search_window.destroy,
        font=button_font,
        bg="#E74C3C",
        fg="white",
        padx=10,
        pady=5
    )
    close_btn.pack(side=tk.LEFT, padx=10)

    book_combo.focus_set()


def find_books_by_work_or_author():
    """Пошук книг за назвою та автором."""
    search_window = tk.Toplevel()
    search_window.title("Пошук книг за назвою та автором")
    search_window.state('zoomed')
    setup_keyboard_bindings(search_window)

    label_font = ("Arial", 12, "bold")
    entry_font = ("Arial", 12)
    text_font = ("Arial", 11)
    button_font = ("Arial", 12, "bold")

    book_frame = tk.LabelFrame(
        search_window,
        text="Пошук книги за назвою",
        padx=10,
        pady=10,
        font=label_font
    )
    book_frame.pack(fill="x", padx=10, pady=5)
    tk.Label(book_frame, text="Введіть назву книги:", font=entry_font).pack(anchor="w")
    title_entry = tk.Entry(book_frame, width=60, font=entry_font)
    title_entry.pack(pady=5, fill='x', expand=True, padx=5)

    author_frame = tk.LabelFrame(
        search_window,
        text="Пошук всіх книг автора",
        padx=10,
        pady=10,
        font=label_font
    )
    author_frame.pack(fill="x", padx=10, pady=5)
    tk.Label(author_frame, text="Введіть ім'я або прізвище автора:", font=entry_font).pack(anchor="w")
    author_entry = tk.Entry(author_frame, width=60, font=entry_font)
    author_entry.pack(pady=5, fill='x', expand=True, padx=5)

    result_frame = tk.LabelFrame(
        search_window,
        text="Результати пошуку",
        padx=10,
        pady=10,
        font=label_font
    )
    result_frame.pack(fill="both", expand=True, padx=10, pady=5)
    result_box = tk.Text(result_frame, width=85, height=20, wrap=tk.WORD, font=text_font)
    scrollbar = tk.Scrollbar(result_frame, command=result_box.yview)
    result_box.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    result_box.pack(fill="both", expand=True, padx=5, pady=5)

    def search_by_title():
        title_query = title_entry.get().strip()
        if not title_query:
            messagebox.showerror("Помилка", "Введіть назву книги!")
            return
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT b.book_id, b.title, CONCAT(a.name, ' ', a.surname) AS author, 
                       b.access_type, b.inventory_number, b.quantity,
                       (SELECT COUNT(*) FROM IssuedBooks ib 
                        WHERE ib.book_id = b.book_id AND ib.returned = FALSE) as borrowed_count
                FROM Books b
                JOIN Authors a ON b.author_id = a.author_id
                WHERE b.title LIKE %s
            """, (f"%{title_query}%",))
            books = cursor.fetchall()
            result_box.delete(1.0, tk.END)
            if not books:
                result_box.insert(tk.END, f"📭 Книг з назвою '{title_query}' не знайдено.\n")
                return
            result_box.insert(
                tk.END,
                f"Знайдено книг за назвою '{title_query}': {len(books)}\n\n"
            )
            for book_id, title, author, access_type, inventory_number, quantity, borrowed_count in books:
                available = quantity - borrowed_count
                result_box.insert(tk.END, f" '{title}'\n")
                result_box.insert(tk.END, f" Автор: {author}\n")
                result_box.insert(tk.END, f" Інвентарний номер: {inventory_number}\n")
                result_box.insert(tk.END, f" Доступ: {access_type}\n")
                result_box.insert(tk.END, f" Доступно: {available} з {quantity}\n")
                result_box.insert(tk.END, f" ID книги: {book_id}\n\n")
        except Exception as e:
            messagebox.showerror("Помилка", f"Сталася помилка при пошуку:\n{e}")
        finally:
            conn.close()

    def search_by_author():
        author_query = author_entry.get().strip()
        if not author_query:
            messagebox.showerror("Помилка", "Введіть ім'я або прізвище автора!")
            return
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT b.book_id, b.title, CONCAT(a.name, ' ', a.surname) AS author, 
                       b.access_type, b.inventory_number, b.quantity,
                       (SELECT COUNT(*) FROM IssuedBooks ib 
                        WHERE ib.book_id = b.book_id AND ib.returned = FALSE) as borrowed_count
                FROM Books b
                JOIN Authors a ON b.author_id = a.author_id
                WHERE a.name LIKE %s OR a.surname LIKE %s
                ORDER BY b.title
            """, (f"%{author_query}%", f"%{author_query}%"))
            books = cursor.fetchall()
            result_box.delete(1.0, tk.END)
            if not books:
                result_box.insert(tk.END, f"📭 Книг автора '{author_query}' не знайдено.\n")
                return
            result_box.insert(
                tk.END,
                f"Всі книги автора '{author_query}': {len(books)}\n\n"
            )
            for book_id, title, author, access_type, inventory_number, quantity, borrowed_count in books:
                available = quantity - borrowed_count
                result_box.insert(tk.END, f"'{title}'\n")
                result_box.insert(tk.END, f"Автор: {author}\n")
                result_box.insert(tk.END, f"Інвентарний номер: {inventory_number}\n")
                result_box.insert(tk.END, f"Доступ: {access_type}\n")
                result_box.insert(tk.END, f"Доступно: {available} з {quantity}\n")
                result_box.insert(tk.END, f"ID книги: {book_id}\n\n")
        except Exception as e:
            messagebox.showerror("Помилка", f"Сталася помилка при пошуку:\n{e}")
        finally:
            conn.close()

    button_frame = tk.Frame(search_window)
    button_frame.pack(pady=10)

    search_title_btn = tk.Button(
        button_frame,
        text="Пошук за назвою (Enter)",
        command=search_by_title,
        bg="blue",
        fg="white",
        font=button_font,
        padx=10,
        pady=5
    )
    search_title_btn.pack(side="left", padx=5)

    search_author_btn = tk.Button(
        button_frame,
        text="Пошук книг автора ",
        command=search_by_author,
        bg="green",
        fg="white",
        font=button_font,
        padx=10,
        pady=5
    )
    search_author_btn.pack(side="left", padx=5)

    def clear_results():
        result_box.delete(1.0, tk.END)
        title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)

    clear_btn = tk.Button(
        button_frame,
        text="Очистити",
        command=clear_results,
        bg="gray",
        fg="white",
        font=button_font,
        padx=10,
        pady=5
    )
    clear_btn.pack(side="left", padx=5)

    close_btn = tk.Button(
        button_frame,
        text="Закрити",
        command=search_window.destroy,
        bg="red",
        fg="white",
        font=button_font,
        padx=10,
        pady=5
    )
    close_btn.pack(side="left", padx=5)

    title_entry.focus_set()


def manage_book_quantity(book_id, new_quantity, room_id):
    """Оновлення кількості примірників (з перевіркою на видані)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) as borrowed_count FROM IssuedBooks "
            "WHERE book_id = %s AND returned = FALSE",
            (book_id,)
        )
        borrowed_count = cursor.fetchone()[0]
        if new_quantity < borrowed_count:
            messagebox.showerror(
                "Помилка",
                f"Не можна встановити кількість менше за кількість виданих книг ({borrowed_count})"
            )
            conn.close()
            return False
        cursor.execute("UPDATE Books SET quantity = %s WHERE book_id = %s", (new_quantity, book_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Успіх", "Кількість примірників успішно оновлено")
        return True
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося оновити кількість примірників: {e}")
        return False


def fetch_all_overdue_books():
    """АДМІН: Отримати всі просрочені книги в системі."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ib.issue_id, r.reader_id, r.user_name as reader_name,
               b.book_id, b.title, c.name as category, 
               ib.issue_date, ib.return_date, ib.reading_place,
               DATEDIFF(CURDATE(), ib.return_date) as days_overdue,
               rr.name as room_name, l.name as librarian_name
        FROM IssuedBooks ib
        JOIN Readers r ON ib.reader_id = r.reader_id
        JOIN Books b ON b.book_id = ib.book_id
        LEFT JOIN Categories c ON b.category_id = c.category_id
        LEFT JOIN ReadingRooms rr ON ib.room_id = rr.room_id
        LEFT JOIN Librarians l ON ib.librarian_id = l.librarian_id
        WHERE ib.return_date < CURDATE() AND ib.returned = FALSE
        ORDER BY DATEDIFF(CURDATE(), ib.return_date) DESC, ib.return_date ASC
    """)
    result = cursor.fetchall()
    conn.close()
    return result


def show_admin_overdue_books():
    """АДМІН: Fluent UI — перегляд всіх просрочених книг."""

    overdue_window = tk.Toplevel()
    overdue_window.title("АДМІН: Просрочені книги")
    overdue_window.state('zoomed')
    overdue_window.resizable(True, True)
    overdue_window.configure(bg="#F0F2F5")
    overdue_window.grab_set()

    setup_keyboard_bindings(overdue_window)

    header = tk.Frame(overdue_window, bg="#1F4E79", height=85)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Просрочені книги",
        fg="white",
        bg="#1F4E79",
        font=("Segoe UI", 28, "bold")
    ).pack(pady=18)

    canvas = tk.Canvas(overdue_window, bg="#F0F2F5", highlightthickness=0)
    scrollbar = ttk.Scrollbar(overdue_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    content = tk.Frame(canvas, bg="#F0F2F5")
    canvas.create_window((0, 0), window=content, anchor="nw")

    def on_resize(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content.bind("<Configure>", on_resize)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def refresh_overdue_data():
        for w in content.winfo_children():
            w.destroy()

        overdue_books = fetch_all_overdue_books()

        if not overdue_books:
            tk.Label(
                content,
                text="Всі книги повернені вчасно!",
                bg="#F0F2F5",
                fg="green",
                font=("Segoe UI", 20, "bold")
            ).pack(pady=100)
            return

        stats = tk.Frame(content, bg="white", bd=1, relief="solid")
        stats.pack(fill="x", padx=25, pady=20)
        stats.configure(highlightbackground="#D0D0D0")

        total = len(overdue_books)
        critical = len([b for b in overdue_books if b[9] > 30])

        tk.Label(
            stats,
            text=f"Загалом просрочених: {total}    |    Критичних (>30 днів): {critical}",
            bg="white",
            fg="#1F4E79",
            font=("Segoe UI", 15, "bold")
        ).pack(pady=12)

        header_row = tk.Frame(content, bg="#233243")
        header_row.pack(fill="x", padx=25)

        def head(text, width):
            tk.Label(
                header_row,
                text=text,
                fg="white",
                bg="#233243",
                font=("Segoe UI", 11, "bold"),
                width=width,
                anchor="w",
                padx=6
            ).pack(side="left")

        head("Читач", 20)
        head("Книга", 40)
        head("Взято", 12)
        head("Повернути до", 15)
        head("Просрочено", 15)
        head("Місце", 18)

        for (
            issue_id, reader_id, reader_name, book_id, title, category,
            issue_date, return_date, place, days_overdue, room_name, librarian_name
        ) in overdue_books:

            if days_overdue > 30:
                bg = "#FFCDD2"
                fg = "#C62828"
                emoji = "🔴"
            elif days_overdue > 14:
                bg = "#FFE0B2"
                fg = "#EF6C00"
                emoji = "🟠"
            elif days_overdue > 7:
                bg = "#FFF9C4"
                fg = "#F9A825"
                emoji = "🟡"
            else:
                bg = "#FFE6E6"
                fg = "#B71C1C"
                emoji = "🟢"

            row = tk.Frame(content, bg=bg, bd=1, relief="solid")
            row.pack(fill="x", padx=25, pady=2)

            def cell(text, width, color="black", bold=False):
                font_style = ("Segoe UI", 10, "bold") if bold else ("Segoe UI", 10)
                tk.Label(
                    row,
                    text=text,
                    bg=bg,
                    fg=color,
                    font=font_style,
                    width=width,
                    anchor="w",
                    padx=6
                ).pack(side="left")

            cell(reader_name[:22], 20)
            cell(title[:45], 40)
            cell(str(issue_date), 12)
            cell(str(return_date), 15)
            cell(f"{emoji} {days_overdue} дн.", 15, fg, True)
            cell(place[:22], 18)

    refresh_btn = tk.Button(
        overdue_window,
        text="Оновити список",
        command=refresh_overdue_data,
        bg="#0078D4",
        fg="white",
        font=("Segoe UI", 13, "bold"),
        padx=20,
        pady=7
    )
    refresh_btn.pack(pady=10)

    close_btn = tk.Button(
        overdue_window,
        text="Закрити",
        command=overdue_window.destroy,
        bg="#C62828",
        fg="white",
        font=("Segoe UI", 13, "bold"),
        padx=20,
        pady=7
    )
    close_btn.pack(pady=5)

    refresh_overdue_data()


# ====================== SQL EDITOR ======================

def create_styled_combobox(parent, values, width=40):
    style = ttk.Style()
    style.theme_use('clam')
    style.configure(
        'Custom.TCombobox',
        fieldbackground='white',
        background='#E8F4FD',
        bordercolor='#4A90E2',
        arrowcolor='#4A90E2',
        focuscolor='#4A90E2'
    )

    combo = ttk.Combobox(
        parent,
        values=values,
        state="readonly",
        width=width,
        style='Custom.TCombobox',
        font=("Segoe UI", 10)
    )
    return combo


def create_section(parent, title, icon="📚"):
    section_frame = tk.Frame(parent, bg="white", relief="solid", borderwidth=1)

    title_frame = tk.Frame(section_frame, bg="#34495E", height=40)
    title_frame.pack(fill="x")
    title_frame.pack_propagate(False)

    title_label = tk.Label(
        title_frame,
        text=f"{icon} {title}",
        font=("Segoe UI", 14, "bold"),
        bg="#34495E",
        fg="white"
    )
    title_label.pack(pady=8)

    content_frame = tk.Frame(section_frame, bg="white", padx=20, pady=15)
    content_frame.pack(fill="both", expand=True)

    return section_frame, content_frame


def show_sql_editor_window():
    sql_window = tk.Toplevel()
    sql_window.title("SQL Query Editor")
    sql_window.state('zoomed')
    setup_keyboard_bindings(sql_window)

    sql_section_frame, sql_section_content = create_section(sql_window, "SQL Query Editor", "💻")
    sql_section_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(
        sql_section_content,
        text="Введіть SQL запит:",
        font=("Segoe UI", 12, "bold"),
        bg="white",
        fg="#2C3E50"
    ).pack(anchor="w", pady=(0, 5))

    sql_text_frame = tk.Frame(sql_section_content)
    sql_text_frame.pack(fill="both", expand=True, pady=(0, 10))

    sql_scrollbar = ttk.Scrollbar(sql_text_frame, orient="vertical")
    sql_text = tk.Text(
        sql_text_frame,
        height=15,
        width=70,
        font=("Consolas", 12),
        wrap=tk.WORD,
        bg="#1E1E1E",
        fg="#FFFFFF",
        insertbackground="white",
        yscrollcommand=sql_scrollbar.set
    )
    sql_scrollbar.config(command=sql_text.yview)
    sql_scrollbar.pack(side="right", fill="y")
    sql_text.pack(side="left", fill="both", expand=True)

    sql_buttons_frame = tk.Frame(sql_section_content, bg="white")
    sql_buttons_frame.pack(fill="x", pady=10)
    sql_buttons_frame.grid_columnconfigure(0, weight=1)
    sql_buttons_frame.grid_columnconfigure(1, weight=1)
    sql_buttons_frame.grid_columnconfigure(2, weight=1)

    def execute_sql():
        query = sql_text.get("1.0", tk.END).strip()
        if not query:
            messagebox.showwarning("Попередження", "Запит не може бути порожнім", parent=sql_window)
            return
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            if query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                conn.close()
                show_sql_results(query, columns, results)
            else:
                conn.commit()
                affected_rows = cursor.rowcount
                conn.close()
                messagebox.showinfo(
                    "Успіх",
                    f"Запит виконано успішно.\nОброблено рядків: {affected_rows}",
                    parent=sql_window
                )
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            messagebox.showerror("Помилка SQL", f"Сталася помилка:\n{e}", parent=sql_window)

    def clear_sql():
        sql_text.delete("1.0", tk.END)

    def insert_select_example():
        example_query = """SELECT 
    b.book_id,
    b.title AS 'Назва книги',
    CONCAT(a.name, ' ', a.surname) AS 'Автор',
    b.access_type AS 'Тип доступу',
    b.quantity AS 'Кількість',
    b.inventory_number AS 'Інвентарний номер',
    c.name AS 'Категорія',
    p.name AS 'Видавництво',
    b.borrowed_count AS 'Кількість видач'
FROM Books b
LEFT JOIN Authors a ON b.author_id = a.author_id
LEFT JOIN Categories c ON b.category_id = c.category_id
LEFT JOIN Publishers p ON b.publisher_id = p.publisher_id
ORDER BY b.title;"""
        sql_text.delete("1.0", tk.END)
        sql_text.insert("1.0", example_query)

    def show_sql_results(query, columns, results):
        results_window = tk.Toplevel(sql_window)
        results_window.title("Результати SQL запиту")
        results_window.state('zoomed')
        setup_keyboard_bindings(results_window)

        tk.Label(
            results_window,
            text="Результати для запиту:",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=5)
        tk.Label(
            results_window,
            text=query,
            font=("Consolas", 10),
            fg="gray",
            wraplength=850
        ).pack(pady=(0, 10))

        stats_label = tk.Label(
            results_window,
            text=f"Знайдено рядків: {len(results)} | Колонок: {len(columns)}",
            font=("Segoe UI", 12, "bold")
        )
        stats_label.pack(pady=5)

        table_frame = tk.Frame(results_window)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 11), rowheight=25)
        style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"))

        tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Custom.Treeview")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.W)
        for row in results:
            tree.insert("", "end", values=row)

        v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        tree.pack(side="left", fill="both", expand=True)

        def export_to_csv():
            try:
                from tkinter import filedialog
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                    title="Зберегти SQL результат як CSV"
                )
                if not file_path:
                    return
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(columns)
                    writer.writerows(results)
                messagebox.showinfo("Успіх", f"Дані успішно експортовано в {file_path}", parent=results_window)
            except Exception as e:
                messagebox.showerror("Помилка експорту", f"Не вдалося зберегти файл: {e}", parent=results_window)

        export_btn = tk.Button(
            results_window,
            text="Експорт в CSV",
            command=export_to_csv,
            bg="green",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=5
        )
        export_btn.pack(pady=20)

    create_modern_button(
        sql_buttons_frame,
        "Виконати запит (Enter)",
        execute_sql,
        bg_color="#27AE60",
        hover_color="#229954",
        width=20,
        font_size=12
    ).grid(row=0, column=0, sticky="ew", padx=5, pady=5)

    create_modern_button(
        sql_buttons_frame,
        " Очистити",
        clear_sql,
        bg_color="#E74C3C",
        hover_color="#C0392B",
        width=15,
        font_size=12
    ).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    create_modern_button(
        sql_buttons_frame,
        "Приклад SELECT книг",
        insert_select_example,
        bg_color="#3498DB",
        hover_color="#2980B9",
        width=20,
        font_size=12
    ).grid(row=0, column=2, sticky="ew", padx=5, pady=5)

    sql_window.bind('<Return>', lambda e: execute_sql() if sql_text.focus_get() else None)
    sql_text.focus_set()


# ====================== ПОВЕРНЕННЯ КНИГ (ВСІ ЧИТАЧІ) ======================

def fetch_all_active_issued_books(search_reader=None, only_overdue=False):
    """Всі активні видачі (returned = FALSE), з фільтрами."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT ib.issue_id,
               r.reader_id,
               r.user_name AS reader_name,
               b.book_id,
               b.title,
               c.name AS category,
               ib.issue_date,
               ib.return_date,
               ib.reading_place,
               DATEDIFF(CURDATE(), ib.return_date) AS days_overdue,
               rr.name AS room_name
        FROM IssuedBooks ib
        JOIN Readers r ON ib.reader_id = r.reader_id
        JOIN Books b ON b.book_id = ib.book_id
        LEFT JOIN Categories c ON b.category_id = c.category_id
        LEFT JOIN ReadingRooms rr ON ib.room_id = rr.room_id
        WHERE ib.returned = FALSE
    """
    params = []

    if only_overdue:
        query += " AND ib.return_date < CURDATE()"

    if search_reader:
        query += " AND r.user_name LIKE %s"
        params.append(f"%{search_reader}%")

    query += " ORDER BY r.user_name, ib.return_date ASC"

    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result


def return_book_by_librarian(issue_id, reader_id, librarian_id, room_id, parent=None):
    """Повернення книги бібліотекарем для конкретного issue_id/reader_id."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT returned FROM IssuedBooks 
            WHERE issue_id = %s AND reader_id = %s
        """, (issue_id, reader_id))
        row = cursor.fetchone()

        if not row:
            messagebox.showerror("Помилка", "Запис видачі книги не знайдено.", parent=parent)
            conn.close()
            return False

        if row[0]:
            messagebox.showinfo("Інформація", "Книга вже повернена.", parent=parent)
            conn.close()
            return False

        cursor.execute("""
            UPDATE IssuedBooks
            SET returned = TRUE, actual_return_date = %s
            WHERE issue_id = %s
        """, (date.today(), issue_id))

        conn.commit()
        conn.close()

        log_library_visit(reader_id, librarian_id, room_id, 'Повернення книги')

        messagebox.showinfo("Успіх", "Книга успішно повернена. Відвідування зафіксовано.", parent=parent)
        return True

    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        messagebox.showerror("Помилка", f"Не вдалося повернути книгу: {e}", parent=parent)
        return False


def show_all_returns_window(librarian_id, room_id):
    """Вікно для бібліотекаря: повернення книг всіх читачів."""
    win = tk.Toplevel()
    win.title("Повернення книг читачів")
    win.state('zoomed')
    win.configure(bg="#F0F2F5")
    win.grab_set()

    setup_keyboard_bindings(win)

    header = tk.Frame(win, bg="#1F4E79", height=80)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Повернення книг читачів",
        fg="white",
        bg="#1F4E79",
        font=("Segoe UI", 24, "bold")
    ).pack(pady=18)

    controls_frame = tk.Frame(win, bg="#F0F2F5")
    controls_frame.pack(fill="x", padx=20, pady=(10, 5))

    tk.Label(
        controls_frame,
        text="Пошук читача (ПІБ):",
        bg="#F0F2F5",
        font=("Segoe UI", 11)
    ).pack(side="left", padx=(0, 5))

    search_var = tk.StringVar()
    search_entry = tk.Entry(
        controls_frame,
        textvariable=search_var,
        width=30,
        font=("Segoe UI", 11)
    )
    search_entry.pack(side="left", padx=(0, 15))

    only_overdue_var = tk.BooleanVar(value=False)
    overdue_check = tk.Checkbutton(
        controls_frame,
        text="Лише прострочені",
        variable=only_overdue_var,
        bg="#F0F2F5",
        font=("Segoe UI", 11)
    )
    overdue_check.pack(side="left", padx=(0, 15))

    list_frame = tk.Frame(win, bg="#F0F2F5")
    list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    style = ttk.Style()
    style.configure("Return.Treeview", font=("Arial", 11), rowheight=26)
    style.configure("Return.Treeview.Heading", font=("Arial", 12, "bold"))

    columns = ('reader', 'book', 'issue_date', 'return_date', 'status', 'place', 'room')
    tree = ttk.Treeview(
        list_frame,
        columns=columns,
        show='headings',
        style="Return.Treeview"
    )

    tree.heading('reader', text='Читач')
    tree.heading('book', text='Книга')
    tree.heading('issue_date', text='Взято')
    tree.heading('return_date', text='Повернути до')
    tree.heading('status', text='Статус')
    tree.heading('place', text='Місце')
    tree.heading('room', text='Зал')

    tree.column('reader', width=180, anchor=tk.W, stretch=True)
    tree.column('book', width=260, anchor=tk.W, stretch=True)
    tree.column('issue_date', width=110, anchor=tk.W, stretch=False)
    tree.column('return_date', width=120, anchor=tk.W, stretch=False)
    tree.column('status', width=150, anchor=tk.W, stretch=False)
    tree.column('place', width=150, anchor=tk.W, stretch=False)
    tree.column('room', width=150, anchor=tk.W, stretch=False)

    v_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=v_scroll.set)
    v_scroll.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    tree.tag_configure("overdue", background="#FFE0E0", foreground="#B71C1C")
    tree.tag_configure("active", background="#FFFFFF")

    row_map = {}

    def refresh_list(event=None):
        for item in tree.get_children():
            tree.delete(item)
        row_map.clear()

        search_text = search_var.get().strip()
        only_overdue = only_overdue_var.get()

        rows = fetch_all_active_issued_books(
            search_reader=search_text if search_text else None,
            only_overdue=only_overdue
        )

        if not rows:
            return

        for (
            issue_id,
            reader_id,
            reader_name,
            book_id,
            title,
            category,
            issue_date,
            return_date,
            reading_place,
            days_overdue,
            room_name
        ) in rows:

            is_overdue = days_overdue is not None and days_overdue > 0

            if is_overdue:
                status = f"Просрочена ({days_overdue} дн.)"
                tag = "overdue"
            else:
                status = "Активна"
                tag = "active"

            item_id = tree.insert(
                "",
                "end",
                values=(
                    reader_name,
                    title,
                    str(issue_date),
                    str(return_date),
                    status,
                    reading_place,
                    room_name if room_name else ""
                ),
                tags=(tag,)
            )

            row_map[item_id] = {
                "issue_id": issue_id,
                "reader_id": reader_id
            }

    def perform_return(event=None):
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Увага", "Оберіть запис з таблиці.")
            return

        info = row_map.get(selected)
        if not info:
            messagebox.showerror("Помилка", "Не вдалося знайти дані для цього рядка.")
            return

        if not messagebox.askyesno(
            "Підтвердження",
            "Ви дійсно хочете повернути цю книгу?"
        ):
            return

        ok = return_book_by_librarian(
            info["issue_id"],
            info["reader_id"],
            librarian_id,
            room_id,
            parent=win
        )
        if ok:
            refresh_list()

    buttons_frame = tk.Frame(win, bg="#F0F2F5")
    buttons_frame.pack(fill="x", padx=20, pady=(0, 10))

    return_btn = tk.Button(
        buttons_frame,
        text="Повернути обрану книгу",
        command=perform_return,
        bg="#27AE60",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        padx=15,
        pady=5
    )
    return_btn.pack(side="left", padx=(0, 10))

    refresh_btn = tk.Button(
        buttons_frame,
        text="Оновити список",
        command=refresh_list,
        bg="#2980B9",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        padx=15,
        pady=5
    )
    refresh_btn.pack(side="left", padx=(0, 10))

    close_btn = tk.Button(
        buttons_frame,
        text="Закрити",
        command=win.destroy,
        bg="#C0392B",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        padx=15,
        pady=5
    )
    close_btn.pack(side="right")

    search_entry.bind('<Return>', refresh_list)
    tree.bind('<Double-1>', perform_return)

    info_label = tk.Label(
        win,
        text="Порада: двічі клацніть по рядку, щоб швидко повернути книгу.",
        bg="#F0F2F5",
        fg="gray",
        font=("Segoe UI", 10, "italic")
    )
    info_label.pack(side="bottom", pady=(0, 5))

    refresh_list()
    search_entry.focus_set()


# ====================== ГОЛОВНЕ ВІКНО БІБЛІОТЕКАРЯ ======================

def show_librarian_window(user):
    """
    Головне вікно бібліотекаря:
      - пошук/видача книг
      - пошук, хто тримає книгу
      - SQL Editor
      - перегляд прострочених
      - повернення книг
      - статистика залу
    """
    librarian_id, room_id, librarian_name = get_librarian_details_by_user(user)

    if not librarian_id:
        user_str = user if isinstance(user, str) else f"user_id {user}"
        messagebox.showerror(
            "Помилка доступу",
            f"Не вдалося ідентифікувати вас як бібліотекаря.\n\n"
            f"Причина: Обліковий запис '{user_str}' (роль 'librarian') не має "
            f"пов'язаного запису в таблиці `Librarians`.\n\n"
            f"Рішення: Переконайтесь, що в таблиці `Librarians` є запис, "
            f"де `librarian_id` дорівнює `user_id` вашого користувача."
        )
        return

    librarian_window = tk.Tk()
    librarian_window.title(f"Панель бібліотекаря: {librarian_name} (Зал: {room_id})")

    librarian_window.state('zoomed')
    librarian_window.resizable(True, True)
    librarian_window.configure(bg="#f0f0f0")

    setup_keyboard_bindings(librarian_window, is_main_window=True)

    # Додамо відлагоджувальну інформацію
    print(f"=== ІНФОРМАЦІЯ ПРО БІБЛІОТЕКАРЯ ===")
    print(f"Бібліотекар ID: {librarian_id}")
    print(f"Зал ID: {room_id}")
    print(f"Ім'я: {librarian_name}")

    # ---------- Верхній заголовок ----------
    top_frame = tk.Frame(librarian_window, pady=15, bg="#2C3E50")
    top_frame.pack(fill=tk.X, padx=0)

    tk.Label(
        top_frame,
        text=f"Вітаємо, {librarian_name}!",
        font=("Arial", 18, "bold"),
        bg="#2C3E50",
        fg="white"
    ).pack(side=tk.LEFT, padx=20)

    tk.Label(
        top_frame,
        text=f"Читальний зал: {room_id}",
        font=("Arial", 12),
        bg="#2C3E50",
        fg="#BDC3C7"
    ).pack(side=tk.LEFT, padx=10)

    exit_btn = tk.Button(
        top_frame,
        text="Вийти",
        font=("Arial", 12, "bold"),
        command=lambda: go_to_login(librarian_window),
        bg="#E74C3C",
        fg="white",
        relief="flat",
        padx=10,
        pady=5
    )
    exit_btn.pack(side=tk.RIGHT, padx=20)

    # ---------- Основний фрейм (зліва видача, справа інструменти) ----------
    main_frame = tk.Frame(librarian_window, bg="#f0f0f0", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # ЛІВА ЧАСТИНА: пошук та видача книг
    left_frame = tk.Frame(main_frame, bg="#f0f0f0")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

    tk.Label(
        left_frame,
        text="Видача книг",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0"
    ).pack(anchor=tk.W, pady=(0, 15))

    # Фрейм пошуку
    search_frame = tk.Frame(left_frame, bg="#f0f0f0")
    search_frame.pack(fill=tk.X, pady=10)

    tk.Label(
        search_frame,
        text="Пошук книги у вашому залі:",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0"
    ).pack(anchor=tk.W, pady=5)

    book_search_var = tk.StringVar()
    book_search_entry = tk.Entry(
        search_frame,
        textvariable=book_search_var,
        width=40,
        font=("Arial", 12)
    )
    book_search_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=5)

    # Таблиця книг у залі
    tree_frame = tk.Frame(left_frame, bg="#f0f0f0")
    tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    style = ttk.Style()
    style.configure("Custom.Treeview", font=("Arial", 11), rowheight=28)
    style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"))

    columns = ('title', 'access_type', 'available_quantity')
    tree = ttk.Treeview(
        tree_frame,
        columns=columns,
        show='headings',
        height=15,
        style="Custom.Treeview"
    )

    tree.heading('title', text='Назва книги')
    tree.heading('access_type', text='Тип доступу')
    tree.heading('available_quantity', text='Доступно')

    tree.column('title', width=300, stretch=tk.YES)
    tree.column('access_type', width=200, stretch=tk.NO)
    tree.column('available_quantity', width=100, anchor=tk.CENTER, stretch=tk.NO)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # book_id_map: item_id -> dict з даними книги
    book_id_map = {}

    def refresh_book_list_treeview(event=None):
        for item in tree.get_children():
            tree.delete(item)
        book_id_map.clear()
        search_term = book_search_var.get().strip()
        books = fetch_available_books(room_id, search_term if search_term else None)
        
        if not books:
            # Додамо повідомлення, якщо книг не знайдено
            item_id = tree.insert('', tk.END, values=("Книг не знайдено", "", ""))
            tree.item(item_id, tags=('empty',))
            tree.tag_configure('empty', foreground='gray')
        else:
            for book in books:
                book_id = book['book_id']
                item_id = tree.insert(
                    '',
                    tk.END,
                    values=(book['title'], book['access_type'], book['available_quantity'])
                )
                book_id_map[item_id] = book
                if book['available_quantity'] <= 0:
                    tree.item(item_id, tags=('unavailable',))
            tree.tag_configure('unavailable', foreground='gray', background='#ffeeee')

    book_search_entry.bind('<Return>', refresh_book_list_treeview)
    search_btn = tk.Button(
        search_frame,
        text="Знайти (Enter)",
        command=refresh_book_list_treeview,
        bg="#3498DB",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=3
    )
    search_btn.pack(side=tk.LEFT, padx=5)

    # ---------- МОДАЛЬНЕ ВІКНО ВИДАЧІ КНИГИ ----------

    def open_issue_window(event):
        selected_item_id = tree.focus()
        if not selected_item_id:
            messagebox.showwarning("Увага", "Оберіть книгу зі списку!")
            return
        
        # Перевірка на пустий запис
        if tree.item(selected_item_id)['values'][0] == "Книг не знайдено":
            messagebox.showwarning("Увага", "Оберіть дійсну книгу зі списку!")
            return
            
        book_details = book_id_map.get(selected_item_id)
        if not book_details:
            messagebox.showerror("Помилка", "Не вдалося отримати деталі книги.")
            return
        if book_details['available_quantity'] <= 0:
            messagebox.showwarning("Недоступно", "Цієї книги немає в наявності. Оновіть список.")
            return

        book_id = book_details['book_id']
        book_title = book_details['title']
        book_access_type = book_details['access_type']

        modal_window = tk.Toplevel(librarian_window)
        modal_window.title("Видача книги")
        modal_window.geometry("500x500")
        modal_window.configure(bg="#f0f0f0")
        modal_window.grab_set()
        modal_window.resizable(False, False)
        setup_keyboard_bindings(modal_window)

        readers_data_modal = {}  # login -> reader_id

        modal_frame = tk.Frame(modal_window, padx=20, pady=20, bg="#f0f0f0")
        modal_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            modal_frame,
            text="Видача книги",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        ).pack(pady=10)
        tk.Label(
            modal_frame,
            text=f"{book_title}",
            font=("Arial", 12),
            bg="#f0f0f0",
            wraplength=450
        ).pack(pady=(0, 20))

        # --- Блок вибору читача ---
        reader_frame = tk.Frame(modal_frame, bg="#f0f0f0")
        reader_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            reader_frame,
            text="Пошук читача (логін):",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0"
        ).grid(row=0, column=0, sticky=tk.W)
        reader_search_var_modal = tk.StringVar()
        reader_search_entry_modal = tk.Entry(
            reader_frame,
            textvariable=reader_search_var_modal,
            width=30,
            font=("Arial", 10)
        )
        reader_search_entry_modal.grid(row=0, column=1, padx=5)

        tk.Label(
            reader_frame,
            text="Оберіть читача:",
            font=("Arial", 11),
            bg="#f0f0f0"
        ).grid(row=1, column=0, sticky=tk.W, pady=5)

        reader_var_modal = tk.StringVar()
        reader_combobox_modal = ttk.Combobox(
            reader_frame,
            textvariable=reader_var_modal,
            state="readonly",
            width=28,
            font=("Arial", 10)
        )
        reader_combobox_modal.grid(row=1, column=1, padx=5, pady=5)

        def refresh_reader_list_modal(event=None):
            """Оновлення списку читачів в модальному вікні видачі."""
            search_term = reader_search_var_modal.get().strip()
            readers_data_modal.clear()
            updated_readers = fetch_all_readers(search_term if search_term else None)
            readers_data_modal.update({login: rid for rid, login in updated_readers})
            reader_combobox_modal['values'] = list(readers_data_modal.keys())

            # Автовибір першого читача, якщо список не порожній
            if readers_data_modal and not reader_var_modal.get():
                first_login = next(iter(readers_data_modal.keys()))
                reader_var_modal.set(first_login)

        reader_search_btn_modal = tk.Button(
            reader_frame,
            text="Знайти",
            command=refresh_reader_list_modal,
            bg="#3498DB",
            fg="white",
            font=("Arial", 9)
        )
        reader_search_btn_modal.grid(row=0, column=2, padx=5)
        reader_search_entry_modal.bind('<Return>', refresh_reader_list_modal)

        # --- Умови видачі ---
        options_frame = tk.Frame(modal_frame, bg="#f0f0f0", pady=15)
        options_frame.pack(fill=tk.X)

        tk.Label(
            options_frame,
            text="Умови видачі:",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0"
        ).pack(anchor=tk.W)

        place_var_modal = tk.StringVar(value="Тільки в читальній залі")
        radio_frame_modal = tk.Frame(options_frame, bg="#f0f0f0")
        radio_frame_modal.pack(fill=tk.X, pady=5)

        tk.Radiobutton(
            radio_frame_modal,
            text="В залі (сьогодні)",
            variable=place_var_modal,
            value="Тільки в читальній залі",
            font=("Arial", 10),
            bg="#f0f0f0",
            command=lambda: toggle_calendar_modal(False)
        ).pack(side=tk.LEFT, padx=10)

        radio_home = tk.Radiobutton(
            radio_frame_modal,
            text="Додому (до 7 днів)",
            variable=place_var_modal,
            value="У читальній залі і вдома",
            font=("Arial", 10),
            bg="#f0f0f0",
            command=lambda: toggle_calendar_modal(True)
        )
        radio_home.pack(side=tk.LEFT, padx=10)

        if book_access_type == "Тільки в читальній залі":
            radio_home.config(state=tk.DISABLED)
            tk.Label(
                radio_frame_modal,
                text="(недоступно для цієї книги)",
                font=("Arial", 8),
                fg="gray",
                bg="#f0f0f0"
            ).pack(side=tk.LEFT, padx=5)

        date_label_modal = tk.Label(
            options_frame,
            text="Дата повернення:",
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        return_calendar_modal = DateEntry(
            options_frame,
            mindate=date.today(),
            maxdate=date.today() + timedelta(days=7),
            date_pattern='yyyy-mm-dd',
            font=("Arial", 10)
        )

        def toggle_calendar_modal(show):
            if show:
                date_label_modal.pack(anchor=tk.W, pady=(5, 0))
                return_calendar_modal.pack(anchor=tk.W, pady=(0, 5))
            else:
                date_label_modal.pack_forget()
                return_calendar_modal.pack_forget()

        toggle_calendar_modal(False)

        # --- Підтвердження видачі ---
        def handle_issue_modal(event=None):
            selected_reader_login = reader_var_modal.get()
            if not selected_reader_login:
                messagebox.showwarning(
                    "Увага",
                    "Будь ласка, оберіть читача.",
                    parent=modal_window
                )
                return
            reader_id = readers_data_modal.get(selected_reader_login)
            if not reader_id:
                messagebox.showerror(
                    "Помилка",
                    "Некоректний ID читача.",
                    parent=modal_window
                )
                return

            reading_place = place_var_modal.get()
            if reading_place == "У читальній залі і вдома":
                selected_date = return_calendar_modal.get_date()
                today = date.today()
                max_return_date = today + timedelta(days=7)
                if selected_date < today or selected_date > max_return_date:
                    messagebox.showerror(
                        "Помилка дати",
                        "Дата повернення має бути в межах 7 днів від сьогодні.",
                        parent=modal_window
                    )
                    return
                return_date = selected_date
            else:
                return_date = date.today()

            success = issue_book_by_librarian(
                librarian_id,
                room_id,
                reader_id,
                book_id,
                reading_place,
                return_date
            )
            if success:
                modal_window.destroy()
                refresh_book_list_treeview()
                refresh_stats()

        issue_btn_modal = tk.Button(
            modal_frame,
            text="Видати книгу",
            font=("Arial", 12, "bold"),
            bg="#27AE60",
            fg="white",
            command=handle_issue_modal,
            padx=15,
            pady=8
        )
        issue_btn_modal.pack(side=tk.BOTTOM, pady=20)

        refresh_reader_list_modal()
        reader_search_entry_modal.focus_set()

    tree.bind("<Double-1>", open_issue_window)
    refresh_book_list_treeview()

    tk.Label(
        left_frame,
        text="Подвійний клік на книзі, щоб відкрити вікно видачі",
        font=("Arial", 9, "italic"),
        bg="#f0f0f0",
        fg="gray"
    ).pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    # ПРАВА ЧАСТИНА: інструменти
    right_frame = tk.Frame(main_frame, bg="#f0f0f0", width=350)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
    right_frame.pack_propagate(False)

    tk.Label(
        right_frame,
        text="Інструменти",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0"
    ).pack(anchor=tk.W, pady=(0, 15))

    tools_frame = tk.Frame(right_frame, bg="#f0f0f0")
    tools_frame.pack(fill=tk.X, pady=5)

    edit_book_btn = create_modern_button(
        tools_frame,
        "Редагувати книгу",
        show_edit_book_window_librarian,
        bg_color="#27AE60",
        hover_color="#229954",
        width=35,
        font_size=12
    )
    edit_book_btn.pack(fill=tk.X, pady=5)

    who_has_btn = create_modern_button(
        tools_frame,
        "Хто тримає книгу",
        find_who_has_book,
        bg_color="#3498DB",
        hover_color="#2980B9",
        width=35,
        font_size=12
    )
    who_has_btn.pack(fill=tk.X, pady=5)

    search_books_btn = create_modern_button(
        tools_frame,
        "Пошук книг",
        find_books_by_work_or_author,
        bg_color="#9B59B6",
        hover_color="#8E44AD",
        width=35,
        font_size=12
    )
    search_books_btn.pack(fill=tk.X, pady=5)

    overdue_btn = create_modern_button(
        tools_frame,
        "Прострочені книги",
        show_admin_overdue_books,
        bg_color="#E74C3C",
        hover_color="#C0392B",
        width=35,
        font_size=12
    )
    overdue_btn.pack(fill=tk.X, pady=5)

    sql_btn = create_modern_button(
        tools_frame,
        "SQL Editor",
        show_sql_editor_window,
        bg_color="#34495E",
        hover_color="#2C3E50",
        width=35,
        font_size=12
    )
    sql_btn.pack(fill=tk.X, pady=5)

    returns_btn = create_modern_button(
        tools_frame,
        "Повернення книг читачів",
        command=lambda: show_all_returns_window(librarian_id, room_id),
        bg_color="#F39C12",
        hover_color="#D68910",
        width=35,
        font_size=12
    )
    returns_btn.pack(fill=tk.X, pady=5)

    separator = ttk.Separator(tools_frame, orient=tk.HORIZONTAL)
    separator.pack(fill=tk.X, pady=15)

    # ---------- Статистика ----------
    stats_frame = tk.Frame(right_frame, bg="#f0f0f0")
    stats_frame.pack(fill=tk.X, pady=10)

    tk.Label(
        stats_frame,
        text="Статистика залу",
        font=("Arial", 14, "bold"),
        bg="#f0f0f0"
    ).pack(anchor=tk.W, pady=(0, 10))

    stats_labels_container = tk.Frame(stats_frame, bg="#f0f0f0")
    stats_labels_container.pack(fill=tk.X)

    def refresh_stats():
        for widget in stats_labels_container.winfo_children():
            widget.destroy()

        all_books = fetch_available_books(room_id)
        total_books = len(all_books)
        available_books = sum(1 for book in all_books if book['available_quantity'] > 0)
        borrowed_books = total_books - available_books
        overdue_count = len(fetch_overdue_books(librarian_id))

        stats_labels_text = [
            f"Загалом книг: {total_books}",
            f"Доступно: {available_books}",
            f"Видано: {borrowed_books}",
            f"Прострочено: {overdue_count}"
        ]

        for label_text in stats_labels_text:
            tk.Label(
                stats_labels_container,
                text=label_text,
                font=("Arial", 11),
                bg="#f0f0f0"
            ).pack(anchor=tk.W, pady=2)

    refresh_stats_btn = tk.Button(
        stats_frame,
        text="Оновити статистику",
        command=refresh_stats,
        bg="#3498DB",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=3
    )
    refresh_stats_btn.pack(anchor=tk.W, pady=10)

    refresh_stats()

    librarian_window.mainloop()