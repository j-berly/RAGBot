from pydantic import BaseModel
import streamlit as st
from llama_index.agent.types import BaseAgent
from llama_index.tools import FunctionTool
from llama_index.agent.react.formatter import ReActChatFormatter
from utils.agent_builder import RAGAgent
from utils.llm_builder import BUILDER_LLM, LLMReAct
from typing import List
from typing import Callable
from prompts import REACT_CHAT_SYSTEM_HEADER
from llama_index.agent import ReActAgent


class CurrentSession(BaseModel):
    class Config:
        arbitrary_types_allowed = True
    rag: RAGAgent
    llm: BaseAgent


def get_state():
    """
    get current state about llm and rag agent
    :return: CurrentSession
    """
    if 'llm' not in st.session_state.keys() or st.session_state.llm is None \
            or 'rag' not in st.session_state.keys() or st.session_state.rag is None:
        rag_agent = RAGAgent(llm=BUILDER_LLM)
        fns: List[Callable] = [
            rag_agent.load_data,
            rag_agent.create_agent
        ]
        fn_tools: List[FunctionTool] = [FunctionTool.from_defaults(fn=fn) for fn in fns]
        llm_react = ReActAgent.from_tools(
            tools=fn_tools,
            llm=BUILDER_LLM,
            react_chat_formatter=ReActChatFormatter(
                system_header=rag_agent.system_prompt + "\n" + REACT_CHAT_SYSTEM_HEADER,
            ),
            verbose=True,
        )
        st.session_state.rag = rag_agent
        st.session_state.llm = llm_react
    return CurrentSession(rag=st.session_state.rag, llm=st.session_state.llm)
