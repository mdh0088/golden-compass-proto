<template>
  <v-card>
    <v-card-title class="text-h6">
      <v-icon class="mr-2">mdi-creation</v-icon>
      새 콘텐츠 생성
    </v-card-title>

    <v-card-text>
      <v-form ref="form" v-model="valid">
        <v-text-field
            v-model="topic"
            label="주제"
            placeholder="예: 2025년 2월 재물운"
            :rules="[v => !!v || '주제를 입력해주세요']"
            required
            class="mb-4"
        />

        <v-radio-group v-model="contentType" label="콘텐츠 타입">
          <v-radio label="숏폼 + 롱폼" value="both" />
          <v-radio label="숏폼만 (10개)" value="shorts_only" />
          <v-radio label="롱폼만 (1개)" value="longform_only" />
        </v-radio-group>

        <v-alert type="info" variant="tonal" class="mb-4">
          <div class="text-caption">
            <strong>숏폼:</strong> 30초 세로형 영상 10개<br>
            <strong>롱폼:</strong> 10분 가로형 영상 1개
          </div>
        </v-alert>
      </v-form>
    </v-card-text>

    <v-card-actions>
      <v-spacer />
      <v-btn
          color="primary"
          variant="elevated"
          :loading="loading"
          :disabled="!valid"
          @click="generateContent"
      >
        <v-icon left>mdi-magic-staff</v-icon>
        생성 시작
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import api from '../services/api'

export default {
  name: 'ContentGenerator',
  data() {
    return {
      valid: false,
      loading: false,
      topic: '',
      contentType: 'both'
    }
  },
  methods: {
    async generateContent() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      try {
        const response = await api.generateContent({
          topic: this.topic,
          content_type: this.contentType
        })

        this.$emit('contentGenerated', response.data.task_id)

        // 폼 초기화
        this.topic = ''
        this.$refs.form.reset()
      } catch (error) {
        console.error('Error generating content:', error)
        alert('콘텐츠 생성 중 오류가 발생했습니다.')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
