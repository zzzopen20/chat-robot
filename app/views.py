import os

from django.http import StreamingHttpResponse
from django.shortcuts import render
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferMemory
from rest_framework.views import APIView
from rest_framework.response import Response
from http import HTTPStatus
from dashscope import Generation
from app.models import KnowledgeBaseModel, FileModel, FileChunkModel

from app.models import SessionWindowModel

# 阿里多轮
class ChatView(APIView):
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
    def post(self, request):
        # 获取前端传来的用户问题
        question = request.data.get("question")
        # messages为什么爆红？

        self.messages.append({'role': 'user', 'content':question})

        response = Generation.call(model="qwen-turbo",
                                   messages=self.messages,
                                   # 将输出设置为"message"格式
                                   result_format='message')
        if response.status_code == HTTPStatus.OK:
            # print(response)
            # 将assistant的回复添加到messages列表中
            self.messages.append({'role':'assistant','content': response.output.choices[0]['message']['content']})
            return Response({'code':200,'message': response.output.choices[0]['message']['content']})
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
            # 如果响应失败，将最后一条user message从messages列表里删除，确保user/assistant消息交替出现
            messages = self.messages[:-1]

# 阿里流
def generate_sse(responses):
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            data1 = response.output.choices[0]['message']['content']
            data = f"data: {data1}\n\n"
            if data1:
                yield data.encode('utf-8')  # 必须编码为字节串
            else:
                return "no message"

ssemessages = []
def ssechat(request):
    question = request.GET.get('question')  # 调用函数获取用户输入
    print(11111,question)

    ssemessages.append({"role": "user", "content": question})

    responses = Generation.call(model="qwen-turbo",
                                messages=ssemessages,
                                result_format='message',
                                stream=True,  # 设置输出方式为流式输出
                                incremental_output=False  # 增量式流式输出
                                )

    response = StreamingHttpResponse(
        generate_sse(responses),
        content_type="text/event-stream",
    )
    response["Cache-Control"] = "no-cache"
    print(666,response)
    return response


# RAG
from langchain_community.llms import Tongyi
class LangchainView(APIView):
    # 设置为类属性，都会使用同一个 memory 对象，聊天机器人才能够记住之前的对话
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    def post(self, request):
        llms = Tongyi()
        question = request.data.get("question")
        switch = request.data.get("switchValue")
        # print(111,switch) True/False
        # print(type(switch))  布尔值

        session_id = request.data.get("session_id")
        try:
            session = SessionWindowModel.objects.get(id=session_id)
        except Exception as e:
            print(e)
            return Response({'code': 400, 'message': 'session_id错误'})
        sessions = session.window_records.all()  # 反向查询
        if not sessions:  #如果没有会话内容
            # print("♥♥♥♥♥♥♥♥♥♥♥♥")
            session.show_content = question
            session.save()
            # print("***********",session.show_content)

        if switch:   #开了知识库
            # 加载文档
            from langchain_community.document_loaders import TextLoader
            # 实例化TextLoader对象
            # 读取文件---相对路径不行，就用绝对路径
            loader = TextLoader('D:/AI-P4/aichat/app/cfpl.txt', encoding="utf-8")
            docs = loader.load()

            #文档分割
            from langchain.text_splitter import CharacterTextSplitter
            # 实例化
            text_splitter = CharacterTextSplitter(
                separator="\n", chunk_size=200, chunk_overlap=0)
            doc = text_splitter.split_documents(docs)

            # 向量化，创建知识库
            # 引入向量化的类
            from langchain_community.vectorstores import Chroma
            from langchain.embeddings.dashscope import DashScopeEmbeddings
            # 实例化，使用阿里千问的嵌入模型将文档转换为向量
            embeddings = DashScopeEmbeddings()
            # 创建向量数据库,向量化文档---doc是分割好的文档，embeddings是向量实例，persist_directory指定一个目录，用于持久化存储向量数据和元数据
            db = Chroma.from_documents(doc, embedding=embeddings, persist_directory="./chroma1")

            # 检索问答
            from langchain.chains import RetrievalQA

            # 实例化
            qa = RetrievalQA.from_chain_type(
                llm=llms, chain_type="stuff", retriever=db.as_retriever())
            ret = qa.invoke(question)
            print(ret)
            return Response({"code": 200, 'message': ret['result']})
        else:  #没有开知识库
            print(000)
            from langchain_core.messages import SystemMessage
            from langchain_core.prompts import (
                ChatPromptTemplate,
                HumanMessagePromptTemplate,
                MessagesPlaceholder,
            )
            # 实现有记忆的多轮会话
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
                    ),
                ]
            )
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            print(20202020202020,memory)
            chat_llm_chain = LLMChain(
                llm=llms,
                prompt=prompt,
                verbose=True,
                memory=self.memory, ## 使用类属性的memory
            )
            ret=chat_llm_chain.predict(human_input=question)


            from .models import SessionRecordsModel
            # 保存会话内容
            SessionRecordsModel.objects.create(session_window=session, session_content="Q:"+question+"\n"+"A:"+ret+"\n", model_class_id=1)
            print(ret)
            return Response({"code": 200, 'message': ret})


