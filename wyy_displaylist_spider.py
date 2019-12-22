import requests,json
from lxml import etree

class WangYi_Music_Spider(object):

    def __init__(self):
        self.start_url = 'https://music.163.com/discover/playlist'
        self.net_domain = 'https://music.163.com'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
            'referer': 'https://music.163.com/'
            }
        self.data_dict = {}


    def get_all_class_url(self):
        #  请求网页
        res = requests.get(self.start_url,headers=self.headers)
        # print(res.content.decode())
        items = {}
        #  获取网页标签元素
        html_object_list = etree.HTML(res.content).xpath('//div[@id="cateListBox"]//dd/a[@class="s-fc1 "]')
        #  取出全部分类和对应的网址
        for temp in html_object_list:
            items[temp.xpath('./text()')[0]] = temp.xpath('./@href')[0]
        return items

    def playlist_next_page(self,url):
        items = {}
        res = requests.get(url,headers=self.headers)
        #  获取html的list
        html_object_list = etree.HTML(res.content).xpath('//ul[@id="m-pl-container"]/li')
        #  获取清单对应的网址
        for temp_html_object in html_object_list:
            items[temp_html_object.xpath('.//a[@class="tit f-thide s-fc0"]/text()')[0]] = temp_html_object.xpath('.//a[@class="tit f-thide s-fc0"]/@href')[0]

        #  获取下一页网址，并判断是否是最后一页
        next_page_url = etree.HTML(res.content).xpath('//div[@class="u-page"]//a[contains(text(),"下一页")]/@href')[0]
        for x in self.data_dict.keys():
            self.data_dict[x].update(items)
            print('-' * 100)
            print(len(self.data_dict[x]))
        if next_page_url.find('discover') != -1:
            return self.playlist_next_page(self.net_domain + next_page_url)
        else:
            return None


    def save_data(self,data):
        with open('./wyy.json','w',encoding='utf-8') as f:
            f.write(json.dumps(data,ensure_ascii=False,indent=2))


    def get_class_palylist(self):
        all_class_playlist_dict = self.get_all_class_url()
        play_dict_items = all_class_playlist_dict.items()
        for temp in play_dict_items:
            #  清空中间字典，self.data_dict主要是起到中转的作用
            self.data_dict = {}
            self.data_dict[temp[0]] = {}
            print('?' * 100)
            print(all_class_playlist_dict)
            self.playlist_next_page(self.net_domain + temp[1])
            all_class_playlist_dict[temp[0]] = self.data_dict
        #  保存数据
        self.save_data(all_class_playlist_dict)


    def run(self):
        #  获取网址
        #  访问网址
        #  提取数据
        #  保存数据
        pass


if __name__ == '__main__':
    wyy = WangYi_Music_Spider()
    wyy.get_class_palylist()