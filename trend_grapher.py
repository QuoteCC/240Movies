from graphics import *
import json
import math
import random

################################################################################
#  Global variables - This point is where the user needs to manually enter the #
#  parameters for how the data should be graphed.                              #
################################################################################
#   Variables that control what the page looks like.
TICK_MARKS_ON_X_AXIS = 5
TICK_MARKS_ON_Y_AXIS = 10

X_AXIS_MAX = 500
Y_AXIS_MAX = 100

X_AXIS_LABEL_TEXT = "Avg. Actor Trend Score"
Y_AXIS_LABEL_TEXT = "iMDB Score"

TITLE_TEXT = "BUDGET VS. IMDB SCORE"

WIN_DIM_X = 500
WIN_DIM_Y = 500
WIN_EDGE = 50

#   Variables that control what is done.
METRIC_1 = 'AvgTrendScores'
METRIC_2 = 'imdbScore'

DO_LINE_OF_BEST_FIT = False
K_MEANS_CLUSTERS = 2
        #   Set K_MEANS_CLUSTERS = 0 if you don't want to do k-means clustering.
USE_RELATIVE_CLUSTERING_MODE = True
        #   Set to False if you want to use absoulute Euclidean distance instead
        #   of relative Euclidean distance in clustering.

X_AXIS_ALARM_THRESHOLD = 540
Y_AXIS_ALARM_THRESHOLD = 420
        #   Set ..._ALARM_THRESOLD = 0 if you don't want to print warnings.
################################################################################
#   End manual user entry.                                                     #
################################################################################

