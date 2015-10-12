import matplotlib.pyplot as plt

from synthesizer import PerlinNoise, PrimeGenerator

if __name__ == '__main__':
    prime_generator = PrimeGenerator(seed=2)
    for octaves in [3, 4, 8, 16]:
        plt.figure()
        parameters = [
            {"persistence": 0.01, "number_of_octaves": octaves},
            {"persistence": 0.10, "number_of_octaves": octaves},
            {"persistence": 0.20, "number_of_octaves": octaves},
            {"persistence": 0.40, "number_of_octaves": octaves},
            {"persistence": 0.50, "number_of_octaves": octaves},
            # {"persistence": 1.00, "number_of_octaves": octaves}
        ]

        for p in parameters:
            noise = PerlinNoise(prime_generator=prime_generator, **p)
            values = [noise(x / 1000.0) for x in range(1000)]

            line = plt.plot(values, label="Persistence: %s" % p["persistence"])

        plt.legend()
        plt.title("Octave count: %d" % octaves)

    plt.show()
