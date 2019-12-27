import { axios } from '@/utils/request'

const videoApi = {
  getVideosByChapterId: (chapterId) => {
    return axios({
      url: `/videos/chapter/${chapterId}`,
      method: 'get'
    })
  },

  getVideoById: id => {
    return axios({
      url: `/videos/${id}`,
      method: 'get'
    })
  },

  addVideo: video => {
    return axios({
      url: '/videos/',
      method: 'post',
      data: video
    })
  },

  updateVideo: video => {
    return axios({
      url: '/videos/',
      method: 'put',
      data: video
    })
  },

  deleteVideoById: id => {
    return axios({
      url: `/videos/${id}`,
      method: 'delete'
    })
  }
}

export default videoApi
