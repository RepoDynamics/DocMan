from typing import Literal as _Literal

import pycolorit as _pcit
import pyserials as _ps
import pybadger as _badger
from markitup.html import elem as _html

from docsman import data as _data


def image(
    src: str,
    src_dark: str | None = None,
    width: str | None = None,
    height: str | None = None,
    align: str | None = None,
    href: str | None = None,
    title: str | None = None,
    alt: str | None = None,
    attrs_img: _badger.param_type.AttrDict = None,
    attrs_a: _badger.param_type.AttrDict = None,
    attrs_picture: _badger.param_type.AttrDict = None,
    attrs_source_light: _badger.param_type.AttrDict = None,
    attrs_source_dark: _badger.param_type.AttrDict = None,
    default_light: bool = True,
    themed: bool = True,
) -> _html.Element:
    attrs_img = (attrs_img or {}) | {
        "width": width,
        "height": height,
        "align": align,
        "alt": alt,
        "title": title,
    }
    if themed and src_dark:
        element = _html.picture_color_scheme(
            src_light=src,
            src_dark=src_dark,
            attrs_img=attrs_img,
            attrs_picture=attrs_picture,
            attrs_source_light=attrs_source_light,
            attrs_source_dark=attrs_source_dark,
            default_light=default_light,
        )
    else:
        element = _html.img(src=src, **attrs_img)
    if href:
        element = _html.a(element, href=href, **(attrs_a or {}))
    return element


def menu(
    items: list[dict],
    align: str | None = None,
    attrs_ul: _badger.param_type.AttrDict = None,
    attrs_li: _badger.param_type.AttrDict = None,
    attrs_a: _badger.param_type.AttrDict = None,
    attrs_div: _badger.param_type.AttrDict = None,
) -> str:

    return str(menu)


def static_badges(
    content: list[dict | str],
    default: dict | None = None,
    space: int | str = 1,
    return_list: bool = False,
    themed: bool = True,
):
    default = default or {}
    default["service"] = "static"
    for badge_content in content:
        if isinstance(badge_content, dict):
            badge_content["args"] = {"message": badge_content.pop("message")}
    return badges(content=content, default=default, space=space, return_list=return_list, themed=themed)


def badges(
    content: list[dict | str],
    default: dict | None = None,
    space: int | str = 1,
    return_list: bool = False,
    themed: bool = True,
) -> str:
    """Create a series of badges.

    Parameters
    ----------
    content : list[dict | str]
        Badges to create.
    default : dict, optional
        Default values for the badges.

    Returns
    -------
    badges: List of `Badge`
    """
    default = default or {}
    gradient = {}
    for theme in ("light", "dark"):
        # Create gradient colors if given
        theme_params = default.get(f"params_{theme}")
        if not theme_params:
            continue
        for color in ("color", "label_color", "logo_color"):
            if color not in theme_params or not isinstance(theme_params[color], dict):
                continue
            grad_def = theme_params.pop(color)
            grad_gen = getattr(_pcit.gradient, grad_def.pop("gradient", "interpolate"))
            grad_def["count"] = len(content)
            gradient.setdefault(theme, {})[color] = grad_gen(**grad_def)
    badge_list = []
    for idx, badge_settings in enumerate(content):
        if isinstance(badge_settings, str):
            badge_settings = {
                "platform": "shields",
                "service": "static",
                "args": {
                    "message": badge_settings
                },
            }
        _ps.update.dict_from_addon(
            data=badge_settings,
            addon=default,
            append_list=True,
            append_dict=True,
            raise_duplicates=False
        )
        for theme in ("light", "dark"):
            # Set gradient colors if available
            theme_gradient = gradient.get(theme)
            if not theme_gradient:
                continue
            for color in ("color", "label_color", "logo_color"):
                gradient_colors = theme_gradient.get(color)
                if not gradient_colors or color in badge_settings.get(f"params_{theme}", {}):
                    continue
                # Only set gradient colors if badge doesn't define a corresponding color
                badge_settings.setdefault(f"params_{theme}", {})[color] = gradient_colors[idx].css_hex()
        badge_list.append(badge(themed=themed, **badge_settings))
    if return_list:
        return badge_list
    spacer = "&nbsp;" * space if isinstance(space, int) else space
    return spacer.join(str(bdg) for bdg in badge_list)


