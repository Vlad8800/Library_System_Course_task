import csv
import json
from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
from tkcalendar import DateEntry
import tkinter.font as tkFont
from datetime import date, timedelta

try:
    from database import get_db_connection
    from utils import get_books, get_reading_rooms
    import login_window
except ImportError:
    def get_db_connection():
        class MockConnection:
            def cursor(self):
                return MockCursor()
            def close(self):
                pass
            def commit(self):
                pass
            def rollback(self):
                pass
        
        class MockCursor:
            def execute(self, query, params=None):
                return self
            def fetchall(self):
                return []
            def fetchone(self):
                return None
            def close(self):
                pass
        
        return MockConnection()
    
    def get_books():
        return [(1, "Тестова книга 1"), (2, "Тестова книга 2")]
    
    def get_reading_rooms():
        return [(1, "Читальний зал 1"), (2, "Читальний зал 2")]
    
    class login_window:
        @staticmethod
        def show_login_window():
            print("Показати окно логіну")

def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT book_id, title FROM Books")
    books = cursor.fetchall()
    conn.close()
    return books

def get_reading_rooms():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT room_id, name FROM ReadingRooms")
    rooms = cursor.fetchall()
    conn.close()
    return rooms

def get_libraries():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT library_id, name FROM Libraries")
    libraries = cursor.fetchall()
    conn.close()
    return libraries

def get_reading_rooms_by_library(library_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT room_id, name FROM ReadingRooms WHERE library_id = %s", (library_id,))
    rooms = cursor.fetchall()
    conn.close()
    return rooms

def get_publishers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT publisher_id, name FROM Publishers")
    publishers = cursor.fetchall()
    conn.close()
    return publishers

def setup_keyboard_bindings(window, is_main_window=False):
    def on_f1(event):
        show_help_window()
        return "break"
    
    def on_escape(event):
        if isinstance(window, tk.Toplevel):
            window.destroy()
        else:
            if messagebox.askyesno("Підтвердження", "Вийти з облікового запису та повернутися до вікна входу?"):
                window.destroy()
                login_window.show_login_window()
        return "break"
    
    def on_tab(event):
        try:
            event.widget.tk_focusNext().focus()
        except:
            pass
        return "break"
    
    def on_shift_tab(event):
        try:
            event.widget.tk_focusPrev().focus()
        except:
            pass
        return "break"
    
    def on_enter(event):
        if isinstance(event.widget, (tk.Entry, ttk.Combobox, tk.Text, tk.Spinbox)):
            return
            
        for widget in window.winfo_children():
            if isinstance(widget, tk.Button) and widget['state'] == 'normal':
                if widget.focus_get() == widget:
                    widget.invoke()
                    return "break"
        
        for widget in window.winfo_children():
            if isinstance(widget, tk.Button) and widget['state'] == 'normal':
                text_lower = widget['text'].lower()
                if any(keyword in text_lower for keyword in ['ок', 'зберегти', 'так', 'підтвердити', 'додати', 'виконати']):
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
            if not isinstance(child, (tk.Menu)):
                child.bind('<F1>', on_f1)
                child.bind('<Escape>', on_escape)
                child.bind('<Tab>', on_tab)
                child.bind('<Shift-Tab>', on_shift_tab)
                child.bind('<Return>', on_enter)
                child.bind('<Key>', ignore_unbound_keys)
                bind_recursive(child)
    
    bind_recursive(window)

def make_window_fullscreen(window):
    try:
        window.state('zoomed')
    except:
        window.attributes('-zoomed', True)

    def toggle_fullscreen(event=None):
        window.attributes('-fullscreen', False)
    
    def exit_fullscreen(event=None):
        window.attributes('-fullscreen', False)
        window.destroy()
    
    window.bind('<F11>', toggle_fullscreen)
    window.bind('<Escape>', exit_fullscreen)

def show_help_window():
    help_window = tk.Toplevel()
    help_window.title("Довідка")
    make_window_fullscreen(help_window)
    
    setup_keyboard_bindings(help_window)
    
    title_label = tk.Label(help_window, text="Довідка по клавіатурним комбінаціям", 
                          font=("Arial", 16, "bold"), fg="darkblue")
    title_label.pack(pady=20)
    
    help_text = """

ОСНОВНІ КЛАВІШІ УПРАВЛІННЯ:

F1 - Відкрити довідку
ESC - Відміна / Повернення назад / Вихід
TAB - Перехід до наступного поля
Shift + TAB - Повернення до попереднього поля
Enter - Підтвердження / Виконання дії
F11 - Увімкнути/вимкнути повноекранний режим

ПРИКЛАДИ ВИКОРИСТАННЯ:

• Натисніть TAB для швидкого переміщення між полями форми
• Натисніть ESC для скасування дії або закриття вікна
• Натисніть Enter для підтвердження введених даних
• Використовуйте F1 для отримання довідки у будь-який момент
• Натисніть F11 для перемикання повноекранного режиму

ПОРАДИ:

• Більшість кнопок можна активувати клавішею Enter
• Вікна пошуку підтримують швидку навігацію клавішами
• Завжди можна повернутися назад клавішею ESC
• Для виходу з повноекранного режиму натисніть F11 або ESC
    """
    
    text_widget = tk.Text(help_window, wrap="word", font=("Arial", 11), 
                         padx=20, pady=20, bg="#f9f9f9")
    text_widget.insert("1.0", help_text)
    text_widget.config(state="disabled")
    text_widget.pack(fill="both", expand=True, padx=20, pady=10)
    
    close_btn = tk.Button(help_window, text="Закрити (ESC)", command=help_window.destroy,
                         bg="#4CAF50", fg="white", font=("Arial", 12), width=15)
    close_btn.pack(pady=10)
    
    close_btn.focus_set()

def fetch_all_authors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT author_id, name, surname FROM Authors ORDER BY surname, name")
    authors = cursor.fetchall()
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
    conn.close()
    return books

def refresh_after_book_creation():
    try:
        refresh_global_data()
        refresh_author_management_window()
        refresh_book_search_data()
        print("Всі дані оновлено після створення книги!")
        
    except Exception as e:
        print(f"Помилка при оновленні даних: {e}")

def refresh_after_collection_creation():
    try:
        refresh_global_data()
        refresh_author_management_window()
        refresh_book_search_data()
        print("Всі дані оновлено після створення збірки!")
        
    except Exception as e:
        print(f"Помилка при оновленні даних: {e}")

def refresh_global_data():
    try:
        global all_books, all_authors
        all_books = fetch_all_books()
        all_authors = fetch_all_authors()
    except Exception as e:
        print(f"Помилка оновлення глобальних даних: {e}")

def refresh_author_management_window():
    try:
        for window in tk._default_root.winfo_children():
            if isinstance(window, tk.Toplevel) and "Управління книгами авторів" in window.title():
                for widget in window.winfo_children():
                    if isinstance(widget, ttk.Combobox):
                        authors = fetch_all_authors()
                        author_map = {f"{surname} {name} (ID: {author_id})": author_id for author_id, name, surname in authors}
                        widget['values'] = list(author_map.keys())
                        break
                break
    except Exception as e:
        print(f"Помилка оновлення вікна авторів: {e}")

def refresh_book_search_data():
    try:
        for window in tk._default_root.winfo_children():
            if isinstance(window, tk.Toplevel) and "Пошук книг" in window.title():
                pass
    except Exception as e:
        print(f"Помилка оновлення пошуку: {e}")

def show_admin_author_management():
    author_window = tk.Toplevel()
    author_window.title("Адмін: Управління книгами авторів")
    make_window_fullscreen(author_window)
    setup_keyboard_bindings(author_window)

    author_window.configure(bg="#ECEFF1")

    header = tk.Canvas(author_window, height=90, bg="#2C3E50", highlightthickness=0)
    header.pack(fill="x")

    title_font = tkFont.Font(family="Segoe UI", size=22, weight="bold")
    subtitle_font = tkFont.Font(family="Segoe UI", size=12)

    header.create_text(35, 25, anchor="w",
                       text="Управління книгами авторів",
                       font=title_font, fill="white")
    header.create_text(35, 60, anchor="w",
                       text="Розширене управління, статистика та додавання книг",
                       font=subtitle_font, fill="#D0D3D4")

    body_container = tk.Frame(author_window, bg="#ECEFF1")
    body_container.pack(fill="both", expand=True)

    canvas = tk.Canvas(body_container, bg="#ECEFF1", highlightthickness=0)
    scrollbar = ttk.Scrollbar(body_container, orient="vertical", command=canvas.yview)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scrollable = tk.Frame(canvas, bg="#ECEFF1")

    scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    container_window = canvas.create_window((0, 0), window=scrollable, anchor="nw")

    canvas.bind("<Configure>", lambda e: canvas.itemconfigure(container_window, width=e.width))

    def create_section(title, icon):
        wrapper = tk.Frame(scrollable, bg="#ECEFF1")
        wrapper.pack(fill="x", padx=20, pady=10)

        frame = tk.Frame(wrapper, bg="white", bd=0)
        frame.pack(fill="x", expand=True)

        header = tk.Label(frame, text=f"{icon} {title}",
                          bg="#37474F", fg="white",
                          font=("Segoe UI", 13, "bold"),
                          anchor="w", padx=15, pady=8)
        header.pack(fill="x")

        content = tk.Frame(frame, bg="white", padx=20, pady=15)
        content.pack(fill="both", expand=True)

        return content

    author_section = create_section("Вибір автора", "👤")

    tk.Label(author_section, text="Оберіть автора:",
             font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")

    authors = fetch_all_authors()
    author_map = {f"{surname} {name} (ID: {author_id})": author_id
                  for author_id, name, surname in authors}

    author_combo = ttk.Combobox(author_section, values=list(author_map.keys()),
                                state="readonly", width=60)
    author_combo.pack(pady=10, anchor="w")

    actions_section = create_section("Дії з автором", "⚙️")

    def show_author_books():
        if not author_combo.get():
            messagebox.showwarning("Попередження", "Оберіть автора!")
            return
        author_id = author_map[author_combo.get()]
        show_books_by_author_admin(author_id, author_combo.get())

    def add_book_for_author():
        if not author_combo.get():
            messagebox.showwarning("Попередження", "Оберіть автора!")
            return
        author_id = author_map[author_combo.get()]
        show_add_book_window_admin(author_id, author_combo.get())

    def create_collection():
        show_collection_window()

    def make_btn(parent, text, cmd, color, hcolor):
        btn = tk.Button(
            parent,
            text=text, command=cmd,
            font=("Segoe UI", 11, "bold"),
            bg=color, fg="white",
            activebackground=hcolor, activeforeground="white",
            bd=0, relief="flat", padx=15, pady=8,
            cursor="hand2"
        )
        return btn

    row1 = tk.Frame(actions_section, bg="white")
    row1.pack(pady=5)

    make_btn(row1, "Переглянути книги автора", show_author_books,
             "#3498DB", "#2E86C1").pack(side="left", padx=5)

    make_btn(row1, "Додати книгу автору", add_book_for_author,
             "#27AE60", "#229954").pack(side="left", padx=5)

    make_btn(row1, "Створити збірку", create_collection,
             "#8E44AD", "#7D3C98").pack(side="left", padx=5)

    stats_section = create_section("Статистика", "📊")

    def show_author_stats():
        if not author_combo.get():
            messagebox.showwarning("Попередження", "Оберіть автора!")
            return
        author_id = author_map[author_combo.get()]
        show_author_statistics(author_id, author_combo.get())

    make_btn(stats_section, "Статистика автора", show_author_stats,
             "#E67E22", "#CA6F1E").pack(anchor="w", pady=5)

    close_btn = tk.Button(scrollable, text="Закрити (ESC)", command=author_window.destroy,
                          font=("Segoe UI", 11, "bold"),
                          bg="#E74C3C", fg="white",
                          activebackground="#C0392B",
                          padx=20, pady=10, bd=0, relief="flat")
    close_btn.pack(pady=25)

    author_combo.focus_set()

def show_books_by_author_admin(author_id, author_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT name, surname FROM Authors WHERE author_id = %s", (author_id,))
        author_info = cursor.fetchone()
        if not author_info:
            messagebox.showerror("Помилка", "Автор не знайдений")
            return

        name, surname = author_info

        cursor.execute("""
            SELECT b.book_id, b.title, b.year, b.languages, b.inventory_number, 
                   COALESCE(c.name, 'Без категорії')
            FROM Books b
            LEFT JOIN Categories c ON b.category_id = c.category_id
            WHERE b.author_id = %s
            ORDER BY b.title
        """, (author_id,))
        books = cursor.fetchall()

        books_window = tk.Toplevel()
        books_window.title(f"Книги автора: {surname} {name}")
        make_window_fullscreen(books_window)
        setup_keyboard_bindings(books_window)

        books_window.configure(bg="#ECEFF1")

        header = tk.Canvas(books_window, height=95, bg="#2C3E50", highlightthickness=0)
        header.pack(fill="x")

        title_font = tkFont.Font(family="Segoe UI", size=22, weight="bold")
        subtitle_font = tkFont.Font(family="Segoe UI", size=12)

        header.create_text(
            35, 28,
            anchor="w",
            text=f"Книги автора: {surname} {name}",
            font=title_font,
            fill="white"
        )

        header.create_text(
            35, 60,
            anchor="w",
            text="Перегляд, редагування та управління бібліотечними записами",
            font=subtitle_font,
            fill="#D0D3D4"
        )

        table_frame = tk.Frame(books_window, bg="#ECEFF1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Назва", "Рік", "Мова", "Інвентарний номер", "Категорія")

        tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), padding=6)
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        col_widths = [60, 350, 80, 120, 160, 180]

        for col, w in zip(columns, col_widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="w")

        for book in books:
            tree.insert("", "end", values=book)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        buttons_frame = tk.Frame(books_window, bg="#ECEFF1")
        buttons_frame.pack(pady=20)

        def make_btn(text, cmd, color, hover):
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=cmd,
                font=("Segoe UI", 12, "bold"),
                bg=color,
                fg="white",
                activebackground=hover,
                activeforeground="white",
                bd=0,
                relief="flat",
                padx=25,
                pady=12,
                cursor="hand2"
            )
            return btn

        def on_double_click(event):
            item = tree.selection()[0]
            book_id = tree.item(item)['values'][0]
            edit_book_admin(book_id, author_id)

        tree.bind("<Double-1>", on_double_click)

        def edit_selected():
            try:
                item = tree.selection()[0]
                book_id = tree.item(item)['values'][0]
                edit_book_admin(book_id, author_id)
            except:
                messagebox.showinfo("Увага", "Оберіть книгу!")

        def delete_selected():
            try:
                item = tree.selection()[0]
                book_id = tree.item(item)['values'][0]
                delete_selected_book(tree, author_id)
            except:
                messagebox.showinfo("Увага", "Оберіть книгу!")

        make_btn("Редагувати обрану", edit_selected, "#2980B9", "#2471A3").pack(side="left", padx=8)

        make_btn(
            "Додати нову книгу",
            lambda: show_add_book_window_admin(author_id, f"{surname} {name}"),
            "#27AE60",
            "#1E8449"
        ).pack(side="left", padx=8)

        make_btn("Закрити (ESC)", books_window.destroy, "#7F8C8D", "#626567").pack(side="left", padx=8)

    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка при завантаженні книг: {e}")

    finally:
        if 'conn' in locals():
            conn.close()

def edit_book_admin(book_id, author_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT title, year, languages, inventory_number, category_id, quantity, access_type
            FROM Books WHERE book_id = %s
        """, (book_id,))
        book_data = cursor.fetchone()

        if not book_data:
            messagebox.showerror("Помилка", "Книгу не знайдено")
            return

        title, year, language, inv_number, category_id, quantity, access_type = book_data

        cursor.execute("SELECT name FROM Categories WHERE category_id = %s", (category_id,))
        category_result = cursor.fetchone()
        category_name = category_result[0] if category_result else ""

    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка при завантаженні даних: {e}")
        return
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    edit_window = tk.Toplevel()
    edit_window.title("Редагування книги")
    make_window_fullscreen(edit_window)
    setup_keyboard_bindings(edit_window)

    edit_window.configure(bg="#ECEFF1")

    header = tk.Canvas(edit_window, height=95, bg="#2C3E50", highlightthickness=0)
    header.pack(fill="x")

    title_font = tkFont.Font(family="Segoe UI", size=22, weight="bold")
    subtitle_font = tkFont.Font(family="Segoe UI", size=12)

    header.create_text(
        40, 28,
        anchor="w",
        text="Редагування книги",
        font=title_font,
        fill="white"
    )

    header.create_text(
        40, 60,
        anchor="w",
        text=f"Редагування запису ID {book_id}",
        font=subtitle_font,
        fill="#D0D3D4"
    )

    form_container = tk.Frame(edit_window, bg="#ECEFF1")
    form_container.pack(fill="both", expand=True)

    form = tk.Frame(form_container, bg="white", padx=40, pady=40)
    form.pack(pady=40, ipadx=20, ipady=20)

    label_font = ("Segoe UI", 12, "bold")
    entry_font = ("Segoe UI", 11)

    def create_field(row, text, default_value):
        tk.Label(form, text=text, font=label_font, bg="white").grid(
            row=row, column=0, sticky="w", pady=8
        )
        entry = tk.Entry(form, font=entry_font, width=45)
        entry.grid(row=row, column=1, pady=8, padx=20)
        entry.insert(0, default_value if default_value else "")
        return entry

    title_entry = create_field(0, "Назва книги:", title)
    year_entry = create_field(1, "Рік виданся:", year)
    language_entry = create_field(2, "Мова:", language)
    inv_entry = create_field(3, "Інвентарний номер:", inv_number)
    quantity_entry = create_field(4, "Кількість:", quantity)

    tk.Label(form, text="Категорія:", font=label_font, bg="white").grid(row=5, column=0, sticky="w", pady=8)

    category_var = tk.StringVar(value=category_name)
    category_combo = ttk.Combobox(form, textvariable=category_var, font=entry_font, width=43)
    category_combo.grid(row=5, column=1, pady=8, padx=20)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Categories ORDER BY name")
        categories = [row[0] for row in cursor.fetchall()]
        category_combo['values'] = categories
    finally:
        cursor.close()
        conn.close()

    tk.Label(form, text="Тип доступу:", font=label_font, bg="white").grid(row=6, column=0, sticky="w", pady=8)

    access_var = tk.StringVar(value=access_type or "Тільки в читальній залі")
    access_combo = ttk.Combobox(form, textvariable=access_var, state="readonly", font=entry_font, width=43)
    access_combo['values'] = ("Тільки в читальній залі", "У читальній залі і вдома")
    access_combo.grid(row=6, column=1, pady=8, padx=20)

    def save_changes():
        new_title = title_entry.get().strip()
        new_year = year_entry.get().strip()
        new_language = language_entry.get().strip()
        new_inv = inv_entry.get().strip()
        new_quantity = quantity_entry.get().strip()
        new_category = category_var.get().strip()
        new_access = access_var.get()

        if not new_title:
            messagebox.showerror("Помилка", "Назва книги не може бути порожньою")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT category_id FROM Categories WHERE name = %s", (new_category,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Помилка", "Категорія не знайдена")
                return

            category_id_new = result[0]

            cursor.execute("""
                UPDATE Books SET 
                    title=%s, year=%s, languages=%s, 
                    inventory_number=%s, quantity=%s, 
                    category_id=%s, access_type=%s
                WHERE book_id=%s
            """, (
                new_title, new_year or None, new_language or None,
                new_inv, int(new_quantity or 1),
                category_id_new, new_access, book_id
            ))

            conn.commit()
            messagebox.showinfo("Успіх", "Зміни успішно збережено")
            edit_window.destroy()
            refresh_after_book_creation()

        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка при збереженні: {e}")
        finally:
            cursor.close()
            conn.close()

    btn_frame = tk.Frame(edit_window, bg="#ECEFF1")
    btn_frame.pack(pady=25)

    def make_btn(text, command, color, hover):
        btn = tk.Button(
            btn_frame, text=text, command=command, 
            font=("Segoe UI", 12, "bold"),
            bg=color, fg="white",
            activebackground=hover, activeforeground="white",
            bd=0, relief="flat",
            padx=35, pady=12,
            cursor="hand2"
        )
        return btn

    make_btn("Зберегти зміни (Enter)", save_changes, "#27AE60", "#1E8449").pack(side="left", padx=12)
    make_btn("Скасувати (ESC)", edit_window.destroy, "#C0392B", "#922B21").pack(side="left", padx=12)

    edit_window.bind("<Return>", lambda e: save_changes())

def show_add_book_window_admin(author_id, author_name):
    def generate_inventory_number():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Books")
            count = cursor.fetchone()[0]
            return f"INV-{count + 1:05d}"
        except:
            return "INV-00001"
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    def save_book():
        title = title_entry.get().strip()
        year = year_entry.get().strip()
        language = language_entry.get().strip()
        inventory_number = inv_var.get()
        category_name = category_var.get().strip()
        quantity = quantity_entry.get().strip()

        if not (title and category_name):
            messagebox.showerror("Помилка", "Заповніть обов'язкові поля")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT category_id FROM Categories WHERE name = %s",
                           (category_name,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Помилка", "Категорії не існує")
                return

            category_id = result[0]

            cursor.execute("""
                INSERT INTO Books 
                (title, author_id, category_id, year, languages, inventory_number, quantity)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                title, author_id, category_id,
                year or None, language or None,
                inventory_number,
                int(quantity) if quantity.isdigit() else 1
            ))

            conn.commit()
            messagebox.showinfo("Успіх", "Книгу успішно додано")
            add_window.destroy()
            refresh_after_book_creation()

        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка: {e}")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    add_window = tk.Toplevel()
    add_window.title(f"Додати книгу для {author_name}")
    make_window_fullscreen(add_window)
    setup_keyboard_bindings(add_window)
    add_window.configure(bg="#ECEFF1")

    header = tk.Canvas(add_window, height=95, bg="#2C3E50", highlightthickness=0)
    header.pack(fill="x")

    title_font = tkFont.Font(family="Segoe UI", size=22, weight="bold")
    subtitle_font = tkFont.Font(family="Segoe UI", size=12)

    header.create_text(
        40, 28, anchor="w",
        text=f"Додати книгу для автора",
        font=title_font, fill="white"
    )

    header.create_text(
        40, 60, anchor="w",
        text=f"Автор: {author_name}",
        font=subtitle_font, fill="#D0D3D4"
    )

    form_container = tk.Frame(add_window, bg="#ECEFF1")
    form_container.pack(fill="both", expand=True)

    form = tk.Frame(form_container, bg="white", padx=40, pady=40)
    form.pack(pady=40, ipadx=20, ipady=20)

    label_font = ("Segoe UI", 12, "bold")
    entry_font = ("Segoe UI", 11)

    def create_field(row, text, default=""):
        tk.Label(form, text=text, font=label_font, bg="white")\
            .grid(row=row, column=0, sticky="w", pady=8)
        e = tk.Entry(form, font=entry_font, width=45)
        e.insert(0, default)
        e.grid(row=row, column=1, pady=8, padx=20)
        return e

    title_entry = create_field(0, "Назва книги:*")
    year_entry = create_field(1, "Рік видання:")
    language_entry = create_field(2, "Мова:")

    tk.Label(form, text="Інвентарний номер:", font=label_font, bg="white")\
        .grid(row=3, column=0, sticky="w", pady=8)

    inv_var = tk.StringVar(value=generate_inventory_number())
    inv_entry = tk.Entry(form, font=entry_font, width=45, textvariable=inv_var)
    inv_entry.grid(row=3, column=1, pady=8, padx=20)

    quantity_entry = create_field(4, "Кількість:", "1")

    tk.Label(form, text="Категорія:*", font=label_font, bg="white")\
        .grid(row=5, column=0, sticky="w", pady=8)

    category_var = tk.StringVar()
    category_combo = ttk.Combobox(form, textvariable=category_var,
                                  font=entry_font, width=43)
    category_combo.grid(row=5, column=1, pady=8, padx=20)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Categories ORDER BY name")
        categories = [row[0] for row in cursor.fetchall()]
        category_combo['values'] = categories
        if categories:
            category_combo.set(categories[0])
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

    btn_frame = tk.Frame(add_window, bg="#ECEFF1")
    btn_frame.pack(pady=30)

    def make_btn(text, cmd, color, hover):
        btn = tk.Button(
            btn_frame, text=text, command=cmd,
            font=("Segoe UI", 12, "bold"),
            bg=color, fg="white",
            activebackground=hover, activeforeground="white",
            bd=0, relief="flat",
            padx=35, pady=12, cursor="hand2"
        )
        return btn

    make_btn("Зберегти книгу (Enter)", save_book, "#27AE60", "#1E8449")\
        .pack(side="left", padx=15)

    make_btn("Скасувати (ESC)", add_window.destroy, "#C0392B", "#922B21")\
        .pack(side="left", padx=15)

    add_window.bind('<Return>', lambda e: save_book())
    title_entry.focus_set()

