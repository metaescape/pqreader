import os
import fitz  # PyMuPDF
import pymupdf
pymupdf.TOOLS.unset_quad_corrections(True) 
import os
import time

def merge_pdfs(input_directory, output_file):
    # 获取目录下所有的 PDF 文件
    pdf_files = [f for f in os.listdir(input_directory) if f.endswith('.pdf')]
    
    # 对文件名进行排序，确保拼接的顺序正确
    pdf_files.sort()

    # 创建一个空的 PDF 文档
    merged_pdf = fitz.open()

    # 遍历每个 PDF 文件并将其页面添加到 merged_pdf 中
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_directory, pdf_file)
        pdf_document = fitz.open(pdf_path)
        
        # 将当前 PDF 文件的每一页添加到目标文档
        merged_pdf.insert_pdf(pdf_document)

    # 保存合并后的 PDF 文件
    merged_pdf.save(output_file)
    merged_pdf.close()
    print(f"PDFs merged successfully into {output_file}")

def test_merge_pdfs():
    input_directory = os.path.expanduser('~/Documents/analysis')
    output_file = os.path.expanduser('~/Documents/notes.pdf')
    merge_pdfs(input_directory, output_file)
    
def convert_epub_to_pdf(doc):
    if doc.is_pdf:
        print("Input is already a PDF.")
        return
    
    b = doc.convert_to_pdf()  # convert to pdf
    pdf = fitz.open("pdf", b)  # open as pdf

    toc = doc.get_toc()  # table of contents of input
    pdf.set_toc(toc)  # simply set it for output
    meta = doc.metadata  # read and set metadata
    if not meta["producer"]:
        meta["producer"] = "PyMuPDF v" + fitz.VersionBind

    if not meta["creator"]:
        meta["creator"] = "PyMuPDF PDF converter"

    pdf.set_metadata(meta)

    # now process the links
    link_cnti = 0
    link_skip = 0
    for pinput in doc:  # iterate through input pages
        links = pinput.get_links()  # get list of links
        link_cnti += len(links)  # count how many
        pout = pdf[pinput.number]  # read corresp. output page
        for l in links:  # iterate though the links
            if l["kind"] == fitz.LINK_NAMED:  # we do not handle named links
                link_skip += 1  # count them
                continue
            pout.insert_link(l)  # simply output the others


def test_epub_to_pdf():
    path = os.path.expanduser('/data/resource/readings/manual/emacs/elisp.epub')
    before_open = time.time()
    doc = pymupdf.open(path)

    after_open = time.time()
    print("open time:", after_open - before_open)
    
    before_convert = time.time()
    convert_epub_to_pdf(doc)
    after_convert = time.time()
    print("convert time:", after_convert - before_convert)
    
def test_search_in_epub():
    
    path = os.path.expanduser('/data/resource/readings/manual/emacs/elisp.epub')
    before_open = time.time()
    doc = pymupdf.open(path)
    
    print(doc.page_count)

    after_open = time.time()
    print("open time:", after_open - before_open)
    
    before_ = time.time()
    text = doc[0].get_text()
    after_ = time.time()
    print("search time:", after_ - before_)
    
    
    before_ = time.time()
    text = doc[2].get_text()
    after_ = time.time()
    print("second search time:", after_ - before_)
    print(text)

    before_ = time.time()
    
    page = doc[0]
    result = page.search_for("debugging")
    after_ = time.time()
    print(result)
    print("search time:", after_ - before_)
    
