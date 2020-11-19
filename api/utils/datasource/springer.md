# Springer API
## 搜索引擎
* Springer Nature Metadata API  -- metadata
* Springer Nature Meta API        -- meta
* Springer Nature openaccess API -- openaccess

## 搜索选项  
* 唯一标识符 doi -- 10.1007/978-3-319-07410-8_4
* 科目 subject    -- Chemistry
* 关键词 keyword  -- onlinear
* 期刊 pub -- Extremes
* 年份 year -- 2007
* 限制日期 onlinedate -- 2019-03-29
* 国家 country -- New Zealand
* 国际标准图书编号 isbn -- 978-0-387-79148-7
* 国际标准期刊号 issn  --1861-0692
* 期刊号 journalid -- 392
* 日期 date -- 2010-03-01
* 主题合集 topicalcollection -- Scleroderma
* 所属种类 type  -- Book

更多不常用选项详见[此处](https://dev.springernature.com/adding-constraints)

## 搜索方式
在python中引用该类，选择任意搜索引擎初始化实例,  将查询选项放入一个dict中, 并调用query函数
```python
import springer

    s = springer("meta")
    params = dict(
        doi='10.1007/978-3-319-07410-8_4',
        year = 2017
        # you could add more constraint here
    )
    pprint(s.query(params))
```

