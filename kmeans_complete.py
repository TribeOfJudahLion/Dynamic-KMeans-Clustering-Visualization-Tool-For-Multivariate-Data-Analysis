import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def load_data(file_path):
    """ Load data from a file. """
    try:
        data = np.loadtxt(file_path, delimiter=',')
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def plot_initial_data(data):
    """ Plot the initial data points. """
    plt.figure()
    plt.scatter(data[:, 0], data[:, 1], marker='o', facecolors='none', edgecolors='k', s=30)
    plt.title('Input Data')
    set_plot_limits(data)
    plt.xticks(())
    plt.yticks(())
    plt.show()


def set_plot_limits(data):
    """ Set limits for the plot based on the data range. """
    x_min, x_max = data[:, 0].min() - 1, data[:, 0].max() + 1
    y_min, y_max = data[:, 1].min() - 1, data[:, 1].max() + 1
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)


def train_kmeans(data, num_clusters):
    """ Train the KMeans model. """
    kmeans = KMeans(init='k-means++', n_clusters=num_clusters, n_init=10)
    kmeans.fit(data)
    return kmeans


def plot_kmeans_results(data, kmeans, step_size=0.01):
    """ Plot the results of the KMeans clustering. """
    # Create a mesh grid
    x_min, x_max = data[:, 0].min() - 1, data[:, 0].max() + 1
    y_min, y_max = data[:, 1].min() - 1, data[:, 1].max() + 1
    x_values, y_values = np.meshgrid(np.arange(x_min, x_max, step_size), np.arange(y_min, y_max, step_size))

    # Predict labels for all points in the mesh
    predicted_labels = kmeans.predict(np.c_[x_values.ravel(), y_values.ravel()])
    predicted_labels = predicted_labels.reshape(x_values.shape)

    # Plotting
    plt.figure()
    plt.imshow(predicted_labels, interpolation='nearest', extent=(x_min, x_max, y_min, y_max), cmap=plt.cm.Paired,
               aspect='auto', origin='lower')
    plt.scatter(data[:, 0], data[:, 1], marker='o', facecolors='none', edgecolors='k', s=30)

    # Plot centroids
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1], marker='o', s=100, linewidths=2, color='w', zorder=10,
                facecolors='black')

    # Annotate cluster numbers
    for i, centroid in enumerate(centroids):
        plt.annotate(f'Cluster {i + 1}', xy=(centroid[0], centroid[1]), xytext=(3, 3), textcoords='offset points')

    plt.title('Centroids and Boundaries Obtained Using KMeans')
    set_plot_limits(data)
    plt.xticks(())
    plt.yticks(())
    plt.show()


def main():
    input_file = 'data_multivar.txt'
    num_clusters = 4

    # Load and plot data
    data = load_data(input_file)
    if data is not None:
        plot_initial_data(data)

        # Train KMeans and plot results
        kmeans = train_kmeans(data, num_clusters)
        plot_kmeans_results(data, kmeans)


if __name__ == "__main__":
    main()
