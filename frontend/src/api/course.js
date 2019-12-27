import { axios } from '@/utils/request'

const api = {
  course: '/courses',
  courseById: '/courses/1'
}

export default api

export function getCourses (parameter) {
  return axios({
    url: api.course,
    method: 'get',
    params: parameter
  })
}

export function getCourseById (id) {
  return axios({
    url: `/courses/${id}`,
    method: 'get'
  })
}
