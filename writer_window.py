# writer_window.py
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from utils import get_user_id
from database import get_db_connection
import mysql.connector
import tkinter as tk

# ---------------------- УТИЛІТИ ----------------------

def show_help():
    """Показує довідку (F1)."""
    messagebox.showinfo("Допомога (F1)",
                        "Основні гарячі клавіші:\n\n"
                        "• Enter: Підтвердити дію / зберегти\n"
                        "• Esc: Скасувати або закрити вікно\n"
                        "• F11: Повноекранний / Звичайний режим\n"
                        "• F1: Показати цю довідку")

def maximize_window(win):
    """
    Розгортає вікно максимально, зберігаючи стандартну рамку ОС.
    Працює на Windows (state('zoomed')), Linux (attributes('-zoomed')) і як fallback ставить геометрію екрана.
    """
    try:
        # гарантуємо, що fullscreen не встановлений
        win.attributes('-fullscreen', False)
    except Exception:
        pass

    try:
        win.state('zoomed')  # Windows
        return
    except Exception:
        pass

    try:
        win.attributes('-zoomed', True)  # Linux
        return
    except Exception:
        pass

    # fallback
    try:
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        win.geometry(f"{ws}x{hs}+0+0")
    except Exception:
        pass

def toggle_fullscreen(window):
    """Перемикає повноекранний режим (F11 або кнопка в заголовку)."""
    try:
        current = window.attributes('-fullscreen')
    except Exception:
        current = False
    window.attributes('-fullscreen', not current)

def go_to_login(window_to_close):
    """Підтвердження виходу і повернення до вікон входу."""
    if messagebox.askyesno("Підтвердження виходу", "Ви дійсно хочете вийти та повернутися до вікна входу?"):
        try:
            from login_window import show_login_window
            window_to_close.destroy()
            show_login_window()
        except Exception:
            # Якщо login_window відсутній — просто закриваємо
            window_to_close.destroy()

# ---------------------- ЗАГОЛОВОК ----------------------

def create_header(parent, title_text, window=None):
    """
    Створює темний заголовок всередині вікна (під системною панеллю).
    Якщо передано 'window', додає кнопку ⛶ для перемикання fullscreen.
    """
    header_frame = Frame(parent, bg='#2c3e50', height=120)
    header_frame.pack(fill='x', pady=(0, 20))
    header_frame.pack_propagate(False)

    header_main = Frame(header_frame, bg='#2c3e50')
    header_main.pack(fill='both', expand=True)

    icon_label = Label(header_main, text="📚", font=("Arial", 36),
                       bg='#2c3e50', fg='#ecf0f1')
    icon_label.pack(side='left', padx=20, pady=10)

    title_label = Label(header_main, text=title_text,
                        font=("Arial", 20, "bold"),
                        bg='#2c3e50', fg='#ecf0f1')
    title_label.pack(side='left', padx=10, pady=10)

    # Кнопка перемикання fullscreen у заголовку
    if window is not None:
        def on_fs_click():
            toggle_fullscreen(window)
        fs_btn = Button(header_main, text="⛶", font=("Arial", 16, "bold"),
                        bg='#2c3e50', fg='#ecf0f1', bd=0, activebackground='#1f2d38',
                        cursor='hand2', command=on_fs_click)
        fs_btn.pack(side='right', padx=20, pady=10)

    return header_frame

# ---------------------- БАЗА ДАНИХ: витягання списків ----------------------

def fetch_all_authors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT author_id, name, surname FROM Authors ORDER BY surname, name")
    authors = cursor.fetchall()
    cursor.close()
    conn.close()
    return authors