def delete_selected_book(tree, author_id):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Увага", "Оберіть книгу для видалення")
        return
    
    book_id = tree.item(selected[0])['values'][0]
    book_title = tree.item(selected[0])['values'][1]
    
    if not messagebox.askyesno("Підтвердження", f"Ви впевнені, що хочете видалити книгу '{book_title}'?"):
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM Books WHERE book_id = %s", (book_id,))
        conn.commit()
        
        messagebox.showinfo("Успіх", "Книгу успішно видалено")
        show_books_by_author_admin(author_id, "")
        
        refresh_after_book_creation()
        
    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка при видаленні: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def show_author_statistics(author_id, author_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_books,
                SUM(quantity) as total_copies,
                AVG(year) as avg_year,
                COUNT(DISTINCT languages) as unique_languages
            FROM Books 
            WHERE author_id = %s
        """, (author_id,))
        
        stats = cursor.fetchone()
        total_books, total_copies, avg_year, unique_languages = stats
        
        cursor.execute("""
            SELECT c.name, COUNT(*) as book_count
            FROM Books b
            JOIN Categories c ON b.category_id = c.category_id
            WHERE b.author_id = %s
            GROUP BY c.name
            ORDER BY book_count DESC
        """, (author_id,))
        
        categories_stats = cursor.fetchall()
        
        stats_window = tk.Toplevel()
        stats_window.title(f"Статистика: {author_name}")
        make_window_fullscreen(stats_window)
        setup_keyboard_bindings(stats_window)
        
        tk.Label(stats_window, text=f"Статистика автора: {author_name}", 
                font=("Arial", 16, "bold")).pack(pady=10)
        
        main_stats_frame = tk.LabelFrame(stats_window, text="Основна статистика", padx=10, pady=10)
        main_stats_frame.pack(fill="x", padx=10, pady=5)
        
        stats_text = f"""
        Загальна кількість книг: {total_books}
        Загальна кількість примірників: {total_copies or 0}
        Мов: {unique_languages or 0}
        Середній рік видання: {int(avg_year) if avg_year else 'Н/Д'}
        """
        
        tk.Label(main_stats_frame, text=stats_text, font=("Arial", 11), 
                justify="left").pack(anchor="w")
        
        if categories_stats:
            categories_frame = tk.LabelFrame(stats_window, text="Книги за категоріями", padx=10, pady=10)
            categories_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            for category, count in categories_stats:
                tk.Label(categories_frame, text=f"• {category}: {count} книг", 
                        font=("Arial", 10)).pack(anchor="w")
        
        tk.Button(stats_window, text="Закрити (ESC)", command=stats_window.destroy,
                 bg="gray", fg="white").pack(pady=10)
        
    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка при завантаженні статистики: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def show_collection_window():
    def generate_collection_inventory():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Collections")
            count = cursor.fetchone()[0]
            return f"COLL-{count + 1:05d}"
        except:
            return "COLL-00001"
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    window = tk.Toplevel()
    window.title("Створення збірки")
    make_window_fullscreen(window)
    window.grab_set()
    
    setup_keyboard_bindings(window)

    selected_authors = []
    selected_books = []

    tk.Label(window, text="Створення нової збірки", 
             font=("Arial", 16, "bold"), fg="darkblue").pack(pady=15)

    info_frame = tk.LabelFrame(window, text="Основна інформація", padx=10, pady=10)
    info_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(info_frame, text="Назва збірки:*", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=8)
    title_entry = tk.Entry(info_frame, width=60, font=("Arial", 11))
    title_entry.grid(row=0, column=1, pady=8, padx=10)

    tk.Label(info_frame, text="Тип збірки:*", font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=8)
    type_var = tk.StringVar()
    type_combo = ttk.Combobox(info_frame, textvariable=type_var, width=57, state="readonly")
    type_combo.grid(row=1, column=1, pady=8, padx=10)

    default_types = ('книги', 'журнали', 'газети', 'збірники статей', 
                     'збірники віршів', 'дисертації', 'реферати', 'збірники доповідей')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT name FROM BookTypes ORDER BY name")
            book_types = [row[0] for row in cursor.fetchall()]
            if book_types:
                type_combo['values'] = book_types
            else:
                type_combo['values'] = default_types
        except Exception:
            type_combo['values'] = default_types
                
    except Exception as e:
        print(f"Помилка завантаження типів: {e}")
        type_combo['values'] = default_types
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

    details_frame = tk.Frame(info_frame)
    details_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=10)

    tk.Label(details_frame, text="Рік:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
    year_entry = tk.Entry(details_frame, width=15)
    year_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(details_frame, text="Мова:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
    language_entry = tk.Entry(details_frame, width=15)
    language_entry.grid(row=0, column=3, padx=5, pady=2)

    tk.Label(details_frame, text="Кількість:").grid(row=0, column=4, padx=5, pady=2, sticky="w")
    quantity_entry = tk.Entry(details_frame, width=15)
    quantity_entry.insert(0, "1")
    quantity_entry.grid(row=0, column=5, padx=5, pady=2)

    tk.Label(details_frame, text="Тип доступу:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    access_var = tk.StringVar()
    access_combo = ttk.Combobox(details_frame, textvariable=access_var, width=20, state="readonly")
    access_combo['values'] = ('Тільки в читальній залі', 'У читальній залі і вдома')
    access_combo.grid(row=1, column=1, padx=5, pady=2)
    access_combo.current(0)

    tk.Label(details_frame, text="Інвентарний номер:").grid(row=1, column=2, padx=5, pady=2, sticky="w")
    inventory_entry = tk.Entry(details_frame, width=20)
    inventory_entry.insert(0, generate_collection_inventory())
    inventory_entry.grid(row=1, column=3, padx=5, pady=2)

    selection_container = tk.Frame(window)
    selection_container.pack(fill="both", expand=True, padx=10, pady=10)

    left_frame = tk.Frame(selection_container)
    left_frame.pack(side="left", fill="both", expand=True, padx=5)

    authors_frame = tk.LabelFrame(left_frame, text="Оберіть авторів", font=("Arial", 11, "bold"))
    authors_frame.pack(fill="both", expand=True, pady=5)

    all_authors = fetch_all_authors()

    author_columns = ("author_id", "name", "surname")
    author_tree = ttk.Treeview(authors_frame, columns=author_columns, show="headings", height=8)
    
    author_tree.heading("author_id", text="ID")
    author_tree.heading("name", text="Ім'я")
    author_tree.heading("surname", text="Прізвище")
    
    author_tree.column("author_id", width=50)
    author_tree.column("name", width=120)
    author_tree.column("surname", width=120)

    for author in all_authors:
        author_tree.insert("", "end", values=author)

    author_scrollbar = ttk.Scrollbar(authors_frame, orient="vertical", command=author_tree.yview)
    author_tree.configure(yscrollcommand=author_scrollbar.set)

    author_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    author_scrollbar.pack(side="right", fill="y", pady=5)

    right_frame = tk.Frame(selection_container)
    right_frame.pack(side="right", fill="both", expand=True, padx=5)

    books_frame = tk.LabelFrame(right_frame, text="Оберіть книги", font=("Arial", 11, "bold"))
    books_frame.pack(fill="both", expand=True, pady=5)

    all_books = fetch_all_books()

    book_columns = ("book_id", "title", "author_name", "author_surname")
    book_tree = ttk.Treeview(books_frame, columns=book_columns, show="headings", height=8)
    
    book_tree.heading("book_id", text="ID")
    book_tree.heading("title", text="Назва книги")
    book_tree.heading("author_name", text="Ім'я автора")
    book_tree.heading("author_surname", text="Прізвище автора")
    
    book_tree.column("book_id", width=50)
    book_tree.column("title", width=200)
    book_tree.column("author_name", width=100)
    book_tree.column("author_surname", width=100)

    for book in all_books:
        book_tree.insert("", "end", values=book)

    book_scrollbar = ttk.Scrollbar(books_frame, orient="vertical", command=book_tree.yview)
    book_tree.configure(yscrollcommand=book_scrollbar.set)

    book_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    book_scrollbar.pack(side="right", fill="y", pady=5)

    selected_frame = tk.LabelFrame(window, text="Обрані елементи", font=("Arial", 11, "bold"), padx=10, pady=10)
    selected_frame.pack(fill="x", padx=10, pady=5)

    selected_listbox = tk.Listbox(selected_frame, height=6, font=("Arial", 10))
    selected_scrollbar = ttk.Scrollbar(selected_frame, orient="vertical", command=selected_listbox.yview)
    selected_listbox.configure(yscrollcommand=selected_scrollbar.set)
    
    selected_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    selected_scrollbar.pack(side="right", fill="y", pady=5)

    def update_selected_items_list():
        selected_listbox.delete(0, tk.END)
        
        for author_id in selected_authors:
            for author in all_authors:
                if author[0] == author_id:
                    selected_listbox.insert(tk.END, f"АВТОР: {author[2]} {author[1]} (ID: {author_id})")
        
        for book_id in selected_books:
            for book in all_books:
                if book[0] == book_id:
                    selected_listbox.insert(tk.END, f"КНИГА: {book[1]} - {book[3]} {book[2]} (ID: {book_id})")

    def add_author():
        selected = author_tree.selection()
        if not selected:
            messagebox.showwarning("Увага", "Оберіть автора зі списку!")
            return
            
        author_id = author_tree.item(selected[0])['values'][0]
        if author_id not in selected_authors:
            selected_authors.append(author_id)
            update_selected_items_list()
            messagebox.showinfo("Успіх", "Автора додано до збірки!")
        else:
            messagebox.showwarning("Увага", "Цей автор вже доданий до збірки!")

    def add_book():
        selected = book_tree.selection()
        if not selected:
            messagebox.showwarning("Увага", "Оберіть книгу зі списку!")
            return
            
        book_id = book_tree.item(selected[0])['values'][0]
        if book_id not in selected_books:
            selected_books.append(book_id)
            update_selected_items_list()
            messagebox.showinfo("Успіх", "Книгу додано до збірки!")
        else:
            messagebox.showwarning("Увага", "Ця книга вже додана до збірки!")

    def remove_selected():
        selected = selected_listbox.curselection()
        if not selected:
            messagebox.showwarning("Увага", "Оберіть елемент для видалення!")
            return
            
        index = selected[0]
        item_text = selected_listbox.get(index)
        
        if item_text.startswith("АВТОР:"):
            author_id = int(item_text.split("ID: ")[1].rstrip(")"))
            if author_id in selected_authors:
                selected_authors.remove(author_id)
        elif item_text.startswith("КНИГА:"):
            book_id = int(item_text.split("ID: ")[1].rstrip(")"))
            if book_id in selected_books:
                selected_books.remove(book_id)
                
        update_selected_items_list()

    buttons_frame = tk.Frame(window)
    buttons_frame.pack(pady=10)

    tk.Button(buttons_frame, text="Додати автора", command=add_author,
             bg="blue", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
    
    tk.Button(buttons_frame, text="Додати книгу", command=add_book,
             bg="green", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
    
    tk.Button(buttons_frame, text="Видалити обране", command=remove_selected,
             bg="red", fg="white", font=("Arial", 10)).pack(side="left", padx=5)

    def save_collection():
        if not title_entry.get().strip():
            messagebox.showerror("Помилка", "Введіть назву збірки!")
            return
            
        if not type_var.get():
            messagebox.showerror("Помилка", "Оберіть тип збірки!")
            return
            
        if not selected_authors and not selected_books:
            messagebox.showerror("Помилка", "Додайте хоча б одного автора або книгу до збірки!")
            return

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            conn.autocommit = False

            type_name = type_var.get()
            cursor.execute("SELECT type_id FROM BookTypes WHERE name = %s", (type_name,))
            type_result = cursor.fetchone()
            
            if type_result:
                type_id = type_result[0]
            else:
                cursor.execute("INSERT INTO BookTypes (name) VALUES (%s)", (type_name,))
                type_id = cursor.lastrowid

            main_author_id = selected_authors[0] if selected_authors else None
            if not main_author_id and selected_books:
                first_book_id = selected_books[0]
                cursor.execute("SELECT author_id FROM Books WHERE book_id = %s", (first_book_id,))
                author_result = cursor.fetchone()
                if author_result:
                    main_author_id = author_result[0]

            cursor.execute("""
                INSERT INTO Collections (title, year, languages, quantity, 
                                       access_type, inventory_number, type_id, author_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                title_entry.get().strip(),
                year_entry.get().strip() if year_entry.get().strip() else None,
                language_entry.get().strip() if language_entry.get().strip() else None,
                int(quantity_entry.get()) if quantity_entry.get().strip().isdigit() else 1,
                access_var.get(),
                inventory_entry.get().strip(),
                type_id,
                main_author_id
            ))
            
            collection_id = cursor.lastrowid

            added_books_count = 0
            
            for author_id in selected_authors:
                cursor.execute("SELECT book_id FROM Books WHERE author_id = %s", (author_id,))
                author_books = cursor.fetchall()
                for (book_id,) in author_books:
                    try:
                        cursor.execute("""
                            INSERT INTO CollectionItems (collection_id, book_id)
                            VALUES (%s, %s)
                        """, (collection_id, book_id))
                        added_books_count += 1
                    except Exception:
                        pass

            for book_id in selected_books:
                try:
                    cursor.execute("""
                        INSERT INTO CollectionItems (collection_id, book_id)
                        VALUES (%s, %s)
                    """, (collection_id, book_id))
                    added_books_count += 1
                except Exception:
                    pass

            collection_book_inventory = f"COL-BOOK-{collection_id:05d}"
            
            cursor.execute("""
                INSERT INTO Books (title, author_id, year, languages, quantity, 
                                 access_type, inventory_number, collection_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                f"[ЗБІРКА] {title_entry.get().strip()}",
                main_author_id,
                year_entry.get().strip() if year_entry.get().strip() else None,
                language_entry.get().strip() if language_entry.get().strip() else None,
                int(quantity_entry.get()) if quantity_entry.get().strip().isdigit() else 1,
                access_var.get(),
                collection_book_inventory,
                collection_id
            ))

            conn.commit()
            
            messagebox.showinfo("Успіх!", 
                              f"Збірку '{title_entry.get().strip()}' успішно створено!\n\n"
                              f"Статистика:\n"
                              f"• Авторів: {len(selected_authors)}\n"
                              f"• Книг: {added_books_count}\n"
                              f"• ID збірки: {collection_id}\n"
                              f"• Інвентарний номер: {inventory_entry.get().strip()}")
            
            window.destroy()
            
            refresh_after_collection_creation()

        except Exception as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Помилка", f"Не вдалося створити збірку:\n{str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    save_frame = tk.Frame(window)
    save_frame.pack(pady=20)

    tk.Button(save_frame, text="Зберегти збірку (Enter)", command=save_collection,
             bg="green", fg="white", font=("Arial", 12, "bold"), padx=20).pack(side="left", padx=10)
    
    tk.Button(save_frame, text="Скасувати (ESC)", command=window.destroy,
             bg="red", fg="white", font=("Arial", 12, "bold"), padx=20).pack(side="left", padx=10)

    window.bind('<Return>', lambda e: save_collection())
    
    author_tree.bind('<Double-1>', lambda e: add_author())
    book_tree.bind('<Double-1>', lambda e: add_book())
    
    selected_listbox.bind('<Delete>', lambda e: remove_selected())

    title_entry.focus_set()

    window.minsize(900, 700)

def show_popular_books_window():
    popular_window = tk.Toplevel()
    popular_window.title("Найпопулярніші книги бібліотеки")
    make_window_fullscreen(popular_window)
    
    setup_keyboard_bindings(popular_window)
    
    title_label = tk.Label(popular_window, text="Найпопулярніші книги бібліотеки", 
                          font=("Arial", 18, "bold"), fg="darkblue")
    title_label.pack(pady=20)
    
    top_frame = ttk.LabelFrame(popular_window, text="ТОП-3 Найпопулярніші твори", padding=20)
    top_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    top_books_frame = tk.Frame(top_frame)
    top_books_frame.pack(fill="both", expand=True)
    
    all_books_frame = ttk.LabelFrame(popular_window, text="Всі книги з статистикою видач", padding=10)
    all_books_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    columns = ("Позиція", "Назва", "Автор", "Категорія", "Кількість видач", "В наявності")
    all_books_tree = ttk.Treeview(all_books_frame, columns=columns, show="headings", height=10)
    
    for col in columns:
        all_books_tree.heading(col, text=col)
        all_books_tree.column(col, width=130)
    
    scrollbar = ttk.Scrollbar(all_books_frame, orient="vertical", command=all_books_tree.yview)
    all_books_tree.configure(yscrollcommand=scrollbar.set)
    
    all_books_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def load_popular_books():
        for widget in top_books_frame.winfo_children():
            widget.destroy()
        
        for item in all_books_tree.get_children():
            all_books_tree.delete(item)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SHOW COLUMNS FROM Books LIKE 'borrowed_count'")
            column_exists = cursor.fetchone()
            
            if not column_exists:
                cursor.execute("ALTER TABLE Books ADD COLUMN borrowed_count INT DEFAULT 0")
                conn.commit()
            
            cursor.execute("""
                SELECT b.title, CONCAT(a.name, ' ', a.surname) as author, c.name as category, 
                       b.year, COALESCE(b.borrowed_count, 0) as borrowed_count, b.quantity
                FROM Books b
                JOIN Authors a ON b.author_id = a.author_id
                LEFT JOIN Categories c ON b.category_id = c.category_id
                ORDER BY COALESCE(b.borrowed_count, 0) DESC
                LIMIT 3
            """)
            
            top_books = cursor.fetchall()
            
            for i, book in enumerate(top_books):
                create_book_card(top_books_frame, book, i + 1)
            
            cursor.execute("""
                SELECT b.title, CONCAT(a.name, ' ', a.surname) as author, c.name as category, 
                       COALESCE(b.borrowed_count, 0) as borrowed_count, b.quantity
                FROM Books b
                JOIN Authors a ON b.author_id = a.author_id
                LEFT JOIN Categories c ON b.category_id = c.category_id
                ORDER BY COALESCE(b.borrowed_count, 0) DESC
            """)
            
            all_books = cursor.fetchall()
            
            for i, book in enumerate(all_books, 1):
                title, author, category, borrowed_count, quantity = book
                all_books_tree.insert("", "end", values=(i, title, author, category or "Не вказана", borrowed_count, quantity))
        
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка при завантаженні даних:\n{e}")
        finally:
            conn.close()
    
    def create_book_card(parent_frame, book, position):
        title, author, category, year, borrowed_count, quantity = book
        
        colors = {1: "#FFD700", 2: "#C0C0C0", 3: "#CD7F32"}
        bg_color = colors.get(position, "#f0f0f0")
        
        card_frame = tk.Frame(parent_frame, bg=bg_color, relief="raised", bd=2)
        card_frame.pack(fill="x", pady=10, padx=20)
        
        position_label = tk.Label(card_frame, text=f"#{position}", 
                                 font=("Arial", 24, "bold"), bg=bg_color)
        position_label.pack(side="left", padx=20, pady=10)
        
        info_frame = tk.Frame(card_frame, bg=bg_color)
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        title_label = tk.Label(info_frame, text=title, 
                              font=("Arial", 16, "bold"), bg=bg_color)
        title_label.pack(anchor="w")
        
        author_label = tk.Label(info_frame, text=f"Автор: {author}", 
                               font=("Arial", 12), bg=bg_color)
        author_label.pack(anchor="w")
        
        if category:
            category_label = tk.Label(info_frame, text=f"Категорія: {category}", 
                                     font=("Arial", 10), bg=bg_color, fg="gray")
            category_label.pack(anchor="w")
        
        if year:
            year_label = tk.Label(info_frame, text=f"Рік: {year}", 
                                 font=("Arial", 10), bg=bg_color, fg="gray")
            year_label.pack(anchor="w")
        
        stats_frame = tk.Frame(card_frame, bg=bg_color)
        stats_frame.pack(side="right", padx=20, pady=10)
        
        borrowed_label = tk.Label(stats_frame, text=f"Видач: {borrowed_count}", 
                                 font=("Arial", 14, "bold"), bg=bg_color, fg="darkred")
        borrowed_label.pack()
        
        quantity_label = tk.Label(stats_frame, text=f"В наявності: {quantity}", 
                                 font=("Arial", 10), bg=bg_color, fg="darkgreen")
        quantity_label.pack()
    
    def show_add_borrow_window():
        add_window = tk.Toplevel(popular_window)
        add_window.title("Додати видачу книги")
        make_window_fullscreen(add_window)
        
        setup_keyboard_bindings(add_window)
        
        tk.Label(add_window, text="Виберіть книгу:", font=("Arial", 12)).pack(pady=10)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.book_id, b.title, CONCAT(a.name, ' ', a.surname) as author
            FROM Books b 
            JOIN Authors a ON b.author_id = a.author_id
            ORDER BY b.title
        ''')
        books = cursor.fetchall()
        conn.close()
        
        book_var = tk.StringVar()
        book_combo = ttk.Combobox(add_window, textvariable=book_var, width=60)
        book_combo['values'] = [f"{book[1]} - {book[2]}" for book in books]
        book_combo.pack(pady=10)
        
        def add_borrow():
            if not book_var.get():
                messagebox.showwarning("Попередження", "Виберіть книгу!")
                return
            
            selected_index = book_combo.current()
            if selected_index >= 0:
                book_id = books[selected_index][0]
                
                conn = get_db_connection()
                cursor = conn.cursor()
                
                try:
                    cursor.execute("SHOW COLUMNS FROM Books LIKE 'borrowed_count'")
                    if not cursor.fetchone():
                        cursor.execute("ALTER TABLE Books ADD COLUMN borrowed_count INT DEFAULT 0")
                    
                    cursor.execute("UPDATE Books SET borrowed_count = COALESCE(borrowed_count, 0) + 1 WHERE book_id = %s", 
                                   (book_id,))
                    conn.commit()
                    
                    messagebox.showinfo("Успішно", "Видачу додано!")
                    add_window.destroy()
                    load_popular_books()
                except Exception as e:
                    messagebox.showerror("Помилка", f"Помилка при додаванні видачі:\n{e}")
                finally:
                    conn.close()
        
        add_btn = tk.Button(add_window, text="Додати видачу (Enter)", command=add_borrow,
                 bg="lightgreen", font=("Arial", 12))
        add_btn.pack(pady=20)
        add_btn.focus_set()
    
    control_frame = tk.Frame(popular_window)
    control_frame.pack(pady=10)
    
    refresh_btn = tk.Button(control_frame, text="Оновити дані", command=load_popular_books,
              bg="lightblue", font=("Arial", 12))
    refresh_btn.pack(side="left", padx=10)
    
    add_btn = tk.Button(control_frame, text="Додати видачу", command=show_add_borrow_window,
              bg="lightgreen", font=("Arial", 12))
    add_btn.pack(side="left", padx=10)

    close_btn = tk.Button(control_frame, text="Закрити (ESC)", command=popular_window.destroy,
              bg="lightcoral", font=("Arial", 12))
    close_btn.pack(side="left", padx=10)
    
    load_popular_books()

def find_books_by_work_or_author():
    search_window = tk.Toplevel()
    search_window.title("Пошук книг за назвою та автором")
    make_window_fullscreen(search_window)
    search_window.configure(bg="#F3F4F8")

    setup_keyboard_bindings(search_window)

    header = tk.Frame(search_window, bg="#1F4E79", height=90)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Пошук книг за назвою або автором",
        font=("Segoe UI", 26, "bold"),
        bg="#1F4E79",
        fg="white"
    ).pack(pady=20)

    container = tk.Frame(search_window, bg="#F3F4F8")
    container.pack(fill="both", expand=True, padx=30, pady=20)

    def card(parent):
        frame = tk.Frame(parent, bg="white", bd=1, relief="solid")
        frame.pack(fill="x", pady=10)
        return frame

    book_frame = card(container)

    tk.Label(
        book_frame,
        text="Пошук книги за назвою",
        font=("Segoe UI", 18, "bold"),
        bg="white"
    ).pack(anchor="w", padx=15, pady=(15, 5))

    tk.Label(book_frame, text="Введіть назву книги:", font=("Segoe UI", 12), bg="white").pack(anchor="w", padx=15)

    title_entry = tk.Entry(book_frame, width=70, font=("Segoe UI", 14))
    title_entry.pack(padx=15, pady=10)

    author_frame = card(container)

    tk.Label(
        author_frame,
        text="Пошук всіх книг автора",
        font=("Segoe UI", 18, "bold"),
        bg="white"
    ).pack(anchor="w", padx=15, pady=(15, 5))

    tk.Label(author_frame, text="Введіть ім'я або прізвище автора:", font=("Segoe UI", 12), bg="white").pack(anchor="w", padx=15)

    author_entry = tk.Entry(author_frame, width=70, font=("Segoe UI", 14))
    author_entry.pack(padx=15, pady=10)

    result_frame = tk.Frame(container, bg="white", bd=1, relief="solid")
    result_frame.pack(fill="both", expand=True, pady=10)

    tk.Label(
        result_frame,
        text="Результати пошуку",
        font=("Segoe UI", 18, "bold"),
        bg="white"
    ).pack(anchor="w", padx=15, pady=10)

    result_box = tk.Text(
        result_frame,
        width=100,
        height=25,
        wrap=tk.WORD,
        font=("Segoe UI", 13),
        bg="white",
        relief="flat"
    )
    result_box.pack(fill="both", expand=True, padx=20, pady=10)

    scrollbar = ttk.Scrollbar(result_box, command=result_box.yview)
    result_box.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

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
                       b.access_type, b.inventory_number
                FROM Books b
                JOIN Authors a ON b.author_id = a.author_id
                WHERE b.title LIKE %s
            """, (f"%{title_query}%",))

            books = cursor.fetchall()
            result_box.delete(1.0, tk.END)

            if not books:
                result_box.insert(tk.END, f"Книг з назвою '{title_query}' не знайдено.\n")
                return

            result_box.insert(tk.END, f"Знайдено книг: {len(books)}\n\n")

            for book_id, title, author, access, inv in books:
                result_box.insert(tk.END, f"──────────────────────────────\n")
                result_box.insert(tk.END, f"Назва: {title}\n")
                result_box.insert(tk.END, f"Автор: {author}\n")
                result_box.insert(tk.END, f"Інв. номер: {inv}\n")
                result_box.insert(tk.END, f"Доступ: {access}\n")

                cursor.execute("""
                    SELECT c.collection_id, c.title, c.year
                    FROM CollectionItems ci
                    JOIN Collections c ON ci.collection_id = c.collection_id
                    WHERE ci.book_id = %s
                """, (book_id,))
                cols = cursor.fetchall()

                if cols:
                    result_box.insert(tk.END, "Належить до збірок:\n")
                    for cid, ctitle, year in cols:
                        result_box.insert(tk.END, f"   • {ctitle} ({year}) [ID {cid}]\n")
                else:
                    result_box.insert(tk.END, "Не входить до збірок\n")

                result_box.insert(tk.END, "\n")

        finally:
            conn.close()

    def search_by_author():
        query = author_entry.get().strip()
        if not query:
            messagebox.showerror("Помилка", "Введіть ім'я або прізвище автора!")
            return

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT b.book_id, b.title, CONCAT(a.name, ' ', a.surname) AS author, 
                       b.access_type, b.inventory_number
                FROM Books b
                JOIN Authors a ON b.author_id = a.author_id
                WHERE a.name LIKE %s OR a.surname LIKE %s
                ORDER BY b.title
            """, (f"%{query}%", f"%{query}%"))

            books = cursor.fetchall()
            result_box.delete(1.0, tk.END)

            if not books:
                result_box.insert(tk.END, f"Книг автора '{query}' не знайдено.\n")
                return

            result_box.insert(tk.END, f"Автор: {query}\n")
            result_box.insert(tk.END, f"Знайдено книг: {len(books)}\n\n")

            for book_id, title, author, access, inv in books:
                result_box.insert(tk.END, "──────────────────────────────\n")
                result_box.insert(tk.END, f"Назва: {title}\n")
                result_box.insert(tk.END, f"Автор: {author}\n")
                result_box.insert(tk.END, f"Інв. номер: {inv}\n")
                result_box.insert(tk.END, f"Доступ: {access}\n")

                cursor.execute("""
                    SELECT c.collection_id, c.title, c.year
                    FROM CollectionItems ci
                    JOIN Collections c ON ci.collection_id = c.collection_id
                    WHERE ci.book_id = %s
                """, (book_id,))
                cols = cursor.fetchall()

                if cols:
                    result_box.insert(tk.END, "Належить до збірок:\n")
                    for cid, ctitle, year in cols:
                        result_box.insert(tk.END, f"   • {ctitle} ({year}) [ID {cid}]\n")
                else:
                    result_box.insert(tk.END, "Не входить до збірок\n")

                result_box.insert(tk.END, "\n")

        finally:
            conn.close()

    btn_frame = tk.Frame(container, bg="#F3F4F8")
    btn_frame.pack(pady=10)

    search_title_btn = tk.Button(
        btn_frame, text="Пошук за назвою", command=search_by_title,
        bg="#0078D4", fg="white", font=("Segoe UI", 13, "bold"),
        padx=30, pady=10
    )
    search_title_btn.pack(side="left", padx=5)

    search_author_btn = tk.Button(
        btn_frame, text="Пошук книг автора", command=search_by_author,
        bg="#2E8B57", fg="white", font=("Segoe UI", 13, "bold"),
        padx=30, pady=10
    )
    search_author_btn.pack(side="left", padx=5)

    def clear_results():
        result_box.delete(1.0, tk.END)
        title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)

    clear_btn = tk.Button(
        btn_frame, text="Очистити", command=clear_results,
        bg="#6E6E6E", fg="white", font=("Segoe UI", 13, "bold"),
        padx=20, pady=10
    )
    clear_btn.pack(side="left", padx=5)

    close_btn = tk.Button(
        btn_frame, text="Закрити", command=search_window.destroy,
        bg="#C62828", fg="white", font=("Segoe UI", 13, "bold"),
        padx=20, pady=10
    )
    close_btn.pack(side="left", padx=5)

    title_entry.focus_set()

def get_librarians_worked_in_room():
    search_window = tk.Toplevel()
    search_window.title("Бібліотекарі за читальним залом")
    make_window_fullscreen(search_window)
    search_window.configure(bg="#F0F2F5")

    setup_keyboard_bindings(search_window)

    header = tk.Frame(search_window, bg="#1F4E79", height=90)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Пошук бібліотекарів за читальним залом",
        font=("Segoe UI", 26, "bold"),
        bg="#1F4E79",
        fg="white"
    ).pack(pady=20)

    container = tk.Frame(search_window, bg="#F0F2F5")
    container.pack(fill="both", expand=True, pady=25)

    tk.Label(
        container,
        text="Оберіть бібліотеку:",
        bg="#F0F2F5",
        fg="#1F1F1F",
        font=("Segoe UI", 14, "bold")
    ).pack()

    libraries = get_libraries()
    library_map = {f"{name} (ID: {lib_id})": lib_id for lib_id, name in libraries}

    library_combo = ttk.Combobox(
        container,
        values=list(library_map.keys()),
        state="readonly",
        width=55,
        font=("Segoe UI", 12)
    )
    library_combo.pack(pady=10)
    library_combo.set("— Оберіть бібліотеку —")

    tk.Label(
        container,
        text="Оберіть читальний зал:",
        bg="#F0F2F5",
        fg="#1F1F1F",
        font=("Segoe UI", 14, "bold")
    ).pack()

    room_combo = ttk.Combobox(
        container,
        state="readonly",
        width=55,
        font=("Segoe UI", 12)
    )
    room_combo.pack(pady=10)

    def update_rooms(event=None):
        selected_library = library_combo.get()
        if not selected_library:
            room_combo["values"] = []
            room_combo.set("")
            return

        library_id = library_map[selected_library]
        rooms = get_reading_rooms_by_library(library_id)

        room_display = [f"{name} (ID: {room_id})" for room_id, name in rooms]
        room_combo["values"] = room_display

        if not room_display:
            room_combo.set("— Немає залів —")
        else:
            room_combo.set("— Оберіть читальний зал —")

    library_combo.bind("<<ComboboxSelected>>", update_rooms)

    result_card = tk.Frame(container, bg="white", bd=1, relief="solid")
    result_card.pack(padx=40, pady=20, fill="both", expand=True)

    result_text = tk.Text(
        result_card,
        font=("Segoe UI", 12),
        bg="white",
        fg="#333333",
        width=90,
        height=18,
        relief="flat",
        wrap=tk.WORD
    )
    result_text.pack(padx=20, pady=20, fill="both", expand=True)

    def search_librarians():
        result_text.delete(1.0, tk.END)

        selected_library = library_combo.get()
        selected_room = room_combo.get()

        if not selected_library or selected_library.startswith("—"):
            messagebox.showerror("Помилка", "Оберіть бібліотеку!")
            return

        if not selected_room or selected_room.startswith("—"):
            messagebox.showerror("Помилка", "Оберіть читальний зал!")
            return

        library_id = library_map[selected_library]
        room_id = selected_room.split("ID: ")[1].rstrip(")")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                l.librarian_id, 
                l.name, 
                u.login,
                COALESCE(stats.books_issued, 0) as books_issued,
                stats.first_work_date,
                stats.last_work_date
            FROM Librarians l
            INNER JOIN Users u ON l.librarian_id = u.user_id
            INNER JOIN ReadingRooms rr ON l.reading_room_id = rr.room_id
            LEFT JOIN (
                SELECT 
                    ib.librarian_id,
                    COUNT(ib.issue_id) as books_issued,
                    MIN(ib.issue_date) as first_work_date,
                    MAX(ib.issue_date) as last_work_date
                FROM IssuedBooks ib
                WHERE ib.room_id = %s
                GROUP BY ib.librarian_id
            ) stats ON l.librarian_id = stats.librarian_id
            WHERE l.reading_room_id = %s 
              AND rr.library_id = %s
            ORDER BY l.name
        """, (room_id, room_id, library_id))

        results = cursor.fetchall()
        conn.close()

        library_name = selected_library.split(" (ID")[0]
        room_name = selected_room.split(" (ID")[0]

        result_text.insert(
            tk.END,
            f"Бібліотека: {library_name}\n"
            f"Читальний зал: {room_name}\n\n",
        )

        if not results:
            result_text.insert(
                tk.END,
                "У цьому читальному залі немає бібліотекарів.\n"
            )
            return

        for lib_id, name, login, count, first, last in results:
            result_text.insert(
                tk.END,
                f"{name} (ID: {lib_id}, Логін: {login})\n"
                f"Видано книг: {count}\n"
            )
            if first and last:
                result_text.insert(
                    tk.END,
                    f"Перша видача: {first}\n"
                    f"Остання видача: {last}\n"
                )
            else:
                result_text.insert(
                    tk.END,
                    "Ще не видавав книги у цьому залі\n"
                )
            result_text.insert(tk.END, "\n")

        result_text.insert(tk.END, f"Всього знайдено: {len(results)}")

    btn_frame = tk.Frame(container, bg="#F0F2F5")
    btn_frame.pack(pady=10)

    search_btn = tk.Button(
        btn_frame,
        text="Знайти (Enter)",
        bg="#0078D4",
        fg="white",
        font=("Segoe UI", 13, "bold"),
        padx=25,
        pady=7,
        command=search_librarians
    )
    search_btn.pack(side="left", padx=10)

    close_btn = tk.Button(
        btn_frame,
        text="Закрити (ESC)",
        bg="#C62828",
        fg="white",
        font=("Segoe UI", 13, "bold"),
        padx=25,
        pady=7,
        command=search_window.destroy
    )
    close_btn.pack(side="left", padx=10)

    library_combo.focus_set()

