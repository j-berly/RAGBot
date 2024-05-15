from llama_index.agent import ReActAgent
from llama_index.agent.react.formatter import ReActChatFormatter
from typing import List, cast, Optional, Type
from llama_index.tools import BaseTool
from llama_index.llms.base import LLM
from llama_index.memory import BaseMemory, ChatMemoryBuffer
from llama_index.llms import LlamaCPP, ChatMessage
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt

BUILDER_LLM = LlamaCPP(
    # You can pass in the URL to a GGML model to download it automatically
    model_url='https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/blob/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf',
    # model_path=r'models\mistral-7b-instruct-v0.2.Q4_K_M.gguf',
    temperature=0.1,
    max_new_tokens=4096,
    # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
    context_window=4096,
    # kwargs to pass to __call__()
    generate_kwargs={},
    # kwargs to pass to __init__()
    # set to at least 1 to use GPU
    model_kwargs={"n_gpu_layers": -1},
    # transform inputs into Llama2 format
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=True,
)


class LLMReAct(ReActAgent):
    def __init__(self):
        super().__init__()