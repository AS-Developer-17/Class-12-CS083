import numpy


# Zero Dimensional Array 
arr= numpy.array(3)
print(arr)
print(f'''The accessed element is :
      {arr}
      ''')
print(type(arr))
print(arr.ndim)
print("\n")

# One Dimensional Array
arr= numpy.array([1,2,3])
print(arr)
print(f'''The accessed element is :
      {arr[2]} that should be 3
      ''')
print(type(arr))
print(arr.ndim)
print("\n")


# Two Dimensional Array
arr= numpy.array([[1,2,3],[0,0,2]])
print(arr)
print(f'''The accessed element is :
      {arr[1,2]} that should be 2
      ''')
print(type(arr))
print(arr.ndim)
print("\n")


# Three Dimensional Array
arr= numpy.array([[[1,2,3],[9,2,1]],[[7,0,2],[9,0,2]],[[0,2,4],[9,2,1]]])
print(arr)
print(f'''The accessed element is :
      {arr[1,0,0]} that should be 7
      ''')
print(type(arr))
print(arr.ndim)
print("\n")