<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title class="text-h5 font-weight-bold">
        🧭 황금나침반 콘텐츠 생성 시스템
      </v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-row>
          <v-col cols="12" md="6">
            <ContentGenerator @contentGenerated="onContentGenerated" />
          </v-col>
          <v-col cols="12" md="6">
            <ContentStatus
                v-if="currentTaskId"
                :taskId="currentTaskId"
                @completed="onContentCompleted"
            />
          </v-col>
        </v-row>

        <v-row class="mt-4">
          <v-col cols="12">
            <ContentList ref="contentList" />
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <v-snackbar v-model="snackbar" :color="snackbarColor">
      {{ snackbarText }}
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar = false">닫기</v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
import ContentGenerator from './components/ContentGenerator.vue'
import ContentStatus from './components/ContentStatus.vue'
import ContentList from './components/ContentList.vue'

export default {
  name: 'App',
  components: {
    ContentGenerator,
    ContentStatus,
    ContentList
  },
  data() {
    return {
      currentTaskId: null,
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success'
    }
  },
  methods: {
    onContentGenerated(taskId) {
      this.currentTaskId = taskId
      this.showSnackbar('콘텐츠 생성이 시작되었습니다!', 'success')
    },
    onContentCompleted() {
      this.showSnackbar('콘텐츠 생성이 완료되었습니다!', 'success')
      this.$refs.contentList.fetchContents()
    },
    showSnackbar(text, color) {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
    }
  }
}
</script>
