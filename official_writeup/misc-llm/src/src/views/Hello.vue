<template>
    <div class="container"><div class="router-view-container">
        <div class="content-container">
            <div class="title">
                电风扇 · Plus
            </div>

            <div class="text">
                <div :class="{ 'input-message-container': true, 'active': isActive }">
                    <textarea v-model="inputMessage" class="input-message" placeholder="你的作文" @input="onInput"
                        @keydown.enter.prevent @keydown.enter="onEnter($event)" @focus="onFocus" @blur="onBlur"></textarea>
                </div>
            </div>
            <div>
                <a-button type="primary" danger :loading="loading" @click="sendMessage"
                    style="margin-top: 10px;margin-bottom: 10px;">获得评语&评分</a-button>
            </div>


            <div class="text" style="height: 100px ;min-height: 100px;">
                <div :class="{ 'input-message-container': true, 'active': isActive2 }">
                    <textarea v-model="inputComment" class="input-message" placeholder="给出你的评语" @input="onInput"
                        @keydown.enter.prevent @keydown.enter="onEnter($event)" @focus="onFocus2"
                        @blur="onBlur2"></textarea>
                </div>
            </div>
            <div>
                <a-button type="primary" danger :loading="loading2" @click="sendComment"
                    style="margin-top: 10px;margin-bottom: 10px;">获得评分</a-button>
            </div>


            <!-- <div class="feedback">
                <div class="feedback-content" v-text="feed1"> </div>
            </div> -->
            <!-- <div class="feedback">
                <div class="feedback-title">
                    评语：
                </div>
                <div class="feedback-content" v-text="feed1"> </div>
            </div>-->


            <div class="feedback">
                <span class="feedback-title">
                    评分：
                </span>
                <span class="feedback-content" v-text="score"></span>
            </div>
        </div>
    </div></div>
</template>


<script lang="ts" setup>

import { ref, nextTick, onMounted, onUnmounted, watch } from 'vue';
import axios from 'axios';
import { message } from 'ant-design-vue';

const inputMessage = ref("刀削面是一只手拿着面团，另一只手里拿刀，站在开水锅前，把面团削成细长的薄片下进锅里煮的面。");
const inputComment = ref("");

const isActive = ref(false);
const onFocus = () => {
    isActive.value = true;
};
const onBlur = () => {
    isActive.value = false;
};

const isActive2 = ref(false);
const onFocus2 = () => {
    isActive2.value = true;
};
const onBlur2 = () => {
    isActive2.value = false;
};

const score = ref("");
const loading = ref(false);
const loading2 = ref(false);

message.config({
  duration: 3,
  maxCount: 1,
});

function requestSVC(url: string, param: any) {
    return axios.get(url, {
        params: param,
        withCredentials: true, // 允许携带凭据（如 cookie）
        headers: {
            'Content-Type': 'application/json',
        }
    });
}
async function sendMessage() {
    console.log("Ciallo～(∠・ω< )⌒★")
    if(!inputMessage.value){
        message.error("输入不能为空")
        return
    }


    loading.value = true
    try {
        var data = (await (requestSVC("/comment", { input: inputMessage.value }))).data
        inputComment.value = data.comment
        score.value = data.score
        if(data.left!==undefined) {
            score.value += "\n本日剩余次数：" + data.left;
        }
        if (data.flag) {
            score.value += "\nFlag：" + data.flag
        }
        message.success('智能打分完成');
    } catch (error) {
        // console.log(error.response.data)
        message.error(error.response.data.error)
    }

    loading.value = false
}
async function sendComment() {
    console.log("Ciallo～(∠・ω< )⌒★")
    if(inputComment.value == decodeBase64Unicode('Q2lhbGxv772eKOKIoOODu8+JPCAp4oyS4piF')){
        console.log(decodeBase64Unicode(my_str2))
    }
    if(!inputComment.value){
        message.error("输入不能为空")
        return
    }


    loading2.value = true
    try {
        var data = (await (requestSVC("/score", { input: inputComment.value }))).data
        score.value = data.score
        if(data.left!==undefined) {
            score.value += "\n本日剩余次数：" + data.left;
        }
        if (data.flag) {
            score.value += "\nFlag：" + data.flag
        }
        message.success('智能打分完成');
    } catch (error) {
        // console.log(error.response.data.error)
        message.error(error.response.data.error)
    }

    loading2.value = false
}

const my_str = 'Q2lhbGxv772eKOKIoOODu8+JPCAp4oyS4piF'
const my_str2 = '6L+Z5LiN5pivd2Vi6aKY77yM5Yir55yLY29uc29sZeS6hg=='
function encodeBase64Unicode(str: string) {
    const encoder = new TextEncoder();
    const data = encoder.encode(str);
    let binary = '';
    data.forEach((byte) => {
        binary += String.fromCharCode(byte);
    });
    return btoa(binary);
}

// Unicode 字符串的 Base64 解码
function decodeBase64Unicode(encoded: string) {
    const binary = atob(encoded);
    const data = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
        data[i] = binary.charCodeAt(i);
    }
    const decoder = new TextDecoder();
    return decoder.decode(data);
}
</script>

<style scoped>
.content-container {
    max-width: 800px;
    padding: 50px 0;
    display: flex;
    margin: 0 auto;
    justify-content: flex-start;
    flex-direction: column;
    align-items: center;
}

.title {
    font-size: 30px;
}

.text {
    height: 600px;
    min-height: 600px;
    width: 100%;
}

.input-message-container {
    background: white;
    width: 100%;
    height: 100%;
    border: 1px solid #dedede;
    border-radius: 10px;
    /* margin-right: 10px; */
    flex-grow: 1;
    transition: border-color 0.3s linear;
    /* margin-top: 10px; */
    box-shadow: 0px 0px 20px 5px #bebebe36;
}

.input-message-container.active {
    border-color: #cdab00;
}

textarea {
    resize: none;
    overflow: hidden;
}

.input-message {
    height: 100%;
    padding: 10px 10px;
    border: none;
    border-radius: 10px;
    flex-grow: 1;
    overflow-y: scroll;
    border-width: 0px;
    width: 100%;
    min-height: 16px;
    font-size: 16px;
    scrollbar-gutter: stable;
    scrollbar-width: thin;
    scrollbar-color: lightgray transparent;
}

.input-message:focus {
    outline: none !important;
    box-shadow: none !important;
}

.feedback {
    border: 1px solid #dedede;
    width: 100%;
    border-radius: 10px;
    padding: 10px;
    margin-top: 10px;
}

.feedback-title {
    /* font-size: 20px; */
}

.feedback-content {
    font-size: 16px;
    min-height: 16px;
    word-wrap: break-word;
    white-space: pre-wrap;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100vw;
  margin: auto;
  /* Add this line */
  box-sizing: border-box;
  height: 100%;


  background-image: url(/src/bg.webp);
  background-position: 0 0;
  background-size: 100% 100%;

  overflow-y: scroll;
}

.router-view-container {
  /* display: flex; */
  justify-content: center;
  align-items: center;
  /* Added to center RouterView vertically */
  width: 100%;
  height: 100%;
  /*max-width: 1000px;*/
}
</style>