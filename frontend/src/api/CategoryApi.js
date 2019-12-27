import { axios } from '@/utils/request'

const categoryApi = {
  getCategories: parameter => {
    return axios({
      url: '/categories/',
      method: 'get',
      params: {
        'page_no': parameter && parameter.pageNo,
        'page_size': parameter && parameter.pageSize
      }
    })
  },
  getCategoryById: id => {
    return axios({
      url: `/categories/${id}`
    })
  },
  addCategory: category => {
    return axios({
      url: '/categories/',
      method: 'post',
      data: category
    })
  },
  updateCategory: category => {
    return axios({
      url: '/categories/',
      method: 'put',
      data: category
    })
  },
  deleteCategory: categoryId => {
    return axios({
      url: `/categories/${categoryId}`,
      method: 'delete'
    })
  }
}

export default categoryApi