# 历史会话列表
class HistoryView(APIView):
    def get(self,request):
        session_window = SessionWindowModel.objects.all()
        history = []
        for item in session_window:
            history.append({
                "id": item.id,
                "show_content": item.show_content
            })
        return Response({"code": 200, 'message': history})
    def post(self,request):  #新建会话
        from app.models import SessionWindowModel
        session_window = SessionWindowModel.objects.create()
        # print("-----------",session_window)
        print(6666666)
        return Response({"code": 200, 'message': "新建成功", "id": session_window.id})

# 根据历史会话的id,查询会话记录内容
class ContentsView(APIView):
    def get(self,request):
        id = request.query_params.get("id")  #查询参数?id=1
        # 根据会话id查内容
        from app.models import SessionRecordsModel
        contents = SessionRecordsModel.objects.filter(session_window=id)
        contents_list = []
        for item in contents:
            contents_list.append({
                "id": item.id,
                "session_content": item.session_content
            })
        return Response({"code": 200, 'message': contents_list})


# 新增知识库
class AddknowledgeBase(APIView):
    def post(self,request):
        knowledge_base_name = request.data.get("knowledgeBaseName")
        chunk_size = request.data.get("chunkSize")
        repeat = request.data.get("repeatLength")
        KnowledgeBaseModel.objects.create(knowledge_base_name=knowledge_base_name,chunk_size=chunk_size,repeat=repeat)
        return Response({"code": 200, 'message': "新增成功"})

# 获取知识库列表
class KnowledgeBaseList(APIView):
    def get(self,request):
        knowledge_base_list = KnowledgeBaseModel.objects.all()
        knowledge_base_list_data = []
        for item in knowledge_base_list:
            knowledge_base_list_data.append({
                "id": item.id,
                "name": item.knowledge_base_name,
                "createtime": item.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "chunksize": item.chunk_size,
                "repeat": item.repeat
            })
        return Response({"code": 200, 'data': knowledge_base_list_data})


# 上传文件,获取文件列表
class UploadView(APIView):
    def post(self,request,pk):   #pk是知识库id
        # print(pk)
        # 前端传过来的文件，怎么获取
        file = request.FILES.get("file")   #NBA新闻.txt
        # print(file.name)  #NBA新闻.txt
        # print(file.content_type)  #text/plain
        file_type = file.name.split(".")[-1]    #txt,pdf


        # print(file.read().decode('utf-8')) #随着约基奇的崛起，丹佛掘金队在过去几个赛季中
        # 路径参数获取
        knowledge_base = KnowledgeBaseModel.objects.get(id=pk)
        # FileModel.objects.create(file_name=file.name,file_type=file_type,file_content=file.read().decode('utf-8'),knowledge_base=knowledge_base)
        ######辉前-----------------------------------------------辉后####
        # 1.保存文件----把文件保存在django项目中
        with open ("D:/AI-P4/aichat/app/"+file.name, "wb") as f:
            f.write(file.read())
        # 2.分类型加载文档load---txt格式
        if file_type == "txt":
            from langchain_community.document_loaders import TextLoader
            # 实例化TextLoader对象
            loader = TextLoader("D:/AI-P4/aichat/app/"+file.name, encoding="utf-8")
            # 加载文档
            docs = loader.load()
            # print(docs)
        # 分类型加载文档load---pdf格式
        elif file_type == "pdf":
            from langchain_community.document_loaders import PyPDFium2Loader
            loader = PyPDFium2Loader("D:/AI-P4/aichat/app/"+file.name)
            docs = loader.load()
            # print(docs)
        # 分类型加载文档load---docx格式
        elif file_type == "docx":
            from langchain_community.document_loaders import Docx2txtLoader
            loader = Docx2txtLoader("D:/AI-P4/aichat/app/"+file.name)
            docs = loader.load()
            # print(docs)
        else:
            return Response({"code":000, 'message': "加载文档失败，可能是文件格式错误"})
        # 3.文档分割
        from langchain.text_splitter import CharacterTextSplitter
        # 实例化
        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=knowledge_base.chunk_size,
          chunk_overlap=knowledge_base.repeat)
        # 对文件内容进行分割
        docs_splitter = text_splitter.split_documents(docs)
        # print(docs_splitter)
        # 4.向量化，创建向量数据库，向量化文档----还债了
        # 引入向量化的类
        from langchain_community.vectorstores import Chroma
        from langchain.embeddings.dashscope import DashScopeEmbeddings

        # 实例化
        embeddings = DashScopeEmbeddings()

        # 获取该知识库中是否有数据,反向查询
        knowledge_base_file_list = knowledge_base.file_knowledge_base.all()
        if not knowledge_base_file_list:
            # 创建向量数据库,向量化文档
            db = Chroma.from_documents(docs_splitter, embeddings,
                                       persist_directory="./chroma/" + knowledge_base.knowledge_base_name)
            db.persist()

        else:
            # 对数据进行加载
            db = Chroma(persist_directory="./chroma/" + knowledge_base.knowledge_base_name,
                        embedding_function=embeddings)
            print(1111111111111111111111111111111111111111111111111111111111111)
            print(db.__len__())

            # 添加文档
            # 添加文档的方法
            db.add_documents(docs_splitter)
            print(22222222222222222)
            print(db.__len__())

        # 将文件内容信息存入mysql数据库
        knowledge_base_file = FileModel.objects.create(file_name=file.name,
                                                       file_type=file_type,
                                                       file_content=docs[0].page_content,
                                                       knowledge_base=knowledge_base)

        # 将分割后的文件内容存入分割表中
        for item in docs_splitter:
            FileChunkModel.objects.create(file=knowledge_base_file,
                                          file_chunk_content=item.page_content,
                                          knowledge_base=knowledge_base, )

        # 删除前端存入django的文件
        os.remove("D:/AI-P4/aichat/app/"+file.name)

        return Response({"code": 200, 'message': "添加文件成功"})
    def get(self,request,pk):
        knowledge_base = KnowledgeBaseModel.objects.get(id=pk)
        file_list = FileModel.objects.filter(knowledge_base=knowledge_base)
        file_list_data = []
        for item in file_list:
            file_list_data.append({
                "id": item.id,
                "name": item.file_name,
                "fileType": item.file_type,
                # "importTime": item.create_time.strftime()
                "importTime": item.create_time.strftime('%Y年%m月%d日 %H时%M分%S秒')
            })
        return Response({"code": 200, 'data': file_list_data})

