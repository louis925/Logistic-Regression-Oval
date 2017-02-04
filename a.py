import sys
import math
import matplotlib.pyplot as plt
#import numpy as np

maxfloat = 1e50

def h_theta(x):
  return 0.5 * (1 + math.tanh(0.5 * x))

def h_m_1_theta(x):
  "1 - h_theta(x)"
  return 0.5 * (1 - math.tanh(0.5 * x))

def z_x(x1, x2, tl):
  return tl[0] + tl[1]*x1 + tl[2]*x2 + tl[3]*x1*x1 + tl[4]*x2*x2 + tl[5]*x1*x2

def log_s(x):
  if x == 0:
    return -maxfloat
  else:
    return math.log(x)

def costi(x1, x2, y, tl):
  if y == 1:
    return -log_s( h_theta(z_x(x1, x2, tl)) )
  elif y == 0:
    return -log_s( h_m_1_theta(z_x(x1, x2, tl)) )

def cost_total(xl, yl, tl):
  cost_sum = 0.0
  m = len(yl)
  i = 0
  while i < m:
    cost_sum += costi(xl[i][0], xl[i][1], yl[i], tl)
    i += 1
  return cost_sum/m

def h_y_diff(xl, yl, tl):
  m = len(yl)
  out = [0.0]*m
  i = 0
  while i < m:
    out[i] = h_theta(z_x(xl[i][0], xl[i][1], tl)) - yl[i]
    i += 1
  return out

def x_j(j, x1, x2):
  if j == 0:
    return 1
  if j == 1:
    return x1
  if j == 2:
    return x2
  if j == 3:
    return x1*x1
  if j == 4:
    return x2*x2
  if j == 5:
    return x1*x2

def d_cost_total_j(a, j, xl, yl, tl):
  # j is the element 
  d_cost_sum = 0.0
  m = len(yl)
  h_y_diff_vec = h_y_diff(xl, yl, tl)
  i = 0
  while i < m:
    d_cost_sum += h_y_diff_vec[i] * x_j(j, xl[i][0], xl[i][1])
    i += 1
  return tl[j] - a * d_cost_sum / m

def main():
  in_file = open('aaa.txt', 'rU')
  data = [[float(s) for s in line.strip().split()] for line in in_file]
  in_file.close()
  xl = [[row[1]/64.0, row[2]/64.0] for row in data]
  yl = [int(row[0]) for row in data]
  
  xTplot = [(row[1]/64.0 for row in data if row[0] == 1]
  del data

  n = len(yl)

  if True:
    t0 = -3.446
    t1 = 9.351
    t2 = 16.93
    t11 = -22.55
    t22 = -22.89
    t12 = 7.988
    a = 10
  
  if False:
    r = 10
    t0 = -0.4*r
    t1 = 1*r
    t2 = 1*r
    t11 = -1*r
    t22 = -1*r
    t12 = 0.0*r
    a = 10
  
  

  tl = [t0,t1,t2,t11,t22,t12]
  n_tl = len(tl)
  tl_next = [0.0] * n_tl
  n_run = 500
  i = 0
  while i < n_run:
    j = 0
    """
    while j < n_tl:
      tl[j] = d_cost_total_j(a, j, xl, yl, tl)
      j += 1
    print '{% .4g, % .4g, % .4g, % .4g, % .4g, % .4g}' % tuple(tl)
    print '% .5g' % cost_total(xl, yl, tl)
   
    """
    while j < n_tl:
      tl_next[j] = d_cost_total_j(a, j, xl, yl, tl)
      j += 1
    if i%50 == 0:
      print '{% .4g, % .4g, % .4g, % .4g, % .4g, % .4g}' % tuple(tl_next)
      print '% .5g' % cost_total(xl, yl, tl)
    j = 0
    while j < n_tl:
      tl[j] = tl_next[j]
      j += 1
    
    i += 1
  print '{% .4g, % .4g, % .4g, % .4g, % .4g, % .4g}' % tuple(tl_next)
  print '% .5g' % cost_total(xl, yl, tl)
    
  #temp = [[h_theta(z_x(xl[i][0], xl[i][1], t0, t1, t2, t11, t22, t12)), xl[i]] for i in range(n) if h_theta(z_x(xl[i][0], xl[i][1], t0, t1, t2, t11, t22, t12)) <= 0]
  #print temp 
  #print [math.log(h_theta(z_x(xl[i][0], xl[i][1], t0, t1, t2, t11, t22, t12))) for i in range(20)]
  #print cost_total(xl, yl, t0, t1, t2, t11, t22, t12)
  #print (xl[n-1], yl[n-1])
  return
	
if __name__ == '__main__':
  main()
