import { axios } from '@/utils/request'

export default {
  getOrgTree: () => {
    return axios({
      url: '/organizations',
      method: 'get'
    })
  }
}
