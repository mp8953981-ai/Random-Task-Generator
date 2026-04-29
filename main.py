import json
import random
import os
from tkinter import *
from tkinter import messagebox, ttk

# ------------------------ Класс приложения ------------------------
class TaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Предопределённые задачи
        self.default_tasks = [
            {"text": "Прочитать статью", "type": "учеба"},
            {"text": "Сделать зарядку", "type": "спорт"},
            {"text": "Написать отчёт", "type": "работа"},
            {"text": "Изучить новую библиотеку Python", "type": "учеба"},
            {"text": "Пробежка 3 км", "type": "спорт"},
            {"text": "Позвонить клиенту", "type": "работа"},
            {"text": "Посмотреть вебинар", "type": "учеба"},
            {"text": "Йога 15 минут", "type": "спорт"},
            {"text": "Сделать бэкап проектов", "type": "работа"}
        ]

        # Загрузка истории из файла
        self.history_file = "tasks.json"
        self.history = self.load_history()

        # Текущая задача
        self.current_task = None

        # Фильтр
        self.current_filter = "все"

        # Создание интерфейса
        self.create_widgets()

        # Обновление списка истории
        self.update_history_list()

    def create_widgets(self):
        # Рамка для генерации
        frame_gen = LabelFrame(self.root, text="Генератор задач", padx=10, pady=10)
        frame_gen.pack(fill="x", padx=10, pady=5)

        self.task_label = Label(frame_gen, text="Нажмите кнопку", font=("Arial", 14), wraplength=500)
        self.task_label.pack(pady=10)

        self.generate_btn = Button(frame_gen, text="Сгенерировать задачу", command=self.generate_task, bg="lightblue")
        self.generate_btn.pack(pady=5)

        # Рамка для добавления новой задачи
        frame_add = LabelFrame(self.root, text="Добавить новую задачу", padx=10, pady=10)
        frame_add.pack(fill="x", padx=10, pady=5)

        Label(frame_add, text="Описание:").grid(row=0, column=0, sticky="w")
        self.new_task_entry = Entry(frame_add, width=40)
        self.new_task_entry.grid(row=0, column=1, padx=5)

        Label(frame_add, text="Тип:").grid(row=1, column=0, sticky="w")
        self.type_var = StringVar(value="учеба")
        type_menu = ttk.Combobox(frame_add, textvariable=self.type_var, values=["учеба", "спорт", "работа"], state="readonly")
        type_menu.grid(row=1, column=1, padx=5, sticky="w")

        self.add_btn = Button(frame_add, text="Добавить задачу", command=self.add_task)
        self.add_btn.grid(row=2, column=0, columnspan=2, pady=5)

        # Рамка для фильтрации
        frame_filter = LabelFrame(self.root, text="Фильтр по типу", padx=10, pady=10)
        frame_filter.pack(fill="x", padx=10, pady=5)

        self.filter_var = StringVar(value="все")
        filters = [("Все", "все"), ("Учеба", "учеба"), ("Спорт", "спорт"), ("Работа", "работа")]
        for i, (text, val) in enumerate(filters):
            Radiobutton(frame_filter, text=text, variable=self.filter_var, value=val, command=self.apply_filter).grid(row=0, column=i, padx=10)

        # Рамка истории
        frame_history = LabelFrame(self.root, text="История задач", padx=10, pady=10)
        frame_history.pack(fill="both", expand=True, padx=10, pady=5)

        self.history_listbox = Listbox(frame_history, height=10)
        self.history_listbox.pack(fill="both", expand=True)

        scrollbar = Scrollbar(self.history_listbox)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_listbox.yview)

    # ---------------------- Логика ----------------------
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def get_all_tasks(self):
        # Объединяем предопределённые и добавленные пользователем задачи из истории (уникальные)
        custom_tasks = [{"text": h["text"], "type": h["type"]} for h in self.history if h["type"] != "custom"]
        # Добавляем уникальные пользовательские задачи (если их нет в default)
        existing_texts = set(t["text"] for t in self.default_tasks)
        for ct in custom_tasks:
            if ct["text"] not in existing_texts:
                self.default_tasks.append(ct)
                existing_texts.add(ct["text"])
        return self.default_tasks

    def generate_task(self):
        all_tasks = self.get_all_tasks()
        if not all_tasks:
            messagebox.showwarning("Нет задач", "Сначала добавьте хотя бы одну задачу")
            return

        # Фильтрация
        if self.current_filter != "все":
            filtered = [t for t in all_tasks if t["type"] == self.current_filter]
        else:
            filtered = all_tasks

        if not filtered:
            messagebox.showinfo("Нет задач", f"Нет задач типа '{self.current_filter}'. Измените фильтр.")
            return

        self.current_task = random.choice(filtered)
        self.task_label.config(text=f"📌 {self.current_task['text']} (тип: {self.current_task['type']})")

        # Добавляем в историю
        self.history.append({
            "text": self.current_task["text"],
            "type": self.current_task["type"],
            "timestamp": "сейчас"  # можно добавить datetime, но для простоты так
        })
        self.save_history()
        self.update_history_list()

    def add_task(self):
        task_text = self.new_task_entry.get().strip()
        task_type = self.type_var.get()

        if not task_text:
            messagebox.showerror("Ошибка", "Описание задачи не может быть пустым")
            return

        # Добавляем в список задач
        self.default_tasks.append({"text": task_text, "type": task_type})
        # Также добавим в историю как факт добавления (по желанию)
        self.history.append({
            "text": f"[Добавлено вручную] {task_text}",
            "type": task_type,
            "timestamp": "сейчас"
        })
        self.save_history()
        self.update_history_list()
        self.new_task_entry.delete(0, END)
        messagebox.showinfo("Успех", f"Задача '{task_text}' добавлена")

    def apply_filter(self):
        self.current_filter = self.filter_var.get()
        self.generate_task()  # Можно сразу сгенерировать новую с фильтром

    def update_history_list(self):
        self.history_listbox.delete(0, END)
        # Применяем фильтр к истории отображения
        filtered_history = [h for h in self.history if self.current_filter == "все" or h["type"] == self.current_filter]
        for item in filtered_history:
            self.history_listbox.insert(END, f"{item['text']} [{item['type']}]")

# ------------------------ Запуск ------------------------
if __name__ == "__main__":
    root = Tk()
    app = TaskGenerator(root)
    root.mainloop()
