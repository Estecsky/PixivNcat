import sys
import os
sys.path.append((os.path.dirname(__file__)))
from pixivtools import pixiv_api
import pixivtools
from get_RankType import get_rank_type
import yaml
import time
global_RankType = "user" # 如果使用排行榜爬虫从下列参数中选择,和下载文件夹名称有关，非排行榜可自定义
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
global_page_num = 1 # 需要下载多少页，默认为只下载第一页

global_data = 20250411 # 榜单统计结束时间  日期，格式为YYYYMMDD

global_options = pixiv_api.ArtworkOptions(   # 全局作品过滤设置，参考： https://github.com/aliubo/pixivtools
    update=False,       # update: bool, 是否更新已存在的artwork
    only_r18=False,     # only_r18: bool, 是否只爬取R18
    only_non_r18=True,  # only_non_r18: bool, 是否只爬取非R18
    skip_manga=True,    # skip_manga: bool, 是否跳过漫画
    artwork_types=0,    # artwork_types: list[ArtworkType], 只爬取指定类型的artwork     ILLUST = 0  # 插画  MANGA = 1  # 漫画 UGORIA = 2  # 动图
    ignore_error=True    # ignore_error: bool, 是否忽略爬取过程中的某个artwork出错，如果为False则会在出错时直接raise
)

global_set_img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),"Pixiv_out",f"images_{global_RankType}")
global_set_log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),"Pixiv_out","out.log")
global_set_sql_url = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),"pixiv.db")
global_config_yaml = os.path.join(os.path.dirname(__file__),"config.yaml")
set_sleep = False
def get_config():
    global global_RankType
    with open(global_config_yaml, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    # Create config using constructor
    cfg_maker = pixivtools.pixiv_config_maker()
    # Replace YOUR_PHPSESSID with your actual PHPSESSID from pixiv
    cfg_maker.set_phpsessid(config_data["phpsessid"])
    cfg_maker.set_proxy(config_data["proxy"])
    cfg_maker.set_img_dir(global_set_img_dir)
    cfg_maker.set_log_file(global_set_log_file)
    cfg_maker.set_sql_url(f"sqlite:///{global_set_sql_url}")  # other db url see ./config.yaml or https://docs.sqlalchemy.org/en/20/core/engines.html
    return cfg_maker()

def run_constructor_rank(page = 1):
    global global_RankType
    global global_data
    global global_options
    """Example: Using constructor to create crawler"""    # Create service and crawler
    cfg = get_config()
    service = pixivtools.new_pixiv_service(cfg)
    crawler = service.crawler()
    
    # Example crawling tasks
    # 1. Get artwork by ID
    # crawler.get_by_artwork_id(98538269)
    
    # # 2. Get latest artworks from followed artists (page 1)
    # crawler.get_by_follow_latest(1)
    
    # # 3. Get artworks from specific user
    # crawler.get_by_user_id(user_id=3428351,options=global_options)
    
    # # 4. Get popular artworks with tag
    # crawler.get_by_tag_popular("ホロライブ")
    # crawler.get_by_rank(pixivtools.RankType.MALE, 20250313, 1)
    # crawler.get_by_rank(rank_type=get_rank_type(global_RankType),date=global_data,page=page,options=global_options)

    # 5. # 根据我的账号获取关注用户的最新的artwork
    crawler.get_by_follow_latest(page,options=global_options)

def run_constructor_user(uid):
    global global_RankType
    global global_data
    global global_options
    """Example: Using constructor to create crawler"""    # Create service and crawler
    cfg = get_config()
    service = pixivtools.new_pixiv_service(cfg)
    crawler = service.crawler()
    
    # Example crawling tasks
    # 1. Get artwork by ID
    # crawler.get_by_artwork_id(98538269)
    
    # # 2. Get latest artworks from followed artists (page 1)
    # crawler.get_by_follow_latest(1)
    
    # # 3. Get artworks from specific user
    crawler.get_by_user_id(user_id=uid,options=global_options)


if __name__ == "__main__":
    # 
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
    # run_constructor_rank(2)
    # time.sleep(120)
    # run_constructor_rank(3)
    # time.sleep(120)
    # run_constructor_rank(4)
    # time.sleep(120)
    # run_constructor_rank(5)
    # time.sleep(120)
    # run_constructor_rank(6)
    # run_constructor_user(3975343)
