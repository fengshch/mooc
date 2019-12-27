import { axios } from '@/utils/request'

const api = {
  category: '/categories'
}

export default api

export function getCategories (parameter) {
  return axios({
    url: api.category,
    method: 'get',
    params: {
      'page_no': parameter && parameter.pageNo,
      'page_size': parameter && parameter.pageSize
    }
  })
}
