
import requests, json, base64, hashlib


def pngjpg2base64(fh):
    #最大不能超过2M，支持JPG,PNG格式
    with open(fh,"rb") as f:
        base64_data = base64.b64encode(f.read())
        #print (base64_data)
    return str(base64_data,'utf-8')

def md5sum(fh):
    file = open(fh, "rb")
    md = hashlib.md5()
    md.update(file.read())
    md5value = md.hexdigest()
    return md5value

def robot_send_image(robot_url,image_path):
    base64_data = pngjpg2base64(image_path)
    md5value = md5sum(image_path)
    url = robot_url
    headers = {"Content-Type": "text/plain"}
    data = {
    "msgtype": "image",
    "image": {
        "base64": base64_data,
        "md5": md5value
        }
    }
    r = requests.post(url, headers=headers, json=data)
    print(r.text)


def robot_text_message(robot_url,message,who):
   headers = {"Content-Type": "text/plain"}
   #message="写啥:{}".format(str(message))
   data = {
      "msgtype": "text",
      "text": {"content": message, "mentioned_list": who}
   }


   ret = requests.post(
      url=robot_url, 
         # 此处为新建机器人以后生成的链接
      headers=headers, 
      json=data
   )
   print(ret.text)  # 成功后的打印结果：{"errcode":0,"errmsg":"ok"}


def robot_markdown_message(robot_url,message):
   headers = {"Content-Type": "text/plain"}
   #message="写啥:{}".format(str(message))
   data = {
      "msgtype": "markdown",
      "markdown": {"content": message}
   }


   ret = requests.post(
      url=robot_url, 
         # 此处为新建机器人以后生成的链接
      headers=headers, 
      json=data
   )
   print(ret.text)  # 成功后的打印结果：{"errcode":0,"errmsg":"ok"}
 


def robot_image_text(robot_url,title,description,image_url):
   headers = {"Content-Type": "text/plain"}
   #message="写啥:{}".format(str(message))
   data = {
      "msgtype": "news",
      "news": {       "articles" : [
           {
               "title" : title,
               "description" : description,
               "url" : "URL",
               "picurl" : image_url
           }
        ]
    }
   }


   ret = requests.post(
      url=robot_url, 
         # 此处为新建机器人以后生成的链接
      headers=headers, 
      json=data
   )
   print(ret.text)  # 成功后的打印结果：{"errcode":0,"errmsg":"ok"}



if __name__ == '__main__':


    text_message=r"测试:requests.post"
    at_who=["@all","Administrator"]  #["@all","名字"]
    robot_url=r"xxx"
    #发送文本信息
    #robot_text_message(robot_url,text_message,at_who)


    #发送 markdown 信息
    markdown=r'''
实时信息:<font color=\"warning\">markdown信息可以控制颜色</font>，请相关同事注意。
# 标题一
## 标题二
### 标题三
#### 标题四
##### 标题五
###### 标题六
>引用形式
<font color="info">绿色</font>
<font color="comment">灰色</font>
<font color="warning">橙红色</font>'''
    #robot_markdown_message(robot_url,markdown)


    #发送本地图片
    image_path=r"F:\test.jpg"
    #robot_send_image(robot_url,image_path)


    #发送网络图片+部分问题
    title = "标题内容：中秋节快乐"
    #128字节 大概63字中文
    description = "描述内容：中秋节图片一张，开心每一天"
    #512字节 大概126字中文
    #一个汉字占2字节,一个英文字母占1个字节
    image_url = "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
    #网络图片支持png,jpg
    robot_image_text(robot_url,title,description,image_url)
#
