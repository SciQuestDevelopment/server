## APIs接口文档

#### 1. Overall

当前服务器仅针对Article提供三个不同的接口, 
```
{
    "Get meta data of a single article ": "GET /posts/meta/one?id=:post_id",
    "Get meta data of all articles": "GET /posts/meta/all",
    "Get meta data of multiple articles": "GET /posts/meta/range?query_num=:query_num&offset_num=:offset_num",
    "Get article content": "GET /posts/content?id=:post_id",
}
```

#### 2. Get Meta Data
MetaData 指文章中除了文章本身的一切数据, 我们提供三个不同的接口来获取article meta data.
分别是 `Get posts/meta/one`, `Get posts/meta/range`和`Get posts/meta/all`

##### 2.1 `Get posts/meta/one`

用于获取指定文章的元数据, 需要传入文章的`id`参数, HTTP方法为`GET`. 

下面是通过浏览器获取数据的使用示例: 
```
https://127.0.0.1:5000/posts/meta/one?id=26
```
服务器将会以String格式返回如下数据: 
```
{
  "doi": "https://doi.org/10.1002/adma.202003484",
  "publish_date": "Thu, 08 Oct 2020 00:00:00 GMT",
  "summary": "Atomically dispersed catalysts, with maximized atom utilization of expensive metal components...",
  "title": "Dual\\u2010Metal Interbonding as the Chemical Facilitator for Single\\u2010Atom Dispersions",
  "url": "https://onlinelibrary.wiley.com/doi/full/10.1002/adma.202003484",
  "venue": "Advanced Materials"
}
```

##### 2.2 `Get posts/meta/all`

我们不建议直接使用该方法, 如非必要请使用"[meta/range](#rangeMethod)".
用于获取数据库中所有文章的元数据, 不需要任何参数, HTTP方法为`GET`. 

下面是通过浏览器获取数据的使用示例: 
```
https://127.0.0.1:5000/posts/meta/all
```
服务器将会以String格式返回如下数据: 
```
{
  "id": 1,
  "doi": "https://doi.org/10.1002/adma.202003484",
  "publish_date": "Thu, 08 Oct 2020 00:00:00 GMT",
  "summary": "Atomically dispersed catalysts, with maximized atom utilization of expensive metal components...",
  "title": "Dual\\u2010Metal Interbonding as the Chemical Facilitator for Single\\u2010Atom Dispersions",
  "url": "https://onlinelibrary.wiley.com/doi/full/10.1002/adma.202003484",
  "venue": "Advanced Materials"
}
...
{
  "id": 10,
  "doi": "https://doi.org/10.1002/adma.202003484",
  "publish_date": "Thu, 08 Oct 2020 00:00:00 GMT",
  "summary": "Atomically dispersed catalysts, with maximized atom utilization of expensive metal components...",
  "title": "Dual\\u2010Metal Interbonding as the Chemical Facilitator for Single\\u2010Atom Dispersions",
  "url": "https://onlinelibrary.wiley.com/doi/full/10.1002/adma.202003484",
  "venue": "Advanced Materials"
}
```

##### 2.3 `Get posts/meta/range`
<span id="rangeMethod"></span>
用于获取数据库中一定范围内文章的元数据, 需要指定`query_num`参数, 可选参数为`offset_num`, HTTP方法为`GET`.  

其中`query_num`返回指定数量的articles的metadata. `offset_num`返回id的偏差值, 如果不指定此参数将从最小的id开始返回. 
下面是通过浏览器获取数据的使用示例: 
```
https://127.0.0.1:5000/posts/meta/range?query_num=2&offset_num=5
```

服务器将会以String格式返回如下数据: 

```
{
  "id": 6,
  "doi": "https://doi.org/10.1002/adma.202003484",
  "publish_date": "Thu, 08 Oct 2020 00:00:00 GMT",
  "summary": "Atomically dispersed catalysts, with maximized atom utilization of expensive metal components...",
  "title": "Dual\\u2010Metal Interbonding as the Chemical Facilitator for Single\\u2010Atom Dispersions",
  "url": "https://onlinelibrary.wiley.com/doi/full/10.1002/adma.202003484",
  "venue": "Advanced Materials"
}
{
  "id": 7,
  "doi": "https://doi.org/10.1002/adma.202003484",
  "publish_date": "Thu, 08 Oct 2020 00:00:00 GMT",
  "summary": "Atomically dispersed catalysts, with maximized atom utilization of expensive metal components...",
  "title": "Dual\\u2010Metal Interbonding as the Chemical Facilitator for Single\\u2010Atom Dispersions",
  "url": "https://onlinelibrary.wiley.com/doi/full/10.1002/adma.202003484",
  "venue": "Advanced Materials"
}
```

#### 3. Get Content Data
content是指文章本体, 此程序当前只提供一个接口获取文章本体. 即为, `Get posts/content`

##### 3.1 `Get posts/content/all`
用于获取数据库中一定范围内文章本体. 需要指定`id`参数, HTTP方法为`GET`. 

下面是通过浏览器获取数据的使用示例: 
```
https://127.0.0.1:5000/posts/content?id=26
```
服务器将以文本文件格式返回文章. 


