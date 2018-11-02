# Faster - a  python registry manager

---- 


![python2.7](https://img.shields.io/badge/python-2.7-green.svg?branch=master)
![python3.6](https://img.shields.io/badge/python-3.6-green.svg?branch=master)
![platform](https://img.shields.io/conda/pn/conda-forge/python.svg)

## Installation 
Use pip: 
```
pip install faster 
```

if you want to install from source code , you can download from pypi or simple use: 
```
git clone https://github.com/lfzark/faster
```
then run: 
```
python setup.py install 
```

## Example 

```bash
faster auto

```

```log
[+] May cost your few minutes according your network situation.
[+] douban      https://pypi.douban.com/simple  0.496495008469
[+] pypi        https://pypi.python.org/simple  2.82570886612
[+] tencent     https://mirrors.cloud.tencent.com/pypi/simple   0.392730951309
[+] tsinghua    https://pypi.tuna.tsinghua.edu.cn/simple        0.177893877029
[+] aliyun      https://mirrors.aliyun.com/pypi/simple  <urlopen error [Errno -2] Name or service not known>
[+] ustc        https://pypi.mirrors.ustc.edu.cn/simple 0.687880992889


[+] BEST PIP : tsinghua  -  https://pypi.tuna.tsinghua.edu.cn/simple ,SPEED: 0.178
USE tsinghua - https://pypi.tuna.tsinghua.edu.cn/simple

```


```
faster use douban

```

```log
USE douban - https://pypi.douban.com/simple
```

## TODO

-  update pip list fron remote