import math
from synthesizer import PrimeGenerator, PerlinNoise


class Interpolator(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        assert len(x) == len(y)

    def __call__(self, x):
        if x <= self.x[0]:
            y = self.y[0]
        elif x >= self.x[len(self.x) - 1]:
            y = self.y[len(self.x) - 1]
        else:
            y = None
            for i in range(len(self.x) - 1):
                if self.x[i] <= x < self.x[i + 1]:
                    x_diff = self.x[i + 1] - self.x[i]
                    frac_x = (x - self.x[i]) / x_diff
                    y = self.cosineInterpolation(self.y[i], self.y[i + 1], frac_x)
                    break

        return y

    def cosineInterpolation(self, a, b, x):
        ft = x * 3.1415927
        f = (1.0 - math.cos(ft)) * 0.5
        return a * (1 - f) + b * f


class ShapeFunction(object):
    def __init__(self, x, y):
        self.interpolator = Interpolator(x, y)

    def __call__(self, x):
        return self.interpolator(x)


class ShapedPerlin(object):

    def __init__(self, perlin, shapeFunction, divergenceFunction, scale=1.0):
        self.shapeFunction = shapeFunction
        self.divergenceFunction = divergenceFunction
        self.perlin = perlin
        self.scale = scale

    def __call__(self, x):
        scaled_x = x * self.scale
        return self.shapeFunction(scaled_x) + self.perlin(x) * self.divergenceFunction(scaled_x)



class ShapeCreator(object):

    @staticmethod
    def createShapeFunction(count=1000, persistence=0.2, octaves=8, seed=1):
        prime_generator = PrimeGenerator(seed=seed)
        perlininator = PerlinNoise(persistence=persistence, number_of_octaves=octaves, prime_generator=prime_generator)

        x_values = [x / float(count) for x in range(count)]
        y_values = [perlininator(x * 10.0) for x in x_values]

        return ShapeFunction(x_values, y_values)
