import scrapy
from scrapy_splash import SplashRequest
import json
from datetime import datetime
from scrapy.utils.project import get_project_settings
from get_id import get_id
import time 
from datetime import datetime, timedelta
import os
import random as rd





def _convert_to_timestamp(the_input):

    ts = -1

    for each in  ["Hôm qua"]:
        if each in the_input:
            today = datetime.now()

            the_time = the_input.split(" ")[-1].split(":")

            d = datetime(year=today.year, month=today.month, day=today.day, hour=int(the_time[0]), minute=int(the_time[1])) - timedelta(days=1)

            ts = int(time.mktime(d.utctimetuple()))

            return ts
    
    for each in  ["tháng"]:
        if each in the_input:
            if "," in the_input:

                the_time = the_input.split(" ")

                the_hrs_mins = the_time[-1].split(":")

                d = datetime(year=int(the_time[3]), month=int(the_time[2].replace(",","")), day=int(the_time[0]), hour=int(the_hrs_mins[0]), minute=int(the_hrs_mins[1]))

                ts = int(time.mktime(d.utctimetuple()))

                return ts

            else:

                today = datetime.now()

                the_time = the_input.split(" ")

                the_hrs_mins = the_time[-1].split(":")

                d = datetime(year=today.year, month=int(the_time[2].replace(",","")), day=int(the_time[0]), hour=int(the_hrs_mins[0]), minute=int(the_hrs_mins[1]))

                ts = int(time.mktime(d.utctimetuple()))

                return ts
    
    for each in  ["giờ"]:
        if each in the_input:

            today = datetime.now()

            the_time = the_input.split(" ")

            d = datetime(year=today.year, month=today.month, day=today.day, hour=today.hour, minute=today.minute, second=today.second) - timedelta(hours=int(the_time[0]))

            ts = int(time.mktime(d.utctimetuple()))

            return ts
    
    for each in  ["phút"]:
        if each in the_input:

            today = datetime.now()

            the_time = the_input.split(" ")

            d = datetime(year=today.year, month=today.month, day=today.day, hour=today.hour, minute=today.minute, second=today.second) - timedelta(minutes=int(the_time[0]))

            ts = int(time.mktime(d.utctimetuple()))

            return ts
    
    for each in  ["giây"]:
        if each in the_input:

            today = datetime.now()

            the_time = the_input.split(" ")

            d = datetime(year=today.year, month=today.month, day=today.day, hour=today.hour, minute=today.minute, second=today.second) - timedelta(seconds=int(the_time[0]))

            ts = int(time.mktime(d.utctimetuple()))
    
            return ts

