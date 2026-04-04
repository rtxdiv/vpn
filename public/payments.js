const paymentsError = document.querySelector('#payments-error')
const paymentsBlock = document.querySelector('#payments')

const popupBg = document.querySelector('#popup-bg')
const popup = document.querySelector('#popup')
const popupContent = document.querySelector('#popup-content')
const popupError = document.querySelector('#popup-error')
const popupTitle = document.querySelector('#popup-content .title')
const popupAmount = document.querySelector('#popup-content .amount')
const popupDetails = document.querySelector('#popup-content .details')
const popupDetailsComment = document.querySelector('#popup-content .details-comment')
const popupPaymentId = document.querySelector('#popup-content .paymentId')
const popupPaymentIdComment = document.querySelector('#popup-content .paymentId-comment')
const popupMessage = document.querySelector('#popup-content .message')
 

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
let popupIsOpened = false


async function getPayments() {
    const resp = await fetch('/payments/getAll', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Telegram ${telegram.initData}`
        }
    })
    if (resp.ok) {
        const body = await resp.json()
        client = body
        displayPayments({ payments: body })

    } else {
        displayPayments({ error: (await resp.json()).detail })
    }
}
async function getPayment(id) {
    const resp = await fetch(`/payments/get?id=${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Telegram ${telegram.initData}`
        }
    })
    if (resp.ok) {
        const body = await resp.json()
        client = body
        displayPayment({ payment: body })

    } else {
        displayPayment({ error: (await resp.json()).detail })
    }
}


const main = async () => {
    const urlParams = new URLSearchParams(window.location.search)
    const id = urlParams.get('id')
    if (id) await getPayment(id)
    await getPayments()
}
main()


function displayPayments({ payments = false, error = false }) {
    console.log(payments)
    if (error) {
        paymentsError.querySelector('.message').innerHTML = error
        paymentsError.classList.add('error-block')
        paymentsError.style.display = 'flex'
        return
    }
    if (payments && payments.length != 0) {
        payments.forEach(payment => {
            const date = new Date(payment.created+'Z')
            const localDate = date.toLocaleDateString('ru-RU', {
                day: 'numeric',
                month: 'short',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            }).replace(' г.', '')
            paymentsBlock.innerHTML += `
                <div class="block" onclick="getPayment('${payment.payment_id}')">
                    <div class="top">
                        <a class="title">${payment.title}</a>
                        <a class="total">${payment.amount}${payment.currency}</a>
                    </div>
                    <div class="bottom">
                        <a class="status">${payment.success? '<green>Подтверждено</green>' : '<yellow>Ожидание</yellow>' }</a>
                        <a class="date">${localDate}</a>
                    </div>
                </div>
            `
        })
    } else {
        paymentsError.querySelector('.message').innerHTML = 'У вас ещё нет созданных платежей'
        paymentsError.style.display = 'flex'
        return
    }
}
function displayPayment({ payment = false, error = false }) {
    console.log(payment)
    popupContent.style.display = 'none'
    popupError.style.display = 'none'
    if (error) {
        popupError.querySelector('.message').innerHTML = error
        popupError.style.display = 'flex'
        openPopup()
        return
    }
    if (payment) {
        popupTitle.innerHTML = payment.title
        popupAmount.innerHTML = `К оплате: <green>${payment.amount}${payment.currency}</green>`
        popupDetails.querySelector('.text').innerHTML = payment.settings.payment_details
        popupDetailsComment.innerHTML = payment.settings.payment_comment
        popupPaymentId.querySelector('.text').innerHTML = `${payment.settings.payment_id_prefix}${payment.paymentId}`
        if (payment.settings.payment_message) popupMessage.innerHTML = payment.settings.payment_message
        popupContent.style.display = 'flex'

    } else {
        popupError.querySelector('.message').innerHTML = 'Ошибка загрузки данных'
        popupError.style.display = 'flex'
    }
    openPopup()
}

function addLink(elem, url) {
    elem.onclick = () => { window.location.href = url }
    elem.style.display = 'flex'
}
function scrollXTo(id) {
    document.querySelector(id).scrollIntoView({
        behavior: 'smooth',
        block: 'nearest'
    })
}
function showBtnResult({ elem, error = false, message }) {
    let overflow = elem.querySelector('.overflow')
    if (!overflow) {
        elem.innerHTML += '<div class="overflow"></div>'
        overflow = elem.querySelector('.overflow')
    }
    overflow.classList.remove('error', 'success', 'animated')
    overflow.classList.add(error? 'error' : 'success')
    overflow.textContent = message? message : error? 'Ошибка' : 'Успешно'
    void overflow.offsetHeight
    overflow.classList.add('animated')
}
function copyContent(elem) {
    const text = elem.querySelector('.text').textContent
    navigator.clipboard.writeText(text).then(() => {
        showBtnResult({ elem: elem, message: 'Скопировано!' })
    }).catch(err => {
        console.log(err)
        showBtnResult({ elem: elem, error: true, message: 'Ошибка копирования' })
    })
}

function openPopup() {
    if (popupIsOpened) return
    popupBg.style.display = 'flex'
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            popup.classList.add('opened')
        })
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