
E3 = (1.0, 2.2, 4.7)

E6 = (1.0, 1.5, 2.2, 3.3, 4.7, 6.8)

E12 = (1.0, 1.2, 1.5, 1.8, 2.2, 2.7,
       3.3, 3.9, 4.7, 5.6, 6.8, 8.2)

E24 = (1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
       3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1)

E48 = (1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54, 1.62, 1.69, 
       1.78, 1.87, 1.96, 2.05, 2.15, 2.26, 2.37, 2.49, 2.61, 2.74, 2.87, 3.01, 
       3.16, 3.32, 3.48, 3.65, 3.83, 4.02, 4.22, 4.42, 4.64, 4.87, 5.11, 5.36, 
       5.62, 5.90, 6.19, 6.49, 6.81, 7.15, 7.50, 7.87, 8.25, 8.66, 9.09, 9.53)

E96 = (1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30, 
       1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74, 
       1.78, 1.82, 1.87, 1.91, 1.96, 2.00, 2.05, 2.10, 2.16, 2.21, 2.26, 2.32, 
       2.37, 2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 
       3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12, 
       4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49, 
       5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32, 
       7.50, 7.68, 7.87, 8.06, 8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76)



def calc_vout(vin, r1, r2):
  return (r2 / (float(r1) + float(r2))) * vin

def calc_voltage_divider_resistance_values(vout, vin, value_set=E24):
  closest_vout = None
  closest_r1 = None
  closest_r2 = None
  for i, r1_value in enumerate(value_set):
    for j, r2_value in enumerate(value_set):
      new_vout = calc_vout(vin, r1_value, r2_value)
      if closest_vout is None or abs(new_vout - vout) < abs(closest_vout - vout):
        closest_vout = new_vout
        closest_r1 = r1_value
        closest_r2 = r2_value
  return closest_r1, closest_r2

def get_set(set):
  value_set = E12
  if(set == "E3"):
    value_set = E3
  elif(set == "E6"):
    value_set = E6
  elif(set == "E12"):
    value_set = E12
  elif(set == "E24"):
    value_set = E24
  elif(set == "E48"):
    value_set = E48
  elif(set == "E96"):
    value_set = E96
  return value_set



def vdiv(vl,vh,**kwargs):
  set=kwargs.get("set","E12")

  value_set = get_set(set) 

  a,b = calc_voltage_divider_resistance_values(vl, vh, value_set=value_set)

  vl_real = vh * ( b/(a+b))
  rel_error = vl_real/vl-1
  #print((a,b))
  print("R_up      : {:3.3f} R".format(a))
  print("R_down    : {:3.3f} R".format(b))
  print("V_low real: {:3.3f} V".format(vl_real))
  print("rel. error: {:3.3f} %".format(rel_error*100))
    

def rfrac(frac,**kwargs):
  set=kwargs.get("set","E12")
  value_set = get_set(set) 
  vl = 1
  vh = 1.+1./frac
  a,b = calc_voltage_divider_resistance_values(vl, vh, value_set=value_set)

  frac_real = b/a
  rel_error = frac_real/frac -1
  print("R_numerator   : {:3.3f} R".format(b))
  print("R_denominator : {:3.3f} R".format(a))
  print("frac real     : {:3.3f} V".format(frac_real))
  print("rel. error    : {:3.3f} %".format(rel_error*100))