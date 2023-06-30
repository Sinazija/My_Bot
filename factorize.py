import multiprocessing
import time


def factorize(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors


def parallel_factorize(numbers):
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = pool.map(factorize, numbers)
    pool.close()
    pool.join()
    return results


def main():
    # Синхронна версія
    start_time = time.time()

    a, b, c, d = factorize(128), factorize(
        255), factorize(99999), factorize(10651060)

    end_time = time.time()

    execution_time = end_time - start_time
    print("Execution Time (Synchronous):", execution_time)

    # Паралельна версія
    start_time = time.time()

    numbers = [128, 255, 99999, 10651060]
    results = parallel_factorize(numbers)

    end_time = time.time()

    execution_time = end_time - start_time
    print("Execution Time (Parallel):", execution_time)


if __name__ == '__main__':
    main()
