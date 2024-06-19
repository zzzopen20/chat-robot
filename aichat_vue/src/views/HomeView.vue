<template>
	<div class="common-layout">
		<el-container>
			<el-aside>
				<el-button type="primary">新建对话</el-button>
				<el-input
					v-model="input1"
					class="SearchInput"
					size="large"
					placeholder="请输入搜索内容"
					:suffix-icon="Search"
				/>
				<el-timeline style="margin-left: none; max-width: 600px">
					<div
						style="
							color: #878aab;
							font-size: 12px;
							padding: 10px;
							width: 100%;
							text-align: start;
						"
					>
						最近7天
					</div>
					<!-- <el-timeline-item placement="top">
						<el-card v-for="his in history" :key="his.id">
							<div class="chatHistory">
								Update Github templateUpdate Github templateUpdate Github
								template
							</div>
						</el-card>
					</el-timeline-item> -->
					<el-timeline-item placement="top">
						<el-card>
							<div>Update Github template</div>
						</el-card>
					</el-timeline-item>
					<el-timeline-item placement="top">
						<el-card>
							<div>Update Github template</div>
						</el-card>
					</el-timeline-item>
				</el-timeline>
			</el-aside>
			<el-main>
				<div class="gpt-chat">
					<div class="chat-messages">
						<div v-for="message in messages" :key="message.id" class="message">
							<div
								v-if="message.role == 'user'"
								:class="{
									'message-content': true,
									'message-user-right': message.role == 'user',
								}"
							>
								{{ message.content }}
							</div>
							<div
								:class="{
									'message-content': true,
									'message-user-left': message.role != 'user',
								}"
								v-else
							>
								{{ message.content }}
							</div>
                            <!-- <div ></div> -->
						</div>
					</div>
					<div class="chat-input">
						<input
							v-model="userInput"
							@keyup.enter="sendMessage"
							type="text"
							placeholder="Enter message"
						/>
						<button @click="sendMessage">Send</button>
						<!-- 模型选择 -->
						<div class="model-select">
							<select v-model="model">
								<option value="qwen-turbo">qwen-turbo</option>
								<option value="ernie-lite-8k">ernie-lite-8k</option>
							</select>
						</div>
					</div>
				</div>
			</el-main>
		</el-container>
	</div>
</template>

<script setup>
// import { ref, reactive,getCurrentInstance } from "vue";
// const globalProperties = getCurrentInstance().appContext.config.globalProperties;// 获取全局属性 vue3不推荐这种写法
// const $http = globalProperties.$http;
import { ref, reactive, inject } from "vue";
import { Search } from "@element-plus/icons-vue";
const axios = inject("$axios");

var messages = reactive([]);
var userInput = ref("");
var model = ref("");
var url = "";
async function sendMessage() {
	if (!model.value) return alert("请选择模型");
	if (userInput.value.trim() == "") return alert("请输入内容");
	messages.push({
		id: Date.now(),
		content: userInput.value,
		role: "user",
	});
	let content = userInput.value;
	userInput.value = "";
	axios
		.post(
			"http://127.0.0.1:8000/chat/",
			{
				content,
			}
			// {
			// 	responseType: "stream",
			// }
		)
		.then(function (response) {
			console.log(response)
			// console.log(JSON.parse(response.data));
			// messages.value.push({
			// 	id: Date.now(),
			// 	content: response.output.choices[0]["message"]["content"],
			// 	role: response.output.choices[0]["message"]["role"],
			// });
			messages.push({
				id: Date.now(),
				content: response.data.chat.content,
				role: response.data.chat.role,
			});
			console.log(messages);
		})
		.catch(function (error) {
			console.log(error);
		});
	// if  "api/chat/";
	// } else if (model.value == "qwen-turbo") {
	// 	url = "api/stu/";
	// }
	// axios
	// 	.post(url, {
	// 		content,
	// 	})
	// 	.then(function (response) {
	// 		messages.push(response.data.chat);
	// 		console.log(messages);
	// 	})
	// 	.catch(function (error) {
	// 		console.log(error);
	// 	});
}
// 构建API请求的URL
// const http = await fetch("http://localhost:8000/api/chat/");
// // 拿到响应头，body:把数据转换可流式(分块)读取,getReader():返回一个遍历器
// const reader = http.body.getReader();
// // 循环读取数据流
// while (true) {
// 	// read():读取当前流
// 	// done: 布尔类型false表示数据没有读完 true:表示已读完数据流
// 	// value: 当前数据流中的数据，它是utf-8文字编码格式，需要解码
// 	const { done, value } = await reader.read();
// 	// 创建解码器对象
// 	const decoder = new TextDecoder("utf-8");
// 	if (done) {
// 		break;
// 	}
// 	// 对数据进行解码
// 	const decodedString = decoder.decode(value);
// 	console.log("数据-->", decodedString);
// }