def fetch_all_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.book_id, b.title, a.name, a.surname 
        FROM Books b
        JOIN Authors a ON b.author_id = a.author_id
        ORDER BY a.surname, a.name, b.title
    """)
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return books

# ---------------------- ПЕРЕГЛЯД КНИГ АВТОРА ----------------------

def show_books_by_author(author):
    """
    Показує вікно зі списком книг указаного автора.
    'author' тут — значення, яке get_user_id знає (наприклад login або id).
    """
    user_id = get_user_id(author)
    if user_id is None:
        messagebox.showerror("Помилка", f"Користувача '{author}' не знайдено")
        return

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT author_id, name, surname FROM Authors WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            messagebox.showerror("Помилка", "Автор не знайдений")
            return
        author_id, name, surname = row

        cursor.execute("""
            SELECT book_id, title, year, languages, inventory_number, category_id 
            FROM Books WHERE author_id = %s
        """, (author_id,))
        books = cursor.fetchall()

        books_window = Toplevel()
        books_window.title("Мої книги")
        maximize_window(books_window)

        # Прив'язки клавіш
        books_window.bind('<Escape>', lambda e: books_window.destroy())
        books_window.bind('<F1>', lambda e: show_help())
        books_window.bind('<F11>', lambda e: toggle_fullscreen(books_window))

        # Оформлення
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 12), rowheight=30)
        style.configure("Treeview.Heading", font=('Arial', 13, 'bold'))

        main_frame = Frame(books_window, bg='#f5f5f5')
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        create_header(main_frame, f"Книги автора: {name} {surname}", window=books_window)

        tree_frame = Frame(main_frame)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        tree = ttk.Treeview(tree_frame, columns=("ID", "Назва", "Рік", "Мова", "Інвентарний", "Категорія"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Назва", text="Назва")
        tree.heading("Рік", text="Рік")
        tree.heading("Мова", text="Мова")
        tree.heading("Інвентарний", text="Інвентарний номер")
        tree.heading("Категорія", text="Категорія")

        tree.column("ID", width=80)
        tree.column("Назва", width=350)
        tree.column("Рік", width=120)
        tree.column("Мова", width=150)
        tree.column("Інвентарний", width=200)
        tree.column("Категорія", width=200)

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Завантажуємо назви категорій
        category_names = {}
        cursor.execute("SELECT category_id, name FROM Categories")
        for cat_id, cat_name in cursor.fetchall():
            category_names[cat_id] = cat_name

        for book in books:
            book_id, title, year, language, inv_number, category_id = book
            category_name = category_names.get(category_id, "Невідомо")
            tree.insert("", END, values=(book_id, title, year, language, inv_number, category_name))

        # Прив'язка Enter до редагування
        tree.bind('<Return>', lambda e: edit_selected_book(tree, author))

        # Кнопки
        button_frame = Frame(main_frame, bg='#f5f5f5')
        button_frame.pack(pady=20)

        edit_btn = Button(button_frame, text="Редагувати обрану книгу",
                          command=lambda: edit_selected_book(tree, author),
                          font=('Arial', 12), bg='#3498db', fg='white',
                          padx=20, pady=10)
        edit_btn.pack(side=LEFT, padx=10)
        edit_btn.bind('<Return>', lambda e: edit_selected_book(tree, author))

        close_btn = Button(button_frame, text="Закрити",
                           command=books_window.destroy,
                           font=('Arial', 12), bg='#e74c3c', fg='white',
                           padx=20, pady=10)
        close_btn.pack(side=LEFT, padx=10)
        close_btn.bind('<Return>', lambda e: books_window.destroy())

    except mysql.connector.Error as err:
        messagebox.showerror("Помилка БД", str(err))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def edit_selected_book(tree, author):
    """Отримує виділену книгу в tree та відкриває вікно редагування."""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Увага", "Оберіть книгу для редагування")
        return

    book_id = tree.item(selected[0])['values'][0]
    show_edit_book_window(author, book_id)

# ---------------------- РЕДАГУВАННЯ КНИГИ ----------------------

def show_edit_book_window(author, book_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title, year, languages, category_id 
            FROM Books WHERE book_id = %s
        """, (book_id,))
        book_data = cursor.fetchone()
        if not book_data:
            messagebox.showerror("Помилка", "Книгу не знайдено")
            return
        title, year, language, category_id = book_data

        cursor.execute("SELECT name FROM Categories WHERE category_id = %s", (category_id,))
        category_result = cursor.fetchone()
        category_name = category_result[0] if category_result else ""

    except mysql.connector.Error as err:
        messagebox.showerror("Помилка БД", str(err))
        return
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    edit_window = Toplevel()
    edit_window.title("Редагувати книгу")
    maximize_window(edit_window)

    edit_window.bind('<Escape>', lambda e: edit_window.destroy())
    edit_window.bind('<F1>', lambda e: show_help())
    edit_window.bind('<F11>', lambda e: toggle_fullscreen(edit_window))
    edit_window.bind('<Return>', lambda e: save_changes_wrapper())

    main_frame = Frame(edit_window, bg='#f5f5f5')
    main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

    create_header(main_frame, "Редагування книги", window=edit_window)

    form_frame = Frame(main_frame, bg='#f5f5f5')
    form_frame.pack(fill=BOTH, expand=True)

    Label(form_frame, text="Назва:", font=('Arial', 14), bg='#f5f5f5').pack(pady=15)
    entry_title = Entry(form_frame, width=50, font=('Arial', 14))
    entry_title.insert(0, title)
    entry_title.pack(pady=5)

    Label(form_frame, text="Рік:", font=('Arial', 14), bg='#f5f5f5').pack(pady=15)
    entry_year = Entry(form_frame, width=50, font=('Arial', 14))
    entry_year.insert(0, year if year is not None else "")
    entry_year.pack(pady=5)

    Label(form_frame, text="Мова:", font=('Arial', 14), bg='#f5f5f5').pack(pady=15)
    entry_language = Entry(form_frame, width=50, font=('Arial', 14))
    entry_language.insert(0, language if language is not None else "")
    entry_language.pack(pady=5)

    Label(form_frame, text="Категорія:", font=('Arial', 14), bg='#f5f5f5').pack(pady=15)
    category_var = StringVar(value=category_name)
    category_combo = ttk.Combobox(form_frame, textvariable=category_var, font=('Arial', 14), width=47)
    category_combo.pack(pady=5)

    # Завантажити категорії
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Categories")
        categories = [row[0] for row in cursor.fetchall()]
        category_combo['values'] = categories
    except Exception:
        messagebox.showerror("Помилка", "Не вдалося завантажити категорії")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    def save_changes():
        title_v = entry_title.get().strip()
        year_v = entry_year.get().strip()
        language_v = entry_language.get().strip()
        category_name_v = category_var.get().strip()

        if not (title_v and year_v and language_v and category_name_v):
            messagebox.showerror("Помилка", "Заповніть усі обов'язкові поля")
            return

        user_id = get_user_id(author)
        if user_id is None:
            messagebox.showerror("Помилка", "Автор не знайдений")
            return

        conn2 = None
        cur2 = None
        try:
            conn2 = get_db_connection()
            cur2 = conn2.cursor()

            cur2.execute("SELECT category_id FROM Categories WHERE name = %s", (category_name_v,))
            r = cur2.fetchone()
            if not r:
                messagebox.showerror("Помилка", "Обрана категорія не існує")
                return
            category_id_v = r[0]

            cur2.execute("""
                UPDATE Books 
                SET title = %s, category_id = %s, year = %s, languages = %s
                WHERE book_id = %s
            """, (title_v, category_id_v, year_v, language_v, book_id))
            conn2.commit()
            messagebox.showinfo("Успіх", "Книгу успішно оновлено")
            edit_window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Помилка БД", str(err))
        finally:
            if cur2:
                cur2.close()
            if conn2:
                conn2.close()

    def save_changes_wrapper():
        save_changes()

    # Кнопки
    button_frame = Frame(main_frame, bg='#f5f5f5')
    button_frame.pack(pady=30)

    save_btn = Button(button_frame, text="Зберегти зміни", command=save_changes,
                      font=('Arial', 14), bg='#27ae60', fg='white',
                      padx=20, pady=10)
    save_btn.pack(side=LEFT, padx=10)
    save_btn.bind('<Return>', lambda e: save_changes())

    cancel_btn = Button(button_frame, text="Скасувати", command=edit_window.destroy,
                        font=('Arial', 14), bg='#e74c3c', fg='white',
                        padx=20, pady=10)
    cancel_btn.pack(side=LEFT, padx=10)
    cancel_btn.bind('<Return>', lambda e: edit_window.destroy())

