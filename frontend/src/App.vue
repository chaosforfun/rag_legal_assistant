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
        <div class="response-header">
          <h3>回答</h3>
          <span class="response-time" v-if="responseTime">
            <el-icon><Timer /></el-icon>
            {{ responseTime }}
          </span>
        </div>
        <el-card><p>{{ answer }}</p></el-card>
      </div>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { Timer } from '@element-plus/icons-vue'

const question = ref('')
const answer = ref('')
const loading = ref(false)
const responseTime = ref('')

const formatTime = (ms) => {
  if (ms < 1000) {
    return `${ms.toFixed(0)}ms`
  }
  return `${(ms / 1000).toFixed(2)}s`
}

const askQuestion = async () => {
  if (!question.value) return
  loading.value = true
  responseTime.value = ''
  const startTime = performance.now()
  try {
    const resp = await axios.post('http://localhost:8000/query', { question: question.value })
    answer.value = resp.data.answer
    const endTime = performance.now()
    responseTime.value = formatTime(endTime - startTime)
  } catch (err) {
    answer.value = `请求失败: ${err}`
    const endTime = performance.now()
    responseTime.value = formatTime(endTime - startTime)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
  padding: 20px;
}

.response-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.response-header h3 {
  margin: 0;
}

.response-time {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #909399;
  font-size: 14px;
  background: #f4f4f5;
  padding: 4px 10px;
  border-radius: 12px;
}

.response-time .el-icon {
  font-size: 14px;
}
</style>
