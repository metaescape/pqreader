VARS = {
    "eaf-buffer-background-color": "#ffffff",
    "eaf-pdf-store-history": False,
    "eaf-pdf-marker-fontsize": 12,
    "eaf-marker-letters": "abcdefghijklmnopqrstuvwxyz",
    "eaf-pdf-dark-mode": False,
    "eaf-pdf-dark-exclude-image": True,
    "eaf-pdf-default-zoom": 1.0,
    "eaf-pdf-zoom-step": 0.2,
    "eaf-pdf-scroll-ratio": 0.05,
    "eaf-pdf-text-highlight-annot-color": "#fa8500",
    "eaf-pdf-text-underline-annot-color": "#11e32a",
    "eaf-pdf-inline-text-annot-color": "#ec3f00",
    "eaf-pdf-inline-text-annot-fontsize": 8,
    "eaf-pdf-show-progress-on-page": 20,
}


class PostGui:
    def __init__(self):
        pass

    def __call__(self, func):
        # do nothing
        return func


class SynctexInfo:  # data class
    page_num = None


def interactive(func):
    return func


def get_emacs_var(var):
    return VARS.get(var, None)


def get_emacs_vars(args):

    return [VARS.get(arg, None) for arg in args]


def message_to_emacs(*args):
    pass
    # print(*args)


def eval_in_emacs(*args):
    pass
    # print("eval_in_emacs", args)


def atomic_edit(*args):
    print("atomic_edit", args)


def get_emacs_config_dir():
    return "./"


def get_emacs_theme_mode():
    return "dark" if get_emacs_var("eaf-pdf-dark-mode") else "light"


def get_emacs_theme_foreground():
    theme_mode = get_emacs_theme_mode()
    if theme_mode == "dark":
        return "#bbc2cf"
    else:
        return "#242730"


def get_emacs_theme_background():
    theme_mode = get_emacs_theme_mode()
    if theme_mode == "dark":
        return "#000000"
    else:
        return "#ffffff"
