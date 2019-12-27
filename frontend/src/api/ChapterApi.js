import { axios } from '@/utils/request'

const chapterApi = {
  getChaptersByCourseId: (queryParam) => {
    return axios({
      url: `/chapters/course/${queryParam.courseId}`,
      method: 'get',
      params: {
        'page_no': queryParam.pageNo,
        'page_size': queryParam.pageSize
      }
    })
  },

  getChapterById: id => {
    return axios({
      url: `/chapters/${id}`,
      method: 'get'
    })
  },

  addChapter: chapter => {
    return axios({
      url: '/chapters/',
      method: 'post',
      data: chapter
    })
  },

  updateChapter: chapter => {
    return axios({
      url: '/chapters/',
      method: 'put',
      data: chapter
    })
  },

  deleteChapterById: chapterId => {
    return axios({
      url: `/chapters/${chapterId}`,
      method: 'delete'
    })
  }
}

export default chapterApi