def save_distribution(book_id, selected_room_ids, shelf, row):
    """Зберігає розподіл книги по читальних залах"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Видаляємо старі розміщення для цієї книги
        cursor.execute("DELETE FROM Placements WHERE book_id = %s", (book_id,))
        
        # Додаємо нові розміщення
        for room_id in selected_room_ids:
            cursor.execute("""
                INSERT INTO Placements (book_id, room_id, shelf, `row`) 
                VALUES (%s, %s, %s, %s)
            """, (book_id, room_id, shelf, row))
        
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def find_who_has_book():
    search_window = tk.Toplevel()
    search_window.title("Хто взяв книгу")
    make_window_fullscreen(search_window)
    search_window.configure(bg="#F0F2F5")

    setup_keyboard_bindings(search_window)

    header = tk.Frame(search_window, bg="#1F4E79", height=85)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Пошук: хто взяв книгу",
        font=("Segoe UI", 26, "bold"),
        bg="#1F4E79",
        fg="white"
    ).pack(pady=18)

    container = tk.Frame(search_window, bg="#F0F2F5")
    container.pack(fill="both", expand=True, pady=20)

    tk.Label(
        container,
        text="Оберіть книгу:",
        bg="#F0F2F5",
        fg="#1F1F1F",
        font=("Segoe UI", 14, "bold")
    ).pack(pady=(5, 5))

    books = get_books()
    book_map = {f"{title} (ID: {book_id})": book_id for book_id, title in books}

    book_combo = ttk.Combobox(
        container,
        values=list(book_map.keys()),
        state="readonly",
        width=55,
        font=("Segoe UI", 12)
    )
    book_combo.pack(pady=10)
    book_combo.set("— Оберіть книгу —")

    result_frame = tk.Frame(container, bg="white", bd=1, relief="solid")
    result_frame.pack(pady=20, padx=40, fill="both", expand=False)

    result_box = tk.Text(
        result_frame,
        font=("Segoe UI", 12),
        bg="white",
        fg="#333333",
        width=80,
        height=14,
        relief="flat"
    )
    result_box.pack(padx=15, pady=15)

    def search_book():
        selected_book = book_combo.get()
        if not selected_book or selected_book.startswith("—"):
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
                    status = f"повернення: {return_date}"

                result_box.insert(
                    tk.END,
                    f"{user_name}\n"
                    f"'{title}'\n"
                    f"Взято: {issue_date}\n"
                    f"{status}\n\n"
                )
        else:
            result_box.insert(tk.END, "Цю книгу зараз ніхто не тримає.\n")

    btn_frame = tk.Frame(container, bg="#F0F2F5")
    btn_frame.pack(pady=10)

    search_btn = tk.Button(
        btn_frame,
        text="Перевірити (Enter)",
        command=search_book,
        bg="#0078D4",
        fg="white",
        font=("Segoe UI", 13, "bold"),
        padx=20,
        pady=6
    )
    search_btn.pack(side="left", padx=10)

    close_btn = tk.Button(
        btn_frame,
        text="Закрити (ESC)",
        command=search_window.destroy,
        bg="#C62828",
        fg="white",
        font=("Segoe UI", 13, "bold"),
        padx=20,
        pady=6
    )
    close_btn.pack(side="left", padx=10)

    book_combo.focus_set()

def show_edit_book_window():
    edit_window = tk.Toplevel()
    edit_window.title("Редагування книги")
    make_window_fullscreen(edit_window)
    setup_keyboard_bindings(edit_window)
    edit_window.configure(bg="#ECEFF1")

    header = tk.Canvas(edit_window, height=95, bg="#2C3E50", highlightthickness=0)
    header.pack(fill="x")

    title_font = tkFont.Font(family="Segoe UI", size=22, weight="bold")
    header.create_text(
        40, 28, anchor="w",
        text="Редагування книги",
        font=title_font, fill="white"
    )
    header.create_text(
        40, 62, anchor="w",
        text="Оберіть книгу та відкоригуйте її властивості",
        font=("Segoe UI", 12), fill="#D0D3D4"
    )

    wrapper = tk.Frame(edit_window, bg="#ECEFF1")
    wrapper.pack(fill="both", expand=True)

    panel = tk.Frame(wrapper, bg="white", padx=40, pady=40)
    panel.pack(pady=40)

    label_font = ("Segoe UI", 13, "bold")
    entry_font = ("Segoe UI", 11)

    books = get_books()
    book_dict = {f"{title} (ID: {book_id})": book_id for book_id, title in books}

    rooms = get_reading_rooms()
    room_dict = {f"{name} (ID: {room_id})": room_id for room_id, name in rooms}

    publishers = get_publishers()
    publisher_dict = {name: publisher_id for publisher_id, name in publishers}

    def make_label(row, text):
        tk.Label(panel, text=text, font=label_font, bg="white")\
            .grid(row=row, column=0, sticky="w", pady=10)

    def make_entry(row):
        e = tk.Entry(panel, font=entry_font, width=45)
        e.grid(row=row, column=1, pady=10, padx=20)
        return e

    def make_combo(row, var, values):
        cb = ttk.Combobox(
            panel, values=values, font=entry_font,
            width=43, state="readonly",
            textvariable=var
        )
        cb.grid(row=row, column=1, pady=10, padx=20)
        return cb

    make_label(0, "Оберіть книгу:")
    book_var = tk.StringVar()
    book_combobox = make_combo(0, book_var, list(book_dict.keys()))

    make_label(1, "Тип доступу:")
    access_type_var = tk.StringVar()
    access_type_combobox = make_combo(
        1, access_type_var,
        ["У читальній залі і вдома", "Тільки в читальній залі"]
    )

    make_label(2, "Видавництво:")
    publisher_var = tk.StringVar()
    publisher_combobox = make_combo(2, publisher_var, list(publisher_dict.keys()))

    make_label(3, "Читальний зал:")
    room_var = tk.StringVar()
    room_combobox = make_combo(3, room_var, list(room_dict.keys()))

    make_label(4, "Полиця:")
    shelf_entry = make_entry(4)

    make_label(5, "Ряд:")
    row_entry = make_entry(5)

    make_label(6, "Кількість примірників:")
    quantity_entry = make_entry(6)

    def load_book_info(event):
        selected = book_var.get()
        if not selected:
            return

        book_id = book_dict[selected]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT access_type, quantity, publisher_id 
            FROM Books 
            WHERE book_id = %s
        """, (book_id,))
        data = cursor.fetchone()

        if data:
            access_type_var.set(data[0])
            quantity_entry.delete(0, tk.END)
            quantity_entry.insert(0, data[1])

            for name, pid in publisher_dict.items():
                if pid == data[2]:
                    publisher_var.set(name)

        cursor.execute("""
            SELECT room_id, shelf, `row`
            FROM Placements
            WHERE book_id = %s
            LIMIT 1
        """, (book_id,))
        place = cursor.fetchone()

        conn.close()

        if place:
            rid, shelf, row = place
            for name, rrid in room_dict.items():
                if rrid == rid:
                    room_var.set(name)

            shelf_entry.delete(0, tk.END)
            shelf_entry.insert(0, shelf)

            row_entry.delete(0, tk.END)
            row_entry.insert(0, row)

    book_combobox.bind("<<ComboboxSelected>>", load_book_info)

    def update_book():
        selected_book_label = book_var.get()
        if not selected_book_label:
            messagebox.showerror("Помилка", "Оберіть книгу.")
            return

        book_id = book_dict[selected_book_label]

        access_type = access_type_var.get().strip()
        publisher_name = publisher_var.get().strip()
        room_name = room_var.get().strip()
        shelf = shelf_entry.get().strip()
        row = row_entry.get().strip()
        quantity = quantity_entry.get().strip()

        if not (access_type and publisher_name and room_name and shelf and row and quantity):
            messagebox.showerror("Помилка", "Усі поля мають бути заповнені.")
            return

        try:
            quantity = int(quantity)
        except:
            messagebox.showerror("Помилка", "Кількість має бути числом.")
            return

        publisher_id = publisher_dict[publisher_name]
        room_id = room_dict[room_name]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE Books 
                SET access_type=%s, quantity=%s, publisher_id=%s 
                WHERE book_id=%s
            """, (access_type, quantity, publisher_id, book_id))

            cursor.execute("DELETE FROM Placements WHERE book_id=%s", (book_id,))
            cursor.execute("""
                INSERT INTO Placements (book_id, room_id, shelf, `row`)
                VALUES (%s, %s, %s, %s)
            """, (book_id, room_id, shelf, row))

            conn.commit()
            messagebox.showinfo("Успіх", "Інформацію оновлено успішно.")
            refresh_after_book_creation()

        except Exception as e:
            messagebox.showerror("Помилка", str(e))

        finally:
            conn.close()

    btn_frame = tk.Frame(edit_window, bg="#ECEFF1")
    btn_frame.pack(pady=35)

    def make_btn(text, cmd, color, hover):
        btn = tk.Button(
            btn_frame, text=text, command=cmd,
            font=("Segoe UI", 13, "bold"),
            bg=color, fg="white",
            activebackground=hover, activeforeground="white",
            relief="flat", bd=0,
            padx=40, pady=12, cursor="hand2"
        )
        return btn

    edit_window.bind("<Return>", lambda e: update_book())
    book_combobox.focus_set()

    def update_book():
        selected_book = book_combobox.get()
        if not selected_book:
            messagebox.showerror("Помилка", "Оберіть книгу.")
            return

        book_id = book_dict[selected_book]
        access_type = access_type_var.get()
        publisher_name = publisher_combobox.get()
        room_name = room_combobox.get()
        shelf = shelf_entry.get().strip()
        row = row_entry.get().strip()
        quantity = quantity_entry.get().strip()

        if not (access_type and publisher_name and room_name and shelf and row and quantity):
            messagebox.showerror("Помилка", "Усі поля мають бути заповнені.")
            return

        try:
            quantity = int(quantity)
        except:
            messagebox.showerror("Помилка", "Кількість має бути числом.")
            return

        pub_id = publisher_dict[publisher_name]
        room_id = room_dict[room_name]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE Books
                SET access_type=%s, quantity=%s, publisher_id=%s
                WHERE book_id=%s
            """, (access_type, quantity, pub_id, book_id))

            cursor.execute("DELETE FROM Placements WHERE book_id=%s", (book_id,))
            cursor.execute("""
                INSERT INTO Placements (book_id, room_id, shelf, `row`)
                VALUES (%s, %s, %s, %s)
            """, (book_id, room_id, shelf, row))

            conn.commit()
            messagebox.showinfo("Успіх", "Книгу оновлено успішно.")
            refresh_after_book_creation()

        except Exception as e:
            messagebox.showerror("Помилка", str(e))
        finally:
            conn.close()

    btn_frame = tk.Frame(edit_window, bg="#ECEFF1")
    btn_frame.pack(pady=35)

    def make_button(text, cmd, color, hover):
        btn = tk.Button(
            btn_frame, text=text, command=cmd,
            font=("Segoe UI", 13, "bold"),
            bg=color, fg="white",
            activebackground=hover, activeforeground="white",
            relief="flat", bd=0,
            padx=40, pady=12, cursor="hand2"
        )
        return btn

    make_button("Оновити книгу (Enter)", update_book, "#27AE60", "#1E8449").pack(side="left", padx=15)
    make_button("Закрити (ESC)", edit_window.destroy, "#C0392B", "#922B21").pack(side="left", padx=15)

    edit_window.bind("<Return>", lambda e: update_book())
    book_combobox.focus_set()

