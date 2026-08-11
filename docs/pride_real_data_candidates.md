# PRIDE 真实数据测试候选（MSDT-Converter v2）

> 调研日期：2026-08-11。只使用 PRIDE Archive / ProteomeXchange 官方项目元数据、PRIDE API 和官方文件主机；未下载大文件。文件大小以 API 的 `fileSizeBytes` 为准，MiB = bytes / 1,048,576。

## 结论

最合适的组合不是一个大项目，而是三层测试集：

1. **SCIEX 冒烟 + 批处理主集：`PXD061973`**。单组 `WIFF/WIFF.scan` 只有 144.81 MiB；4 组合计 615.28 MiB，正好同时验证 WIFF 扫描映射、`file_list` 和 global FDR。
2. **Thermo 回归集：`PXD000001`**。经典 LTQ Orbitrap Velos RAW 只有 210.26 MiB，还有 FASTA、Mascot DAT，以及项目记录直接链接的后续 mzML，很适合做 RAW→mzML 转换回归。
3. **PTM / 多电荷压力集：`PXD079474`**。直接下载已转换 mzML + FASTA + mzIdentML 约 587 MiB；官方方法明确是 Exploris 480 DDA Top15、HCD、前体电荷 2–6，且是 Fe-NTA 富集的 STY 磷酸化样本。

如需“官方已转 mzML 与同名 WIFF 一对一”的金标准，再增加 `PXD064530`；它的价值高，但单组完整下载要 2.44 GiB，不应作为首次冒烟测试。

## A. 首选：PXD061973（SCIEX 小文件 + 4 文件批处理）

