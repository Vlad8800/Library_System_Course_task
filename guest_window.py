import tkinter as tk
from tkinter import messagebox
from database import get_db_connection
from register_window import show_register_window

def fetch_all_books():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            b.book_id, 
            b.title,
            COALESCE(c.name, 'Без категорії'),
            b.quantity
        FROM Books b
        LEFT JOIN Categories c ON b.category_id = c.category_id
        ORDER BY b.title
    """)

    books = cursor.fetchall()
    conn.close()
    return books

def show_guest_window():
    guest = tk.Toplevel()

    # 🌟 ПОВНОЕКРАННИЙ РЕЖИМ
    guest.state('zoomed')
    guest.configure(bg="#F8F9FA")
    guest.title("Гостьовий режим")

    guest.lift()
    guest.focus_force()

    tk.Label(
        guest,
        text="Гостьовий режим",
        font=("Arial", 26, "bold"),
        bg="#F8F9FA"
    ).pack(pady=15)

    tk.Label(
        guest,
        text="Як гість, ви можете лише переглядати книги.\n"
             "Щоб отримати повний доступ — зареєструйтесь.",
        font=("Arial", 13),
        bg="#F8F9FA",
        fg="gray"
    ).pack(pady=5)

    wrapper = tk.Frame(guest, bg="#F8F9FA")
    wrapper.pack(fill="both", expand=True, padx=20, pady=10)

    canvas = tk.Canvas(wrapper, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="white")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    header = tk.Frame(scroll_frame, bg="#EAEAEA")
    header.pack(fill=tk.X)

    tk.Label(header, text="Назва книги", font=("Arial", 14, "bold"), bg="#EAEAEA",
             width=60, anchor="w").pack(side=tk.LEFT, padx=10)
    tk.Label(header, text="Категорія", font=("Arial", 14, "bold"), bg="#EAEAEA",
             width=30, anchor="w").pack(side=tk.LEFT, padx=10)
    tk.Label(header, text="Кількість", font=("Arial", 14, "bold"), bg="#EAEAEA",
             width=15, anchor="w").pack(side=tk.LEFT, padx=10)

    tk.Frame(scroll_frame, height=3, bg="gray").pack(fill=tk.X, pady=3)

    books = fetch_all_books()

    for book_id, title, category, qty in books:
        row = tk.Frame(scroll_frame, bg="white")
        row.pack(fill=tk.X, pady=2)

        tk.Label(row, text=title[:60], font=("Arial", 13), width=60, bg="white",
                 anchor="w").pack(side=tk.LEFT, padx=10)
        tk.Label(row, text=category, font=("Arial", 13), width=30, bg="white",
                 anchor="w").pack(side=tk.LEFT, padx=10)
        tk.Label(row, text=str(qty), font=("Arial", 13), width=15, bg="white",
                 anchor="w").pack(side=tk.LEFT, padx=10)

    btn_frame = tk.Frame(guest, bg="#F8F9FA")
    btn_frame.pack(pady=15)

    def go_register():
        if messagebox.askyesno(
                "Підтвердження",
                "Щоб отримати повний доступ потрібно зареєструватися.\nПерейти до реєстрації?"
        ):
            guest.destroy()
            show_register_window()

    tk.Button(
        btn_frame,
        text="📨 Подати запит на підтвердження (Перейти до реєстрації)",
        font=("Arial", 13, "bold"),
        bg="#0d6efd",
        fg="white",
        padx=20,
        pady=8,
        command=go_register
    ).pack(pady=5)

   
    def exit_guest():
        if messagebox.askyesno("Вихід", "Вийти до вікна входу?"):
            guest.destroy()
            from login_window import show_login_window
            show_login_window()

    tk.Button(
        btn_frame,
        text="Вийти",
        font=("Arial", 13),
        bg="#dc3545",
        fg="white",
        padx=20,
        pady=8,
        command=exit_guest
    ).pack(pady=5)
