import random
import os
from ncatbot.utils.logger import get_log
_log = get_log()

Ori_img_id_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"logs","Ori_img_id.txt")
selected_img_id_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"logs")
# "selected_img_id.txt"
def getOri_imgId(img_path):
    for root,dirs,files in os.walk(img_path):
        with open(Ori_img_id_path,"w") as f:
            for file in files:
                # if file.endswith(".jpg"):
                #     print(file)
                #     print(file.split(".")[0])
                #     print(file.split(".")[0].split("_")[1])
                #     print(file.split(".")[0].split("_")[1].split("-"))
                f.write(file +"\n")

        break
    # print("done")

def random_id(random_lst):
    i = 0
    while i < 10:
        x = random.choice(random_lst)
        i += 1
        random_lst.append(x)
    a = random.choice(random_lst)
    random_lst.reverse()
    b = random.choice(random_lst)
    final_lst = [a,b]
    return random.choice(final_lst)
          
def get_Ramdom_imgId(ori_img_path,group_id):
    out_of_index = False
    getOri_imgId(img_path= ori_img_path)
    with open(Ori_img_id_path,"r") as f:
        lst = f.readlines()
    gruop_select_id = os.path.join(selected_img_id_path,f"{group_id}_selected_img_id.txt")
    if not os.path.exists(gruop_select_id):
        with open(gruop_select_id,"w") as f:
                f.write("")

    with open(gruop_select_id ,"r") as f:
        selected_id = f.readlines()

    result = random_id(lst)
    limlit = 0
    while result in selected_id and limlit < 20:
        result = random_id(lst)
        limlit += 1
        
    with open(gruop_select_id ,"a") as f:
        f.write(result)
        # f.write("\n")
        
    with open(gruop_select_id ,"r") as f:
        lst = f.readlines()
        
    if not len(lst) == len(set(lst)):
        out_of_index = True
        
    # if out_of_index:
    #     pass
        # with open("selected_imgId.txt","w") as f:
        #     f.write("")
        # _log.info("！！！已抽取图片列表出现重复，自动清空！！！！")
    # result = result.replace("\n","")
    return result