def show_librarian_window(user_login):
    librarian_window = tk.Tk()
    librarian_window.title("Вікно бібліотекаря")
    make_window_fullscreen(librarian_window)
    
    setup_keyboard_bindings(librarian_window, is_main_window=True)
    
    def on_closing():
        if messagebox.askyesno("Підтвердження", "Вийти з облікового запису та повернутися до вікна входу?"):
            librarian_window.destroy()
            login_window.show_login_window()
    
    librarian_window.protocol("WM_DELETE_WINDOW", on_closing)

    greeting = f"Вітаємо, {user_login} (Бібліотекар)!"

    tk.Label(librarian_window, text=greeting, font=("Arial", 16), pady=30).pack()

    def logout():
        if messagebox.askyesno("Підтвердження", "Вийти з облікового запису та повернутися до вікна входу?"):
            librarian_window.destroy()
            login_window.show_login_window()

    tk.Button(librarian_window, text="Вийти (ESC)", font=("Arial", 12),
           command=logout).pack(pady=20)

    librarian_window.mainloop()

def show_librarian_stats():
    stats_window = tk.Toplevel()
    stats_window.title("Статистика бібліотекарів")

    try:
        make_window_fullscreen(stats_window)
    except:
        make_window_fullscreen(stats_window)

    stats_window.configure(bg="#E5E8EC")
    setup_keyboard_bindings(stats_window)

    header = tk.Canvas(stats_window, height=90, bg="#374151", highlightthickness=0)
    header.pack(fill="x")

    header.create_text(
        40, 30, anchor="w",
        text="Статистика бібліотекарів",
        font=("Segoe UI", 22, "bold"),
        fill="white"
    )
    header.create_text(
        40, 62, anchor="w",
        text="Перегляньте індивідуальну або загальну статистику обслуговування читачів",
        font=("Segoe UI", 11),
        fill="#D1D5DB"
    )

    wrapper = tk.Frame(stats_window, bg="#E5E8EC")
    wrapper.pack(fill="both", expand=True, padx=25, pady=25)

    selection_card = tk.Frame(wrapper, bg="white", padx=25, pady=25)
    selection_card.pack(fill="x", pady=(0, 20))

    tk.Label(
        selection_card,
        text="Оберіть бібліотекаря для перегляду статистики",
        font=("Segoe UI", 13, "bold"),
        bg="white",
        fg="#111827"
    ).pack(anchor="w", pady=(0, 15))

    selection_line = tk.Frame(selection_card, bg="white")
    selection_line.pack(fill="x")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.user_id, l.name
        FROM Users u
        JOIN Librarians l ON u.user_id = l.librarian_id
    """)
    librarians = cursor.fetchall()
    conn.close()

    librarian_map = {f"{name} (ID: {user_id})": user_id for user_id, name in librarians}

    librarian_combo = ttk.Combobox(
        selection_line,
        values=list(librarian_map.keys()),
        state="readonly",
        width=45,
        font=("Segoe UI", 11)
    )
    librarian_combo.pack(side="left", padx=(0, 25))

    def create_fluent_btn(parent, text, command, bg, hover):
        btn = tk.Label(
            parent,
            text=text,
            bg=bg,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        btn.pack(side="left", padx=10)

        def enter(e): btn.config(bg=hover)
        def leave(e): btn.config(bg=bg)
        btn.bind("<Enter>", enter)
        btn.bind("<Leave>", leave)
        btn.bind("<Button-1>", lambda e: command())
        return btn

    def get_specific_stats():
        result_box.config(state="normal")
        result_box.delete("1.0", tk.END)

        selected = librarian_combo.get()
        if not selected:
            result_box.insert(tk.END, "Оберіть бібліотекаря.\n")
            result_box.config(state="disabled")
            return

        librarian_id = librarian_map[selected]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(DISTINCT ib.reader_id)
            FROM IssuedBooks ib
            WHERE ib.librarian_id = %s
        """, (librarian_id,))
        count = cursor.fetchone()[0]
        conn.close()

        result_box.insert(tk.END, f"Бібліотекар *{selected}* обслуговував:\n")
        result_box.insert(tk.END, f"{count} унікальних читачів\n")
        result_box.config(state="disabled")

    def get_general_stats():
        result_box.config(state="normal")
        result_box.delete("1.0", tk.END)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.name, COUNT(DISTINCT ib.reader_id) as reader_count
            FROM Librarians l
            LEFT JOIN IssuedBooks ib ON l.librarian_id = ib.librarian_id
            GROUP BY l.librarian_id, l.name
        """)
        results = cursor.fetchall()
        conn.close()

        total = sum(row[1] for row in results)

        result_box.insert(tk.END, "Загальна статистика обслуговування:\n\n")
        for name, count in results:
            result_box.insert(tk.END, f"• {name}: {count} читачів\n")

        result_box.insert(tk.END, f"\nЗагалом: {total} унікальних читачів")
        result_box.config(state="disabled")

    create_fluent_btn(selection_line, "Переглянути вибраного", get_specific_stats,
                      "#2563EB", "#1D4ED8")

    create_fluent_btn(selection_line, "Загальна статистика", get_general_stats,
                      "#059669", "#047857")

    results_card = tk.Frame(wrapper, bg="white", padx=25, pady=25)
    results_card.pack(fill="both", expand=True)

    tk.Label(
        results_card,
        text="Результат",
        font=("Segoe UI", 13, "bold"),
        bg="white",
        fg="#1F2937"
    ).pack(anchor="w")

    result_box = tk.Text(
        results_card,
        wrap="word",
        font=("Segoe UI", 11),
        height=15,
        padx=15,
        pady=15,
        bg="#F9FAFB",
        relief="flat"
    )
    result_box.pack(fill="both", expand=True, pady=10)

    result_box.config(state="disabled")

    close_btn = tk.Button(
        wrapper,
        text="Закрити (ESC)",
        command=stats_window.destroy,
        bg="#DC2626",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        padx=20, pady=10,
        relief="flat",
        cursor="hand2"
    )
    close_btn.pack(pady=15, anchor="e")

    librarian_combo.focus_set()

def show_books_management_window(parent_window=None):
    management_window = tk.Toplevel(parent_window) if parent_window else tk.Toplevel()
    management_window.title("Управління книгами та звіти")
    make_window_fullscreen(management_window)
    setup_keyboard_bindings(management_window)
    management_window.configure(bg="#ECEFF1")

    header = tk.Canvas(management_window, height=95, bg="#2C3E50", highlightthickness=0)
    header.pack(fill="x")

    title_font = tkFont.Font(family="Segoe UI", size=22, weight="bold")
    header.create_text(
        40, 28, anchor="w",
        text="Управління книгами",
        font=title_font,
        fill="white"
    )
    header.create_text(
        40, 63, anchor="w",
        text="Списання, надходження, формування звітів та повна аналітика",
        font=("Segoe UI", 12),
        fill="#D0D3D4"
    )

    wrapper = tk.Frame(management_window, bg="#ECEFF1")
    wrapper.pack(fill="both", expand=True)

    panel = tk.Frame(wrapper, bg="white", padx=60, pady=60)
    panel.pack(pady=60)

    def modern_button(parent, text, command, bg_color, hover_color):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg=bg_color,
            activebackground=hover_color,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=50,
            pady=18,
            cursor="hand2"
        )
        return btn

    modern_button(
        panel,
        "Списати книги",
        lambda: show_writeoff_window(management_window),
        "#C0392B", "#A93226"
    ).pack(fill="x", pady=12)

    modern_button(
        panel,
        "Звіт по надходженню",
        show_arrivals_report,
        "#27AE60", "#1E8449"
    ).pack(fill="x", pady=12)

    modern_button(
        panel,
        "Звіт по списанню",
        show_writeoff_report,
        "#F39C12", "#D68910"
    ).pack(fill="x", pady=12)

    modern_button(
        panel,
        "Переглянути списані книги",
        show_written_off_books,
        "#7F8C8D", "#707B7C"
    ).pack(fill="x", pady=12)

    close_btn = tk.Button(
        management_window,
        text="Закрити (ESC)",
        command=management_window.destroy,
        font=("Segoe UI", 14, "bold"),
        bg="#B03A2E",
        fg="white",
        activebackground="#922B21",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=40,
        pady=12
    )
    close_btn.pack(pady=30)

def show_writeoff_window(parent_window=None):
    writeoff_window = tk.Toplevel(parent_window) if parent_window else tk.Toplevel()
    writeoff_window.title("Списання книг")
    make_window_fullscreen(writeoff_window)
    writeoff_window.configure(bg="#f0f0f0")
    
    setup_keyboard_bindings(writeoff_window)

    main_frame = tk.Frame(writeoff_window, bg="#f0f0f0")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    selected_book_id = None
    selected_book_data = None

    def search_books():
        nonlocal selected_book_id, selected_book_data
        selected_book_id = None
        selected_book_data = None
        update_selected_book_info()
        
        search_query = search_entry.get().strip()

        conn = get_db_connection()
        if not conn:
            return

        cursor = conn.cursor()

        try:
            if search_query:
                cursor.execute("""
                    SELECT 
                        b.book_id, 
                        b.title, 
                        CONCAT(a.name, ' ', a.surname) as author,
                        b.inventory_number, 
                        b.year,
                        b.date_added,
                        CASE 
                            WHEN EXISTS (
                                SELECT 1 FROM borrowing 
                                WHERE book_id = b.book_id AND status = 'active'
                            ) THEN 'Видана' 
                            ELSE 'Доступна' 
                        END as status
                    FROM Books b
                    JOIN Authors a ON b.author_id = a.author_id
                    WHERE b.title LIKE %s 
                       OR b.inventory_number LIKE %s
                       OR CONCAT(a.name, ' ', a.surname) LIKE %s
                    ORDER BY b.title
                """, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
            else:
                cursor.execute("""
                    SELECT 
                        b.book_id, 
                        b.title, 
                        CONCAT(a.name, ' ', a.surname) as author,
                        b.inventory_number, 
                        b.year,
                        b.date_added,
                        CASE 
                            WHEN EXISTS (
                                SELECT 1 FROM borrowing 
                                WHERE book_id = b.book_id AND status = 'active'
                            ) THEN 'Видана' 
                            ELSE 'Доступна' 
                        END as status
                    FROM Books b
                    JOIN Authors a ON b.author_id = a.author_id
                    ORDER BY b.title
                    LIMIT 100
                """)
            
            results = cursor.fetchall()

            for item in books_tree.get_children():
                books_tree.delete(item)

            for row in results:
                books_tree.insert("", "end", values=row)
                
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка пошуку: {e}")
        finally:
            conn.close()

    def clear_search():
        search_entry.delete(0, tk.END)
        search_books()

    def on_book_select():
        nonlocal selected_book_id, selected_book_data
        
        selected_item = books_tree.selection()
        if not selected_item:
            messagebox.showwarning("Увага", "Оберіть книгу зі списку!")
            return
            
        book_data = books_tree.item(selected_item[0])["values"]
        selected_book_id = book_data[0]
        selected_book_data = book_data
        
        for item in books_tree.selection():
            books_tree.selection_set(item)
        
        update_selected_book_info()
        
        if book_data[6] == "Видана":
            messagebox.showwarning("Увага", 
                "Ця книга видана читачу! Спочатку потрібно повернути книгу.")
        

    def update_selected_book_info():
        if selected_book_data:
            selected_title.config(text=selected_book_data[1], fg="#000")
            selected_author.config(text=selected_book_data[2], fg="#000")
            selected_inventory.config(text=selected_book_data[3], fg="#000")
            selected_status.config(text=selected_book_data[6], 
                                 fg="#4CAF50" if selected_book_data[6] == "Доступна" else "#F44336")
        else:
            selected_title.config(text="Не обрано", fg="#666")
            selected_author.config(text="Не обрано", fg="#666")
            selected_inventory.config(text="Не обрано", fg="#666")
            selected_status.config(text="Не обрано", fg="#666")

    def check_book_status():
        if not selected_book_id:

            return
            
        conn = get_db_connection()
        if not conn:
            return
            
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT COUNT(*), 
                       GROUP_CONCAT(CONCAT('Позика #', borrowing_id, ' (до ', due_date, ')') SEPARATOR '\n')
                FROM borrowing 
                WHERE book_id = %s AND status = 'active'
            """, (selected_book_id,))
            
            borrowing_count, borrowing_info = cursor.fetchone()
            if borrowing_info is None:
                borrowing_info = "Немає активних позик"
            
            cursor.execute("""
                SELECT COUNT(*), 
                       GROUP_CONCAT(CONCAT('Колекція #', collection_id) SEPARATOR '\n')
                FROM collectionitems 
                WHERE book_id = %s
            """, (selected_book_id,))
            
            collection_count, collection_info = cursor.fetchone()
            if collection_info is None:
                collection_info = "Не входить до колекцій"
            
            status_report = f"КНИГА: {selected_book_data[1]}\n"
            status_report += f"ID: {selected_book_id}\n"
            status_report += f"Автор: {selected_book_data[2]}\n"
            status_report += f"Інвентарний: {selected_book_data[3]}\n"
            status_report += "─" * 40 + "\n"
            
            status_report += f"\nАКТИВНІ ПОЗИКИ: {borrowing_count}\n"
            status_report += borrowing_info + "\n"
            
            status_report += f"\nКОЛЕКЦІЇ: {collection_count}\n"
            status_report += collection_info + "\n"
            
            status_report += "─" * 40 + "\n"
            
            if borrowing_count > 0:
                status_report += "\nНЕ МОЖНА СПИСАТИ - активні позики!\n"
            elif collection_count > 0:
                status_report += "\nМОЖНА СПИСАТИ - буде видалена з колекцій\n"
            else:
                status_report += "\nМОЖНА СПИСАТИ - немає залежностей\n"
                
            show_status_report(status_report)
            
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка перевірки статусу: {e}")
        finally:
            conn.close()

    def show_status_report(report_text):
        report_window = tk.Toplevel(writeoff_window)
        report_window.title("Детальний статус книги")
        make_window_fullscreen(report_window)
        report_window.configure(bg="#f0f0f0")
        
        setup_keyboard_bindings(report_window)
        
        text_frame = tk.Frame(report_window, bg="#f0f0f0")
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap="word", font=("Courier New", 10), bg="#fff", padx=10, pady=10)
        text_widget.insert("1.0", report_text)
        text_widget.config(state="disabled")
        
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        close_btn = tk.Button(report_window, text="Закрити (ESC)", command=report_window.destroy,
                            bg="#607D8B", fg="white", font=("Arial", 10), width=20)
        close_btn.pack(pady=10)
        close_btn.focus_set()

    def writeoff_selected_book():
        nonlocal selected_book_id, selected_book_data
        
        if not selected_book_id:
            messagebox.showerror("Помилка", "Спочатку оберіть книгу для списання!")
            return

        reason = reason_entry.get().strip()
        if not reason:
            messagebox.showerror("Помилка", "Вкажіть причину списання!")
            return

        if selected_book_data[6] == "Видана":
            messagebox.showerror("Помилка", "Книга видана читачу! Не можна списати.")
            return

        confirm_msg = f"Дана книга буде списана\n\n"
        confirm_msg += f"Назва: {selected_book_data[1]}\n"
        confirm_msg += f"Автор: {selected_book_data[2]}\n"
        confirm_msg += f"Інвентарний: {selected_book_data[3]}\n"
        confirm_msg += f"Рік: {selected_book_data[4]}\n"
        confirm_msg += f"Причина: {reason}\n\n"
        
        if not messagebox.askyesno("ПІДТВЕРДЖЕННЯ СПИСАННЯ", confirm_msg):
            return

        conn = get_db_connection()
        if not conn:
            return
            
        cursor = conn.cursor()
        
        try:
            conn.autocommit = False
            
            cursor.execute("""
                SELECT book_id, title, author_id, category_id, year, 
                       languages, access_type, inventory_number, date_added
                FROM Books WHERE book_id = %s
            """, (selected_book_id,))
            
            book_data = cursor.fetchone()
            
            if not book_data:
                messagebox.showerror("Помилка", "Книга не знайдена!")
                return
            
            cursor.execute("""
                INSERT INTO writtenoffbooks (
                    original_book_id, title, author_id, category_id, year, 
                    languages, access_type, inventory_number, date_added, 
                    date_written_off, writeoff_reason
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE(), %s)
            """, (*book_data, reason))
            
            cursor.execute("DELETE FROM collectionitems WHERE book_id = %s", (selected_book_id,))
            
            cursor.execute("DELETE FROM Books WHERE book_id = %s", (selected_book_id,))
            
            conn.commit()
            
            selected_book_id = None
            selected_book_data = None
            update_selected_book_info()
            reason_entry.delete(0, tk.END)
            search_books()
            
            refresh_after_book_creation()
            
        except Exception as e:
            conn.rollback()
            error_msg = f"Помилка при списанні книги:\n{str(e)}"
            
        finally:
            conn.autocommit = True
            conn.close()

    search_frame = tk.LabelFrame(main_frame, text="Пошук книги для списання", 
                               font=("Arial", 12, "bold"), bg="#f0f0f0", padx=15, pady=15)
    search_frame.pack(fill="x", pady=(0, 10))

    search_container = tk.Frame(search_frame, bg="#f0f0f0")
    search_container.pack(fill="x")

    tk.Label(search_container, text="Пошук за назвою, автору або інвентарному номеру:", 
            font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))

    search_input_frame = tk.Frame(search_container, bg="#f0f0f0")
    search_input_frame.pack(fill="x", pady=5)

    search_entry = tk.Entry(search_input_frame, width=50, font=("Arial", 10))
    search_entry.pack(side="left", padx=(0, 10))
    search_entry.bind('<Return>', lambda event: search_books())

    search_btn = tk.Button(search_input_frame, text="Пошук (Enter)", command=search_books,
                         bg="#4CAF50", fg="white", font=("Arial", 10), width=12)
    search_btn.pack(side="left", padx=(0, 5))

    clear_btn = tk.Button(search_input_frame, text="Очистити", command=clear_search,
                        bg="#FF9800", fg="white", font=("Arial", 10), width=10)
    clear_btn.pack(side="left")

    books_frame = tk.LabelFrame(main_frame, text="Знайдені книги", 
                              font=("Arial", 12, "bold"), bg="#f0f0f0", padx=15, pady=15)
    books_frame.pack(fill="both", expand=True, pady=(0, 10))

    columns = ("ID", "Назва", "Автор", "Інвентарний номер", "Рік", "Дата додавання", "Статус")
    books_tree = ttk.Treeview(books_frame, columns=columns, show="headings", height=12)
    
    column_widths = {
        "ID": 50,
        "Назва": 250,
        "Автор": 150,
        "Інвентарний номер": 120,
        "Рік": 60,
        "Дата додавання": 100,
        "Статус": 100
    }
    
    for col in columns:
        books_tree.heading(col, text=col)
        books_tree.column(col, width=column_widths.get(col, 100))

    scrollbar_y = ttk.Scrollbar(books_frame, orient="vertical", command=books_tree.yview)
    scrollbar_x = ttk.Scrollbar(books_frame, orient="horizontal", command=books_tree.xview)
    books_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    books_tree.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    books_frame.grid_rowconfigure(0, weight=1)
    books_frame.grid_columnconfigure(0, weight=1)

    books_tree.bind('<Double-1>', lambda event: on_book_select())

    selected_frame = tk.LabelFrame(main_frame, text="Вибрана книга для списання", 
                                 font=("Arial", 12, "bold"), bg="#f0f0f0", padx=15, pady=15)
    selected_frame.pack(fill="x", pady=(0, 10))

    info_container = tk.Frame(selected_frame, bg="#f0f0f0")
    info_container.pack(fill="x")

    left_info = tk.Frame(info_container, bg="#f0f0f0")
    left_info.pack(side="left", fill="both", expand=True, padx=(0, 20))

    tk.Label(left_info, text="Назва книги:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
    selected_title = tk.Label(left_info, text="Не обрано", font=("Arial", 10), bg="#f0f0f0", fg="#666")
    selected_title.pack(anchor="w", pady=(0, 10))

    tk.Label(left_info, text="Автор:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
    selected_author = tk.Label(left_info, text="Не обрано", font=("Arial", 10), bg="#f0f0f0", fg="#666")
    selected_author.pack(anchor="w", pady=(0, 10))

    right_info = tk.Frame(info_container, bg="#f0f0f0")
    right_info.pack(side="right", fill="both", expand=True)

    tk.Label(right_info, text="Інвентарний номер:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
    selected_inventory = tk.Label(right_info, text="Не обрано", font=("Arial", 10), bg="#f0f0f0", fg="#666")
    selected_inventory.pack(anchor="w", pady=(0, 10))

    tk.Label(right_info, text="Статус:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
    selected_status = tk.Label(right_info, text="Не обрано", font=("Arial", 10), bg="#f0f0f0", fg="#666")
    selected_status.pack(anchor="w", pady=(0, 10))

    reason_frame = tk.LabelFrame(main_frame, text="Причина списання", 
                               font=("Arial", 12, "bold"), bg="#f0f0f0", padx=15, pady=15)
    reason_frame.pack(fill="x", pady=(0, 10))

    reason_entry = tk.Entry(reason_frame, width=80, font=("Arial", 10))
    reason_entry.pack(pady=5)

    buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
    buttons_frame.pack(pady=10)

    check_btn = tk.Button(buttons_frame, text="Перевірити статус", command=check_book_status,
                        bg="#2196F3", fg="white", font=("Arial", 10), width=15, height=2)
    check_btn.pack(side="left", padx=5)

    select_btn = tk.Button(buttons_frame, text="Обрати книгу", command=on_book_select,
                         bg="#FFC107", fg="black", font=("Arial", 10), width=15, height=2)
    select_btn.pack(side="left", padx=5)

    writeoff_btn = tk.Button(buttons_frame, text="Списати книгу (Enter)", command=writeoff_selected_book,
                           bg="#F44336", fg="white", font=("Arial", 10), width=18, height=2)
    writeoff_btn.pack(side="left", padx=5)

    close_btn = tk.Button(buttons_frame, text="Закрити (ESC)", command=writeoff_window.destroy,
                        bg="#607D8B", fg="white", font=("Arial", 10), width=15, height=2)
    close_btn.pack(side="left", padx=5)

    search_books()
    search_entry.focus_set()

def show_arrivals_report():
    report_window = tk.Toplevel()
    report_window.title("Звіт по надходженню книг")

    try:
        make_window_fullscreen(report_window)
    except:
        make_window_fullscreen(report_window)

    report_window.configure(bg="#E5E8EC")
    setup_keyboard_bindings(report_window)

    header = tk.Canvas(report_window, height=90, bg="#2563EB", highlightthickness=0)
    header.pack(fill="x")

    title_font = tkFont.Font(family="Segoe UI", size=22, weight="bold")
    subtitle_font = tkFont.Font(family="Segoe UI", size=11)

    header.create_text(
        40, 30, anchor="w",
        text="Звіт по надходженню книг",
        font=title_font, fill="white"
    )
    header.create_text(
        40, 63, anchor="w",
        text="Перегляд усіх книг, що надійшли у вибраний період",
        font=subtitle_font, fill="#E0ECFF"
    )

    wrapper = tk.Frame(report_window, bg="#E5E8EC")
    wrapper.pack(fill="both", expand=True, padx=25, pady=25)

    period_card = tk.Frame(wrapper, bg="white", padx=25, pady=25)
    period_card.pack(fill="x", pady=(0, 20))

    tk.Label(
        period_card,
        text="Оберіть період",
        bg="white",
        fg="#111827",
        font=("Segoe UI", 14, "bold")
    ).pack(anchor="w")

    form_row = tk.Frame(period_card, bg="white")
    form_row.pack(pady=15, fill="x")

    label_style = ("Segoe UI", 11, "bold")

    tk.Label(form_row, text="Від:", bg="white", font=label_style)\
        .grid(row=0, column=0, sticky="w", padx=(0, 10))

    start_date = DateEntry(
        form_row,
        width=14,
        font=("Segoe UI", 11),
        date_pattern='yyyy-mm-dd',
        background="#2563EB",
        foreground="white",
        borderwidth=1
    )
    start_date.grid(row=0, column=1, padx=(0, 10))

    tk.Label(form_row, text="До:", bg="white", font=label_style)\
        .grid(row=0, column=2, sticky="w", padx=(20, 10))

    end_date = DateEntry(
        form_row,
        width=14,
        font=("Segoe UI", 11),
        date_pattern='yyyy-mm-dd',
        background="#2563EB",
        foreground="white",
        borderwidth=1
    )
    end_date.grid(row=0, column=3, padx=(0, 10))

    def generate_report():
        start_date_str = start_date.get()
        end_date_str = end_date.get()

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT b.book_id, b.title, 
                   COALESCE(CONCAT(a.name, ' ', a.surname), '-') as author,
                   b.inventory_number, b.date_added, 
                   COALESCE(c.name, '-') as category
            FROM Books b
            LEFT JOIN Authors a ON b.author_id = a.author_id
            LEFT JOIN Categories c ON b.category_id = c.category_id
            WHERE b.date_added BETWEEN %s AND %s
            ORDER BY b.date_added DESC
        """, (start_date_str, end_date_str))

        results = cursor.fetchall()
        conn.close()

        results_tree.delete(*results_tree.get_children())
        for row in results:
            results_tree.insert("", "end", values=row)

        total_label.config(text=f"Знайдено: {len(results)} книг")

    def make_btn(parent, text, command, bg, hover, w=18):
        btn = tk.Button(
            parent, text=text, command=command,
            bg=bg, fg="white",
            relief="flat", bd=0,
            activebackground=hover,
            font=("Segoe UI", 11, "bold"),
            padx=10, pady=6,
            cursor="hand2",
            width=w
        )
        return btn

    btn_row = tk.Frame(period_card, bg="white")
    btn_row.pack(anchor="w")

    make_btn(
        btn_row, "Генерувати звіт (Enter)",
        generate_report, "#10B981", "#059669"
    ).pack(side="left", padx=(0, 15))

    results_card = tk.Frame(wrapper, bg="white", padx=25, pady=25)
    results_card.pack(fill="both", expand=True)

    tk.Label(
        results_card,
        text="Результати",
        font=("Segoe UI", 14, "bold"),
        bg="white",
        fg="#111827"
    ).pack(anchor="w")

    tree_container = tk.Frame(results_card, bg="white")
    tree_container.pack(fill="both", expand=True, pady=10)

    columns = ("ID", "Назва", "Автор", "Інвентарний номер", "Дата надходження", "Категорія")

    style = ttk.Style()
    style.configure("Fluent.Treeview", font=("Segoe UI", 10), rowheight=28)
    style.configure("Fluent.Treeview.Heading", font=("Segoe UI", 11, "bold"))

    results_tree = ttk.Treeview(
        tree_container,
        columns=columns,
        show="headings",
        style="Fluent.Treeview"
    )

    widths = {
        "ID": 60,
        "Назва": 260,
        "Автор": 170,
        "Інвентарний номер": 150,
        "Дата надходження": 130,
        "Категорія": 140
    }

    for col in columns:
        results_tree.heading(col, text=col)
        results_tree.column(col, width=widths[col], anchor="w")

    scrollbar_y = ttk.Scrollbar(tree_container, orient="vertical", command=results_tree.yview)
    results_tree.configure(yscrollcommand=scrollbar_y.set)

    results_tree.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")

    total_label = tk.Label(
        results_card, text="",
        font=("Segoe UI", 11, "bold"),
        bg="white", fg="#374151"
    )
    total_label.pack(anchor="w", pady=(5, 5))

    close_btn = tk.Button(
        wrapper,
        text="Закрити (ESC)",
        command=report_window.destroy,
        bg="#6B7280",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        bd=0,
        padx=20,
        pady=12,
        cursor="hand2"
    )
    close_btn.pack(pady=(10, 0), anchor="e")

    report_window.bind("<Return>", lambda e: generate_report())
    start_date.focus_set()

def show_writeoff_report():
    report_window = tk.Toplevel()
    report_window.title("Звіт по списанню книг")

    try:
        make_window_fullscreen(report_window)
    except:
        make_window_fullscreen(report_window)

    report_window.configure(bg="#E5E8EC")
    setup_keyboard_bindings(report_window)

    header = tk.Canvas(report_window, height=90, bg="#DC2626", highlightthickness=0)
    header.pack(fill="x")

    title_font = tkFont.Font(family="Segoe UI", size=22, weight="bold")
    subtitle_font = tkFont.Font(family="Segoe UI", size=11)

    header.create_text(
        40, 30, anchor="w",
        text="Звіт по списанню книг",
        font=title_font, fill="white"
    )
    header.create_text(
        40, 63, anchor="w",
        text="Перегляд усіх книг, списаних за обраний період",
        font=subtitle_font, fill="#FBD5D5"
    )

    wrapper = tk.Frame(report_window, bg="#E5E8EC")
    wrapper.pack(fill="both", expand=True, padx=25, pady=25)

    period_card = tk.Frame(wrapper, bg="white", padx=25, pady=25)
    period_card.pack(fill="x", pady=(0, 20))

    tk.Label(
        period_card,
        text="Оберіть період",
        bg="white",
        fg="#111827",
        font=("Segoe UI", 14, "bold")
    ).pack(anchor="w")

    form_row = tk.Frame(period_card, bg="white")
    form_row.pack(pady=15, fill="x")

    label_style = ("Segoe UI", 11, "bold")

    tk.Label(form_row, text="Від:", bg="white", font=label_style)\
        .grid(row=0, column=0, sticky="w", padx=(0, 10))

    start_date = DateEntry(
        form_row,
        width=14,
        font=("Segoe UI", 11),
        date_pattern='yyyy-mm-dd',
        background="#DC2626",
        foreground="white",
        borderwidth=1
    )
    start_date.grid(row=0, column=1)

    tk.Label(form_row, text="До:", bg="white", font=label_style)\
        .grid(row=0, column=2, sticky="w", padx=(20, 10))

    end_date = DateEntry(
        form_row,
        width=14,
        font=("Segoe UI", 11),
        date_pattern='yyyy-mm-dd',
        background="#DC2626",
        foreground="white",
        borderwidth=1
    )
    end_date.grid(row=0, column=3)

    def make_btn(parent, text, command, bg, hover, w=18):
        btn = tk.Button(
            parent, text=text, command=command,
            bg=bg, fg="white",
            relief="flat", bd=0,
            activebackground=hover,
            font=("Segoe UI", 11, "bold"),
            padx=12, pady=6,
            cursor="hand2",
            width=w
        )
        return btn

    def generate_writeoff_report():
        start_date_str = start_date.get()
        end_date_str = end_date.get()

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT wob.writeoff_id, wob.title, CONCAT(a.name, ' ', a.surname) as author,
                   wob.inventory_number, wob.date_written_off, wob.writeoff_reason
            FROM WrittenOffBooks wob
            JOIN Authors a ON wob.author_id = a.author_id
            WHERE wob.date_written_off BETWEEN %s AND %s
            ORDER BY wob.date_written_off DESC
        """, (start_date_str, end_date_str))

        results = cursor.fetchall()
        conn.close()

        results_tree.delete(*results_tree.get_children())
        for row in results:
            results_tree.insert("", "end", values=row)

        total_label.config(text=f"Списано книг: {len(results)}")

    btn_row = tk.Frame(period_card, bg="white")
    btn_row.pack(anchor="w", pady=5)

    make_btn(
        btn_row,
        "Генерувати звіт (Enter)",
        generate_writeoff_report,
        "#DC2626",
        "#B91C1C"
    ).pack(side="left", padx=(0, 20))

    results_card = tk.Frame(wrapper, bg="white", padx=25, pady=25)
    results_card.pack(fill="both", expand=True)

    tk.Label(
        results_card,
        text="Результати списання",
        font=("Segoe UI", 14, "bold"),
        bg="white",
        fg="#111827"
    ).pack(anchor="w")

    tree_container = tk.Frame(results_card, bg="white")
    tree_container.pack(fill="both", expand=True, pady=15)

    columns = ("ID списання", "Назва", "Автор", "Інвентарний номер", "Дата списання", "Причина")

    style = ttk.Style()
    style.configure("Fluent.Treeview", font=("Segoe UI", 10), rowheight=28)
    style.configure("Fluent.Treeview.Heading", font=("Segoe UI", 11, "bold"))

    results_tree = ttk.Treeview(
        tree_container,
        columns=columns,
        show="headings",
        style="Fluent.Treeview"
    )

    widths = {
        "ID списання": 120,
        "Назва": 260,
        "Автор": 160,
        "Інвентарний номер": 150,
        "Дата списання": 140,
        "Причина": 260
    }

    for col in columns:
        results_tree.heading(col, text=col)
        results_tree.column(col, width=widths[col], anchor="w")

    scrollbar_y = ttk.Scrollbar(tree_container, orient="vertical", command=results_tree.yview)
    results_tree.configure(yscrollcommand=scrollbar_y.set)

    results_tree.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")

    total_label = tk.Label(
        results_card, text="",
        font=("Segoe UI", 11, "bold"),
        bg="white", fg="#374151"
    )
    total_label.pack(anchor="w")

    close_btn = tk.Button(
        wrapper,
        text="Закрити (ESC)",
        command=report_window.destroy,
        bg="#6B7280",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        padx=20, pady=10,
        cursor="hand2"
    )
    close_btn.pack(pady=(10, 0), anchor="e")

    report_window.bind("<Return>", lambda e: generate_writeoff_report())
    start_date.focus_set()

def show_written_off_books():
    books_window = tk.Toplevel()
    books_window.title("Списані книги")

    try:
        make_window_fullscreen (books_window)
    except:
        make_window_fullscreen(books_window)

    books_window.configure(bg="#E5E8EC")
    setup_keyboard_bindings(books_window)

    header = tk.Canvas(books_window, height=90, bg="#6B7280", highlightthickness=0)
    header.pack(fill="x")

    title_font = tkFont.Font(family="Segoe UI", size=22, weight="bold")
    subtitle_font = tkFont.Font(family="Segoe UI", size=11)

    header.create_text(
        40, 30, anchor="w",
        text="Списані книги",
        font=title_font, fill="white"
    )
    header.create_text(
        40, 63, anchor="w",
        text="Повний список усіх списаних одиниць фонду",
        font=subtitle_font, fill="#E5E7EB"
    )

    wrapper = tk.Frame(books_window, bg="#E5E8EC")
    wrapper.pack(fill="both", expand=True, padx=25, pady=25)

    table_card = tk.Frame(wrapper, bg="white", padx=25, pady=25)
    table_card.pack(fill="both", expand=True)

    tk.Label(
        table_card,
        text="Перелік списаних книг",
        font=("Segoe UI", 16, "bold"),
        bg="white",
        fg="#111827"
    ).pack(anchor="w")

    table_frame = tk.Frame(table_card, bg="white")
    table_frame.pack(fill="both", expand=True, pady=15)

    columns = ("ID", "Назва", "Автор", "Інвентарний номер", "Дата додавання", "Дата списання", "Причина")

    style = ttk.Style()
    style.configure("Fluent.Treeview", font=("Segoe UI", 10), rowheight=30)
    style.configure("Fluent.Treeview.Heading", font=("Segoe UI", 11, "bold"))
    style.map("Treeview", background=[("selected", "#D1D5DB")])

    results_tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        style="Fluent.Treeview"
    )

    widths = {
        "ID": 80,
        "Назва": 260,
        "Автор": 180,
        "Інвентарний номер": 150,
        "Дата додавання": 150,
        "Дата списання": 150,
        "Причина": 260
    }

    for col in columns:
        results_tree.heading(col, text=col)
        results_tree.column(col, width=widths[col], anchor="w")

    scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=results_tree.yview)
    results_tree.configure(yscrollcommand=scrollbar_y.set)

    results_tree.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT wob.writeoff_id, wob.title, 
               CONCAT(a.name, ' ', a.surname) as author,
               wob.inventory_number, wob.date_added, 
               wob.date_written_off, wob.writeoff_reason
        FROM WrittenOffBooks wob
        JOIN Authors a ON wob.author_id = a.author_id
        ORDER BY wob.date_written_off DESC
    """)

    results = cursor.fetchall()
    conn.close()

    for row in results:
        results_tree.insert("", "end", values=row)

    summary_label = tk.Label(
        table_card,
        text=f"Загалом списано: {len(results)} книг",
        font=("Segoe UI", 11, "bold"),
        bg="white",
        fg="#374151"
    )
    summary_label.pack(anchor="w", pady=(10, 0))

    close_btn = tk.Button(
        wrapper,
        text="Закрити (ESC)",
        command=books_window.destroy,
        bg="#DC2626",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        relief="flat",
        padx=20, pady=12,
        cursor="hand2"
    )
    close_btn.pack(pady=15, anchor="e")

def get_readers_by_criteria(university=None, faculty=None, reader_type=None, organization=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT reader_id, user_name, address, reader_type, university, faculty, organization
        FROM Readers
        WHERE 1=1
    """
    params = []
    
    if university:
        query += " AND university = %s"
        params.append(university)
    
    if faculty:
        query += " AND faculty = %s"
        params.append(faculty)
    
    if reader_type:
        query += " AND reader_type = %s"
        params.append(reader_type)
    
    if organization:
        query += " AND organization = %s"
        params.append(organization)
    
    cursor.execute(query, params)
    readers = cursor.fetchall()
    conn.close()
    
    return readers

def fetch_all_overdue_books():
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
        WHERE ib.return_date < CURDATE()
        ORDER BY DATEDIFF(CURDATE(), ib.return_date) DESC, ib.return_date ASC
    """)
    result = cursor.fetchall()
    conn.close()
    return result

def show_admin_overdue_books():
    import tkinter as tk
    from tkinter import ttk, messagebox

    overdue_window = tk.Toplevel()
    overdue_window.title("АДМІН: Просрочені книги")
    make_window_fullscreen(overdue_window)
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
                header_row, text=text, fg="white", bg="#233243",
                font=("Segoe UI", 11, "bold"), width=width, anchor="w", padx=6
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
                    row, text=text, bg=bg, fg=color,
                    font=font_style, width=width, anchor="w", padx=6
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
        text="Закрити (Esc)",
        command=overdue_window.destroy,
        bg="#C62828",
        fg="white",
        font=("Segoe UI", 13, "bold"),
        padx=20,
        pady=7
    )
    close_btn.pack(pady=5)

    refresh_overdue_data()

def fetch_user_issued_books(reader_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ib.issue_id, ib.book_id, b.title, c.name as category, 
               ib.issue_date, ib.return_date, ib.reading_place, ib.room_id, ib.librarian_id,
               CASE 
                   WHEN ib.returned = TRUE THEN 0
                   ELSE DATEDIFF(CURDATE(), ib.return_date)
               END as days_overdue,
               ib.returned
        FROM IssuedBooks ib
        JOIN Books b ON b.book_id = ib.book_id
        LEFT JOIN Categories c ON b.category_id = c.category_id
        WHERE ib.reader_id = %s
        ORDER BY ib.issue_date DESC
    """, (reader_id,))

    result = cursor.fetchall()
    conn.close()
    return result

