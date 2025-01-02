import tkinter as tk
from tkinter import messagebox
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os


def load_form_config(config_file):
    """
    Загружает конфигурацию формы из JSON-файла.
    """
    with open(config_file, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_xpath(question_text, answer_text):
    """
    Генерирует XPath для выбора ответа на основе текста вопроса и ответа.
    """
    return f"//div[contains(., '{question_text}')]//following-sibling::div//span[contains(text(), '{answer_text}')]"


def fill_form(browser, form_data, runs):
    """
    Заполняет форму на основе предоставленных данных.
    """
    for i in range(runs):
        print(f"\nЗапуск #{i + 1} из {runs}")
        try:
            # Переход по ссылке формы
            browser.get(form_data["form_link"])
            print("Открыта форма:", form_data["form_link"])

            # Заполнение каждого вопроса
            for question in form_data["questions"]:
                question_text = question["text"]
                answer_text = question["answer"]

                # Генерация XPath
                question_xpath = generate_xpath(question_text, answer_text)

                try:
                    # Ожидание появления вопроса
                    question_container_xpath = f"//div[contains(., '{question_text}')]"
                    WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.XPATH, question_container_xpath))
                    )

                    # Ожидание кликабельности ответа
                    answer = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, question_xpath))
                    )

                    # Скроллинг до ответа и клик
                    browser.execute_script("arguments[0].scrollIntoView();", answer)
                    answer.click()
                    print(f"Ответ '{answer_text}' выбран для вопроса '{question_text}'")
                except Exception as e:
                    print(f"Ошибка: не удалось выбрать ответ '{answer_text}' для вопроса '{question_text}': {e}")

            # Нажатие кнопки "Отправить"
            submit_xpath = "//span[@class='NPEfkd RveJvd snByac' and text()='Отправить']"
            try:
                submit_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, submit_xpath))
                )
                submit_button.click()
                print("Форма отправлена!")
            except Exception as e:
                print(f"Ошибка при отправке формы: {e}")

        except Exception as e:
            print(f"Ошибка при заполнении формы: {e}")

        time.sleep(2)  # Пауза между запусками


class FormFillerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Forms Bot")

        # Поле для ввода количества запусков
        self.label_runs = tk.Label(root, text="Введите количество запусков:")
        self.label_runs.pack(pady=5)

        self.entry_runs = tk.Entry(root)
        self.entry_runs.pack(pady=5)

        # Кнопка для запуска
        self.button_run = tk.Button(root, text="Запустить", command=self.run_bot)
        self.button_run.pack(pady=10)

    def run_bot(self):
        """
        Запускает бота для заполнения формы.
        """
        # Фиксированное имя JSON-файла
        config_file = "config.json"

        # Проверка существования файла
        if not os.path.exists(config_file):
            messagebox.showerror("Ошибка", f"Файл '{config_file}' не найден в текущей директории.")
            return

        # Загрузка JSON
        try:
            form_data = load_form_config(config_file)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке JSON-файла: {e}")
            return

        # Проверка ввода количества запусков
        try:
            runs = int(self.entry_runs.get().strip())
            if runs <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное количество запусков (целое положительное число).")
            return

        # Запуск Selenium
        try:
            browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            fill_form(browser, form_data, runs)
            messagebox.showinfo("Успех", "Форма успешно заполнена!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при работе бота: {e}")
        finally:
            browser.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = FormFillerApp(root)
    root.mainloop()
