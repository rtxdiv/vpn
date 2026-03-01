const debug = document.querySelector('#debug')
const subBlock = document.querySelector('#sub')
const subStatus = document.querySelector('#sub .status')
const subName = document.querySelector('#sub .name')
const subDevices = document.querySelector('#sub .devices')
const subDate = document.querySelector('#sub .date')
const subConf = document.querySelector('#sub .conf')

const telegram = window.Telegram.WebApp
telegram.expand()


const main = async () => {
    const resp = await fetch('/user', {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Telegram ${telegram.initData}`
        }
    })
    if (resp.ok) {
        const body = await resp.json()
        return drawSub(body.user)
    }
    drawSub(false, true)
}
// main()

let user = {"email":"5019916197","enable":true,"id":"3657bbfc-6f79-454b-a3e5-87442c5df7a5","password":"","inboundId":null,"up":0,"down":0,"expiryTime":1774461052796,"total":0,"reset":0,"flow":"","method":"","limitIp":3,"subId":"3657bbfc-6f79-454b-a3e5-87442c5df7a5","comment":"SOLO","tgId":"","totalGB":0,"uuid":null}
function drawSub(user, error = false) {
    if (error) {
        subBlock.classList.add('errblock')
        subBlock.innerHTML = '<a>Ошибка при загрузке подписки</a>'
        return
    }
    if (user) {
        subStatus.innerHTML = user['enable']? '<green>Активна</green>' : '<red>Неактивна</red>'
        subName.innerHTML = `«${ user["comment"] || 'Подписка' }»`
        subDevices.innerHTML = `Устройства: ${ user['limitIp'] == 0? 'бесконечно' : user['limitIp'] }`

        const expiry = user['expiryTime']
        let localDate
        if (expiry !== 0) {
            const date = new Date(user['expiryTime'])
            localDate = date.toLocaleDateString('ru-RU')
        } else localDate = 'бессрочно'
        subDate.innerHTML = `Действует до: ${ localDate }`

        subConf.addEventListener('click', function(event) {
            telegram.openLink('https://' + location.hostname + ':8080/sub/' + user['subId'])
        })
        
    } else {
        subBlock.innerHTML = '<a>У вас ещё нет подписки</a>'
    }
}
drawSub(user)