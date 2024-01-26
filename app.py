import langchain
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.schema import HumanMessage, AIMessage
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory


def load_prompt(content):

	template = """You are an expert educator, and are responsible for walking the user \
	through this lesson plan. You should make sure to guide them along, \
	encouraging them to progress when appropriate. \
	If they ask questions not related to this getting started guide, \
	you should politely decline to answer and remind them to stay on topic.

	Please limit any responses to only one concept or step at a time. \
	Each step show only be ~5 lines of code at MOST. \
	Only include 1 code snippet per message - make sure they can run that before giving them any more. \
	Make sure they fully understand that before moving on to the next. \
	This is an interactive lesson - do not lecture them, but rather engage and guide them along!
	-----------------

	{content}
	
	-----------------
	End of Content.

	Now remember short response with only 1 code snippet per message.""".format(content=content)

	prompt_template = ChatPromptTemplate(messages = [
		SystemMessage(content=template), 
		MessagesPlaceholder(variable_name="chat_history"), 
		HumanMessagePromptTemplate.from_template("{input}")
		])
	return prompt_template

def load_prompt_with_questions(content):

	template = """You are an expert educator, and are responsible for walking the user \
	through this lesson plan. You should make sure to guide them along, \
	encouraging them to progress when appropriate. \
		make the content too fun to learn and wearry wearry easy and clear explanation so that a person with 0 knowldge can aslo understand and remeber it with out any hustle \
	If they ask questions not related to this getting started guide, \
	you should politely decline to answer and remind them to stay on topic.\
	You should ask them questions about the instructions after each instructions \
	and verify their response is correct before proceeding to make sure they understand \
	the lesson. If they make a mistake, give them good explanations and encourage them \
	to answer your questions, instead of just moving forward to the next step. 
	explain them in detail if they make a mistake.

	Please limit any responses to only one concept or step at a time. \
	plesase ask one question at a time and wait for the response. \
	check weather the response is ai generated or human generated. if it is ai generated politely denay and ask to right again \
	Each step show only be ~5 lines of code at MOST. \
	Only include 1 code snippet per message - make sure they can run that before giving them any more. \
	Make sure they fully understand that before moving on to the next. \
	This is an interactive lesson - do not lecture them, but rather engage and guide them along!\
	-----------------

	{content}


	-----------------
	End of Content.

	Now remember short response with only 1 code snippet per message and ask questions\
	to test user knowledge right after every short lesson.
	
	Your teaching should be in the following interactive format:
	
	Short lesson 3-5 sentences long
	Questions about the short lesson (1-3 questions)

	Short lesson 3-5 sentences long
	Questions about the short lesson (1-3 questions)
	...

	 """.format(content=content)

	prompt_template = ChatPromptTemplate(messages = [
		SystemMessage(content=template), 
		MessagesPlaceholder(variable_name="chat_history"), 
		HumanMessagePromptTemplate.from_template("{input}")
		])
	return prompt_template

load_dotenv()





st.set_page_config(page_title="C lang: Getting Started Class", page_icon="C")
st.title("C lang: Getting Started Class")
button_css =""".stButton>button {
    color: #4F8BF9;
    border-radius: 50%;
    height: 2em;
    width: 2em;
    font-size: 4px;
}"""
st.markdown(f'<style>{button_css}</style>', unsafe_allow_html=True)


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

from langchain.chat_models import ChatOpenAI





with open("lesson.txt") as f:
    lesson = f.read()

# from get_prompt import load_prompt



prompt_template = load_prompt(content = lesson)

from langchain.chains import LLMChain



if "messages" not in st.session_state:
    st.session_state["messages"] = [AIMessage(content="Welcome! This short course with help you started with C Language . Let me know when you're ready to proceed!")]

for msg in st.session_state["messages"]:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    else:
        st.chat_message("assistant").write(msg.content)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        model = ChatOpenAI(streaming=True, callbacks=[stream_handler], model="gpt-3.5-turbo-16k")
        #model = ChatAnthropic(streaming=True, callbacks=[stream_handler], model="claude-2")
        chain = LLMChain(prompt=prompt_template, llm=model)

        response = chain({"input":prompt, "chat_history":st.session_state.messages[-20:]}, include_run_info=True)
        st.session_state.messages.append(HumanMessage(content=prompt))
        st.session_state.messages.append(AIMessage(content=response[chain.output_key]))
        run_id = response["__run"].run_id

       
