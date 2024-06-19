<template>
    <h2>添加知识库</h2>
    <el-form :model="form" label-width="100px">
        <el-form-item label="知识库名称">
            <el-input v-model="form.knowledgeBaseName"></el-input>
        </el-form-item>
        <el-form-item label="切块大小">
            <el-input-number v-model="form.chunkSize"></el-input-number>
        </el-form-item>
        <el-form-item label="重复长度">
            <el-input-number v-model="form.repeatLength"></el-input-number>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="submitForm">提交</el-button>
        </el-form-item>
    </el-form>
</template>

<script>
import instance from '@/plugins/axios';
export default {
    data() {
        return {
            form: {
                knowledgeBaseName: '',
                chunkSize: 0,
                repeatLength: 0
            }
        }
    },
    methods: {
        submitForm() {
            // 添加提交表单的逻辑
            console.log('Form submitted:', this.form);
            alert('Form submitted:', this.form)
            //  传给后端
            instance.post('addknowledgeBase/', this.form).then(res => {
                console.log(res)
                alert("新增知识库成功")
                // 自动刷新历史会话列表
                // this.history_list();
            })



        }
    }
}
</script>

<style></style>