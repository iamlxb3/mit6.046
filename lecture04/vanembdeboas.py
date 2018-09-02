"""
van Embde Boas Tree
-------------------

Can do the 3 binary search operations:
add, delete, successor

In O(log(log(u))) where u is the
maximum size of the data structure

Recurrence:

T'(u) = T(sqrt(u)) + O(1)

Justification:
Previously shown from analyzing BSTs that
O(log(n)) has the reccurence

T(k) = T(k / 2) + O(1)

So therefore

T(log(k)) = T(log(k) / 2) + O(1)

A substituion of variables

"""


class VEBTreeNode(object):
  def __init__(self, size):
    """
    Create a bit vector of given size
    Works best if size is a perfect square

    """
    sqrt_size = (int(size ** .5))
    self.size = size
    self.sqrt_size = sqrt_size
    self.min = None
    self.max = None
    if size == 2:
      return
    self.summary = VEBTreeNode(sqrt_size)
    self.cluster = [VEBTreeNode(sqrt_size) for _ in range(sqrt_size)]

  def _high(self, x):
    """
    Get the index of which cluster the value x
    would be in

    """
    return x // self.sqrt_size

  def _low(self, x):
    """
    Get the index of x in its respective cluster

    """
    return x % self.sqrt_size

  def _index(self, i, k):
    return (i * self.sqrt_size) + k

  def insert(self, x):
    """
    Insert a value x into the tree in log(log(size)) time

    """
    if self.min is None:
      self.min = self.max = x
      return
    if x < self.min:
      self.min, x = x, self.min
    if x > self.max:
      self.max = x
    i = self._high(x)
    lo = self._low(x)
    if self.cluster[i].min is None:
      self.summary.insert(i)
    self.cluster[i].insert(lo)

  def successor(self, x):
    """
    Get the smallest element in the tree greater than x

    """
    try:
      if self.min is not None \
        and x < self.min:
          return self.min
      i = self._high(x)
      lo = self._low(x)
      if lo < self.cluster[i].max:
        k = self.cluster[i].successor(lo)
      else:
        i = self.summary.successor(i)
        k = self.cluster[i].min
      return self._index(i, k)
    except:
      return None

  def delete(self, x):
    """
    Delete a value x from the tree

    """
    if x == self.min:
      i = self.summary.min
      if i is None: # only happens when we have made the structure completely empty
        self.min = self.max = None
        return
      else:
        x = self.min = self._index(i, self.cluster[i].min)
    i = self._high(x)
    lo = self._low(x)
    self.cluster[i].delete(lo)
    if self.cluster[i].min == None:
      self.summary.delete(i)
    if x == self.max:
      if self.summary.max is None: # means there is at most 1 item left
        self.max = self.min
      else:
        i = self.summary.max
        self.max = self._index(i, self.cluster[i].max)
