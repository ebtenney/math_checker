from pylatexenc.latexwalker import (
    LatexWalker, LatexMacroNode, LatexCharsNode, LatexGroupNode, LatexEnvironmentNode
)
def latex_nodes_to_string(nodelist):
    return "".join(node.latex_verbatim() for node in nodelist)
def SeperateLatex(text):
    lw = LatexWalker(text)
    nodes, _, _ = lw.get_latex_nodes()
    commands = []
    content = []
    arguments = []
    split_content = text.split('&')
    for part in split_content:
        sub_lw = LatexWalker(part)
        sub_nodes, _, _ = sub_lw.get_latex_nodes()
        
        for node in sub_nodes:
            if isinstance(node, LatexMacroNode):
                macro_args = []
                for arg in node.nodeargd.argnlist:
                    if isinstance(arg, LatexGroupNode):
                        macro_args.append(latex_nodes_to_string(arg.nodelist))
                    elif isinstance(arg, LatexCharsNode):
                        macro_args.append(arg.chars)
                    else:
                        macro_args.append("")
                command = f"\\{node.macroname}{{{'{}' * len(macro_args)}}}"
                commands.append(command)
                arguments.extend(macro_args)

            elif isinstance(node, LatexCharsNode):
                chars = node.chars
                split_chars = [s.strip() for s in chars.replace('^', ' ^ ').replace('{', ' { ').replace('}', ' } ').split()]
                content.extend(split_chars)

    return commands, content, arguments
latex_text = r"\[ \begin{array}{ll} 17 & y=x^{3 / 2} y=8, x=0 \\ V=2 \pi \int_{0}^{8} y \cdot y^{2 / 3} d y & V=2 \pi \cdot \frac{3}{8} \cdot 256 \\ V=2 \pi \int_{0}^{8} y^{5 / 3} d y, & V=192 \pi \\ V=2 \pi\left[\frac{3}{8} y^{8 / 3}\right]_{0}^{8} & \end{array} \]"
commands, content, arguments = SeperateLatex(latex_text)
print("Commands:", commands)
