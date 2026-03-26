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
        <div class="answer-header">
          <h3>回答</h3>
          <el-tag v-if="elapsedTime !== null" type="info" size="small" effect="plain" class="time-tag">
            <el-icon><Timer /></el-icon>
            {{ elapsedTime }}ms
          </el-tag>
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
const elapsedTime = ref(null)

const askQuestion = async () => {
  if (!question.value) return
  loading.value = true
  elapsedTime.value = null
  const startTime = performance.now()
  try {
    const resp = await axios.post('http://localhost:8000/query', { question: question.value })
    answer.value = resp.data.answer
  } catch (err) {
    answer.value = `请求失败: ${err}`
  } finally {
    elapsedTime.value = Math.round(performance.now() - startTime)
    loading.value = false
  }
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
  padding: 20px;
}

.answer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.answer-header h3 {
  margin: 0;
}

.time-tag {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>
