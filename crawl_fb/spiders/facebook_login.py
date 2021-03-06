import scrapy
from scrapy.utils.project import get_project_settings
from scrapy_splash import SplashRequest
import json

class FacebookSpider(scrapy.Spider):

    # This name will be use to call the crawling spider, for example: scrapy crawl facebook_login

    name = 'facebook_login'

    # This will setup settings variable to get constant from settings.py

    settings = get_project_settings()

    # Lua script to interact with js in the website while crawling

    script_login = """
        function main(splash, args)
            assert(splash:go{
                splash.args.url,
                headers=splash.args.headers
            })
            function focus(sel)
                splash:select(sel):focus()
            end
  
            focus('input[name=email]')   
            splash:send_text(args.acc)
            assert(splash:wait(math.random(0,1)))
            focus('input[name=pass]')
            splash:send_text(args.pwd)
            assert(splash:wait(math.random(0,1)))
            splash:select('button[name=login]'):mouse_click()
            assert(splash:wait(math.random(4,6)))
            assert(splash:go("https://www.facebook.com/pler.united"))
            assert(splash:wait(math.random(1, 3)))
            return {
                cookies = splash:get_cookies(),
                html = splash:html(),
                acc = args.acc
            }
        end
    """
    
    def start_requests(self):

        # This print step is to check whether login is successfull or not base on the HTML return that is written to homepage.html

        with open('./result/homepage/html/homepage.html', 'w+') as out:
            out.write('')

        # Get Facebook Account from settings.py

        acc = self.settings.get("FACEBOOK_ACCOUNT")[0]

        # Send splash request with facebook accounnt and lua script to facebook login page to get logged cookie

        yield SplashRequest(
                url="https://www.facebook.com/login",
                callback=self.parse_login,
                session_id="test",
                meta={
                    "splash": {
                        "endpoint": "execute", 
                        "args": {
                            "lua_source": self.script_login,
                            "acc": acc["account"],
                            "pwd": acc["password"]
                        }
                    }
                }
            )

    def parse_login(self, response):

        # Store return HTML tags to homepage.html for checking

        with open('./result/homepage/html/homepage.html', 'w+', encoding="utf-8") as out:
            out.write(response.text)

        # Store cookie to json file

        with open("./cookies/cookie.json", 'w+') as jsonfile:
            json.dump(response.data['cookies'], jsonfile, ensure_ascii=False)