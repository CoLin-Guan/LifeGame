# 单元测试
import pygame, sys, time
import numpy as np
from pygame.locals import *
from main import Cell, draw, next_generation, init, stop, move, gameControl, getWorldSize, setWorldSize
import unittest

# 定义测试类
class CellTestCase(unittest.TestCase):
    # 细胞类
    def setUp(self):
        self.cell = Cell((20,20))
    def tearDown(self):
        self.cell.dispose()
        self.cell = None
    def testSize(self):
        self.cell.setSize(10)
        self.assertEqual(self.cell.size, 10)
    def testPosition(self):
        # 设置矩阵位置
        self.cell.setPosition((100,100))
        self.assertEqual(self.cell.getPosition(), (100, 100))
    def testImage(self):
        image = self.cell.getImage()
        color = image.get_at_mapped((1,1))
        self.assertEqual(color, 16777215)

class TestFun(unittest.TestCase):
    # 测试功能函数
    def setUp(self):
        self.WIDTH = 80
        self.HEIGHT = 60
        pygame.world = np.zeros((self.HEIGHT,self.WIDTH))
        # 随机初始化
        pygame.world[2,2] = 1;
        pygame.world[3,3] = 1;
        pygame.world[10,10] = 1;
        self.cell = Cell((100,100))

    def testWidthHeight(self):
        setWorldSize(80, 60)
        [WIDTH, HEIGHT] = getWorldSize()
        self.assertEqual(WIDTH, 80)
        self.assertEqual(HEIGHT, 60)

    def testNextGeneration(self):
        # 进化迭代测试
        old_world = pygame.world
        new_world = next_generation(pygame.world)
        self.assertTrue((new_world-old_world).any)

        old_world = np.zeros((self.HEIGHT,self.WIDTH))
        old_world[0][0] = 1;
        new_world = next_generation(old_world)
        self.assertEqual(new_world[0][0], 0)

        old_world = np.zeros((self.HEIGHT,self.WIDTH))
        old_world[0][0] = 1;
        old_world[0][1] = 1;
        old_world[1][1] = 1;
        old_world[1][0] = 1;
        new_world = next_generation(old_world)
        self.assertEqual(new_world[0][0], 1)
        self.assertEqual(new_world[0][1], 1)


    def testInit(self):
        # 地图初始化测试
        key = init()
        self.assertEqual(key, 'Stop')

    def testGameControl(self):
        class event():
            def __init__(self, type, key):
                self.type = type
                self.key = key

        event1 = event(KEYDOWN, K_SPACE)
        event2 = event(KEYDOWN, K_r)
        key1 = gameControl(event1)
        key2 = gameControl(event2)
        self.assertEqual(key1, 'Stop')
        self.assertEqual(key2, 'Reset')

#测试
if __name__ == "__main__":
    #构造测试集
    suite = unittest.TestSuite()
    suite.addTest(CellTestCase("testSize"))
    suite.addTest(CellTestCase("testPosition"))
    suite.addTest(TestFun("testWidthHeight"))
    suite.addTest(TestFun("testNextGeneration"))
    suite.addTest(TestFun("testInit"))
    suite.addTest(TestFun("testGameControl"))
    #执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)