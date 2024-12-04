import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


class AnimalParser:

    def __init__(self, url: str, result_dict: dict[str, int]) -> None:
        self.url = url
        self.result_dict = result_dict
        self.driver: WebDriver | None = None

    def create_driver(self) -> None:
        """Создает экземпляр драйвера Selenium."""
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.url)

    def parse(self) -> None:
        """Парсит список животных на текущей странице."""
        if not self.driver:
            raise ValueError("Driver is not initialized.")

        animals = self.driver.find_elements(By.CSS_SELECTOR, "#mw-pages > div.mw-content-ltr > div > div > ul > li")
        for animal in animals:
            name: str = animal.text
            first_letter: str = name[0]
            if first_letter in self.result_dict:
                self.result_dict[first_letter] += 1

    def change_page(self) -> bool:
        """Переходит на следующую страницу, если кнопка доступна."""
        if not self.driver:
            raise ValueError("Driver is not initialized.")

        try:
            next_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="mw-pages"]/a[text()="Следующая страница"]'))
            )
            next_button.click()
            return True
        except Exception as e:
            print(f"Ошибка при переходе на следующую страницу: {e}")
            return False

    def save_to_csv(self, filename: str = "beasts.csv") -> None:
        """Сохраняет словарь result_dict в файл CSV."""
        with open(filename, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            for key, value in self.result_dict.items():
                writer.writerow([key, value])

    def run(self, max_pages: int = 110) -> None:
        """Основной метод для запуска парсинга."""
        try:
            self.create_driver()
            for _ in range(max_pages):
                self.parse()
                if not self.change_page():
                    break
            self.save_to_csv()
            print("Результаты сохранены в beasts.csv")
        finally:
            if self.driver:
                self.driver.quit()


if __name__ == "__main__":
    result_dict: dict[str, int] = {
        'А': 0, 'Б': 0, 'В': 0, 'Г': 0, 'Д': 0, 'Е': 0, 'Ё': 0, 'Ж': 0, 'З': 0, 'И': 0, 'Й': 0, 'К': 0, 'Л': 0,
        'М': 0, 'Н': 0, 'О': 0, 'П': 0, 'Р': 0, 'С': 0, 'Т': 0, 'У': 0, 'Ф': 0, 'Х': 0, 'Ц': 0, 'Ч': 0, 'Ш': 0,
        'Щ': 0, 'Ъ': 0, 'Ы': 0, 'Ь': 0, 'Э': 0, 'Ю': 0, 'Я': 0
    }

    url: str = "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту"
    parser = AnimalParser(url, result_dict)
    parser.run()
