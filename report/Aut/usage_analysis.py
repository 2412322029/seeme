import os
import sqlite3

from .logger import APPDATA

sqlite_file = os.path.join(APPDATA, "app_usage.db")
conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()


def print_app_usage_time():
    """打印每个应用的使用时间"""
    cursor.execute('''
    SELECT name, hourly_start_time, SUM(duration) AS total_duration
    FROM app_usage
    GROUP BY name, hourly_start_time
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(f"应用名称：{row[0]}, 每小时开始时间：{row[1]}, 总持续时间：{row[2]:.2f}秒")
    return rows


def get_all_names():
    """获取所有不同的应用名称"""
    cursor.execute('''
    SELECT DISTINCT name
    FROM app_usage
    ''')
    rows = cursor.fetchall()
    names = [row[0] for row in rows]
    return names


def get_total_duration_for_name(name):
    """获取特定应用的总使用时长"""
    cursor.execute('''
    SELECT SUM(duration) AS total_duration
    FROM app_usage
    WHERE name = ?
    ''', (name,))
    result = cursor.fetchone()
    total_duration = result[0] if result[0] else 0
    return {"name": name, "total_duration": total_duration}


def get_total_duration_for_all():
    """获取所有应用的总使用时长"""
    cursor.execute('''
    SELECT name, SUM(duration) AS total_duration
    FROM app_usage
    GROUP BY name
    ORDER BY total_duration DESC
    ''')
    results = cursor.fetchall()
    total_durations = [{"name": row[0], "total_duration": row[1]} for row in results]
    print(f"get {len(results)}个应用的总使用时长")
    return total_durations


def format_seconds(duration):
    """将秒转换为小时、分钟和秒的格式"""
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    time_str = ""
    if hours > 0:
        time_str += f"{hours:.0f}h"
    if minutes > 0 or hours > 0:
        time_str += f"{minutes:.0f}m"
    if seconds > 0 or time_str == "":
        time_str += f"{seconds:.0f}s"

    return time_str


def seconds2hms(total_duration):
    hours = int(total_duration) // 3600
    remaining_seconds = total_duration % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    if hours:
        s = f"{int(total_duration) / 3600:.01f}小时"
        return s
    if minutes:
        return f"{minutes:.0f}分钟"
    return f"{seconds:.0f}秒"



def print_analysis():
    """以表格形式打印应用的总使用时长"""
    print(f"{'应用名称':<28} {'总使用时长':<15} {'路径'}")
    print("-" * 70)
    for item in get_total_duration_for_all():
        name = item['name'].split('\\')[-1]
        duration = format_seconds(item['total_duration'])
        print(f"{name:<30} {duration:<20} {item['name']}")


def get_hourly_duration_for_name(name):
    """获取特定应用的每小时使用时长"""
    cursor.execute('''
    SELECT hourly_start_time, SUM(duration) AS total_duration
    FROM app_usage
    WHERE name = ?
    GROUP BY hourly_start_time
    ORDER BY hourly_start_time
    ''', (name,))
    rows = cursor.fetchall()
    hourly_durations = [{"hourly_start_time": row[0], "total_duration": row[1]} for row in rows]
    return {"name": name, "hourly_durations": hourly_durations}


def get_hourly_duration_for_all():
    """获取所有应用的每小时使用时长"""
    cursor.execute('''
    SELECT name, hourly_start_time, SUM(duration) AS total_duration
    FROM app_usage
    GROUP BY name, hourly_start_time
    ORDER BY name, hourly_start_time
    ''')
    rows = cursor.fetchall()

    # 将结果按应用名称分组
    app_durations = {}
    for row in rows:
        name, hourly_start_time, total_duration = row
        if name not in app_durations:
            app_durations[name] = []
        app_durations[name].append({"hourly_start_time": hourly_start_time, "total_duration": total_duration})

    # 转换为 JSON 格式
    result = [{"name": name, "hourly_durations": hourly_durations} for name, hourly_durations in app_durations.items()]
    return result


def get_data_for_hourly_start_time(start_time, end_time):
    """
    获取指定时间段内的所有数据
    :param start_time: 开始时间，格式为 'YYYY-MM-DD HH:00:00'
    :param end_time: 结束时间，格式为 'YYYY-MM-DD HH:00:00'
    :return: 查询结果列表
    """
    cursor.execute('''
    SELECT name, hourly_start_time, start_time, end_time, duration
    FROM app_usage
    WHERE hourly_start_time BETWEEN ? AND ?
    ORDER BY hourly_start_time
    ''', (start_time, end_time))
    rows = cursor.fetchall()
    data = [{"name": row[0], "duration": row[4]} for row in rows]
    return data


if __name__ == '__main__':
    # print_app_usage_time()
    # print(get_total_duration_for_all())
    print_analysis()
    # print(get_data_for_hourly_start_time("2025-01-26 00:00:00", "2025-01-26 24:00:00"))