def main():
    #   Initialize the graphics window.
    graphics_window = GraphWin("Trend Grapher Window", WIN_DIM_X, WIN_DIM_Y)

    #   Draw the x and y axes.
    x_axis = Line(Point(WIN_EDGE, WIN_DIM_Y - WIN_EDGE), \
                  Point(WIN_DIM_X - WIN_EDGE, WIN_DIM_Y - WIN_EDGE))
    y_axis = Line(Point(WIN_EDGE, WIN_EDGE), \
                  Point(WIN_EDGE, WIN_DIM_Y - WIN_EDGE))
    x_axis.draw(graphics_window)
    y_axis.draw(graphics_window)

    #   Draw the tick marks on the axes; if TICK_MARKS_ON_AXIS <= 0, skip.
    if TICK_MARKS_ON_X_AXIS > 0:
        tick_mark_dist = float(WIN_DIM_X - 2 * WIN_EDGE) / TICK_MARKS_ON_X_AXIS

        for i in range(0, TICK_MARKS_ON_X_AXIS + 1):
            tick_mark = Line(Point(WIN_EDGE + int(i * tick_mark_dist), \
                                    WIN_DIM_Y - WIN_EDGE - WIN_EDGE / 5), \
                             Point(WIN_EDGE + int(i * tick_mark_dist), \
                                    WIN_DIM_Y - WIN_EDGE + WIN_EDGE / 5))
            tick_mark.draw(graphics_window);

            label_value = int(i * float(X_AXIS_MAX) / TICK_MARKS_ON_X_AXIS)
            label = Text(Point(WIN_EDGE + int(i * tick_mark_dist), \
                                    WIN_DIM_Y - WIN_EDGE + 2 * (WIN_EDGE / 5)), \
                    label_value)
            label.draw(graphics_window)


    if TICK_MARKS_ON_Y_AXIS > 0:
        tick_mark_dist = float(WIN_DIM_Y - 2 * WIN_EDGE) / TICK_MARKS_ON_Y_AXIS

        for i in range(0, TICK_MARKS_ON_Y_AXIS + 1):
            tick_mark = Line(Point(WIN_EDGE - WIN_EDGE / 5, \
                                    WIN_EDGE + int(i * tick_mark_dist)), \
                             Point(WIN_EDGE + WIN_EDGE / 5, \
                                    WIN_EDGE + int(i * tick_mark_dist)))
            tick_mark.draw(graphics_window);

            label_value = int((TICK_MARKS_ON_Y_AXIS - i) * \
                    float(Y_AXIS_MAX) / TICK_MARKS_ON_Y_AXIS)
            label = Text(Point(WIN_EDGE - 2 * WIN_EDGE / 5, \
                                    WIN_EDGE + int(i * tick_mark_dist)), \
                    label_value)
            label.draw(graphics_window)

    #   Use getData() to get the data we want to plot.
    get_data_results = getData()

    #   Draw the axes labels, title text, and correlation coefficient. Note
    #   that, for the y-axis, we print each letter one row at a time (since
    #   there is no way to rotate text).
    x_axis_label = Text(Point(WIN_DIM_X / 2, \
            WIN_DIM_Y - WIN_EDGE + 3.5 * (WIN_EDGE / 5)), \
            X_AXIS_LABEL_TEXT)
    x_axis_label.draw(graphics_window)

    title_label = Text(Point(WIN_DIM_X / 2, WIN_EDGE - 3.5 * (WIN_EDGE / 5)), \
            TITLE_TEXT)
    title_label.draw(graphics_window)

    correlation_label = Text(Point(WIN_DIM_X / 2, WIN_EDGE - 2 * WIN_EDGE / 5), \
            "r^2 = " + str(get_data_results[3]))
    correlation_label.draw(graphics_window)

    for i in range(0, len(Y_AXIS_LABEL_TEXT)):
        number_of_letters_after_midpoint = i - len(Y_AXIS_LABEL_TEXT) / 2

        y_axis_letter = Text(Point(WIN_EDGE - 4 * (WIN_EDGE / 5), \
            WIN_DIM_Y / 2 + (12 * number_of_letters_after_midpoint)), \
            Y_AXIS_LABEL_TEXT[i])
        y_axis_letter.draw(graphics_window)

    #   Do k-means clustering (if the user entered a valid number of means).
    if K_MEANS_CLUSTERS > 0:
        means = performKMeansClustering(K_MEANS_CLUSTERS, get_data_results[0])

    #   Draw the data points. Data points are stored as a list; in the list
    #   returned from getData(), they are the first entry (at index 0)
    for data_point in get_data_results[0]:
        data_point_on_graph = Circle(Point(float(WIN_DIM_X - 2 * WIN_EDGE) \
                                            * data_point[0] / \
                                            X_AXIS_MAX + WIN_EDGE, \
                                        WIN_DIM_Y - WIN_EDGE - \
                                            float(WIN_DIM_Y - 2 * WIN_EDGE) \
                                            * data_point[1] / Y_AXIS_MAX), 2)

        data_point_on_graph.setOutline(getColorFromCluster(data_point[2]))
        data_point_on_graph.setFill(getColorFromCluster(data_point[2]))
        data_point_on_graph.draw(graphics_window)

    #   Draw the means (once again, if the user entered a valid number of them).
    if K_MEANS_CLUSTERS > 0:
        for i in range(0, len(means)):
            data_point = means[i]
            data_point_on_graph = Rectangle(
                                        Point(float(WIN_DIM_X - 2 * WIN_EDGE) \
                                            * data_point[0] / \
                                            X_AXIS_MAX + WIN_EDGE - 2, \
                                        WIN_DIM_Y - WIN_EDGE - \
                                            float(WIN_DIM_Y - 2 * WIN_EDGE) \
                                            * data_point[1] / Y_AXIS_MAX - 2),
                                        Point(float(WIN_DIM_X - 2 * WIN_EDGE) \
                                            * data_point[0] / \
                                            X_AXIS_MAX + WIN_EDGE + 2, \
                                        WIN_DIM_Y - WIN_EDGE - \
                                            float(WIN_DIM_Y - 2 * WIN_EDGE) \
                                            * data_point[1] / Y_AXIS_MAX + 2))

            #   We always draw means/centers in black. The reason for this is
            #   simple: against a background of a bunch of points colored to
            #   match the cluster, it should stand out. Note that we still keep
            #   the outline in the cluster color, just in case two are really
            #   close to each other.
            data_point_on_graph.setOutline(getColorFromCluster(i + 1))
            data_point_on_graph.setFill('black')
            data_point_on_graph.draw(graphics_window)

    #   Draw the line-of-best-fit (if the user asked us to; even if the user
    #   didn't we still calculate the endpoints, since the computational
    #   power required is negligible).
    if DO_LINE_OF_BEST_FIT:
        line_of_best_fit = Line(Point(float(WIN_DIM_X - 2 * WIN_EDGE) \
                                        * get_data_results[1][0] /
                                        X_AXIS_MAX + WIN_EDGE,
                                    WIN_DIM_Y - WIN_EDGE - \
                                        float(WIN_DIM_Y - 2 * WIN_EDGE)
                                        * get_data_results[1][1] / Y_AXIS_MAX),
                                Point(float(WIN_DIM_X - 2 * WIN_EDGE) \
                                        * get_data_results[2][0] /
                                        X_AXIS_MAX + WIN_EDGE,
                                    WIN_DIM_Y - WIN_EDGE - \
                                        float(WIN_DIM_Y - 2 * WIN_EDGE)
                                        * get_data_results[2][1] / Y_AXIS_MAX))
        line_of_best_fit.draw(graphics_window)

    #   Print a few status messages.
    print (len(get_data_results[0]), "total points plotted.")
    print (get_data_results[4], "points had invalid/out-of-bounds data.")

    #   Pause the graphics window (so we can view the graphed data); when done,
    #   close the graphics window (this will exit the program).
    graphics_window.getMouse()
    graphics_window.close()

