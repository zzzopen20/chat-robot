from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Tongyi
from rest_framework.response import Response
from rest_framework.views import APIView
class LangchainView(APIView):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    def post(self, request):
        llms = Tongyi()
        question = request.data.get("question")
        from langchain_core.messages import SystemMessage
        from langchain_core.prompts import (
                ChatPromptTemplate,
                HumanMessagePromptTemplate,
                MessagesPlaceholder,
            )
        prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(
                        content="You are a chatbot having a conversation with a human."
                    ),  # The persistent system prompt
                    MessagesPlaceholder(
                        variable_name="chat_history"
                    ),  # Where the memory will be stored.
                    HumanMessagePromptTemplate.from_template(
                        "{human_input}"
                    ),  # Where the human input will injected
                ]
            )

        chat_llm_chain = LLMChain(
                llm=llms,
                prompt=prompt,
                verbose=True,
                memory=self.memory,
            )
        ret=chat_llm_chain.predict(human_input=question)
        print(ret)
        return Response({"code": 200, 'message': ret})