from client import avg, count, count0, _pretty_print

# Our system is configured to use epsilon = 1/2
# for any query.
EPSILON = 0.5

# This class exposes the avg, count, and count0 functions
# while keeping track of the privacy budget.
class BudgetTracker:
  # The privacy budget we start with.
  def __init__(self, budget):
    self.budget = budget
    pass

  # Every time a query is made, this function is called.
  # The function checks that the budget is permissive of making
  # this query. If that is the case, this function should update the budget
  # and return True. Otherwise, this function should raise an error.
  def check_and_update_budget(self):
    # TODO: implement budget check.
    # TODO: update budget if check succeeds.
    if self.budget >= EPSILON:
      self.budget -= EPSILON
      return True
    else:         
      raise ValueError("Out of budget")
  
  def avg(self, group_by, averaged_column):
    self.check_and_update_budget()    
    return avg(group_by, averaged_column, True)
  
  def count(self, group_by):
    self.check_and_update_budget()
    return count(group_by, True)
  
  def count0(self, group_by):
    self.check_and_update_budget()
    return count0(group_by, True)

if __name__ == "__main__":
  # If every query consumes EPSILON = 0.5, then a budget = 2 should be
  # good for 4 queries.
  tracker = BudgetTracker(2.0)

  # These queries should succeed.
  _pretty_print(*tracker.avg(["programming"], "age"))
  _pretty_print(*tracker.count(["age", "music"]))
  _pretty_print(*tracker.count0(["programming"]))
  _pretty_print(*tracker.count(["programming"]))
  
  # This query should fail.
  _pretty_print(*tracker.avg(["sport"], "age"))