#   The performKMeansClustering() function is used to assign clusters to points
#   in a data set. It takes a list of 3-tuples as input, resets the cluster
#   value to 0 for all of them (in case we accidentally already have something
#   there), and sorts them into num_means clusters. Initial means are random.
#
#   Returns the list of means (data_points should be updated, since it should
#   be passed in by-reference).
def performKMeansClustering(num_means, data_points):
    #   Initialize the empty list of means and at_least_one_change (a boolean
    #   value that will be used to determine when k-means clustering has
    #   finished).
    means = []
    at_least_one_change = True

    #   Create our initial means (randomly).
    for i in range(0, num_means):
        means.append([random.uniform(0.0, X_AXIS_MAX), \
                random.uniform(0.0, Y_AXIS_MAX)])

    for mean in means:
        print "The mean is ", mean[0], ",", mean[1]

    while at_least_one_change:
        at_least_one_change = False
        data_points_moved_this_loop = 0

        #   Recaltulate the clusters the points belong in.
        for data_point in data_points:
            closest_mean = 0
            closest_mean_dist = float('inf')

            #   Find the closest mean.
            for i in range(0, num_means):
                if USE_RELATIVE_CLUSTERING_MODE:
                    dist = math.sqrt((means[i][0]/X_AXIS_MAX - data_point[0]/X_AXIS_MAX) ** 2 + \
                                     (means[i][1]/Y_AXIS_MAX - data_point[1]/Y_AXIS_MAX) ** 2)
                else:
                    dist = math.sqrt((means[i][0] - data_point[0]) ** 2 + \
                                     (means[i][1] - data_point[1]) ** 2)

                if dist < closest_mean_dist:
                    #   Note that, since 0 is used for "no cluster", we here
                    #   increment the index value of the closest mean, to ensure
                    #   we get the proper cluster number.
                    closest_mean = i + 1
                    closest_mean_dist = dist

            #   Determine if we are reassigning clusters; if we are, reassign
            #   the cluster and set at_least_one_change to True.
            if data_point[2] != closest_mean:
                data_point[2] = int(closest_mean)
                at_least_one_change = True
                data_points_moved_this_loop = data_points_moved_this_loop + 1

        #   Recalculate the cluster means.
        for i in range(0, num_means):
            x_sum = 0.0
            y_sum = 0.0
            point_count = 0

            for data_point in data_points:
                #   If this data point belongs to the current mean, update x_sum
                #   and y_sum, as well as point_count. If not, skip it.
                if data_point[2] == i + 1:
                    x_sum = x_sum + data_point[0]
                    y_sum = y_sum + data_point[1]
                    point_count = point_count + 1

            #   If we have no points, then we don't recalculate the mean
            #   (really, this should never happen; we're just doing this to
            #   avoid divide-by-zero errors). If we have at least one point in
            #   this mean's cluster, recalculate the mean.
            if point_count > 0:
                means[i][0] = x_sum / point_count
                means[i][1] = y_sum / point_count

        print data_points_moved_this_loop, "data points moved this loop."

    return means

#   The getColorFromCluster() function offers a simple lookup table to color
#   data points based on their cluster. Note that we have a limit of 9 clusters
#   (anything else will just be colored brown), and, in practice, a limit of 8
#   (since cluster == 0 is used for non-clusterd data).
def getColorFromCluster(cluster):
    if cluster == 0:
        return 'black'
    elif cluster == 1:
        return 'red'
    elif cluster == 2:
        return 'blue'
    elif cluster == 3:
        return 'green'
    elif cluster == 4:
        return 'yellow'
    elif cluster == 5:
        return 'magenta'
    elif cluster == 6:
        return 'cyan'
    elif cluster == 7:
        return 'orange'
    else:
        return 'brown'


