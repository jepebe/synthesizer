import matplotlib.pyplot as plt

from synthesizer import PerlinNoise, PrimeGenerator, ShapedNoise, ShapeFunction

if __name__ == '__main__':
    prime_generator = PrimeGenerator(seed=1)

    shapes = [
        # {"x": [0.0, 0.5, 1.0], "y": [0.0, 0.5, 1.0]},
        {"x": [0.0, 0.5, 1.0], "y": [1.0, 0.5, 0.0]},
        # {"x": [0.0, 0.5, 1.0], "y": [0.5, 0.5, 0.5]},
        # {"x": [0.0, 0.5, 1.0], "y": [0.0, 0.5, 0.5]},

    ]

    divergences = [{"x": [0.0, 1.0], "y": [0.0, 0.5]},
                  {"x": [0.0, 1.0], "y": [0.25, 0.25]},
                  {"x": [0.0, 0.5, 1.0], "y": [0.25, 0.75, 0.25]}]

    for shape in shapes:
        for divergence in divergences:
            plt.figure()
            octaves = 8
            parameters = [
                {"persistence": 0.01, "number_of_octaves": octaves},
                {"persistence": 0.10, "number_of_octaves": octaves},
                {"persistence": 0.20, "number_of_octaves": octaves},
                {"persistence": 0.40, "number_of_octaves": octaves},
                {"persistence": 0.50, "number_of_octaves": octaves},
            ]

            shapeFunction = ShapeFunction(shape["x"], shape["y"])
            divergenceFunction = ShapeFunction(divergence["x"], divergence["y"])

            for p in parameters:

                noise = PerlinNoise(prime_generator=prime_generator, **p)
                shaper = ShapedNoise(noise, shapeFunction, divergenceFunction)
                values = [shaper(x, scale=0.001) for x in range(1000)]

                line = plt.plot(values, label=str(p))

            plt.legend()

    plt.show()