def get_all_readers_with_login():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.reader_id, u.login, r.user_name
        FROM Readers r
        JOIN Users u ON r.user_id = u.user_id
        ORDER BY u.login
    """)

    readers = cursor.fetchall()
    conn.close()
    return readers

def show_admin_reader_search(parent=None): 
    """АДМІН: Пошук історії книг читача за період (Fluent UI, без зовнішніх констант)."""

    BG_MAIN = "#F4F6F9"
    BG_HEADER = "#2D5A88"
    CARD_BG = "white"
    BTN_BLUE = "#1A73E8"
    BTN_RED = "#D93025"
    TEXT_DARK = "#1F1F1F"

    FONT_TITLE = ("Segoe UI", 20, "bold")
    FONT_BOLD = ("Segoe UI", 12, "bold")
    FONT_NORMAL = ("Segoe UI", 12)

    win = tk.Toplevel(parent)
    win.title("АДМІН: Пошук історії книг читача")
    make_window_fullscreen(win)
    win.configure(bg=BG_MAIN)

    header = tk.Frame(win, bg=BG_HEADER, height=70)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="ПОШУК КНИГ ЧИТАЧА ЗА ПЕРІОД",
        font=FONT_TITLE,
        bg=BG_HEADER,
        fg="white"
    ).pack(pady=10)

    container = tk.Frame(win, bg=BG_MAIN, padx=30, pady=20)
    container.pack(fill="both", expand=True)

    # 🔳 Біла картка
    card = tk.Frame(container, bg=CARD_BG, bd=2, relief="groove")
    card.pack(fill="x", pady=10)

    user_frame = tk.Frame(card, bg=CARD_BG, padx=20, pady=20)
    user_frame.pack(fill="x")

    tk.Label(
        user_frame,
        text="Оберіть користувача:",
        bg=CARD_BG,
        fg=TEXT_DARK,
        font=FONT_BOLD
    ).grid(row=0, column=0, sticky="w", padx=5)

    try:
        readers_list = get_all_readers_with_login()
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося завантажити читачів:\n{e}")
        readers_list = []

    readers_display = [f"{r[1]} ({r[2]})" for r in readers_list]

    reader_cb = ttk.Combobox(user_frame, values=readers_display, state="readonly", width=45, font=("Segoe UI", 12))
    reader_cb.grid(row=0, column=1, padx=10)
    reader_cb.set("Оберіть користувача")

    period_frame = tk.Frame(card, bg=CARD_BG, padx=20, pady=5)
    period_frame.pack(fill="x")

    tk.Label(period_frame, text="Від:", bg=CARD_BG, font=FONT_BOLD).grid(row=0, column=0, padx=5)
    start_date = DateEntry(period_frame, date_pattern="yyyy-mm-dd", font=("Segoe UI", 11), width=15)
    start_date.grid(row=0, column=1, padx=10)
    start_date.set_date(date.today().replace(day=1))

    tk.Label(period_frame, text="До:", bg=CARD_BG, font=FONT_BOLD).grid(row=0, column=2, padx=5)
    end_date = DateEntry(period_frame, date_pattern="yyyy-mm-dd", font=("Segoe UI", 11), width=15)
    end_date.grid(row=0, column=3, padx=10)
    end_date.set_date(date.today())

    table_card = tk.Frame(container, bg=CARD_BG, bd=2, relief="groove")
    table_card.pack(fill="both", expand=True, pady=10)

    columns = ("Користувач", "Книга", "Час взяття", "Видання")
    table = ttk.Treeview(table_card, columns=columns, show="headings", height=20)
    table.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    vsb = ttk.Scrollbar(table_card, orient="vertical", command=table.yview)
    vsb.pack(side="right", fill="y")
    table.configure(yscrollcommand=vsb.set)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=250, anchor="w")

    def search_action():
        selected = reader_cb.get()
        if selected == "Оберіть користувача":
            messagebox.showwarning("Помилка", "Оберіть користувача!")
            return

        idx = readers_display.index(selected)
        reader_id = readers_list[idx][0]

        d_from = start_date.get()
        d_to = end_date.get()

        for i in table.get_children():
            table.delete(i)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT u.login, b.title, t.issue_date, p.name
                FROM thinkbooks t
                JOIN Readers r ON t.reader_id = r.reader_id
                JOIN Users u ON r.user_id = u.user_id
                JOIN Books b ON t.book_id = b.book_id
                JOIN Publishers p ON b.publisher_id = p.publisher_id
                WHERE t.reader_id = %s AND t.issue_date BETWEEN %s AND %s
                ORDER BY t.issue_date DESC
            """, (reader_id, d_from, d_to))

            rows = cursor.fetchall()

            if not rows:
                messagebox.showinfo("Результат", "Немає записів за цей період.")
                return

            for row in rows:
                table.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка при пошуку:\n{e}")
        finally:
            conn.close()

    btn_frame = tk.Frame(container, bg=BG_MAIN)
    btn_frame.pack(pady=10)

    btn_search = tk.Button(
        btn_frame,
        text=" Знайти (Enter)",
        bg=BTN_BLUE,
        fg="white",
        font=FONT_BOLD,
        padx=20,
        pady=8,
        command=search_action
    )
    btn_search.pack(side="left", padx=10)

    btn_close = tk.Button(
        btn_frame,
        text="Закрити",
        bg=BTN_RED,
        fg="white",
        font=FONT_BOLD,
        padx=20,
        pady=8,
        command=win.destroy
    )
    btn_close.pack(side="left", padx=10)

    setup_keyboard_bindings(win, on_enter=search_action)
    win.grab_set()
    win.focus_set()

