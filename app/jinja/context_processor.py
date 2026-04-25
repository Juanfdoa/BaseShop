from flask import g

def inject_translations():
    def t_func(key):
        return getattr(g, "translations", {}).get(key, key)

    return dict(t=t_func)