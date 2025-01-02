import tkinter as tk
from tkinter import messagebox
import json
import subprocess  # Для запуска внешних программ

class FormConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Создание JSON для Google Forms")

        # Поле для ввода ссылки на форму
        self.label_form_link = tk.Label(root, text="Введите ссылку на Google Form:")
        self.label_form_link.pack(pady=5)

        self.entry_form_link = tk.Entry(root, width=50)
        self.entry_form_link.pack(pady=5)

        # Количество вопросов
        self.label_num_questions = tk.Label(root, text="Введите количество вопросов:")
        self.label_num_questions.pack(pady=5)

        self.entry_num_questions = tk.Entry(root)
        self.entry_num_questions.pack(pady=5)

        self.button_set_questions = tk.Button(root, text="Создать поля для вопросов", command=self.create_question_fields)
        self.button_set_questions.pack(pady=5)

        # Контейнер для полей вопросов и ответов
        self.questions_frame = tk.Frame(root)
        self.questions_frame.pack(pady=10)

        # Кнопка для сохранения
        self.button_save = tk.Button(root, text="Сохранить в JSON и запустить forms.py", command=self.save_to_json, state=tk.DISABLED)
        self.button_save.pack(pady=10)

        # Список для хранения полей ввода
        self.question_fields = []

    def create_question_fields(self):
        """
        Создаёт поля для ввода вопросов и ответов на основе указанного количества.
        """
        try:
            num_questions = int(self.entry_num_questions.get())
            if num_questions <= 0:
                raise ValueError("Количество вопросов должно быть положительным числом.")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное количество вопросов (положительное число).")
            return

        # Очищаем предыдущие поля
        for widget in self.questions_frame.winfo_children():
            widget.destroy()
        self.question_fields = []

        # Создаём новые поля
        for i in range(num_questions):
            question_label = tk.Label(self.questions_frame, text=f"Вопрос {i + 1}:")
            question_label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)

            question_entry = tk.Entry(self.questions_frame, width=50)
            question_entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)

            answer_label = tk.Label(self.questions_frame, text=f"Ответ {i + 1}:")
            answer_label.grid(row=i, column=2, padx=5, pady=5, sticky=tk.W)

            answer_entry = tk.Entry(self.questions_frame, width=50)
            answer_entry.grid(row=i, column=3, padx=5, pady=5, sticky=tk.W)

            self.question_fields.append((question_entry, answer_entry))

        self.button_save.config(state=tk.NORMAL)

    def save_to_json(self):
        """
        Сохраняет введённые вопросы, ответы и ссылку на форму в JSON-файл.
        """
        form_link = self.entry_form_link.get().strip()
        if not form_link:
            messagebox.showerror("Ошибка", "Введите ссылку на Google Form.")
            return

        questions = []
        for i, (question_entry, answer_entry) in enumerate(self.question_fields):
            question_text = question_entry.get().strip()
            answer_text = answer_entry.get().strip()

            if not question_text or not answer_text:
                messagebox.showerror("Ошибка", f"Пожалуйста, заполните вопрос и ответ для Вопроса {i + 1}.")
                return

            questions.append({"text": question_text, "answer": answer_text})

        # Сохраняем в JSON
        json_data = {
            "form_link": form_link,
            "questions": questions
        }

        try:
            with open("config.json", "w", encoding="utf-8") as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Данные успешно сохранены в 'config.json'.")

            # Запуск forms.py
            self.run_forms_py()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить JSON-файл: {e}")

    def run_forms_py(self):
        """
        Запускает скрипт forms.py после сохранения JSON.
        """
        try:
            subprocess.run(["python", "forms.py"], check=True)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Не удалось найти файл 'forms.py'. Убедитесь, что он находится в той же папке.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при запуске 'forms.py': {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FormConfigApp(root)
    root.mainloop()
