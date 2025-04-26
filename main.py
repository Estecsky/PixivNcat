# main.py

from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core.message import GroupMessage, PrivateMessage
from .PixivCrawler_by_pid import run_constructor_pid
from .PixivCrawler_by_rank import global_RankType 
from Unit.random_img import get_Ramdom_imgId
from .saucenao_search import msg_saucenao_format
import yaml
import os
from ncatbot.core.element import (
    MessageChain,  # 消息链，用于组合多个消息元素
    Image,         # 图片
)
from ncatbot.utils.logger import get_log
import sys
sys.path.append((os.path.dirname(__file__)))
_log = get_log()
Pixiv_help_info =[
    "Pixivbot 使用方法：",
    "1.输入 /pixiv+空格+随机涩图 或者直接输入 随机涩图 ，bot会自动发送随机图片。",
    "2.输入 /pixiv+空格+pid+空格+[pid] ，bot会自动下载并发送图片。\n  例： /pixiv pid 129105117",
    "3.输入 /pixiv+空格+help 或者/pixiv+空格+帮助，bot会自动发送帮助信息。",

]

# 随机涩图需要的图库，默认和排行榜爬虫文件中全局类型一致，或者根据自己的文件路径修改
# 例如 img_RankType = 'weekly' 如果修改了images_path可忽略此项
# img_RankType = global_RankType
img_RankType = "custom"

# 最好使用绝对路径，随机涩图需要的图库路径
# images_path = ""
images_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),"Pixiv_out",f"images_{img_RankType}")

# 最好使用绝对路径，pid爬取图片保存路径
# images_pid_path = ""
images_pid_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),"Pixiv_out","images_pid")


global_config_yaml = os.path.join(os.path.dirname(__file__),"config.yaml")
global_temp_qq =  123456790  # 临时消息qq,为发送合并消息做准备

bot = CompatibleEnrollment  # 兼容回调函数注册器
super_user = ""

