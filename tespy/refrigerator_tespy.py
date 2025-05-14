# 1. Import the necessary packages
from tespy.networks import Network
from tespy.components import (Sink, Source, Valve, SimpleHeatExchanger, Compressor, CycleCloser)
from tespy.connections import Connection, Bus
from CoolProp.CoolProp import PropsSI

# 2. Create the Network for the refrigerator and set the units you want to use
refrigerator = Network(T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s')

# 3. Set the fluids of the system (for easier access in the functions)
wf = "R600a"
wf_dict = {wf: 1}

# 4. Set the components of the system
val = Valve('throttling-valve')
eva = SimpleHeatExchanger('evaporator')
cond = SimpleHeatExchanger('condenser')
comp = Compressor('compressor')
cc = CycleCloser('cycle-closer')

# 5. Set the connections of the system and add them to the Network
c01 = Connection(eva, 'out1', comp, 'in1', label='1')
c02 = Connection(comp, 'out1', cond, 'in1', label='2')
c02cc = Connection(cond, 'out1', cc, 'in1', label='2cc')
c03 = Connection(cc, 'out1', val, 'in1', label='3')
c04 = Connection(val, 'out1', eva, 'in1', label='4')
refrigerator.add_conns(c01, c02, c02cc, c03, c04)


# 6. Define the parameters and design variables
# Components
eva.set_attr(Q=150, pr=1)
comp.set_attr(eta_s=0.75)
cond.set_attr(pr=1)
# Connections
c03.set_attr(fluid=wf_dict)
p4_set = PropsSI("P", "Q", 1, "T", 273.15 - 20, wf) / 1e5  # saturation pressure at given temperature
c04.set_attr(p=p4_set)
h1_set = PropsSI("H", "P", p4_set*1e5, "T", 273.15 - 18, wf) / 1e3  # superheated state at given temperature and pressure
c01.set_attr(h=h1_set)
c02.set_attr(T=60)
h2cc_set = PropsSI("H", "Q", 0, "T", 273.15 + 40, wf) / 1e3  # 
c02cc.set_attr(h=h2cc_set)

# 7. Add busses for heat and power flows
motor = Bus('motor')
motor.add_comps({'comp': comp, 'char': 0.95, 'base': 'bus'})
cooling = Bus('cooling heat')
cooling.add_comps({'comp': eva, 'base': 'bus'})
refrigerator.add_busses(motor, cooling)

# 8. Run the simulation and calculate the coefficient of performance
refrigerator.solve(mode='design')
refrigerator.print_results()
print('COP:', cooling.P.val / motor.P.val)