const debug = document.querySelector('#debug')

const telegram = window.Telegram.WebApp
telegram.expand()

// {"email":"5019916197","enable":true,"id":"3657bbfc-6f79-454b-a3e5-87442c5df7a5","password":"","inboundId":null,"up":0,"down":0,"expiryTime":1774461052796,"total":0,"reset":0,"flow":"","method":"","limitIp":3,"subId":"3657bbfc-6f79-454b-a3e5-87442c5df7a5","comment":"","tgId":"","totalGB":0,"uuid":null}
const main = async () => {
    const resp = await fetch('/user', {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Telegram ${telegram.initData}`
        }
    })
    const body = await resp.json()
}

main()