
// return cookie by name or undefined
function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
  }

const csrftoken = getCookie('csrftoken')

async function send_post_request(request_url, body = null){
    return await fetch(request_url, {
        method: 'POST',
        body: JSON.stringify(body),
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken
        }
    })
}

async function if_user_auth(func, ...args){
    let is_auth = (document.querySelector('meta[name="usr-auth-check"]').content == 'True')
    if (is_auth){
       await func(...args)
    }
    else {
        window.location.href = '/login/?next=' + window.location.pathname
    }
}

async function comment_vote(element){
    let data = {
        'comment-id': element.getAttribute('comment-id'),
        'comment-action': element.getAttribute('action')
    }
    response = await send_post_request(window.location.href, data)
    let score_elem = document.getElementById(data['comment-id'] + '-score')
    score_elem.innerHTML = response.headers.get('comment-score') || score_elem.innerHTML
}

async function post_vote(element){
    let data = {
        post_id: element.getAttribute('post_id'),
        action: element.getAttribute('action')
    }
    // send up/down vote
    response = await send_post_request(vote_url, data)
    let score_elem = document.getElementById(element.getAttribute('post_id') + '_score')
    // display updated score
    score_elem.innerHTML = response.headers.get('score') || score_elem.innerHTML
}


async function post_fav(element, is_favorit){
    let data = {
        post_id: element.getAttribute('post_id'),
        fav: is_favorit
    }
    // send fav
    await send_post_request(fav_url, data)
}

function replaceUrlParam(url, paramName, paramValue)
{
    if (paramValue == null) {
        paramValue = '';
    }
    var pattern = new RegExp('\\b('+paramName+'=).*?(&|#|$)');
    if (url.search(pattern)>=0) {
        return url.replace(pattern,'$1' + paramValue + '$2');
    }
    url = url.replace(/[?#]$/,'');
    return url + (url.indexOf('?')>0 ? '&' : '?') + paramName + '=' + paramValue;
}


const vote_url = '/rate-post/'
const fav_url = '/fav-post/'
const vote_list = document.getElementsByClassName('vote')
const fav_list = document.getElementsByClassName('fav')
const comment_vote_list = document.getElementsByClassName('comment-vote')
const page_links = document.getElementsByClassName('page-link')

// add event for each button
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
for (let elem of page_links){
    elem.addEventListener('click', event => {
        window.location.href = replaceUrlParam(window.location.href, 'page', elem.getAttribute('value'))
    })
}

var order = document.getElementById("selectOrdering");

order.onchange = function() {
    window.location.href = replaceUrlParam(window.location.href, 'order', order.value)
    return false;
}