def show_readers_list_window():
    readers_window = tk.Toplevel()
    readers_window.title("Пошук читачів за характеристиками")
    make_window_fullscreen(readers_window)
    
    setup_keyboard_bindings(readers_window)

    header = tk.Frame(readers_window, bg="#17406D", height=70)
    header.pack(fill="x")

    tk.Label(
        header,
        text="Пошук читачів за характеристиками",
        font=("Segoe UI", 24, "bold"),
        fg="white",
        bg="#17406D"
    ).pack(pady=10)

    main_frame = tk.Frame(readers_window, bg="#ECEFF1")
    main_frame.pack(fill="both", expand=True, padx=20, pady=15)

    criteria_frame = tk.LabelFrame(
        main_frame,
        text="Критерії пошуку",
        font=("Segoe UI", 16, "bold"),
        bg="white",
        fg="black",
        padx=15,
        pady=15
    )
    criteria_frame.pack(fill="x", pady=10)

    fields_frame = tk.Frame(criteria_frame, bg="white")
    fields_frame.pack(fill="x", padx=20, pady=10)

    def add_field(row, label_text):
        label = tk.Label(
            fields_frame,
            text=label_text,
            font=("Segoe UI", 13),
            bg="white"
        )
        label.grid(row=row, column=0, sticky="w", pady=12)

        entry = tk.Entry(fields_frame, width=50, font=("Segoe UI", 13))
        entry.grid(row=row, column=1, sticky="w", padx=(30, 0))
        return entry

    university_entry = add_field(0, "Навчальний заклад:")

    faculty_entry = add_field(1, "Факультет:")

    organization_entry = add_field(2, "Організація:")

    tk.Label(fields_frame, text="Тип читача:", font=("Segoe UI", 13), bg="white")\
        .grid(row=3, column=0, sticky="w", pady=12)

    reader_type_var = tk.StringVar()
    reader_type_combo = ttk.Combobox(
        fields_frame,
        textvariable=reader_type_var,
        values=["", "Студент", "Викладач", "Науковець", "Працівник", "Інше"],
        state="readonly",
        font=("Segoe UI", 13),
        width=48
    )
    reader_type_combo.grid(row=3, column=1, sticky="w", padx=(30, 0))

    buttons_frame = tk.Frame(criteria_frame, bg="white")
    buttons_frame.pack(pady=10)

    def search_readers():
        university = university_entry.get().strip() or None
        faculty = faculty_entry.get().strip() or None
        organization = organization_entry.get().strip() or None
        reader_type = reader_type_var.get() or None

        if not any([university, faculty, organization, reader_type]):
            if not messagebox.askyesno(
                "Попередження",
                "Не вказано жодного критерію пошуку. Показати всіх читачів?"
            ):
                return
        
        readers = get_readers_by_criteria(university, faculty, reader_type, organization)

        for item in results_tree.get_children():
            results_tree.delete(item)

        for reader in readers:
            reader_id, user_name, address, r_type, uni, fac, org = reader
            results_tree.insert("", "end", values=(
                reader_id, user_name, address, r_type,
                uni or "-", fac or "-", org or "-"
            ))

        total_label.config(text=f"Знайдено читачів: {len(readers)}")

    def clear_fields():
        university_entry.delete(0, tk.END)
        faculty_entry.delete(0, tk.END)
        organization_entry.delete(0, tk.END)
        reader_type_var.set("")

        for item in results_tree.get_children():
            results_tree.delete(item)

        total_label.config(text="Знайдено читачів: 0")

    def get_unique_organizations():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT organization FROM Readers "
            "WHERE organization IS NOT NULL AND organization != '' "
            "ORDER BY organization"
        )
        result = [row[0] for row in cursor.fetchall()]
        conn.close()
        return result

    def show_org_list():
        win = tk.Toplevel()
        win.title("Організації")
        make_window_fullscreen(win)
        setup_keyboard_bindings(win)

        tk.Label(win, text="Список організацій", font=("Segoe UI", 18, "bold")).pack(pady=10)

        orgs = get_unique_organizations()
        if not orgs:
            tk.Label(win, text="Організацій не знайдено").pack(pady=20)
            return
        
        listbox = tk.Listbox(win, font=("Segoe UI", 14), width=50, height=15)
        listbox.pack(pady=10)

        for org in orgs:
            listbox.insert(tk.END, org)

        def select():
            sel = listbox.curselection()
            if sel:
                organization_entry.delete(0, tk.END)
                organization_entry.insert(0, listbox.get(sel[0]))
                win.destroy()

        tk.Button(win, text="Вибрати", command=select,
                  font=("Segoe UI", 14), bg="#2962FF", fg="white")\
            .pack(pady=10)

    btn_style = {"font": ("Segoe UI", 13, "bold"), "width": 16, "pady": 6}

    tk.Button(buttons_frame, text="Пошук", command=search_readers,
              bg="#1976D2", fg="white", **btn_style)\
        .pack(side="left", padx=10)

    tk.Button(buttons_frame, text="Очистити", command=clear_fields,
              bg="#455A64", fg="white", **btn_style)\
        .pack(side="left", padx=10)

    tk.Button(buttons_frame, text="Організації", command=show_org_list,
              bg="#7B1FA2", fg="white", **btn_style)\
        .pack(side="left", padx=10)

    results_frame = tk.LabelFrame(
        main_frame,
        text="Результати пошуку",
        font=("Segoe UI", 16, "bold"),
        bg="white",
        padx=10,
        pady=10
    )
    results_frame.pack(fill="both", expand=True, pady=15)

    columns = ("ID", "ПІБ", "Адреса", "Тип", "Університет", "Факультет", "Організація")
    results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=18)

    widths = {"ID": 60, "ПІБ": 180, "Адреса": 180, "Тип": 120, "Університет": 150, "Факультет": 150, "Організація": 150}

    for col in columns:
        results_tree.heading(col, text=col)
        results_tree.column(col, width=widths[col], anchor="w")

    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results_tree.yview)
    results_tree.configure(yscrollcommand=scrollbar.set)

    results_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    total_label = tk.Label(main_frame, text="Знайдено читачів: 0", font=("Segoe UI", 13, "bold"), bg="#ECEFF1")
    total_label.pack(pady=5)

    tk.Button(main_frame, text="Закрити (ESC)", command=readers_window.destroy,
              bg="#D32F2F", fg="white", font=("Segoe UI", 13, "bold"), width=16, pady=6)\
        .pack(pady=5)

    university_entry.focus_set()

