<template>
  <v-card>
    <v-card-title class="text-h6">
      <v-icon class="mr-2">mdi-progress-clock</v-icon>
      생성 진행 상태
    </v-card-title>

    <v-card-text>
      <div v-if="status === 'processing'" class="text-center py-4">
        <v-progress-circular
            :model-value="progress"
            :size="100"
            :width="10"
            color="primary"
        >
          {{ progress }}%
        </v-progress-circular>

        <div class="mt-4">
          <p class="text-h6">{{ statusText }}</p>
          <p class="text-caption">예상 소요시간: 10-15분</p>
        </div>
      </div>

      <div v-else-if="status === 'completed'" class="text-center py-4">
        <v-icon size="64" color="success">mdi-check-circle</v-icon>
        <p class="text-h6 mt-2">생성 완료!</p>

        <v-list class="mt-4">
          <v-list-item v-if="results.shorts && results.shorts.length > 0">
            <v-list-item-title>
              숏폼: {{ results.shorts.length }}개
            </v-list-item-title>
          </v-list-item>

          <v-list-item v-if="results.longform">
            <v-list-item-title>
              롱폼: 1개 ({{ Math.floor(results.longform.duration / 60) }}분)
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </div>

      <div v-else-if="status === 'failed'" class="text-center py-4">
        <v-icon size="64" color="error">mdi-alert-circle</v-icon>
        <p class="text-h6 mt-2">생성 실패</p>
        <p class="text-caption">다시 시도해주세요.</p>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import api from '../services/api'

export default {
  name: 'ContentStatus',
  props: {
    taskId: String
  },
  data() {
    return {
      status: 'processing',
      progress: 0,
      results: {
        shorts: [],
        longform: null
      },
      polling: null
    }
  },
  computed: {
    statusText() {
      if (this.progress < 50) {
        return '숏폼 생성 중...'
      } else if (this.progress < 80) {
        return '롱폼 생성 중...'
      } else {
        return '마무리 작업 중...'
      }
    }
  },
  watch: {
    taskId: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.startPolling()
        }
      }
    }
  },
  beforeUnmount() {
    this.stopPolling()
  },
  methods: {
    async checkStatus() {
      try {
        const response = await api.getContentStatus(this.taskId)
        this.status = response.data.status
        this.progress = response.data.progress || 0
        this.results = response.data.results

        if (this.status === 'completed') {
          this.$emit('completed')
          this.stopPolling()
        } else if (this.status === 'failed') {
          this.stopPolling()
        }
      } catch (error) {
        console.error('Error checking status:', error)
      }
    },
    startPolling() {
      this.checkStatus()
      this.polling = setInterval(() => {
        this.checkStatus()
      }, 2000) // 2초마다 확인
    },
    stopPolling() {
      if (this.polling) {
        clearInterval(this.polling)
        this.polling = null
      }
    }
  }
}
</script>
