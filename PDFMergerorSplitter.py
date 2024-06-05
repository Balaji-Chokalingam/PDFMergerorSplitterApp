import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

def merge_pdfs(pdf_paths, output_path):
    merger = PdfMerger()
    for pdf in pdf_paths:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()
    print(f"Merged PDF saved as '{output_path}'")

def split_pdf(input_pdf, mode, pages_or_range):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    rest_writer = PdfWriter()

    if mode == "pages":
        pages = pages_or_range
        for i in range(len(reader.pages)):
            if i in pages:
                writer.add_page(reader.pages[i])
            else:
                rest_writer.add_page(reader.pages[i])

    elif mode == "chapters":
        chapter, start_page, end_page = pages_or_range
        for i in range(len(reader.pages)):
            if start_page <= i <= end_page:
                writer.add_page(reader.pages[i])
            else:
                rest_writer.add_page(reader.pages[i])

    output_path = os.path.dirname(input_pdf)
    selected_output = os.path.join(output_path, "Selected.pdf")
    rest_output = os.path.join(output_path, "Rest.pdf")

    with open(selected_output, "wb") as f:
        writer.write(f)
    with open(rest_output, "wb") as f:
        rest_writer.write(f)

    print(f"Selected pages saved as '{selected_output}'")
    print(f"Rest of the pages saved as '{rest_output}'")

def get_pdf_paths(num_files):
    pdf_paths = []
    for _ in range(num_files):
        path = input("Enter the path to a PDF file: ")
        if os.path.exists(path) and path.endswith('.pdf'):
            pdf_paths.append(path)
        else:
            print("Invalid path or file type. Please enter a valid PDF file path.")
            return []
    return pdf_paths

def get_pages():
    pages = input("Enter the page numbers to extract, separated by commas (e.g., 0,2,4): ")
    return [int(p.strip()) for p in pages.split(',')]

def get_chapter_range():
    chapter = input("Enter the chapter name: ")
    start_page = int(input("Enter the start page number: "))
    end_page = int(input("Enter the end page number: "))
    return (chapter, start_page, end_page)

def main():
    choice = input("Do you want to merge or split PDFs? (merge/split): ").strip().lower()

    if choice == 'merge':
        num_files = int(input("How many files do you want to merge? "))
        pdf_paths = get_pdf_paths(num_files)
        if pdf_paths:
            output_path = input("Enter the output path for the merged PDF: ")
            if os.path.isdir(output_path):
                output_path = os.path.join(output_path, "Merged.pdf")
            merge_pdfs(pdf_paths, output_path)

    elif choice == 'split':
        input_pdf = input("Enter the path to the PDF to split: ")
        mode = input("Do you want to split by pages or chapters? (pages/chapters): ").strip().lower()

        if mode == 'pages':
            pages = get_pages()
            split_pdf(input_pdf, mode, pages)

        elif mode == 'chapters':
            chapter_range = get_chapter_range()
            split_pdf(input_pdf, mode, chapter_range)

        else:
            print("Invalid mode selected. Please choose 'pages' or 'chapters'.")

    else:
        print("Invalid choice. Please choose 'merge' or 'split'.")

if __name__ == "__main__":
    main()
