from fasthtml.common import *

# .plot_section { margin: 10px; padding: 20px; background-color: var(--pico-code-background-color); border-radius: 20px; }
# .section_grid {
#     display: grid;
#     grid-template-columns: 25% 75%;
#     grid-gap: 15px;
#     padding: 5px;
#     align-items: start;
#     background-color: green;
# }

# .color_picker {display: flex; justify_content: flex-start, flex-direction: row; margin: 10px; padding: 20px; border-radius: 20px;}

css = Style('''
    .parent_section { 
          display: flex;
          flex-direction: row;
          flex-wrap: wrap;
          gap: 20px;
          align-items: start;
          padding: 20px;
          justify-content: left;
          width: 100%;
    }
    html {data-theme="light"}
    :root { width: 100%; height: 2
    00%; margin: auto; margin-top: 5vh; padding: 0px; data-theme: light; max-width: 1500px; }
    .background-color-pico {background-color: var(--pico-secondary-background);}
    .background-color-pico-code {background-color: var(--pico-code-background-color)}
    .section { display: flex; justify-content: center; margin: 20px; padding: 0;}
    #color_selector { margin: 10px; padding: 20px; background-color: #F4F4F4; border-radius: 20px;}
    .group_slider {font-size: 80%; border-color: transparent; display: flex; justify-content: center; align-items: center; border-radius: 20px; }}}
    #chart { border-radius: 20px; padding: 20px; }
    .cst_button {color: var(--pico-h1-color); border-radius: 10px; background-color: var(--pico-muted-border-color); border-color: transparent; padding: 12px; font-weight: medium; font-size: 15px; width: 200px; height: 45px; font-weight: medium; align-items: center; justify-content: center; display: flex;} }
    .icon_button {  border-radius: 10px; background-color: #EEEEEE; margin: 15px; border-color: transparent; color: black; padding-left: 0px; font-weight: medium; font-size: 14px; width: 200px; padding: 12px; height: 45px; }
    .plot_configurator {
    display: flex; flex-direction:: column; border: none; outline: none; font-size: 14px; font-weight: medium; align-items: center; justify-content: right; flex-wrap: wrap;
    }
.section_label {font-weight: bold; }
''')

# parent_section = 'display: grid; grid-template-columns: 25% 75%; grid-gap: 0px; padding: 5px; align-items: start; background-color: green; width: 100%;'
# parent_section = '''
#   display: grid;
#   grid-template-columns: minmax(0, 25%) minmax(0, 75%);
#   gap: 20px;
#   padding: 5px;
#   align-items: start;
#   width: 100%;
#   box-sizing: border-box;
#   flex-wrap: wrap;
# '''

# parent_section = '''
#   display: grid;
#   grid-template-columns: 25% 75%;
#   flex-wrap: wrap;
#   gap: 20px;
#   padding: 5px;
#   align-items: start;
#   width: 100%;
#   box-sizing: border-box;
# '''

color_picker = 'margin-top: 20px;'

plot_grid = '''
    flex-grow: 1;
    border-radius: 20px; 
    max-width: 60%
    background-color: var(--pico-code-background-color); 
    padding: 40px;
    '''
color_picker_grid = '''
    border-radius: 20px; 
    background-color: var(--pico-code-background-color); 
    padding: 40px;
'''

grid_section_child = 'padding: 20px; background-color: blue;'

h2_style = "color: var(--pico-color)"
section_header = ''

remove_button_style = 'position: absolute; top: -3px; left: -3px; z-index: 5; border-color: transparent; display: flex; align-items: center; justify-content: center; width: 20px; height: 20px; display: flex; justify-content: center; align-items: center; font-size: 14px; margin: 0px; padding: 0px; border-radius: 15px;'
# cst_button_style = 'color: var(--pico-h1-color); border-radius: 10px; background-color: var(--pico-muted-border-color); margin: 15px; border-color: transparent; padding: 12px; font-weight: medium; font-size: 15px; width: 200px; height: 45px; font-weight: medium; align-items: center; justify-content: center; display: flex; '

cst_button_style = 'color: var(--pico-h1-color); border-radius: 10px; background-color: var(--pico-muted-border-color); border-color: transparent; font-weight: medium; font-size: 15px; height: 45px; font-weight: medium; align-items: center; justify-content: center; display: flex; '

config_header = 'font-weight: bold; font-size: 20px; margin-bottom: 10px; margin-top: 10px;'

slider_css = "width: 10px; margin-top: 10px; margin-bottom: 10px; border-radius: 10px; border: none; outline: none;"

#FUNCTION update_plot_type
# update_plot_type_conf_style = '''
#     width: 100%;
#     display: flex;
#     flex-wrap: wrap;
#     min-width: 400px;
#     flex-direction: row;
#     padding: 0px;
#     margin: 0px;
#     justify-content: space-between;
#     align-items: center;
#     background-color: blue;
# '''

# update_plot_type_default_style = '''
#     display: flex;
#     justify-content: center;
#     align-items: center;
#     border-radius: 10px;
#     background-color: white;
#     padding: 10px;
#     margin-top: 20px;
#     margin-left: 20px;'
# '''

#FUNCTION color_selector_raw

