import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.chrome.webdriver import WebDriver
from solution import AnimalParser


class TestAnimalParser(unittest.TestCase):
    def setUp(self) -> None:
        """Настройка перед каждым тестом."""
        self.url = "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту"
        self.result_dict = {chr(letter): 0 for letter in range(ord('А'), ord('Я') + 1)}
        self.parser = AnimalParser(self.url, self.result_dict)

    @patch("selenium.webdriver.Chrome")
    def test_create_driver(self, mock_chrome: MagicMock) -> None:
        """Тест метода create_driver."""
        mock_driver = MagicMock(spec=WebDriver)
        mock_chrome.return_value = mock_driver

        self.parser.create_driver()
        mock_chrome.assert_called_once()
        mock_driver.get.assert_called_once_with(self.url)

    def test_parse(self) -> None:
        """Тест метода parse."""
        mock_driver = MagicMock(spec=WebDriver)
        mock_driver.find_elements.return_value = [
            MagicMock(text="Антилопа"),
            MagicMock(text="Белка"),
            MagicMock(text="Волк")
        ]
        self.parser.driver = mock_driver

        self.parser.parse()
        self.assertEqual(self.parser.result_dict["А"], 1)
        self.assertEqual(self.parser.result_dict["Б"], 1)
        self.assertEqual(self.parser.result_dict["В"], 1)

    def test_change_page_success(self) -> None:
        """Тест успешного перехода на следующую страницу."""
        mock_driver = MagicMock(spec=WebDriver)
        self.parser.driver = mock_driver
        mock_button = MagicMock()
        mock_driver.find_element.return_value = mock_button

        with patch("selenium.webdriver.support.ui.WebDriverWait.until", return_value=mock_button):
            result = self.parser.change_page()
            self.assertTrue(result)
            mock_button.click.assert_called_once()

    def test_change_page_failure(self) -> None:
        """Тест неудачного перехода на следующую страницу."""
        mock_driver = MagicMock(spec=WebDriver)
        self.parser.driver = mock_driver

        with patch("selenium.webdriver.support.ui.WebDriverWait.until", side_effect=Exception("No button")):
            result = self.parser.change_page()
            self.assertFalse(result)

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("csv.writer")
    def test_save_to_csv(self, mock_csv_writer: MagicMock, mock_open: MagicMock) -> None:
        """Тест сохранения словаря в CSV."""
        self.parser.result_dict = {"А": 10, "Б": 5, "В": 3}

        self.parser.save_to_csv("test.csv")
        mock_open.assert_called_once_with("test.csv", mode="w", encoding="utf-8", newline="")
        mock_csv_writer.assert_called_once()
        mock_csv_writer.return_value.writerow.assert_any_call(["А", 10])
        mock_csv_writer.return_value.writerow.assert_any_call(["Б", 5])
        mock_csv_writer.return_value.writerow.assert_any_call(["В", 3])


if __name__ == "__main__":
    unittest.main()
