from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import re
from art import tprint


class FoodSoulOrder:
    service = Service(executable_path='chromedriver_win32/chromedriver.exe')
    options = Options()

    # headless режим не работает, т.к. приходится вручную вводить капчу.
    # options.add_argument('--headless=new')

    # Инициализация объекта класса FoodSoulOrder.
    def __init__(self):
        self.number = self.number_and_code_validation('phone_number')
        self.code = None
        self.driver = webdriver.Chrome(options=FoodSoulOrder.options, service=FoodSoulOrder.service)

    # Метод для ввода номера телефона и кода из смс и проверки правильности ввода.
    @staticmethod
    def number_and_code_validation(input_type):
        templates = {
            'phone_number': r'\d{10}',
            'code': r'\d{6}'
        }

        phrases = {'phone_number': ['Введите номер телефона без "+7" и "8" в формате "9876543210":',
                                    "Номер введен неверно. Попробуйте ещё раз:"
                                    ],
                   'code': [
                       'Введите 6-тизначный код в формате "123456":',
                       "Код введен неверно. Попробуйте ещё раз:"
                   ]
                   }

        print(phrases[input_type][0])

        # Цикл работает до тех пор, пока введенные данные не будут корректны.
        while True:
            code_or_number = input()
            if re.fullmatch(templates[input_type], code_or_number):
                break
            print(phrases[input_type][1])

        return code_or_number

    # Метод делает скриншот заказа и открывает его в программе по умолчанию.
    @staticmethod
    def cart_screenshot(driver):
        cart = driver.find_element(By.CSS_SELECTOR,
                                   '#app > div.pe-none.cart-button.container > div > div > div.popover__content')
        cart.screenshot('cart.png')
        screen = Image.open('cart.png')
        screen.show()

    @staticmethod
    def delivery_way(driver):
        delivery_way = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/ul/li[2]")
        delivery_way.click()

    @staticmethod
    def pick_up_points(driver):
        pick_up_points = driver.find_element(By.XPATH,
                                             "/html/body/div[4]/div/div/div/div[2]/div[1]/div/div[1]/div["
                                             "2]/div/div/div/ul/li[2]")
        pick_up_points.click()

    @staticmethod
    def add_meal(driver):
        add_meal = driver.find_element(By.CSS_SELECTOR,
                                       '#recommendrecommend > div > div:nth-child(1) > div.product__wrapper > '
                                       'div.product-menu > div.product-actions > '
                                       'button.button.position-relative.d-inline-flex.align-items-center.overflow'
                                       '-hidden.outline-none.cursor-pointer.us-none.button--default.button'
                                       '--medium.button--secondary.button--square.add-button')
        add_meal.click()

    @staticmethod
    def go_to_cart(driver):
        go_to_cart = driver.find_element(By.CSS_SELECTOR,
                                         '#app > div.pe-none.cart-button.container > div > div > div > button')
        go_to_cart.click()

    @staticmethod
    def place_the_order(driver):
        place_the_order = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/button')
        place_the_order.click()

    @staticmethod
    def authorization(driver):
        authorization = driver.find_element(By.CSS_SELECTOR,
                                            '#topBar > div > div > div.topbar__menu > div > div > '
                                            'div.popover__content > form > div.login-ways > div > '
                                            'button.button.position-relative.d-inline-flex.align-items-center'
                                            '.overflow-hidden.outline-none.cursor-pointer.us-none.button--default'
                                            '.button--large.button--primary.button--uppercase.button--expanded')
        authorization.click()

    @staticmethod
    def checkout(driver):
        try:
            cart = driver.find_element(By.CSS_SELECTOR,
                                       '#app > div.pe-none.cart-button.container > div > div > div.popover__content > '
                                       'div')
            checkout = driver.find_element(By.CSS_SELECTOR,
                                           '#app > div.pe-none.cart-button.container > div > div > '
                                           'div.popover__content > div > button')
            checkout.click()
        except:
            go_to_cart = driver.find_element(By.CSS_SELECTOR, '#app > div.pe-none.cart-button.container > div')
            go_to_cart.click()
            checkout = driver.find_element(By.CSS_SELECTOR,
                                           '#app > div.pe-none.cart-button.container > div > div > '
                                           'div.popover__content > div > button')
            checkout.click()

    def number_box(self, driver):
        number_box = driver.find_element(By.CSS_SELECTOR,
                                         '#topBar > div > div > div.topbar__menu > div > div > '
                                         'div.popover__content > form > div.login-form > '
                                         'div.text-field-wrapper.position-relative.text-field-wrapper--prepend'
                                         '-icon.text-field-wrapper--large.phone-field > input')
        number_box.click()
        number_box.send_keys(self.number)

    def enter_code(self, driver):
        self.code = self.number_and_code_validation('code')
        confirmation = driver.find_element(By.CSS_SELECTOR,
                                           '#topBar > div > div > div.topbar__menu > div > div > '
                                           'div.popover__content > form > div > div > input')
        confirmation.click()
        confirmation.send_keys(self.code)

    # Метод для формирования заказа.
    def order(self):
        driver = self.driver
        driver.maximize_window()
        driver.implicitly_wait(20)
        try:
            driver.get("https://shop.foodsoul.pro/")
            # Выбор способа получения заказа, в данном случае самовывозом.
            self.delivery_way(driver)
            # Выбор пункта выдачи.
            self.pick_up_points(driver)
            # Скролл страницы для прогрузки товаров
            driver.execute_script("window.scrollTo(0, 1200);")
            # Добавление в корзину первого блюда из рекомендаций
            self.add_meal(driver)
            driver.execute_script("window.scrollTo(0, -1200);")
            # Переход к корзине.
            self.go_to_cart(driver)
            # Метод делает скриншот корзины.
            self.cart_screenshot(driver)
            # Клик на оформление заказа.
            self.place_the_order(driver)
            # Ввод номера телефона.
            self.number_box(driver)
            # Нажатие на кнопку телефона.
            self.authorization(driver)
            # Ввод кода и его проверка с помощью метода класса.
            self.enter_code(driver)
            # Нажатие на кнопку оформления заказа.
            self.checkout(driver)
            time.sleep(5)

            # Выбор способа оплаты
            payment = driver.find_element(By.XPATH, '//*[@id="app"]/main/div[2]/form/div/div/div[1]/div[2]/ul/li['
                                                    '4]/div/div[1]/button')

            driver.execute_script("arguments[0].scrollIntoView();", payment)
            payment.click()
            # action = webdriver.common.action_chains.ActionChains(driver)
            # action.move_to_element_with_offset(payment, 5, 5)
            # action.click()
            # action.perform()

            pay_by_card = driver.find_element(By.XPATH, '//*[@id="app"]/main/div[2]/form/div/div/div[1]/div[2]/ul/li['
                                                        '4]/div/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]')
            # driver.execute_script("arguments[0].scrollIntoView();", pay_by_card)
            action2 = webdriver.common.action_chains.ActionChains(driver)
            action2.move_to_element_with_offset(pay_by_card, 5, 5)
            action2.click()
            action2.perform()
            # pay_by_card.click()

            # Размещение заказа
            place_an_order = driver.find_element(By.CSS_SELECTOR,
                                                 '#app > main > div.main-slot > form > div > div > div:nth-child(1) > '
                                                 'button > div')
            place_an_order.click()
            time.sleep(5)
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()


if __name__ == '__main__':
    tprint('FoodSoul')
    fs_order = FoodSoulOrder()
    fs_order.order()