def test_rect():
    file_path = "/data/resource/readings/manual/emacs/elisp.pdf"
    """检查 PDF 文件中所有页面的尺寸是否一致。"""

    doc = pymupdf.open(file_path)
    if not doc:
        return False, "无法打开文件"
    from PyQt6.QtWidgets import QApplication, QWidget
    app = QApplication([])
    
    print(QWidget().devicePixelRatioF())
    print(QWidget().devicePixelRatio())
    print(QWidget().devicePixelRatioFScale())
    first_page_rect = doc[0].rect  # 获取第一页的尺寸
    print(first_page_rect)
    
    doc[0].set_cropbox(doc[0].cropbox)
    pixmap = doc[0].get_pixmap(alpha=True)
    width1, height1 = pixmap.width, pixmap.height
    print(pixmap.width, pixmap.height)
    for page in doc:
        
        if page.rect != first_page_rect:
            return False, f"第 {page.number + 1} 页的尺寸与第一页不同"
        page.set_cropbox(page.cropbox)
        pixmap = page.get_pixmap(alpha=True)
        width2, height2 = pixmap.width, pixmap.height
        if width1 != width2 or height1 != height2:
            return False, f"第 {page.number + 1} 页的尺寸与第一页不同"
        
        
    return True, "所有页面的尺寸一致"

def test_search():
    file_path = "/data/resource/readings/manual/emacs/elisp.pdf"
    keyword = "model.build"
    doc = pymupdf.open(file_path)
    import time 
    before_ = time.time()
    for page in doc:
        quads = page.search_for(keyword)
        if quads:
            print(f"Found on page {page.number + 1}: {quads}")
    else:
        print(f"Keyword '{keyword}' not found in the document.")
        
    after_ = time.time()
    print("search time:", after_ - before_)
    
    file_path = "/data/resource/readings/manual/emacs/elisp.pdf"
    keyword = "debugging"
    doc = pymupdf.open(file_path)
    import time 
    before_ = time.time()
    cnt = 0

    for page in doc:
        quads = page.search_for(keyword)
        if quads:
            # print(f"Found on page {page.number + 1}: {quads}")
            cnt += 1
    else:
        print(f"Keyword '{keyword}' not found in the document.")
    print("cnt", cnt)
    
        
    after_ = time.time()
    print("search time:", after_ - before_)
    
    before_ = time.time()
    cnt = 0

    for page in doc:
        quads = page.search_for("a")
        if quads:
            # print(f"Found on page {page.number + 1}: {quads}")
            cnt += 1
    else:
        print(f"Keyword '{keyword}' not found in the document.")
    print("cnt", cnt)
    
        
    after_ = time.time()
    print("search for single char:", after_ - before_)
    
    before_ = time.time()
    # generate textPage for each page
    text_pages = []
    for page in doc:
        text_page = page.get_textpage()
        text_pages.append(text_page)
        
    print("text pages generated time:", time.time() - before_)
    # search for keyword in textPage
    print(f"{len(text_pages)} text pages")
    before_ = time.time()
    cnt = 0
    for text_page in text_pages:
        quads = text_page.search(keyword)
        if quads:
            # print(f"Found on page {page.number + 1}: {quads}")
            cnt += 1
    else:
        print(f"Keyword '{keyword}' not found in the document.")
    after_ = time.time()
    print("cnt", cnt)
    print("search time:", after_ - before_)
    
def test_cropbox():
    file_path = "/data/resource/readings/manual/emacs/elisp.pdf"
    doc = pymupdf.open(file_path)
    page = doc.new_page()
    print(page.rect)
    print("mediabox:", page.mediabox)
    page.set_cropbox(pymupdf.Rect(100, 100, 400, 400))
    # this will also change the "rect" property:
    print(page.rect)
    print(page.cropbox)
    print("mediabox:", page.mediabox)
    
def test_page_counts():
    file_path = "/data/resource/readings/manual/emacs/elisp.pdf"
    doc = pymupdf.open(file_path)
    page_cnts = doc.page_count
    _before = time.time()
    heights = []
    widths = []
    for i in range(page_cnts):
        heights.append(doc.page_cropbox(i).height)
        widths.append(doc.page_cropbox(i).width)
        
    _after = time.time()
    
    from collections import Counter
    height_counter = Counter(heights)
    width_counter = Counter(widths)

    print("height counter:", height_counter)
    print("width counter:", width_counter)
    print("page count time:", _after - _before)

