import os, sys, time, pygame
from sense_hat import SenseHat
from pygame.locals import *
from random import randint
from time import sleep

class Snake():
	UP = [0, -1]
	DOWN = [0, 1]
	LEFT = [-1, 0]
	RIGHT = [1, 0]

	COLOR_SNAKE = [255, 255, 255]
	COLOR_DEAD_SNAKE = [233, 13, 13]
	COLOR_APPLE = [13, 233, 13]
	COLOR_OFF = [0, 0, 0]

	snake = []
	apple = None
	direction = RIGHT
	score = 0

	def __init__(self):
		pygame.init()
		pygame.display.set_mode((640, 480))

		self.sense = SenseHat()
		self.sense.clear()

		self.playing = True

		self.appendToSnake(2, 2)
		self.appendToSnake(3, 2)
		self.appendToSnake(4, 2)

		self.makeApple()

	def startGame(self):
		pygame.time.set_timer(USEREVENT + 1, 500)
		while self.playing:
			for event in pygame.event.get():
				if event.type == USEREVENT + 1:
					self.move()
				if event.type == KEYDOWN:
					self.changeDirection(event)

					# Exit
					if event.key == pygame.K_RETURN:
						self.playing = False
		self.quitGame()

	def quitGame(self):
		self.sense.clear()
		pygame.quit()
		sys.exit()

	def gameOver(self):
		self.playing = False

		for part in self.snake:
			self.sense.set_pixel(part[0], part[1], self.COLOR_DEAD_SNAKE)

		# Remove the apple
		self.sense.set_pixel(self.apple[0], self.apple[1], self.COLOR_OFF)

		sleep(2)

		msg = "SCORE: {}".format(self.score)
		self.sense.show_message(msg)

	def move(self):
		x = self.snake[-1][0] + self.direction[0]
		y = self.snake[-1][1] + self.direction[1]

		# If x or y is outside of the screen area
		if x > 7:
			x = 0
		elif x < 0:
			x = 7

		if y > 7:
			y = 0
		elif y < 0:
			y = 7

		if [x, y] == self.apple:
			self.makeApple()

		else: 
			last = self.snake.pop(0)
			self.sense.set_pixel(last[0], last[1], self.COLOR_OFF)	

		tmp_snake = self.snake[:]
		tmp_snake.pop()
		for part in tmp_snake:
			if part == [x, y]:
				self.gameOver()

		if self.playing:
			self.snake.append([x, y])
			self.sense.set_pixel(x, y, self.COLOR_SNAKE)

	def appendToSnake(self, x, y):
		self.snake.append([x, y])
		self.sense.set_pixel(x, y, self.COLOR_SNAKE)
		self.score = self.score + 1

	def changeDirection(self, event):
		if event.key == pygame.K_DOWN and self.direction != self.UP:
			self.direction = self.DOWN

		elif event.key == pygame.K_UP and self.direction != self.DOWN:
			self.direction = self.UP

		elif event.key == pygame.K_RIGHT and self.direction != self.LEFT:
			self.direction = self.RIGHT

		elif event.key == pygame.K_LEFT and self.direction != self.RIGHT:
			self.direction = self.LEFT

	def makeApple(self):
		deny_apple = True
		while deny_apple:
			x = randint(0,7)
			y = randint(0,7)
			deny_apple = self.testCollision(x, y)

		self.apple = [x, y]
		self.sense.set_pixel(x, y, self.COLOR_APPLE)

	def testCollision(self, x, y):
		for part in self.snake:
			if part == [x, y]:
				return True
		return False

game = Snake()
game.startGame()


