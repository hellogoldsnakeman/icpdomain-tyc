#!/usr/bin/env python
# coding: utf-8
# author:hellogoldsnakeman

import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


def get_icpdomain(company_name):
    # 搜索公司
    driver.get(f"https://www.tianyancha.com/search?key={company_name}")
    try:
        # 等待页面中特定元素加载完成，这里根据需要调整目标元素的类名
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "index_alink__zcia5"))
        )

        # 获取完整的页面源代码
        html_content = driver.page_source

        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(html_content, 'html.parser')

        # 查找目标元素，这里根据需要调整目标元素的类名
        link = soup.find('a', class_='index_alink__zcia5 link-click', href=True)

        # 提取数据
        if link:
            result = {
                'text': link.text,
                'href': link['href']
            }
            print(f"{company_name}的详情页url为:{result['href']}")
            time.sleep(random.randint(4, 10))

            # 进入公司详情页
            driver.get(result["href"])
            time.sleep(random.randint(4, 10))
            try:
                # 等待页面加载备案标签
                element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//a[@class='index_down-item__fQ46z' and @at='icp']")))

                # 获取备案详情页
                icp_link = element.get_attribute('href')
                if icp_link:
                    icp_result = {"href": icp_link}
                    # 跳转到备案域名详情页
                    driver.get(icp_result["href"])
                    time.sleep(random.randint(4, 10))

                    # 等待页面加载备案域名的父标签
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-dim='icp']")))

                    # 定位到备案域名div元素
                    div_icp =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-dim='icp']")))
                    # 定位备案域名数量页面，并获取数量
                    icp_sum = div_icp.find_element(By.CLASS_NAME,"dimHeader_nameCount__rowId").text
                    print("备案域名数量为: "+icp_sum)
                    if 0 < int(icp_sum) <= 10:
                        try:
                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-dim='icp']"))).click()
                            time.sleep(random.randint(4, 10))
                            # 定位<div data-dim='icp'>元素
                            div_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-dim='icp']")))
                            # 定位table-wrap元素
                            icpdomains_elements = div_element.find_element(By.CLASS_NAME, "table-wrap")
                            # 定位tr元素
                            tr_elements = icpdomains_elements.find_elements(By.TAG_NAME, "tr")
                            for tr in tr_elements:
                                # 获取tr下所有td元素
                                td_elements = tr.find_elements(By.TAG_NAME, "td")
                                # 如果 td 元素存在，遍历并提取数据
                                if td_elements:
                                    row_data = [td.text.strip() for td in td_elements]  # 获取每个 td 的文本内容
                                    icp_doamin = row_data[4]
                                    print(f"备案域名为:{icp_doamin}")
                                    with open('/Users/tayue/Desktop/icpdomain.txt', 'a+') as f:
                                        f.writelines(company_name+'\t'+icp_doamin+'\n')
                        except Exception as e:
                            print(e)
                            pass

                    elif int(icp_sum) > 10:
                        try:
                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-dim='icp']"))).click()
                            time.sleep(random.randint(4, 10))
                            # 定位<div data-dim='icp'>元素
                            css_div_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-dim='icp']")))
                            table_element = css_div_element.find_element(By.CLASS_NAME, "table-footer")
                            page_elements = table_element.find_elements(By.CLASS_NAME, "num")
                            for page in page_elements:
                                page.click()
                                time.sleep(random.randint(4, 10))
                                div_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-dim='icp']")))
                                # 定位table-wrap元素
                                icpdomains_elements = div_element.find_element(By.CLASS_NAME, "table-wrap")
                                # 定位tr元素
                                tr_elements = icpdomains_elements.find_elements(By.TAG_NAME, "tr")
                                for tr in tr_elements:
                                    # 获取 tr 下所有 td 元素（表格中的列）
                                    td_elements = tr.find_elements(By.TAG_NAME, "td")
                                    # 如果 td 元素存在，遍历并提取数据
                                    if td_elements:
                                        row_data = [td.text.strip() for td in td_elements]  # 获取每个 td 的文本内容
                                        icp_doamin = row_data[4]
                                        print(f"备案域名:{icp_doamin}")
                                        with open('/Users/tayue/Desktop/icpdomain.txt', 'a+') as f:
                                            f.writelines(company_name+'\t'+icp_doamin+'\n')
                        except Exception as e:
                            print(e)
                            pass
                    else:
                        pass
            except Exception as e:
                print(e)
                pass
    except Exception as e:
        print(e)
        input("随便输入什么东西吧: ")
            # 这里为了防止爬取过程中触发反爬需要手动验证，预留一个手动窗口，如果没有这个窗口，完成手工验证后程序就会退出，这里随便输入什么都行


if __name__ == "__main__":
    # 配置Selenium WebDriver，以下两个service路径均需替换为你的ChromeDriver实际路径
    service = Service('/usr/local/bin/chromedriver') 
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')  # 禁用GPU加速，提升兼容性
    options.add_argument('--no-sandbox')  # 针对Linux系统
    options.add_argument('--disable-blink-features=AutomationControlled')  # 防反爬设置
    service = Service(executable_path='/Users/tayue/Documents/work/tools/chromedriver/chromedriver') # 定位chromedriver目录
    driver = webdriver.Chrome(service=service, options=options)


    # 登录网站
    driver.get(f"https://www.tianyancha.com")
    time.sleep(20)
    with open('/Users/tayue/Desktop/company_name.txt','r',encoding='utf-8') as f:
        for company_name in f.readlines():
            company_name = company_name.strip('\n\t\r')
            get_icpdomain(company_name)


