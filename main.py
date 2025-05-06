'''
Author: matiastang
Date: 2025-05-06 15:47:44
LastEditors: matiastang
LastEditTime: 2025-05-06 18:15:55
FilePath: /welfare-lottery-server-python/main.py
Description: welfare-lottery-server
'''
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from app.welfare_lottery_types import WelfareLotteryInfo, WelfareLotteryResponse

# Initialize FastMCP server
mcp = FastMCP("welfare-lottery")

# Define constants
WELFARE_LOTTERY_API_BASE = "https://api.tdytech.cn/api"
USER_AGENT = "welfare-lottery-app/0.1.0"
WELFARE_LOTTERY_LINK_BASE = "https://www.cwl.gov.cn"


async def welfare_lottery_request(url: str) -> dict[str, Any] | None:
    """
    调用远程服务接口

    Args:
        url (str): 地址

    Returns:
        dict[str, Any] | None: 结果
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as err:

            err_msg = str(err)

            print("Request Error:", err_msg)

            return None


def format_info(data: WelfareLotteryInfo) -> str:
    """
    格式化信息

    Args:
        data (WelfareLotteryInfo): 数据

    Returns:
        str: 信息
    """
    date = data.date
    code = data.code
    red = data.red
    blue = data.blue
    content = data.content
    prize_grades = data.prize_grades
    sales = data.sales
    poolmoney = data.poolmoney
    video_link = data.video_link
    details_link = data.details_link

    info_msg = f"""{date}第{code}期中奖号码：红球{red}，蓝球{blue}"""
    if content:
        info_msg += f"，一等奖地理分布为：{content}"
    if isinstance(prize_grades, list) and len(prize_grades) > 0:
        prize_grade_info = "、".join([f"{i.type}等奖：{i.num}注，每注奖金：{i.money}元" for i in prize_grades])
        info_msg += f"，各等级中奖信息为：{prize_grade_info}"
    if sales:
        info_msg += f"，销售额为：{sales}元"
    if poolmoney:
        info_msg += f"，奖金池为：{poolmoney}元"
    if video_link:
        info_msg += f"，[视频链接]({WELFARE_LOTTERY_LINK_BASE + video_link})"
    if details_link:
        info_msg += f"，[详情链接]({WELFARE_LOTTERY_LINK_BASE + details_link})"

    return info_msg


@mcp.tool()
async def get_welfare_lottery_last(count: int | None = None) -> str:
    """
    获取福利彩票最新中奖信息，包含：日期、期号、红球（6个1-33的数字）、蓝球（1个1-16的数字）、每个省份一等奖中奖注数、各等级中奖信息（各等级中间数量及单注金额）、当期销售额、当期后奖金池、视频链接、详情链接
    双色球玩儿法说明：双色球投注区分为红色球号码区和蓝色球号码区，红色球号码区由1-33共三十三个号码组成，蓝色球号码区由1-16共十六个号码组成。
    中奖等级对照表：一等奖：6+1，二等奖：6+0，三等奖：5+1，四等奖：5+0、4+1，五等奖：4+0、3+1，六等奖：2+1、1+1、0+1。

    Args:
        count (int | None, optional): 获取最新的多少期信息. Defaults to None.

    Returns:
        str: 最新的信息总结
    """
    url = f"{WELFARE_LOTTERY_API_BASE}/history/last"
    if count is not None:
        url += f"?count={count}"
    res = await welfare_lottery_request(url)

    if not isinstance(res, dict):
        return "未获取到中奖信息"

    try:
        wlres = WelfareLotteryResponse(**res)
        data = wlres.data
        if not data:
            return "中奖列表为空"

        latest = data[0]
        red_balls = latest.red.split()
        blue_ball = latest.blue
        return f"红球: {', '.join(red_balls)} 蓝球: {blue_ball}"
    except Exception as err:

        errMsg = str(err)

        print("Error parsing response:", res)

        print("Error:", errMsg)

        return "响应结果解析错误"


def main():
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
    main()
