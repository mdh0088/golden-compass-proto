import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json'
    }
})

export default {
    // 콘텐츠 생성
    generateContent(data) {
        return api.post('/api/content/generate', data)
    },

    // 상태 확인
    getContentStatus(taskId) {
        return api.get(`/api/content/status/${taskId}`)
    },

    // 콘텐츠 목록
    getContentList() {
        return api.get('/api/content/list')
    }
}
