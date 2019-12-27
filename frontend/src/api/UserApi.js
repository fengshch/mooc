import { axios } from '@/utils/request'

export default {
  getUsersByOrgId: (queryParam) => {
    return axios({
      url: `/users/organization/${queryParam.orgId}`,
      method: 'get',
      params: {
        page_no: queryParam && queryParam.pageNo,
        page_size: queryParam && queryParam.pageSize
      }
    })
  }
}
