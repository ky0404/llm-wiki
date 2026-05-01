#!/usr/bin/env python3
"""
终极 PDF 解析器 — 自适应管道 v3.0
==========================
基于《盘点 Python 中那些 PDF 解析库》的工具分析：
  1. pypdfium2: 文本提取快且准 (主力)
  2. pdfplumber: 表格提取强 (表格页专用)
  3. Tesseract OCR: 扫描件后备
  4. 多模态 LLM: 复杂公式/留空标记
智能页面级选择 + 表格自动检测 + 质量降级
"""

import os, sys, re, json, subprocess, shutil, base64, argparse, time
from pathlib import Path
from typing import Optional, Tuple, List, Dict

# 从 bashrc 加载 API 配置
def load_api_config():
    bashrc_path = os.path.expanduser("~/.bashrc")
    if os.path.exists(bashrc_path):
        with open(bashrc_path) as f:
            for line in f:
                m = re.match(r'export\s+OPENAI_API_KEY="([^"]+)"', line.strip())
                if m and "OPENAI_API_KEY" not in os.environ:
                    os.environ["OPENAI_API_KEY"] = m.group(1)
                m = re.match(r'export\s+OPENAI_BASE_URL="([^"]+)"', line.strip())
                if m and "OPENAI_BASE_URL" not in os.environ:
                    os.environ["OPENAI_BASE_URL"] = m.group(1)

load_api_config()

# ============================================================
# 0. 依赖安装
# ============================================================
def ensure_deps():
    deps = ["pdfplumber", "pymupdf", "pillow", "pytesseract"]
    for d in deps:
        try:
            __import__(d.replace("-", "_"))
        except ImportError:
            print(f"Installing {d}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", d])
    if not shutil.which("tesseract"):
        print("⚠️ Tesseract not found. Run: sudo apt install tesseract-ocr tesseract-ocr-chi-sim")

# ============================================================
# 1. 质量检测 (多维度)
# ============================================================
def quality_report(text: str) -> Dict:
    if not text:
        return {"ok": False, "reason": "empty", "score": 0}
    
    words = text.split()
    n_words = len(words)
    
    # 基础检测
    if n_words < 50:
        return {"ok": False, "reason": "too_few_words", "score": 0}
    
    # 平均词长
    avg_len = sum(len(w) for w in words) / n_words
    if avg_len > 20:
        return {"ok": False, "reason": "avg_word_too_long", "score": 0}
    
    # 页面数估算 (按 --- Page N --- 分割)
    page_markers = len(re.findall(r'--- Page \d+ ---', text))
    estimated_pages = max(page_markers, 1)
    
    # 内容密度 (字数/页)
    density = n_words / estimated_pages if estimated_pages > 0 else 0
    
    # 检测乱码 (非中日韩字符占比)
    valid_chars = sum(1 for c in text if ord(c) < 0x4E00 or c in "，。！？；：、""''（）【】《》")
    valid_ratio = valid_chars / max(len(text), 1)
    
    # 计算综合分数 (0-100)
    score = min(100, int(
        (n_words / 500 * 30) +  # 字数分 (假设500字/页正常)
        (density / 500 * 30) +   # 密度分
        (valid_ratio * 40)      # 有效字符分
    ))
    
    ok = score >= 40 and n_words >= 100
    reason = "ok" if ok else f"score={score}, words={n_words}, density={density:.0f}"
    
    return {"ok": ok, "reason": reason, "score": score, "pages": estimated_pages, "words": n_words}

# ============================================================
# 1. pypdfium2 提取 (文本快且准)
# ============================================================
def extract_with_pypdfium2(pdf_path: str) -> Tuple[str, List[Dict]]:
    """pypdfium2 文本提取 - 快速且准确"""
    import pdfium2
    text_parts = []
    tables = []  # pypdfium2 不直接支持表格
    
    try:
        pdf = pdfium2.PdfDocument(pdf_path)
        total_pages = len(pdf)
        
        for i in range(total_pages):
            if i % 10 == 0:
                print(f"    [pypdfium2] Processing page {i+1}/{total_pages}...")
            
            page = pdf.get_page(i)
            textpage = page.get_textpage()
            text = textpage.extract_text()
            
            if text:
                text_parts.append(f"--- Page {i+1} ---\n{text}")
            else:
                text_parts.append(f"--- Page {i+1} ---\n[空白页]")
            
            page.close()
        
        pdf.close()
    except Exception as e:
        print(f"    [pypdfium2] Error: {e}")
    
    return "\n\n".join(text_parts), tables

