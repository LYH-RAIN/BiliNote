from typing import Optional, Union

from openai import OpenAI

from app.utils.logger import get_logger

logging= get_logger(__name__)
class OpenAICompatibleProvider:
    def __init__(self, api_key: str, base_url: str, model: Union[str, None]=None):
        # 针对阿里云DashScope API的特殊处理
        if 'dashscope.aliyuncs.com' in base_url:
            # 阿里云不需要Bearer前缀，直接使用API Key
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url,
                default_headers={
                    "Authorization": f"{api_key}",  # 不使用Bearer
                }
            )
        else:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    @property
    def get_client(self):
        return self.client

    @staticmethod
    def test_connection(api_key: str, base_url: str) -> bool:
        try:
            client = OpenAI(api_key=api_key, base_url=base_url)
            model = client.models.list()
            # for segment in model:
            #     print(segment)
            # print(model)
            logging.info("连通性测试成功")
            return True
        except Exception as e:
            logging.info(f"连通性测试失败：{e}")

            # print(f"Error connecting to OpenAI API: {e}")
            return False