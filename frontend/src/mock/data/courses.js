const Mock = require('mockjs2')
// import { builder, getQueryParameters } from '../util'
const Random = Mock.Random

const categories = () => {
// module.exports = function () {
  let data = [{
      'id': 1,
      'name': '计算机和互联网',
      'idx': 1
    }, {
      'id': 2,
      'name': '财务会计',
      'idx': 2
    }, {
      'id': 3,
      'name': '人力资源',
      'idx': 3
    }, {
      'id': 4,
      'name': '建筑施工',
      'idx': 4
    }]
  return data
}

const courses = (count) => {
  const data = []
  let categoryId = 0

  for (let i = 0; i < count; i++) {
    categoryId = Random.integer(0, 3)
    data.push({
      'id': i + 1,
      'title': Random.cword(2, 8),
      'intro': Random.cparagraph(),
      'content': Random.cparagraph(),
      'avatar': Random.image('300x200'),
      'categoryId': categoryId,
      'categoryName': categories()[categoryId].name,
      'published': Random.boolean(),
      'idx': i + 1
    })
  }

  return data
}

module.exports = {
  categories,
  courses
}