# ---------------------- ДОДАННЯ НОВОЇ КНИГИ ----------------------

def show_add_book_window(author):
    def generate_inventory_number():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Books")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return f"INV-{count + 1:05d}"
        except Exception:
            return "INV-00001"

    def save_book():
        title = entry_title.get().strip()
        year = entry_year.get().strip()
        language = entry_language.get().strip()
        inventory_number = inventory_number_var.get().strip()
        category_name = category_var.get().strip()

        if not (title and year and language and category_name):
            messagebox.showerror("Помилка", "Заповніть усі поля")
            return

        user_id = get_user_id(author)
        if user_id is None:
            messagebox.showerror("Помилка", "Автор не знайдений")
            return

        conn2 = None
        cur2 = None
        try:
            conn2 = get_db_connection()
            cur2 = conn2.cursor()
            cur2.execute("SELECT author_id FROM Authors WHERE user_id = %s", (user_id,))
            res = cur2.fetchone()
            if not res:
                messagebox.showerror("Помилка", "Автор не знайдено в базі")
                return
            author_id = res[0]

            cur2.execute("SELECT category_id FROM Categories WHERE name = %s", (category_name,))
            cat = cur2.fetchone()
            if not cat:
                messagebox.showerror("Помилка", "Категорія не знайдена")
                return
            category_id = cat[0]

            cur2.execute("""
                INSERT INTO Books (title, author_id, category_id, year, languages, inventory_number)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (title, author_id, category_id, year, language, inventory_number))
            conn2.commit()
            messagebox.showinfo("Успіх", "Книгу додано")
            add_window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Помилка БД", str(err))
        finally:
            if cur2:
                cur2.close()
            if conn2:
                conn2.close()

    add_window = Toplevel()
    add_window.title("Додати книгу")
    maximize_window(add_window)

    add_window.bind('<Escape>', lambda e: add_window.destroy())
    add_window.bind('<F1>', lambda e: show_help())
    add_window.bind('<F11>', lambda e: toggle_fullscreen(add_window))
    add_window.bind('<Return>', lambda e: save_book())

    main_frame = Frame(add_window, bg='#f5f5f5')
    main_frame.pack(fill=BOTH, expand=True, padx=50, pady=50)

    create_header(main_frame, "Додати нову книгу", window=add_window)

    form_frame = Frame(main_frame, bg='#f5f5f5')
    form_frame.pack(fill=BOTH, expand=True)

    Label(form_frame, text="Назва:", font=('Arial', 14), bg='#f5f5f5').pack(pady=10)
    entry_title = Entry(form_frame, width=50, font=('Arial', 14))
    entry_title.pack(pady=5)

    Label(form_frame, text="Рік:", font=('Arial', 14), bg='#f5f5f5').pack(pady=10)
    entry_year = Entry(form_frame, width=50, font=('Arial', 14))
    entry_year.pack(pady=5)

    Label(form_frame, text="Мова:", font=('Arial', 14), bg='#f5f5f5').pack(pady=10)
    entry_language = Entry(form_frame, width=50, font=('Arial', 14))
    entry_language.pack(pady=5)

    Label(form_frame, text="Інвентарний номер:", font=('Arial', 14), bg='#f5f5f5').pack(pady=10)
    inventory_number_var = StringVar(value=generate_inventory_number())
    entry_inventory = Entry(form_frame, textvariable=inventory_number_var, width=50, font=('Arial', 14))
    entry_inventory.configure(state='readonly')
    entry_inventory.pack(pady=5)

    Label(form_frame, text="Категорія:", font=('Arial', 14), bg='#f5f5f5').pack(pady=10)
    category_var = StringVar()
    category_combo = ttk.Combobox(form_frame, textvariable=category_var, font=('Arial', 14), width=47)
    category_combo.pack(pady=5)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Categories")
        categories = [row[0] for row in cursor.fetchall()]
        category_combo['values'] = categories
    except Exception:
        messagebox.showerror("Помилка", "Не вдалося завантажити категорії")
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

    button_frame = Frame(main_frame, bg='#f5f5f5')
    button_frame.pack(pady=30)

    save_btn = Button(button_frame, text="Зберегти книгу", command=save_book,
                      font=('Arial', 14), bg='#27ae60', fg='white',
                      padx=20, pady=10)
    save_btn.pack(side=LEFT, padx=10)

    cancel_btn = Button(button_frame, text="Скасувати", command=add_window.destroy,
                        font=('Arial', 14), bg='#e74c3c', fg='white',
                        padx=20, pady=10)
    cancel_btn.pack(side=LEFT, padx=10)

# ---------------------- ГЕНЕРАЦІЯ НОМЕРІВ ДЛЯ ЗБІРОК ----------------------

def generate_collection_inventory():
    """Повертає унікальний інвентарний номер для збірки."""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Collections")
        count = cursor.fetchone()[0]
        return f"COLL-{count + 1:05d}"
    except Exception:
        return "COLL-00001"
    finally:
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        except Exception:
            pass

# ---------------------- СТВОРЕННЯ ЗБІРКИ ----------------------

# ---------------------- СТВОРЕННЯ ЗБІРКИ ----------------------

# ---------------------- СТВОРЕННЯ ЗБІРКИ ----------------------

def show_collection_window():
    window = Toplevel()
    window.title("Створення збірки")
    maximize_window(window)
    window.grab_set()

    window.bind('<Escape>', lambda e: window.destroy())
    window.bind('<F1>', lambda e: show_help())
    window.bind('<F11>', lambda e: toggle_fullscreen(window))

    style = ttk.Style()
    style.configure("Treeview", font=('Arial', 11), rowheight=30)
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))

    selected_authors = []
    selected_books = []

    main_frame = Frame(window, bg='#f5f5f5')
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    create_header(main_frame, "Створення збірки", window=window)

    canvas = Canvas(main_frame, bg='#f5f5f5')
    scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas, bg='#f5f5f5')

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Налаштування сітки для розтягування на всю ширину
    scrollable_frame.columnconfigure(0, weight=1)
    scrollable_frame.columnconfigure(1, weight=1)

    Label(scrollable_frame, text="Назва збірки:", font=("Arial", 14, "bold"), bg='#f5f5f5').grid(row=0, column=0, padx=10, pady=10, sticky=W)
    title_entry = Entry(scrollable_frame, width=50, font=('Arial', 12))
    title_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2, sticky=EW)

    Label(scrollable_frame, text="Тип збірки:", font=("Arial", 14, "bold"), bg='#f5f5f5').grid(row=1, column=0, padx=10, pady=10, sticky=W)
    type_var = StringVar()
    type_combo = ttk.Combobox(scrollable_frame, textvariable=type_var, width=47, font=('Arial', 12), state="readonly")
    type_combo.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky=EW)

    default_types = ('книги', 'журнали', 'газети', 'збірники статей', 
                     'збірники віршів', 'дисертації', 'реферати', 'збірники доповідей')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name FROM BookTypes ORDER BY name")
            book_types = [row[0] for row in cursor.fetchall()]
            type_combo['values'] = book_types if book_types else default_types
        except Exception:
            type_combo['values'] = default_types
    except Exception:
        type_combo['values'] = default_types
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

    # Контейнер для авторів та книг (однаковий рівень)
    selection_container = Frame(scrollable_frame, bg='#f5f5f5')
    selection_container.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky=NSEW)

    # Налаштування сітки для рівномірного розподілу на всю ширину
    selection_container.columnconfigure(0, weight=1)
    selection_container.columnconfigure(1, weight=1)

    # Author tree - ліва сторона (розтягнута на всю доступну ширину)
    authors_label_frame = LabelFrame(selection_container, text="Оберіть авторів", font=("Arial", 14, "bold"), bg='#f5f5f5')
    authors_label_frame.grid(row=0, column=0, padx=(0, 5), pady=5, sticky=NSEW)

    # Налаштування сітки всередині фрейму авторів для розтягування
    authors_label_frame.columnconfigure(0, weight=1)
    authors_label_frame.rowconfigure(0, weight=1)

    author_columns = ("author_id", "name", "surname")
    author_tree = ttk.Treeview(authors_label_frame, columns=author_columns, show="headings", height=12)
    author_tree.heading("author_id", text="ID")
    author_tree.heading("name", text="Ім'я")
    author_tree.heading("surname", text="Прізвище")
    author_tree.column("author_id", width=80, minwidth=80)
    author_tree.column("name", width=200, minwidth=150)
    author_tree.column("surname", width=200, minwidth=150)

    try:
        all_authors = fetch_all_authors()
        for author in all_authors:
            author_tree.insert("", "end", values=author)
    except Exception:
        all_authors = []
        messagebox.showerror("Помилка", "Не вдалося завантажити авторів")

    author_scrollbar = ttk.Scrollbar(authors_label_frame, orient=VERTICAL, command=author_tree.yview)
    author_tree.configure(yscrollcommand=author_scrollbar.set)
    
    # Розміщення treeview з розтягуванням
    author_tree.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)
    author_scrollbar.grid(row=0, column=1, sticky=NS, pady=5)

    # Book tree - права сторона (розтягнута на всю доступну ширину)
    books_label_frame = LabelFrame(selection_container, text="Оберіть книги", font=("Arial", 14, "bold"), bg='#f5f5f5')
    books_label_frame.grid(row=0, column=1, padx=(5, 0), pady=5, sticky=NSEW)

    # Налаштування сітки всередині фрейму книг для розтягування
    books_label_frame.columnconfigure(0, weight=1)
    books_label_frame.rowconfigure(0, weight=1)

    book_columns = ("book_id", "title", "author_name", "author_surname")
    book_tree = ttk.Treeview(books_label_frame, columns=book_columns, show="headings", height=12)
    book_tree.heading("book_id", text="ID")
    book_tree.heading("title", text="Назва книги")
    book_tree.heading("author_name", text="Ім'я автора")
    book_tree.heading("author_surname", text="Прізвище автора")
    book_tree.column("book_id", width=80, minwidth=80)
    book_tree.column("title", width=300, minwidth=200)
    book_tree.column("author_name", width=150, minwidth=120)
    book_tree.column("author_surname", width=150, minwidth=120)

    try:
        all_books = fetch_all_books()
        for book in all_books:
            book_tree.insert("", "end", values=book)
    except Exception:
        all_books = []
        messagebox.showerror("Помилка", "Не вдалося завантажити книги")

    book_scrollbar = ttk.Scrollbar(books_label_frame, orient=VERTICAL, command=book_tree.yview)
    book_tree.configure(yscrollcommand=book_scrollbar.set)
    
    # Розміщення treeview з розтягуванням
    book_tree.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)
    book_scrollbar.grid(row=0, column=1, sticky=NS, pady=5)

    # Selected items - під двома дереввами (також розтягнуте)
    selected_label_frame = LabelFrame(scrollable_frame, text="Обрані елементи", font=("Arial", 14, "bold"), bg='#f5f5f5')
    selected_label_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky=NSEW)
    
    # Налаштування сітки для списку обраних елементів
    selected_label_frame.columnconfigure(0, weight=1)
    selected_label_frame.rowconfigure(0, weight=1)

    selected_listbox = Listbox(selected_label_frame, font=('Arial', 12), height=8)
    selected_scrollbar_list = ttk.Scrollbar(selected_label_frame, orient=VERTICAL, command=selected_listbox.yview)
    selected_listbox.configure(yscrollcommand=selected_scrollbar_list.set)
    
    # Розміщення listbox з розтягуванням
    selected_listbox.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)
    selected_scrollbar_list.grid(row=0, column=1, sticky=NS, pady=5)

    def update_selected_items_list():
        selected_listbox.delete(0, END)
        for author_id in selected_authors:
            for author in all_authors:
                if author[0] == author_id:
                    selected_listbox.insert(END, f"АВТОР: {author[2]} {author[1]}")
        for book_id in selected_books:
            for book in all_books:
                if book[0] == book_id:
                    selected_listbox.insert(END, f"КНИГА: {book[1]} ({book[3]} {book[2]})")

    def add_author():
        selected = author_tree.selection()
        if selected:
            author_id = author_tree.item(selected[0])['values'][0]
            if author_id not in selected_authors:
                selected_authors.append(author_id)
                update_selected_items_list()
            else:
                messagebox.showwarning("Увага", "Цей автор вже доданий")
        else:
            messagebox.showwarning("Увага", "Оберіть автора зі списку")

    def add_book():
        selected = book_tree.selection()
        if selected:
            book_id = book_tree.item(selected[0])['values'][0]
            if book_id not in selected_books:
                selected_books.append(book_id)
                update_selected_items_list()
            else:
                messagebox.showwarning("Увага", "Ця книга вже додана")
        else:
            messagebox.showwarning("Увага", "Оберіть книгу зі списку")

    def remove_selected():
        selected = selected_listbox.curselection()
        if selected:
            index = selected[0]
            item_text = selected_listbox.get(index)
            if item_text.startswith("АВТОР:"):
                author_name = item_text.replace("АВТОР: ", "")
                for i, author_id in enumerate(selected_authors):
                    for author in all_authors:
                        if author[0] == author_id and f"{author[2]} {author[1]}" == author_name:
                            selected_authors.pop(i)
                            break
            elif item_text.startswith("КНИГА:"):
                book_info = item_text.replace("КНИГА: ", "")
                for i, book_id in enumerate(selected_books):
                    for book in all_books:
                        if book[0] == book_id and f"{book[1]} ({book[3]} {book[2]})" == book_info:
                            selected_books.pop(i)
                            break
            update_selected_items_list()
        else:
            messagebox.showwarning("Увага", "Оберіть елемент для видалення")

    author_tree.bind('<Return>', lambda e: add_author())
    book_tree.bind('<Return>', lambda e: add_book())
    selected_listbox.bind('<Return>', lambda e: remove_selected())
    selected_listbox.bind('<Delete>', lambda e: remove_selected())

    buttons_frame = Frame(scrollable_frame, bg='#f5f5f5')
    buttons_frame.grid(row=4, column=0, columnspan=3, pady=15)

    add_auth_btn = Button(buttons_frame, text="Додати автора", command=add_author,
                         bg="#3498db", fg='white', font=('Arial', 12), padx=15, pady=8)
    add_auth_btn.pack(side=LEFT, padx=10)

    add_book_btn = Button(buttons_frame, text="Додати книгу", command=add_book,
                         bg="#27ae60", fg='white', font=('Arial', 12), padx=15, pady=8)
    add_book_btn.pack(side=LEFT, padx=10)

    remove_btn = Button(buttons_frame, text="Видалити обране", command=remove_selected,
                       bg="#e74c3c", fg='white', font=('Arial', 12), padx=15, pady=8)
    remove_btn.pack(side=LEFT, padx=10)

    details_frame = Frame(scrollable_frame, bg='#f5f5f5')
    details_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=15, sticky=EW)
    
    # Налаштування сітки для деталей
    details_frame.columnconfigure(1, weight=1)
    details_frame.columnconfigure(3, weight=1)

    Label(details_frame, text="Рік:", font=('Arial', 12), bg='#f5f5f5').grid(row=0, column=0, padx=10, pady=5, sticky=W)
    year_entry = Entry(details_frame, width=20, font=('Arial', 12))
    year_entry.grid(row=0, column=1, padx=10, pady=5, sticky=EW)

    Label(details_frame, text="Мова:", font=('Arial', 12), bg='#f5f5f5').grid(row=0, column=2, padx=10, pady=5, sticky=W)
    language_entry = Entry(details_frame, width=20, font=('Arial', 12))
    language_entry.grid(row=0, column=3, padx=10, pady=5, sticky=EW)

    Label(details_frame, text="Кількість:", font=('Arial', 12), bg='#f5f5f5').grid(row=1, column=0, padx=10, pady=5, sticky=W)
    quantity_entry = Entry(details_frame, width=20, font=('Arial', 12))
    quantity_entry.grid(row=1, column=1, padx=10, pady=5, sticky=EW)

    Label(details_frame, text="Тип доступу:", font=('Arial', 12), bg='#f5f5f5').grid(row=1, column=2, padx=10, pady=5, sticky=W)
    access_var = StringVar()
    access_combo = ttk.Combobox(details_frame, textvariable=access_var, width=22, font=('Arial', 12), state="readonly")
    access_combo['values'] = ('Тільки в читальній залі', 'У читальній залі і вдома')
    access_combo.grid(row=1, column=3, padx=10, pady=5, sticky=EW)
    access_combo.current(0)

    Label(details_frame, text="Інвентарний номер:", font=('Arial', 12), bg='#f5f5f5').grid(row=2, column=0, padx=10, pady=5, sticky=W)
    inventory_entry = Entry(details_frame, width=20, font=('Arial', 12))
    inventory_entry.grid(row=2, column=1, padx=10, pady=5, sticky=EW)
    inventory_entry.insert(0, generate_collection_inventory())

    def save_collection():
        if not title_entry.get().strip():
            messagebox.showerror("Помилка", "Введіть назву збірки")
            return

        if not selected_authors and not selected_books:
            messagebox.showerror("Помилка", "Оберіть хоча б одного автора або книгу")
            return

        if not type_var.get():
            messagebox.showerror("Помилка", "Оберіть тип збірки")
            return

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            conn.autocommit = False

            type_name = type_var.get()
            try:
                cursor.execute("SELECT type_id FROM BookTypes WHERE name = %s", (type_name,))
                type_result = cursor.fetchone()
                if not type_result:
                    cursor.execute("INSERT INTO BookTypes (name) VALUES (%s)", (type_name,))
                    type_id = cursor.lastrowid
                else:
                    type_id = type_result[0]
            except mysql.connector.Error:
                messagebox.showerror("Помилка", "Не вдалося обробити тип збірки")
                conn.rollback()
                return

            access_type_value = access_var.get()

            unique_books = set()
            unique_authors = set()

            # Додаємо книги обраних авторів
            for author_id in selected_authors:
                unique_authors.add(author_id)
                cursor.execute("SELECT book_id FROM Books WHERE author_id = %s", (author_id,))
                for (book_id,) in cursor.fetchall():
                    unique_books.add(book_id)

            # Додаємо окремо вибрані книги та їх авторів
            for book_id in selected_books:
                unique_books.add(book_id)
                cursor.execute("SELECT author_id FROM Books WHERE book_id = %s", (book_id,))
                result = cursor.fetchone()
                if result:
                    unique_authors.add(result[0])

            if not unique_books:
                messagebox.showerror("Помилка", "Не знайдено жодної книги для збірки")
                conn.rollback()
                return

            # Визначаємо основного автора для збірки
            main_author_id = None
            if selected_authors:
                main_author_id = selected_authors[0]
            elif unique_books:
                first_book_id = list(unique_books)[0]
                cursor.execute("SELECT author_id FROM Books WHERE book_id = %s", (first_book_id,))
                result = cursor.fetchone()
                if result:
                    main_author_id = result[0]

            # Додаємо збірку в Collections
            cursor.execute("""
                INSERT INTO Collections (title, category_id, year, languages, quantity, 
                                       access_type, inventory_number, type_id, author_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                title_entry.get().strip(),
                type_id,
                year_entry.get().strip() if year_entry.get().strip() else None,
                language_entry.get().strip() if language_entry.get().strip() else None,
                int(quantity_entry.get()) if quantity_entry.get().strip().isdigit() else len(unique_books),
                access_type_value,
                inventory_entry.get().strip() if inventory_entry.get().strip() else generate_collection_inventory(),
                type_id,
                main_author_id
            ))
            collection_id = cursor.lastrowid

            # Запис збірки як книга (спрощено)
            if main_author_id:
                collection_inventory = f"COLL-BOOK-{collection_id:05d}"
                cursor.execute("""
                    INSERT INTO Books (title, author_id, category_id, year, languages, 
                                     quantity, access_type, inventory_number, collection_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    f"[ЗБІРКА] {title_entry.get().strip()}",
                    main_author_id,
                    type_id,
                    year_entry.get().strip() if year_entry.get().strip() else None,
                    language_entry.get().strip() if language_entry.get().strip() else None,
                    int(quantity_entry.get().strip()) if quantity_entry.get().strip().isdigit() else 1,
                    access_type_value,
                    collection_inventory,
                    collection_id
                ))

            # Додаємо книги до CollectionBooks
            for book_id in unique_books:
                try:
                    cursor.execute("INSERT INTO CollectionBooks (collection_id, book_id) VALUES (%s, %s)", (collection_id, book_id))
                except mysql.connector.IntegrityError:
                    pass

            # Додаємо до CollectionItems (деталі)
            for book_id in unique_books:
                try:
                    cursor.execute("""
                        SELECT title, author_id, category_id, year, languages, 
                               quantity, access_type, inventory_number
                        FROM Books WHERE book_id = %s
                    """, (book_id,))
                    book_data = cursor.fetchone()
                    if book_data:
                        cursor.execute("""
                            INSERT INTO CollectionItems 
                            (collection_id, book_id, title, author_id, category_id, 
                             year, languages, quantity, access_type, inventory_number)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (collection_id, book_id) + book_data)
                except mysql.connector.IntegrityError:
                    pass
                except mysql.connector.Error as e:
                    print(f"Помилка при збереженні книги {book_id} до CollectionItems: {e}")

            conn.commit()
            messagebox.showinfo("Успіх",
                               f"Збірку '{title_entry.get()}' успішно створено!\n"
                               f"Додано {len(unique_books)} книг від {len(unique_authors)} авторів.")
            window.destroy()

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            messagebox.showerror("Помилка БД", f"Помилка бази даних: {err}")
            print(f"Детальна помилка: {err}")
        except Exception as err:
            if conn:
                conn.rollback()
            messagebox.showerror("Помилка", f"Невідома помилка: {err}")
            print(f"Детальна помилка: {err}")
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except Exception:
                pass

    # Save / Cancel buttons
    save_buttons_frame = Frame(scrollable_frame, bg='#f5f5f5')
    save_buttons_frame.grid(row=6, column=0, columnspan=3, pady=30)

    save_btn = Button(save_buttons_frame, text="Зберегти збірку", command=save_collection,
                      bg="green", fg="white", font=("Arial", 14, "bold"), padx=30, pady=12)
    save_btn.pack(side=LEFT, padx=20)

    cancel_btn = Button(save_buttons_frame, text="Скасувати", command=window.destroy,
                        bg="red", fg="white", font=("Arial", 14, "bold"), padx=30, pady=12)
    cancel_btn.pack(side=LEFT, padx=20)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_scroll_region)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)
    
