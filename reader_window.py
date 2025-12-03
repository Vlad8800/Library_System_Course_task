from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import tkinter as tk
from datetime import date, timedelta
from database import get_db_connection
from utils import get_user_id
import mysql.connector  


def show_help():
    """Показує повідомлення з допомогою про гарячі клавіші."""
    messagebox.showinfo(
        "Допомога (F1)",
        "Основні гарячі клавіші:\n\n"
        "• Enter: Підтвердити дію, зберегти, завершити введення.\n"
        "• Esc: Скасувати дію, закрити поточне вікно.\n"
        "• Tab: Перехід до наступного поля.\n"
        "• Shift+Tab: Повернення до попереднього поля.\n"
        "• F1: Виклик цієї довідки.\n"
        "• F11: Увімкнути/вимкнути повноекранний режим."
    )


def go_to_login(window_to_close):
    """Показує підтвердження, і якщо 'Так' - закриває поточне вікно та відкриває вікно входу."""
    if messagebox.askyesno("Підтвердження виходу", "Ви дійсно хочете вийти та повернутися до вікна входу?"):
        from login_window import show_login_window
        window_to_close.destroy()
        show_login_window()

def fetch_reading_rooms():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT room_id, name FROM ReadingRooms")
    rooms = cursor.fetchall()
    conn.close()
    return rooms


def fetch_user_issued_books(reader_id, show_overdue=False):
    """
    Отримує список виданих книг користувача.
    show_overdue: якщо True, показує тільки прострочені книги.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if show_overdue:
        cursor.execute("""
            SELECT ib.issue_id, ib.book_id, b.title, c.name as category, 
                   ib.issue_date, ib.return_date, ib.reading_place, ib.room_id, ib.librarian_id,
                   DATEDIFF(CURDATE(), ib.return_date) as days_overdue
            FROM IssuedBooks ib
            JOIN Books b ON b.book_id = ib.book_id
            LEFT JOIN Categories c ON b.category_id = c.category_id
            WHERE ib.reader_id = %s 
              AND ib.return_date < CURDATE()
              AND ib.returned = FALSE
            ORDER BY ib.return_date ASC
        """, (reader_id,))
    else:
        cursor.execute("""
            SELECT ib.issue_id, ib.book_id, b.title, c.name as category, 
                   ib.issue_date, ib.return_date, ib.reading_place, ib.room_id, ib.librarian_id,
                   CASE 
                       WHEN ib.return_date < CURDATE() AND ib.returned = FALSE 
                           THEN DATEDIFF(CURDATE(), ib.return_date)
                       ELSE 0
                   END as days_overdue
            FROM IssuedBooks ib
            JOIN Books b ON b.book_id = ib.book_id
            LEFT JOIN Categories c ON b.category_id = c.category_id
            WHERE ib.reader_id = %s
              AND ib.returned = FALSE
            ORDER BY ib.return_date < CURDATE() DESC, ib.issue_date DESC
        """, (reader_id,))

    result = cursor.fetchall()
    conn.close()
    return result


def fetch_librarians_by_room(room_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    if room_id:
        cursor.execute("""
            SELECT librarian_id, name 
            FROM Librarians 
            WHERE reading_room_id = %s
        """, (room_id,))
    else:
        cursor.execute("SELECT librarian_id, name FROM Librarians")

    librarians = cursor.fetchall()
    conn.close()
    return librarians


def fetch_all_librarians():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT librarian_id, name FROM Librarians")
    librarians = cursor.fetchall()
    conn.close()
    return librarians


def fetch_book_reading_place(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT reading_place FROM BookReadingTypes WHERE book_id = %s
    """, (book_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def fetch_reader_books_by_period(reader_id, start_date, end_date):
    """
    Отримує список видань, якими користувався читач протягом вказаного періоду (для історії).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ib.issue_id, ib.book_id, b.title, c.name as category, 
               ib.issue_date, ib.return_date, ib.reading_place,
               rr.name as room_name, l.name as librarian_name,
               CASE 
                   WHEN ib.returned = TRUE THEN 'Повернена'
                   WHEN ib.return_date < CURDATE() THEN 'Просрочена'
                   ELSE 'Активна'
               END as status
        FROM IssuedBooks ib
        JOIN Books b ON b.book_id = ib.book_id
        LEFT JOIN Categories c ON b.category_id = c.category_id
        LEFT JOIN ReadingRooms rr ON ib.room_id = rr.room_id
        LEFT JOIN Librarians l ON ib.librarian_id = l.librarian_id
        WHERE ib.reader_id = %s 
          AND ib.issue_date BETWEEN %s AND %s
        ORDER BY ib.issue_date DESC
    """, (reader_id, start_date, end_date))
    result = cursor.fetchall()
    conn.close()
    return result


