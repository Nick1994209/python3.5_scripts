from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains

CHROME_DRIVER = '/Users/nvkorolkov/Documents/chromedriver'


def login_to_skyeng(browser: Chrome):
    print('login_to_skyeng')

    url = 'https://pcs.skyeng.ru'
    browser.get(url)

    login_input, password_input = browser.find_elements_by_class_name('b-auth-login__input')
    login_input.send_keys('nick1994209@yandex.ru')
    password_input.send_keys('65656565')
    browser.find_element_by_class_name('b-gui-v2-button__holder').click()


def download_skyeng_extension(browser: Chrome):
    print('download_skyeng_extension')
    url = 'https://chrome.google.com/webstore/detail/vimbox-%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4%D1%87%D0%B8%D0%BA-%D0%BE%D1%82-skye/heeikiohkfkolhmdodhcjdklofmhmmhn?hl=ru'
    browser.get(url)

    sleep(2)
    browser.find_element_by_xpath("//*[text()='Установить']").click()

    # browser.find_element_by_xpath("//div[@aria-label='Установить']").click()

    # driver.find_elements_by_xpath("//*[contains(text(), 'Установить расширение')]")

    # browser.find_element_by_xpath("//*[matches(.,'Установить',)]").click()

    # browser.find_element_by_xpath("//*[text()='Установить']").click()
    # browser.find_element_by_xpath("//*[matches(.,'Установить расширение',)]").click()
    # browser.find_element_by_xpath("//*[matches(.,'Установить расширение', 'i')]").click()
    #
    # browser.find_element_by_xpath("//div[@aria-label='Установить']").click()
    # browser.find_element_by_xpath("//div[text='Установить']").click()
    # browser.find_element_by_xpath("driver.find_element_by_xpath("//*[text()='Установить']")").click()
    # browser.find_element_by_class_name('webstore-test-button-label').click()
    # browser.find_element_by_class_name('webstore-test-button-label').click()

    # browser.find_element_by_xpath("//div[@aria-label='Установить']")

    input('Установи extension и ввойди в него!!!')


def delete_words_from_skyeng(browser: Chrome):
    print('delete_words_from_skyeng')
    url = 'https://ext.skyeng.tv/translate/dictionary.html'
    browser.get(url)
    sleep(2)

    while True:
        delete_item = browser.find_element_by_class_name('word-set__title-icon--delete')
        sleep(0.3)
        ActionChains(browser).move_to_element(delete_item).perform()
        sleep(0.3)
        browser.find_element_by_class_name('word-set__title-icon--delete').click()
        sleep(0.3)
        browser.find_element_by_xpath("//*[text()='Да, удалить']").click()
        sleep(1)


browser = Chrome(CHROME_DRIVER)

try:
    login_to_skyeng(browser)
    download_skyeng_extension(browser)
    delete_words_from_skyeng(browser)
except Exception as e:
    import logging
    logging.getLogger(__name__).exception(e)

    # browser.close()