def flags_decomposer(flags):
    """Make font flags human readable."""
    l = []
    if flags & 2 ** 0:
        l.append("superscript")
    if flags & 2 ** 1:
        l.append("italic")
    if flags & 2 ** 2:
        l.append("serifed")
    else:
        l.append("sans")
    if flags & 2 ** 3:
        l.append("monospaced")
    else:
        l.append("proportional")
    if flags & 2 ** 4:
        l.append("bold")
    return ", ".join(l)    

def test_color():
    file_path = "/data/resource/readings/manual/emacs/elisp.pdf"
    doc = pymupdf.open(file_path)
    page_174 = doc[174]
    # get color of the text
    blocks = page_174.get_text("dict", flags=11)["blocks"]
    for b in blocks:  # iterate through the text blocks
        for l in b["lines"]:  # iterate through the text lines
            for s in l["spans"]:  # iterate through the text spans
                print("")
                font_properties = "Font: '%s' (%s), size %g, color #%06x" % (
                    s["font"],  # font name
                    flags_decomposer(s["flags"]),  # readable font flags
                    s["size"],  # font size
                    s["color"],  # font color
                )
                print("Text: '%s'" % s["text"])  # simple print of text
                print(font_properties)
                
def test_blocks():
    
    path = "/data/resource/readings/papers/2024-qiShapeLLM.pdf"
    doc = pymupdf.open(path)
    # cat = doc.pdf_catalog()  # get the xref of the catalog
    # doc.xref_set_key(cat, "StructTreeRoot", "null") 
    
    
    page_2 = doc[1]
    
    raw_dict = page_2.get_text("rawdict", flags=pymupdf.TEXT_ACCURATE_BBOXES)
    import json
    os.makedirs("logs", exist_ok=True)
    with open("logs/shapellm2blocks.json", "w", encoding="utf-8") as f:
        json.dump(raw_dict, f, indent=4, ensure_ascii=False)

    lines_list = []
    spans_list = []
    chars_list = []

    for block in raw_dict["blocks"]:
        if "lines" in block:
            lines_list += block["lines"]

    for line in lines_list:
        if "spans" in line:
            spans_list += line["spans"]

    for span in spans_list:
        if "chars" in span:
            chars_list += span["chars"]
    chars = []
    for ch in chars_list:
        chars.append(ch["c"])
        
    print("".join(chars))
    # print(page_2.get_text())

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="pymupdf test")
    parser.add_argument("--merge", action="store_true", help="Merge PDFs in the specified directory")
    parser.add_argument("--convert", action="store_true", help="Test EPUB to PDF conversion")
    parser.add_argument("--epub", action="store_true", help="Test search in EPUB")
    parser.add_argument("--rect", action="store_true", help="Test rect and pixmap")
    parser.add_argument(
        "--search", action="store_true", help="Test search in PDF"
    )
    parser.add_argument(
        "--cropbox", action="store_true", help="Test cropbox in PDF"
    )
    parser.add_argument(
        "--count", action="store_true", help="Test page counts in PDF"
    )
    parser.add_argument("--color", action="store_true", help="Test color in PDF")
    parser.add_argument(
        "--blocks", action="store_true", help="Test blocks in PDF"
    )
    
    args = parser.parse_args()
    # 如果没有提供参数，则使用默认路径
    print(args)
    if args.merge:
        test_merge_pdfs()
    elif args.convert:
        test_epub_to_pdf()
    elif args.epub:
        print("test search in epub")
 
        test_search_in_epub()
    elif args.rect:
        print("test rect")
        test_rect()
    elif args.search:
        print("test search")
        test_search()
    elif args.cropbox:
        print("test cropbox")
        test_cropbox()
    elif args.count:
        print("test page counts")
        test_page_counts()
    elif args.color:
        print("test color")
        test_color()
    elif args.blocks:
        print("test blocks")
        test_blocks()