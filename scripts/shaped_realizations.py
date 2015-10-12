import matplotlib.pyplot as plt
from synthesizer import PerlinNoise, PrimeGenerator, ShapedNoise, ShapeFunction, ShapeCreator

if __name__ == '__main__':
    realization_count = 10
    # shape = {"x": [0.0, 0.5, 1.0], "y": [1.0, 0.5, 0.0]}
    # shapeFunction = ShapeFunction(shape["x"], shape["y"])
    shapeFunction = ShapeCreator.createShapeFunction(seed=2)

    divergence = {"x": [0.0, 0.3, 0.4, 0.6, 1.0], "y": [0.01, 0.1, 0.2, 0.2, 0.5]}
    # divergence = {"x": [0.0, 1.0], "y": [0.1, 0.1]}
    divergenceFunction = ShapeFunction(divergence["x"], divergence["y"])

    prime_generators = {realization : PrimeGenerator(seed=realization) for realization in range(realization_count)}

    for persistence in [0.1, 0.5]:
        plt.figure()
        octaves = 8

        for realization in range(realization_count):
            prime_generator = prime_generators[realization]

            noise = PerlinNoise(persistence=persistence, number_of_octaves=octaves, prime_generator=prime_generator)
            shaper = ShapedNoise(noise, shapeFunction, divergenceFunction, scale=0.1)
            values = [shaper(x / 100.0) for x in range(1000)]

            line = plt.plot(values, label="R: %s" % realization)

        plt.legend()
        plt.title("Persistence: %s" % persistence)

    plt.show()