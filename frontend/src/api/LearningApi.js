import { axios } from '@/utils/request'

export default {
  getLearningByOrgId: (queryParam) => {
    return axios({
      url: `/learning/organization/${queryParam.orgId}`,
      method: 'get',
      params: {
        page_no: queryParam && queryParam.pageNo,
        page_size: queryParam && queryParam.pageSize,
        show_grand: queryParam && queryParam.showGrand
      }
    })
  },
  getLearningByCourseId: queryParam => {
    return axios({
      url: `/learning/course/${queryParam.courseId}`,
      method: 'get',
      params: {
        organization_id: queryParam && queryParam.orgId,
        show_grand: queryParam && queryParam.showGrand
      }
    })
  },
  addLearningByCourseId: queryParam => {
    return axios({
      url: `/learning/course/${queryParam.courseId}`,
      method: 'post',
      data: queryParam.userIds
    })
  },
  deleteLearningByCourseId: queryParam => {
    return axios({
      url: `/learning/course/${queryParam.courseId}`,
      method: 'delete',
      data: queryParam.userIds
    })
  },
  getLearningByUserIdAndCourseId: (userId, courseId) => {
    return axios({
      url: `/learning/user/${userId}/course/${courseId}`,
      method: 'get'
    })
  },
  getLearningByUserId: queryParam => {
    return axios({
      url: `/learning/user/${queryParam.userId}`,
      method: 'get',
      params: {
        page_no: queryParam && queryParam.pageNo,
        page_size: queryParam && queryParam.pageSize
      }
    })
  },
  addLearningByUserIdAndCourseId: (userId, courseId) => {
    return axios({
      url: `/learning/user/${userId}/course/${courseId}`,
      method: 'post'
    })
  },
  getLearningById: id => {
    return axios({
      url: `/learning/${id}`
    })
  },
  addLearning: learning => {
    return axios({
      url: '/learning/',
      method: 'post',
      data: learning
    })
  },
  updateLearning: learning => {
    return axios({
      url: '/learning/',
      method: 'put',
      data: learning
    })
  },
  deleteLearningById: learningId => {
    return axios({
      url: `/learning/${learningId}`,
      method: 'delete'
    })
  }
}
