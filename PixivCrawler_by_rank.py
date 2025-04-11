import pixivtools
from get_RankType import get_rank_type
import os
import yaml
global_RankType = "monthly" # 从下列参数中选择
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
global_data = 20250402 # 榜单统计结束时间  日期，格式为YYYYMMDD

global_options = pixivtools.pixiv_api.ArtworkOptions(
    update=False,
    only_r18=False,
    only_non_r18=False,
    skip_manga=True,
    artwork_types=None,
    ignore_error=True
)
global_set_img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),"Pixiv_out",f"images_{global_RankType}")
global_set_log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),"Pixiv_out","out.log")
global_set_sql_url = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),"pixiv.db")
def get_config():
    global global_RankType
    with open("config.yaml", "r", encoding="utf-8") as f:
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
    # crawler.get_by_user_id(23279364)
    
    # # 4. Get popular artworks with tag
    # crawler.get_by_tag_popular("ホロライブ")
    # crawler.get_by_rank(pixivtools.RankType.MALE, 20250313, 1)
    crawler.get_by_rank(rank_type=get_rank_type(global_RankType),date=global_data,page=page,options=global_options)

if __name__ == "__main__":
    i = 0
    while i < global_page_num:
        run_constructor_rank(i+1) 
        i += 1