<template>
    <!-- <div class="flex flex-wrap gap-4">
        <el-card style="width: 1200px;text-align: center; display: flex; align-items: center; justify-content: center;"
            shadow="hover">文件块中的内容</el-card>
        <br>
        <el-card style="width: 1200px;text-align: center; display: flex; align-items: center; justify-content: center;"
            shadow="hover">文件块中的内容</el-card>
        <br>
        <el-card style="width: 1200px;text-align: center; display: flex; align-items: center; justify-content: center;"
            shadow="hover">文件块中的内容</el-card>
        <br>
        <el-card style="width: 1200px;text-align: center; display: flex; align-items: center; justify-content: center;"
            shadow="hover">文件块中的内容</el-card>
        <br>
        <el-card style="width: 1200px;text-align: center; display: flex; align-items: center; justify-content: center;"
            shadow="hover">文件块中的内容</el-card>
        <br>
        <el-card style="width: 1200px;text-align: center; display: flex; align-items: center; justify-content: center;"
            shadow="hover">文件块中的内容</el-card>
        <br>
        <el-card style="width: 1200px;text-align: center; display: flex; align-items: center; justify-content: center;"
            shadow="hover">文件块中的内容</el-card>
        <br>
        <br>
        <el-card style="width: 1200px;text-align: center; display: flex; align-items: center; justify-content: center;"
            shadow="hover">文件块中的内容</el-card>
    </div> -->
    <div class="flex flex-wrap gap-4">
        <el-card class="chunk" v-for="(item, index) in fileChunks" :key="index"
            style="width: 1200px; text-align: center; display: flex; align-items: center; justify-content: center;"
            shadow="hover">
            {{ item.content }} <!-- 假设每个文件块有content字段 -->
        </el-card>
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
            fileChunks: [] // 初始化一个空数组来存放文件块数据
        };
    },
    created() {
        // 访问后端获取文件列表
        this.fetchData();
    },
    methods: {
        //  定义一个方法来获取后端数据
        fetchData() {
            // 路由上的id
            instance.get('file_chunk/' + this.$route.params.id).then(response => {
                // 把返回数据渲染到页面上
                // 假设后端返回的数据是一个对象数组，每个对象代表一个文件块
                this.fileChunks = response.data; // 将获取到的数据赋值给fileChunks
                console.log(response.data)
            })
                .catch(error => {
                    // 请求失败处理
                    console.error('Error fetching data:', error);
                });
        },
    }
}
</script>
<style scoped>
.chunk {
    /* white-space: pre-wrap; */
    /* 如果你想保持一定的间距，可以设置 margin-bottom */
    margin-bottom: 40px;
    /* 或者任意你认为合适的间距 */
}
</style>