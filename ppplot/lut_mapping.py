from collections import OrderedDict

code2name = OrderedDict()
abbr2name = OrderedDict()
code2unit = OrderedDict()
abbr2unit = OrderedDict()

code2name[1]       = 'density'
abbr2name['rho']   = 'density'
code2unit[1]       = r'$kg \cdot m^{-3}$'
abbr2unit['rho']   = r'$kg \cdot m^{-3}$'

code2name[2]       = 'pressure'
abbr2name['press'] = 'pressure'
code2unit[2]       = r'$Pa$'
abbr2unit['press'] = r'$Pa$'

code2name[3]       = 'temperature'
abbr2name['temp']  = 'temperature'
code2unit[3]       = r'$K$'
abbr2unit['temp']  = r'$K$'

code2name[4]       = 'potential temperature'
abbr2name['theta'] = 'potential temperature'
code2unit[4]       = r'$K$'
abbr2unit['theta'] = r'$K$'

code2name[5]       = 'zonal velocity'
abbr2name['vlat']  = 'zonal velocity'
code2unit[5]       = r'$m \cdot s^{-1}$'
abbr2unit['vlat']  = r'$m \cdot s^{-1}$'

code2name[6]       = 'meridional velocity'
abbr2name['vlon']  = 'meridional velocity'
code2unit[6]       = r'$m \cdot s^{-1}$'
abbr2unit['vlon']  = r'$m \cdot s^{-1}$'

code2name[7]       = 'vertical velocity'
abbr2name['vel1']  = 'vertical velocity'
code2unit[7]       = r'$m \cdot s^{-1}$'
abbr2unit['vel1']  = r'$m \cdot s^{-1}$'

code2name[8]       = r'velocity $v$'
abbr2name['vel2']  = r'velocity $v$'
code2unit[8]       = r'$m \cdot s^{-1}$'
abbr2unit['vel2']  = r'$m \cdot s^{-1}$'

code2name[9]       = r'velocity $u$'
abbr2name['vel3']  = r'velocity $u$'
code2unit[9]       = r'$m \cdot s^{-1}$'
abbr2unit['vel3']  = r'$m \cdot s^{-1}$'
