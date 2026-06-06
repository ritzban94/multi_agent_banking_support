from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from Constants import MODEL_GPT, MODEL_GPT_USER_INIT_MESSAGE, MODEL_GPT_SYS_INIT_MESSAGE

class LlmClient:
    """
    A wrapper class for creating LLM instance
    """
    _llm = None

    def __init__(self):
        load_dotenv()
        self._llm = LiteLlm(model=MODEL_GPT)
        self.init_llm_client()

    def init_llm_client(self):
        self._llm.llm_client.completion(
            model=self._llm.model,
            messages=[
                {"role": "system", "content": MODEL_GPT_SYS_INIT_MESSAGE},
                {"role": "user", "content": MODEL_GPT_USER_INIT_MESSAGE}
            ],
            temperature=0.1,
            tools=[]
        )

    def get_llm_client(self):
        return self._llm
    
llm_client = LlmClient()