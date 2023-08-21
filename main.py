from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import re
from art import tprint
from selenium.webdriver.support.ui import Select


class FoodSoulOrder:
    service = Service(executable_path='chromedriver_win32/chromedriver.exe')
    options = Options()
    options.add_argument("--window-size=450,570")

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

    @staticmethod
    def template_check(driver):
        pattern = r'template="[a-z]*"'
        time.sleep(2)
        html = driver.page_source
        template = re.search(pattern, html)
        return template[0][10:-1]

    def delivery_way(self, driver):
        xpath_dict = {
            'mosaic': "/html/body/div[4]/div/div/div/ul/li[2]",
            'mobile': '/html/body/div[2]/div[2]/div[4]/div[2]/div/div[3]/button[2]/span'
        }
        template = self.template_check(driver)
        delivery_way = driver.find_element(By.XPATH, xpath_dict[template])
        delivery_way.click()

    def pick_up_points(self, driver):
        xpath_dict = {
            'mosaic': "/html/body/div[4]/div/div/div/div[2]/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]",
            'mobile': "/html/body/div[2]/div[2]/div[2]/main/div/div[1]/div[2]/div[2]/div/div[2]/div[1]"
        }
        template = self.template_check(driver)
        if template == 'mobile':
            is_kirov = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/div[2]/div/div[3]/button[1]/span')
            is_kirov.click()
            cookies = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/div[2]/div/div[2]/button/span')
            cookies.click()
        pick_up_points = driver.find_element(By.XPATH, xpath_dict[template])
        pick_up_points.click()

    def add_meal(self, driver):
        css_selector_dict = {
            'mosaic': '#recommendrecommend > div > div:nth-child(1) > div.product__wrapper > '
                      'div.product-menu > div.product-actions > '
                      'button.button.position-relative.d-inline-flex.align-items-center.overflow'
                      '-hidden.outline-none.cursor-pointer.us-none.button--default.button'
                      '--medium.button--secondary.button--square.add-button',
            'mobile': '#recommendrecommend > div.block-products.d-flex.flex-wrap > div:nth-child(1) > '
                      'div.product-card > div.product-card__actions > '
                      'div.product-quantity.d-flex.justify-content-between > div > svg > use '
        }
        template = self.template_check(driver)
        add_meal = driver.find_element(By.CSS_SELECTOR, css_selector_dict[template])
        add_meal.click()
        if template == 'mobile':
            driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/main/div/button/span').click()

    def go_to_cart(self, driver):
        css_selector_dict = {
            'mosaic': '#app > div.pe-none.cart-button.container > div > div > div > button',
            'mobile': '#app > div.content.position-relative.d-flex.flex-column > main > div.catalog-page.h-100 > a > '
                      'span '
        }
        template = self.template_check(driver)
        go_to_cart = driver.find_element(By.CSS_SELECTOR, css_selector_dict[template])
        go_to_cart.click()

    # Метод делает скриншот заказа и открывает его в программе по умолчанию.
    def cart_screenshot(self, driver):
        css_selector_dict = {
            'mosaic': '#app > div.pe-none.cart-button.container > div > div > div.popover__content',
            'mobile': '#app > div.content.position-relative.d-flex.flex-column > main > div > div.cart-page'
        }
        template = self.template_check(driver)
        cart = driver.find_element(By.CSS_SELECTOR, css_selector_dict[template])
        cart.screenshot('cart.png')
        screen = Image.open('cart.png')
        screen.show()

    def place_order(self, driver):
        xpath_dict = {
            'mosaic': '/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/button',
            'mobile': '/html/body/div[2]/div[2]/div[2]/main/div/div[1]/button/span'
        }
        template = self.template_check(driver)
        place_the_order = driver.find_element(By.XPATH, xpath_dict[template])
        place_the_order.click()

    def number_box(self, driver):
        css_selector_dict = {
            'mosaic': '/html/body/div[2]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/form/div[1]/div[1]/input',
            'mobile': '/html/body/div[2]/div[2]/div[2]/main/form/div[1]/div[3]/div[1]/div[2]/input'
        }
        template = self.template_check(driver)
        number_box = driver.find_element(By.XPATH, css_selector_dict[template])
        if template != 'mobile':
            number_box.click()
        number_box.send_keys(self.number)

    def authorization(self, driver):
        css_selector_dict = {
            'mosaic': '#topBar > div > div > div.topbar__menu > div > div > '
                      'div.popover__content > form > div.login-ways > div > '
                      'button.button.position-relative.d-inline-flex.align-items-center'
                      '.overflow-hidden.outline-none.cursor-pointer.us-none.button--default'
                      '.button--large.button--primary.button--uppercase.button--expanded',
            'mobile': '#app > div.content.position-relative.d-flex.flex-column > main > form > '
                      'div.login-page__buttons > button:nth-child(2) > span '
        }
        template = self.template_check(driver)
        authorization = driver.find_element(By.CSS_SELECTOR, css_selector_dict[template])
        authorization.click()

    def enter_code(self, driver):
        css_selector_dict = {
            'mosaic': '#topBar > div > div > div.topbar__menu > div > div > '
                      'div.popover__content > form > div > div > input',
            'mobile': '#app > div.content.position-relative.d-flex.flex-column > main > div > div > '
                      'div.input-box.position-relative.d-flex.justify-content-center > input '
        }
        template = self.template_check(driver)
        self.code = self.number_and_code_validation('code')
        confirmation = driver.find_element(By.CSS_SELECTOR, css_selector_dict[template])
        confirmation.click()
        confirmation.send_keys(self.code)

    def checkout(self, driver):
        css_selector_dict = {
            'mosaic': '#app > div.pe-none.cart-button.container > div > div > div.popover__content > div > button',
            'mobile': '#app > div.content.position-relative.d-flex.flex-column > main > div > div.cart-page > button '
                      '> span '
        }
        template = self.template_check(driver)
        if template == 'mobile':
            self.go_to_cart(driver)
        checkout = driver.find_element(By.CSS_SELECTOR, css_selector_dict[template])
        driver.execute_script("arguments[0].click();", checkout)

    def payment_method(self, driver):
        template = self.template_check(driver)
        if template == 'mobile':
            select = Select(driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/main/div/form/div['
                                                          '3]/div/div[2]/div[2]/div[1]/div/div/select'))
            select.select_by_value('1')
        else:
            payment = driver.find_element(By.XPATH, '//*[@id="app"]/main/div[2]/form/div/div/div[1]/div['
                                                    '2]/ul/li[4]/div/div[1]/button')
            driver.execute_script("arguments[0].scrollIntoView();", payment)
            driver.execute_script("arguments[0].click();", payment)
            pay_by_card = driver.find_element(By.XPATH, '//*[@id="app"]/main/div[2]/form/div/div/div[1]/div[2]/ul/li['
                                                        '4]/div/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]')

            driver.execute_script("arguments[0].click();", pay_by_card)

    def place_the_order(self, driver):
        css_selector_dict = {
            'mosaic': '#app > main > div.main-slot > form > div > div > div:nth-child(1) > '
                      'button > div',
            'mobile': '#app > div.content.position-relative.d-flex.flex-column > main > div > form > '
                      'div.checkout-page__submit > button > span '
        }
        template = self.template_check(driver)
        place_an_order = driver.find_element(By.CSS_SELECTOR, css_selector_dict[template])
        driver.execute_script("arguments[0].click();", place_an_order)

    # Метод для формирования заказа.
    def order(self):
        driver = self.driver
        # driver.maximize_window()
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
            self.place_order(driver)
            # Ввод номера телефона.
            self.number_box(driver)
            # Нажатие на кнопку телефона.
            self.authorization(driver)
            # Ввод кода и его проверка с помощью метода класса.
            self.enter_code(driver)
            time.sleep(5)
            # Нажатие на кнопку оформления заказа.
            self.checkout(driver)
            # Выбор способа оплаты (картой при получении).
            self.payment_method(driver)
            # Размещение заказа
            self.place_the_order(driver)
            time.sleep(10)
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()


if __name__ == '__main__':
    tprint('FoodSoul')
    fs_order = FoodSoulOrder()
    fs_order.order()
