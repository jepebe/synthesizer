import matplotlib.pyplot as plt
from synthesizer import PerlinNoise, PrimeGenerator, ShapedNoise, ShapeFunction, ShapeCreator

if __name__ == '__main__':
    realization_count = 10

    prime_generators = {realization : PrimeGenerator(seed=realization) for realization in range(realization_count)}

    for persistence in [0.1, 0.5]:
        plt.figure()
        octaves = 8

        for realization in range(realization_count):
            prime_generator = prime_generators[realization]

            noise = PerlinNoise(persistence=persistence, number_of_octaves=octaves, prime_generator=prime_generator)
            values = [noise(x * 0.001) for x in range(1000)]

            line = plt.plot(values, label="R: %s" % realization)

        plt.legend()
        plt.title("Persistence: %s" % persistence)

    plt.show()