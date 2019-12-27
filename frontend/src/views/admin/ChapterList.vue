<template>
  <a-card :bordered="false">
    <div class="table-operator">
      <a-button type="primary" incon="plus" @click="handleNew">新建</a-button>
    </div>
    <a-table
      :columns="columns"
      :dataSource="chapters"
      class="components-table-demo-nested"
      :pagination="pagination"
      rowKey="id"
      :bordered="false"
    >
      <template slot="operation" slot-scope="text, record">
        <a @click="handleEdit(record)">编辑</a>
        <a-divider type="vertical"/>
        <a @click="handleNewVideo(record)">添加视频</a>
        <a-divider type="vertical"/>
        <a-popconfirm
          v-if="chapters.length"
          title="确定要删除吗？"
          @confirm="handleDel(record)">
          <a>删除</a>
        </a-popconfirm>
      </template>
      <a-table
        slot="expandedRowRender"
        :columns="videoColumns"
        slot-scope="record"
        :dataSource="record.videos"
        :pagination="false"
        rowKey="id"
        :bordered="false"
      >
        <template slot="thumbnail" slot-scope="thumbnail">
          <img :src="thumbnail" style="width: 60px; height: 40px" />
        </template>
        <template slot="action" slot-scope="text, item">
          <a @click="handleEditVideo(item)">编辑</a>
          <a-divider type="vertical"/>
          <a-popconfirm
            v-if="record.videos.length"
            title="确定要删除吗？"
            @confirm="handleDelVideo(item)">
            <a>删除</a>
          </a-popconfirm>
          <a-divider type="vertical"/>
          <a @click="handlePlayVideo(item)">播放视频</a>
        </template>
      </a-table>
    </a-table>
  </a-card>
</template>

<script>
import chapterApi from '@/api/ChapterApi'
import videoApi from '@/api/VideoApi'
import { mapActions } from 'vuex'
const columns = [
  {
    title: '序号',
    dataIndex: 'no',
    customRender: (value, row, index) => {
      return value
    }
  },
  { title: '标题', dataIndex: 'title', key: 'title' },
  {
    title: '操作',
    dataIndex: 'operation',
    scopedSlots: { customRender: 'operation' }
  }
]
const videoColumns = [
  {
    title: '序号',
    dataIndex: 'no',
    customRender: (value, row, index) => {
      return index + 1
    }
  },
  {
    title: '标题',
    dataIndex: 'title',
    key: 'title'
  },
  {
    title: '视频',
    dataIndex: 'thumbnail',
    scopedSlots: { customRender: 'thumbnail' }
  },
  {
    title: '操作',
    dataIndex: 'action',
    scopedSlots: { customRender: 'action' }
  }
]
export default {
  data () {
    return {
      columns,
      chapters: [],
      videoColumns,
      videos: [],
      pagination: {
        pageSizeOptions: ['5', '10', '20'],
        hideOnSinglePage: true,
        defaultCurrent: 1,
        defaltPageSize: 5,
        showSizeChanger: true,
        showQuickJumper: false,
        pageSize: 5,
        total: 0,
        onChange: pageNo => {
          this.queryParam.pageNo = pageNo
          this.loadData(this.queryParam)
        },
        onShowSizeChange: (current, pageSize) => {
          console.log(pageSize)
          this.pagination.pageSize = pageSize
          this.queryParam.pageSize = this.pagination.pageSize
          this.loadData(this.queryParam)
        }
      },
      queryParam: {
        courseId: this.$route.params.courseId,
        pageNo: 1,
        pageSize: 5
      }
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      const courseId = parseInt(to.params.courseId)
      vm.loadData(courseId)
    })
  },
  watch: {
    $route (to, from) {
      console.log(to.name)
      console.log(to.params.courseId)
      if (to.name === 'ChapterListAdmin') {
        const courseId = parseInt(to.params.courseId)
        this.loadData(courseId)
      }
    }
  },
  methods: {
    ...mapActions(['showAlert']),
    loadData (courseId) {
      this.queryParam.courseId = courseId
      chapterApi.getChaptersByCourseId(this.queryParam).then(res => {
        this.pagination.pageSize = res.pageSize
        this.pagination.total = res.totalCount
        this.chapters = res.data
        this.chapters.forEach((value, index) => {
          value.no = (this.queryParam.pageNo - 1) * res.pageSize + index + 1
        })
      }).catch(error => {
        console.log(error)
      })
    },
    handleNew () {
      this.$router.push({ name: 'ChapterEditAdmin', params: { chapterId: 'new', courseId: this.queryParam.courseId } })
    },
    handleNewVideo (record) {
      this.$router.push({
        name: 'VideoEditAdmin',
        params: {
          videoId: 'new',
          chapterId: record.id
        }
      })
    },
    handleEdit (record) {
      this.$router.push({ name: 'ChapterEditAdmin', params: { chapterId: record.id, courseId: this.queryParam.courseId } })
    },
    handleEditVideo (item) {
      this.$router.push({ name: 'VideoEditAdmin', params: { videoId: item.id, chapterId: item.chapter_id } })
    },
    handleDel (record) {
      chapterApi.deleteChapterById(record.id).then(res => {
        if (this.chapters.length === 1 && this.queryParam.pageNo > 1) {
          this.queryParam.pageNo = this.queryParam.pageNo - 1
        }
        this.loadData()
        this.showAlert({
          'type': 'success',
          'message': res.message
        })
      }).catch(err => {
        this.showAlert({
          'type': 'error',
          'message': err.message
        })
      })
    },
    handleDelVideo (item) {
      videoApi.deleteVideoById(item.id).then(res => {
        this.loadData()
        this.showAlert({
          'type': 'success',
          'message': res.message
        })
      }).catch(err => {
        this.showAlert({
          'type': 'error',
          'message': err.message
        })
      })
    },
    handlePlayVideo (item) {
      console.log(item)
    }
  }
}
</script>
