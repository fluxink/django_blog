

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
        return await fetch(request_url, {
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

async function comment_vote(element){
    let data = {
        'comment-id': element.getAttribute('comment-id'),
        'comment-action': element.getAttribute('action')
    }
    response = await send_vote_request('POST', window.location.href, data)
    let score_elem = document.getElementById(data['comment-id'] + '-score')
    score_elem.innerHTML = response.headers.get('comment-score')
}

async function post_vote(element){
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

async function if_user_auth(func, ...args){
    let is_auth = (document.querySelector('meta[name="usr-auth-check"]').content == 'True')
    if (is_auth){
       await func(...args)
    }
    else{
        window.location.href = '/login/'
    }
}

async function post_fav(element, is_favorit){
    let data = {
        post_id: element.getAttribute('post_id'),
        fav: is_favorit
    }
    // send fav
    await send_vote_request('POST', fav_url, data)
}

const vote_url = '/rate-post/'
const fav_url = '/fav-post/'
const vote_list = document.getElementsByClassName('vote')
const fav_list = document.getElementsByClassName('fav')
const comment_vote_list = document.getElementsByClassName('comment-vote')

// add event for each vote button
for (let elem of vote_list){
    elem.addEventListener('click', event => {
        if_user_auth(post_vote,elem)
    } )
}
for (let elem of fav_list){
    elem.addEventListener('change', (event) => {
        if (event.currentTarget.checked){
            if_user_auth(post_fav,elem, 'True')
        }
        else {
            if_user_auth(post_fav,elem, 'False')
        }
    } )
}
for (let elem of comment_vote_list){
    elem.addEventListener('click', event => {
        if_user_auth(comment_vote, elem)
    })
}