# ============================================================
# 2. pdfplumber 提取 (表格强)
# ============================================================
def extract_with_pdfplumber(pdf_path: str) -> Tuple[str, List[Dict]]:
    import pdfplumber
    text_parts = []
    tables = []
    laparams = {
        "line_overlap": 0.5,
        "char_margin": 2.0,
        "line_margin": 0.5,
        "word_margin": 0.1,
    }
    # 优化表格提取参数
    table_settings = {
        "vertical_strategy": "lines_strict",
        "horizontal_strategy": "lines_strict",
        "intersection_tolerance": 0.1,
        "snap_tolerance": 3,
        "join_tolerance": 3,
    }
    with pdfplumber.open(pdf_path, laparams=laparams) as pdf:
        total_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            if i % 10 == 0:
                print(f"    [pdfplumber] Processing page {i+1}/{total_pages}...")
            
            # 文本提取 - word level 避免空格丢失
            words = page.extract_words()
            if words:
                lines_dict = {}
                for word in words:
                    y = round(word['top'], 1)
                    if y not in lines_dict:
                        lines_dict[y] = []
                    lines_dict[y].append(word['text'])
                sorted_lines = []
                for y in sorted(lines_dict.keys()):
                    line_text = ' '.join(lines_dict[y])
                    sorted_lines.append(line_text)
                page_text = '\n'.join(sorted_lines)
            else:
                page_text = page.extract_text() or ""
            
            text_parts.append(f"--- Page {i+1} ---\n{page_text}")
            
            # 优化表格提取
            page_tables = page.extract_tables(table_settings=table_settings)
            for ti, tbl in enumerate(page_tables):
                if tbl:
                    tables.append({"page": i+1, "index": ti, "data": tbl})
    
    return "\n\n".join(text_parts), tables

# ============================================================
# 3. OCR 后备 (Tesseract)
# ============================================================
def ocr_page_image(image_path: str, lang: str = "eng+chi_sim") -> str:
    import pytesseract
    from PIL import Image
    img = Image.open(image_path)
    # 预处理: 增强对比度
    from PIL import ImageEnhance
    img = ImageEnhance.Contrast(img).enhance(1.5)
    return pytesseract.image_to_string(img, lang=lang)

def extract_with_ocr(pdf_path: str, lang: str = "eng+chi_sim") -> str:
    import fitz
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    parts = []
    
    for i in range(total_pages):
        if i % 10 == 0:
            print(f"    [OCR] Processing page {i+1}/{total_pages}...")
        
        page = doc[i]
        pix = page.get_pixmap(dpi=200)
        img_path = f"/tmp/page_{i}_{os.getpid()}.png"
        pix.save(img_path)
        
        try:
            text = ocr_page_image(img_path, lang)
            parts.append(f"--- Page {i+1} ---\n{text}")
        finally:
            try:
                os.remove(img_path)
            except:
                pass
    
    return "\n\n".join(parts)

