import random
from matplotlib import pyplot as plt
from matplotlib import animation

FPS = 60
MAX_FRAMES = 10000

def create_data(data_size):
    """Create a random data set"""
    data = [x for x in range(data_size)]
    random.shuffle(data)
    return data


def init():
    """Create an empty plot/frame"""
    line.set_data([], [])
    return line,


def bubble_sort(data):
    """Bubble sort method"""
    swapped = True
    for i in range(len(data)-1):
        if not swapped:
            break
        swapped = False
        for j in range(len(data)-1-i):
            if data[j] > data[j+1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
            yield data
    return


def insertion_sort(data):
    """Insertion sort method"""
    for i in range(1, len(data)):

        key = data[i]
        j = i-1

        while j >= 0 and key < data[j]:
            data[j], data[j + 1] = data[j + 1], data[j]
            j -= 1
            yield data
        else:
            yield data


def selection_sort(data):
    """Selection sort method"""
    for i in range(len(data)):

        min_index = i
        min_value = data[i]
        for j in range(i, len(data)):
            if data[j] < min_value:
                min_index = j
                min_value = data[j]
            yield data

        data[i], data[min_index] = data[min_index], data[i]
        yield data

def merge_sort(data, start, end):
    """Merge sort method"""

    if end <= start:
        return

    mid = start + ((end - start + 1) // 2) - 1
    yield from merge_sort(data, start, mid)
    yield from merge_sort(data, mid + 1, end)
    yield from merge(data, start, mid, end)
    yield data


def merge(data, start, mid, end):
    """Helper function for merge sort"""

    merged = []
    left_index = start
    right_index = mid + 1
    while left_index <= mid and right_index <= end:
        if data[left_index] < data[right_index]:
            merged.append(data[left_index])
            left_index += 1
        else:
            merged.append(data[right_index])
            right_index += 1

    while left_index <= mid:
        merged.append(data[left_index])
        left_index += 1

    while right_index <= end:
        merged.append(data[right_index])
        right_index += 1

    for i, sorted_val in enumerate(merged):
        data[start + i] = sorted_val
        yield data


def update_fig(data, rects, iteration):
    """Updates the number of comparisons text"""
    for rect, val in zip(rects, data):
        rect.set_height(val)
    iteration[0] += 1
    text.set_text("# of comparisons: %s" % iteration[0])

# all the different sort sizes wanted
data_sizes = [10, 15, 25, 50, 75, 100, 150, 200]
# loop through every size wanted
for j, data_size in enumerate(data_sizes):

    data = create_data(data_size)

    generators = [bubble_sort(data.copy()), merge_sort(data.copy(), 0, data_size-1),
                  selection_sort(data.copy()), insertion_sort(data.copy())]
    sort_names = ["bubble_sort", "merge_sort", "selection_sort", "insertion_sort"]

    # loop through each sort method and visualise sorting method and save to a mp4
    for i, gen in enumerate(generators):

        print(gen, "-" data_size)

        fig, ax = plt.subplots()

        bar_rects = ax.bar(range(len(data)), data, align="edge")

        plt.title(sort_names[i])

        ax.set_xlim(0, data_size)
        ax.set_ylim(0, int(1.07 * data_size))

        text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

        iteration = [0]

        anim = animation.FuncAnimation(fig, func=update_fig,
                                       fargs=(bar_rects, iteration), frames=gen, interval=1,
                                       repeat=False, save_count=MAX_FRAMES)

        plt.rcParams['animation.ffmpeg_path'] ='E:\\Videos\\ffmpeg\\bin\\ffmpeg.exe'
        FFwriter = animation.FFMpegWriter(fps=FPS)
        name = "video\\" + sort_names[i] + "-" + str(data_size) + ".mp4"
        anim.save(name, writer=FFwriter)

        # show the animation
        # plt.show()

        plt.close()

