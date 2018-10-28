# ⭐Instagram_Spider
爬取ins图片、评论数、点赞数、文章内容

### js加密破解
```
要想获取下一页json格式的数据，headers就必须带上X-Instagram-GIS这个参数，否则会403
获取步骤：
  1. 从用户首页https://www.instagram.com/instagram/获取user_id、rhx_gis、end_cursor参数
  2. variables = '{"id":"' + id + '","first":12,"after":"' + end_cursor + '"}'，对params = rhx_gis + ":" + variables进行md5加密
  3. headers加入"x-instagram-gis": params,即可进行抓取
```

### 数据格式如下：
```
{
  "img_url": "https://scontent-ams3-1.cdninstagram.com/vp/2cce52ebd5d0b51ceb172b7517bd824d/5C6EBBD0/t51.2885- 15/e35/43984406_283934812453381_1088198781644886302_n.jpg", 
  "comment_count": 3718, 
  "like_count": 354345, 
  "text": "Photo by @birduyen \u201cMy work has a very warm and calm atmosphere,\u201d says Theresa \u201cT\u201d Le (@birduyen), \u201clike when the sunlight is on your face in the morning, while the birds are softly chirping. I say that because I wouldn\u2019t describe my art as striking or dynamic. Rather, I aim to create a peaceful and soft feeling.\u201d A recent university graduate with a degree in statistics, T is taking part in #Inktober, an annual drawing challenge where artists all over the world create one ink each day of October. \u201cIt\u2019s so inspiring to see all the different techniques and art styles that are showcased,\u201d she explains. \u201cI really wanted to be a part of that community, so I\u2019m trying my best to be consistent, but also experimenting and having fun with my art during this spooky time of the year.\u201d Check out today's story to see more of T's spooky and soothing art."
  }
```