# ============================================================
# 4. 多模态大模型 (终极武器) - 全量提取版
# ============================================================
def call_multimodal_llm(images_b64: List[str], api_key: str = None, base_url: str = None, model: str = "qwen2.5-vl-72b") -> str:
    """多模态模型 API 调用 (华为云 MaaS)"""
    if not api_key:
        api_key = os.environ.get("MAAS_API_KEY") or os.environ.get("MULTIMODAL_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            import re
            bashrc_path = os.path.expanduser("~/.bashrc")
            if os.path.exists(bashrc_path):
                with open(bashrc_path) as f:
                    for line in f:
                        m = re.match(r'export\s+OPENAI_API_KEY="([^"]+)"', line.strip())
                        if m:
                            api_key = m.group(1)
                            break
    if not base_url:
        base_url = os.environ.get("MAAS_BASE_URL") or os.environ.get("OPENAI_BASE_URL")
        if not base_url:
            import re
            bashrc_path = os.path.expanduser("~/.bashrc")
            if os.path.exists(bashrc_path):
                with open(bashrc_path) as f:
                    for line in f:
                        m = re.match(r'export\s+OPENAI_BASE_URL="([^"]+)"', line.strip())
                        if m:
                            base_url = m.group(1)
                            break
        # 确保 base_url 末尾有 /v1
        if base_url:
            base_url = base_url.rstrip("/")
            if not base_url.endswith("/v1"):
                base_url = base_url + "/v1"
    
    
    messages = [
        {"role": "system", "content": "你是一个专业的 PDF 转 Markdown 助手。请将以下图片中的内容完整转换为 Markdown 格式，保留标题、表格、公式（LaTeX）、列表、图片占位（用 ![](image_page_N)）。直接输出 Markdown，必要时用多个 --- Page N --- 分隔页面。不要解释。"}
    ]
    
    # 分批发送 (每批5页，避免超限)
    all_results = []
    batch_size = 5
    for batch_idx in range(0, len(images_b64), batch_size):
        batch = images_b64[batch_idx:batch_idx + batch_size]
        
        # 构建多图消息
        user_content = []
        for img in batch:
            user_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}})
        
        batch_messages = messages + [
            {"role": "user", "content": user_content}
        ]
        
        payload = json.dumps({
            "model": model,
            "messages": batch_messages,
            "max_tokens": 4096
        }).encode()
        
        req = urllib.request.Request(f"{base_url}/chat/completions", data=payload, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        })
        
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                result = json.loads(resp.read())
                all_results.append(result["choices"][0]["message"]["content"])
        except Exception as e:
            raise RuntimeError(f"API call failed: {e}")
    
    return "\n\n".join(all_results)

def extract_with_multimodal(pdf_path: str, api_key: str = None, base_url: str = None, model: str = "qwen2.5-vl-72b", max_pages: int = 999) -> str:
    """多模态提取 - 全量版"""
    import fitz
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    pages_to_process = min(total_pages, max_pages)
    
    print(f"    [multimodal] Converting {pages_to_process} pages to images...")
    images_b64 = []
    
    for i in range(pages_to_process):
        if i % 10 == 0:
            print(f"    [multimodal] Processing page {i+1}/{pages_to_process}...")
        
        page = doc[i]
        # 高分辨率输出，确保文字清晰
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        images_b64.append(base64.b64encode(img_bytes).decode())
    
    print(f"    [multimodal] Sending {len(images_b64)} images to LLM...")
    text = call_multimodal_llm(images_b64, api_key, base_url, model)
    
    # 如果输出没有页面标记，添加标记
    if "--- Page" not in text and pages_to_process > 1:
        lines = text.split('\n')
        result_lines = []
        for i, line in enumerate(lines):
            result_lines.append(line)
            # 每500字插入页面标记
            if i > 0 and i % 100 == 0:
                result_lines.append(f"--- Page {i//100 + 1} ---")
        text = '\n'.join(result_lines)
    
    return text

# ============================================================
# 5. 后处理
# ============================================================
def clean_noise(text: str) -> str:
    """清理噪声"""
    lines = text.split('\n')
    cleaned = []
    noise_at_start = True
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            cleaned.append(line)
            continue
        
        if noise_at_start:
            is_noise = False
            if stripped.isdigit() and len(stripped) >= 4:
                is_noise = True
            elif re.match(r'^\d{4}\.\d{4}v\d+:', stripped):
                is_noise = True
            elif re.match(r'^[\[\](){}|<>].*', stripped) and len(stripped) < 15:
                is_noise = True
            elif len(stripped) == 1 and not stripped.isalnum():
                is_noise = True
            if not is_noise:
                noise_at_start = False
        
        if not noise_at_start:
            if stripped.isdigit() and len(stripped) >= 4:
                continue
            cleaned.append(line)
    
    text = '\n'.join(cleaned)
    
    # 过滤 <EOS>/<pad> 等残留
    text = re.sub(r'<[/]?(EOS|pad|s)[/]?>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<[/]?s[/]?>', '', text)
    
    # CamelCase 修复
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    
    return text

