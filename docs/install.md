## 安装和运行文档

#### 1. Overall
服务器(文中称为此程序)基于Python3.6开发, 在任何低于这个版本的Python中我们不保证此程序可以运行. 
此程序依赖的必须库有`flask` 和 `PyMySQL`. 下表详细展示了此程序用到所有第三方库及其版本: 

| LIBs | Flask | PyMySQl | Python-dotenv |
|:----:|:-----:|:-------:|:-------------:|
| VERs | 1.1.2 |  0.10.1 |     0.14.0    |

#### 2. Download
您可以使用Git指令下载此程序, 
```
$ git clone https://github.com/SciQuestDevelopment/Server.git
``` 

#### 3. Virtual environment (Optional but suggested) 


为下载必须的第三方Python库, 我们建议使用虚拟环境. 可以通过以下指令初始化并激活虚拟环境, 

```bash
// 安装 virtualenv 
$ pip install virtualenv 
// 创建虚拟环境
$ virtualenv  name_for_the_venv
// 激活虚拟环境
$ source path_to_venv/bin/activate
```

#### 4. Installation packages

我们建议直接使用, `requirement.txt`文件来安装必须的第三方库. 可以通过以下指令安装

```
(venv)$ pip install -r requirement.txt 
```

当完整安装所有依赖的第三方库之后, 在运行服务器之前需要预先设置一些环境变量. 
如果安装了python-dotenv库, 您可以通过添加`.env` 文件来设置. 
如果是SciQuest的开发者, 请从通过 [此链接](https://share.weiyun.com/IVUVQy8u) 下载文件. 
然后将文件命名为`.env`后放置到项目根目录中. 
如果需要自定义`.env` 文件, 请为下列变量赋值

```
// 数据库URI
DB_URI=?
// 数据库端口号
DB_PORT=?
// 数据库用户名
DB_ACCOUNT=?
// 数据库密码
DB_PASSWORD=?
```

#### 5. Running 

请使用如下指令运行此程序

```
(venv)$ flask run
```
