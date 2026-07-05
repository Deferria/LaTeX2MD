# LaTeX 转为 MD 的妙妙小工具

本工具旨在解决我们以 LaTeX 书写的笔记的种种限制性, 例如实时性差, 必须需要 LaTeX 渲染器, 不能完美配合 HTML 等等问题, 而其最好的替代方案就是转为支持 KaTeX 的 Markdown, 这样我们就可以在任何支持 Markdown 的地方使用 LaTeX 了, 例如 GitHub, Notion, Obsidian 以及几乎所有的 HTML 等等.

## 工作流

LaTeX 笔记是按条目组织的. 其文章内容存放在 `sections.tex` 文件中, 有 section 与 subsection 等多级结构, 每章节之中还有以下几种环境, 使用 `\begin{...}` 与 `\end{...}` 来标记:

- 定义类环境: `dfn` (definition) 和 `vardfn` (variant definition) ;
- 定理类环境: `thm` (theorem), `varthm` (variant theorem), `ppt` (property), `crl` (corollary), `lma` (lemma) 和 `pps` (proposition) ;
- 实例类环境: `xmp` (example), `cxmp` (counterexample) 和 `ins` (instance) ;
- 证明类环境: `prf` (proof) ;
- 注释类环境: `rmk` (remark) 和 `intrormk` (introduction remark) ;

并且现行的 schema 是不统一的. 例如: 每个 `dfn` 环境接受 7 个参数, 除去需要绑到计数器上的最后一个参数, 实际传入的只需要 6 个参数, 其 xargs 标签为 somsoo. 其中两个 boolean 参数仅涉及显示样式, 所以可以忽略. 一个典型的环境看起来应该是这样子:

```tex
\begin{dfn}
    [closed-linear-operator]
    {闭线性算子}
    [Closed Linear Operator]
    [contribution-meta]
    设 \(X,Y\) 是两个 Banach 空间, \(T:X\to Y\) 是一个线性映射. 定义 \(T\) 是一个\textbf{闭线性算子}, 当且仅当 \(T\) 的图像 \(\Gamma(T)=\{(x,T(x)):x\in X\}\) 是积拓扑空间 \(X\times Y\) 中的一个闭集. 这个闭集称为\textbf{闭图像(Closed Graph)}.
\end{dfn}
```

当然更有可能是可选参数缺少的情况. 并且其可能在任意位置缺少任意数量.

所以拿到一个这样的 `sections.tex` 文件, 我们的工作流计划是这样的:

### `extract.py` 将 TeX 写入 JSON

使用正则表达式, 识别各个环境, 并将其参数信息写入一个 `extracted.json` 文件中. 其具有以下键值对:

- `env`: 环境类型, 例如 `dfn`, `thm`, `xmp` 等等;
- `uuid`: 该条目的唯一标识符, 例如 `closed-linear-operator`;
- `name`: 该条目的名称, 例如 `闭线性算子`;
- `alias`: 该条目的别名, 在此处即为其英文名, 例如 `Closed Linear Operator`;
- `content`: 该条目的内容, 其为原始的 LaTeX Code. 

针对缺少可选参数的环境, 按照多种正则表达式样式进行匹配. 缺失的可选参数统一补全为 `null`. 

### `format.py` 处理 JSON 文件

这一步的目的是转义 Markdown 特殊字符, 有三个, 分别是 `′` , `~` 和 `|`.

### `macroescape.py` 处理特殊 LaTeX 语法和宏定义

这一步的目的是考虑到 KaTeX 并非完整复刻了所有 LaTeX 的语法, 原先使用的一些常用宏包, 例如 `physics` 宏包, 其提供的 `\norm` 命令在 KaTeX 中是无法识别的. 所以我们需要将其转为 KaTeX 可识别的语法, 例如 `\norm{x}` 转为 `\left\lVert x \right\rVert`. 还有一个问题是用户自己定义的命令, 最常见的就是 `\newcommand{\N}{\mathbb{N}}` 这种, 这类命令在 KaTeX 中同样无法识别, 所以我们需要将其转为 `\mathbb{N}`. 当然, 这类命令甚至可以是接受参数的, 例如 `\newcommand{\set}[1]{\{#1\}}`. 也需要替换. 甚至于 LaTeX 原生的 `\textbf{}` 这样的命令, 也需要在 Markdown 中进行替换, 更有甚者, LaTeX 的链接系统 `\hyperref` 也需要进行相应的处理. 这一步在做的就是这样的事情. 

替换同样使用正则表达式.

### `display.py` 将 JSON 写入 MD

从处理好的 JSON 文件中读取数据, 并将其写入 `output.md` 文件中. 其会根据环境类型, 选择不同的 Markdown 模板进行渲染, 并且引入了标签系统, 为每个 `uuid` 不为空的条目生成一个锚点, 方便在 Markdown 中进行链接和跳转. 


## 问题与局限性

目前潜在的问题及相应的改进方向为:

1. 不能识别附有 boolean 参数的环境;
2. 目前没有将 contribution meta 相关的内容写入 JSON 文件;
3. **由于不同的渲染器有不同的显示标准, 尽量不要在公式中直接使用特殊字符! 请使用 `ast` 来代替 `~`, 请使用 `ver` 或 `abs` 来代替 `|`** ! 这一点想不到什么好的解决方法.
4. 在 `macroescape.py` 中, 所有的命令都需要人为添加进替换规则中;
5. 原有的 counter 系统并无记录, 也没有保留在 JSON 文件中. 这就导致了链接系统目前只考虑了 `\hyperref` 而没有考虑 `\ref` .