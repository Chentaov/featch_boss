from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import code_mapping_city
from fake_useragent import UserAgent
from urllib.parse import urlparse, urlunparse
from Models.Jobs import Jobs
from selenium.webdriver.common.keys import Keys

ua = UserAgent()
u_a = ua.random
chrome_op = webdriver.ChromeOptions()
chrome_op.add_argument(f'user-agent={u_a}')
driver = webdriver.Chrome(options=chrome_op)

query_job = 'python'  # 查什么工作
experience = '102,101,103'  # 经验要求102=应届，103=一年以内，101=不限
salary = '405,404'  # 405 10-20k,404 5-10k
query_city = code_mapping_city.get_city_code('杭州')  # 查找的城市代码
# query_area = code_mapping_city.get_region_code('余杭区') #查找的区域代码
query_areas = ['上城区', '余杭区', '拱墅区', '西湖区', '滨江区', '萧山', '钱塘区', '临平区']

# query_areas = [code_mapping_city.get_region_code(area) for area in query_areas]


def login():
    login_mode = input('选择登录方式(验证码或扫码)，验证码输入1扫码输入2')
    if login_mode == '1':
        driver.get('https://www.zhipin.com/web/user/?ka=header-login')
        login = driver.find_element(By.XPATH, '//*[@id="wrap"]/div/div[2]/div[2]/div[2]/div[1]/div[3]/button')
        confirm = driver.find_element(By.XPATH, '//*[@id="wrap"]/div/div[2]/div[2]/div[2]/div[2]/span/input')
        send_code = driver.find_element(By.XPATH, '//*[@id="wrap"]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/span/div')
        tel = driver.find_element(By.XPATH, '//*[@id="wrap"]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/span[2]/input')

        tel.send_keys(13735784705)
        confirm.click()
        send_code.click()
        time.sleep(5)
        hascode = True

        while hascode:
            code = driver.find_element(By.XPATH,
                                       '//*[@id="wrap"]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/span/input')
            code = code.get_attribute('value')
            if str(code) != '' and len(str(code)) >= 6:
                hascode = False
                print('登录成功')
        login.click()
        time.sleep(5)
    elif login_mode == '2':
        driver.get('https://www.zhipin.com/web/user/?ka=header-login')
        time.sleep(15)




def bugInfo():
    filePath = 'data_store/web_jobs.csv'
    try:

        data = {'url': [], 'name': [], 'salary': [], 'company': [], 'scale': [], 'hr': [], 'region': []}
        for query_area in query_areas:
            page = 1
            while page <= 11:

                query_url = 'https://www.zhipin.com/web/geek/job?query=' + query_job + '&city=' + query_city + '&areaBusiness=' + code_mapping_city.get_region_code(query_area) + '&page=' + str(
                    page) + '&experience=' + experience + '&salary=' + salary
                driver.get(query_url)
                driver.refresh()
                time.sleep(7)
                print('page=' + str(page))

                varify_code_url = '/web/user/safe/verify-slider'
                url_parse = urlparse(driver.current_url)
                url_parse = url_parse.path
                print(url_parse)
                if url_parse == varify_code_url:
                    print('遇到了验证码验证，延时18秒')
                    time.sleep(18)
                    driver.get(query_url)
                    driver.refresh()
                    time.sleep(3)

                job_url = driver.find_elements(By.CLASS_NAME, 'job-card-left')
                job_name = driver.find_elements(By.CLASS_NAME, 'job-name')
                job_salary = driver.find_elements(By.CLASS_NAME, 'salary')
                company_name = driver.find_elements(By.CSS_SELECTOR, '.company-name a')
                company_scale = driver.find_elements(By.CSS_SELECTOR, '.company-tag-list li')[-1]
                hr = driver.find_elements(By.CLASS_NAME, 'info-public')

                job_tables = pd.DataFrame(
                    {'job_name': job_name, 'job_url': job_url, 'job_salary': job_salary, 'company_name': company_name,
                     'company_scale': company_scale, 'hr': hr, 'region': query_area})

                #必须循环将对象数据解析成真实数据
                for index, row in job_tables.iterrows():
                    data['url'].append(row['job_url'].get_attribute('href'))
                    data['name'].append(row['job_name'].get_attribute('textContent'))
                    data['salary'].append(row['job_salary'].get_attribute('textContent'))
                    data['company'].append(row['company_name'].get_attribute('textContent'))
                    data['scale'].append(row['company_scale'].text)
                    data['hr'].append(row['hr'].text)
                    data['region'].append(query_area)

                    print(index, row['job_name'].get_attribute('textContent'), row['job_url'].get_attribute('href'),
                          row['job_salary'].get_attribute('textContent'),
                          row['company_name'].get_attribute('textContent'),
                          row['company_scale'].get_attribute('textContent'),
                          row['hr'].get_attribute('textContent')
                          )
                csv_table = pd.DataFrame(data)
                # 必须循环将对象数据解析成真实数据

                csv_table.to_csv(filePath, index=False, encoding='utf-8')

                # nojob_notice = driver.find_element(By.XPATH, '///*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/div/div/p')
                max_page = driver.find_elements(By.CSS_SELECTOR, '.options-pages a')[-2]
                max_page = max_page.get_attribute('textContent')

                print('max_page=' + max_page+'page='+str(page))
                if max_page == str(page):
                    break
                page = page + 1
                # elif nojob_notice is not None:
                #     break

    except Exception:
        pass
    time.sleep(15)
    driver.quit()


