import time
import requests
import matplotlib.pyplot as plt
from statistics import mean, variance





def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"Execution time: {end - start:.2f} seconds")

        return end - start
    return wrapper


@log_execution_time
def count_words_dict(text):
    words = text.split()
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    return word_counts

from collections import Counter

@log_execution_time
def count_words_counter(text):
    words = text.split()
    word_counts = Counter(words)
    return word_counts

if __name__ == '__main__':
    url = "https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt"

    response = requests.get(url)
    text = response.text


    # Create two lists to store the execution times for each function
    dict_times = []
    counter_times = []

    # Run the experiment 100 times
    for i in range(100):
        # Measure the time taken for each function to execute
        print(i)
        dict_time = count_words_dict(text)
        counter_time = count_words_counter(text)

        # Add the execution times to the lists
        dict_times.append(dict_time)
        counter_times.append(counter_time)


    # Calculate the mean and variance of the execution times
    dict_mean = mean(dict_times)
    dict_variance = variance(dict_times)
    counter_mean = mean(counter_times)
    counter_variance = variance(counter_times)


    # Plot the distribution of execution times
    plt.plot(dict_times, alpha=0.5, label='Dictionary')
    plt.plot(counter_times, alpha=0.5, label='Counter')
    plt.legend()
    plt.show()
