# PixivNcat  

## 关于
#### NcatBot 插件,提供Pixiv爬虫工具，并可通过多种条件发送图片,爬虫工具来自 [pixivtools](https://github.com/aliubo/pixivtools)  

## 功能

- **Pixiv 爬虫** 
  - 按照artwork id下载图片
  - 按照画师id(userid)下载图片
  - 按照pixivision id下载图片(pixvision站)
  - 按照关注的画师最新上传下载图片
  - 按照首页推荐的作品下载图片
  - 按照排行榜下载图片
  - 按照接稿的推荐作品下载图片
  - 按照用户的收藏下载图片
  - 按照指定标签的热门作品下载图片
  - 按照指定的artwork id的相似作品下载图片
  - 按照指定的画师id的所有相似画师下载图片
  - 按照平台推荐的画师下载图片
  - 按照接稿的最新接稿画师下载图片  
  - 详细配置参考：[pixivtools](https://github.com/aliubo/pixivtools)
- **随机发图**
  - 从配置图库随机发送一张图片(目前只支持本地图库)
  - 对每个群聊单独记录抽取图片记录，避免重复

## 安装

1. 将 PixivNcat 插件文件夹放置在 `ncatbot/plugins` 目录下
2. 在 `ncatbot/plugins/PixivNcat` 目录下存在以下配置文件：
   - `config.yaml`：管理员id配置信息
   - `main.py` ：插件主入口,配置图库路径
   - `PixivCrawler_by_rank.py`：自定义Pixiv爬虫配置脚本
   - `PixivCrawler_by_pid.py`：根据Pid爬取作品配置脚本


## 配置

### Config.yaml
在 `./config.yaml` 文件中配置:
```yaml
# 配置管理员QQ  例如 manager_id: 1234567890
manager_id: 

# 代理地址https/http，修改为你的代理地址
proxy: "127.0.0.1:10809"

# Replace YOUR_PHPSESSID with your actual PHPSESSID from pixiv
phpsessid: ""
```
Phpsessid获取方法见  ：[PHPSESSID](https://zhuzemin.github.io/pixiv_sort_by_popularity/)

### main.py
插件主操作,配置图库路径

`img_RankType` : 随机涩图需要的图库目录名称后缀，默认和排行榜爬虫文件中全局类型一致，或者根据自己的文件路径修改，如果修改了images_path可忽略此项
```python
# 随机涩图需要的图库，默认和排行榜爬虫文件中全局类型一致，或者根据自己的文件路径修改
# 例如 img_RankType = 'weekly' 如果修改了images_path可忽略此项
img_RankType = global_RankType
# img_RankType = "custom"
```
`images_path` : 使用绝对路径，随机涩图需要的图库路径

`images_pid_path` ：使用绝对路径，pid爬取图片保存路径

`global_config_yaml` ： 全局配置文件路径，不建议修改

#### 使用Pid爬取并发送图片时，暂时不会R18图片做发送操作，如果在`PixivCrawler_by_pid.py` 设置了全局作品配置为仅爬取非R18，图片不会下载

### PixivCrawler_by_rank.py
该文件为配置自定义 Pixiv 爬虫，支持多种方式爬取  

`global_RankType` : 爬取排行榜类型,和下载文件夹名称有关，当使用其他爬取时可自定义，如果修改输出目录了可忽略此项
```python
global_RankType = "monthly" # 如果使用排行榜爬虫从下列参数中选择,和下载文件夹名称有关，非排行榜可自定义
'''
    'daily'  # 日榜
    'weekly'  # 周榜
    'monthly'  # 月榜
    "rookie"  # 新人榜
    "original"  # 原创榜
    "daily_ai"  # 日榜-ai
    "male"  # 男性喜爱
    "female"  # 女性喜爱

    'daily_r18'
    'weekly_r18'
    'r18g'
    "daily_r18_ai"
    "male_r18"
    "female_r18"
'''
```
`global_page_num` : 需要下载多少页，默认为只下载第一页

`global_data`  : 榜单统计结束时间  日期，格式为YYYYMMDD  

`global_options` : 全局作品过滤设置，参考：[pixivtools](https://github.com/aliubo/pixivtools)
```python
global_options = pixiv_api.ArtworkOptions(   # 全局作品过滤设置，参考： https://github.com/aliubo/pixivtools
    update=False,       # update: bool, 是否更新已存在的artwork
    only_r18=False,     # only_r18: bool, 是否只爬取R18
    only_non_r18=True,  # only_non_r18: bool, 是否只爬取非R18
    skip_manga=True,    # skip_manga: bool, 是否跳过漫画
    artwork_types=0,    # artwork_types: list[ArtworkType], 只爬取指定类型的artwork # ILLUST = 0 插画  # MANGA = 1 漫画 # UGORIA = 2 动图
    ignore_error=True    # ignore_error: bool, 是否忽略爬取过程中的某个artwork出错，如果为False则会在出错时直接raise
)
```
`global_set_img_dir`  :  全局作品保存路径，默认将根据`global_RankType`自动生成，若进行自定义要使用绝对路径

`global_set_log_file`  :  全局Log文件保存路径，若进行自定义要使用绝对路径

`global_set_sql_url` :   全局DB文件保存路径，若进行自定义要使用绝对路径

`global_config_yaml`  :  全局配置文件路径，不建议修改

#### 运行该文件,当`global_page_num`大于1时，启用等待，避免触发Pixiv流控限制：
```python
    # Pixiv 疑似于 2022 年 8 月 15 日左右调整了流控策略，与以往的几乎不限制 API 请求频率不同，只要一次性批量获取的作品过多，就可能受到流控限制，具体表现为：

    # 判定区间短：只要在短时间（1~2分钟内）内请求数量超过三位数，就容易触发该流控限制
    # 限制时间短：只要停止请求 1~2分钟，限制自动解除
    # 
    i = 0
    if global_page_num > 1:
        set_sleep = True
    while i < global_page_num:
        run_constructor_rank(i+1) 
        i += 1
        if set_sleep:
            time.sleep(120)  # 等待2分钟   
```
### PixivCrawler_by_pid.py
该文件为根据Pid 爬取Pixiv作品,当群聊输入/pixiv+空格+pid+空格+`pid`，插件会自动调用  

`global_options` : 全局作品过滤设置，同上

`global_set_img_dir`  :  同上

`global_set_log_file`  :  同上

`global_set_sql_url` :   同上

`global_config_yaml`  :  同上,建议不修改
## 使用
- **群聊使用**
  - 启动 Ncatbot。 

  - 配置管理员id后，发送 `测试PixivBot` 消息以测试插件是否正常工作。 

  - 输入 `/pixiv 随机涩图` 或者直接输入 随机涩图 ，bot会从配置图库自动发送随机图片。

  - 输入 /pixiv pid `pid` ，bot会自动下载并发送图片。 例： `/pixiv pid 129105117`  

  - 输入 `/pixiv help` 或者`/pixiv 帮助`，bot会自动发送帮助信息。

  - 配置管理员id后，发送 `关闭PixivBot` ，bot会关闭。

  - 配置管理员id后，发送 `开启PixivBot` ，bot会开启(启动插件默认为开启)。

- **爬虫使用**
  - 配置 `PixivCrawler_by_rank.py` 和 `PixivCrawler_by_pid.py`
  - 运行 `PixivCrawler_by_rank.py` 来爬取图片
    ```shell
      python PixivCrawler_by_rank.py
    ```
  - 在输出目录查看下载图片
## 文档
- [main.py](./main.py)： 插件主操作,配置图库路径

- [PixivCrawler_by_rank.py](./PixivCrawler_by_rank.py)： 配置自定义 Pixiv 爬虫

- [PixivCrawler_by_pid](./PixivCrawler_by_rank.py)： 配置按照Pid爬取文件

- [pixivtools](https://github.com/aliubo/pixivtools)： Pixiv 爬虫的详细说明
