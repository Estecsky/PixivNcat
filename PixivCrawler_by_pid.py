import sys
import os
sys.path.append((os.path.dirname(__file__)))
from pixivtools import pixiv_api
import pixivtools
import asyncio
import yaml
global_pid = 129162873
# # 定义两个不同的 PID
# # global_pid1 = "129153029"
# global_pid1 = "1314520"
# global_pid2 = "128252798"

global_options = pixiv_api.ArtworkOptions(
        update=False,
        only_r18=False,
        only_non_r18=True,
        skip_manga=True,
        artwork_types=0,
        ignore_error=True
)
global_set_img_pid_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),"Pixiv_out","images_pid")
global_set_log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),"Pixiv_out","out.log")
global_set_sql_url = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),"pixiv.db")
global_config_yaml = os.path.join(os.path.dirname(__file__),"config.yaml")

def get_config():
    with open(global_config_yaml, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    # Create config using constructor
    cfg_maker = pixivtools.pixiv_config_maker()
    # Replace YOUR_PHPSESSID with your actual PHPSESSID from pixiv
    cfg_maker.set_phpsessid(config_data["phpsessid"])
    cfg_maker.set_proxy(config_data["proxy"])
    cfg_maker.set_img_dir(global_set_img_pid_dir)
    cfg_maker.set_log_file(global_set_log_file)
    cfg_maker.set_sql_url(f"sqlite:///{global_set_sql_url}")  # other db url see ./config.yaml or https://docs.sqlalchemy.org/en/20/core/engines.html
    return cfg_maker()

async def run_constructor_pid(pid):
# def run_constructor_pid(pid):
    global is_r18
    """Example: Using constructor to create crawler"""    # Create service and crawler
    cfg = get_config()
    service = pixivtools.new_pixiv_service(cfg)
    crawler = service.crawler()
    try:
    # Example crawling tasks
    # 1. Get artwork by ID
        # 使用 loop.run_in_executor 运行同步代码
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, lambda: crawler.get_by_artwork_id(artwork_id=pid, options=global_options))
        # result = crawler.get_by_artwork_id(artwork_id=pid, options=global_options)
        
        if result:
            return f"PID {pid}: is_R18"
        else:
            return f"PID {pid}: non_R18"
    except TypeError as e:
        # logging.error(f"ValueError occurred for PID {pid}: {e}")
        return f"PID {pid}: 找不到图片"
    except Exception as e:
        # logging.error(f"Unexpected error for PID {pid}: {e}")
        return f"PID {pid}: 发生意外错误{e}"
    # # 2. Get latest artworks from followed artists (page 1)
    # crawler.get_by_follow_latest(1)
    # # 3. Get artworks from specific user
    # crawler.get_by_user_id(23279364)
    
    # # 4. Get popular artworks with tag
    # crawler.get_by_tag_popular("ホロライブ")


# async def main():
#     """主函数：并发执行两个任务"""
#     tasks = [
#         # run_constructor_pid(global_pid1),
#         # run_constructor_pid(global_pid2)
#     ]
#     results = await asyncio.gather(*tasks)
#     return results


if __name__ == "__main__":
    try:
        # results = asyncio.run(main())
        # for result in results:
        #     print(result)
        run_constructor_pid(global_pid)
    except Exception as e:
        print(f"发生错误: {e}")
