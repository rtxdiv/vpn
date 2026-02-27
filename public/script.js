const debug = document.querySelector('#debug')

// const telegram = window.Telegram.WebApp
// telegram.expand()

const main = async () => {
    const resp = await fetch('http://127.0.0.1:8443/user', {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Telegram ${'okak'}`
        }
    })
    debug.innerHTML += `${JSON.stringify(resp)}`
    const body = await resp.json()
    debug.innerHTML += `\n${JSON.stringify(body)}`
}

main()