__all__ = ['A', 'Form', 'AX', 'Hidden', 'CheckboxX', 'Script', 'Style', 'double_braces', 'undouble_braces', 'loose_format', 'ScriptX', 'replace_css_vars', 'StyleX', 'On', 'Any', 'Prev', 'Now', 'AnyNow', 'run_js', 'Titled', 'Socials', 'Favicon', 'jsd', 'clear']
from dataclasses import dataclass, asdict
from typing import Any
from fastcore.utils import *
from fastcore.xtras import partial_format
from fastcore.xml import *
from fastcore.meta import use_kwargs, delegates
from .components import *
try:
    from IPython import display
except ImportError:
    display = None

def A(*c, hx_get=None, target_id=None, hx_swap=None, href='#', hx_vals=None, id=None, cls=None, title=None, style=None, accesskey=None, contenteditable=None, dir=None, draggable=None, enterkeyhint=None, hidden=None, inert=None, inputmode=None, lang=None, popover=None, spellcheck=None, tabindex=None, translate=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs) -> FT:
    """An A tag; `href` defaults to '#' for more concise use with HTMX"""
    ...

def Form(*c, enctype='multipart/form-data', target_id=None, hx_vals=None, id=None, cls=None, title=None, style=None, accesskey=None, contenteditable=None, dir=None, draggable=None, enterkeyhint=None, hidden=None, inert=None, inputmode=None, lang=None, popover=None, spellcheck=None, tabindex=None, translate=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_swap=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs) -> FT:
    """A Form tag; identical to plain `ft_hx` version except default `enctype='multipart/form-data'`"""
    ...

def AX(txt, hx_get=None, target_id=None, hx_swap=None, href='#', *, hx_vals=None, id=None, cls=None, title=None, style=None, accesskey=None, contenteditable=None, dir=None, draggable=None, enterkeyhint=None, hidden=None, inert=None, inputmode=None, lang=None, popover=None, spellcheck=None, tabindex=None, translate=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs) -> FT:
    """An A tag with just one text child, allowing hx_get, target_id, and hx_swap to be positional params"""
    ...

def Hidden(value: Any='', id: Any=None, *, target_id=None, hx_vals=None, cls=None, title=None, style=None, accesskey=None, contenteditable=None, dir=None, draggable=None, enterkeyhint=None, hidden=None, inert=None, inputmode=None, lang=None, popover=None, spellcheck=None, tabindex=None, translate=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_swap=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs) -> FT:
    """An Input of type 'hidden'"""
    ...

def CheckboxX(checked: bool=False, label=None, value='1', id=None, name=None, *, target_id=None, hx_vals=None, cls=None, title=None, style=None, accesskey=None, contenteditable=None, dir=None, draggable=None, enterkeyhint=None, hidden=None, inert=None, inputmode=None, lang=None, popover=None, spellcheck=None, tabindex=None, translate=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_swap=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs) -> FT:
    """A Checkbox optionally inside a Label, preceded by a `Hidden` with matching name"""
    ...

def Script(code: str='', *, id=None, cls=None, title=None, style=None, attrmap=None, valmap=None, **kwargs) -> FT:
    """A Script tag that doesn't escape its code"""
    ...

def Style(*c, id=None, cls=None, title=None, style=None, attrmap=None, valmap=None, **kwargs) -> FT:
    """A Style tag that doesn't escape its code"""
    ...

def double_braces(s):
    """Convert single braces to double braces if next to special chars or newline"""
    ...

def undouble_braces(s):
    """Convert double braces to single braces if next to special chars or newline"""
    ...

def loose_format(s, **kw):
    """String format `s` using `kw`, without being strict about braces outside of template params"""
    ...

def ScriptX(fname, src=None, nomodule=None, type=None, _async=None, defer=None, charset=None, crossorigin=None, integrity=None, **kw):
    """A `script` element with contents read from `fname`"""
    ...

def replace_css_vars(css, pre='tpl', **kwargs):
    """Replace `var(--)` CSS variables with `kwargs` if name prefix matches `pre`"""
    ...

def StyleX(fname, **kw):
    """A `style` element with contents read from `fname` and variables replaced from `kw`"""
    ...

def On(code: str, event: str='click', sel: str='', me=True):
    """An async surreal.js script block event handler for `event` on selector `sel`"""
    ...

def Any(sel: str, code: str, event: str='click'):
    """An `any` async surreal.js script block event handler for `event` on selector `sel`"""
    ...

def Prev(code: str, event: str='click'):
    """An async surreal.js script block event handler for `event` on previous sibling"""
    ...

def Now(code: str, sel: str=''):
    """An async surreal.js script block on selector `me(sel)`"""
    ...

def AnyNow(sel: str, code: str):
    """An async surreal.js script block on selector `any(sel)`"""
    ...

def run_js(js, id=None, **kw):
    """Run `js` script, auto-generating `id` based on name of caller if needed, and js-escaping any `kw` params"""
    ...

def Titled(title: str='FastHTML app', *args, cls='container', target_id=None, hx_vals=None, id=None, style=None, accesskey=None, contenteditable=None, dir=None, draggable=None, enterkeyhint=None, hidden=None, inert=None, inputmode=None, lang=None, popover=None, spellcheck=None, tabindex=None, translate=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_swap=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs) -> FT:
    """An HTML partial containing a `Title`, and `H1`, and any provided children"""
    ...

def Socials(title, site_name, description, image, url=None, w=1200, h=630, twitter_site=None, creator=None, card='summary'):
    """OG and Twitter social card headers"""
    ...

def Favicon(light_icon, dark_icon):
    """Light and dark favicon headers"""
    ...

def jsd(org, repo, root, path, prov='gh', typ='script', ver=None, esm=False, **kwargs) -> FT:
    """jsdelivr `Script` or CSS `Link` tag, or URL"""
    ...

def clear(id):
    ...