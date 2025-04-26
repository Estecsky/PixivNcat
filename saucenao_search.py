from saucenao_api import SauceNao
import json
import yaml
import os
from datetime import datetime
import asyncio
global_config_yaml = os.path.join(os.path.dirname(__file__),"config.yaml")
global_saucenao_search_log = os.path.join(os.path.dirname(__file__),"saucenao_search_log")

async def saucenao_searchImg(img_url):
    with open(global_config_yaml, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    
    sauce = SauceNao(api_key=config_data['saucenao_api_key'])
    results = await asyncio.to_thread(sauce.from_url, img_url)  # 使用 asyncio.to_thread 包装同步调用  # or from_file()
    if not os.path.exists(global_saucenao_search_log):
        os.mkdir(global_saucenao_search_log)
    # results = sauce.from_file(r'E:\vivo互传\2d146f38ab6ccb36.png')
    # best = results[0]  # results sorted by similarity
    # Collect all raw data into a list
    raw_data_list = [result.raw for result in results]
    
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d_%H_%M_%S_%f")

    json_file_path = os.path.join(global_saucenao_search_log,f'{current_time_str}.json')
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json_str = json.dumps(raw_data_list, ensure_ascii=False, indent=4)
        f.write(json_str)
        
    return json_file_path
async def format_saucenao_results(img_url):
    similarity_limit = 75.0
    has_img = False
    json_file_path = await saucenao_searchImg(img_url)
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    formatted_data = []
    for result in data:
        data_keys = result['data'].keys()
        if "source" in data_keys or "ext_urls" in data_keys:
            if float(result['header']['similarity']) >=similarity_limit:
                formatted_result = {}
                has_img = True
                formatted_result['相似度'] = result["header"]["similarity"]
                if "title" in data_keys:
                    title = result['data']["title"]
                    if title:
                        formatted_result["标题"] = title
                if 'creator' in data_keys:
                    creator = result['data']["creator"]
                    if creator:
                        formatted_result["作者"] = creator

                if 'characters' in data_keys:
                    characters = result['data']["characters"]
                    if characters:
                        formatted_result["角色"] = characters
                    
                if 'material' in data_keys:
                    material = result['data']["material"]
                    if material:
                        formatted_result["素材"] = material

                if 'source' in data_keys:
                    source = result['data']["source"]
                    if source:
                        if "i.pximg.net" in source:
                            pid = source.split("/")[-1]
                            source = f"https://www.pixiv.net/artworks/{pid}"
                            formatted_result["来源"] = source
                            formatted_result["Pixiv作品id"] = pid
                        else:
                            formatted_result["来源"] = source
                    
                if 'ext_urls' in data_keys:
                    ext_urls = result['data']["ext_urls"]
                    if ext_urls:
                        formatted_result["其他链接"] = ext_urls

                # if 'pixiv_id' in data_keys:
                #     pixiv_id = result['data']["pixiv_id"]
                #     if pixiv_id:
                #         formatted_result["pixiv_id"] = pixiv_id

                if 'danbooru_id' in data_keys:
                    danbooru_id = result['data']["danbooru_id"]
                    if danbooru_id:
                        formatted_result["danbooru_id"] = danbooru_id

                if 'yandere_id' in data_keys:                
                    yandere_id = result['data']["yandere_id"]
                    if yandere_id:
                        formatted_result["yandere_id"] = yandere_id

                if 'gelbooru_id' in data_keys:                
                    gelbooru_id = result['data']["gelbooru_id"]
                    if gelbooru_id:
                        formatted_result["gelbooru_id"] = gelbooru_id

                
                formatted_data.append(formatted_result)
                
    return [has_img,formatted_data]

async def msg_saucenao_format(img_url):
    msg_raw = await format_saucenao_results(img_url)
    if msg_raw[0]:
        msg_list = []
        for msg in msg_raw[1]:
            msg_list.append(f"相似度：{msg['相似度']}\n")
            if "标题" in msg.keys():
                msg_list.append(f"标题：{msg['标题']}\n")
            if "作者" in msg.keys():
                msg_list.append(f"作者：{msg['作者']}\n")
            if "角色" in msg.keys():
                msg_list.append(f"角色：{msg['角色']}\n")
            if "素材" in msg.keys():
                msg_list.append(f"素材：{msg['素材']}\n")
            if "来源" in msg.keys():
                msg_list.append(f"来源：{msg['来源']}\n")
            if "Pixiv作品id" in msg.keys():
                msg_list.append(f"Pid：{msg['Pixiv作品id']}\n")
            if "danbooru_id" in msg.keys():
                msg_list.append(f"danbooru_id：{msg['danbooru_id']}\n")
            if "yandere_id" in msg.keys():
                msg_list.append(f"yandere_id：{msg['yandere_id']}\n")
            if "gelbooru_id" in msg.keys():
                msg_list.append(f"gelbooru_id：{msg['gelbooru_id']}\n")
            if "其他链接"in msg.keys():
                # msg_list.append(f"其他链接：{msg['其他链接']}\n")
                msg_list.append(f"其他链接：\n")
                for url in msg['其他链接']:
                    msg_list.append(f"{url}\n")
            #分隔线
                msg_list.append("---------------------------\n")
                
    else:
        msg_list = ["未找到高相似图片"]
        
    return msg_list

# async def main():
#     img_url = ""  # 替换为实际图片URL
#     result = await msg_saucenao_format(img_url)
#     with open("result.txt", "w",encoding='utf-8') as f:
#         f.write("".join(result))

# if __name__ == "__main__":
#     asyncio.run(main())
#     print("Done")