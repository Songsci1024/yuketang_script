from selenium import webdriver
import time
import os
import re
from configparser import ConfigParser


class AutoPlay():
    def __init__(self):
        self.filepath = os.getcwd()
        self.driver = webdriver.Chrome(executable_path=self.filepath + r'\chromedriver.exe')  # r表示后面的字符串不转义
        self.id, self.pwd = "", ""
        self.class_list = []
        self.url = "https://www.yuketang.cn/web"
        self.get_user_info()
        self.driver.implicitly_wait(30)  # 隐式等待30s，等待所有文件加载完成

    def get_user_info(self):  # 读取配置文件
        cf = ConfigParser()
        cf.read(self.filepath + r'\config.ini', encoding='utf-8')  # 有中文的话，要加上encoding='utf-8'
        self.id = cf.get('userinfo', 'uid')
        self.pwd = cf.get('userinfo', 'pwd')
        for i in cf.options('classinfo'):
            self.class_list.append(cf.get('classinfo', i))

    def start(self):
        browser = self.driver
        browser.get(self.url)
        browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/img').click()
        browser.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/input').send_keys(self.id)
        browser.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div/input').send_keys(self.pwd)
        browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/div[5]').click()
        browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[1]/div[1]/div/div/div/div[3]').click()

        class_list = browser.find_elements_by_class_name('el-card__body')  # 目前所学的所有课程
        # 存储出需要刷视频的课索引
        target_class_index = [i for i in range(len(class_list)) if
                              class_list[i].find_element_by_tag_name('h1').text in self.class_list]
        print(target_class_index)
        finished_class = 0
        for class_index in target_class_index:
            browser.find_elements_by_class_name('el-card__body')[class_index].click()
            browser.find_elements_by_css_selector('span[class="blue ml20"]')[0].click()  # 展开课程
            video_list = browser.find_elements_by_css_selector(
                'div[class="activity-info el-tooltip"] > span[class="tag"] > svg[class="icon"]')
            # 存储出需要刷的视频索引
            video_list = [i for i in range(len(video_list)) if
                          video_list[i].find_element_by_css_selector('use').get_attribute(
                              'xlink:href') == '#icon-shipin']
            finished_video = 0
            for video_index in video_list:
                browser.find_elements_by_css_selector('div[class="activity-info el-tooltip"]')[video_index].click()
                while True:
                    # #选择二倍速
                    # t = browser.find_element_by_xpath('//*[@id="video-box"]/div/xt-wrap/xt-controls/xt-inner/xt-speedbutton/xt-speedlist/ul/li[1]')

                    # 播放视频
                    button = browser.find_elements_by_xpath(
                        '//*[@id="video-box"]/div/xt-wrap/xt-controls/xt-inner/xt-playbutton')[0]
                    if button.find_element_by_css_selector('.play-btn-tip').get_attribute(
                            'innerText') == '暂停':  # 如果视频是暂停状态，点击播放按钮
                        button.click()
                    finish_monitor = browser.find_element_by_xpath(
                        '//*[@id="app"]/div[2]/div/div[2]/div/div[1]/div[2]/section[1]/div[2]/div/div/span')
                    comp = re.compile('[1-9]\d*|0')
                    finish = comp.findall(finish_monitor.get_attribute('innerText'))[0]
                    if int(finish) > 98:  # 视频播放完成
                        finished_video = finished_video + 1
                        print(f'第{finished_video}个视频已看完')
                        browser.back()  # 返回上一层，即课程列表
                        browser.refresh()  # 刷新页面,避免假死
                        browser.find_elements_by_css_selector('span[class="blue ml20"]')[0].click()  # 展开课程
                        break
                    else:
                        time.sleep(360)  # 等待6分钟
                        browser.refresh()  # 刷新页面
            finished_class = finished_class + 1
            print(f'==============第{finished_class}个课程已看完==============')
            browser.back()
            browser.refresh()
        print('=======================全部课程已看完=======================')


if __name__ == '__main__':
    ap = AutoPlay()
    ap.start()