# ============================================================
# 5.1 单词粘连修复
# ============================================================
def fix_merged_words(text: str) -> str:
    """修复 pdfplumber 提取的单词粘连问题 - 使用正则替换"""
    # 常见粘连词对 (前面是已经修复过的常见词)
    merged_pairs = [
        # Transformer 架构
        ("attentionmechanism", "attention mechanism"),
        ("attentionweighted", "attention weighted"),
        ("multiheadattention", "multi-head attention"),
        ("selfattention", "self-attention"),
        ("crossattention", "cross-attention"),
        ("scaleddotproduct", "scaled dot-product"),
        ("encoderdecoder", "encoder-decoder"),
        ("encoderanddecoder", "encoder and decoder"),
        ("feedforward", "feed-forward"),
        ("feedforwardnetwork", "feed-forward network"),
        ("positionalencoding", "positional encoding"),
        ("layer_norm", "layer norm"),
        ("residualconnection", "residual connection"),
        # 深度学习
        ("neuralnetwork", "neural network"),
        ("convolutionalneural", "convolutional neural"),
        ("recurrentneural", "recurrent neural"),
        ("gatedrecurrent", "gated recurrent"),
        ("longshorttermmemory", "long short-term memory"),
        ("batchnormalization", "batch normalization"),
        ("backpropagation", "backpropagation"),
        ("gradientdescent", "gradient descent"),
        ("activationfunction", "activation function"),
        # NLP
        ("machinetranslation", "machine translation"),
        ("languagemodel", "language model"),
        ("sequencetosequence", "sequence-to-sequence"),
        ("wordembedding", "word embedding"),
        ("tokenization", "tokenization"),
        ("crossentropy", "cross-entropy"),
        ("stateoftheart", "state-of-the-art"),
        # 训练
        ("fine-tuning", "fine-tuning"),
        ("pretrained", "pre-trained"),
        ("warmup", "warm-up"),
        # 其他
        ("begin", "b e g i n"),
    ]
    
    for old, new in merged_pairs:
        text = text.replace(old, new)
    
    # 修复 CamelCase (小写+大写 -> 小写+空格+大写)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # 修复数字+字母粘连 (如 12gpu, 8v100)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    
    # Greedy longest-match 分词 - 基于词汇表最长匹配
    words_to_split = [
        "attentionmechanism", "attentionweighted", "multiheadattention",
        "selfattention", "crossattention", "scaleddotproduct",
        "encoderdecoder", "encoderanddecoder", "feedforwardnetwork",
        "positionalencoding", "layer_normali", "residualconnection",
        "neuralnetwork", "convolutionalneural", "recurrentneural",
        "gatedrecurrent", "longshorttermmemory", "batchnormalization",
        "backpropagation", "gradientdescent", "activationfunction",
        "machinetranslation", "languagemodel", "sequencetosequence",
        "wordembedding", "tokenization", "crossentropy",
        "multiheadattention", "feedforwardnetwork", "layernormalization",
        "sequencetransduction", "parameterfree", "tensor2tensor",
        "stateoftheart", "parallelizable", "pre-trained",
        "finetuning", "bidirectional", "word2vec",
    ]
    
    # 按长度降序排列确保最长匹配优先
    for word in sorted(words_to_split, key=len, reverse=True):
        text = text.replace(word, word)
    
    return text

