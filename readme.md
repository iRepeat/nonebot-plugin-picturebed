可拓展的 **[Nonebot2](https://github.com/nonebot/nonebot2)** 图床插件

## 说明

借助  **[Nonebot2](https://github.com/nonebot/nonebot2)** 调用图床API，快速将图片（或图片链接）上传至图床。

## 使用

- clone后导入 **[Nonebot2](https://github.com/nonebot/nonebot2)** 插件目录，然后配置config，启动bot。
- 使用 `upload 【图片】` 命令上传图片。
- 使用 `图床 【图床名称】` 临时切换图床。

## 自定义图床

该插件默认实现了 `gitee `和 `sm.ms` 图片上传功能，添加更多图床请参照以下步骤：

#### 1. 添加配置

向 config.py 添加图床可能用到的配置参数，如token，password

#### 2. 创建图床类

创建图床类并继承抽象类 PictureBed 。

#### 3. 实现抽象方法

PictureBed 有两个抽象方法需要实现：

- ##### _\_init\_\_(config: dict)

  在这里初始化图床的配置信息.

  - `:param config:` config.py中对应图床的配置信息

- ##### upload(url: str) -> dict

  上传图片方法.

  - `:param url:` 图片地址

  - `:returns: ` 上传结果信息，合法的返回值请参照 upload_fail 或 upload_success ，可直接使用

#### 4. 注册图床类

在 [\_\_init\_\_.py](./__init__.py) 中的 `picture_beds` 中注册前面创建的图床类。

```python
# 在这里注册图床类
picture_beds = {
    "gitee": PBGitee(config.gitee),
    "smms": PBSMMS(config.smms)
}
```

