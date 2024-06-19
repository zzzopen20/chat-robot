<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="200px" class="left">
        <br>
        <el-switch v-model="temp.switchValue" @change="handleSwitchChange" /> <span>RAG开关</span>
        <br><br>
        <!-- 下拉列表 -->
        <div>
          <select v-model="selectedValue">
            <option disabled value="">模型选择</option>
            <option v-for="option in options" :key="option.value" :value="option.value">
              {{ option.text }}
            </option>
          </select>
        </div>
        <!-- 知识库管理 -->
        <el-button type="primary" :icon="Edit" @click="manageKnowledge">知识库管理</el-button>
        <br><br>
        <!-- 新建会话 -->
        <el-button type="primary" :icon="Edit" @click="new_session">新建会话</el-button>
        <!-- 历史会话列表 -->
        <ul list-style: none>
          <li v-for="(item, index) in history" :key="index">
            <button @click="handleClick(item.id)" class="li_button">{{ item.show_content }}</button>
          </li>
        </ul>

      </el-aside>
      <el-main class="right">
        <div v-if="!isKnowledgeManagement">
          <!-- 问题:<input v-model="temp.question" /> <br /> -->
          <el-input v-model="temp.question" placeholder="Please input" />
          <br>
          <!-- <button @click="add">提交</button> -->
          <el-button type="primary" plain :icon="Edit" @click="add">提交</el-button>
          <!--阿里流 <div style="white-space: pre-line;" v-html="text">
            </div> -->
          <div style="white-space: pre-line;font-size:x-large;">
            {{ answer }}
          </div>
        </div>

        <div v-else>
          <button @click="addKnowledgeBase">添加知识库</button>&nbsp;&nbsp;<button @click="exitManageKnowledge">退出管理</button>
          <!-- 表格 -->
          <el-table :data="tableData" style="width: 100%">
            <!-- 表格列定义 -->
            <el-table-column prop="id" label="id" width="100"></el-table-column>
            <el-table-column prop="name" label="知识库名称" width="180"></el-table-column>
            <el-table-column prop="createtime" label="创建时间" width="180"></el-table-column>
            <el-table-column prop="chunksize" label="块大" width="100"></el-table-column>
            <el-table-column prop="repeat" label="重复" width="100"></el-table-column>

            <el-table-column label="操作">
              <template v-slot:default="scope">
                <!-- 根据当前行数据渲染按钮 -->
                <el-button type="primary" size="mini" @click="editKnowledge(scope.row)">编辑</el-button>
                <el-button type="success" size="mini" @click="viewKnowledge(scope.row)">查看</el-button>
                <el-button type="danger" size="mini" @click="deleteKnowledge(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-main>

    </el-container>
  </div>



</template>

<script>
import { ArrowDown } from '@element-plus/icons-vue'
import { ElFormItem, radioGroupKey } from 'element-plus'
// 导包axios---instance是实例
import instance from "../plugins/axios"
import { ref } from 'vue'
// 下拉列表


