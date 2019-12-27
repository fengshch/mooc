module.exports = {
  '/api/*': '/$1',
  '/api/categories?pageNo=:pageNoa&pageSize=:pageSize': '/api/categories?_page=:pageNo&_limit=:pageSize'
}