def badge(
    platform: _Literal["shields", "pepy"] = "shields",
    service: str = "generic",
    endpoint: str | None = None,
    args: dict | None = None,
    width: str | None = None,
    height: str | None = None,
    align: str | None = None,
    href: str | None = None,
    title: str | None = None,
    alt: str | None = None,
    params_light: _badger.param_type.AttrDict = None,
    params_dark: _badger.param_type.AttrDict = None,
    attrs_img: _badger.param_type.AttrDict = None,
    attrs_a: _badger.param_type.AttrDict = None,
    attrs_picture: _badger.param_type.AttrDict = None,
    attrs_source_light: _badger.param_type.AttrDict = None,
    attrs_source_dark: _badger.param_type.AttrDict = None,
    default_light: bool = True,
    merge_params: bool = True,
    use_defaults: bool = True,
    themed: bool = True,
) -> str:
    if href:
        attrs_a = (attrs_a or {}) | {"href": href}
    attrs_img = (attrs_img or {}) | {
        "width": width,
        "height": height,
        "align": align,
        "alt": alt,
        "title": title,
    }
    badge = _badger.create(
        platform=platform,
        service=service,
        endpoint=endpoint,
        args=args,
        params_light=params_light,
        params_dark=params_dark if themed else None,
        attrs_img=attrs_img,
        attrs_a=attrs_a,
        attrs_picture=attrs_picture,
        attrs_source_light=attrs_source_light,
        attrs_source_dark=attrs_source_dark,
        default_light=default_light,
        merge_params=merge_params,
        use_defaults=use_defaults
    )
    return str(badge)


def highlights(
    content: list[dict],
    badge_default: dict,
    align: str | None = None,
    styles: list[dict] | None = None,
    attrs_p: _badger.param_type.AttrDict = None,
    space: int | str = "",
    themed: bool = True,
):
    title_badges = static_badges(
        content=[highlight["title"] for highlight in content],
        default=badge_default,
        return_list=True,
        themed=themed,
    )
    contents = []
    spacer = "&nbsp;" * space if isinstance(space, int) else space
    for highlight, title_badge in zip(content, title_badges):
        contents.append(title_badge)
        if spacer:
            contents.append(spacer)
        text = paragraph(
            text=highlight["description"],
            attrs_p=attrs_p,
            styles=styles,
            align=align,
        )
        contents.append(text)
    return "\n".join([str(content) for content in contents])


def line(
    width: str | None = None,
    attrs_hr: _badger.param_type.AttrDict = None,
    themed: bool = True,
) -> _html.Element:
    return _html.hr(width=width, **(attrs_hr or {}))


def paragraph(
    text: str,
    styles: list[dict] | None = None,
    align: str | None = None,
    attrs_p: _badger.param_type.AttrDict = None,
    themed: bool = True,
) -> _html.Element:
    return _html.paragraph(text, styles=styles, align=align, attrs_p=attrs_p)


def covenant(contact_name: str, contact_url: str, themed: bool) -> str:
    raw_text = _data.code_of_conduct("contributor_covenant")
    return raw_text.format(contact=f"[{contact_name}]({contact_url})")


def heading(content, level, themed: bool) -> str:
    # if isinstance(content, dict):
    #     content = self.generate([content])
    return _html.h(level=level, content=content)


def _elem_spacer(spacer: dict):
    s = html.IMG(
        src="docs/source/_static/img/spacer.svg",
        **{k: v for k, v in spacer.items() if k not in ("id",)},
    )
    return str(s)


def _elem_newline(newline: dict):
    return "\n" * newline["count"]