PRIDE 项目：[PXD061973](https://www.ebi.ac.uk/pride/archive/projects/PXD061973)
官方元数据：[project API](https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD061973) · [files API](https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD061973/files?pageSize=1000&page=0)

- 仪器：PRIDE 受控字段为 **TripleTOF 5600**；样本方法文本写 **Triple-TOF 5600+ (AB SCIEX)**。
- 采集：PRIDE 受控字段为 **Data-dependent acquisition**，方法文本写 **information-dependent acquisition (IDA)**。
- PTM：PRIDE 标注“No PTMs are included in the dataset”，适合先排除 PTM 干扰。
- 处理：原作者用 ProteinPilot 4.5，E. coli + rabbit UniProt（2021-09-28），1% FDR。但该项目是 partial submission，**未存放 FASTA 或搜索结果**；因此它适合使用本项目统一的 FragPipe/FASTA 重搜，不适合要求复现原论文鉴定数。

| Run | WIFF | WIFF.scan | 合计 |
|---|---:|---:|---:|
| `1` | `1.wiff` — 12,455,936 B (11.88 MiB) | `1.wiff.scan` — 139,391,092 B (132.93 MiB) | 144.81 MiB |
| `2` | `2.wiff` — 12,156,928 B (11.59 MiB) | `2.wiff.scan` — 155,982,256 B (148.76 MiB) | 160.35 MiB |
| `3` | `3.wiff` — 12,161,024 B (11.60 MiB) | `3.wiff.scan` — 149,001,820 B (142.10 MiB) | 153.70 MiB |
| `4` | `4.wiff` — 12,840,960 B (12.25 MiB) | `4.wiff.scan` — 151,177,880 B (144.17 MiB) | 156.42 MiB |
| **全部** |  |  | **645,167,896 B = 615.28 MiB** |

官方 HTTPS 目录前缀：`https://ftp.pride.ebi.ac.uk/pride/data/archive/2026/03/PXD061973/`。示例：[1.wiff](https://ftp.pride.ebi.ac.uk/pride/data/archive/2026/03/PXD061973/1.wiff) · [1.wiff.scan](https://ftp.pride.ebi.ac.uk/pride/data/archive/2026/03/PXD061973/1.wiff.scan)。

**用法：**先只下载 Run 1 做冒烟；通过后下载 1–4，用同一 msconvert 参数转为 4 个 mzML，用同一 FASTA/工作流跑 FragPipe，然后测 `file_list` 与 global Percolator。**`.wiff` 和同名 `.wiff.scan` 必须一起下载和保存。**

## B. Thermo 回归：PXD000001

PRIDE 项目：[PXD000001](https://www.ebi.ac.uk/pride/archive/projects/PXD000001)
官方元数据：[project API](https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD000001) · [files API](https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD000001/files?pageSize=1000&page=0)

- 仪器：**LTQ Orbitrap Velos**；实验类型标注为 bottom-up proteomics。原始文件名包含 `Top10HCD`，可用于 HCD 回归；PRIDE 受控字段未另外标注 DDA，所以应从实际 mzML 扫描结构再确认。
- PTM：PRIDE 标注 monohydroxylation、TMT6plex acylation 和 methylthiolation。

| 角色 | 文件 | 大小 |
|---|---|---:|
| Thermo RAW | [`TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.raw`](https://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/PXD000001/TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.raw) | 220,475,548 B (210.26 MiB) |
| 数据库 | [`erwinia_carotovora.fasta`](https://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/PXD000001/erwinia_carotovora.fasta) | 1,657,668 B (1.58 MiB) |
| 原搜索结果（仅作参考） | [`F063721.dat`](https://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/PXD000001/F063721.dat) | 21,185,462 B (20.20 MiB) |
| 后续转换 mzML | [`...01-20141210.mzML`](https://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/PXD000001/TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML) | 450,032,788 B (429.18 MiB) |

注：当前 files API 列出 RAW、FASTA、DAT 和旧 mzXML，却未列出上表的 `-20141210.mzML`；但该 mzML 由**项目自身的 data-processing protocol 直接链接**，且官方 PRIDE HTTPS 主机返回 200 与上述 Content-Length。它因此可作为转换对照，但不应假设它与当前 msconvert 参数完全相同。

**最小下载：**RAW + FASTA = 211.84 MiB。
**RAW/mzML 对照：**RAW + FASTA + 官方 mzML = 641.03 MiB。

## C. PTM / 多电荷：PXD079474

PRIDE 项目：[PXD079474](https://www.ebi.ac.uk/pride/archive/projects/PXD079474)
官方元数据：[project API](https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD079474) · [files API](https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD079474/files?pageSize=1000&page=0)

- 仪器：**Orbitrap Exploris 480**。
- 样本：Fe-NTA 富集 phosphopeptide，搜索可变修饰包括 oxidation (M)、protein N-terminal acetylation 和 phosphorylation (S/T/Y)，固定 carbamidomethylation (C)。PRIDE PTM 受控字段是 phosphorylated residue。
- 采集：方法文本明确是 **DDA Top15, HCD, MS2 charge 2–6**，因此能直接压测 `charge`、修饰序列和 PSM 富集字段。“允许 2–6”不等于每个电荷一定存在，最终要以提取后直方图为准。

| 角色 | 文件 | 大小 |
|---|---|---:|
| 首选输入 | [`SpermC_Rep1.mzML`](https://ftp.pride.ebi.ac.uk/pride/data/archive/2026/07/PXD079474/SpermC_Rep1.mzML) | 591,044,161 B (563.66 MiB) |
| FASTA | [`SwissProt_Mouse_03232022.fasta`](https://ftp.pride.ebi.ac.uk/pride/data/archive/2026/07/PXD079474/SwissProt_Mouse_03232022.fasta) | 11,926,463 B (11.37 MiB) |
| 外部鉴定对照 | [`SpermC_Rep1.mzid`](https://ftp.pride.ebi.ac.uk/pride/data/archive/2026/07/PXD079474/SpermC_Rep1.mzid) | 12,712,011 B (12.12 MiB) |
| 可选 Thermo RAW | [`SpermC_Rep1.raw`](https://ftp.pride.ebi.ac.uk/pride/data/archive/2026/07/PXD079474/SpermC_Rep1.raw) | 1,268,241,220 B (1,209.49 MiB) |
| 可选 PD 结果 | [`SpermC_Rep1.pdResult`](https://ftp.pride.ebi.ac.uk/pride/data/archive/2026/07/PXD079474/SpermC_Rep1.pdResult) | 593,108,992 B (565.63 MiB) |

**建议下载：**先取 mzML + FASTA + mzid，共 587.16 MiB；这已足以检查 PTM/电荷。除非要额外测试 Exploris RAW 转换，否则不必下载 1.21 GiB RAW 和 565.63 MiB `pdResult`。

## D. 可选金标准：PXD064530（同名 WIFF/WIFF.scan/mzML）

PRIDE 项目：[PXD064530](https://www.ebi.ac.uk/pride/archive/projects/PXD064530)
官方元数据：[project API](https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD064530) · [files API](https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD064530/files?pageSize=1000&page=0)

- 仪器 / 采集：**TripleTOF 5600, DDA**。
- PTM：PRIDE 标注 oxidation、deamidation、iodoacetamide derivatization 和 iTRAQ8plex-116 acylation；处理方法详细说明 iTRAQ8plex (K/Y/peptide N-terminus)、carbamidomethyl (C) 等搜索设置。
- 关键价值：项目 data-processing protocol 明确说明 `.wiff` 由 ProteoWizard `qtofpeakpicker` 转为 mzML（resolution 15,000，threshold 7.5），且三个文件同名；非常适合检查 native ID、MS2 数量、RT 和 precursor m/z 映射。

| 文件 | 大小 |
|---|---:|
| [`23062_EA1Cleavage_iTRAQ.wiff`](https://ftp.pride.ebi.ac.uk/pride/data/archive/2025/11/PXD064530/23062_EA1Cleavage_iTRAQ.wiff) | 10,194,944 B (9.72 MiB) |
| [`23062_EA1Cleavage_iTRAQ.wiff.scan`](https://ftp.pride.ebi.ac.uk/pride/data/archive/2025/11/PXD064530/23062_EA1Cleavage_iTRAQ.wiff.scan) | 1,551,030,628 B (1,479.18 MiB) |
| [`23062_EA1Cleavage_iTRAQ.mzML`](https://ftp.pride.ebi.ac.uk/pride/data/archive/2025/11/PXD064530/23062_EA1Cleavage_iTRAQ.mzML) | 1,062,876,923 B (1,013.64 MiB) |
| **合计** | **2,624,102,495 B = 2.44 GiB** |

## E. 可选 SCIEX + MGF 对照：PXD074970

PRIDE 项目：[PXD074970](https://www.ebi.ac.uk/pride/archive/projects/PXD074970)
官方元数据：[project API](https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD074970) · [files API](https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD074970/files?pageSize=1000&page=0)

该项目的价值是每组都有 `WIFF + WIFF.scan + MGF`，可用 MGF 做独立 peak-list 对照；仪器是 TripleTOF 5600，ProteinPilot/Paragon 搜索方法包含 Met oxidation、N-terminal pyroGlu/acetylation 等可变修饰和 Cys carboxyamidomethylation。

| Run | WIFF | WIFF.scan | MGF | 合计 |
|---|---:|---:|---:|---:|
| `pcDNA_section_1` | 17.94 MiB | 474.21 MiB | 2.85 MiB | 495.00 MiB |
| `PACS1_WT_section_2` | 16.78 MiB | 461.44 MiB | 7.31 MiB | 485.53 MiB |
| `PACS1_R203W_section_3` | 16.62 MiB | 449.72 MiB | 5.33 MiB | 471.67 MiB |

精确文件名可见 [files API](https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD074970/files?pageSize=1000&page=0)。元数据有一处需要注意：受控 experiment type 写“Top-down proteomics”，但样本/数据处理文本明确写了 trypsin 和基于多肽的 ProteinPilot 鉴定。因此它适合做格式与谱峰对照，但测试报告中不应盲目照抄“Top-down”。

## 建议的执行顺序与验收点

### 1. 最小 SCIEX 冒烟（~145 MiB）

仅使用 `PXD061973/1.wiff` + `1.wiff.scan`：

- Windows + SCIEX 兼容 msconvert 转 mzML；
- `wiff_mzml_rawspecturm` 能完整提取 MS2；
- FragPipe `ScanNr` 与 Parquet `scan + 1` 映射无缺失/重复；
- native ID 不使用非唯一 cycle 单独对齐；
- RT / precursor m/z 交叉检查全部通过。

### 2. 4-run `file_list` + true global FDR（~615 MiB）

使用 `PXD061973` 的 1–4，所有 run 用完全相同的 FASTA、FragPipe workflow 和 Percolator 版本：

- `file_list` 四个输入都实际搜索，不覆盖输出；
- 4 个 PIN 特征表头与 `DefaultDirection` 一致；
- global remap 后 `(run_id, ScanNr)` 全局唯一，同一 spectrum 的多 candidate 仍共用一个 remapped scan；
- global target/decoy 回填到单 run 后，PSM 总数与可解释的 FDR 过滤一致，不因 run 间 scan 重号丢数据。

### 3. Thermo RAW 回归（~212 MiB 最小）

用 `PXD000001` RAW + FASTA，与当前已有 Thermo 测试结果比较 schema、scan、RT、precursor m/z、charge、`score/q-value/PEP` 缺失率。如下载官方后续 mzML，再比较 MS2 数与关键元数据；允许因转换工具/参数不同而存在可说明差异。

### 4. 磷酸化 / 多电荷（~587 MiB）

用 `PXD079474` 的 mzML + FASTA + mzid：

- 统计实际 `charge` 分布，检查范围与 DDA 2–6 设置相容；
- 磷酸化 S/T/Y、oxidation M、N-term acetylation 和 carbamidomethyl C 的序列/位点表达不丢失、不重复、不误归一化；
- 比较 FragPipe/Percolator 输出与存档 mzIdentML 的 scan/电荷/序列覆盖，但不强求不同搜索引擎的 PSM 一对一相等。

## 不建议首批下载的类型

- 只下载 `.wiff` 而遗漏 `.wiff.scan`。
- 一开始就下载数 GB 的 SWATH/DIA 队列；当前主要验收的是 DDA + FragPipe/Percolator 路径。
- 对不同批次、不同 FASTA/搜索空间的 PIN 强行做 global FDR。
- 把存档的 Mascot DAT、ProteinPilot XLSX 或 PD `pdResult` 当成本转换器可直接消费的 FragPipe PIN；这些只是外部参考。

## 官方资料

- [PRIDE Archive API guide](https://www.ebi.ac.uk/pride/ws/archive/v2/docs/api-guide.html)：项目、文件、MSRun 元数据等接口说明。
- [PRIDE API overview](https://www.ebi.ac.uk/pride/markdownpage/prideapi)：v3 project/search 接口与 Swagger 入口。
- [PRIDE file download guide](https://www.ebi.ac.uk/pride/markdownpage/pridefiledownload)：FTP/Aspera/Globus/流式下载方式。
- [ProteomeXchange dataset lookup](https://proteomecentral.proteomexchange.org/cgi/GetDataset)：用 PXD accession 查询 ProteomeXchange 记录。