// axios
// 	.post(
// 		"http://127.0.0.1:8000/api/chat/",
// 		{
// 			content,
// 		}
// 		// {
// 		// 	responseType: "stream",
// 		// }
// 	)
// 	.then(function (response) {
// 		// console.log(JSON.parse(response.data));
// 		// messages.value.push({
// 		// 	id: response.output.choices[0]['message']['content'],
// 		// 	content: response.output.choices[0]['message']['content'],
// 		// 	user: false,
// 		// });
// 		console.log(response);
// 	})
// 	.catch(function (error) {
// 		console.log(error);
// 	});

// 这里模拟向GPT发送请求并接收响应
// mockGptResponse().then(response => {
// 	messages.value.push({
// 		id: Date.now(),
// 		content: response,
// 		user: false,
// 	});
// });

// 模拟GPT响应函数,返回一个Promise对象，在1秒后通过resolve函数传递模拟的响应结果："GPT Response: Hello, how can I help you?"。这个函数通常用于测试或开发过程中，代替真实的GPT调用，以减少依赖和加快开发速度。
function mockGptResponse() {
	return new Promise(resolve => {
		setTimeout(() => {
			resolve("GPT Response: Hello, how can I help you?");
		}, 1000);
	});
}

</script>

<style scoped>
.el-timeline {
	padding-inline-start: 0;
}
.chatHistory {
	overflow: hidden;
	white-space: nowrap;
	text-overflow: ellipsis;
}
.el-button--primary {
	width: 300px;
	border-radius: 32px;
}
.SearchInput {
	align-items: center;
	background: #f7f8fc;
	border: 1px solid #f7f8fc;
	border-radius: 32px;
	height: 42px;
	margin: 16px 0;
	padding: 12px 17px;
}

.el-input >>> .el-input__wrapper {
	background-color: transparent;
	border: none !important;
	box-shadow: none !important;
}

.gpt-chat {
	max-width: 1000px;
	min-width: 700px;
	margin: auto;
}
.chat-messages {
	padding: 10px;
	overflow-y: scroll;
	height: 700px;
}
::-webkit-scrollbar {
	display: none;
}
.message {
	margin-bottom: 15px;
}
.message-content {
	padding: 10px;
	background-color: #f0f0f0;
	border-radius: 5px;
	max-width: 80%;
}
.message-user-left {
	text-align: start;
    white-space: pre-wrap; /* 保留空格和换行符，且文本会自动换行 */
}
.message-user-right {
	text-align: end;
    width: fit-content;
    margin: 0 0 0 auto;
    white-space: pre-wrap; /* 保留空格和换行符，且文本会自动换行 */
}
.chat-input {
	display: flex;
}
.chat-input input {
	padding: 10px;
	border: 1px solid #ccc;
	border-radius: 5px;
	width: 100%;
	margin: 0 10px;
	outline: none;
}
.chat-input button {
	padding: 10px 15px;
	background-color: #007bff;
	color: white;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	outline-color: white;
}
.model-select {
	/* position: fixed;
	top: 30px;
	right: 32%; */
	margin: 10px;
}
</style>
