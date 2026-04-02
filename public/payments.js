const paymentsError = document.querySelector('#payments-error')
const paymentsBlock = document.querySelector('#payments')

const popupBg = document.querySelector('#popup-bg')
const popup = document.querySelector('#popup')

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
    alert(id)
    return
    const resp = await fetch('/payments/get', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Telegram ${telegram.initData}`
        },
        body: JSON.stringify({
            payment_id: id,
        })
    })
    if (resp.ok) {
        const body = await resp.json()
        client = body
        displayPayments({ payments: body })

    } else {
        displayPayments({ error: (await resp.json()).detail })
    }
}


const main = async () => {
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