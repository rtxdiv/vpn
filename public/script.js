// imports
const settingsMessage = document.querySelector('#settings-message')

const clientBlock = document.querySelector('#client')
const clientError = document.querySelector('#client-error')
const clientInfoStatus = document.querySelector('#client-info .status')
const clientInfoName = document.querySelector('#client-info .name')
const clientInfoDevices = document.querySelector('#client-info .devices')
const clientInfoDate = document.querySelector('#client-info .date')
const clientSettingsCopy = document.querySelector('#client-settings .copy')
const clientSettingsLink = document.querySelector('#client-settings .link')

const tariffsBlock = document.querySelector('#tariffs')
const tariffsError = document.querySelector('#tariffs-error')

const helpBlock = document.querySelector('#help')
const paymentsBlock = document.querySelector('#help-payments')
const aboutBlock = document.querySelector('#help-about')
const tutorialBlock = document.querySelector('#help-tutorial')
const supportBlock = document.querySelector('#help-support')

const popupBg = document.querySelector('#popup-bg')
const popup = document.querySelector('#popup')
const popupContent = document.querySelector('#popup-content')
const popupTitle = document.querySelector('#popup-content .title')
const popupText = document.querySelector('#popup-content .text')
const popupRadiogroup = document.querySelector('#popup-content .radiogroup')
const popupButton = document.querySelector('#popup-content .button')
const popupUname = document.querySelector('#popup-content .uname')
const popupError = document.querySelector('#popup-error')


popupBg.addEventListener('click', closePopup)
window.addEventListener('popstate', function(event) {
    if (popupIsOpened) {
        closePopup()
    }
})
window.addEventListener('pagehide', function(event) {
    if (popupIsOpened) {
        closePopup()
    }
})

const telegram = window.Telegram.WebApp
telegram.expand()


// globals
let client
let tariffs
let settings
let paymentPeriods
let popupIsOpened = false


async function getClient() {
    const resp = await fetch('/client', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Telegram ${telegram.initData}`
        }
    })
    if (resp.ok) {
        const body = await resp.json()
        client = body
        displayClient({ user: body })

    } else {
        displayClient({ error: (await resp.json()).detail })
    }
}
async function getTariffs() {
    const resp = await fetch('/tariffs', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    if (resp.ok) {
        const body = await resp.json()
        tariffs = body
        displayTariffs({ tariffs: body })
        
    } else {
        displayTariffs({ error: true })
    }
}
async function getSettings() {
    const resp = await fetch('/settings', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    if (resp.ok) {
        const body = await resp.json()
        settings = body
        displaySettings({ settings: body })

    } else {
        displaySettings({ error: true })
    }
}
async function getPeriods() {
    const resp = await fetch('/paymentPeriods', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    if (resp.ok) {
        const body = await resp.json()
        paymentPeriods = body
        displayPeriods(body)
    }
}
async function getBuy({ uname, months = 0 }) {
    popupUname.value = uname
    openPopup()
    const resp = await fetch('/payments/buy', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Telegram ${telegram.initData}`
        },
        body: JSON.stringify({
            to_tariff_uname: uname,
            months: months
        })
    })
    if (resp.ok) {
        const body = await resp.json()
        displayPopup({ info: body })
    } else {
        displayPopup({ error: (await resp.json()).detail })
    }
}


const main = async () => {
    await getSettings()
    await getClient()
    await getTariffs()
    await getPeriods()
}
main()


