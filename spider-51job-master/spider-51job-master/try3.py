import json
import os
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd


class Job51Crawler:
    def __init__(self):
        # 表头
        self.fieldnames = [
            'job_id',
            'job_name',
            'update_time',
            'com_name',
            'salary',
            'workplace',
            'job_exp',
            'job_edu',
            'job_rent',
            'company_type',
            'company_size',
            'job_welfare',
            'company_ind',
            'job_info',
            'job_type',
        ]
        self.j_id = 1

    def search_city(self, job, code, city, page):
        chrome_driver = 'E:\\Anaconda2023\\Scripts\\chromedriver.exe'
        opts = Options()
        opts.add_argument('--disable-gpu')
        opts.add_argument('--no-sandbox')
        prefs = {'profile.default_content_setting_values': {'images': 2}}
        opts.add_experimental_option('prefs', prefs)

        try:
            self.web = webdriver.Chrome(options=opts, executable_path=chrome_driver)
            self.web.get(f"https://we.51job.com/pc/search?keyword={job}&searchType=2&sortType=0&metro=")
            self.web.implicitly_wait(30)
        except Exception as e:
            print(e)
            return

        # 选择城市
        if city:
            WebDriverWait(self.web, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'allcity')))
            self.web.find_element(by=By.CLASS_NAME, value="allcity").click()
            for i in self.web.find_elements(by=By.CLASS_NAME, value="el-tabs__item"):
                i.click()
                try:
                    WebDriverWait(self.web, 1).until(
                        EC.visibility_of_element_located((By.XPATH, f"//*[text()='{city}']")))
                    self.web.find_element(By.XPATH, f"//*[text()='{city}']").click()
                except Exception as e:
                    pass

            WebDriverWait(self.web, 20).until(
                EC.visibility_of_element_located((By.XPATH, f'//*[@id="dilog"]/div/div[3]/span/button/span')))
            self.web.find_element(By.XPATH, f'//*[@id="dilog"]/div/div[3]/span/button/span').click()

            WebDriverWait(self.web, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'btn-next')))

        page_num = int(self.web.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/ul/li[last()]').text)
        print(f"page_num:{page_num}")

        if page > page_num:
            page = page_num

        # Prepare file
        file = f'./data/{city}_{job}.csv'
        header = not os.path.exists(file)

        # 翻页操作
        for i in range(page):
            data_list = self.get_data()
            self.save(data_list, file, header)
            header = False  # Only write the header for the first page
            # 翻页
            self.web.find_element(by=By.CLASS_NAME, value="btn-next").click()
            print(f"page={i}")

        return f"Data saved to {file}"

    def get_data(self):
        WebDriverWait(self.web, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'joblist')))
        job_list = self.web.find_element(by=By.CLASS_NAME, value='joblist')
        data_list = []

        for job in job_list.find_elements(By.CLASS_NAME, value="joblist-item"):
            item = dict()
            item['job_id'] = self.j_id
            self.j_id += 1
            item['com_name'] = job.find_element(by=By.XPATH, value=".//a[@class='cname text-cut']").text
            item['job_name'] = job.find_element(by=By.XPATH, value=".//span[@class='jname text-cut']").text

            job_element = job.find_element(By.XPATH, "//div[@sensorsname='JobShortExposure']")
            sensorsdata = job_element.get_attribute("sensorsdata")
            sensorsdata_dict = json.loads(sensorsdata)

            item['update_time'] = sensorsdata_dict['jobTime']
            item['salary'] = sensorsdata_dict['jobSalary']
            item['workplace'] = sensorsdata_dict['jobArea']
            item['job_exp'] = sensorsdata_dict['jobYear']
            item['job_edu'] = sensorsdata_dict['jobDegree']
            item['job_rent'] = ''

            item['company_type'] = job.find_element(by=By.XPATH, value=".//span[@class='dc text-cut']").text

            try:
                item['company_size'] = job.find_element(by=By.XPATH, value="(.//span[@class='dc shrink-0'])[2]").text
            except NoSuchElementException:
                item['company_size'] = ""

            item['job_welfare'] = ""
            item['company_ind'] = ""
            item['job_info'] = ""
            item['job_type'] = ""
            data_list.append(item)

        return data_list

    def save(self, data, file, header):
        df2 = pd.DataFrame(data)
        df2.to_csv(file, mode='a', index=False, header=header, columns=self.fieldnames)


if __name__ == '__main__':
    spider = Job51Crawler()
    print(spider.search_city("python", 111, "西安", 3))