// imports
const settingsMessage = document.querySelector('#settings-message')

const subBlock = document.querySelector('#sub')
const subStatus = document.querySelector('#sub-info .status')
const subName = document.querySelector('#sub-info .name')
const subDevices = document.querySelector('#sub-info .devices')
const subDate = document.querySelector('#sub-info .date')
const subError = document.querySelector('#sub-error')

const tariffsBlock = document.querySelector('#tariffs')
const tariffsError = document.querySelector('#tariffs-error')

const aboutBlock = document.querySelector('#help-about')
const tutorialBlock = document.querySelector('#help-tutorial')
const supportBlock = document.querySelector('#help-support')

const popupBg = document.querySelector('#popup-bg')
const popup = document.querySelector('#popup')
popupBg.addEventListener('click', closeWindow)
window.addEventListener('click', function(event) {
    if (popupIsOpened) {
        event.preventDefault()
        closeWindow()
    }
})

const telegram = window.Telegram.WebApp
telegram.expand()


// globals
let client
let tariffs
let settings
let popupIsOpened = false


const getClient = async () => {
    const resp = await fetch('/client', {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Telegram ${telegram.initData}`
        }
    })
    if (resp.ok) {
        const body = await resp.json()
        client = body
        displayClient({ user: body })
        
    } else if (resp.status == 401) {
        displayClient({ authorization: false })

    } else {
        displayClient({ error: true })
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
        tariffs = body
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
        settings = body
        displaySettings({ settings: body })

    } else {
        displaySettings({ error: true })
    }
}

const main = async () => {
    await getSettings()
    await getClient()
    await getTariffs()
}
main()


function displayClient({ user = false, error = false, authorization = true }) {
    console.log(user)
    if (error) {
        subError.querySelector('.message').innerHTML = 'Ошибка при загрузке подписки'
        subError.classList.add('error-block')
        subError.style.display = 'flex'
        addButton(aboutBlock, settings.about_url)
        addButton(supportBlock, settings.support_url)
        return
    }
    if (!authorization) {
        subError.querySelector('.message').innerHTML = 'Запустите приложение через Telegram, чтобы получить информацию о подписке'
        subError.style.display = 'flex'
        addButton(supportBlock, settings.support_url)
        return
    }
    if (user) {
        subBlock.style.display = 'flex'
        subStatus.innerHTML = user['enable']? '<green>Активна</green>' : '<red>Неактивна</red>'
        subName.innerHTML = `${ user["comment"] || 'Подписка' }`
        subDevices.innerHTML = `Устройства: ${ user['limitIp'] == 0? 'бесконечно' : user['limitIp'] }`

        const expiry = user['expiryTime']
        let localDate
        if (expiry !== 0) {
            const date = new Date(user['expiryTime'])
            localDate = date.toLocaleDateString('ru-RU')
        } else localDate = 'бессрочно'
        subDate.innerHTML = `Действует до: ${ localDate }`
        addButton(tutorialBlock, settings.tutorial_url)
        addButton(supportBlock, settings.support_url)

    } else {
        subError.querySelector('.message').innerHTML = 'У вас ещё нет подписки'
        subError.style.display = 'flex'
        addButton(aboutBlock, settings.about_url)
        addButton(supportBlock, settings.support_url)
    }
}
function displayTariffs({ tariffs = false, error = false }) {
    console.log(tariffs)
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
                        <div class="rect-btn" onclick="openWindow({action:'buy', id:'${tariff.tariff_id}'})">Купить</div>
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
        settingsMessage.style.display = 'flex'
        return
    }
    if (settings.message) {
        settingsMessage.querySelector('.message').innerHTML = settings.message
        settingsMessage.style.display = 'flex'
    }
}

function addButton(elem, url = null) {
    elem.style.display = 'flex'
    elem.style.cursor = 'pointer'
    elem.addEventListener('click', function(event) {
        link = url? url : event.target.dataset.url
        if (link) telegram.openLink(link)
    })
}
function openWindow({ action, id = null }) {
    console.log(`${action}: ${id}`)
    popupBg.style.display = 'flex'
    popup.style.transform = 'none'
    popupIsOpened = true
}
function closeWindow() {
    // popupBg.style.display = 'none'
    popup.style.transform = ''
    popupIsOpened = false
}