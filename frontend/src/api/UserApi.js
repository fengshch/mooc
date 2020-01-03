import { axios } from '@/utils/request'

export default {
  getUsersByOrgId: (queryParam) => {
    return axios({
      url: `/users/organization/${queryParam.orgId}`,
      method: 'get',
      params: {
        page_no: queryParam && queryParam.pageNo,
        page_size: queryParam && queryParam.pageSize,
        show_grand: queryParam && queryParam.showGrand
      }
    })
  },
  getUserById: id => {
    return axios({
      url: `/users/${id}`
    })
  },
  addUser: user => {
    return axios({
      url: '/users/',
      method: 'post',
      data: user
    })
  },
  updateUser: user => {
    return axios({
      url: '/users/',
      method: 'put',
      data: user
    })
  },
  deleteUser: userId => {
    return axios({
      url: `/users/${userId}`,
      method: 'delete'
    })
  },
  resetPassword: userId => {
    return axios({
      url: '/users/reset_password',
      method: 'put',
      data: {
        user_id: userId
      }
    })
  },
  updatePassword: (userId, password) => {
    return axios({
      url: '/users/update_password',
      method: 'put',
      data: {
        user_id: userId,
        password: password
      }
    })
  }
}
