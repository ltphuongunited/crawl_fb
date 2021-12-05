# crawl_fb
1. File chromedriver.exe for Windows 10
2. File get_id.py use Selenium to get id fb
3. Run docker:
```
docker pull scrapinghub/splash
```

```
docker run -p 8050:8050 scrapinghub/splash
```

4. Login to get cookies
```
scrapy crawl facebook_login
```

5. Crawl profile: Link user in "link_user.txt"
```
scrapy crawl facebook_profile
```
Output in result folder: 
![Profile](https://github.com/ltphuongunited/crawl_fb/tree/main/readme_images/profile.png)

6. Crawl group: Link group in "link_group.txt"
```
scrapy crawl facebook_group
```
Output in result folder: 
![Group](https://github.com/ltphuongunited/crawl_fb/tree/main/readme_images/group.png)
