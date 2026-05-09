import re

# 去除 HTML 标签并提取评论内容
raw_comment = """
<div class="comment">
   <div class="user-info">
       <span class="user-id">用户12345</span>
       <span class="product-id">商品67890</span>
       <span class="score">★★★★☆</span>
       <span class="time">2024-05-20 14:30:45</span>
   </div>
   <div class="content">
       <p>宝贝收到了，质量很好，物流也很快！👍</p>
       <p>价格有点贵，不过还是值得购买的。</p>
   </div>
</div>
"""
# 1. 去除所有HTML标签
# [^>]+ 不是 “>” 的任意字符 1~n 次
clean_comment = re.sub(r"<[^>]+>", "", raw_comment)
print("清洗后的评论内容：")
print(clean_comment)
print("=" * 50)

# 提取关键信息（用户 ID、商品 ID、评分、时间）
info_pattern = r"""
\s*用户(\d+)\s*          # 提取用户ID（数字部分）
商品(\d+)\s*          # 提取商品ID（数字部分）
([★☆]{5})\s*       # 匹配评分（★☆组合）
(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s*  # 提取时间戳
"""
# 使用re.search()查找匹配项
# 匹配时用 () 进行了分组，有几个括号，就能取几个 group
# re.VERBOSE    re.X    正则可换行加注释
match = re.search(info_pattern, clean_comment, re.VERBOSE)
print(match)
if match:
    user_id = match.group(1)
    product_id = match.group(2)
    score = match.group(3)
    timestamp = match.group(4)

    print("提取的关键信息：")
    print(f"用户ID：{user_id}")
    print(f"商品ID：{product_id}")
    print(f"评分：{score}")
    print(f"评论时间：{timestamp}")
    print("=" * 50)


# 提取评论内容并进行关键词识别
content_pattern = r"宝贝收到了，([^。！]+)，([^。！]+)！([^。]+)。([^。]+)"
content_match = re.search(content_pattern, clean_comment)
if content_match:
    quality_comment = content_match.group(1)
    logistics_comment = content_match.group(2)
    price_comment = content_match.group(3)
    overall_comment = content_match.group(4)
    print("提取的评论内容：")
    print(f"质量评价：{quality_comment}")
    print(f"物流评价：{logistics_comment}")
    print(f"价格评价：{price_comment}")
    print(f"总体评价：{overall_comment}")
    print("=" * 50)


# 情感分析（基于关键词匹配）
positive_words = ["好", "快", "值得", "满意"]
negative_words = ["贵", "慢", "失望", "差"]
positive_count = 0
negative_count = 0
# 检查评论内容中的情感词
for word in positive_words:
    # 字符串.count(子串) 就是统计 子串 在字符串里不重叠出现的次数
    # s = "aaaaa"
    # print(s.count("aa"))
    # 第 1 个 aa 占前两位，不回头重叠，结果是 2
    positive_count += clean_comment.count(word)
for word in negative_words:
    negative_count += clean_comment.count(word)
print("情感分析结果：")
print(f"正向词出现次数：{positive_count}")
print(f"负向词出现次数：{negative_count}")
if positive_count > negative_count:
    sentiment = "正向"
elif negative_count > positive_count:
    sentiment = "负向"
else:
    sentiment = "中性"

print(f"情感倾向：{sentiment}")
print("=" * 50)


# 完整的数据处理流程
def process_comment(raw_comment):
    """处理单条评论数据，返回结构化信息"""
    # 步骤1：清洗HTML标签
    clean_comment = re.sub(r"<[^>]+>", "", raw_comment)
    # 步骤2：提取关键信息
    info_match = re.search(r"\s*用户(\d+)\s*商品(\d+)\s*([★☆]{5})\s*(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s*", clean_comment)
    if not info_match:
        return None
    user_id = info_match.group(1)
    product_id = info_match.group(2)
    score = info_match.group(3)
    timestamp = info_match.group(4)
    # 步骤3：提取评论内容
    content_match = re.search(r"宝贝收到了，([^。！]+)，([^。！]+)！([^。]+)。([^。]+)", clean_comment)
    quality = content_match.group(1) if content_match else "未提及"
    logistics = content_match.group(2) if content_match else "未提及"
    price = content_match.group(3) if content_match else "未提及"
    overall = content_match.group(4) if content_match else "未提及"
    # 步骤4：情感分析
    positive_count = sum(clean_comment.count(word) for word in positive_words)
    negative_count = sum(clean_comment.count(word) for word in negative_words)
    if positive_count > negative_count:
        sentiment = "正向"
    elif negative_count > positive_count:
        sentiment = "负向"
    else:
        sentiment = "中性"
    # 返回结构化数据
    return {
        "user_id": user_id,
        "product_id": product_id,
        "score": score,
        "timestamp": timestamp,
        "quality": quality,
        "logistics": logistics,
        "price": price,
        "overall": overall,
        "sentiment": sentiment
    }


# 测试完整流程
processed_data = process_comment(raw_comment)
if processed_data:
    print("完整的评论数据：")
    for key, value in processed_data.items():
        print(f"{key}：{value}")
    print("=" * 50)









