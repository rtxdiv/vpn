const subBlock = document.querySelector('#sub')
const subStatus = document.querySelector('#sub-info .status')
const subName = document.querySelector('#sub-info .name')
const subDevices = document.querySelector('#sub-info .devices')
const subDate = document.querySelector('#sub-info .date')
const subError = document.querySelector('#sub-error')

const aboutBlock = document.querySelector('#about')
const tutorialBlock = document.querySelector('#tutorial')
const supportBlock = document.querySelector('#support')

const telegram = window.Telegram.WebApp
telegram.expand()


const main = async () => {
    const resp = await fetch('/sub', {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Telegram ${telegram.initData}`
        }
    })
    if (resp.ok) {
        const body = await resp.json()
        drawSub({ user: body.user, subHost: body.subHost })
        
    } else if (resp.status == 401) {
        drawSub({ authorization: false })

    } else {
        drawSub({ error: true })
    }
}
main()


function drawSub({ user = false, error = false, authorization = true, subHost = false }) {
    if (error) {
        subBlock.style.display = 'none'
        subError.style.display = 'flex'
        subError.innerHTML = '<a>Ошибка при загрузке подписки</a>'

        addButton(aboutBlock)
        addButton(supportBlock)
        return
    }
    if (!authorization) {
        subBlock.style.display = 'none'
        subError.style.display = 'flex'
        subError.innerHTML = '<a>Запустите приложение через Telegram, чтобы получить информацию о подписке</a>'
        addButton(aboutBlock)
        addButton(supportBlock)
        return
    }
    if (user) {
        subBlock.style.display = 'flex'
        subStatus.innerHTML = user['enable']? '<green>Активна</green>' : '<red>Неактивна</red>'
        subName.innerHTML = `<def>«</def>${ user["comment"] || 'Подписка' }<def>»</def>`
        subDevices.innerHTML = `Устройства: ${ user['limitIp'] == 0? 'бесконечно' : user['limitIp'] }`

        const expiry = user['expiryTime']
        let localDate
        if (expiry !== 0) {
            const date = new Date(user['expiryTime'])
            localDate = date.toLocaleDateString('ru-RU')
        } else localDate = 'бессрочно'
        subDate.innerHTML = `Действует до: ${ localDate }`
        addButton(subConf, `${subHost}/${user['subId']}`)

        addButton(tutorialBlock)
        addButton(supportBlock)
        
    } else {
        subBlock.innerHTML = '<a>У вас ещё нет подписки</a>'
        
        addButton(aboutBlock)
        addButton(supportBlock)
    }
}

function addButton(elem, link = undefined) {
    elem.style.display = 'flex'
    elem.addEventListener('click', function(event) {
        telegram.openLink(link ?? event.target.dataset.url)
    })
}