# def continuous_integration(self, data):
#     def github(filename, **kwargs):
#         badge = self._github_badges.workflow_status(filename=filename, **kwargs)
#         return badge
#
#     def readthedocs(rtd_name, rtd_version=None, **kwargs):
#         badge = bdg.shields.build_read_the_docs(project=rtd_name, version=rtd_version, **kwargs)
#         return badge
#
#     def codecov(**kwargs):
#         badge = bdg.shields.coverage_codecov(
#             user=self.github["user"],
#             repo=self.github["repo"],
#             branch=self.github["branch"],
#             **kwargs,
#         )
#         return badge
#
#     func_map = {"github": github, "readthedocs": readthedocs, "codecov": codecov}
#
#     badges = []
#     for test in copy.deepcopy(data["args"]["tests"]):
#         func = test.pop("type")
#         if "style" in test:
#             style = test.pop("style")
#             test = style | test
#         badges.append(func_map[func](**test))
#
#     div = html.DIV(
#         align=data.get("align") or "center",
#         content=[
#             self._marker(start="Continuous Integration"),
#             self.heading(data=data["heading"]),
#             *badges,
#             self._marker(end="Continuous Integration"),
#         ],
#     )
#     return div
#
#
# def activity(self, data):
#     pr_button = bdg.shields.static(text="Pull Requests", style="for-the-badge", color="444")
#
#     prs = []
#     issues = []
#     for label in (None, "bug", "enhancement", "documentation"):
#         prs.append(self._github_badges.pr_issue(label=label, raw=True, logo=None))
#         issues.append(self._github_badges.pr_issue(label=label, raw=True, pr=False, logo=None))
#
#     prs_div = html.DIV(align="right", content=html.ElementCollection(prs, "\n<br>\n"))
#     iss_div = html.DIV(align="right", content=html.ElementCollection(issues, "\n<br>\n"))
#
#     table = html.TABLE(
#         content=[
#             html.TR(
#                 content=[
#                     html.TD(
#                         content=html.ElementCollection([pr_button, *prs], seperator="<br>"),
#                         align="center",
#                         valign="top",
#                     ),
#                     html.TD(
#                         content=html.ElementCollection(
#                             [
#                                 bdg.shields.static(
#                                     text="Milestones",
#                                     style="for-the-badge",
#                                     color="444",
#                                 ),
#                                 self._github_badges.milestones(
#                                     state="both",
#                                     style="flat-square",
#                                     logo=None,
#                                     text="Total",
#                                 ),
#                                 "<br>",
#                                 bdg.shields.static(
#                                     text="Commits",
#                                     style="for-the-badge",
#                                     color="444",
#                                 ),
#                                 self._github_badges.last_commit(logo=None),
#                                 self._github_badges.commits_since(logo=None),
#                                 self._github_badges.commit_activity(),
#                             ],
#                             seperator="<br>",
#                         ),
#                         align="center",
#                         valign="top",
#                     ),
#                     html.TD(
#                         content=html.ElementCollection(
#                             [
#                                 bdg.shields.static(
#                                     text="Issues",
#                                     style="for-the-badge",
#                                     logo="github",
#                                     color="444",
#                                 ),
#                                 *issues,
#                             ],
#                             seperator="<br>",
#                         ),
#                         align="center",
#                         valign="top",
#                     ),
#                 ]
#             )
#         ]
#     )
#
#     div = html.DIV(
#         align=data.get("align") or "center",
#         content=[
#             self._marker(start="Activity"),
#             self.heading(data=data["heading"]),
#             table,
#             self._marker(end="Activity"),
#         ],
#     )
#     return div
#
#
# def pr_issue_badge(
#     self,
#     pr: bool = True,
#     status: Literal["open", "closed", "both"] = "both",
#     label: str | None = None,
#     raw: bool = False,
#     **kwargs,
# ) -> bdg.Badge:
#     """Number of pull requests or issues on GitHub.
#
#     Parameters
#     ----------
#     pr : bool, default: True
#         Whether to query pull requests (True, default) or issues (False).
#     closed : bool, default: False
#         Whether to query closed (True) or open (False, default) issues/pull requests.
#     label : str, optional
#         A specific GitHub label to query.
#     raw : bool, default: False
#         Display 'open'/'close' after the number (False) or only display the number (True).
#     """
#
#     def get_path_link(closed):
#         path = self._url / (
#             f"issues{'-pr' if pr else ''}{'-closed' if closed else ''}"
#             f"{'-raw' if raw else ''}/{self._address}{f'/{label}' if label else ''}"
#         )
#         link = self._repo_link.pr_issues(pr=pr, closed=closed, label=label)
#         return path, link
#
#     def half_badge(closed: bool):
#         path, link = get_path_link(closed=closed)
#         if "link" not in args:
#             args["link"] = link
#         badge = ShieldsBadge(path=path, **args)
#         badge.html_syntax = ""
#         if closed:
#             badge.color = {"right": "00802b"}
#             badge.text = ""
#             badge.logo = None
#         else:
#             badge.color = {"right": "AF1F10"}
#         return badge
#
#     desc = {
#         None: {True: "pull requests in total", False: "issues in total"},
#         "bug": {True: "pull requests related to a bug-fix", False: "bug-related issues"},
#         "enhancement": {
#             True: "pull requests related to new features and enhancements",
#             False: "feature and enhancement requests",
#         },
#         "documentation": {
#             True: "pull requests related to the documentation",
#             False: "issues related to the documentation",
#         },
#     }
#     text = {
#         None: {True: "Total", False: "Total"},
#         "bug": {True: "Bug Fix", False: "Bug Report"},
#         "enhancement": {True: "Enhancement", False: "Feature Request"},
#         "documentation": {True: "Docs", False: "Docs"},
#     }
#
#     args = self.args | kwargs
#     if "text" not in args:
#         args["text"] = text[label][pr]
#     if "title" not in args:
#         args["title"] = (
#             f"Number of {status if status != 'both' else 'open (red) and closed (green)'} "
#             f"{desc[label][pr]}. "
#             f"Click {'on the red and green tags' if status == 'both' else ''} to see the details of "
#             f"the respective {'pull requests' if pr else 'issues'} in the "
#             f"'{'Pull requests' if pr else 'Issues'}' section of the repository."
#         )
#     if "style" not in args and status == "both":
#         args["style"] = "flat-square"
#     if status not in ("open", "closed", "both"):
#         raise ValueError()
#     if status != "both":
#         path, link = get_path_link(closed=status == "closed")
#         if "link" not in args:
#             args["link"] = link
#         return ShieldsBadge(path=path, **args)
#     return html.element.ElementCollection(
#         [half_badge(closed) for closed in (False, True)], seperator=""
#     )
#
#
