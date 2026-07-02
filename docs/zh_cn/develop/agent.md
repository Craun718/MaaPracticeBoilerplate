# AgentServer 编写指引

> [!NOTE]  
> Agent 属于 MaaFramework 的高级功能之一。在学习本章节以前请确保你已经掌握以下技能，否则请先学习[基础](/docs/zh_cn/develop/how_to_develop.md)的编写方法。
>
> - 至少熟练掌握一门编程语言，并理解面向对象的实现方法。
> - 至少用 `Pipeline` 编写过一个完整的可用`通用UI` 执行的任务链，了解 `ProjectInterface 协议`和 `Pipeline`。

<!-- markdownlint-disable-line 28 -->
> [!WARNING]  
>
> 本教程推荐使用 vscode 并安装 [Maa Pipeline Support 插件](https://marketplace.visualstudio.com/items?itemName=nekosu.maa-support) 进行调试，如果你正在使用 vscode 的编辑器，请查阅其他[开发工具](https://github.com/MaaXYZ/MaaFramework#%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7)的文档。

本教程使用 Python 编写 AgentServer 示例。如果你有面向对象编程的经验，也可选用[任意 MaaFramework 支持的编程语言](https://github.com/MaaXYZ/MaaFramework/blob/main/docs/zh_cn/2.1-%E9%9B%86%E6%88%90%E6%96%87%E6%A1%A3.md)来实现，将示例代码套用到其他语言是一件很容易的事。

> [!TIP]  
>
> 本教程可能会使用到 python 的某些高级特性。如果你正在使用其他的编程语言，请查阅[源码](https://github.com/MaaXYZ/MaaFramework/blob/main/docs/zh_cn/2.1-%E9%9B%86%E6%88%90%E6%96%87%E6%A1%A3.md)以了解某些特殊写法的差异。

_（本篇为编写基础指引，仅介绍 custom recognition 和 custom action 的编写方法，如需了解更多，请参考 [其他内容](#其他内容)）_

## ProjectInterface

要使用 AgentServer 首先要在 interface.json 中补充相关的字段。

```json
{
    ...
    "agent": {
        // 执行命令，可以是 interface.json 所在目录的相对位置，也可以是Path中已有的路径
        "child_exec": "python",
        // 命令的参数
        "child_args": [
            "./agent/main.py"
        ]
    },
    ...
}
```

若按以上内容进行填写，则通用 UI 在启动时会尝试执行 `python ./agent/main.py`。（CWD为 interface.json 所在目录）

## 内容编写

本文将围绕仓库中附带的一个简单的 [demo](/agent) 示例进行讲解。

在开始前，请确保你已经安装了 python 依赖。

```bash
pip install MaaFw
```

> [!CAUTION]
> **千万不要装错了！**

### 自定义识别

#### 基本结构

完整内容请参考 [my_reco.py](/agent/my_reco.py)。

```python
from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
# 如果 vscode 在这里报错了说明你没仔细看上一步

@AgentServer.custom_recognition("my_reco_222") # 注册识别方法
class MyRecongition(CustomRecognition):

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        
        # dosomething...

        return CustomRecognition.AnalyzeResult(
            box=(0, 0, 100, 100), # 传回识别到的区域
            detail="Hello World!"
        )
        # 或传回 None 表示识别失败
        # return CustomRecognition.AnalyzeResult(
        #     box=None, detail="World not found!"
        # )

```

当在 pipeline 中进入以下节点时则会调用 `MyRecongition` 的 `analyze` 方法。

```json
{
    ...
    "MyTask4": {
        "recognition": "Custom",
        "custom_recognition": "my_reco_222",
        ...
    }
}
```

#### 高级用法

请参考[其他内容](#其他内容)）

### 自定义动作

#### 基本结构

完整内容请参考 [my_action.py](/agent/my_action.py)。

```python
# my_action.py
...
@AgentServer.custom_action("my_action_111")
class MyCustomAction(CustomAction):
    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> bool:

        # dosomething...

        return True
```

当在 pipeline 中进入以下节点时则会调用 `MyCustomAction` 的 `run` 方法。

```json
{
    ...
    "MyTask4": {
        ...
        "action": "Custom",
        "custom_action": "my_action_111"
    }
}
```

#### 高级用法

请参考[其他内容](#其他内容)）

### 方法注册

在启动 AgentServer 前，需要先将方法注册到 AgentServer 中。

```python
# main.py
...
import my_action
import my_reco

def main():
    ...

    AgentServer.start_up(socket_id)
    AgentServer.join()
    AgentServer.shut_down()

if __name__ == "__main__":
    main()
```

<details>
<summary>
<b>原理说明</b>
</summary>

```python
# my_action.py
...
@AgentServer.custom_action("my_action_111")
class MyCustomAction(CustomAction):
    ...
```

虽然没有在 `main.py` 中进行显示调用，但这里利用了 python 的特性，在导入时会自动执行 `my_action.py` 中的 `@AgentServer.custom_action` 装饰器，将 `MyCustomAction` 注册到 `AgentServer` 中。

</details>
