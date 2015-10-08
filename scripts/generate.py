#! /usr/bin/env python

from synthesizer import PerlinNoise

def createObservationFile(report_step, observation, count, std=0.2):
    with open("perlin_obs_%d.txt" % report_step, "w") as f:

        for index in range(count):
            x = index / 8.0
            f.write("%f %f\n" % (observation.perlinNoise1D(x), std))



def readParameters(filename):
    params = {}
    with open(filename, "r") as f:
        for line in f:
            key, value = line.split(":", 1)
            params[key] = float(value)

    return params


if __name__ == "__main__":
    count = 100

    # primes = []
    # for p in range(128):
    #     primes.append(str(PerlinNoise.createPrime(7)))
    #
    # print(",".join(primes))

    observations = {1: PerlinNoise(prime_1=15731, prime_2=789221, prime_3=1376312589),
                    2: PerlinNoise(prime_1=8831, prime_2=1300237, prime_3=32416187567),
                    3: PerlinNoise(prime_1=10657, prime_2=105767, prime_3=2902956923)}

    for report_step in observations:
        observation = observations[report_step]
        # createObservationFile(report_step, observation, count)

        params = readParameters("perlin_params.txt")

        scale = params["SCALE"]
        offset = params["OFFSET"]
        octaves = int(round(params["OCTAVES"]))
        persistence = params["PERSISTENCE"]
        p1_index = int(round(params["PRIME_1"]))
        p2_index = int(round(params["PRIME_2"]))
        p3_index = int(round(params["PRIME_3"]))

        with open("perlin_%d.txt" % report_step, "w") as f:
            P1 = PRIME_INDEX_1[p1_index]
            P2 = PRIME_INDEX_2[p2_index]
            P3 = PRIME_INDEX_3[p3_index]
            # P1 = PerlinNoise.createPrime()
            # P2 = PerlinNoise.createPrime()
            # P3 = PerlinNoise.createPrime()
            report_step_noise = PerlinNoise(persistence=persistence, number_of_octaves=octaves, prime_1=P1, prime_2=P2, prime_3=P3)

            for i in range(count):
                x = i / 8.0
                obs = observation.perlinNoise1D(x)
                noise = report_step_noise.perlinNoise1D(x)
                f.write("%f\n" % (obs + offset + noise * scale))
