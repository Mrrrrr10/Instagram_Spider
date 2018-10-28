# 爬取ins图片、评论数、点赞数、文章内容

import re
import json
import hashlib
import requests


class Spider(object):
    def __init__(self):
        self.HTTP_PROXY = {
            "http": "127.0.0.1:8123",
            "https": "127.0.0.1:8123",
        }
        self.home_url = "https://www.instagram.com/instagram/"
        self.base_url = "https://www.instagram.com/graphql/query/?query_hash=5b0222df65d7f6659c9b82246780caa7&variables=%7B\"id\"%3A\"{id}\"%2C\"first\"%3A12%2C\"after\"%3A\"{end_cursor}\"%7D"
        self.data_list = []
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip,deflate,br",
            "accept-language": "zh-CN,zh;q=0.9",
        }

    def run(self):
        html = requests.get(url=self.home_url, headers=self.headers, proxies=self.HTTP_PROXY).text
        print(html)
        pattern = re.compile('edge_owner_to_timeline_media":(.*?),"edge_saved_media"')
        text_json = json.loads(pattern.search(html).group(1))
        user_id = re.findall('"profilePage_([0-9]+)"', html, re.S)[0]
        GIS_rhx_gis = re.findall('"rhx_gis":"([0-9a-z]+)"', html, re.S)[0]
        self.parse_json(text_json, user_id, GIS_rhx_gis)

    def parse_json(self, text_json, id, gis):
        try:
            data = text_json.get('data')
            if data:
                data = data.get('user').get('edge_owner_to_timeline_media')
                has_next_page = data.get('page_info').get('has_next_page')
                end_cursor = data.get('page_info').get('end_cursor')
                edges = data.get('edges')
            else:
                has_next_page = text_json.get('page_info').get('has_next_page')
                end_cursor = text_json.get('page_info').get('end_cursor')
                edges = text_json.get("edges")
            if has_next_page:
                if text_json:
                    if edges:
                        for edge in edges:
                            node = edge.get('node')
                            img_url = node.get('display_url')
                            comment_count = node.get('edge_media_to_comment').get('count')
                            edge_liked_by = node.get('edge_liked_by')
                            edge_media_preview_like = node.get('edge_media_preview_like')
                            like_count = edge_liked_by.get(
                                'count') if edge_liked_by else edge_media_preview_like.get('count')
                            text = node.get('edge_media_to_caption').get('edges')[0].get('node').get('text')
                            json_format = {
                                "img_url": img_url,
                                "comment_count": comment_count,
                                "like_count": like_count,
                                "text": text
                            }
                            self.data_list.append(json_format)
                            print(json_format)

                url = self.base_url.format(id=id, end_cursor=end_cursor)
                variables = '{"id":"' + id + '","first":12,"after":"' + end_cursor + '"}'
                params = self.get_x_instagram_gis(gis + ":" + variables)
                self.request_url(url, params, id, gis)

            with open('instagram.json', 'a', encoding='utf-8') as f:
                json.dump(self.data_list, f)

        except Exception as e:
            print(e)

    def get_x_instagram_gis(self, params):
        h = hashlib.md5()
        h.update(params.encode("utf-8"))
        return h.hexdigest()

    def request_url(self, url, params, id, gis):
        self.headers.update({
            "referer": "https://www.instagram.com/instagram/",
            "x-instagram-gis": params,
            "x-requested-with": "XMLHttpRequest",
            "accept": "*/*",
        })
        text_json = requests.get(url, headers=self.headers, proxies=self.HTTP_PROXY).json()
        self.parse_json(text_json, id, gis)


if __name__ == '__main__':
    spider = Spider()
    spider.run()
