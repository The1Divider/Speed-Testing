import speedtest
import numpy as np
import matplotlib.pyplot as plt
import time
import asyncio
iteration = -1


async def results(array):
    result = await speedTest()
    iteration_number = result[0]
    for i in range(3):
        array[iteration_number, i] = result[i + 1]
    return array


async def speedTest():
    global iteration
    iteration += 1
    st = speedtest.Speedtest()
    latency = st.get_best_server()['latency']
    down = st.download() / 1000000
    up = st.upload() / 1000000
    return iteration, latency, down, up


def main(iterations):
    data = np.zeros((iterations, 3))
    start = time.time()
    start_time = " ".join(time.asctime().split(" ")[1:4])
    for i in range(iterations):
        data = asyncio.run(results(data))
    end_time = " ".join(time.asctime().split(" ")[1:4])
    time_taken = time.time() - start
    np.savetxt("results.dat", data,
               header=f"Time taken = {time_taken/60} min\n,avg latency = {np.average(data[:,0])}, avg download = {np.average(data[:,1])}, "
                      f"avg upload = {np.average(data[:,2])}",
               footer=f"{start_time} - {end_time} , {iterations} iterations")
    while True:
        plot = input("Plot? (y/n):\n").lower()
        if plot == "y":
            x = np.arange(iterations)
            plt.plot(x, data[:, 1], label="Download Speed")
            plt.plot(x, data[:, 2], label="Upload Speed")
            plt.xlabel("Iteration")
            plt.ylabel("Speed (mbps)")
            plt.legend()
            plt.show()
            plt.plot(x, data[:, 0], label="Latency")
            plt.xlabel("Iteration")
            plt.ylabel("Latency (ms)")
            plt.show()
            break
        elif plot == "n":
            break
        else:
            print("Invalid input")


if __name__ == '__main__':
    iterations = input("Iterations = ")
    try:
        iterations = int(iterations)
    except TypeError:
        iterations = 100
    main(iterations)