def bugUrl():
    push_count = 0
    query = (Jobs.select(Jobs.url, Jobs.chated, Jobs.id_job, Jobs.job_name)
             .where(((Jobs.job_name.contains('数据分析师')) | Jobs.job_name.contains('python') | Jobs.job_name.contains('爬虫') | Jobs.job_name.contains('测试') | (Jobs.job_name.contains('后端开发'))) & (Jobs.active == 1) & (Jobs.chated == 0)))
    query = query.execute()
    for i in query:
        if push_count == 100:
            break
        driver.get(i.url)
        driver.refresh()
        print(driver.current_url)

        varify_code_url = '/web/user/safe/verify-slider'
        # other_url = '/web/common/security-check.html'
        url_parse = urlparse(driver.current_url)
        url_parse = url_parse.path
        print(url_parse)
        if url_parse == varify_code_url :
            print('遇到了验证码验证，延时15秒')
            time.sleep(15)
            driver.get(i.url)
            driver.refresh()
            time.sleep(3)

        time.sleep(3)
        # job_detail = driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/div[1]/div[2]')
        # job_detail = job_detail.text
        # try:
        try:
            driver.find_element(By.CLASS_NAME, 'boss-active-time')
        except Exception:

            try:
                driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/div/div[1]/div[3]/div[1]/a[2]')
            except Exception:
                continue
            chat = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/div/div[1]/div[3]/div[1]/a[2]')
            chat.click()
            driver.implicitly_wait(5)
            name = driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div[2]/div[1]/div[1]/p/span[1]').text
            first_name = name[0]
            chat_input = driver.find_element(By.CLASS_NAME, 'chat-input')
            chat_input.send_keys((first_name+'总你好！我对这个岗位很感兴趣，方便聊聊吗？'), Keys.ENTER)
            print('已经沟通')
            Jobs.update({'chated': 1}).where(Jobs.id_job == i.id_job).execute()
            push_count = push_count + 1
            continue

        active_time = driver.find_element(By.CLASS_NAME, 'boss-active-time')

        # chated = Jobs.get_by_id(Jobs.id_job==i.id_job)
        # print('chated=' + str(chated.chated))
        if active_time.get_attribute('textContent') in ['刚刚活跃', '本周活跃', '3日内活跃', '4日内活跃', '2日内活跃'
                                                        '今日活跃']:
            try:
                driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/div/div[1]/div[3]/div[1]/a[2]')
            except Exception:
                continue
            chat = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/div/div[1]/div[3]/div[1]/a[2]')
            chat.click()

            driver.implicitly_wait(5)
            name = driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div[2]/div[1]/div[1]/p/span[1]').text
            first_name = name[0]
            chat_input = driver.find_element(By.CLASS_NAME, 'chat-input')
            chat_input.send_keys((first_name + '总你好！我对这个岗位很感兴趣，方便聊聊吗？'), Keys.ENTER)

            print('已经沟通')
            Jobs.update({'chated': 1}).where(Jobs.id_job == i.id_job).execute()
            push_count = push_count + 1
        else:
            Jobs.update({'active': 0}).where(Jobs.id_job == i.id_job).execute()
        # except Exception:
        #     pass
    print("共推送给了"+str(push_count)+"个HR")

login()
bugUrl()
# bugInfo()
# def imgShotcut():
#     driver.get_screenshot_as_base64()
