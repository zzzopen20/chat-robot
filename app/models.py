from django.db import models

# Create your models here.
# 选择模型
class ModelClassModel(models.Model):
    name = models.CharField(max_length=20, verbose_name="大模型种类名")

    class Meta:
        db_table = "tb_model_class"

    def __str__(self):
        return self.name


# 新建会话窗口
class SessionWindowModel(models.Model):
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    show_content = models.CharField(max_length=30, verbose_name="展示内容", null=True)

    class Meta:
        db_table = "tb_session_window"
        ordering = ['-create_time']  #倒序，最新的放在前面

    def __str__(self):
        return self.show_content

# 会话历史记录
class SessionRecordsModel(models.Model):
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    session_window = models.ForeignKey(SessionWindowModel, related_name="window_records", on_delete=models.CASCADE, verbose_name="所属窗口")
    model_class = models.ForeignKey(ModelClassModel, related_name="records_model_class", on_delete=models.CASCADE, verbose_name="所属大模型类")
    session_content = models.TextField(verbose_name="单条会话记录")
    class Meta:
        db_table = "tb_session_records"
        ordering = ['create_time']
    def __str__(self):
        return self.session_content


# 知识库表
class KnowledgeBaseModel(models.Model):
    # 创建时间
    knowledge_base_name = models.CharField(max_length=10, unique=True, verbose_name="知识库名")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    chunk_size = models.IntegerField(verbose_name="每块最大长度")
    repeat = models.IntegerField(verbose_name="重复字符长度")

    class Meta:
        db_table = "tb_knowledge_base"
        # ordering = ['-create_time']

    def __str__(self):
        return self.knowledge_base_name

# 文件表
class FileModel(models.Model):
    file_name = models.CharField(max_length=20, verbose_name="文件名")
    file_type = models.CharField(max_length=10, verbose_name="文件类型")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    file_content = models.TextField()
    knowledge_base = models.ForeignKey(KnowledgeBaseModel, related_name="file_knowledge_base", on_delete=models.CASCADE, verbose_name="所属知识库")

    class Meta:
        db_table = "tb_knowledge_base_file"
        # ordering = ['-create_time']

    def __str__(self):
        return self.file_name

# 文件分块表
class FileChunkModel(models.Model):
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    file = models.ForeignKey(FileModel, related_name="file_chunk", on_delete=models.CASCADE, verbose_name="所属文件")
    knowledge_base = models.ForeignKey(KnowledgeBaseModel, related_name="file_chunk_knowledge_base", on_delete=models.CASCADE, verbose_name="所属知识库")
    file_chunk_content = models.TextField()

    class Meta:
        db_table = "tb_file_chunk"
        ordering = ['create_time']

    def __str__(self):
        return self.create_time