from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_driver_path = 'E:\\Anaconda2023\\Scripts\\chromedriver.exe'  # 确保路径正确

opts = Options()
opts.add_argument('--headless')

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=opts)
driver.get('http://www.google.com')
print(driver.title)  # 应该输出 Google 页面的标题
driver.quit()
