
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import time
import csv
from bs4 import BeautifulSoup


options = Options()
options.headless = True
print('please wait')
driver = WebDriver(executable_path='driver.exe', options=options)
CSV = 'cards.csv' #CSV path and file name
content = []
url = 'https://secure.helpscout.net/'

#Get len of pages in customers
def get_number_of_pages(url):
    while True:
        driver.get(url)
        user_login = input('Please input your login: ')
        user_password = input('Please input your password: ')
        print('going in to accaunt')
        while True:
            try:
                driver.find_element_by_css_selector('#email')
                break
            except NoSuchElementException:
                continue
        login_input = driver.find_element_by_css_selector('#email')
        login_input.send_keys(user_login)
        pass_input = driver.find_element_by_css_selector('#password')
        pass_input.send_keys(user_password)
        login_button = driver.find_element_by_css_selector('#logInButton')
        login_button.click()
        time.sleep(10)
        try:
            customers_button = driver.find_element_by_css_selector('.nav-main > li:nth-child(5) > a')
            customers_button.click()
            print('Password accept')
            print('finding number of pages in customers')
            break
        except NoSuchElementException:
            print('wrong password or login name')
            continue

    time.sleep(2)
    last_page_button = driver.find_element_by_css_selector('button.Buttoncss__ButtonUI-sc-11k3518-0:nth-child(4)')
    last_page_button.click()
    time.sleep(4)
    last_page = driver.current_url
    pages = BeautifulSoup(last_page, 'html.parser').text.split('=')[1]
    last_page_number = int(pages)
    print('pages number of customers is: ' + str(last_page_number))
    return last_page_number

#Get number of pages in customer
def get_pages_urls():
    last_page_number = get_number_of_pages(url)
    pages_urls = ['https://secure.helpscout.net/customers/',]
    num = 1
    for x in range(last_page_number-1):
        num +=1
        page_url = 'https://secure.helpscout.net/customers/?page='+str(num)
        pages_urls.append(page_url)
    return pages_urls

#Save to CSV file (file name "card.csv"
def save_doc(item, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        #writer.writerow([item['title'], item['opisanie'], item['tech_opisanie'], item['pic_links']])
        writer.writerow(['Name', 'Email', 'Number'])
        for item in item:
             writer.writerow([item['name'], item['mail'], item['number']])

#Get all content from customers
def get_all_content():
    page_urls = get_pages_urls()
    x = 0
    for page_url in page_urls:
        x += 1
        print('parsing page: '+ str(x))
        driver.get(page_url)

        time.sleep(3)
        names = driver.find_elements_by_xpath('//div[@class="Flexycss__FlexyBlockUI-mfgely-1 bCujEv c-Flexy__block sc-fzozJi kxWqr"]')
        emails_name = driver.find_elements_by_xpath('//span[@class="c-Truncate__content__chunks__first"]')
        emails_domain = driver.find_elements_by_xpath('//span[@class="c-Truncate__content__chunks__second"]')
        nums = driver.find_elements_by_xpath('//span[@class="Textcss__TextUI-cdrlb6-0 eMuyYC c-Text is-span is-13 is-default sc-fzplWN fwFPgA"]')
        a = 0
        b = 0
        for email_name in emails_name:
            content.append(
                {
                    'name': names[a].text,
                    'mail': emails_name[a].text+emails_domain[a].text,
                    'number': nums[b].text
                }
            )
            a +=1
            b +=2

    save_doc(content, CSV)
    driver.close()
    print('All is done well!')
    print('Content is saved in "card.csv" (you can open with Microsoft Excel')

if __name__ == '__main__':
    get_all_content()