'''
Author: matiastang
Date: 2025-05-06 16:06:37
LastEditors: matiastang
LastEditTime: 2025-05-06 16:36:50
FilePath: /welfare-lottery-server-python/types/welfare_lottery_types.py
Description: 类型声明
'''

from typing import Optional
from pydantic import BaseModel, Field


class WelfareLotteryPrizeGrade(BaseModel):

    num: Optional[str] = Field(default=None, description='数量')

    type: Optional[str] = Field(default=None, description='等级')

    money: Optional[str] = Field(default=None, description='金额')


class WelfareLotteryInfo(BaseModel):

    code: str = Field(description='期号')

    date: str = Field(description='日期')

    week: str | None = Field(default=None, description='星期')

    red: str = Field(description='红球')

    blue: str = Field(description='蓝球')

    content: str | None = Field(default=None, description='中奖内容')

    prize_grades: list[WelfareLotteryPrizeGrade] = Field(default=[], description='中奖等级')

    sales: str | None = Field(default=None, description='销售额')

    poolmoney: str | None = Field(default=None, description='奖金池')

    video_link: str | None = Field(default=None, description='视频链接')

    details_link: str | None = Field(default=None, description='详情链接')

    creat_time: str | None = Field(default=None, description='创建时间')

    update_time: str | None = Field(default=None, description='更新时间')

    disabled: int = Field(default=0, description='是否禁用')


class WelfareLotteryResponse(BaseModel):

    code: int = Field(description='代码')

    data: list[WelfareLotteryInfo] | None = Field(default=None, description='信息')

    total: Optional[int] = Field(default=None, description='总数')

    msg: Optional[str] = Field(default=None, description='信息')
