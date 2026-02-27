const debug = document.querySelector('#debug')

const telegram = window.Telegram.WebApp
telegram.expand()

const main = async () => {
    const resp = await fetch('/user', {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Telegram ${telegram.initData}`
        }
    })
    debug.innerHTML += `${JSON.stringify(resp)}`
    const body = await resp.json()
    debug.innerHTML += `\n${JSON.stringify(body)}`
}

main()