def show_writer_window(user_login):
    # Отримуємо логін/ім'я користувача (якщо user_login - це id)
    username = user_login
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT login FROM users WHERE user_id = %s", (user_login,))
        result = cursor.fetchone()
        if result:
            username = result[0]
    except mysql.connector.Error as err:
        print(f"Помилка отримання імені користувача: {err}")
    finally:
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        except Exception:
            pass

    writer_window = Tk()
    writer_window.title("Вікно автора")
    writer_window.configure(bg='#f5f5f5')

    maximize_window(writer_window)

    writer_window.bind('<Escape>', lambda e: go_to_login(writer_window))
    writer_window.bind('<F1>', lambda e: show_help())
    writer_window.bind('<F11>', lambda e: toggle_fullscreen(writer_window))

    main_container = Frame(writer_window, bg='#ffffff', relief='flat', bd=0)
    main_container.pack(fill='both', expand=True, padx=50, pady=50)

    header_frame = create_header(main_container, f"Вітаємо, {username}!", window=writer_window)

    # оновити іконку головного вікна
    for widget in header_frame.winfo_children():
        if isinstance(widget, Frame):
            for child in widget.winfo_children():
                if isinstance(child, Label) and child.cget('text') == "📚":
                    child.config(text="✍️")
                    break

    menu_frame = Frame(main_container, bg='#ffffff')
    menu_frame.pack(fill='both', expand=True, padx=50)

    def create_menu_button(parent, text, command, icon="", bg_color="#3498db", hover_color="#2980b9"):
        button_container = Frame(parent, bg='#ffffff', height=100)
        button_container.pack(fill='x', pady=15)
        button_container.pack_propagate(False)

        button_inner = Frame(button_container, bg=bg_color, relief='flat', bd=0)
        button_inner.pack(fill='both', expand=True, padx=3, pady=3)
        button_inner.configure(takefocus=1)

        shadow_frame = Frame(button_container, bg='#bdc3c7', height=100)
        shadow_frame.place(x=6, y=6, relwidth=1, relheight=1)
        button_inner.lift()

        icon_label = None
        if icon:
            icon_label = Label(button_inner, text=icon, font=("Arial", 28), bg=bg_color, fg='white')
            icon_label.pack(side='left', padx=(40, 30), pady=30)

        text_label = Label(button_inner, text=text, font=("Arial", 16, "bold"),
                          bg=bg_color, fg='white', anchor='w')
        text_label.pack(side='left', fill='x', expand=True, pady=30)

        arrow_label = Label(button_inner, text="→", font=("Arial", 24, "bold"),
                           bg=bg_color, fg='white')
        arrow_label.pack(side='right', padx=(30, 40), pady=30)

        def on_enter(event):
            button_inner.configure(bg=hover_color)
            for widget in (icon_label, text_label, arrow_label):
                if widget:
                    widget.configure(bg=hover_color)

        def on_leave(event):
            button_inner.configure(bg=bg_color)
            for widget in (icon_label, text_label, arrow_label):
                if widget:
                    widget.configure(bg=bg_color)

        def on_click(event=None):
            button_inner.configure(bg='#1a252f')
            writer_window.after(100, lambda: button_inner.configure(bg=hover_color))
            writer_window.after(150, command)

        widgets_to_bind = [button_inner, text_label, arrow_label]
        if icon_label:
            widgets_to_bind.append(icon_label)

        for w in widgets_to_bind:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)
            w.bind("<Return>", on_click)
            w.configure(cursor="hand2")

    # Підключаємо функції
    create_menu_button(menu_frame, "Переглянути мої книги",
                      lambda: show_books_by_author(user_login),
                      "📖", "#3498db", "#2980b9")

    create_menu_button(menu_frame, "Додати нову книгу",
                      lambda: show_add_book_window(user_login),
                      "➕", "#27ae60", "#229954")

    create_menu_button(menu_frame, "Створити збірку",
                      show_collection_window,
                      "📚", "#e67e22", "#d68910")

    create_menu_button(menu_frame, "Редагувати мої книги",
                      lambda: show_books_by_author(user_login),
                      "✏️", "#9b59b6", "#8e44ad")

    # Вихід
    exit_container = Frame(menu_frame, bg='#ffffff', height=100)
    exit_container.pack(fill='x', pady=(40, 0))
    exit_container.pack_propagate(False)

    exit_button = Button(exit_container, text="🚪  Вийти", font=("Arial", 16, "bold"),
                         bg='#e74c3c', fg='white', relief='flat', bd=0,
                         activebackground='#c0392b', activeforeground='white',
                         cursor='hand2', command=lambda: go_to_login(writer_window),
                         height=2)
    exit_button.pack(fill='both', expand=True, padx=3, pady=3)
    exit_button.bind('<Return>', lambda e: go_to_login(writer_window))

    footer_frame = Frame(main_container, bg='#ffffff', height=80)
    footer_frame.pack(fill='x', side='bottom', pady=(30, 0))

    footer_line = Frame(footer_frame, bg='#bdc3c7', height=2)
    footer_line.pack(fill='x', pady=(20, 0))

    footer_label = Label(footer_frame, text="Система управління бібліотекою • Версія 1.0",
                         font=("Arial", 12), bg='#ffffff', fg='#7f8c8d')
    footer_label.pack(pady=(20, 0))

    writer_window.mainloop()
