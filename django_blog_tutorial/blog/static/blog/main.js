

// return cookie by name or undefined
function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
  }

const csrftoken = getCookie('csrftoken')

async function send_vote_request(method, request_url, body = null){
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

async function post_vote(element){
    let is_auth = (document.querySelector('meta[name="usr-auth-check"]').content == 'True')
    if (is_auth){
        let data = {
            post_id: element.getAttribute('post_id'),
            action: element.getAttribute('action')
        }
        // send up/down vote
        await send_vote_request('POST', vote_url, data)
        let score_elem = document.getElementById(element.getAttribute('post_id') + '_score')
        // get updated score
        let post_score = await send_vote_request('GET', vote_url, data)
        score_elem.innerHTML = post_score.headers.get('score')
    }
    else {
        window.location.href = '/login/'
    }
}

let vote_url = '/rate-post/'
let vote_list = document.getElementsByClassName('vote')

// add event for each vote button
for (let elem of vote_list){
    elem.addEventListener('click', event => {post_vote(elem)} )
}