def show_user_history_window(reader_id):
    """
    Вікно для перегляду особистої історії читання користувача (read-only).
    """
    history_window = tk.Toplevel()
    history_window.title("Моя історія читання")
    history_window.geometry("900x550")
    history_window.grab_set()

    history_window.bind('<Escape>', lambda e: history_window.destroy())
    history_window.bind('<F1>', lambda e: show_help())

    tk.Label(
        history_window,
        text="Історія ваших видач",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    period_frame = tk.Frame(history_window)
    period_frame.pack(pady=10)

    tk.Label(period_frame, text="Від:").pack(side=tk.LEFT, padx=5)
    start_date_entry = DateEntry(period_frame, date_pattern='yyyy-mm-dd')
    start_date_entry.pack(side=tk.LEFT, padx=5)

    tk.Label(period_frame, text="До:").pack(side=tk.LEFT, padx=5)
    end_date_entry = DateEntry(period_frame, date_pattern='yyyy-mm-dd')
    end_date_entry.pack(side=tk.LEFT, padx=5)

    results_frame = tk.Frame(history_window)
    results_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def search_my_books():
        start_date = start_date_entry.get_date()
        end_date = end_date_entry.get_date()

        if start_date > end_date:
            messagebox.showerror("Помилка", "Початкова дата не може бути пізніше кінцевої")
            return

        books = fetch_reader_books_by_period(reader_id, start_date, end_date)

        for widget in results_frame.winfo_children():
            widget.destroy()

        if not books:
            tk.Label(
                results_frame,
                text="За вказаний період книги не видавались",
                font=("Arial", 12),
                fg="gray"
            ).pack(pady=50)
            return

        tk.Label(
            results_frame,
            text=f"Знайдено записів: {len(books)}",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        container = tk.Frame(results_frame)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", on_mousewheel)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        header = tk.Frame(scrollable_frame, bg="#dddddd")
        header.pack(fill=tk.X, pady=5)

        tk.Label(header, text="Книга", font=("Arial", 11, "bold"), width=35, anchor="w", bg="#dddddd").pack(side=tk.LEFT)
        tk.Label(header, text="Категорія", font=("Arial", 11, "bold"), width=15, anchor="w", bg="#dddddd").pack(side=tk.LEFT)
        tk.Label(header, text="Взято", font=("Arial", 11, "bold"), width=12, anchor="w", bg="#dddddd").pack(side=tk.LEFT)
        tk.Label(header, text="Повернути до", font=("Arial", 11, "bold"), width=15, anchor="w", bg="#dddddd").pack(side=tk.LEFT)
        tk.Label(header, text="Статус", font=("Arial", 11, "bold"), width=15, anchor="w", bg="#dddddd").pack(side=tk.LEFT)

        for issue_id, book_id, title, category, issue_date, return_date, place, room_name, librarian_name, status in books:
            row_color = "#ffe6e6" if status == "Просрочена" else "#ffffff"

            row = tk.Frame(scrollable_frame, bg=row_color)
            row.pack(fill=tk.X, pady=1)

            tk.Label(row, text=title[:40], width=35, anchor="w", bg=row_color, font=("Arial", 10)).pack(side=tk.LEFT)
            tk.Label(row, text=category or "—", width=15, anchor="w", bg=row_color, font=("Arial", 10)).pack(side=tk.LEFT)
            tk.Label(row, text=str(issue_date), width=12, anchor="w", bg=row_color, font=("Arial", 10)).pack(side=tk.LEFT)
            tk.Label(row, text=str(return_date), width=15, anchor="w", bg=row_color, font=("Arial", 10)).pack(side=tk.LEFT)

            status_color = (
                "red" if status == "Просрочена"
                else "green" if status == "Активна"
                else "gray"
            )
            tk.Label(
                row,
                text=status,
                width=15,
                anchor="w",
                bg=row_color,
                font=("Arial", 10),
                fg=status_color
            ).pack(side=tk.LEFT)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    history_window.bind('<Return>', lambda e: search_my_books())

    search_btn = tk.Button(
        period_frame,
        text="Показати",
        command=search_my_books,
        bg="blue",
        fg="white"
    )
    search_btn.pack(side=tk.LEFT, padx=10)
    search_btn.bind('<Return>', lambda e: search_my_books())


def show_returned_books_inline(reader_id, parent_frame, show_overdue_only=False):
    """
    Показує книги користувача з можливістю фільтрації прострочених.
    READ-ONLY: без можливості повернути книгу.
    """
    for widget in parent_frame.winfo_children():
        widget.destroy()

    if show_overdue_only:
        tk.Label(
            parent_frame,
            text="\nВаші прострочені книги:",
            font=("Arial", 13, "bold"),
            anchor="w",
            bg="#f0f0f0",
            fg="red"
        ).pack(anchor="w", padx=10, pady=(20, 5))
    else:
        tk.Label(
            parent_frame,
            text="\nВаші активні книги:",
            font=("Arial", 13, "bold"),
            anchor="w",
            bg="#f0f0f0"
        ).pack(anchor="w", padx=10, pady=(20, 5))

    button_frame = tk.Frame(parent_frame, bg="#f0f0f0")
    button_frame.pack(anchor="w", padx=10, pady=5)

    all_btn = tk.Button(
        button_frame,
        text="Всі активні",
        command=lambda: show_returned_books_inline(reader_id, parent_frame, False),
        bg="blue",
        fg="white"
    )
    all_btn.pack(side=tk.LEFT, padx=5)
    all_btn.bind('<Return>', lambda e: show_returned_books_inline(reader_id, parent_frame, False))

    overdue_btn = tk.Button(
        button_frame,
        text="Тільки прострочені",
        command=lambda: show_returned_books_inline(reader_id, parent_frame, True),
        bg="red",
        fg="white"
    )
    overdue_btn.pack(side=tk.LEFT, padx=5)
    overdue_btn.bind('<Return>', lambda e: show_returned_books_inline(reader_id, parent_frame, True))

    books = fetch_user_issued_books(reader_id, show_overdue_only)

    if not books:
        no_books_msg = "Немає прострочених книг" if show_overdue_only else "Немає активних книг"
        tk.Label(
            parent_frame,
            text=no_books_msg,
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="gray"
        ).pack(anchor="w", padx=10, pady=10)
        return

    container = tk.Frame(parent_frame, bg="#f0f0f0")
    container.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(container, bg="#f0f0f0")
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind("<MouseWheel>", on_mousewheel)
    scrollable_frame.bind("<MouseWheel>", on_mousewheel)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    header = tk.Frame(scrollable_frame, bg="#dddddd")
    header.pack(fill=tk.X, pady=2)

    tk.Label(header, text="Назва книги", font=("Arial", 11, "bold"), width=35, anchor="w", bg="#dddddd").pack(side=tk.LEFT)
    tk.Label(header, text="Категорія", font=("Arial", 11, "bold"), width=20, anchor="w", bg="#dddddd").pack(side=tk.LEFT)
    tk.Label(header, text="Дата видачі", font=("Arial", 11, "bold"), width=15, anchor="w", bg="#dddddd").pack(side=tk.LEFT)
    tk.Label(header, text="Дата повернення", font=("Arial", 11, "bold"), width=18, anchor="w", bg="#dddddd").pack(side=tk.LEFT)
    tk.Label(header, text="Місце", font=("Arial", 11, "bold"), width=25, anchor="w", bg="#dddddd").pack(side=tk.LEFT)
    tk.Label(header, text="Статус", font=("Arial", 11, "bold"), width=20, anchor="w", bg="#dddddd").pack(side=tk.LEFT)

    for issue_id, book_id, title, category, issue_date, return_date, place, room_id, librarian_id, days_overdue in books:
        is_overdue = days_overdue > 0

        row_color = "#ffe6e6" if is_overdue else "#ffffff"

        row = tk.Frame(scrollable_frame, bg=row_color)
        row.pack(fill=tk.X, pady=2)

        tk.Label(row, text=title[:40], width=35, anchor="w", bg=row_color, font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Label(row, text=category or "—", width=20, anchor="w", bg=row_color, font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Label(row, text=str(issue_date), width=15, anchor="w", bg=row_color, font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Label(row, text=str(return_date), width=18, anchor="w", bg=row_color, font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Label(row, text=place, width=25, anchor="w", bg=row_color, font=("Arial", 10)).pack(side=tk.LEFT)

        if is_overdue:
            status_text = f"Просрочена ({days_overdue} дн.)"
            status_color = "red"
        else:
            status_text = "Активна"
            status_color = "green"

        tk.Label(
            row,
            text=status_text,
            width=20,
            anchor="w",
            bg=row_color,
            font=("Arial", 10),
            fg=status_color
        ).pack(side=tk.LEFT)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


def show_books(reader_id, category=None, title_search=None, room_filter=None, get_ids=None):
    """
    Показ доступних книг у read-only режимі:
    - без кнопок видачі, тільки інформація;
    - фільтр за читальним залом, категорією, назвою.
    """
    global available_books_frame
    for widget in available_books_frame.winfo_children():
        widget.destroy()

    container = tk.Frame(available_books_frame, bg="#f0f0f0")
    container.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(container, bg="#f0f0f0")
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind("<MouseWheel>", on_mousewheel)
    scrollable_frame.bind("<MouseWheel>", on_mousewheel)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    header = tk.Frame(scrollable_frame, bg="#f5f5f5")
    header.pack(fill=tk.X, pady=5)

    tk.Label(header, text="Назва книги", font=("Arial", 12, "bold"), width=50, anchor="w", bg="#f5f5f5").pack(side=tk.LEFT)
    tk.Label(header, text="Категорія", font=("Arial", 12, "bold"), width=20, anchor="w", bg="#f5f5f5").pack(side=tk.LEFT)
    tk.Label(header, text="У читальному залі", font=("Arial", 12, "bold"), width=20, anchor="w", bg="#f5f5f5").pack(side=tk.LEFT)
    tk.Label(header, text="Доступна кількість", font=("Arial", 12, "bold"), width=20, anchor="w", bg="#f5f5f5").pack(side=tk.LEFT)

    tk.Frame(scrollable_frame, height=2, bg="gray").pack(fill=tk.X, pady=2)

    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT 
        b.book_id, 
        b.title, 
        COALESCE(c.name, 'Без категорії') AS category_name,
        b.access_type,
        IF(EXISTS (
            SELECT 1 FROM Placements p WHERE p.book_id = b.book_id
        ), 'Так', 'Ні') AS is_in_room,
        EXISTS (
            SELECT 1 FROM IssuedBooks ib
            WHERE ib.book_id = b.book_id
              AND ib.reader_id = %s
              AND ib.return_date >= CURDATE()
              AND ib.returned = FALSE
        ) AS is_issued_by_user,
        b.quantity - (
            SELECT COUNT(*) FROM IssuedBooks ib2
            WHERE ib2.book_id = b.book_id
              AND ib2.return_date >= CURDATE()
              AND ib2.returned = FALSE
        ) AS available_quantity
    FROM Books b
    LEFT JOIN Categories c ON b.category_id = c.category_id
    """
    conditions = []
    params = [reader_id]

    if room_filter:
        conditions.append("EXISTS (SELECT 1 FROM Placements p WHERE p.book_id = b.book_id AND p.room_id = %s)")
        params.append(room_filter)
    if category:
        conditions.append("c.name LIKE %s")
        params.append(f"%{category}%")
    if title_search:
        conditions.append("b.title LIKE %s")
        params.append(f"%{title_search}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY is_issued_by_user ASC, b.title"

    cursor.execute(query, params)
    books = cursor.fetchall()
    conn.close()

    if not books:
        tk.Label(
            scrollable_frame,
            text="За заданими фільтрами книги не знайдено",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="gray"
        ).pack(pady=15, anchor="w", padx=10)
    else:
        for book_id, title, category_name, access_type, is_in_room, is_issued_by_user, available_quantity in books:
            row = tk.Frame(scrollable_frame, bg="#e6e6e6" if is_issued_by_user else "#ffffff")
            row.pack(fill=tk.X, pady=3)

            tk.Label(row, text=title[:60], font=("Arial", 11), width=50, anchor="w", bg=row.cget("bg")).pack(side=tk.LEFT)
            tk.Label(row, text=category_name, font=("Arial", 11), width=25, anchor="w", bg=row.cget("bg")).pack(side=tk.LEFT)
            tk.Label(row, text=is_in_room, font=("Arial", 11), width=20, anchor="w", bg=row.cget("bg")).pack(side=tk.LEFT)
            tk.Label(row, text=str(available_quantity), font=("Arial", 11), width=20, anchor="w", bg=row.cget("bg")).pack(side=tk.LEFT)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


def show_reader_window(reader_id):
    """
    Головне вікно читача у read-only режимі:
    - перегляд доступних книг;
    - перегляд своїх активних/прострочених книг;
    - НІЯКИХ ФІЛЬТРІВ;
    - тільки кнопки: Історія читання + Вихід;
    - гарячі клавіші F1/F11/Esc.
    """
    global available_books_frame, return_books_frame

    root = tk.Tk()
    root.title("Бібліотечна система - Читач")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.state('zoomed')

    root.configure(bg="#f0f0f0")

    def toggle_fullscreen(event=None):
        root.attributes('-fullscreen', not root.attributes('-fullscreen'))

    root.bind('<Escape>', lambda e: go_to_login(root))
    root.bind('<F1>', lambda e: show_help())
    root.bind('<F11>', toggle_fullscreen)

    main_container = tk.Frame(root, bg="#f0f0f0")
    main_container.pack(fill="both", expand=True, padx=20, pady=15)

    top = tk.Frame(main_container, bg="#f0f0f0")
    top.pack(fill=tk.X, pady=(0, 15))

    exit_btn = tk.Button(
        top,
        text="Вихід",
        command=lambda: go_to_login(root),
        bg="red",
        fg="white",
        font=("Arial", 10)
    )
    exit_btn.pack(side=tk.RIGHT, padx=5)

    history_btn = tk.Button(
        top,
        text="Історія читання",
        command=lambda: show_user_history_window(reader_id),
        bg="darkgreen",
        fg="white",
        font=("Arial", 10)
    )
    history_btn.pack(side=tk.RIGHT, padx=5)

    content_frame = tk.Frame(main_container, bg="#f0f0f0")
    content_frame.pack(fill="both", expand=True)

    available_section = tk.LabelFrame(
        content_frame,
        text="Доступні книги",
        font=("Arial", 14, "bold"),
        bg="#f0f0f0",
        padx=15,
        pady=10,
        relief=tk.RAISED,
        bd=2
    )
    available_section.pack(fill="both", expand=True, pady=(0, 15))

    available_books_frame = tk.Frame(available_section, bg="#f0f0f0", height=450)
    available_books_frame.pack(fill="both", expand=True)
    available_books_frame.pack_propagate(False)

    returned_section = tk.LabelFrame(
        content_frame,
        text="Ваші активні книги",
        font=("Arial", 14, "bold"),
        bg="#f0f0f0",
        padx=15,
        pady=10,
        relief=tk.RAISED,
        bd=2
    )
    returned_section.pack(fill="both", expand=True)

    return_books_frame = tk.Frame(returned_section, bg="#f0f0f0", height=350)
    return_books_frame.pack(fill="both", expand=True)
    return_books_frame.pack_propagate(False)

    
    def refresh_books():
        show_books(reader_id)

    refresh_books()
    show_returned_books_inline(reader_id, return_books_frame)

    info_label = tk.Label(
        main_container,
        text="F11 - повноекранний режим | Esc - вихід з програми | F1 - допомога",
        font=("Arial", 10),
        bg="#f0f0f0",
        fg="gray"
    )
    info_label.pack(side=tk.BOTTOM, pady=10)

    root.mainloop()
