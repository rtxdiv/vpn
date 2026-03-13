const settingsMessage = document.querySelector('#settings-message')

const subBlock = document.querySelector('#sub')
const subStatus = document.querySelector('#sub-info .status')
const subName = document.querySelector('#sub-info .name')
const subDevices = document.querySelector('#sub-info .devices')
const subDate = document.querySelector('#sub-info .date')
const subError = document.querySelector('#sub-error')

const tariffsBlock = document.querySelector('#tariffs')
const tariffsError = document.querySelector('#tariffs-error')

const aboutBlock = document.querySelector('#about')
const tutorialBlock = document.querySelector('#tutorial')
const supportBlock = document.querySelector('#support')

const telegram = window.Telegram.WebApp
telegram.expand()


const getSub = async () => {
    const resp = await fetch('/sub', {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Telegram ${telegram.initData}`
        }
    })
    if (resp.ok) {
        const body = await resp.json()
        displaySub({ user: body })
        
    } else if (resp.status == 401) {
        displaySub({ authorization: false })

    } else {
        displaySub({ error: true })
    }
}
const getTariffs = async () => {
    const resp = await fetch('/tariffs', {
        headers: {
            'Content-Type': 'application/json'
        }
    })
    if (resp.ok) {
        const body = await resp.json()
        displayTariffs({ tariffs: body })
        
    } else {
        displayTariffs({ error: true })
    }
}
const getSettings = async () => {
    const resp = await fetch('/settings', {
        headers: {
            'Content-Type': 'application/json'
        }
    })
    if (resp.ok) {
        const body = await resp.json()
        displaySettings({ settings: body })

    } else {
        displaySettings({ error: true })
    }
}

const main = async () => {
    getSub()
    getTariffs()
    getSettings()
}
main()


function displaySub({ user = false, error = false, authorization = true }) {
    if (error) {
        subError.querySelector('.message').innerHTML = 'Ошибка при загрузке подписки'
        subError.classList.add('error-block')
        subError.style.display = 'flex'
        return
    }
    if (!authorization) {
        subError.querySelector('.message').innerHTML = 'Запустите приложение через Telegram, чтобы получить информацию о подписке'
        subError.style.display = 'flex'
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

    } else {
        subError.querySelector('.message').innerHTML = 'У вас ещё нет подписки'
        subError.style.display = 'flex'
    }
}
function displayTariffs({ tariffs = false, error = false }) {
    if (error) {
        tariffsError.querySelector('.message').innerHTML = 'Ошибка при загрузке тарифов'
        subError.classList.add('error-block')
        tariffsError.display = 'flex'
        return
    }
    if (tariffs) {
        tariffs.forEach(tariff => {
            tariffsBlock.innerHTML += `
                <div class="block">
                    <div class="top">
                        <a class="country">${tariff.country}</a>
                        <a class="name">${tariff.name}</a>
                        <a class="devices">Устройсва: ${tariff.devices}</a>
                        <a class="traffic">Трафик: ${tariff.traffic==0? 'бесконечно' : tariff.traffic + " Gb" }</a>
                        <a class="price">${tariff.price}₽<span class="note"> / мес.</span></a>
                    </div>
                    <div class="bottom">
                        <div class="rect-btn">Купить</div>
                    </div>
                </div>
            `
        })
        tariffsBlock.style.display = 'flex'
    }
}
function displaySettings({ settings = false, error = false }) {
    console.log(settings)
    if (error) {
        settingsMessage.querySelector('.message').innerHTML = 'Ошибка при загрузке настроек'
        settingsMessage.classList.add('error-block')
        settingsMessage.display = 'flex'
        return
    }
    if (settings['message']) {
        settingsMessage.querySelector('.message').innerHTML = settings['message']
        settingsMessage.display = 'flex'
    }
}

function addButton(elem, link = undefined) {
    elem.style.display = 'flex'
    elem.addEventListener('click', function(event) {
        telegram.openLink(link ?? event.target.dataset.url)
    })
}