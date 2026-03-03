const debug = document.querySelector('#debug')
const subBlock = document.querySelector('#sub')
const subStatus = document.querySelector('#sub .status')
const subName = document.querySelector('#sub .name')
const subDevices = document.querySelector('#sub .devices')
const subDate = document.querySelector('#sub .date')
const subConf = document.querySelector('#sub .conf')
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
        drawSub({ user: body.user })
        
    } else if (resp.status == 401) {
        drawSub({ authorization: false })

    } else {
        drawSub({ error: true })
    }
}
main()


function drawSub({ user = false, error = false, authorization = true }) {
    if (error) {
        subBlock.classList.add('errblock')
        subBlock.innerHTML = '<a>Ошибка при загрузке подписки</a>'

        addButton(aboutBlock)
        addButton(supportBlock)
        return
    }
    if (!authorization) {
        subBlock.innerHTML = '<a>Запустите приложение через Telegram, чтобы получить информацию о подписке</a>'
        addButton(aboutBlock)
        addButton(supportBlock)
        return
    }
    if (user) {
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
        addButton(subConf, location.hostname + ':8080/sub/' + user['subId'])

        addButton(tutorialBlock)
        addButton(supportBlock)
        
    } else {
        subBlock.innerHTML = '<a>У вас ещё нет подписки</a>'
        
        addButton(aboutBlock)
        addButton(supportBlock)
    }
}

function addButton(elem, link = false) {
    elem.style.display = 'flex'
    elem.addEventListener('click', function(event) {
        telegram.openLink(link ?? elem.dataset.url)
    })
}