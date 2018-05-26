# 工作进度条

## 使用方法

将 pypg.py 放置你的项目相同路径下

```
from pypg import PyProgress

total = 150
p = PyProgress(total, isIpy=True)
for i in range(total+1):
        time.sleep(0.1)
        p.update(i)
```

![运行结果](src/0.png)
