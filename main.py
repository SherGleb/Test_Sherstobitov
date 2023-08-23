from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import re
from art import tprint
from selenium.webdriver.support.ui import Select


class User:
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

    def __init__(self):
        self.number = self.number_and_code_validation('phone_number')
        self.code = None

    @classmethod
    def number_and_code_validation(cls, input_type):

        print(cls.phrases[input_type][0])

        # Цикл работает до тех пор, пока введенные данные не будут корректны.
        while True:
            code_or_number = input()
            if re.fullmatch(cls.templates[input_type], code_or_number):
                break
            print(cls.phrases[input_type][1])

        return code_or_number

    def set_code(self):
        self.code = self.number_and_code_validation('code')


class Driver:
    # service = Service(executable_path='chromedriver_win32/chromedriver.exe')
    service = Service()
    options = Options()
    options.add_argument("--window-size=500,650")

    def __init__(self):
        self.driver = webdriver.Chrome(options=Driver.options, service=Driver.service)

    def get_url(self, url):
        self.driver.get(url)

    def template_check(self):
        pattern = r'template="[a-z]*"'
        time.sleep(2)
        html = self.driver.page_source
        template = re.search(pattern, html)
        return template[0][10:-1]

    def find_element(self, by_obj, path):
        return self.driver.find_element(by_obj, path)

    def implicitly_wait(self, sec):
        self.driver.implicitly_wait(sec)

    def exit(self):
        self.driver.close()
        self.driver.quit()


class DeliveryPage:
    def __init__(self, driver_obj: Driver):
        self.driver_obj = driver_obj

    def delivery_way(self):
        xpath_dict = {
            'mosaic': "/html/body/div[4]/div/div/div/ul/li[2]",
            'mobile': '/html/body/div[2]/div[2]/div[4]/div[2]/div/div[3]/button[2]/span'
        }
        template = self.driver_obj.template_check()
        delivery_way = self.driver_obj.find_element(By.XPATH, xpath_dict[template])
        delivery_way.click()

    def pick_up_points(self):
        xpath_dict = {
            'mosaic': "/html/body/div[4]/div/div/div/div[2]/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]",
            'mobile': "/html/body/div[2]/div[2]/div[2]/main/div/div[1]/div[2]/div[2]/div/div[2]/div[1]"
        }
        template = self.driver_obj.template_check()
        if template == 'mobile':
            is_kirov = self.driver_obj.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/div[2]/div/div[3]/button[1]/span')
            is_kirov.click()
            cookies = self.driver_obj.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/div[2]/div/div[2]/button/span')
            cookies.click()
        pick_up_points = self.driver_obj.find_element(By.XPATH, xpath_dict[template])
        pick_up_points.click()


class MainPage:
    def __init__(self, driver_obj: Driver):
        self.driver_obj = driver_obj

    def add_meal(self):
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
        template = self.driver_obj.template_check()
        self.driver_obj.driver.execute_script("window.scrollTo(0, 1200);")
        add_meal = self.driver_obj.find_element(By.CSS_SELECTOR, css_selector_dict[template])
        add_meal.click()
        self.driver_obj.driver.execute_script("window.scrollTo(0, -1200);")
        if template == 'mobile':
            self.driver_obj.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/main/div/button/span').click()

    def go_to_cart(self):
        css_selector_dict = {
            'mosaic': '#app > div.pe-none.cart-button.container > div > div > div > button',
            'mobile': '#app > div.content.position-relative.d-flex.flex-column > main > div.catalog-page.h-100 > a > '
                      'span '
        }
        template = self.driver_obj.template_check()
        go_to_cart = self.driver_obj.find_element(By.CSS_SELECTOR, css_selector_dict[template])
        go_to_cart.click()


class Cart:
    def __init__(self, driver_obj: Driver):
        self.driver_obj = driver_obj

    def cart_screenshot(self):
        css_selector_dict = {
            'mosaic': '#app > div.pe-none.cart-button.container > div > div > div.popover__content',
            'mobile': '#app > div.content.position-relative.d-flex.flex-column > main > div > div.cart-page'
        }
        template = self.driver_obj.template_check()
        cart = self.driver_obj.find_element(By.CSS_SELECTOR, css_selector_dict[template])
        cart.screenshot('cart.png')
        screen = Image.open('cart.png')
        screen.show()

    def place_order(self):
        xpath_dict = {
            'mosaic': '/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/button',
            'mobile': '/html/body/div[2]/div[2]/div[2]/main/div/div[1]/button/span'
        }
        template = self.driver_obj.template_check()
        place_the_order = self.driver_obj.find_element(By.XPATH, xpath_dict[template])
        place_the_order.click()

    def checkout(self, main_pg: MainPage):
        css_selector_dict = {
            'mosaic': '#app > div.pe-none.cart-button.container > div > div > div.popover__content > div > button',
            'mobile': '#app > div.content.position-relative.d-flex.flex-column > main > div > div.cart-page > button '
                      '> span '
        }
        template = self.driver_obj.template_check()
        if template == 'mobile':
            main_pg.go_to_cart()
        checkout = self.driver_obj.find_element(By.CSS_SELECTOR, css_selector_dict[template])
        self.driver_obj.driver.execute_script("arguments[0].click();", checkout)