#   The getData() function is used to generate the data points that will be
#   graphed in main(). We re-used this script several times when generating our
#   numerous graphs, with the only major change being how we calculated the
#   x_axis_value and y_axis_value for each point; this is controlled in the
#   global variables block at the top of this script.
#
#   The function itself returns a list (so that we could return several useful,
#   easily-calculated values in addition to returning just a list of points).
#   The following list indicates what is stored at each index of this return:
#       0   The nested list of data points (list of 3-len lists; the first two
#               indices store x/y coordinate data; the last index stores cluster
#               data, which defaults to 0).
#       1   One of the endpoints of the best-fit line (2-length list).
#       2   One of the endpoints of the best-fit line (2-length list).
#       3   The r^2 value (float).
#       4   The total number of data points we were unable to use (int).
#
#   Note that 0, 1, and 2 are given in terms of their numbers here, NOT their
#   actual physical plots on the graph (calculated in terms of WIN_X_DIM, etc.);
#   that will be done later.
def getData():
    #   Initialize the empty data_points list (returned at index 0) and the
    #   default value for unusable_points (returned at index 4).
    data_points = []
    unusable_points = 0

    #   Load the master_dataset.txt file.
    with open('master_dataset.txt') as dataset_file:
        dataset_movie_list = dataset_file.readlines()

    #   For each movie in the dataset...
    for movie in dataset_movie_list:
        #   Initialize the json for this particular movie.
        movie_json = json.loads(movie)

        try:
            x_axis_value = float(movie_json[METRIC_1])
            y_axis_value = float(movie_json[METRIC_2])

            if x_axis_value <= X_AXIS_MAX and y_axis_value <= Y_AXIS_MAX and \
                    x_axis_value >= 0 and y_axis_value >= 0:
                #   Both of the values are within the boundaries; we can graph
                #   this data point, so we add it to data_points.
                data_points.append([x_axis_value, y_axis_value, 0])


            #   Print warnings if values exceed ..._ALARM_THRESOLDs.
            if x_axis_value > X_AXIS_ALARM_THRESHOLD \
                    and X_AXIS_ALARM_THRESHOLD > 0:
                print "Warning:", str(movie_json['Title']), "exceeds", \
                        X_AXIS_ALARM_THRESHOLD, "for", METRIC_1, ":", \
                        str(x_axis_value)

            if y_axis_value > Y_AXIS_ALARM_THRESHOLD \
                    and Y_AXIS_ALARM_THRESHOLD > 0:
                print "Warning:", str(movie_json['Title']), "exceeds", \
                        Y_AXIS_ALARM_THRESHOLD, "for", METRIC_2, ":", \
                        str(y_axis_value)
        except:
            #   One of the values is entered incorreclty; as a result, we cannot
            #   graph this data point.
            unusable_points = unusable_points + 1

    #   Calculate the values we need to find the endpoints of the line of best
    #   fit and the correlation coefficient.
    x_sum = 0.0
    y_sum = 0.0
    x_sq_sum = 0.0
    y_sq_sum = 0.0
    xy_sum = 0.0
    x_var_numer = 0.0
    y_var_numer = 0.0
    xy_cov_numer = 0.0

    for data_point in data_points:
        x_sum = x_sum + data_point[0]
        y_sum = y_sum + data_point[1]
        x_sq_sum = x_sq_sum + data_point[0] ** 2
        y_sq_sum = y_sq_sum + data_point[1] ** 2
        xy_sum = xy_sum + data_point[0] * data_point[1]

        x_mean = float(x_sum) / len(data_points)
        y_mean = float(y_sum) / len(data_points)

    for data_point in data_points:
        x_var_numer = x_var_numer + (data_point[0] - x_mean) ** 2
        y_var_numer = y_var_numer + (data_point[1] - y_mean) ** 2
        xy_cov_numer = xy_cov_numer + (data_point[0] - x_mean) * (data_point[1] - y_mean)

    #   Calculate the slope and y-intercept of the line of best fit.
    slope = ((len(data_points) * xy_sum) - (x_sum * y_sum)) / \
            ((len(data_points) * x_sq_sum) - (x_sum ** 2))
    y_intercept = ((x_sq_sum * y_sum) - (x_sum * xy_sum)) / \
            ((len(data_points) * x_sq_sum) - x_sum ** 2)


    #   Calculate the endpoints. For now, we will simply use x = 0 and x =
    #   X_AXIS_MAX; later, we may wish to change this.
    endpoint_1 = [0, y_intercept]
    endpoint_2 = [X_AXIS_MAX, X_AXIS_MAX * slope + y_intercept]


    print "m = ", slope
    print "b = ", y_intercept

    x_var = x_var_numer / (len(data_points) - 1)
    y_var = y_var_numer / (len(data_points) - 1)
    x_stdev = math.sqrt(x_var)
    y_stdev = math.sqrt(y_var)
    xy_cov = xy_cov_numer / (len(data_points) - 1)

    #   Calculate the correlation.
    correlation = (xy_cov / (x_stdev * y_stdev)) ** 2

    return [data_points, endpoint_1, endpoint_2, correlation, unusable_points]

main()
