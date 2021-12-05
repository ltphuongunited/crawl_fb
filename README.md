# crawl_fb
1. File chromedriver.exe for Windows 10
2. Run docker:
```
docker pull scrapinghub/splash
```

```
docker run -p 8050:8050 scrapinghub/splash
```

3. Login to get cookies
```
scrapy crawl facebook_login
```

4. Crawl profile: Link user in "link_user.txt"
```
scrapy crawl facebook_profile
```
Output in result folder: 
![](./readme_img/profile.png)

5. Crawl group: Link group in "link_group.txt"
```
scrapy crawl facebook_group
```
Output in result folder: 
![](./readme_img/group.png)
