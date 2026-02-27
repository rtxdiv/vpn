const debug = document.querySelector('#debug')

const telegram = window.Telegram.WebApp
telegram.expand()

const resp = await fetch('https://your-server.com/profile', {
    headers: {
        'Authorization': `Telegram ${telegram.initData}`
    }
})
debug.innerHTML += `${resp}`
const body = await resp.json()
debug.innerHTML += `\n${body}`