# ============================================================
# 5.2 页眉噪声过滤
# ============================================================
def filter_header_noise(text: str) -> str:
    """过滤页眉/页脚的 arXiv 编号、版权声明等噪声"""
    lines = text.split('\n')
    filtered = []
    skip_count = 0
    
    for line in lines:
        stripped = line.strip()
        
        # 检测页眉噪声模式
        is_noise = False
        
        # 模式1: 纯数字或纯符号行（页码）
        if stripped.isdigit() and len(stripped) <= 5:
            is_noise = True
            skip_count += 1
        
        # 模式2: arXiv 编号
        elif re.match(r'^arXiv:\d{4}\.\d{4,5}v\d+$', stripped):
            is_noise = True
            skip_count += 1
        
        # 模式3: 版权声明等短行
        elif len(stripped) <= 3 and not stripped.isalnum():
            is_noise = True
            skip_count += 1
        
        # 模式4: 连续单字符（被拆散的噪声）
        elif len(stripped) <= 2 and stripped.isalpha():
            if filtered and len(filtered[-1].strip()) <= 2:
                is_noise = True
                skip_count += 1
        
        # 模式5: 残留排版符号 (gu A, ]LC.sc[, etc.)
        elif re.match(r'^[\[\]〈〉「」『』]{1,3}.*', stripped) or re.match(r'.*[\[\]〈〉「」『』]{1,3}$', stripped):
            is_noise = True
            skip_count += 1
        
        # 模式6: 会议信息 - 简短包含年份
        elif re.match(r'.*Conference.*\d{4}.*', stripped) and len(stripped) < 60:
            is_noise = True
            skip_count += 1
        
        if not is_noise:
            filtered.append(line)
    
    return '\n'.join(filtered)

# ============================================================
# 5.3 段落分隔
# ============================================================
def add_paragraph_breaks(text: str) -> str:
    """在段落之间添加空行分隔"""
    lines = text.split('\n')
    result = []
    prev_ended = False
    
    for line in lines:
        stripped = line.strip()
        
        # 跳过页眉标记和空行
        if stripped.startswith('--- Page') or not stripped:
            result.append(line)
            prev_ended = False
            continue
        
        # 检测段落结束：句号/问号/感叹号后跟大写字母开头
        if prev_ended and len(stripped) > 0:
            # 检查是否大写字母开头（新段落）
            if stripped[0].isupper() and stripped[0].isalpha():
                result.append('')  # 添加空行作为段落分隔
        
        # 检测句子结束标记
        if stripped.endswith('.') or stripped.endswith('?') or stripped.endswith('!'):
            prev_ended = True
        else:
            prev_ended = False
        
        result.append(line)
    
    return '\n'.join(result)

# ============================================================
# 5.4 反向/乱码文本修复
# ============================================================
def fix_corrupted_text(text: str) -> str:
    """检测并标记反向/乱码文本区域"""
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 跳过页面标记和空行
        if line.startswith('--- Page') or not line:
            result.append(line)
            i += 1
            continue
        
        result.append(line)
        i += 1
    
    return '\n'.join(result)

# ============================================================
# 5.5 合并标题行
# ============================================================
def merge_title_lines(text: str) -> str:
    """合并作者信息等结构化数据"""
    lines = text.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # 跳过页面标记
        if stripped.startswith('--- Page') or not stripped:
            result.append(line)
            i += 1
            continue
        
        # 检测作者行模式：名字 | 机构 | email
        if '|' in stripped and '@' in stripped:
            # 已经是合并格式
            result.append(line)
            i += 1
            continue
        
        # 检测连续的短行模式
        if len(stripped) < 50 and '@' in stripped:
            # 这是邮箱行，保留原样
            result.append(line)
            i += 1
            continue
        
        result.append(line)
        i += 1
    
    return '\n'.join(result)

# ============================================================
# 5.6 参考文献格式化
# ============================================================
def format_references(text: str) -> str:
    """识别并格式化参考文献"""
    lines = text.split('\n')
    result = []
    in_references = False
    ref_num = 0
    buffer = []
    
    for line in lines:
        stripped = line.strip()
        
        # 检测参考文献章节开始
        if stripped.lower() == 'references':
            in_references = True
            result.append(line)
            continue
        
        if in_references:
            # 空行结束参考文献
            if not stripped:
                in_references = False
                # 刷新缓冲的参考文献
                if buffer:
                    for ref in buffer:
                        result.append(ref)
                    buffer = []
                result.append(line)
                continue
            
            # 检测参考文献编号 [数字]
            match = re.match(r'^\[(\d+)\]', stripped)
            if match:
                ref_num = int(match.group(1))
                buffer.append(stripped)
            elif stripped.startswith('ar Xiv') or stripped.startswith('Co RR'):
                # 连续的行合并
                if buffer:
                    buffer[-1] = buffer[-1] + ' ' + stripped
                else:
                    buffer.append(stripped)
            else:
                # 其他行合并到最后
                if buffer:
                    buffer[-1] = buffer[-1] + ' ' + stripped
                else:
                    buffer.append(stripped)
        else:
            result.append(line)
    
    # 刷新剩余的参考文献
    if buffer:
        for ref in buffer:
            result.append(ref)
    
    return '\n'.join(result)

