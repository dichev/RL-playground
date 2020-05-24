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



let dom = {
    world: [],
    btnEvaluate: document.getElementById('btnEvaluate'),
    btnReset: document.getElementById('btnReset'),
    btnPlay: document.getElementById('btnPlay'),
    showValues: document.getElementById('showValues'),
    showPolicy: document.getElementById('showPolicy'),
    showColors: document.getElementById('showColors'),
}

rows = document.querySelectorAll('tr').length // tmp
for (let m=0; m<rows; m++){
    dom.world.push([...document.querySelectorAll(`[id^="${m},"]`)])
}


class Playground {

    constructor() {
        this.state = []
        this.rows = 0
        this.cols = 0

        this.server = new WebSocket('ws://localhost:8080')
        this.server.onmessage = async (e) => {
            let data = JSON.parse(e.data)
            if (data.state){
                this.state = data.state
                this.rows = this.state.length
                this.cols = this.state[0].length
            }
            await playground.update(data.values, data.policy)
        }
        this.server.onopen = async (e) => {
            await this.reset()
        }

    }

    async message(command, params = {}){ // todo: move to server class
        let msg = JSON.stringify([ command, params])
        this.server.send(msg)
    }

    async sample(row, col){
        if (!this._isWall(row, col)) {
            this.message('sample', {position: [row, col]})
        }
    }

    async evaluate(){
        this.message('evaluate')
    }

    async reset(){
        this.message('reset')
    }

    colors(pos){
        let intensity = 100 // 0..255
        let red   = Math.round(pos < 0.5 ? intensity : ((1 - pos) * 2) * intensity)
        let green = Math.round(pos < 0.5 ? (pos * 2) * intensity : intensity)
        let blue  = 0
        let alpha  = 1.0
        return [red, green, blue, alpha]
    }

    update(values, policy) {
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
                dom.world[m][n].className = dictClasses[this.state[m][n]]
            }
        }
    }

    _isTerminal(m, n){
        return this.state[m][n] === G // this.state[m][n] === Z ||
    }
    _isWall(m, n){
        return this.state[m][n] === W
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

playground = new Playground()
dom.btnEvaluate.addEventListener('click', () => playground.evaluate())
dom.btnReset.addEventListener('click', () => playground.reset())
dom.btnPlay.addEventListener('click', async () => {
    for (let n=0; n<100;n++) await playground.evaluate()
})

dom.showValues.addEventListener('click', () => document.querySelector('.world').classList.toggle('show_values'))
dom.showPolicy.addEventListener('click', () => document.querySelector('.world').classList.toggle('show_policy'))
dom.showColors.addEventListener('click', () => document.querySelector('.world').classList.toggle('show_colors'))

for (let m=0; m<dom.world.length; m++) { // todo: a bit handlebars?
    for (let n = 0; n < dom.world[0].length; n++) {
        dom.world[m][n].addEventListener('click', () => playground.sample(m,n))
        // let timer
        // dom.world[m][n].addEventListener('mousedown', () => timer = setInterval(() => playground.sample(m,n), 1000/30))
        // dom.world[m][n].addEventListener('mouseup', () => clearInterval(timer))
    }
}





