PixivNcat_on = True
Img_Search_on = True
prev_msg_time = 0
search_prev_msg_time = 0
cold_time = 20
class PixivNcat(BasePlugin):
    name = "PixivNcat" # 插件名称
    version = "0.8.0"  # 插件版本
    
    @bot.group_event()
    async def on_group_event(self, msg: GroupMessage):
        '''
        群聊事件处理-配置与帮助信息
        '''
        global PixivNcat_on
        global Pixiv_help_info
        global cold_time
        global Img_Search_on
    # 定义的回调函数
        if msg.raw_message.lower() == "测试PixivBot".lower():
            if msg.user_id == super_user:
                await self.api.post_group_msg(msg.group_id, text="插件PixivBot测试成功")
        if msg.raw_message.lower().startswith("冷却时间"):
            if msg.user_id == super_user:
                if  msg.raw_message[4:].isdigit():
                    # with open(global_config_yaml, 'r',encoding="utf-8") as file:
                    #     data = yaml.safe_load(file)
                    # with open(global_config_yaml, 'w',encoding="utf-8") as file:
                    #     data["cold_time"] = int(msg.raw_message[4:])
                    #     yaml.dump(data, file)
                    cold_time = int(msg.raw_message[4:])
                    await self.api.post_group_msg(msg.group_id, text=f"冷却时间为{cold_time}")
        if msg.raw_message.lower() == "关闭PixivBot".lower():
            if msg.user_id == super_user:
                PixivNcat_on = False
                Img_Search_on = False
                await self.api.post_group_msg(msg.group_id, text="PixivBot已关闭")
        if msg.raw_message.lower() == "开启PixivBot".lower():
            if msg.user_id == super_user:
                PixivNcat_on = True
                Img_Search_on = True
                await self.api.post_group_msg(msg.group_id, text="PixivBot已打开")
        if msg.raw_message.lower() == "/pixiv help" or msg.raw_message.lower() == "/pixiv 帮助":
                await self.api.post_group_msg(msg.group_id, text="\n".join(Pixiv_help_info))
                
    @bot.group_event()
    async def on_group_event(self, msg: GroupMessage):
        '''
        群聊事件处理-PixivBot运行
        '''
        global PixivNcat_on
        global prev_msg_time
        global cold_time
        global super_user
        if PixivNcat_on == True:
            if msg.raw_message.lower() == "/pixiv 随机涩图" or msg.raw_message.lower() == "随机涩图":
                if msg.time - prev_msg_time < cold_time and msg.user_id != super_user:
                    await self.api.post_group_msg(msg.group_id, text=f"{cold_time}秒冷却中喵",reply=msg.message_id)
                    return
                else:
                # if msg.user_id != super_user: 
                #     await self.api.post_group_msg(msg.group_id, text="调试中，暂时禁用",reply=msg.message_id)
                # print(msg.time)
                    selceted_img_name = get_Ramdom_imgId(images_path,msg.group_id)
                    selceted_img_name = selceted_img_name.replace("\n",'')
                    selceted_file_path = os.path.join(images_path, selceted_img_name)
                    if not os.path.exists(selceted_file_path):
                        _log.info(f"图片路径不存在 {selceted_file_path}")
                        return
                    # Send the file as a message
                    msg_chain = MessageChain([
                        Image(selceted_file_path)
                    ])
                    prev_msg_time = msg.time
                    # await self.api.post_group_file(msg.group_id,image=selceted_file_path)
                    send_status = await self.api.post_group_msg(msg.group_id,rtf=msg_chain)
                    # print(send_status)
                    if send_status['status'] ==  'failed':
                        prev_msg_time = 0
                        await self.api.post_group_msg(msg.group_id, text="图片发送失败喵~，再次抽取喵~",reply=msg.message_id)

                return
                
            if msg.raw_message.lower().startswith("/pixiv pid "):
                artwork_pid = msg.message[0]["data"]["text"].strip()[11:] #/pixiv pid 129105117
                if not artwork_pid.isdigit():
                    await self.api.post_group_msg(msg.group_id, text="输入pid非纯数字，最好不要随便乱输入喵",reply=msg.message_id)
                    return
                else:
                    artwork_result = await run_constructor_pid(artwork_pid)
                    if "is_R18" in artwork_result:  
                        # 默认不会对R18图片做任何操作，如果在PixivCrawler_by_pid.py 设置了全局作品配置为仅爬取非R18，图片不会下载
                        await self.api.post_group_msg(msg.group_id, text="图片是R18喵~只有主人AQ才能看喵!",reply=msg.message_id)
                    elif "找不到图片" in artwork_result:
                        await self.api.post_group_msg(msg.group_id, text="pid找不到图片喵~",reply=msg.message_id)
                    elif "发生意外错误" in artwork_result:
                        await self.api.post_group_msg(msg.group_id, text="出错了喵~",reply=msg.message_id)
                    elif "non_R18" in artwork_result:
                        for root,dirs,files in os.walk(images_pid_path):
                            file_name = None
                            for file in files:
                                if artwork_pid in file:
                                    file_name = file
                                    break
                            break
                        if file_name is None:
                            await self.api.post_group_msg(msg.group_id, text="好像找不到图片喵~",reply=msg.message_id)
                            return
                        else: #开始处理图片文件路径
                            
                            file_name = file_name.split(".")[0].split("_")[0]+"_0"+"."+file_name.split(".")[1]
                            img_file_path = os.path.join(images_pid_path, file_name)
                            if not os.path.exists(img_file_path):
                                _log.info(f"图片路径不存在{img_file_path}")
                                return
                            # Send the file as a message
                            msg_chain = MessageChain([
                                Image(img_file_path)
                            ])
                            await self.api.post_group_msg(msg.group_id,rtf=msg_chain)
                            # await self.api.post_group_file(msg.group_id,image=img_file_path)
                            await self.api.post_group_msg(msg.group_id,text=f"喵~Pid:{artwork_pid}")

    @bot.group_event()
    async def on_group_event(self, msg: GroupMessage):
        global global_temp_qq
        global Img_Search_on
        global search_prev_msg_time
        message_segs = msg.message
        # 默认冷却20秒
        search_cold_time = 20
        # 初始化两个标志变量
        has_text = False
        has_reply = False
        
        # 定义要搜索的关键词
        Key_word="/二次元搜图"
        Key_word2="/搜图测试"
        if Img_Search_on:
            # 遍历列表中的每个字典
            for item in message_segs:
                if item['type'] == 'text' and (item["data"]["text"].strip().startswith(Key_word) or item["data"]["text"].strip().startswith(Key_word2)):
                    has_text = True
                    
                elif item['type'] == 'reply':
                    has_reply = True
                    msg_id_img = item['data']["id"]
            if has_reply and has_text :
                if msg.time - search_prev_msg_time < search_cold_time and msg.user_id != super_user:
                    await self.api.post_group_msg(msg.group_id, text=f"搜图{search_cold_time}秒冷却中喵",reply=msg.message_id)
                    return
                else:
                    await self.api.post_group_msg(msg.group_id, text="正在搜图喵~",reply=msg.message_id)
                    msg_dict = await self.api.get_msg(message_id=msg_id_img)
                    
                    # _log.info(f"获取信息示例{msg_dict['data']["message"][0]["data"]["url"]}")
                    # await self.api.post_group_msg(msg.group_id, text=f"消息图片地址为{msg_dict['data']["message"][0]["data"]["url"]}")
                    
                    if msg_dict['data']["message"][0]["type"] == "image":
                        # if msg.user_id == super_user:
                        msg_img_url = msg_dict['data']["message"][0]["data"]["url"]
                        img_search_msg = await msg_saucenao_format(msg_img_url)
                        img_search_result = "".join(img_search_msg)
                        if img_search_msg[0] == "未找到高相似图片":
                            await self.api.post_group_msg(msg.group_id, text="没有找到高相似图片喵~",reply=msg.message_id)
                            return
                        # 向中转qq发送搜图结果
                        await self.api.post_private_msg(user_id=global_temp_qq,text=img_search_result)
                        
                        # 获取需要合并的消息
                        result_history = await self.api.get_friend_msg_history(user_id=global_temp_qq,message_seq=0,count=1,reverse_order=False)
                        history_lst = result_history["data"]["messages"]
                        send_msg_id = []
                        for msg_each in history_lst:
                            send_msg_id.append(str(msg_each["message_id"]))
                        # 发送合并信息
                        search_prev_msg_time = msg.time
                        await self.api.send_group_forward_msg(msg.group_id,messages=send_msg_id)
                    else:
                        await self.api.post_group_msg(msg.group_id, text="不是图片喵~",reply=msg.message_id)



    
    @bot.private_event()
    async def on_private_message(self, msg: PrivateMessage):
        '''
        私聊事件处理
        '''
        pass
    
    
    
    async def on_load(self):
        print("插件加载中……")
        print(f"图库路径为:{images_path}")
        print(f"Pid结果路径为:{images_pid_path}")
        # 从 config.yaml 中读取配置
        with open(global_config_yaml, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
            global super_user
            super_user = config_data["manager_id"]

        # 插件加载时执行的操作, 可缺省
        print(f"{self.name} 插件已加载")
        print(f"插件版本: {self.version}")