function displayClient({ user = false, error = false }) {
    console.log(user)
    helpBlock.style.display = 'flex'
    if (error) {
        clientError.querySelector('.message').innerHTML = error
        clientError.classList.add('error-block')
        clientError.style.display = 'flex'
        addButton(paymentsBlock, settings.payments_url)
        addButton(aboutBlock, settings.about_url)
        addButton(supportBlock, settings.support_url)
        return
    }
    if (user) {
        clientBlock.style.display = 'flex'
        clientInfoStatus.innerHTML = user['enable']? '<green>Активна</green>' : '<red>Неактивна</red>'
        clientInfoName.innerHTML = `${ user["comment"] }`
        clientInfoDevices.innerHTML = `Устройства: ${ user['limitIp'] == 0? 'бесконечно' : user['limitIp'] }`

        const expiry = user['expiryTime']
        let localDate
        if (expiry !== 0) {
            const date = new Date(user['expiryTime'])
            localDate = date.toLocaleDateString('ru-RU', {
                day: 'numeric',
                month: 'long',
                year: 'numeric'
            }).replace(' г.', '')
        } else localDate = 'бессрочно'
        clientInfoDate.innerHTML = `Действует до: ${ localDate }`
        addButton(paymentsBlock, settings.payments_url)
        addButton(tutorialBlock, settings.tutorial_url)
        addButton(supportBlock, settings.support_url)
        addButton(clientSettingsLink, settings.sub_url + client.subId)

    } else {
        clientError.querySelector('.message').innerHTML = 'У вас ещё нет подписки'
        clientError.style.display = 'flex'
        addButton(aboutBlock, settings.about_url)
        addButton(supportBlock, settings.support_url)
    }
}
function displayTariffs({ tariffs = false, error = false }) {
    console.log(tariffs)
    if (error) {
        tariffsError.querySelector('.message').innerHTML = 'Ошибка при загрузке тарифов'
        tariffsError.classList.add('error-block')
        tariffsError.display = 'flex'
        return
    }
    if (tariffs) {
        tariffs.forEach(tariff => {
            if (client && tariff.uname == client["comment"]) clientInfoName.innerHTML = tariff.name
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
                        <div class="rect-btn" onclick="getBuy({ uname: '${tariff.uname}', months: 0 })">Купить</div>
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
function displayPeriods(periods) {
    console.log(periods)
    popupRadiogroup.innerHTML = ''
        periods.forEach(period => {
            popupRadiogroup.innerHTML += `
                <label>
                    <input type="radio" name="popup-option" value="${period.months}" onchange="getBuy({ uname: 'document.querySelector('#popup-content .uname').value', months: ${period.months} })">
                    <span><a class="months">${period.months} мес.</a>${period.discount? `<a class="discount">-${period.discount * 100}%</a>` : ''}</span>
                </label>
            `
        })
    popupRadiogroup.children[0].querySelector('input').checked = true
}
function displayPopup({ info = false, error = false }) {
    popupContent.style.display = 'none'
    popupError.style.display = 'none'
    if (!paymentPeriods) {
        popupError.querySelector('.message').innerHTML = `Не удалось загрузить доступные периоды для оплаты`
        popupError.style.display = 'flex'
        return
    }
    if (error) {
        popupError.querySelector('.message').innerHTML = error
        popupError.style.display = 'flex'
        return
    }
    if (info) {
        popupTitle.innerHTML = info.title
        popupText.innerHTML = `
            Начнется: ${info.starts}
        `
        popupButton.innerHTML = `Создать платёж: ${info.total}₽`
        popupButton.onclick = function() {
            alert('В разработке...')
        }
        popupContent.style.display = 'flex'
    } else {
        popupError.querySelector('.message').innerHTML = 'Ошибка загрузки данных'
        popupError.style.display = 'flex'
        return
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
function scrollXTo(id) {
    document.querySelector(id).scrollIntoView({
        behavior: 'smooth',
        block: 'nearest'
    })
}

function openPopup() {
    if (popupIsOpened) return
    popupBg.style.display = 'flex'
    requestAnimationFrame(() => {
        popup.classList.add('opened')
    })
    document.body.style.overflow = 'hidden'
    history.pushState({ popup: true }, '', location.href)
    popupIsOpened = true
}
function closePopup(event) {
    if (!event || event.target == popupBg) {
        popup.classList.remove('opened')
        setTimeout(() => {
            popupBg.style.display = 'none'
        }, 200)
        document.body.style.overflow = 'auto'
        popupIsOpened = false
    }
}

function showBtnResult({ elem, error = false, message }) {
    const overflow = elem.querySelector('.overflow')
    overflow.classList.remove('error', 'success', 'animated')
    overflow.classList.add(error? 'error' : 'success')
    overflow.textContent = message? message : error? 'Ошибка' : 'Успешно'
    void overflow.offsetHeight
    overflow.classList.add('animated')
}
function copySubLink() {
    navigator.clipboard.writeText(settings.sub_url + client.subId).then(() => {
        showBtnResult({ elem: clientSettingsCopy, message: 'Скопировано!' })
    }).catch(err => {
        console.log(err)
        showBtnResult({ elem: clientSettingsCopy, error: true })
    })
}

function openOffer() {
    if (confirm('Отркыть публичную оферту?')) telegram.openLink('docs/offer')
}