import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []

        # Создаем поля ввода
        self.create_input_fields()

        # Создаем кнопки
        self.create_buttons()

        # Создаем таблицу
        self.create_treeview()

        # Создаем фильтры
        self.create_filters()

        # Загружаем данные при запуске (опционально)
        self.load_data()

    def create_input_fields(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Название книги").grid(row=0, column=0)
        self.title_entry = tk.Entry(frame)
        self.title_entry.grid(row=0, column=1)

        tk.Label(frame, text="Автор").grid(row=0, column=2)
        self.author_entry = tk.Entry(frame)
        self.author_entry.grid(row=0, column=3)

        tk.Label(frame, text="Жанр").grid(row=1, column=0)
        self.genre_entry = tk.Entry(frame)
        self.genre_entry.grid(row=1, column=1)

        tk.Label(frame, text="Количество страниц").grid(row=1, column=2)
        self.pages_entry = tk.Entry(frame)
        self.pages_entry.grid(row=1, column=3)

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()

        add_btn = tk.Button(frame, text="Добавить книгу", command=self.add_book)
        add_btn.pack(side=tk.LEFT, padx=5)

        save_btn = tk.Button(frame, text="Сохранить в JSON", command=self.save_to_json)
        save_btn.pack(side=tk.LEFT, padx=5)

        load_btn = tk.Button(frame, text="Загрузить из JSON", command=self.load_from_json)
        load_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = tk.Button(frame, text="Очистить фильтры", command=self.reset_filters)
        reset_btn.pack(side=tk.LEFT, padx=5)

    def create_treeview(self):
        columns = ("Название", "Автор", "Жанр", "Страницы")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(pady=10)

    def create_filters(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Фильтр по жанру").grid(row=0, column=0)
        self.genre_filter = ttk.Combobox(frame, values=["Все"])
        self.genre_filter.current(0)
        self.genre_filter.grid(row=0, column=1)
        self.genre_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())

        tk.Label(frame, text="Страницы больше").grid(row=0, column=2, padx=5)
        self.pages_filter = tk.Entry(frame)
        self.pages_filter.grid(row=0, column=3)
        self.pages_filter.bind("<KeyRelease>", lambda e: self.apply_filters())

        self.update_genre_filter()

    def update_genre_filter(self):
        genres = set(book['genre'] for book in self.books)
        genre_list = ["Все"] + sorted(genres)
        self.genre_filter['values'] = genre_list
        self.genre_filter.current(0)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        # Проверка корректности ввода
        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return
        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }
        self.books.append(book)
        self.refresh_treeview()
        self.update_genre_filter()
        self.clear_input_fields()

    def clear_input_fields(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    def refresh_treeview(self, filtered_books=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        display_books = filtered_books if filtered_books is not None else self.books
        for book in display_books:
            self.tree.insert("", tk.END, values=(book['title'], book['author'], book['genre'], book['pages']))

    def apply_filters(self):
        genre_filter = self.genre_filter.get()
        pages_filter = self.pages_filter.get()

        filtered_books = self.books
        if genre_filter != "Все":
            filtered_books = [b for b in filtered_books if b['genre'] == genre_filter]
        if pages_filter.isdigit():
            num = int(pages_filter)
            filtered_books = [b for b in filtered_books if b['pages'] > num]
        self.refresh_treeview(filtered_books)

    def save_to_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Сохранено", "Данные успешно сохранены")

    def load_from_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                self.books = json.load(f)
            self.refresh_treeview()
            self.update_genre_filter()

    def load_data(self):
        # Можно реализовать автоматическую загрузку при старте
        pass

    def reset_filters(self):
        self.genre_filter.current(0)
        self.pages_filter.delete(0, tk.END)
        self.refresh_treeview()

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
