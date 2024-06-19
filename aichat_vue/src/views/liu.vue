<template>
  <div>
    <h2>Server-Sent Events Example</h2>

     <el-form :inline="true"  class="demo-form-inline">
  <el-form-item label="问题">
    <el-input v-model="askmes" placeholder="请输入问题"></el-input>
  </el-form-item>
  
  <el-form-item>
    <el-button type="primary" @click="connectToStream">查询</el-button>
  </el-form-item>
</el-form>

    <ul>
     
      <div id="notifications">{{resmes}}</div>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      askmes:'',
      source: null,
      resmes:''
    };
  },
  mounted() {
    // this.connectToStream();
  },
  beforeDestroy() {
    this.disconnectStream();
  },
  methods: {
    connectToStream() {
      
       var source = new EventSource("http://127.0.0.1:8000/ssechat?question="+this.askmes);

        source.onmessage = (event=> {
          this.resmes = this.resmes + event.data
        });

        source.onerror = function(error) {
            console.error('EventSource failed:', error);
        };
    },
    disconnectStream() {
      if (this.source) {
        this.source.close();
        this.source = null;
      }
    },
  },
};
</script>