def show_inactive_readers_admin_window():
    import tkinter as tk
    from tkinter import ttk, messagebox

    def get_inactive_readers_from_visits():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    r.reader_id,
                    r.user_name,
                    r.address,
                    r.reader_type,
                    r.university,
                    r.faculty,
                    r.organization,
                    COALESCE(MAX(lv.visit_date), 'Ніколи не відвідував') as last_visit_date,
                    CASE 
                        WHEN MAX(lv.visit_date) IS NULL THEN 'Ніколи не відвідував'
                        ELSE CONCAT(DATEDIFF(CURDATE(), MAX(lv.visit_date)), ' днів тому')
                    END as days_since_last_visit,
                    COALESCE(COUNT(lv.visit_id), 0) as total_visits,
                    CASE 
                        WHEN MAX(lv.visit_date) IS NULL THEN 'Ніколи не був'
                        WHEN DATEDIFF(CURDATE(), MAX(lv.visit_date)) > 90 THEN 'Більше 3 місяців'
                        WHEN DATEDIFF(CURDATE(), MAX(lv.visit_date)) > 30 THEN 'Більше 1 місяця'
                        WHEN DATEDIFF(CURDATE(), MAX(lv.visit_date)) > 7 THEN 'Більше 1 тижня'
                        ELSE 'Активний (менше 1 тижня)'
                    END as activity_status
                FROM Readers r
                LEFT JOIN LibraryVisits lv ON r.reader_id = lv.reader_id
                GROUP BY r.reader_id
                ORDER BY 
                    CASE WHEN MAX(lv.visit_date) IS NULL THEN 1 ELSE 0 END,
                    MAX(lv.visit_date) DESC
            """)

            result = cursor.fetchall()
            conn.close()
            return result

        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося отримати список читачів:\n{e}")
            return []

    def search_inactive_readers():
        search_type = search_var.get()

        for item in results_tree.get_children():
            results_tree.delete(item)

        loading_label.config(text="Завантаження…")
        main_window.update()

        readers = get_inactive_readers_from_visits()
        filtered = []

        if search_type == "all":
            filtered = readers

        elif search_type == "range":
            try:
                f = int(days_from_entry.get())
                t = int(days_to_entry.get())

                for r in readers:
                    if r[7] != 'Ніколи не відвідував' and "днів" in r[8]:
                        d = int(r[8].split()[0])
                        if f <= d <= t:
                            filtered.append(r)

            except:
                messagebox.showerror("Помилка", "Некоректний діапазон")
                return

        elif search_type == "more_than":
            try:
                x = int(days_entry.get())
                for r in readers:
                    if r[7] != 'Ніколи не відвідував' and "днів" in r[8]:
                        if int(r[8].split()[0]) >= x:
                            filtered.append(r)
                    elif r[7] == "Ніколи не відвідував":
                        filtered.append(r)
            except:
                messagebox.showerror("Помилка", "Некоректне число днів")
                return

        for i, r in enumerate(filtered):
            tag = "active"
            if r[7] == "Ніколи не відвідував":
                tag = "never_visited"
            elif "днів" in r[8]:
                d = int(r[8].split()[0])
                if d > 90:
                    tag = "very_inactive"
                elif d > 30:
                    tag = "inactive"
                elif d > 7:
                    tag = "less_active"

            results_tree.insert("", "end", values=(i+1,*r), tags=(tag,))

        result_count_label.config(text=f"Знайдено: {len(filtered)}")
        loading_label.config(text="")

    main_window = tk.Toplevel()
    main_window.title("Активність читачів — Адмін панель")
    make_window_fullscreen(main_window)
    setup_keyboard_bindings(main_window)

    main_window.configure(bg="#F0F2F5")

    header = tk.Frame(main_window, bg="#1F4E79", height=80)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Активність читачів бібліотеки",
        bg="#1F4E79",
        fg="white",
        font=("Segoe UI", 26, "bold")
    ).pack(pady=15)

    control_panel = tk.Frame(main_window, bg="white", padx=20, pady=20, bd=1, relief="solid")
    control_panel.pack(fill="x", padx=20, pady=15)
    control_panel.configure(highlightbackground="#D0D0D0")

    tk.Label(
        control_panel,
        text="Фільтрація читачів",
        font=("Segoe UI", 16, "bold"),
        bg="white",
        fg="#1F4E79"
    ).pack(anchor="w")

    top_controls = tk.Frame(control_panel, bg="white")
    top_controls.pack(fill="x", pady=10)

    tk.Label(top_controls, text="Тип пошуку:", font=("Segoe UI", 12), bg="white").pack(side="left")

    search_var = tk.StringVar(value="all")
    options = [
        ("Всі читачі", "all"),
        ("Більше ніж (днів)", "more_than"),
        ("Діапазон", "range")
    ]

    for t, v in options:
        ttk.Radiobutton(top_controls, text=t, variable=search_var, value=v,
                        command=lambda: update_search_controls()).pack(side="left", padx=10)

    days_frame = tk.Frame(top_controls, bg="white")
    tk.Label(days_frame, text="днів ≥", bg="white", font=("Segoe UI", 12)).pack(side="left")
    days_entry = tk.Entry(days_frame, font=("Segoe UI", 12), width=8)
    days_entry.insert(0, "30")
    days_entry.pack(side="left", padx=5)

    range_frame = tk.Frame(top_controls, bg="white")
    tk.Label(range_frame, text="від", bg="white", font=("Segoe UI", 12)).pack(side="left")
    days_from_entry = tk.Entry(range_frame, font=("Segoe UI", 12), width=8)
    days_from_entry.insert(0, "20")
    days_from_entry.pack(side="left", padx=5)
    tk.Label(range_frame, text="до", bg="white", font=("Segoe UI", 12)).pack(side="left")
    days_to_entry = tk.Entry(range_frame, font=("Segoe UI", 12), width=8)
    days_to_entry.insert(0, "90")
    days_to_entry.pack(side="left", padx=5)

    btns = tk.Frame(control_panel, bg="white")
    btns.pack(fill="x", pady=10)

    search_btn = tk.Button(
        btns,
        text="Пошук",
        command=search_inactive_readers,
        bg="#0078D4",
        fg="white",
        font=("Segoe UI", 13, "bold"),
        padx=20,
        pady=7
    )
    search_btn.pack(side="left", padx=5)

    close_btn = tk.Button(
        btns,
        text="Закрити",
        command=main_window.destroy,
        bg="#C62828",
        fg="white",
        font=("Segoe UI", 13, "bold"),
        padx=20,
        pady=7
    )
    close_btn.pack(side="left", padx=5)

    bottom_controls = tk.Frame(control_panel, bg="white")
    bottom_controls.pack(fill="x", pady=5)

    loading_label = tk.Label(bottom_controls, text="", bg="white", font=("Segoe UI", 12))
    loading_label.pack(side="left")

    result_count_label = tk.Label(bottom_controls, text="", bg="white", fg="green", font=("Segoe UI", 12, "bold"))
    result_count_label.pack(side="left", padx=20)

    table_frame = tk.Frame(main_window, bg="#F0F2F5")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = (
        "№", "ID", "ПІБ", "Адреса", "Тип",
        "Університет", "Факультет", "Організація",
        "Останнє", "Статус", "Всього", "Активність"
    )

    results_tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=25
    )

    for col in columns:
        results_tree.heading(col, text=col, anchor="w")
        results_tree.column(col, width=150, anchor="w")

    results_tree.tag_configure("never_visited", background="#FFCDD2")
    results_tree.tag_configure("very_inactive", background="#FFE0B2")
    results_tree.tag_configure("inactive", background="#FFF9C4")
    results_tree.tag_configure("less_active", background="#DCEDC8")
    results_tree.tag_configure("active", background="#C8E6C9")

    vs = ttk.Scrollbar(table_frame, orient="vertical", command=results_tree.yview)
    hs = ttk.Scrollbar(table_frame, orient="horizontal", command=results_tree.xview)
    results_tree.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)

    results_tree.grid(row=0, column=0, sticky="nsew")
    vs.grid(row=0, column=1, sticky="ns")
    hs.grid(row=1, column=0, sticky="ew")

    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    legend = tk.Frame(main_window, bg="white", padx=15, pady=10, bd=1, relief="solid")
    legend.pack(fill="x", padx=20, pady=10)

    tk.Label(
        legend, text="Легенда:", bg="white",
        font=("Segoe UI", 12, "bold"), fg="#1F4E79"
    ).pack(side="left")

    legend_items = [
        ("Ніколи не відвідував", "#FFCDD2"),
        ("Більше 3 місяців", "#FFE0B2"),
        ("Більше 1 місяця", "#FFF9C4"),
        ("Більше 1 тижня", "#DCEDC8"),
        ("Активний", "#C8E6C9")
    ]

    for text, color in legend_items:
        box = tk.Frame(legend, width=18, height=18, bg=color, bd=1, relief="solid")
        box.pack(side="left", padx=10)
        tk.Label(legend, text=text, bg="white", font=("Segoe UI", 10)).pack(side="left", padx=5)

    def update_search_controls():
        days_frame.pack_forget()
        range_frame.pack_forget()

        if search_var.get() == "more_than":
            days_frame.pack(side="left", padx=10)
        elif search_var.get() == "range":
            range_frame.pack(side="left", padx=10)

    update_search_controls()
    search_inactive_readers()

def show_add_user_window():
    add_user_window = tk.Toplevel()
    add_user_window.title("Додати користувача")
    make_window_fullscreen(add_user_window)

    add_user_window.configure(bg="#f4f6fb")

    header_frame = tk.Frame(add_user_window, bg="#f4f6fb")
    header_frame.pack(fill="x", pady=10)

    tk.Label(
        header_frame,
        text="ДОДАТИ НОВОГО КОРИСТУВАЧА",
        font=("Arial", 20, "bold"),
        fg="#1f3b6f",
        bg="#f4f6fb"
    ).pack(pady=5)

    tk.Label(
        header_frame,
        text="Заповніть логін, пароль та оберіть роль. Для деяких ролей потрібні додаткові дані.",
        font=("Arial", 11),
        fg="#445",
        bg="#f4f6fb"
    ).pack()

    content_frame = tk.Frame(add_user_window, bg="#f4f6fb", padx=30, pady=20)
    content_frame.pack(fill="both", expand=True)

    content_frame.grid_columnconfigure(0, weight=0)
    content_frame.grid_columnconfigure(1, weight=1)
    content_frame.grid_columnconfigure(2, weight=0)

    tk.Label(
        content_frame,
        text="Логін:",
        font=("Arial", 13, "bold"),
        bg="#f4f6fb"
    ).grid(row=0, column=0, sticky="e", pady=10, padx=(0, 10))
    login_entry = tk.Entry(content_frame, width=40, font=("Arial", 13))
    login_entry.grid(row=0, column=1, pady=10, sticky="w")

    tk.Label(
        content_frame,
        text="Пароль:",
        font=("Arial", 13, "bold"),
        bg="#f4f6fb"
    ).grid(row=1, column=0, sticky="e", pady=10, padx=(0, 10))
    password_entry = tk.Entry(content_frame, width=40, font=("Arial", 13), show="*")
    password_entry.grid(row=1, column=1, pady=10, sticky="w")

    def toggle_password_visibility():
        if password_entry.cget("show") == "*":
            password_entry.config(show="")
            show_hide_btn.config(text="Сховати")
        else:
            password_entry.config(show="*")
            show_hide_btn.config(text="Показати")

    show_hide_btn = tk.Button(
        content_frame,
        text="Показати",
        font=("Arial", 9),
        command=toggle_password_visibility
    )
    show_hide_btn.grid(row=1, column=2, padx=(10, 0), sticky="w")

    password_warning = tk.Label(
        content_frame,
        text="Пароль має бути не менше 4 символів",
        font=("Arial", 9),
        fg="red",
        bg="#f4f6fb"
    )
    password_warning.grid(row=2, column=1, sticky="w", pady=(0, 5))
    password_warning.grid_remove()

    tk.Label(
        content_frame,
        text="Роль:",
        font=("Arial", 13, "bold"),
        bg="#f4f6fb"
    ).grid(row=3, column=0, sticky="e", pady=10, padx=(0, 10))

    role_var = tk.StringVar(value="")
    role_combo = ttk.Combobox(
        content_frame,
        textvariable=role_var,
        state="readonly",
        font=("Arial", 12),
        width=25,
        values=[
            "Reader",
            "Librarian",
            "Writer",
            "Operator",
            "Admin",
            "Learner",
            "Guest"
        ]
    )
    role_combo.grid(row=3, column=1, sticky="w", pady=10)

    role_hint_label = tk.Label(
        content_frame,
        text="Для Reader / Librarian / Writer будуть потрібні додаткові дані нижче.",
        font=("Arial", 9),
        fg="#555",
        bg="#f4f6fb"
    )
    role_hint_label.grid(row=4, column=1, sticky="w")

    reader_frame = tk.LabelFrame(
        content_frame,
        text="Дані читача (Reader)",
        font=("Arial", 11, "bold"),
        bg="#f4f6fb",
        padx=20,
        pady=15
    )
    reader_frame.grid(row=5, column=0, columnspan=3, sticky="ew", pady=15)
    reader_frame.grid_columnconfigure(0, weight=0)
    reader_frame.grid_columnconfigure(1, weight=1)
    reader_frame.grid_remove()

    tk.Label(
        reader_frame,
        text="ПІБ читача:",
        font=("Arial", 12),
        bg="#f4f6fb"
    ).grid(row=0, column=0, sticky="e", pady=5, padx=(0, 10))
    reader_name_entry = tk.Entry(reader_frame, width=45, font=("Arial", 12))
    reader_name_entry.grid(row=0, column=1, sticky="w", pady=5)

    tk.Label(
        reader_frame,
        text="Адреса:",
        font=("Arial", 12),
        bg="#f4f6fb"
    ).grid(row=1, column=0, sticky="e", pady=5, padx=(0, 10))
    reader_address_entry = tk.Entry(reader_frame, width=45, font=("Arial", 12))
    reader_address_entry.grid(row=1, column=1, sticky="w", pady=5)

    tk.Label(
        reader_frame,
        text="Тип читача:",
        font=("Arial", 12),
        bg="#f4f6fb"
    ).grid(row=2, column=0, sticky="e", pady=5, padx=(0, 10))
    reader_type_var = tk.StringVar(value="")
    reader_type_combo = ttk.Combobox(
        reader_frame,
        textvariable=reader_type_var,
        state="readonly",
        font=("Arial", 11),
        width=30,
        values=["Студент", "Викладач", "Науковець", "Інше"]
    )
    reader_type_combo.grid(row=2, column=1, sticky="w", pady=5)

    student_frame = tk.Frame(reader_frame, bg="#f4f6fb")
    student_frame.grid_columnconfigure(0, weight=0)
    student_frame.grid_columnconfigure(1, weight=1)

    tk.Label(
        student_frame,
        text="Університет:",
        font=("Arial", 12),
        bg="#f4f6fb"
    ).grid(row=0, column=0, sticky="e", pady=5, padx=(0, 10))
    reader_university_entry = tk.Entry(student_frame, width=45, font=("Arial", 12))
    reader_university_entry.grid(row=0, column=1, sticky="w", pady=5)

    tk.Label(
        student_frame,
        text="Факультет:",
        font=("Arial", 12),
        bg="#f4f6fb"
    ).grid(row=1, column=0, sticky="e", pady=5, padx=(0, 10))
    reader_faculty_entry = tk.Entry(student_frame, width=45, font=("Arial", 12))
    reader_faculty_entry.grid(row=1, column=1, sticky="w", pady=5)

    tk.Label(
        reader_frame,
        text="Організація (для науковця):",
        font=("Arial", 12),
        bg="#f4f6fb"
    ).grid(row=4, column=0, sticky="e", pady=5, padx=(0, 10))
    reader_organization_entry = tk.Entry(reader_frame, width=45, font=("Arial", 12))
    reader_organization_entry.grid(row=4, column=1, sticky="w", pady=5)

    student_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
    student_frame.grid_remove()
    reader_organization_entry.grid_remove()

    librarian_frame = tk.LabelFrame(
        content_frame,
        text="Дані бібліотекаря (Librarian)",
        font=("Arial", 11, "bold"),
        bg="#f4f6fb",
        padx=20,
        pady=15
    )
    librarian_frame.grid(row=6, column=0, columnspan=3, sticky="ew", pady=10)
    librarian_frame.grid_columnconfigure(0, weight=0)
    librarian_frame.grid_columnconfigure(1, weight=1)
    librarian_frame.grid_remove()

    tk.Label(
        librarian_frame,
        text="Ім'я бібліотекаря:",
        font=("Arial", 12),
        bg="#f4f6fb"
    ).grid(row=0, column=0, sticky="e", pady=5, padx=(0, 10))
    librarian_name_entry = tk.Entry(librarian_frame, width=45, font=("Arial", 12))
    librarian_name_entry.grid(row=0, column=1, sticky="w", pady=5)

    tk.Label(
        librarian_frame,
        text="Читальний зал:",
        font=("Arial", 12),
        bg="#f4f6fb"
    ).grid(row=1, column=0, sticky="e", pady=5, padx=(0, 10))

    reading_room_var = tk.StringVar(value="")
    reading_room_combo = ttk.Combobox(
        librarian_frame,
        textvariable=reading_room_var,
        state="readonly",
        font=("Arial", 11),
        width=35
    )
    reading_room_combo.grid(row=1, column=1, sticky="w", pady=5)

    room_id_map = {}
    try:
        rooms = get_reading_rooms()
        values = []
        for r_id, r_name in rooms:
            label = f"{r_id}: {r_name}"
            values.append(label)
            room_id_map[label] = r_id
        reading_room_combo["values"] = values
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося завантажити читальні зали:\n{e}")

    writer_frame = tk.LabelFrame(
        content_frame,
        text="Дані автора (Writer)",
        font=("Arial", 11, "bold"),
        bg="#f4f6fb",
        padx=20,
        pady=15
    )
    writer_frame.grid(row=7, column=0, columnspan=3, sticky="ew", pady=10)
    writer_frame.grid_columnconfigure(0, weight=0)
    writer_frame.grid_columnconfigure(1, weight=1)
    writer_frame.grid_remove()

    tk.Label(
        writer_frame,
        text="Ім'я:",
        font=("Arial", 12),
        bg="#f4f6fb"
    ).grid(row=0, column=0, sticky="e", pady=5, padx=(0, 10))
    author_name_entry = tk.Entry(writer_frame, width=45, font=("Arial", 12))
    author_name_entry.grid(row=0, column=1, sticky="w", pady=5)

    tk.Label(
        writer_frame,
        text="Прізвище:",
        font=("Arial", 12),
        bg="#f4f6fb"
    ).grid(row=1, column=0, sticky="e", pady=5, padx=(0, 10))
    author_surname_entry = tk.Entry(writer_frame, width=45, font=("Arial", 12))
    author_surname_entry.grid(row=1, column=1, sticky="w", pady=5)

    tk.Label(
        writer_frame,
        text="Країна:",
        font=("Arial", 12),
        bg="#f4f6fb"
    ).grid(row=2, column=0, sticky="e", pady=5, padx=(0, 10))
    author_country_entry = tk.Entry(writer_frame, width=45, font=("Arial", 12))
    author_country_entry.grid(row=2, column=1, sticky="w", pady=5)

    tk.Label(
        writer_frame,
        text="Дата народження:",
        font=("Arial", 12),
        bg="#f4f6fb"
    ).grid(row=3, column=0, sticky="e", pady=5, padx=(0, 10))
    author_birth_date = DateEntry(
        writer_frame,
        width=20,
        background="darkblue",
        foreground="white",
        borderwidth=2,
        date_pattern="yyyy-mm-dd",
        font=("Arial", 11)
    )
    author_birth_date.grid(row=3, column=1, sticky="w", pady=5)

    def update_reader_type_fields(*args):
        r_type = reader_type_var.get()
        student_frame.grid_remove()
        reader_organization_entry.grid_remove()

        if r_type == "Студент":
            student_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
        elif r_type == "Науковець":
            reader_organization_entry.grid(row=4, column=1, sticky="w", pady=5)

    def update_role_frames(*args):
        reader_frame.grid_remove()
        librarian_frame.grid_remove()
        writer_frame.grid_remove()

        r = role_var.get()
        if r == "Reader":
            reader_frame.grid()
        elif r == "Librarian":
            librarian_frame.grid()
        elif r == "Writer":
            writer_frame.grid()

    reader_type_combo.bind("<<ComboboxSelected>>", update_reader_type_fields)
    role_combo.bind("<<ComboboxSelected>>", update_role_frames)

    buttons_frame = tk.Frame(add_user_window, bg="#f4f6fb")
    buttons_frame.pack(pady=15)

    def clear_form():
        login_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        role_var.set("")
        reader_name_entry.delete(0, tk.END)
        reader_address_entry.delete(0, tk.END)
        reader_type_var.set("")
        reader_university_entry.delete(0, tk.END)
        reader_faculty_entry.delete(0, tk.END)
        reader_organization_entry.delete(0, tk.END)
        librarian_name_entry.delete(0, tk.END)
        reading_room_var.set("")
        author_name_entry.delete(0, tk.END)
        author_surname_entry.delete(0, tk.END)
        author_country_entry.delete(0, tk.END)
        reader_frame.grid_remove()
        librarian_frame.grid_remove()
        writer_frame.grid_remove()
        student_frame.grid_remove()
        reader_organization_entry.grid_remove()
        password_warning.grid_remove()

    def validate_fields():
        login = login_entry.get().strip()
        password = password_entry.get().strip()
        role = role_var.get()

        if not login or not password:
            messagebox.showerror("Помилка", "Логін і пароль є обов'язковими!")
            return False

        if len(password) < 4:
            password_warning.grid()
            messagebox.showerror("Помилка", "Пароль має бути не менше 4 символів!")
            return False
        else:
            password_warning.grid_remove()

        if not role:
            messagebox.showerror("Помилка", "Оберіть роль користувача!")
            return False

        if role == "Reader":
            if not reader_name_entry.get().strip():
                messagebox.showerror("Помилка", "Вкажіть ПІБ читача!")
                return False
            if reader_type_var.get() == "Студент":
                if not reader_university_entry.get().strip() or not reader_faculty_entry.get().strip():
                    messagebox.showerror("Помилка", "Для студента обов'язкові Університет та Факультет!")
                    return False
            if reader_type_var.get() == "Науковець":
                if not reader_organization_entry.get().strip():
                    messagebox.showerror("Помилка", "Для науковця вкажіть організацію!")
                    return False

        if role == "Librarian":
            if not librarian_name_entry.get().strip():
                messagebox.showerror("Помилка", "Вкажіть ім'я бібліотекаря!")
                return False
            if not reading_room_var.get():
                messagebox.showerror("Помилка", "Оберіть читальний зал!")
                return False

        if role == "Writer":
            if not author_name_entry.get().strip() or not author_surname_entry.get().strip():
                messagebox.showerror("Помилка", "Для Writer обов'язкові ім'я та прізвище!")
                return False

        return True

    def add_user():
        if not validate_fields():
            return

        login = login_entry.get().strip()
        password = password_entry.get().strip()
        role = role_var.get()

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Users WHERE login = %s", (login,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Помилка", f"Користувач з логіном '{login}' вже існує!")
                return

            cursor.execute(
                "INSERT INTO Users (login, password, role) VALUES (%s, %s, %s)",
                (login, password, role)
            )
            user_id = cursor.lastrowid

            if role == "Reader":
                r_name = reader_name_entry.get().strip()
                r_addr = reader_address_entry.get().strip()
                r_type = reader_type_var.get() or None
                r_uni = reader_university_entry.get().strip() or None
                r_fac = reader_faculty_entry.get().strip() or None
                r_org = reader_organization_entry.get().strip() or None

                cursor.execute(
                    """
                    INSERT INTO Readers 
                        (user_id, user_name, address, reader_type, university, faculty, organization)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (user_id, r_name, r_addr, r_type, r_uni, r_fac, r_org)
                )

            elif role == "Librarian":
                l_name = librarian_name_entry.get().strip()
                room_label = reading_room_var.get()
                room_id = room_id_map.get(room_label)

                cursor.execute(
                    """
                    INSERT INTO Librarians (librarian_id, name, reading_room_id)
                    VALUES (%s, %s, %s)
                    """,
                    (user_id, l_name, room_id)
                )

            elif role == "Writer":
                a_name = author_name_entry.get().strip()
                a_surname = author_surname_entry.get().strip()
                a_country = author_country_entry.get().strip()
                a_birth = author_birth_date.get_date().strftime("%Y-%m-%d")

                cursor.execute(
                    """
                    INSERT INTO Authors (name, surname, country, user_id, birth_year)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (a_name, a_surname, a_country, user_id, a_birth)
                )

            conn.commit()

            messagebox.showinfo(
                "Успіх",
                f"Користувача '{login}' успішно створено з роллю '{role}'!"
            )
            clear_form()
            login_entry.focus_set()

        except Exception as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Помилка", f"Помилка при додаванні користувача:\n{e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    add_btn = tk.Button(
        buttons_frame,
        text="Створити користувача (Enter)",
        command=add_user,
        bg="#28a745",
        fg="white",
        font=("Arial", 13, "bold"),
        padx=20,
        pady=5
    )
    add_btn.pack(side="left", padx=10)

    clear_btn = tk.Button(
        buttons_frame,
        text="Очистити форму",
        command=clear_form,
        bg="#ffc107",
        fg="black",
        font=("Arial", 12),
        padx=20,
        pady=5
    )
    clear_btn.pack(side="left", padx=10)

    close_btn = tk.Button(
        buttons_frame,
        text="Закрити (ESC)",
        command=add_user_window.destroy,
        bg="#dc3545",
        fg="white",
        font=("Arial", 12),
        padx=20,
        pady=5
    )
    close_btn.pack(side="left", padx=10)

    add_user_window.bind("<Return>", lambda e: add_user())
    login_entry.focus_set()

def show_pending_requests(parent_window):
    requests_window = tk.Toplevel(parent_window)
    requests_window.title("Запити на підтвердження ролі")
    make_window_fullscreen(requests_window)
    
    setup_keyboard_bindings(requests_window)
    
    tk.Label(requests_window, text="Запити на підтвердження ролі", 
             font=("Arial", 16, "bold")).pack(pady=10)

    table_frame = tk.Frame(requests_window)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(table_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    columns = ("ID", "Логін", "Бажана роль", "Додаткова інформація", "Статус")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                       yscrollcommand=scrollbar.set)
    
    scrollbar.config(command=tree.yview)

    tree.heading("ID", text="ID")
    tree.heading("Логін", text="Логін")
    tree.heading("Бажана роль", text="Бажана роль")
    tree.heading("Додаткова інформація", text="Додаткова інформація")
    tree.heading("Статус", text="Статус")

    tree.column("ID", width=50, anchor=tk.CENTER)
    tree.column("Логін", width=120, anchor=tk.W)
    tree.column("Бажана роль", width=100, anchor=tk.CENTER)
    tree.column("Додаткова інформація", width=500, anchor=tk.W)
    tree.column("Статус", width=100, anchor=tk.CENTER)

    tree.pack(fill=tk.BOTH, expand=True)

    def load_pending_users():
        tree.delete(*tree.get_children())
        
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT user_id, login, role, usercol 
                FROM Users 
                WHERE role = 'Guest'
                ORDER BY user_id DESC
            """)
            
            users = cursor.fetchall()
            
            for user in users:
                user_id, login, role, usercol = user
                
                if usercol:
                    try:
                        user_data = json.loads(usercol)
                        requested_role = user_data.get('requested_role', 'N/A')
                        status = user_data.get('status', 'pending')
                        
                        info_parts = []
                        if requested_role == 'Reader':
                            info_parts.append(f"Ім'я: {user_data.get('name', 'N/A')}")
                            info_parts.append(f"Адреса: {user_data.get('address', 'N/A')}")
                            info_parts.append(f"Тип: {user_data.get('reader_type', 'N/A')}")
                            if 'university' in user_data:
                                info_parts.append(f"Університет: {user_data.get('university')}")
                                info_parts.append(f"Факультет: {user_data.get('faculty')}")
                            if 'organization' in user_data:
                                info_parts.append(f"Організація: {user_data.get('organization')}")
                        elif requested_role == 'Librarian':
                            info_parts.append(f"Ім'я: {user_data.get('name', 'N/A')}")
                            info_parts.append(f"Зал: {user_data.get('reading_room_id', 'N/A')}")
                        elif requested_role == 'Writer':
                            info_parts.append(f"Ім'я: {user_data.get('name', 'N/A')}")
                            info_parts.append(f"Прізвище: {user_data.get('surname', 'N/A')}")
                            info_parts.append(f"Країна: {user_data.get('country', 'N/A')}")
                            info_parts.append(f"Дата народження: {user_data.get('birth_date', 'N/A')}")
                        
                        additional_info = ", ".join(info_parts)
                        
                    except json.JSONDecodeError:
                        requested_role = "N/A"
                        additional_info = "Помилка читання даних"
                        status = "error"
                else:
                    requested_role = "N/A"
                    additional_info = "Немає даних"
                    status = "pending"
                
                tree.insert("", tk.END, values=(user_id, login, requested_role, 
                                            additional_info, status))
        
        except Exception as err:
            messagebox.showerror("Помилка", f"Помилка БД: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def approve_user():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Увага", "Виберіть користувача зі списку")
            return
        
        item = tree.item(selected[0])
        user_id = item['values'][0]
        requested_role = item['values'][2]
        
        if requested_role == "N/A":
            messagebox.showerror("Помилка", "Не вдалося визначити бажану роль")
            return
        
        result = messagebox.askyesno("Підтвердження", 
                                     f"Підтвердити роль '{requested_role}' для користувача ID {user_id}?")
        if not result:
            return
        
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT usercol FROM Users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            
            if not result or not result[0]:
                messagebox.showerror("Помилка", "Не знайдено даних користувача")
                return
            
            user_data = json.loads(result[0])
            
            if not conn.in_transaction:
                conn.start_transaction()
            
            cursor.execute("UPDATE Users SET role = %s WHERE user_id = %s", 
                          (requested_role, user_id))
            
            if requested_role == 'Reader':
                cursor.execute("""
                    INSERT INTO Readers (user_id, user_name, address, reader_type, 
                                       university, faculty, organization) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (user_id, 
                     user_data.get('name'),
                     user_data.get('address'),
                     user_data.get('reader_type'),
                     user_data.get('university'),
                     user_data.get('faculty'),
                     user_data.get('organization')))
                     
            elif requested_role == 'Librarian':
                try:
                    room_id = int(user_data.get('reading_room_id'))
                except (ValueError, TypeError):
                    messagebox.showerror("Помилка", "Невірний ID читального залу")
                    conn.rollback()
                    return
                    
                cursor.execute("""
                    INSERT INTO Librarians (librarian_id, name, reading_room_id) 
                    VALUES (%s, %s, %s)
                """, (user_id, user_data.get('name'), room_id))
                
            elif requested_role == 'Writer':
                cursor.execute("""
                    INSERT INTO Authors (user_id, name, surname, country, birth_year) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, 
                     user_data.get('name'),
                     user_data.get('surname'),
                     user_data.get('country'),
                     user_data.get('birth_date')))
            
            cursor.execute("UPDATE Users SET usercol = NULL WHERE user_id = %s", (user_id,))
            
            conn.commit()
            messagebox.showinfo("Успіх", f"Користувач успішно підтверджений з роллю '{requested_role}'")
            load_pending_users()
            
        except Exception as err:
            messagebox.showerror("Помилка", f"Помилка БД: {err}")
            if conn:
                conn.rollback()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def reject_user():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Увага", "Виберіть користувача зі списку")
            return
        
        item = tree.item(selected[0])
        user_id = item['values'][0]
        login = item['values'][1]
        
        result = messagebox.askyesno("Підтвердження", 
                                     f"Відхилити запит користувача '{login}' (ID {user_id})?\n"
                                     "Акаунт буде видалено!")
        if not result:
            return
        
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
            conn.commit()
            
            messagebox.showinfo("Успіх", "Користувач відхилений та видалений")
            load_pending_users()
            
        except Exception as err:
            messagebox.showerror("Помилка", f"Помилка БД: {err}")
            if conn:
                conn.rollback()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    button_frame = tk.Frame(requests_window)
    button_frame.pack(pady=10)

    approve_btn = tk.Button(button_frame, text="Підтвердити (Enter)", command=approve_user, 
           bg="green", fg="white", font=("Arial", 12), 
           padx=20, pady=5)
    approve_btn.pack(side=tk.LEFT, padx=10)
    
    reject_btn = tk.Button(button_frame, text="Відхилити", command=reject_user, 
           bg="red", fg="white", font=("Arial", 12), 
           padx=20, pady=5)
    reject_btn.pack(side=tk.LEFT, padx=10)
    
    refresh_btn = tk.Button(button_frame, text="Оновити", command=load_pending_users, 
           bg="blue", fg="white", font=("Arial", 12), 
           padx=20, pady=5)
    refresh_btn.pack(side=tk.LEFT, padx=10)

    close_btn = tk.Button(button_frame, text="Закрити (ESC)", command=requests_window.destroy, 
           bg="gray", fg="white", font=("Arial", 12), 
           padx=20, pady=5)
    close_btn.pack(side=tk.LEFT, padx=10)

    load_pending_users()