export default {
  data() {
    return {
      isKnowledgeManagement: false, // 控制是否显示知识库管理界面
      tableData: [
        // 表格数据示例,键和后代一致
        // { id: '1', name: '库1', createtime: '2024-06-10', chunksize: '100', repeat: '0' },
        // 数据是访问后端get_knowledge_base_list/获取的数据


      ],
      // 下拉列表
      selectedValue: '', // 用于绑定选中的值
      options: [
        { value: 'option1', text: '通义千问' },
        { value: 'option2', text: '文心一言' },
      ],

      // 给后端传,必须是字典格式
      temp: {
        question: "",
        switchValue: false,
        session_id: 0,

      },
      answer: "",
      history: [], //历史会话列表
      current_session_id: 0, //当前会话id

    }
  },
  // 阿里流
  // computed: {
  //   text() {
  //    let q = "Q:" + this.temp.question
  //    let a = "A:" + this.answer

  //    return q + "<br>" + a
  //   }
  // },
  methods: {
    handleSwitchChange(value) {
      console.log('Switch value changed:', value);
    },
    // 切换到知识库管理界面
    manageKnowledge() {
      this.isKnowledgeManagement = true;
      // 访问数据库
      instance.get('get_knowledge_base_list/').then(res => {
        console.log(res.data)
        this.tableData = res.data
      })
    },
    editKnowledge(row) {
      // 编辑知识库的逻辑
      console.log('编辑知识库', row);
    },
    deleteKnowledge(row) {
      // 删除知识库的逻辑
      console.log('删除知识库', row);
    },
    viewKnowledge(row) {
      // 查看知识库的逻辑
      console.log('查看知识库', row)
      this.$router.push({
        name: 'KnowledgeDetail',
        params: {
          id: row.id, // 假设每行数据都有一个id属性
          name: row.name, // 知识库名称
        }
      });
    },
    // 添加知识库
    addKnowledgeBase() {
      console.log('添加知识库');
      alert('添加知识库')
      this.$router.push({
        name: 'AddKnowledgeBase',
      });
    },

    // 退出知识库管理界面
    exitManageKnowledge() {
      this.isKnowledgeManagement = false;
    },
    // 阿里多轮 提问
    add() {
      //调用 接口，
      alert(this.current_session_id)
      if (this.selectedValue == "") {
        alert("请选择模型")
        return
      }

      else if (this.selectedValue == "option2") {
        alert("选择了文心一言")
        alert("拉倒吧，还没写后端")
        return
      }
      else if (this.selectedValue == "option1") {
        alert("选择了通义千问")
        this.temp.session_id = this.current_session_id
        this.answer += "Q:" + this.temp.question + "\n"
        instance.post('langchain/', this.temp).then(res => {
          console.log(res)
          this.answer += "A:" + res.message + "\n"
          // 自动刷新历史会话列表
          this.history_list();
        })
      }



    },
    // 历史会话列表
    history_list() {
      instance.get('history/').then(res => {
        console.log(res)
        this.history = res.message
      })
    },
    // 根据历史id获取对话内容记录
    handleClick(id) {
      this.current_session_id = id
      this.answer = ""
      instance.get('contents/?id=' + id).then(res => {
        console.log(res)
        for (let i = 0; i < res.message.length; i++) {
          this.answer += res.message[i].session_content + "\n\n"
        }
      })
    },
    // 新建会话
    new_session() {
      alert("已新建会话")
      // 刷新右边问答区
      this.answer = "";
      // 访问后端
      instance.post('history/', {}).then(res => {
        console.log(res)
        // 刷新历史列表
        // this.history_list();
        // 后端新创建了一个会话，并返回id
        alert(res.id)
        // 刷新当前会话id
        this.current_session_id = res.id
      })

    },





    // 阿里流
    // add(){
    //   this.answer += "Q:"+this.temp.question+"\n"
    //   this.source = new EventSource("http://127.0.0.1:8000/ssechat?question="+this.temp.question);

    //   this.answer +="A:"
    //   this.source.onmessage = (event=> {
    //     this.answer = event.data
    //     // this.answer += event.data
    //   });

    //   this.source.onerror = (error=> {
    //       console.error('EventSource failed:', error);
    //       this.source.close();
    //       this.source = null;
    //   });
    // }
  },
  // 启动页面，自动调用该函数，并渲染函数里的内容
  mounted() {
    this.history_list()
  }
}
</script>

<style scoped>
/* 下拉列表 */
.example-showcase .el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}

.left {
  background-color: white;
  height: 800px;
}

.right {
  background-color: white;
  height: 800px;
}

/* 为ul元素添加一些基本样式 */
ul {
  list-style: none;
  /* 移除默认的列表样式 */
  padding: 0;
  /* 移除默认的内边距 */
  margin: 0;
  /* 移除默认的外边距 */
}

/* 为li元素添加一些基本样式 */
li {
  margin-bottom: 1px;
  /* 在列表项之间添加一些空间 */
  padding: 10px;
  /* 添加内边距以增加点击区域 */
  background-color: white;
  /* 背景颜色#f8f8f8 */
  border: 1px solid white;
  /* 边框 #ddd */
  border-radius: 4px;
  /* 圆角 */
  cursor: pointer;
  /* 鼠标悬停时显示手形 */
}


/* 为列表项添加悬停效果 */
li:hover {
  background-color: #E8F5FF;
  /* 鼠标悬停时的背景颜色#e8e8e8 */
}

/* 为按钮添加一些基本样式 */
.li_button {
  background-color: transparent;
  /* 透明背景 */
  border: none;
  /* 移除默认边框 */
  padding: 0;
  /* 移除默认内边距 */
  cursor: pointer;
  /* 鼠标悬停时显示手形 */
  font-size: 16px;
  /* 字体大小 */
  color: #333;
  /* 字体颜色 */
  text-align: left;
  /* 文本对齐方式 */
  width: 100%;
  /* 按钮宽度 */
  outline: none;
  /* 移除焦点轮廓 */
}

/* 当按钮被点击时的样式 */
.li_button:active {
  background-color: #e8e8e8;
  /* 点击时的背景颜色 */
}
</style>