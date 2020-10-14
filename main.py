import sys
import time
import asyncio
import speedtest
import numpy as np
import matplotlib.pyplot as plt

iteration = -1
plot = False


async def results(array):
    result = await speedTest()
    iteration_number = result[0]
    for i in range(3):
        array[iteration_number, i] = result[i + 1]
    print(f"Down = {array[iteration_number, 1]} mbps, Latency = {array[iteration_number, 2]} ms")
    return array


async def speedTest():
    global iteration
    iteration += 1
    st = speedtest.Speedtest()
    latency = st.get_best_server()['latency']
    down = st.download() / 1000000
    up = st.upload() / 1000000
    return iteration, latency, down, up


def main(iters, plot):
    data = np.zeros((iters, 3))
    start = time.time()
    start_time = " ".join(time.asctime().split(" ")[1:4])
    for i in range(iters):
        data = asyncio.run(results(data))
    end_time = " ".join(time.asctime().split(" ")[1:4])
    time_taken = time.time() - start
    np.savetxt("results.dat", data,
               header=f"Time taken = {time_taken/60} min\n,avg latency = {np.average(data[:,0])}, avg download = {np.average(data[:,1])}, "
                      f"avg upload = {np.average(data[:,2])}",
               footer=f"{start_time} - {end_time} , {iters} iterations")

    if plot:
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


if __name__ == '__main__':
    opts_list = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args_list = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    help_tag = [opt for opt in opts_list if opt in ["-h, -help, -man, --h, --help"]]

    if len(help_tag) != 0:
        raise SystemExit(f"Usage: {sys.argv[0]} -i #ofIterations\n")
    elif "-i" in opts_list:
        iterations = args_list[opts_list.index("-i")]
    else:
        iterations = 100
    if "-p" in opts_list:
        plot = True

    try:
        iterations = int(iterations)
    except ValueError:
        iterations = 100
        print("Invalid value of iterations, defaulted to 100...")
    main(iterations, plot)