class Authorization:
    def __init__(self, driver_obj: Driver):
        self.driver_obj = driver_obj

    def number_box(self, user: User):
        css_selector_dict = {
            'mosaic': '/html/body/div[2]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/form/div[1]/div[1]/input',
            'mobile': '/html/body/div[2]/div[2]/div[2]/main/form/div[1]/div[3]/div[1]/div[2]/input'
        }
        template = self.driver_obj.template_check()
        number_box = self.driver_obj.find_element(By.XPATH, css_selector_dict[template])
        if template != 'mobile':
            number_box.click()
        number_box.send_keys(user.number)

    def phone_button(self):
        css_selector_dict = {
            'mosaic': '#topBar > div > div > div.topbar__menu > div > div > '
                      'div.popover__content > form > div.login-ways > div > '
                      'button.button.position-relative.d-inline-flex.align-items-center'
                      '.overflow-hidden.outline-none.cursor-pointer.us-none.button--default'
                      '.button--large.button--primary.button--uppercase.button--expanded',
            'mobile': '#app > div.content.position-relative.d-flex.flex-column > main > form > '
                      'div.login-page__buttons > button:nth-child(2) > span '
        }
        template = self.driver_obj.template_check()
        authorization = self.driver_obj.find_element(By.CSS_SELECTOR, css_selector_dict[template])
        authorization.click()

    def enter_code(self, user: User):
        css_selector_dict = {
            'mosaic': '#topBar > div > div > div.topbar__menu > div > div > '
                      'div.popover__content > form > div > div > input',
            'mobile': '#app > div.content.position-relative.d-flex.flex-column > main > div > div > '
                      'div.input-box.position-relative.d-flex.justify-content-center > input '
        }
        template = self.driver_obj.template_check()
        user.set_code()
        confirmation = self.driver_obj.find_element(By.CSS_SELECTOR, css_selector_dict[template])
        confirmation.click()
        confirmation.send_keys(user.code)


class OrderingPage:
    def __init__(self, driver_obj: Driver):
        self.driver_obj = driver_obj

    def payment_method(self):
        template = self.driver_obj.template_check()
        if template == 'mobile':
            select = Select(self.driver_obj.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/main/div/form/div['
                                                          '3]/div/div[2]/div[2]/div[1]/div/div/select'))
            select.select_by_value('1')
        else:
            payment = self.driver_obj.find_element(By.XPATH, '//*[@id="app"]/main/div[2]/form/div/div/div[1]/div['
                                                    '2]/ul/li[4]/div/div[1]/button')
            self.driver_obj.driver.execute_script("arguments[0].scrollIntoView();", payment)
            self.driver_obj.driver.execute_script("arguments[0].click();", payment)
            pay_by_card = self.driver_obj.find_element(By.XPATH, '//*[@id="app"]/main/div[2]/form/div/div/div[1]/div[2]/ul/li['
                                                        '4]/div/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]')

            driver.execute_script("arguments[0].click();", pay_by_card)

    def place_the_order(self):
        css_selector_dict = {
            'mosaic': '#app > main > div.main-slot > form > div > div > div:nth-child(1) > '
                      'button > div',
            'mobile': '#app > div.content.position-relative.d-flex.flex-column > main > div > form > '
                      'div.checkout-page__submit > button > span '
        }
        template = self.driver_obj.template_check()
        place_an_order = self.driver_obj.find_element(By.CSS_SELECTOR, css_selector_dict[template])
        self.driver_obj.driver.execute_script("arguments[0].click();", place_an_order)


if __name__ == '__main__':
    tprint('FoodSoul')
    usr = User()
    driver = Driver()
    # driver.driver.maximize_window()
    driver.implicitly_wait(20)
    try:
        driver.get_url("https://shop.foodsoul.pro/")
        delivery = DeliveryPage(driver)
        delivery.delivery_way()
        delivery.pick_up_points()
        mainpage = MainPage(driver)
        mainpage.add_meal()
        mainpage.go_to_cart()
        cart_window = Cart(driver)
        cart_window.cart_screenshot()
        cart_window.place_order()
        login = Authorization(driver)
        login.number_box(usr)
        login.phone_button()
        login.enter_code(usr)
        cart_window.checkout(mainpage)
        time.sleep(5)
        order = OrderingPage(driver)
        order.payment_method()
        order.place_the_order()
        time.sleep(10)
    except Exception as ex:
        print(ex)
    finally:
        driver.exit()
