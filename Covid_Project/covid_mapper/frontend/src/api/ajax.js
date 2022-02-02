import axios from 'axios'

export default function ajax (url, data = {}, type = 'GET') {
  return new Promise(function (resolve, reject) {
    let Promise
    if (type === 'GET') {
      promise = axios.get(url)
    } else {
      promise = axios.post(url, data)
    }
    promise.then(function (response) {
      resolve(response.data)
    }).catch(function (error) {
      reject(error)
    })
  })
}
