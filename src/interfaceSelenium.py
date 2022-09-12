from selenium import webdriver
import time
from bs4 import BeautifulSoup
from configure import configure


class InterfaceSelenium:
    """Class for working with Selenium"""
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(
        executable_path='B:/MonitoringResource54e/driver/chromedriver.exe',
        options=options)
    url = configure.url_vcloud

    @classmethod
    def vcloud_connections(cls):
        """Connections"""
        cls.driver.get(cls.url)

        username_input = cls.driver.find_element_by_id('usernameInput')
        username_input.clear()
        username_input.send_keys(configure.name_user_vcloud)
        cls.sleep5()

        password_input = cls.driver.find_element_by_id('passwordInput')
        password_input.clear()
        password_input.send_keys(configure.password_vcloud)

        button_login = cls.driver.find_element_by_id('loginButton')
        button_login.click()
        cls.sleep5()
        cls.driver.get(f'{configure.url_vcloud}cloud/orgvdcs')
        cls.sleep10()

    @classmethod
    def get_dict_ord_vdc_url(cls) -> dict:
        """Returns a dictionary with all VDC clients and references to them"""
        url_dict = {}
        while True:

            items = cls.driver.find_elements_by_class_name('d-block')

            for i in items:
                name_vdc = i.text
                url_vdc = i.get_attribute('href')
                if url_vdc is not None:
                    url_dict[name_vdc] = url_vdc
            cls.sleep10()
            button_paginator = cls.driver.find_element_by_class_name('pagination-next')
            if button_paginator.is_enabled():
                button_paginator.click()
                time.sleep(10)
            else:
                break
        print(url_dict)
        return url_dict

    @classmethod
    def get_data_cpu_quota(cls, data_cpu):
        """Returns the allocated CPU"""
        data_cpu = data_cpu.split()
        if len(data_cpu) == 1:
            cpu_quota = data_cpu[0]
            return cpu_quota
        else:
            cpu_quota = data_cpu[3]
            return cpu_quota

    @classmethod
    def get_data_cpu_used(cls, data_cpu):
        """Returns the number of CPU used"""
        data_cpu = data_cpu.split()
        cpu_used = data_cpu[0]
        return cpu_used

    @classmethod
    def get_data_memory_quota(cls, data_memory):
        """Returns the number of allocated Memory"""
        data_memory = data_memory.split()
        if len(data_memory) == 1:
            memory_quota = data_memory[0]
            return memory_quota
        else:
            memory_quota = data_memory[3]
            return memory_quota

    @classmethod
    def get_data_memory_used(cls, data_memory):
        """Returns the number of Memory used"""
        data_memory = data_memory.split()
        memory_used = data_memory[0]
        return memory_used

    @classmethod
    def sleep5(cls):
        time.sleep(5)

    @classmethod
    def sleep10(cls):
        time.sleep(10)

    @classmethod
    def close_connection(cls):
        """Closing the connection"""
        cls.driver.close()
        cls.driver.quit()

    @classmethod
    def go_to_storage(cls):
        """go to the tab with disk policies"""
        button_storage = cls.driver.find_element_by_link_text('Storage')
        button_storage.click()
        cls.sleep5()

    @classmethod
    def count_policy(cls, data_storage):
        """Returns the number of policies"""
        count_policy = 0
        for item in data_storage:
            if 'GB' in item.text or 'Unlimited' in item.text:
                count_policy = count_policy + 1
        return count_policy/2

    @classmethod
    def get_list_resource_vdces(cls, url_dict):
        """Returns a list containing dictionaries with an indication of all resources"""
        list_data = []
        for name_user_vdc, url_user_vdc in url_dict.items():
            cls.driver.get(url_user_vdc)
            cls.sleep10()
            list_object = cls.driver.find_elements_by_class_name('stack-block-content')
            cls.sleep5()

            data_cpu = list_object[6].text
            data_memory = list_object[7].text

            cls.go_to_storage()

            html = cls.driver.page_source
            soup = BeautifulSoup(html, features="lxml")
            data_storage = soup.find_all(class_="datagrid-cell")

            cpu_used = cls.get_data_cpu_used(data_cpu).replace('.', ',')
            cpu_quota = cls.get_data_cpu_quota(data_cpu).replace('.', ',')
            memory_used = cls.get_data_memory_used(data_memory).replace('.', ',')
            memory_quota = cls.get_data_memory_quota(data_memory).replace('.', ',')

            data = {
                'Name_VDC': name_user_vdc,
                'CPU_Used': cpu_used,
                'CPU_Quota': cpu_quota,
                'Memory_Used': memory_used,
                'Memory_Quota': memory_quota,

            }
            i = 0
            dict_policy = {}

            for item in data_storage:
                name_policy = data_storage[2 + i].text
                quota_policy = data_storage[5 + i].text.split()[0].replace('.', ',')
                used_policy = data_storage[6 + i].text.split()[0].replace('.', ',')

                data[f"{name_policy} used"] = used_policy
                data[f"{name_policy} quota"] = quota_policy
                dict_policy[f"{name_policy} used"] = used_policy

                if len(dict_policy) == cls.count_policy(data_storage):
                    break
                i = i + 8

            cls.sleep5()
            list_data.append(data)

        return list_data

