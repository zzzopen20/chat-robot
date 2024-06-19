# Generated by Django 4.2.2 on 2024-06-10 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeBaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('knowledge_base_name', models.CharField(max_length=10, unique=True, verbose_name='知识库名')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('chunk_size', models.IntegerField(verbose_name='每块最大长度')),
                ('repeat', models.IntegerField(verbose_name='重复字符长度')),
            ],
            options={
                'db_table': 'tb_knowledge_base',
                'ordering': ['-create_time'],
            },
        ),
    ]
