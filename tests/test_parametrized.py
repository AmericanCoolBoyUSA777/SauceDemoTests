import json
import allure
import pytest
from pages.login_page import LoginPage

def load_test_data():
    with open("test_data.json", encoding="utf-8") as f:
        return json.load(f)

@allure.feature("Data-Driven Testing")
class TestLoginParametrized:

    @pytest.mark.parametrize("user_data", load_test_data())
    def test_login_with_different_users(self, driver, user_data):
        login_page = LoginPage(driver)
        login_page.open_page()

        with allure.step(f"Логин под пользователем {user_data['username']}"):
            login_page.login(user_data["username"], user_data["password"])

        if user_data["expected"] == "success":
            with allure.step("Проверка успешного входа"):
                assert "inventory.html" in driver.current_url
        else:
            with allure.step("Проверка сообщения об ошибке"):
                error_msg = login_page.get_error_message()
                assert "locked out" in error_msg

        # Возврат на страницу логина для следующей итерации
        if "inventory.html" in driver.current_url:
            driver.get("https://www.saucedemo.com/")