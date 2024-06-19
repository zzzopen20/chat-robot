
from django.urls import path
from .views import *
urlpatterns = [
    path('chat/',ChatView.as_view()),
    # path('chat/',generate_sse), # 阿里流
    path('ssechat/',ssechat,name='ssechat'),
    path('langchain/',LangchainView.as_view()),
    path('history/',HistoryView.as_view()),  # 历史会话列表展示
    path('contents/',ContentsView.as_view()),  #会话内容
    path('addknowledgeBase/',AddknowledgeBase.as_view()), #新增知识库
    path('get_knowledge_base_list/',KnowledgeBaseList.as_view()), #知识库列表
    path('upload/<int:pk>',UploadView.as_view()), #上传导入文件
    path('file_chunk/<int:pk>',FileChunkView.as_view()), # 文件块内容

]