def create_modern_button(parent, text, command, bg_color="#4A90E2", hover_color="#357ABD", 
                        text_color="white", width=30, font_size=11):
    button = tk.Button(parent, text=text, command=command, 
                      bg=bg_color, fg=text_color, font=("Segoe UI", font_size, "bold"),
                      width=width, height=2, relief="flat", cursor="hand2",
                      activebackground=hover_color, activeforeground=text_color,
                      borderwidth=0)
    
    def on_enter(e):
        button.config(bg=hover_color, relief="raised")
    
    def on_leave(e):
        button.config(bg=bg_color, relief="flat")
    
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    
    return button

def create_styled_combobox(parent, values, width=40):
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Custom.TCombobox',
                   fieldbackground='white',
                   background='#E8F4FD',
                   bordercolor='#4A90E2',
                   arrowcolor='#4A90E2',
                   focuscolor='#4A90E2')
    
    combo = ttk.Combobox(parent, values=values, state="readonly", width=width,
                        style='Custom.TCombobox', font=("Segoe UI", 10))
    return combo

def show_operator_window(user_login):
    operator_window = tk.Tk()
    operator_window.title("Панель Оператора")
    make_window_fullscreen(operator_window)
    operator_window.configure(bg="#F8F9FA")
    operator_window.resizable(True, True)

    setup_keyboard_bindings(operator_window, is_main_window=True)

    def on_closing():
        if messagebox.askyesno("Підтвердження", "Вийти з облікового запису та повернутися до вікна входу?"):
            operator_window.destroy()
            login_window.show_login_window()

    operator_window.protocol("WM_DELETE_WINDOW", on_closing)

    try:
        operator_window.iconbitmap('admin_icon.ico')
    except:
        pass

    main_container = tk.Frame(operator_window, bg="#F8F9FA")
    main_container.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(main_container, bg="#F8F9FA", highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)

    style = ttk.Style()
    style.configure("Custom.Vertical.TScrollbar",
                    background="#E0E0E0",
                    troughcolor="#F5F5F5",
                    bordercolor="#D0D0D0",
                    arrowcolor="#888888",
                    darkcolor="#C0C0C0",
                    lightcolor="#F0F0F0")

    scrollbar.configure(style="Custom.Vertical.TScrollbar")

    scrollable_frame = tk.Frame(canvas, bg="#F8F9FA")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # ---------- Хедер ----------
    header_frame = tk.Frame(scrollable_frame, bg="#2C3E50", height=80)
    header_frame.pack(fill="x", pady=(0, 20))
    header_frame.pack_propagate(False)

    title_font = tkFont.Font(family="Segoe UI", size=18, weight="bold")
    welcome_label = tk.Label(
        header_frame,
        text=f"Вітаємо, {user_login}",
        font=title_font,
        bg="#2C3E50", fg="white"
    )
    welcome_label.pack(pady=10)

    subtitle_label = tk.Label(
        header_frame,
        text="Панель Оператора",
        font=("Segoe UI", 12),
        bg="#2C3E50", fg="#BDC3C7"
    )
    subtitle_label.pack()
    def create_section(parent, title, icon=""):
        section_frame = tk.Frame(parent, bg="white", relief="solid", borderwidth=1)

        title_frame = tk.Frame(section_frame, bg="#34495E", height=40)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text=f"{icon} {title}",
            font=("Segoe UI", 12, "bold"),
            bg="#34495E", fg="white"
        )
        title_label.pack(pady=8)

        content_frame = tk.Frame(section_frame, bg="white", padx=20, pady=15)
        content_frame.pack(fill="x")

        return section_frame, content_frame

    # =============== СЕКЦІЯ РОЗПОДІЛУ КНИГ ==================
    book_section_frame, book_section_content = create_section(
        scrollable_frame, "Розподіл Книг", ""
    )
    book_section_frame.pack(fill="x", padx=10, pady=10, anchor="n")

    tk.Label(
        book_section_content,
        text="Оберіть книгу для розподілу:",
        font=("Segoe UI", 10, "bold"),
        bg="white", fg="#2C3E50"
    ).pack(anchor="w", pady=(0, 5))

    # Книги
    books = get_books()
    book_map = {f"{title} (ID: {book_id})": book_id for book_id, title in books}
    book_combo = create_styled_combobox(
        book_section_content, list(book_map.keys()), width=50
    )
    book_combo.pack(pady=(0, 15))

    tk.Label(
        book_section_content,
        text="Тип доступу до книги:",
        font=("Segoe UI", 10, "bold"),
        bg="white", fg="#2C3E50"
    ).pack(anchor="w", pady=(0, 5))

    access_combo = create_styled_combobox(
        book_section_content,
        ["Тільки в читальній залі", "У читальній залі і вдома"],
        width=35
    )
    access_combo.current(0)
    access_combo.pack(pady=(0, 15))

    tk.Label(
        book_section_content,
        text="Читальні зали:",
        font=("Segoe UI", 10, "bold"),
        bg="white", fg="#2C3E50"
    ).pack(anchor="w", pady=(0, 5))

    rooms = get_reading_rooms()
    room_vars = []
    rooms_frame = tk.Frame(book_section_content, bg="white")
    rooms_frame.pack(fill='x', pady=(0, 15))

    # Чекбокси читальних залів
    for room_id, room_name in rooms:
        var = tk.IntVar(master=rooms_frame, value=0)
        checkbox = tk.Checkbutton(
            rooms_frame,
            text=room_name,
            variable=var,
            onvalue=1,
            offvalue=0,
            font=("Segoe UI", 9),
            bg="white",
            fg="#2C3E50",
            activebackground="white",
            selectcolor="#E8F4FD"
        )
        checkbox.pack(anchor='w', pady=2)
        room_vars.append((var, room_id))

    # Полиця / ряд
    location_frame = tk.Frame(book_section_content, bg="white")
    location_frame.pack(fill='x', pady=(0, 15))

    shelf_frame = tk.Frame(location_frame, bg="white")
    shelf_frame.pack(side="left", padx=(0, 20))

    tk.Label(
        shelf_frame,
        text="Полиця (Shelf):",
        font=("Segoe UI", 10, "bold"),
        bg="white", fg="#2C3E50"
    ).pack(anchor="w")
    shelf_combo = create_styled_combobox(
        shelf_frame, ["A", "B", "C", "D", "E"], width=5
    )
    shelf_combo.current(0)
    shelf_combo.pack()

    row_frame = tk.Frame(location_frame, bg="white")
    row_frame.pack(side="left")

    tk.Label(
        row_frame,
        text="Ряд (Row):",
        font=("Segoe UI", 10, "bold"),
        bg="white", fg="#2C3E50"
    ).pack(anchor="w")
    row_combo = create_styled_combobox(
        row_frame, [str(i) for i in range(1, 11)], width=5
    )
    row_combo.current(0)
    row_combo.pack()

    def on_save():
        selected_book = book_combo.get()
        if not selected_book:
            messagebox.showerror("Помилка", "Будь ласка, оберіть книгу.")
            return

        try:
            book_id = book_map[selected_book]
        except KeyError:
            messagebox.showerror("Помилка", "Не вдалося отримати ID книги.")
            return

        # вибрані зали
        selected_rooms = [room_id for var, room_id in room_vars if var.get() == 1]
        if not selected_rooms:
            messagebox.showerror("Помилка", "Оберіть хоча б один читальний зал.")
            return

        shelf = shelf_combo.get()
        row = row_combo.get()
        access_type = access_combo.get()

        if not shelf or not row:
            messagebox.showerror("Помилка", "Заповніть полицю та ряд.")
            return

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Оновлюємо тип доступу книги
            cursor.execute(
                "UPDATE Books SET access_type = %s WHERE book_id = %s",
                (access_type, book_id)
            )

            # Видаляємо старі розміщення цієї книги
            cursor.execute("DELETE FROM placements WHERE book_id = %s", (book_id,))

            # Додаємо нові розміщення
            for room_id in selected_rooms:
                cursor.execute(
                    """INSERT INTO placements (book_id, room_id, shelf, `row`)
                       VALUES (%s, %s, %s, %s)""",
                    (book_id, room_id, shelf, row)
                )

            conn.commit()

            messagebox.showinfo(
                "Успішно",
                f"Книгу розподілено до {len(selected_rooms)} читальних залів!\n"
                f"Полиця: {shelf}, Ряд: {row}\n"
                f"Тип доступу: {access_type}"
            )

            # очищення форми
            book_combo.set('')
            access_combo.current(0)
            shelf_combo.current(0)
            row_combo.current(0)
            for var, _ in room_vars:
                var.set(0)

        except Exception as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Помилка", f"Сталася помилка: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    save_btn = create_modern_button(
        book_section_content,
        "Розподілити книгу (Enter)",
        on_save,
        bg_color="#27AE60",
        hover_color="#229954",
        width=25
    )
    save_btn.pack(pady=10)

    # =============== ІНШІ СЕКЦІЇ ==================
    grid_container = tk.Frame(scrollable_frame, bg="#F8F9FA")
    grid_container.pack(fill="both", expand=True, padx=0, pady=0)

    grid_container.grid_columnconfigure(0, weight=1, uniform="group1")
    grid_container.grid_columnconfigure(1, weight=1, uniform="group1")

    # --- Основні операції ---
    operations_section_frame, operations_section_content = create_section(
        grid_container, "Основні Операції", ""
    )
    operations_section_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    buttons_frame1 = tk.Frame(operations_section_content, bg="white")
    buttons_frame1.pack(fill='x', pady=5)

    create_modern_button(
        buttons_frame1, "Редагувати книгу", show_edit_book_window,
        bg_color="#3498DB", hover_color="#2980B9", width=22
    ).pack(side="left", padx=5)

    create_modern_button(
        buttons_frame1, "Управління книгами",
        lambda: show_books_management_window(operator_window),
        bg_color="#9B59B6", hover_color="#8E44AD", width=22
    ).pack(side="left", padx=5)

    create_modern_button(
        buttons_frame1, "Управління авторами", show_admin_author_management,
        bg_color="#16A085", hover_color="#138D75", width=22
    ).pack(side="left", padx=5)

    # --- Статистика ---
    stats_section_frame, stats_section_content = create_section(
        grid_container, "Статистика та Звіти", ""
    )
    stats_section_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    stats_buttons = [
        ("Статистика бібліотекарів", show_librarian_stats, "#E74C3C", "#C0392B"),
        ("Популярні книги", show_popular_books_window, "#F39C12", "#E67E22"),
        ("Заборговані книги", show_admin_overdue_books, "#E67E22", "#D35400"),
        ("Активність читачів", show_inactive_readers_admin_window, "#1ABC9C", "#16A085"),
    ]

    for text, command, bg_color, hover_color in stats_buttons:
        create_modern_button(
            stats_section_content, text, command,
            bg_color=bg_color, hover_color=hover_color, width=35
        ).pack(pady=3)

    # --- Пошук та аналітика ---
    search_section_frame, search_section_content = create_section(
        grid_container, "Пошук та Аналітика", ""
    )
    search_section_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    search_buttons = [
        ("Хто тримає книгу", find_who_has_book, "#8E44AD", "#7D3C98"),
        ("Бібліотекарі за залом", get_librarians_worked_in_room, "#2ECC71", "#27AE60"),
        ("Пошук за назвою/автором", find_books_by_work_or_author, "#3498DB", "#2980B9"),
        ("Пошук читачів", show_readers_list_window, "#F39C12", "#E67E22"),
    ]

    for text, command, bg_color, hover_color in search_buttons:
        create_modern_button(
            search_section_content, text, command,
            bg_color=bg_color, hover_color=hover_color, width=35
        ).pack(pady=3)

    sql_section_frame, sql_section_content = create_section(
        grid_container, "SQL Query Editor", ""
    )
    sql_section_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    sql_example = """SELECT 
    b.book_id,
    b.title AS 'Назва книги',
    CONCAT(a.name, ' ', a.surname) AS 'Автор',
    b.access_type AS 'Тип доступу',
    b.quantity AS 'Кількість',
    b.inventory_number AS 'Інвентарний номер',
    c.name AS 'Категорія',
    p.name AS 'Видавництво',
    GROUP_CONCAT(DISTINCT CONCAT(rr.name, ' (', pl.shelf, '-', pl.`row`, ')') SEPARATOR ', ') AS 'Розміщення'
FROM books b
LEFT JOIN authors a ON b.author_id = a.author_id
LEFT JOIN categories c ON b.category_id = c.category_id
LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
LEFT JOIN placements pl ON b.book_id = pl.book_id
LEFT JOIN reading_rooms rr ON pl.room_id = rr.room_id
GROUP BY b.book_id
ORDER BY b.title;"""

    tk.Label(
        sql_section_content,
        text="Введіть SQL запит:",
        font=("Segoe UI", 10, "bold"),
        bg="white", fg="#2C3E50"
    ).pack(anchor="w", pady=(0, 5))

    sql_text = tk.Text(
        sql_section_content,
        height=8, width=70,
        font=("Consolas", 10),
        wrap=tk.WORD,
        bg="#1E1E1E", fg="#FFFFFF",
        insertbackground="white"
    )
    sql_text.pack(fill="both", expand=True, pady=(0, 10))

    sql_scrollbar = ttk.Scrollbar(sql_section_content, orient="vertical", command=sql_text.yview)
    sql_text.configure(yscrollcommand=sql_scrollbar.set)

    sql_buttons_frame = tk.Frame(sql_section_content, bg="white")
    sql_buttons_frame.pack(fill="x", pady=10)

    def execute_sql():
        sql_query = sql_text.get("1.0", tk.END).strip()

        if not sql_query:
            messagebox.showwarning("Попередження", "Введіть SQL запит!")
            return

        dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE', 'INSERT', 'UPDATE']
        if any(keyword in sql_query.upper() for keyword in dangerous_keywords):
            if not messagebox.askyesno(
                "Попередження",
                "Цей запит може змінити дані. Ви впевнені, що хочете продовжити?"
            ):
                return

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(sql_query)

            if sql_query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                show_sql_results(sql_query, columns, results)
            else:
                conn.commit()
                affected_rows = cursor.rowcount
                messagebox.showinfo(
                    "Успіх",
                    f"Запит виконано успішно!\nЗмінено рядків: {affected_rows}"
                )

        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка при виконанні SQL запиту:\n{str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def clear_sql():
        sql_text.delete("1.0", tk.END)

    def insert_example():
        sql_text.delete("1.0", tk.END)
        sql_text.insert("1.0", sql_example)

    def show_sql_results(query, columns, results):
        results_window = tk.Toplevel(operator_window)
        results_window.title("Результати SQL запиту")
        make_window_fullscreen(results_window)

        setup_keyboard_bindings(results_window)

        header_frame = tk.Frame(results_window, bg="#2C3E50", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="Результати SQL запиту",
            font=("Arial", 14, "bold"),
            bg="#2C3E50", fg="white"
        ).pack(pady=10)

        query_frame = tk.Frame(results_window, bg="#F8F9FA")
        query_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            query_frame,
            text="Запит:",
            font=("Arial", 10, "bold"),
            bg="#F8F9FA"
        ).pack(anchor="w")

        query_text = tk.Text(
            query_frame,
            height=3, width=80,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#1E1E1E", fg="#FFFFFF"
        )
        query_text.insert("1.0", query)
        query_text.config(state="disabled")
        query_text.pack(fill="x", pady=5)

        table_frame = tk.Frame(results_window)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="w")

        for row_data in results:
            tree.insert("", "end", values=row_data)

        scrollbar_tree = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_tree.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar_tree.pack(side="right", fill="y")

        stats_frame = tk.Frame(results_window, bg="#F8F9FA")
        stats_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            stats_frame,
            text=f"Знайдено рядків: {len(results)} | Колонок: {len(columns)}",
            font=("Arial", 10, "bold"),
            bg="#F8F9FA"
        ).pack()

        def export_results():
            from tkinter import filedialog
            import csv

            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Зберегти результати як CSV"
            )

            if not file_path:
                return

            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(columns)
                    for row_data in results:
                        writer.writerow(row_data)

                messagebox.showinfo("Успіх", f"Результати успішно експортовано у файл: {file_path}")
            except Exception as e:
                messagebox.showerror("Помилка", f"Помилка при експорті: {str(e)}")

        export_btn = tk.Button(
            results_window,
            text="Експортувати в CSV",
            command=export_results,
            bg="green", fg="white",
            font=("Arial", 10)
        )
        export_btn.pack(pady=10)

        close_btn = tk.Button(
            results_window,
            text="Закрити (ESC)",
            command=results_window.destroy,
            bg="red", fg="white",
            font=("Arial", 10)
        )
        close_btn.pack(pady=5)

    create_modern_button(
        sql_buttons_frame, "Приклад SELECT книг", insert_example,
        bg_color="#3498DB", hover_color="#2980B9", width=18
    ).pack(side="left", padx=5)

    create_modern_button(
        sql_buttons_frame, "Виконати запит (Enter)", execute_sql,
        bg_color="#27AE60", hover_color="#229954", width=18
    ).pack(side="left", padx=5)

    create_modern_button(
        sql_buttons_frame, "Очистити", clear_sql,
        bg_color="#E74C3C", hover_color="#C0392B", width=15
    ).pack(side="left", padx=5)

  
    exit_frame = tk.Frame(scrollable_frame, bg="#F8F9FA", height=80)
    exit_frame.pack(fill="x", pady=20)
    exit_frame.pack_propagate(False)

    def logout():
        if messagebox.askyesno(
            "Підтвердження",
            "Вийти з облікового запису та повернутися до вікна входу?"
        ):
            operator_window.destroy()
            login_window.show_login_window()

    exit_btn = create_modern_button(
        exit_frame,
        "Вийти з системи (ESC)",
        logout,
        bg_color="#E74C3C",
        hover_color="#C0392B",
        width=25,
        font_size=12
    )
    exit_btn.pack(pady=20)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def bind_mousewheel(event):
        canvas.bind_all("<MouseWheel>", on_mousewheel)

    def unbind_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind('<Enter>', bind_mousewheel)
    canvas.bind('<Leave>', unbind_mousewheel)

    operator_window.mainloop()
