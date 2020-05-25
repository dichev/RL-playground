const W = 1 // wall
const G = 2 // goal
const Z = 3 // electricity
const A = 4 // agent


let dictClasses = {
    0: 'path',
    1: 'wall',
    2: 'goal',
    3: 'trap'
}

class Playground {

    constructor() {
        this.world = []
        this.values = []
        this.policy = []
        this.rows = 0
        this.cols = 0

        this.toggle_using_policy(true)

        this.server = new WebSocket('ws://localhost:8080')
        this.server.onmessage = async (e) => {
            let data = JSON.parse(e.data)
            if (data.world){
                this.world = data.world
                this.rows = this.world.length
                this.cols = this.world[0].length
            }
            if (data.values){
                this.values = data.values
            }
            if (data.policy){
                this.policy = data.policy
            }
            await playground.update()
        }
        this.server.onopen = async (e) => {
            await this.reset()
        }

    }

    async loop_message(command, params = {}){
        playground.message(command, params)
        let timer = setInterval(() => playground.message(command, params), 100)
        window.addEventListener('mouseup', () => clearInterval(timer), { once: true })
    }

    async message(command, params = {}){ // todo: move to server class
        let msg = JSON.stringify([ command, params])
        this.server.send(msg)
    }

    async reset(){
        this.message('reset')
    }

    colors(state){
        let intensity = 100 // 0..255
        let red   = Math.round(state < 0.5 ? intensity : ((1 - state) * 2) * intensity)
        let green = Math.round(state < 0.5 ? (state * 2) * intensity : intensity)
        let blue  = 0
        let alpha  = 1.0
        return [red, green, blue, alpha]
    }

    update() {
        let values = this.values
        let policy = this.policy
        let [min, max] = this._minMax(values)
        let ARROWS = '↑↓←→'

        for (let m=0; m<this.rows; m++){ // todo: a bit handlebars?
            for (let n=0; n<this.cols; n++){
                let value = values[m][n]
                let color = this.colors(this._normalize(value, min, max))

                let arrows = ''
                for (let a = 0; a < policy[m][n].length; a++) {
                    if (policy[m][n][a] > 0) {
                        arrows += ARROWS[a]
                    }
                }

                dom.world[m][n].querySelector('.value').innerText = value.toFixed(4) + '..'
                dom.world[m][n].querySelector('.color').style.backgroundColor = `rgba(${color.join(',')})`
                dom.world[m][n].querySelector('.policy').innerText = arrows
                dom.world[m][n].className = dictClasses[this.world[m][n]]
            }
        }
    }

    toggle_using_policy(using_policy = true){
        dom.btnPolicyUpdate.disabled = !using_policy
        dom.btnPolicyEvaluate.disabled = !using_policy
        dom.btnPolicyIteration.disabled = !using_policy
        dom.btnValueIteration.disabled = using_policy
        dom.showPolicy.disabled = !using_policy

        if(dom.showPolicy.checked !== using_policy){
            dom.showPolicy.click()
        }
    }

    _isTerminal(m, n){
        return this.world[m][n] === G // this.world[m][n] === Z ||
    }
    _isWall(m, n){
        return this.world[m][n] === W
    }

    _normalize(value, min, max) {
        return (value - min) / (max - min)
    }

    _minMax(matrix){
        let min = null, max = null
        let rows = matrix.length
        let cols = matrix[0].length
        for (let m=0; m < rows; m++) {
            for (let n = 0; n < cols; n++) {
                if (this._isTerminal(m, n)) continue // tmp
                min = Math.min(min, matrix[m][n])
                max = Math.max(max, matrix[m][n])
            }
        }
        return [min, max]
    }

}


let dom = {
    world: [],
    btnReset: document.getElementById('btnReset'),
    btnPolicyEvaluate: document.getElementById('btnPolicyEvaluate'),
    btnPolicyUpdate: document.getElementById('btnPolicyUpdate'),
    btnPolicyIteration: document.getElementById('btnPolicyIteration'),
    btnValueIteration: document.getElementById('btnValueIteration'),
    cfgRandomPolicy: document.getElementById('cfgRandomPolicy'),
    cfgGreedyPolicy: document.getElementById('cfgGreedyPolicy'),
    cfgNoPolicy: document.getElementById('cfgNoPolicy'),
    cfgGamma: document.getElementById('cfgGamma'),
    gammaValue: document.getElementById('gammaValue'),
    showValues: document.getElementById('showValues'),
    showPolicy: document.getElementById('showPolicy'),
    showColors: document.getElementById('showColors'),
}
rows = document.querySelectorAll('tr').length // tmp
for (let m=0; m<rows; m++){
    dom.world.push([...document.querySelectorAll(`[id^="${m},"]`)])
}

playground = new Playground()

dom.btnReset.addEventListener('click', () => playground.reset())
dom.btnPolicyEvaluate.addEventListener('mousedown',  () => playground.loop_message('policy_evaluate'))
dom.btnPolicyUpdate.addEventListener('mousedown',    () => playground.loop_message('policy_update'))
dom.btnPolicyIteration.addEventListener('mousedown', () => playground.loop_message('policy_iteration'))
dom.btnValueIteration.addEventListener('mousedown',  () => playground.loop_message('value_iteration'))



dom.cfgGreedyPolicy.addEventListener('click', () => {
    playground.toggle_using_policy(true)
    playground.message('config', {greedy_policy: true})
})
dom.cfgRandomPolicy.addEventListener('click', () => {
    playground.toggle_using_policy(true)
    playground.message('config', {greedy_policy: false})
})
dom.cfgNoPolicy.addEventListener('click', () => {
    playground.toggle_using_policy(false)
})
dom.cfgGamma.addEventListener('input', () => {
    dom.gammaValue.innerText = parseFloat(dom.cfgGamma.value).toFixed(2)
})
dom.cfgGamma.addEventListener('change', () => {
    playground.message('config', {gamma: parseFloat(dom.cfgGamma.value) })
})

dom.showValues.addEventListener('click', () => document.querySelector('.world').classList.toggle('show_values'))
dom.showPolicy.addEventListener('click', () => document.querySelector('.world').classList.toggle('show_policy'))
dom.showColors.addEventListener('click', () => document.querySelector('.world').classList.toggle('show_colors'))

//for (let m=0; m<dom.world.length; m++) {
//    for (let n = 0; n < dom.world[0].length; n++) {
//        dom.world[m][n].addEventListener('click', () => playground.single(m,n))
//    }
//}





























