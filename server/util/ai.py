import hashlib
import json
import time
import traceback

from openai import OpenAI

from util.logger import logger

from .config import cfg
from .rediscache import get_all_types_data, r

client = OpenAI(
    base_url=cfg.get("openai", {}).get("base_url", ""),
    api_key=cfg.get("openai", {}).get("api_key", ""),
)
model = cfg.get("openai", {}).get("model", "")


def limit_cache(max_items=1):
    """限制 Redis 缓存条目数量"""
    keys = r.keys("openai_response:*")  # 获取所有相关缓存键
    if len(keys) >= max_items:
        r.delete(keys[0])


def del_cache():
    keys = r.keys("openai_response:*")
    s = len(keys)
    for k in keys:
        r.delete(k)
    return s


def gen_prompt():
    s = ""
    d = get_all_types_data()
    # print(d)
    for k, v in d.items():
        s += f"这是{k}类型的活动数据"
        for item in v:
            s += "\n"
            for i, j in item.items():
                s += f"{i}::{j}|"
        s += "\n"
    return s


def completion_api(
    prompt=gen_prompt(),
    tip="你是总结员,只输出下面数据的总结,加上适当推测，不要详细说每段时间干什么，不超过500字"
    "(每种数据都是k:v形式，'::'连接,'|'分隔不同类型,一行一条),可以使用html格式",
):
    if cfg.get("without_redis"):
        return (i for i in ["data: without_redis no cache!\n\n"])
    cache_key = "openai_response:" + hashlib.md5(prompt.encode()).hexdigest()
    logger.info(f"{cache_key=}")
    # 尝试从 Redis 中获取缓存
    cached_response = r.get(cache_key)
    if cached_response:
        response_data = json.loads(cached_response)
        generated_at = response_data["generated_at"]
        data = response_data["data"]

        # print(data)
        def stream():
            yield f"data: [{model}][cached at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(generated_at))}]<br>\n\n"
            for chunk in data.split("\n"):
                if chunk:
                    chunk = chunk.replace("\n", "")  # 先处理换行符
                    yield f"data: {chunk}\n\n"
            yield "event: end"

        return stream()
    else:

        def stream():
            yield f"data: [{model}][cache miss, generating response]<br>\n\n"
            response_data = {"data": "", "generated_at": int(time.time())}
            try:
                completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": tip},
                        {"role": "user", "content": prompt},
                    ],
                    stream=True,
                )
                for chunk in completion:
                    chunk = chunk.choices[0].delta.content or ""
                    if chunk:
                        response_data["data"] += chunk
                        yield f"data: {chunk}\n\n"
                yield "event: end"

                limit_cache()  # 限制缓存条目数量
                r.set(cache_key, json.dumps(response_data))
            except Exception as e:
                logger.error(traceback.format_exc())
                yield f"data: {str(e)}\n\n"

        return stream()


if __name__ == "__main__":
    # del_cache()
    for i in completion_api():
        print(i)
