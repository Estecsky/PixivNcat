import enum
from pixivtools import RankType

# class RankType(enum.Enum):
#     DAILY = 'daily'  # 日榜
#     WEEKLY = 'weekly'  # 周榜
#     MONTHLY = 'monthly'  # 月榜
#     NEWBIE = "rookie"  # 新人榜
#     ORIGINAL = "original"  # 原创榜
#     DAILY_AI = "daily_ai"  # 日榜-ai
#     MALE = "male"  # 男性喜爱
#     FEMALE = "female"  # 女性喜爱

#     DAILY_R18 = 'daily_r18'
#     WEEKLY_R18 = 'weekly_r18'
#     WEEKLY_R18G = 'r18g'
#     DAILY_AI_R18 = "daily_r18_ai"
#     MALE_R18 = "male_r18"
#     FEMALE_R18 = "female_r18"
    
def get_rank_type(rank_type: str) -> RankType:
    if rank_type == 'daily':
        return RankType.DAILY
    elif rank_type == 'weekly':
        return RankType.WEEKLY
    elif rank_type == 'monthly':
        return RankType.MONTHLY
    elif rank_type == 'rookie':
        return RankType.NEWBIE
    elif rank_type == 'original':
        return RankType.ORIGINAL
    elif rank_type == 'daily_ai':
        return RankType.DAILY_AI
    elif rank_type == 'male':
        return RankType.MALE
    elif rank_type == 'female':
        return RankType.FEMALE
    elif rank_type == 'daily_r18':
        return RankType.DAILY_R18
    elif rank_type == 'weekly_r18':
        return RankType.WEEKLY_R18
    elif rank_type == 'r18g':
        return RankType.WEEKLY_R18G
    elif rank_type == 'daily_r18_ai':
        return RankType.DAILY_AI_R18
    elif rank_type == 'male_r18':
        return RankType.MALE_R18
    elif rank_type == 'female_r18':
        return RankType.FEMALE_R18
    else:
        raise ValueError(f"Invalid rank type: {rank_type}")