# style of the actual color picker
color_style = '''
    background-color: none; 
    border: none; 
    border-color: none; 
    border-radius: 50%; 
    height: 60px; 
    width: 50px; 
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    padding: 0px;
    margin: 0px;
    cursor: pointer;
'''

color_picker_container = '''
    position: relative; 
    margin: 6px;"
    padding: 0px;
'''

color_selector_raw_add_button_style = 'height: 35px; width: 35px; border-radius: 50%; border-color: transparent; display: flex; line-height: 1; padding: 0; cursor: pointer; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%)'
color_selector_raw_add_div_style = '''
    display: flex;  
    align-items: center; 
    justify-content: center; 
    height: 60px; 
    width: 50px; 
    position: relative; 
    padding-left: 8px; 
    padding-right: 5px; 
    margin-top: 3px;
'''
# color_selector_raw_grid_style = 'margin: 10px; display: flex; flex-wrap: wrap; justify-content: flex-start; width: 100%; padding-right: 5px; padding-left: 8px; background-color: green;'
color_selector_raw_grid_style = '''
    display: flex; 
    flex-wrap: wrap; 
    justify-content: flex-start; 
    width: 100%; 
    margin: 0px;'
'''

plot_config_btn_div_style = """
    padding-left: 10px;
"""

#FUNCTION get_plot_header
# get_plot_header_style = "display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;"
# get_plot_header_H2_style = "margin: 10px; display: inline; color: var(--pico-color);"

#FUNCTIONS plot_config_hist, plot_config_scatter, plot_conf_plot

# Add these to styling.py
# plot_section_container_style = '''
#     display: flex;
#     flex-direction: row;
#     justify-content: space-between;
#     align-items: flex-start;
#     width: 100%;
#     background-color: green;
#     flex-wrap: wrap;
#     gap: 20px;
# '''

# plot_section_style = '''
#     display: flex;
#     flex-direction: column;
#     justify-content: flex-start;
#     align-items: flex-start;
#     flex-wrap: wrap;
#     gap: 40px;
#     padding: 0px;
#     margin: 0px;
#     width: 100%;
#     box-sizing: border-box;
#     background-color: green;
# '''

# plot_section_style = '''
#     display: grid;
#     grid-template-columns: 40% 60%;
# '''

### CONFIGURATION FOR PLOT CONFIG

# configurator_style = """
#     min-width: 400px;
#     max-width: 60%;
#     flex-grow: 1;
#     flex-shrink: 1;
#     flex-basis: auto;
#     background-color: blue;
# """

# plot_section_style = '''
#     display: flex;
#     flex-direction: row;
#     flew-wrap: wrap;
#     justify-content: flex-start;
#     align-items: flex-start;
#     width: 100%;
#     background-color: green;
# '''

plot_section_style = '''
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 20px;
    width: 100%;
    box-sizing: border-box;
'''

plot_config_style = """
    display: flex;
    justify-content: left;
    width: 100%;
    align-items: left;
"""

plot_chart_style = '''
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: white;
    border-radius: 10px;
    padding: 10px;
    width: 100%;
    min-width: 400px;  /* Ensures plot doesn't get too small */
'''
# plot_chart_style = '''
#     display: flex;
#     justify-content: center;
#     align-items: center;
#     background-color: white;
#     border-radius: 10px;
#     padding: 10px;
#     width: 30%;
# '''

configurator_style = """
    width: 100%;
    box-sizing: border-box;
"""

# plot_chart_style = '''
#     display: flex;
#     justify-content: center;
#     align-items: center;
#     background-color: white;
#     border-radius: 10px;
#     padding: 10px;
#     width: 40%;
#     min-width: 400px;
# '''

###

# plot_config_style = '''
#     flex-
# '''

# plot_config_container_style = '''
#     display: flex;
#     flex-direction: column;
#     gap: 15px;
#     padding: 20px;
#     background-color: var(--pico-secondary-background);
#     border-radius: 10px;
# '''

plot_config_header_style = '''
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-bottom: 10px;
'''

plot_config_button_style = '''
    color: var(--pico-h1-color);
    border-radius: 8px;
    background-color: var(--pico-muted-border-color);
    border: none;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
'''

plot_config_section_style = '''
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
'''

plot_config_label_style = '''
    font-weight: 600;
    font-size: 14px;
    color: var(--pico-color);
    margin-bottom: 5px;
'''

# Add to styling.py
color_section_style = '''
    display: flex;
    flex-direction: column;
    gap: 15px;
    padding: 20px;
    border-radius: 10px;
'''

color_picker_container_style = '''
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 15px;
    border-radius: 10px;
'''

color_grid_style = '''
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
    gap: 10px;
    padding: 10px;
'''

plot_header_style = """
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: left;
    width: 30%;
    padding-top: 0px;
    margin-top: 0px;
"""
plot_selector_style = """
    width: 200px;
    padding: 8px;
    border-radius: 8px;
    border: 1px solid var(--pico-muted-border-color);
    background-color: var(--pico-background-color);
    font-size: 14px;
"""

color_preset_select = '''
    color: var(--pico-h1-color); 
    border-radius: 10px; 
    background-color: var(--pico-muted-border-color);
    border-color: transparent; 
    padding: 12px;
    font-size: 15px; 
    height: 45px;
    width: 200px;
'''