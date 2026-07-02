from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context


@AgentServer.custom_action("my_action_111")
class MyCustomAction(CustomAction):

    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> bool:

        print("my_action_111 is running!")

        # 执行点击
        click_job = context.tasker.controller.post_click(10, 20)
        # 等待点击完成，这一步必须有！
        click_job.wait()

        return True
