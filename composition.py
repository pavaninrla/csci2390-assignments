from client import avg, count, count0, _pretty_print
from dp import dp_histogram

# This function should expose the true value of some aggregate/query
# by abusing the fact that you can make many such queries.
# query_func is a 0-arguments function, every time you call it, you execute the
# query once and get one set of results.
def expose(query_func):
  headers, many_results = None, []
  # Make many queries and save their results.
  print("Making 200 queries with noise. This may take a minute...")
  for i in range(200):
    headers, results = query_func()
    many_results.append(results)

  # Expose the value of the query.
  #
  # many_results is structured as follows:
  # - many_results is a list of results from the 200 queries
  # - many_results[i] is a set of rows returned from a particular query
  # - many_results[i][r] is a set of columns for the query, with the aggregation
  #   value in the last column
  exposed_result = []
  num_iterations = len(many_results)
  cols = len(headers)
  rows = len(many_results[0])
  # This generates a single table with `rows` rows; your task is to use
  # `many_results` to compute each row's aggregation value.
  for r in range(0, rows):
    # TODO: compute the actual value of row r, given all the noised values from
    # making many queries.
    
    # Combine the results to factor out the noise
    values = [many_results[i][r][-1] for i in range(num_iterations)]
    value = sum(values) / num_iterations
    #value = round(value)

    # Append value and attached label to exposed result.
    labels = tuple(many_results[0][r][:-1])
    exposed_result.append(labels + (value,))    

  return headers, exposed_result

if __name__ == "__main__":
  # For testing: if your expose function works, then you should be able
  # to expose the original results of the age and music histogram from 
  # the noised data.
  print("TESTING: the two histograms should be (almost) equal.\n")



  print("Non-noised histogram (from part 1):")
  headers, result = count(["age", "music"], False)
  _pretty_print(headers, result)

  headers, result = expose(lambda: dp_histogram(0.5))
  _pretty_print(headers, result)  

  # Expose the average age per programming level.
  
  print("Exposing average:")
  headers, result = expose(lambda: avg(["programming"], "age", True))
  _pretty_print(headers, result)
  print("")
  
  
  # Expose the count of people per programming level.
  
  print("Exposing count:")
  headers, result = expose(lambda: count0(["programming"], True))
  _pretty_print(headers, result)
  print("")
  
