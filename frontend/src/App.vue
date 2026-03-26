<template>
  <el-container class="layout">
    <el-header>
      <h2>法规 RAG 助手</h2>
    </el-header>
    <el-main>
      <el-form @submit.prevent>
        <el-form-item label="问题">
          <el-input type="textarea" v-model="question" rows="4" placeholder="请输入法律法规问题"></el-input>
        </el-form-item>
        <el-button type="primary" :loading="loading" @click="askQuestion">提问</el-button>
      </el-form>
      <el-divider></el-divider>
      <div v-if="answer">
        <h3>回答</h3>
        <el-card>
          <p>{{ answer }}</p>
          <div class="time-info" v-if="elapsedTime > 0">
            <el-tag size="small" type="info">
              耗时: {{ (elapsedTime / 1000).toFixed(2) }} 秒
            </el-tag>
          </div>
        </el-card>
      </div>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const question = ref('')
const answer = ref('')
const loading = ref(false)
const elapsedTime = ref(0)

const askQuestion = async () => {
  if (!question.value) return
  loading.value = true
  elapsedTime.value = 0
  
  const startTime = Date.now()
  try {
    const resp = await axios.post('http://localhost:8000/query', { question: question.value })
    answer.value = resp.data.answer
  } catch (err) {
    answer.value = `请求失败: ${err}`
  } finally {
    elapsedTime.value = Date.now() - startTime
    loading.value = false
  }
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
  padding: 20px;
}

.time-info {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #ebeef5;
  text-align: right;
}
</style>
