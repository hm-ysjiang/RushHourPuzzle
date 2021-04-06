/*
 * @author hmysjiang
 */

const CAR_COLORS = [
	'red', '#39e667', '#25e8d1', '#1597ed', '#ffbe7d', '#bd4061',
	'#d8fa2d', '#999eff', '#002473', '#3c267a', '#44804a', '#e317c1',
	'#8736d9', '#73e86b', '#782076', '#00f2ff', '#ff8000', '#bcf7c8'
]

var DOM_puzzle
var DOM_solution
var DOM_flag

var RUNNING = false
var map
var hold = 0
const HOLD_THRESHOLD = 25

function setup() {
	createCanvas(450, 600).parent('p5container')
	DOM_puzzle = select('#puzzle')
	DOM_solution = select('#solution')
	DOM_flag = select('#flag')
}

function mousePressed() {
	if (map.prev != null && mouseX >= 45 && mouseX < 165 && mouseY >= 510 && mouseY < 550) {
		hold = 1
		map = map.prev
	}
	else if (map.next != null && mouseX >= 285 && mouseX < 405 && mouseY >= 510 && mouseY < 550) {
		hold = 1
		map = map.next
	}
}

function mouseReleased() {
	hold = 0
}

function draw() {
	if (DOM_flag.value() == 'ready') {
		RUNNING = true
		DOM_flag.value('running')

		map = populateHistory(DOM_puzzle.value().split('\n').filter(_ => _), DOM_solution.value().split('\n').filter(_ => _))
	}
	if (RUNNING) {
		background('#eaeaea')
		drawGameBackground()
		map.render()
		drawButton()
		if (hold > 0) {
			hold = min(hold + 1, HOLD_THRESHOLD)
			if (hold == HOLD_THRESHOLD) {
				if (map.prev != null && mouseX >= 45 && mouseX < 165 && mouseY >= 510 && mouseY < 550) {
					map = map.prev
				}
				else if (map.next != null && mouseX >= 285 && mouseX < 405 && mouseY >= 510 && mouseY < 550) {
					map = map.next
				}
			}
		}
	}
}

function drawGameBackground() {
	push()
	noStroke()
	translate(31, 31)
	fill('black')
	rect(0, 0, 388, 388)
	fill('white')
	for (let row = 0; row < 6; row++)
		for (let col = 0; col < 6; col++)
			rect(4 + 64 * col, 4 + 64 * row, 60, 60)
	rect(384, 138, 4, 48)
	pop()
}

function drawButton() {
	push()
	translate(225, 510)
	strokeWeight(2)
	fill('#bbbbbb')
	if (map.prev != null)
		rect(-180, 0, 120, 40)
	if (map.next != null)
		rect(60, 0, 120, 40)

	fill('black')
	textAlign(CENTER, CENTER)
	textSize(20)
	translate(-120, 0)
	if (map.prev != null)
		text('Prev', 0, 20)
	translate(240, 0)
	if (map.next != null)
		text('Next', 0, 20)
	pop()
}

function populateHistory(puzzle, solution) {
	let init = new Map(puzzle)
	init.updateHash()
	let cur = init
	for (let i = 0; i < solution.length; i++)
		cur = cur.connect(solution[i])
	return init
}

class Map {
	constructor(puzzle, cars = null) {
		this.prev = null
		this.next = null

		if (puzzle == null) {
			this.cars = cars.slice()
		}
		else {
			this.cars = puzzle.map(car => new Car(car))
			this.steps = 0
		}
	}

	connect(step) {
		let new_map = new Map(null, this.cars)
		new_map.steps = this.steps + 1
		new_map.cars[parseInt(step.split()[0])] = new Car(null, new_map.cars[parseInt(step.split()[0])], step)
		this.next = new_map
		new_map.prev = this
		new_map.updateHash()
		return new_map
	}

	render() {
		for (let i = 0; i < this.cars.length; i++)
			this.cars[i].render()
		push()
		translate(225, 435)
		textSize(20)
		textAlign(CENTER, TOP)
		text(`Step ${this.steps}`, 0, 0)
		textSize(12)
		text(this.hash, 0, 32)
		pop()
	}

	updateHash() {
		this.hash = sha1(this.cars.reduce((accu, cur) => (`${accu} ${cur.id},${cur.row},${cur.col},${cur.len},${cur.orient}`), '')).toUpperCase()
	}
}

class Car {
	constructor(spec, car = null, step = null) {
		if (spec != null) {
			const [id, row, col, len, orient] = spec.split(' ')
			this.id = parseInt(id)
			this.row = parseInt(row)
			this.col = parseInt(col)
			this.len = parseInt(len)
			this.orient = parseInt(orient)
		}
		else {
			const [id, row, col] = step.split(' ')
			this.id = car.id
			this.row = row
			this.col = col
			this.len = car.len
			this.orient = car.orient
		}
	}

	render() {
		push()
		noStroke()
		translate(31, 31)
		fill(CAR_COLORS[this.id])
		rect(8 + 64 * this.col, 8 + 64 * this.row,
			this.orient == 1 ? 52 + 64 * (this.len - 1) : 52,
			this.orient == 2 ? 52 + 64 * (this.len - 1) : 52)
		pop()
	}
}