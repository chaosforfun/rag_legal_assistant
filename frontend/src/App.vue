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
        <el-card><p>{{ answer }}</p></el-card>
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

const askQuestion = async () => {
  if (!question.value) return
  loading.value = true
  try {
    const resp = await axios.post('http://localhost:8000/query', { question: question.value })
    answer.value = resp.data.answer
  } catch (err) {
    answer.value = `请求失败: ${err}`
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
</style>
