const toggle = document.getElementById('theme-toggle');
const revamp_reminder = document.getElementById('revamp-reminder')
let rotation = 0

revamp_reminder.addEventListener('click', () => {
    window.location.href = '/legacy'
})

toggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    rotation += 180
    document.getElementById('theme-icons').style.transform = `rotate(${rotation}deg)`


    localStorage.setItem(
        'theme',
        document.body.classList.contains('dark') ? 'dark' : 'light'
    );
});

lines = document.querySelectorAll('.line')

async function animateLine(line) {
    while (true) {

        let delay = Math.floor(Math.random() * 3) * 1000
        let x = 0
        let y = 0

        await new Promise(resolve => setTimeout(resolve, delay))

        while (y <= 100) {
            if (x >= 20) {
                y+= 1
            }
            line.style.clipPath = `polygon(0 ${x}%, 100% ${x}%, 100% ${y}%, 0 ${y}%)`
            x += 1
            await new Promise(resolve => setTimeout(resolve, 30))
        }

        line.style.clipPath = `polygon(0 0, 0 0, 0 0, 0 ${y}%)`
    }
}

function setDiag(line) {
    const parent = line.parentElement
    const w = parent.offsetWidth
    const h = parent.offsetHeight
    const B = Math.atan2(w, h) * (180 / Math.PI)
    line.style.height = `${Math.sqrt(w ** 2 + h ** 2)+50}px`
    line.style.transform = `rotate(-${B}deg)`

}

lines.forEach(line =>  {
    animateLine(line)
    setDiag(line)
})
window.addEventListener('resize', () => lines.forEach(setDiag))

// Load saved theme
if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark');
    rotation += 180
    document.getElementById('theme-icons').style.transform = `rotate(${rotation}deg)`

}

window.addEventListener('scroll', ()=> {
    const landing = document.getElementById('landing')

    landing.style.opacity = `${1 - (window.scrollY / landing.offsetHeight)}`
    if (parseFloat(landing.style.opacity) <= 0.1) {
        landing.classList.add('hidden')
    }
    else {
        landing.classList.remove('hidden')
    }

})

function setTime(){
    const time = document.getElementById('time')
    let d = new Date()
    let [h, m, s] = [("0" + d.getHours()).slice(-2), ("0" + d.getMinutes()).slice(-2), ("0" + d.getSeconds()).slice(-2)]
    time.textContent = `${h}:${m}:${s}`
}

document.addEventListener('DOMContentLoaded', () => {
    setTime()
    setInterval(()=>{
        setTime()
    }, 1000)
})
