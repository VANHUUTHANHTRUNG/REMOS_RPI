# Constant for strain cal
GF = 2.12
mapped_init_voltage = 0.0 # Get from the tunnel
RL = 0.3
RG = 120

Vin = 4.88

def strain_therm(input_R):
    T = -0.002660 * pow(input_R,2) + 2.251 * input_R - 197.7
    return (-16.2 + 1.91*T - 0.0608*pow(T,2) + 0.000246 * pow(T,3))

def strain_total(mapped_read_voltage):
    Vr = (mapped_read_voltage - mapped_init_voltage)/Vin
    return ((-4*Vr/(GF*(1+2*Vr)))*(1+RL/RG))
