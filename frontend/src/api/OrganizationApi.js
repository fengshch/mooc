import { axios } from '@/utils/request'

const organizationApi = {
  getOrgTree: () => {
    return axios({
      url: '/organizations',
      method: 'get'
    })
  },
  getOrganization: id => {
    return axios({
      url: `/organizations/${id}`
    })
  },
  addOrganization: organization => {
    return axios({
      url: '/organizations/',
      method: 'post',
      data: organization
    })
  },
  updateOrganization: organization => {
    return axios({
      url: '/organizations/',
      method: 'put',
      data: organization
    })
  },
  deleteOrganization: organizationId => {
    return axios({
      url: `/organizations/${organizationId}`,
      method: 'delete'
    })
  }
}

export default organizationApi
