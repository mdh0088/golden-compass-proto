<template>
  <v-card>
    <v-card-title class="text-h6">
      <v-icon class="mr-2">mdi-folder-multiple-outline</v-icon>
      생성된 콘텐츠
      <v-spacer />
      <v-btn icon variant="text" @click="fetchContents">
        <v-icon>mdi-refresh</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-data-table
          :headers="headers"
          :items="contents"
          :loading="loading"
          class="elevation-1"
      >
        <template v-slot:item.created_at="{ item }">
          {{ formatDate(item.created_at) }}
        </template>

        <template v-slot:item.status="{ item }">
          <v-chip
              :color="getStatusColor(item.status)"
              size="small"
          >
            {{ getStatusText(item.status) }}
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn
              v-if="item.status === 'completed'"
              icon
              variant="text"
              @click="viewContent(item)"
          >
            <v-icon>mdi-eye</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card-text>

    <!-- 콘텐츠 상세 보기 다이얼로그 -->
    <v-dialog v-model="dialog" max-width="600">
      <v-card v-if="selectedContent">
        <v-card-title>
          {{ selectedContent.topic }}
        </v-card-title>

        <v-card-text>
          <v-list>
            <v-list-subheader>숏폼 ({{ selectedContent.shorts_count }}개)</v-list-subheader>
            <v-list-item v-for="(short, index) in selectedShorts" :key="index">
              <v-list-item-title>{{ short.title }}</v-list-item-title>
              <template v-slot:append>
                <v-btn
                    size="small"
                    :href="`http://localhost:8000${short.file_url}`"
                    target="_blank"
                >
                  다운로드
                </v-btn>
              </template>
            </v-list-item>

            <v-divider v-if="selectedLongform" class="my-4" />

            <v-list-subheader v-if="selectedLongform">롱폼</v-list-subheader>
            <v-list-item v-if="selectedLongform">
              <v-list-item-title>{{ selectedLongform.title }}</v-list-item-title>
              <template v-slot:append>
                <v-btn
                    size="small"
                    :href="`http://localhost:8000${selectedLongform.file_url}`"
                    target="_blank"
                >
                  다운로드
                </v-btn>
              </template>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn @click="dialog = false">닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import api from '../services/api'

export default {
  name: 'ContentList',
  data() {
    return {
      loading: false,
      contents: [],
      headers: [
        { title: '주제', key: 'topic' },
        { title: '생성일', key: 'created_at' },
        { title: '상태', key: 'status' },
        { title: '숏폼', key: 'shorts_count' },
        { title: '롱폼', key: 'has_longform' },
        { title: '액션', key: 'actions', sortable: false }
      ],
      dialog: false,
      selectedContent: null,
      selectedShorts: [],
      selectedLongform: null
    }
  },
  mounted() {
    this.fetchContents()
  },
  methods: {
    async fetchContents() {
      this.loading = true
      try {
        const response = await api.getContentList()
        this.contents = response.data.contents
      } catch (error) {
        console.error('Error fetching contents:', error)
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString('ko-KR')
    },
    getStatusColor(status) {
      const colors = {
        pending: 'grey',
        processing: 'primary',
        completed: 'success',
        failed: 'error'
      }
      return colors[status] || 'grey'
    },
    getStatusText(status) {
      const texts = {
        pending: '대기중',
        processing: '생성중',
        completed: '완료',
        failed: '실패'
      }
      return texts[status] || status
    },
    async viewContent(content) {
      if (content.status !== 'completed') return

      try {
        const response = await api.getContentStatus(content.id)
        this.selectedContent = content
        this.selectedShorts = response.data.results.shorts || []
        this.selectedLongform = response.data.results.longform
        this.dialog = true
      } catch (error) {
        console.error('Error viewing content:', error)
      }
    }
  }
}
</script>