# 添加文件、文件分块、向量化、创建向量化知识库或存入向量化知识库
def receive_front_end_file(file, knowledge_id):
    # 获取该知识库信息，即相关参数
    try:
        knowledge_base = KnowledgeBaseModel.objects.get(id=knowledge_id)
    except Exception as e:
        print(e)
        return "该知识库不存在"

    # 将前端传来的二进制文件存入django中
    print(file.name)
    with open(file.name, "wb") as f:
        f.write(file.read())

    # 在分割前先判断文件类型，根据对应类型进行切割，支持txt、pdf、docx格式
    file_type = file.name.split(".")[-1]
    print(file_type)
    if file_type == "txt":
        from langchain_community.document_loaders import TextLoader
        # 实例化TextLoader对象
        loader = TextLoader(file.name, encoding="utf-8")
        # 加载文档
        docs = loader.load()
        print(docs)


    elif file_type == "pdf":
        from langchain_community.document_loaders import PyPDFium2Loader

        # 加载PDF文件
        loader = PyPDFium2Loader(file.name)
        docs = loader.load()
        print(docs)
    elif file_type == "docx":
        from langchain_community.document_loaders import Docx2txtLoader

        # 加载docx
        loader = Docx2txtLoader(file.name)
        docs = loader.load()
        print(docs)
    else:
        return "文件类型错误"

    # 导入分割类
    from langchain.text_splitter import CharacterTextSplitter

    # 实例化
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=knowledge_base.maximum_block_length,
                                          chunk_overlap=knowledge_base.repeated_character_length)
    # 对文件内容进行分割
    docs_splitter = text_splitter.split_documents(docs)
    # print(docs_splitter)

    # 引入向量化的类
    from langchain_community.vectorstores import Chroma
    from langchain.embeddings.dashscope import DashScopeEmbeddings

    # 实例化
    embeddings = DashScopeEmbeddings()

    # 获取该知识库中是否有数据,反向查询
    knowledge_base_file_list = knowledge_base.file_knowledge_base.all()
    if not knowledge_base_file_list:
        # 创建向量数据库,向量化文档
        db = Chroma.from_documents(docs_splitter, embeddings, persist_directory="./chroma/"+knowledge_base.knowledge_base_name)
        db.persist()

    else:
        # 对数据进行加载
        db = Chroma(persist_directory="./chroma/"+knowledge_base.knowledge_base_name, embedding_function=embeddings)
        print(db.__len__())

        # 添加文档
        # 添加文档的方法
        db.add_documents(docs_splitter)
        print(db.__len__())

    # 将文件内容信息存入mysql数据库
    knowledge_base_file = FileModel.objects.create(file_name=file.name,
                                                   file_type=file_type,
                                                   file_content=docs[0].page_content,
                                                   knowledge_base=knowledge_base)

    # 将分割后的文件内容存入分割表中
    for item in docs_splitter:
        FileChunkModel.objects.create(file=knowledge_base_file,
                                      file_chunk_content=item.page_content,
                                      knowledge_base=knowledge_base,)

    # 删除前端存入django的文件
    os.remove(file.name)

    return "文件添加到各库成功"

# 文件每块内容
class FileChunkView(APIView):
    def get(self,request,pk):
        target_file = FileModel.objects.get(id=pk)
        file_chunks = FileChunkModel.objects.filter(file=target_file)
        file_chunk_list=[]
        for item in file_chunks:
            print(item.file_chunk_content)
            print("-------------------------------------------------")
            file_chunk_list.append({
                "content": item.file_chunk_content
            })
        return Response({"code": 200, 'data': file_chunk_list})