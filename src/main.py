from fasthtml.common import *
import numpy as np
import matplotlib.colors as mcolors

# import numpy as np
# import matplotlib.pylab as plt
# import seaborn as sns
# from fh_matplotlib import matplotlib2fasthtml


css = Style('''
    html {data-theme="light"}
    :root { width: 100%; height: 100%; margin: auto; margin-top: 5vh; padding: 0px; data-theme: light; max-width: 1500px;}
    .section_grid {display: grid; grid-template-columns:30% 70%; grid-gap: 0px;}
    .section { display: flex; justify-content: center; margin: 20px; padding: 0;}
    .color_section {display: flex; justify-content: flex-start; flex-direction: row; margin: 10px; padding: 20px; background-color: #F4F4F4; border-radius: 20px; }
    .plot_section { margin: 10px; padding: 20px; background-color: #F4F4F4; border-radius: 20px; }
    #color-picker-grid { width: 30vw ; margin: 10px; gap: 10px; }
    .colors { background-color: #FFF; border: none; border-radius: 15px;}
    #color_selector { margin: 10px; padding: 20px; background-color: #F4F4F4; border-radius: 20px;}
    .remove_color_btn {width: 20px; height: 20px; display: flex; justify-content: center; align-items: center; font-size: 14px; margin: 0px; padding: 0px; border-radius: 50%;}
    .group_slider {border-color: transparent; display: flex; justify-content: center; align-items: center; margin: 10px; padding-left: 20px; border-radius: 20px; }}}
    #chart { border-radius: 20px; padding: 20px; }
    .cst_button { border-radius: 10px; background-color: #EEEEEE; margin: 15px; border-color: transparent; color: black; padding: 12px; font-weight: medium; font-size: 14px; width: 200px; height: 45px; }
    .icon_button {  border-radius: 10px; background-color: #EEEEEE; margin: 15px; border-color: transparent; color: black; padding-left: 0px; font-weight: medium; font-size: 14px; width: 200px; padding: 12px; height: 45px; }
    .plot_selector { width: 200px; border: none; outline: none; font-size: 14px; font-weight: medium; background-color: #EEEEEE; margin: 15px; border}
    .plot_configurator {
    display: flex; flex-direction:: column; border: none; outline: none; font-size: 14px; font-weight: medium; align-items: center; justify-content: right; flex-wrap: wrap;
    }
''')

slider_css = "width: 10px; margin: 15px; border-radius: 10px; border: none; outline: none;"

app, rt = fast_app(
    pico=False,
    hdrs=(
        # Link(rel='stylesheet', href='css/pico.min.css', type='text/css'),
        Link(rel='stylesheet',
             href='https://unpkg.com/normalize.css',
             type='text/css'),
        picolink,  ## uncomment to get dark mode
        MarkdownJS(),
        HighlightJS(),
        css))


@rt("/")
def home():
    return (
        Socials(
            title="Vercel + FastHTML",
            site_name="Vercel",
            description="A demo of Vercel and FastHTML integration",
            image="https://vercel.fyi/fasthtml-og",
            url="https://fasthtml-template.vercel.app",
            twitter_site="@vercel",
        ),
        Container(
            Card(
                Group(
                    P(
                        "FastHTML is a new next-generation web framework for fast, scalable web applications with minimal, compact code. It builds on top of popular foundations like ASGI and HTMX. You can now deploy FastHTML with Vercel CLI or by pushing new changes to your git repository.",
                    ),
                ),
                header=(Titled("FastHTML + Vercel")),
                footer=(
                    P(
                        A(
                            "Deploy your own",
                            href="https://vercel.com/templates/python/fasthtml-python-boilerplate",
                        ),
                        " or ",
                        A("learn more", href="https://docs.fastht.ml/"),
                        "about FastHTML.",
                    )
                ),
            ),
        ),
    )
    
    
serve()