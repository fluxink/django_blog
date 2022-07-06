
// function vote_post(vote){
//     const csrftoken = getCookie('csrftoken');
//     let response = await fetch('/blog/rate-post/', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json;charset=utf-8',
//           'X-CSRFToken': csrftoken 
//         },
//         body: JSON.stringify(vote)
//       });
// }
// возвращает куки с указанным name,
// или undefined, если ничего не найдено
function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
  }

let vote = {
    post_id: '1',
    action: 'like'
}
const csrftoken = getCookie('csrftoken')

async function send_request(method, request_url, body = null){
    if (method == 'POST'){
        const response = await fetch(request_url, {
            method: method,
            body: JSON.stringify(body),
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'X-CSRFToken': csrftoken
            }
        })
    }
    if (method == 'GET'){
        let head = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken
        }
        head['post-id'] = body['post_id']
        return await fetch(request_url, {
            method: method,
            headers: head
        })
    }

}

let url = '/rate-post/'

let vote_list = document.getElementsByClassName('vote')

async function test(element){
    let data = {
        post_id: element.getAttribute('post_id'),
        action: element.getAttribute('action')
    }
    await send_request('POST', url, data)
    let score_elem = document.getElementById(element.getAttribute('post_id') + '_score')
    
    let post_score = await send_request('GET', url, data)
    score_elem.innerHTML = post_score.headers.get('score')
}

for (let elem of vote_list){
    // elem.addEventListener('click', send_request('POST', url, {post_id: elem.getAttribute('post_id'), action: elem.getAttribute('action')}))
    elem.addEventListener('click', event => {test(elem)} )
}


// send_request('POST', url, vote)