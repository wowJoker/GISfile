import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '', filename)

def search_jobs(region, city, industry1, industry2):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    url = "https://job.ncss.cn/student/m/jobs/index.html"
    driver.get(url)
    time.sleep(3)

    region_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='van-ellipsis' and text()='地区']"))
    )
    region_dropdown.click()

    province = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[@class='van-sidebar-item__text' and text()='{region}']"))
    )
    province.click()

    city_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[@class='van-ellipsis van-tree-select__item' and text()='{city}']"))
    )
    city_option.click()

    industry_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='van-ellipsis' and text()='行业']"))
    )
    industry_dropdown.click()

    industry_main = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[@class='van-sidebar-item__text' and text()='{industry1}']"))
    )
    industry_main.click()

    industry_sub = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[@class='van-ellipsis van-tree-select__item' and text()='{industry2}']"))
    )
    industry_sub.click()

    more_choose = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='more-sp' and text()='更多']"))
    )
    more_choose.click()

    all_choose = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='filter-default-txt van-ellipsis' and text()='全部']"))
    )
    all_choose.click()

    sure_choose = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='van-button--bottom-action van-button van-button--primary van-button--normal']"))
    )
    sure_choose.click()

    time.sleep(3)
    last_height = driver.execute_script("return document.body.scrollHeight")
    max_scrolls = 20
    scroll_count = 0

    while scroll_count < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height
        scroll_count += 1

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()

    job_list = soup.find('ul', class_='job-list')
    if not job_list:
        print("没有找到相关的职位信息")
        return

    jobs = job_list.find_all('li')

    file_name = f"E:/系统默认/桌面/2024(下)/GIS综合实习/数据获取/{clean_filename(region)}-{clean_filename(city)}-{clean_filename(industry1)}-{clean_filename(industry2)}.csv"

    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['实习名称', '公司名称',  '实习地点', '学历要求', '工资', '发布日期', '来源'])

            for job in jobs:
                title = job.find('h5').text.strip()
                company = job.find('p', class_='corp-name').text.strip() if job.find('p', 'corp-name') else '无'
                job_infos = job.find('p', 'job-infos').text.strip()
                # 分割并去除空格
                job_location, education_requirements = [(info.strip() if info else '无') for info in
                                                        (job_infos.split('|') + ['无', '无'])[:2]]
                # job_location, education_requirements = (job_infos.split('|') + ['无', '无'])[:2]
                pay = job.find('p', 'paymoney-p').text.strip()
                publish_date = job.find('time').text.strip()
                source = job.find('p', 'source-p').text.strip()

                writer.writerow([title, company, job_location, education_requirements, pay, publish_date, source])

        print(f"职位信息已保存为文件: {file_name}")

    except Exception as e:
        print(f"发生错误: {e}")

# 示例调用
search_jobs(region="河北省", city="唐山市", industry1="互联网/通信/电子", industry2="网络游戏")
