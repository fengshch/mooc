import { axios } from '@/utils/request'

const courseApi = {
  getCourses: parameter => {
    return axios({
      url: '/courses/',
      method: 'get',
      params: {
        'page_no': parameter && parameter.pageNo,
        'page_size': parameter && parameter.pageSize
      }
    })
  },

  getCourseById: id => {
    return axios({
      url: `/courses/${id}`,
      method: 'get'
    })
  },

  getCoursesByUserId: userId => {
    return axios({
      url: `/courses/users/${userId}`,
      methid: 'get'
    })
  },

  getCoursesByCategoryId: queryParams => {
    return axios({
      url: `/courses/category/${queryParams.categoryId}`,
      method: 'get',
      params: {
        'page_no': queryParams.pageNo,
        'page_size': queryParams.pageSize
      }
    })
  },

  addCourse: course => {
    return axios({
      url: '/courses/',
      method: 'post',
      data: course
    })
  },

  updateCourse: course => {
    return axios({
      url: '/courses/',
      method: 'put',
      data: course
    })
  },

  deleteCourseById: courseId => {
    return axios({
      url: `/courses/${courseId}`,
      method: 'delete'
    })
  }
}

export default courseApi
