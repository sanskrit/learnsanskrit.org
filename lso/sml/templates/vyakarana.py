import lso.data as data_api
from lso.sml.parse import Text
from .base import *
from .common import quick_sa, Raw
from lso.sml.templates.sanskrit_text import Sa1, Sa2
from lso.sml.templates.utils import split_multiline_text


class AshtadhyayiRule(View):
    def enter(self):
        return '<ul class="examples vyakarana">'

    @staticmethod
    def ast_link(code: str, text: str) -> str:
        url_code = code.replace(".", "/")
        url = f"https://ashtadhyayi.com/sutraani/{url_code}"
        return f'<a href="{url}" target="_blank">{text}</a>'

    def children(self):
        assert len(self.node.children) == 1

        text = self.node.children[0].value

        children = []
        for rule in split_multiline_text(text):
            if not rule.strip():
                continue

            lines = rule.splitlines()
            assert len(lines) >= 3, lines

            # Format sa
            sa = lines[0]
            assert "|" in sa, sa
            text, bar, num = sa.partition("|")
            text = text.strip()
            num = num.strip()

            sandhi = lines[1]
            if sandhi == "_":
                sandhi, _, _ = sa.partition("|")
            translation = " ".join(lines[2:])
            li_nodes = [
                Sa1.to_node(text + "| " + num),
                Node("br"),
                Sa2.to_node(f"{text}"),
                Text(" ("),
                Raw.to_node(self.ast_link(num, num)),
                Text(")"),
                Node("br"),
                Sa2.to_node(sandhi),
                Node("br"),
            ]
            li_nodes.extend(quick_sa(translation))

            children.append(Node("li", li_nodes))
        return children

    def exit(self):
        return "</ul>"


class AshtadhyayiRuleCitation(View):
    def enter(self):
        return ""

    def children(self):
        nodes = self.node.children
        assert len(nodes) == 1
        code = nodes[0].value
        sa = data_api.ashtadhyayi_rules()[code]
        return [Text(code), Text(" ("), Sa2.to_node(sa), Text(")")]

    def exit(self):
        return ""


class Prakriya(View):
    def enter(self):
        return '<ol class="prakriya">'

    def children(self):
        nodes = self.node.children
        assert len(nodes) == 1
        text = nodes[0].value

        ret = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            result, _, code_str = line.partition("|")
            result = result.strip()
            code_str = code_str.strip()
            ret.extend(
                [
                    Raw.to_node('<li><span class="result">'),
                    Sa2.to_node(result),
                    Raw.to_node('</span><span class="rule">'),
                ]
            )
            if code_str:
                codes = [x.strip() for x in code_str.split(";")]
                for i, code in enumerate(codes):
                    if i != 0:
                        ret.append(Raw.to_node("<br>"))
                    sa = data_api.ashtadhyayi_rules()[code]
                    ret.extend(
                        [
                            Raw.to_node(AshtadhyayiRule.ast_link(code, code)),
                            Text(" "),
                            Sa2.to_node(sa),
                        ]
                    )
            ret.append(Raw.to_node("</span></li>"))

        return ret

    def exit(self):
        return "</ol>"


class Dhatupatha(View):
    def enter(self):
        return '<ul class="examples">'

    @staticmethod
    def dhp_link(code: str, text: str) -> str:
        url_code = code
        url = f"https://ashtadhyayi.com/dhatu/{url_code}"
        return f'<a href="{url}" target="_blank">{text}</a>'

    def children(self):
        assert len(self.node.children) == 1

        text = self.node.children[0].value

        children = []
        for rule in split_multiline_text(text):
            if not rule.strip():
                continue

            lines = rule.splitlines()
            assert len(lines) >= 2, lines

            # Format sa
            sa = lines[0]
            assert "|" in sa, sa
            text, bar, num = sa.partition("|")
            text = text.strip()
            num = num.strip()

            translation = " ".join(lines[1:])
            li_nodes = [
                Sa1.to_node(text + "| " + num),
                Node("br"),
                Sa2.to_node(f"{text}"),
                Text(" ("),
                Raw.to_node(self.dhp_link(num, num)),
                Text(")"),
                Node("br"),
            ]
            li_nodes.extend(quick_sa(translation))

            children.append(Node("li", li_nodes))
        return children

    def exit(self):
        return "</ul>"
