<template>
    <div>
        <h1>{{ knowledgeName }}</h1>
        <hr>
        <!-- <el-button type="primary" @click="importFile">导入文件</el-button> -->
        <!-- 导入文件按钮 -->
        <el-button type="primary" @click="importFile">导入文件</el-button>
        <!-- 文件选择器隐藏起来，通过按钮触发 -->
        <input type="file" ref="fileInput" @change="handleFileChange" style="display: none;" />
        <!-- 表格 -->
        <el-table :data="tableData" style="width: 100%">
            <!-- 表格列定义 -->
            <el-table-column prop="id" label="id" width="100"></el-table-column>
            <el-table-column prop="name" label="文件名称" width="180"></el-table-column>
            <el-table-column prop="fileType" label="文件类型" width="180"></el-table-column>
            <el-table-column prop="importTime" label="导入时间" width="180"></el-table-column>
            <el-table-column label="操作">
                <template v-slot:default="scope">
                    <!-- 根据当前行数据渲染按钮 -->
                    <!-- <el-button type="primary" size="mini" @click="editKnowledge(scope.row)">编辑</el-button> -->
                    <el-button type="success" size="mini" @click="viewKnowledge(scope.row)">查看</el-button>
                    <el-button type="danger" size="mini" @click="deleteKnowledge(scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
import instance from '@/plugins/axios';

export default {
    props: {
            id: String,
            name: String
    },
    data() {
            return {
                knowledgeName: '' ,// 初始化knowledgeName
                tableData: [
        // 表格数据示例
        // aciton里是三个按钮
        // { id: '1', name: '文件名1', fileType: 'txt', importTime: '2024-06-10' },
        ],
            };
    },     
    created() {
            // 在组件创建时设置knowledgeName
        this.knowledgeName = this.name;
            // 访问后端获取文件列表
            this.fetchData();
        },
    

    methods: {
        //  定义一个方法来获取后端数据
        fetchData() {
            // 使用axios或fetch等方法发起请求
            instance.get('upload/' + this.$route.params.id).then(response => {
            // 请求成功，将数据赋值给data属性
            this.tableData = response.data;
            console.log()
        })
        .catch(error => {
          // 请求失败处理
          console.error('Error fetching data:', error);
        });
    },
        // 查看知识库的逻辑
        viewKnowledge(row) {
        console.log('查看知识库', row)
        this.$router.push({
            name: 'fileDetail',
            params: {
                id: row.id, // 每行数据都有一个id属性
                name: row.name, //文件名名称
            }
        });
            instance.get('file_chunk/'+row.id).then(res => {
          console.log(res.data)
        })
      },
        // 删除知识库的逻辑
        deleteKnowledge(row) {
        console.log('删除知识库', row);
        },

        // importFile() {
        //     // 导入文件的逻辑
        //     console.log('导入文件');
        // },
        

        importFile() {
        // 触发文件选择器
        this.$refs.fileInput.click();
        },
    
        handleFileChange(event) {
        // 获取选中的文件
        const file = event.target.files[0];
        if (file) {
        // 这里可以添加文件处理逻辑，例如检查文件类型和大小
        if (this.isFileTypeAllowed(file)) {
            // 如果文件类型被允许，可以进行进一步处理，例如上传
            this.uploadFile(file);
        } else {
            alert('文件类型不被允许');
        }
      }
        },
        // 检查文件类型是否在允许的范围内
        isFileTypeAllowed(file) {
            const allowedTypes = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain', 'application/pdf'];
            return allowedTypes.includes(file.type);
        },
        // 上传文件
        uploadFile(file) {
                // 创建 FormData 对象
                const formData = new FormData();
                // 将文件添加到 FormData 对象中
                formData.append('file', file);
            // 可以使用 fetch 或 axios 发送文件到服务器
            alert('开始上传文件')
            console.log('开始上传文件:');
            // 想把知识库id放在路由上
            alert(this.$route.params.id)
            alert(file)
            instance.post('upload/' + this.$route.params.id, formData, {
                headers: {
                    // 设置请求头，告诉服务器这是一个 multipart/form-data 请求
                    'Content-Type': 'multipart/form-data'
                }
            }).then(response => {
                console.log(response);
                alert("上传文件成功");
                // 自动刷新文件列表
                this.fetchData()
            }).catch(error => {
                console.error(error);
                alert("上传文件失败");
            });

    }
  }
            
    }
    

</script>