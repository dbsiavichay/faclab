from django import template

register = template.Library()


def get_breadcrumb(menus):
    def get_path_selected(item, parents):
        if item.selected:
            return parents + [item]
        else:
            for child in item.children:
                path_selected = get_path_selected(child, parents + [item])
                if path_selected:
                    return path_selected

    for menu in menus:
        path_selected = get_path_selected(menu, [])
        if path_selected:
            return path_selected


@register.simple_tag(takes_context=True)
def build_breadcrumbs(context, selected_menu):
    breadcrumbs = get_breadcrumb(selected_menu.children)
    context["breadcrumbs"] = breadcrumbs