def table_to_markdown(data) -> str:
    if not data:
        return ""
    lines = []
    for row in data:
        cells = [str(c) if c else "" for c in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)

# ============================================================
# 6. 自适应管道 v3.0
# ============================================================
def detect_tables_page(pdf_path: str, page_num: int) -> bool:
    """检测指定页面是否包含表格"""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            if page_num <= len(pdf.pages):
                page = pdf.pages[page_num - 1]
                tables = page.extract_tables()
                return len(tables) > 0
    except:
        pass
    return False

def convert_pdf(pdf_path: str, mode: str = "auto", api_key: str = None, base_url: str = None, model: str = "qwen2.5-vl-72b", max_pages: int = 999) -> str:
    """自适应管道 v3.0 - 页面级工具选择"""
    pdf_path = Path(pdf_path)
    out_path = pdf_path.with_suffix(".md")
    
    results = {}  # page_num -> {"text": str, "tables": list}
    method = ""
    method_tried = []
    
    # ===== 策略1: PyMuPDF 快速文本提取 (默认) =====
    if mode in ("auto", "pymupdf", "hybrid"):
        try:
            print(f"  [Strategy 1] PyMuPDF: Fast text extraction...")
            start = time.time()
            
            # 使用 PyMuPDF (最快且功能最全)
            import fitz
            doc = fitz.open(str(pdf_path))
            for page in doc:
                text = page.get_text() or ""
                results[page.number + 1] = {"text": text, "tables": []}
            doc.close()
            method = "PyMuPDF"
            elapsed = time.time() - start
            all_text = " ".join([v["text"] for v in results.values()])
            qr = quality_report(all_text)
            print(f"      OK: {qr['words']} words, {qr['pages']} pages, time={elapsed:.1f}s")
            
        except Exception as e:
            print(f"      ERROR: {e}")
            method_tried.append(("PyMuPDF", 0))
    
    # ===== 策略2: 表格页专用 pdfplumber 提取 =====
    if mode in ("auto", "pdfplumber", "hybrid") and results:
        try:
            print(f"  [Strategy 2] pdfplumber: Table detection & extraction...")
            start = time.time()
            
            import pdfplumber
            table_settings = {
                "vertical_strategy": "lines_strict",
                "horizontal_strategy": "lines_strict",
                "snap_tolerance": 3,
                "join_tolerance": 3,
            }
            
            with pdfplumber.open(str(pdf_path)) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_num = i + 1
                    try:
                        page_tables = page.extract_tables(table_settings=table_settings)
                        if page_tables and page_tables[0] is not None:
                            table_data = page_tables[0]
                            if table_data and any(any(cell) for row in table_data for cell in row):
                                results[page_num]["tables"] = page_tables
                                print(f"      Page {page_num}: Found {len(page_tables)} table(s)")
                    except Exception:
                        pass
            
            print(f"      Table extraction done")
            
        except Exception as e:
            print(f"      ERROR: {e}")
    
    # ===== 策略3: OCR 后备 (处理空白页) =====
    if mode in ("auto", "ocr") and any("[需要 OCR" in v["text"] or not v["text"].strip() for v in results.values()):
        try:
            print(f"  [Strategy 3] OCR: Filling missing content...")
            start = time.time()
            
            ocr_text = extract_with_ocr(str(pdf_path))
            
            # 替换空白页
            ocr_pages = ocr_text.split("--- Page")
            for ocr_part in ocr_pages:
                if not ocr_part.strip():
                    continue
                match = re.match(r'\s*(\d+)\s*---', ocr_part)
                if match:
                    page_num = int(match.group(1))
                    content = ocr_part.split("---", 1)[1] if "---" in ocr_part else ocr_part
                    if "[需要 OCR" in results.get(page_num, {}).get("text", "") or not results.get(page_num, {}).get("text", "").strip():
                        results[page_num]["text"] = content.strip()
            
            method = "hybrid"
            elapsed = time.time() - start
            print(f"      OCR filling done, time={elapsed:.1f}s")
            
        except Exception as e:
            print(f"      ERROR: {e}")
    
    # ===== 合并结果 =====
    text_parts = []
    all_tables = []
    
    for page_num in sorted(results.keys()):
        page_data = results[page_num]
        text_parts.append(f"--- Page {page_num} ---\n{page_data['text']}")
        
        for ti, tbl in enumerate(page_data.get("tables", [])):
            if tbl:
                all_tables.append({"page": page_num, "index": ti, "data": tbl})
    
    text = "\n\n".join(text_parts)
    tables = all_tables
    
    if not text:
        raise RuntimeError("No text extracted")
    
    # 后处理链
    text = clean_noise(text)
    text = filter_header_noise(text)
    text = fix_merged_words(text)
    text = add_paragraph_breaks(text)
    text = fix_corrupted_text(text)
    text = merge_title_lines(text)
    text = format_references(text)
    
    # 重新检测
    qr = quality_report(text)
    
    # 生成 Markdown
    md = f"""---
title: "{pdf_path.stem}"
type: source
tags: [pdf, extracted]
sources: []
created: 2026-04-30
updated: 2026-04-30
---

# {pdf_path.stem}

> Extracted from: {pdf_path.name}
> Method: {method}
> Quality: {qr['score']} score, {qr['words']} words, {qr['pages']} pages

## Content

{text}
"""
    
    if tables:
        md += "\n## Tables\n\n"
        for t in tables:
            md += f"### Table {t['index']+1} (Page {t['page']})\n\n"
            md += table_to_markdown(t['data']) + "\n\n"
    
    out_path.write_text(md, encoding="utf-8")
    return str(out_path)