class FacebookSpider(scrapy.Spider):
    name = 'facebook_cmt'

    # This will setup settings variable to get constant from settings.py

    settings = get_project_settings()
    xpath_view_all_cmt = "async_elem"
    xpath_view_more_reply = "_2b1h async_elem"
    # Lua script to interact with js in the website while crawling

    
    def start_requests(self):

        script_link = """
                function main(splash, args)
                    splash:init_cookies(splash.args.cookies)
                    assert(splash:go{
                        splash.args.url,
                        headers=splash.args.headers
                    })
                    assert(splash:wait(5))
                    splash:set_viewport_full()
                    local scroll_to = splash:jsfunc("window.scrollTo")
                    local get_body_height = splash:jsfunc(
                        "function() {return document.body.scrollHeight;}"
                    )
                    for _ = 1, 2 do
                        scroll_to(0, get_body_height())
                        assert(splash:wait(1))
                    end 
                    
                    assert(splash:wait(5))

                    local all_cmt = splash:select("div[class='""" + self.xpath_view_all_cmt + """']")
                        if all_cmt ~= nil then
                            assert(all_cmt:mouse_click())
                            assert(splash:wait(5))
                        end

                    
                    local divs = splash:select_all("div[class='""" + self.xpath_view_more_reply + """']")
                    for _, _ in ipairs(divs) do
                        local _div = splash:select("div[class='""" + self.xpath_view_more_reply + """']")
                        if _div ~= nil then
                            assert(_div:mouse_click())
                            assert(splash:wait(3))
                        end
                    end
                    
                    
                    local entries = splash:history()
                    local last_response = entries[#entries].response

                    return {
                        cookies = splash:get_cookies(),
                        headers = last_response.headers,
                        html = splash:html(),
                        url = splash.url()
                    }
                end
            """


        # Send splash request with facebook cookie and lua script to check if cookie is logged in or not
        with open('./cookies/cookie.json', 'r') as jsonfile:
            cookies = json.load(jsonfile)

        with open('./result/cmt/html/cmt.html', 'w+') as out:
            out.write('')

        yield SplashRequest(
            url="https://m.facebook.com/groups/236713123651143/permalink/854487381873711/?m_entstream_source=group",
            callback=self.parse,
            session_id="test",
            meta={
                "splash": {
                    "endpoint": "execute", 
                    "args": {
                        "lua_source": script_link,
                        "cookies": cookies,
                    }
                }
            }
        )


    def parse(self, response):
        with open('./result/cmt/html/cmt.html', 'w+',encoding='utf-8') as out:
            out.write(response.text)
        
        h = scrapy.Selector(response)
        all_cmt = h.css("div._14v5")

        res = []
        for cmt in all_cmt:
            item = {}
            item['post_message'] = cmt.css("div._2b06 div[data-sigil*=comment-body] ::text").extract()
            res.append(item)

        with open('./result/cmt/cmt.json', 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=4)
                
        # result = {}
        # result['id'] = 1
        # res = {}
        # res['group_id'] = group_id[0]
        # res['post'] = []
        # for post in post_info:
        #     item = {}
        #     item['post_id'] = post.css("div._52jc._5qc4._78cz._24u0._36xo a::attr(href)").extract_first()


        #     post_user_id = str(post.css("h3._52jd._52jb._52jg._5qc3._4vc-._3rc4._4vc- strong a::attr(href)").extract_first())
        #     if post_user_id == "None":
        #         post_user_id = str(post.css("h3._52jd._52jb._52jh._5qc3._4vc-._3rc4._4vc- strong a::attr(href)").extract_first())
        #     # item['post_user_id'] = 'https://m.facebook.com' + post_user_id
        #     item['post_user_id'] =  str(post_user_id).split("?")[0].split("/")[-1]
        #     if item['post_user_id'] == 'profile.php':
        #         item['post_user_id'] = str(post_user_id).split("&")[0].split("?")[-1][3:] 

        #     item["timestamp"] = _convert_to_timestamp(post.css("div._52jc._5qc4._78cz._24u0._36xo ::text").extract_first())
        #     item["message"] = " ".join(post.css("div._5rgt._5nk5._5msi ::text").extract())

        #     temp = post.css("i.img._5sgi.img._2sxw._4s0y").xpath("@style").extract()
        #     img_link = []
        #     if len(temp) > 0:
        #         for t in temp:
        #             t = t.replace('\\3d ','=').replace('\\26 ','&').replace('\\3a ', ':')
        #             t = 'https://' + t.split('https://')[1].split("\')")[0]
        #             img_link.append(t)
    
        #     item["post_image_link"] = img_link


        #     item["post_image_alt"] = (post.css("i.img._5sgi.img._2sxw._4s0y").xpath("@aria-label").extract())


        #     post_total_reactions= post.css("div._1g06 ::text").extract()
        #     if len(post_total_reactions) == 0:
        #         item["post_total_reactions"] = 0
        #     else:
        #         item["post_total_reactions"] = int(post_total_reactions[0])

        #     comments_and_shares = post.css("div._1fnt ::text").extract()
            
        #     if len(comments_and_shares) > 0:

        #         item["post_total_comments"] = int((comments_and_shares[0].split(" "))[0])
            
        #     else:

        #         item["post_total_comments"] = 0
            
        #     if len(comments_and_shares) > 1:
                
        #         item["post_total_shares"] = int((comments_and_shares[1].split(" "))[0])

        #     else:

        #         item["post_total_shares"] = 0
        #     res['post'].append(item)

        # result['detail'] = res

        # with open('./result/group/group_' + str(group_id[0]) + '.json', 'w', encoding='utf-8') as f:
        #     json.dump(result, f, ensure_ascii=False, indent=4)


