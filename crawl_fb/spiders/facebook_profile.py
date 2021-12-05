import scrapy
from scrapy_splash import SplashRequest
import json
from get_id import get_id



class FacebookSpider(scrapy.Spider):
    name = 'facebook_profile'
    # Lua script to interact with js in the website while crawling
    
    
    script_login = """
        function main(splash, args)
            splash:init_cookies(splash.args.cookies)
                assert(splash:go{
                    splash.args.url,
                    headers=splash.args.headers
                })
            assert(splash:wait(math.random(1, 3)))
            splash:set_viewport_full()      
            assert(splash:go(args.about))
            assert(splash:wait(math.random(1, 3)))

            splash:select("div[class='_86nv _2pin']"):mouse_click()
            assert(splash:wait(math.random(1, 3)))
            splash:set_viewport_full()
            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc(
                "function() {return document.body.scrollHeight;}"
            )

            for _ = 1, """ + str(3) + """ do
                scroll_to(0, get_body_height())
                assert(splash:wait(math.random(2,3)))
            end



            return {
                cookies = splash:get_cookies(),                
                html = splash:html(),
                url = splash:url(),
                acc = args.acc
            }
        end
    """
    
    def start_requests(self):
        #Read link facebook
        f = open("link_user.txt", "r")
        link = str(f.read()).split("\n")
        user_id = get_id(link)

        # This print step is to check whether login is successfull or not base on the HTML return that is written to homepage.html

        with open('./cookies/cookie.json', 'r') as jsonfile:
            cookies = json.load(jsonfile)
        with open('./result/profile/html/profile_' + str(user_id[0]) + '.html', 'w+') as out:
            out.write('')
        with open('./result/profile/profile_' + str(user_id[0]) + '.json', 'w+') as out:
            out.write('')  
            
        # Send splash request with facebook accounnt and lua script to facebook login page to get logged cookie


            
        yield SplashRequest(
                url="https://www.facebook.com/login",
                callback=self.parse,
                session_id="test",
                meta={
                    "splash": {
                        "endpoint": "execute", 
                        "args": {
                            "lua_source": self.script_login,
                            "cookies": cookies,
                            "about": link
                        }
                    }
                }
            )

    def parse(self, response):
        # Store return HTML tags to homepage.html for checking

        
        with open('./result/profile/html/profile.html', 'w+', encoding="utf-8") as out:
            out.write(response.text)


        res = {}
        h = scrapy.Selector(response)
        pro_infos = h.css("div._55wo._2xfb._1kk1")
        res["name"] = h.css("div._6j_d.show ::text").extract_first()
        for info in pro_infos:
            text = info.css("div.__gx ::text").extract_first()
            if (text == "Học vấn"):
                list_studyAt = info.css("div._5cds._2lcw")
                res["studyAt"] = []
                for study in list_studyAt:
                    res["studyAt"].append(study.css(" ::text").extract_first())
                if len(res["studyAt"]) == 0:
                    res["studyAt"] = res["studyAt"][0]
                else:
                    res["studyAt"] = " ; ".join(res["studyAt"])


            elif (text == "Công việc"):
                list_workAt = info.css("div._5cds._2lcw")
                res["workAt"] = []
                for work in list_workAt:
                    res["workAt"].append(work.css(" ::text").extract_first())
                if len(res["workAt"]) == 0:
                    res["workAt"] = res["workAt"][0]
                else:
                    res["workAt"] = " ; ".join(res["workAt"])

            elif (text == "Nơi từng sống"):
                list_liveAt = info.css("div._2swz._2lcw")
                res["liveAt"] = []
                for live in list_liveAt:
                    res["liveAt"].append(live.css("i.img._1-yc.profpic").xpath('@aria-label').extract_first()[:-17])
                if len(res["liveAt"]) == 0:
                    res["liveAt"] = res["liveAt"][0]
                else:
                    res["liveAt"] = " ; ".join(res["liveAt"])                                  

            elif (text == "Thông tin cơ bản"):
                list_profile = info.css("div._5cds._2lcw._5cdu")
                for each in list_profile:
                    temp = each.css("::text").extract()
                    if (temp[1] == "Năm sinh" or temp[1] == "Ngày sinh"):
                        res["dob"] = temp[0]
                    elif (temp[1] == "Giới tính"):
                        res["gender"] = temp[0]


        with open('./result/profile/profile_' + str(user_id[0]) + '.json', 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=4)
    
