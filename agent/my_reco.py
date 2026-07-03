from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context


# 数字比大小并返回较小的
@AgentServer.custom_recognition("my_reco_222")
class MyRecongition(CustomRecognition):

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:

        rois = [
            [100, 100, 200, 100],
            [300, 100, 200, 100],
        ]

        res = []

        for roi in rois:
            # 找到 pipeline 中名为 "MyCustomOCR" 的节点，并执行他的识别逻辑
            reco_detail = context.run_recognition(
                "MyCustomOCR",
                argv.image,  # 使用当前获取到的图片
                pipeline_override={  # 临时覆盖节点参数
                    "MyCustomOCR": {  # 要覆盖的节点的名称
                        "roi": roi,  # 覆盖识别区域
                        "only_rec": True,  # 不进行文本检测，直接进行识别
                    }
                },
            )

            if reco_detail is None or not reco_detail.hit:
                print(f"无法读取到内容 {roi}")
                res.append(None)
                continue

            text = str(reco_detail.best_result.text)
            if not text.isdigit():
                print(f"{text} 不是数字!")
                res.append(None)
                continue

            res.append(float(text))

        if not res or None in res:
            return CustomRecognition.AnalyzeResult(
                box=None,
                detail="存在无法读取到内容",
            )

        min_index = res.index(min(res))
        return CustomRecognition.AnalyzeResult(
            box=rois[min_index], detail=f"最小值是 {res[min_index]}"
        )