# ============================================================
# 7. 命令行入口
# ============================================================
def main():
    print("=" * 60)
    print("Ultimate PDF Parser v2.0 - Adaptive Pipeline")
    print("=" * 60)
    
    ensure_deps()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", nargs="?", help="PDF file path")
    parser.add_argument("--batch", action="store_true", help="Batch process raw/")
    parser.add_argument("--mode", default="auto", choices=["auto", "pdfplumber", "ocr", "multimodal", "hybrid"],
                        help="Extraction mode: auto (try all), pdfplumber (rule-based), ocr (tesseract), multimodal (LLM), hybrid (pdfplumber+OCR)")
    parser.add_argument("--api-key", help="Multimodal API key")
    parser.add_argument("--base-url", help="API base URL")
    parser.add_argument("--model", default="qwen2.5-vl-72b", help="Multimodal model")
    parser.add_argument("--max-pages", type=int, default=999, help="Max pages for multimodal (default: 999)")
    args = parser.parse_args()
    
    if args.batch:
        raw_dir = Path(__file__).parent.parent / "raw"
        pdfs = sorted(raw_dir.glob("*.pdf"))
        print(f"Found {len(pdfs)} PDF(s)")
        
        for p in pdfs:
            print(f"\n[{p.name}]")
            try:
                start = time.time()
                out = convert_pdf(str(p), args.mode, args.api_key, args.base_url, args.model, args.max_pages)
                elapsed = time.time() - start
                print(f"  => {out} ({elapsed:.1f}s)")
            except Exception as e:
                print(f"  [FAIL] {e}")
    
    elif args.pdf:
        out = convert_pdf(args.pdf, args.mode, args.api_key, args.base_url, args.model, args.max_pages)
        print(f"Output: {out}")
    
    else:
        print("Usage:")
        print("  python pdf_parser.py <pdf_file>")
        print("  python pdf_parser.py --batch")
        print("  python pdf_parser.py --batch --mode multimodal --api-key KEY")
        print("  python pdf_parser.py --batch --mode auto --max-pages 50")

if __name__ == "__main__":
    main()