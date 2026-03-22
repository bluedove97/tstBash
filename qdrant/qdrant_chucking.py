import traceback

from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 문서 로드 (예시: PDF 파일)
# 실제 경로에 맞게 수정하세요
documents = []



# PDF 파일 로드
# pdf_path = "request.pdf"
# try:
#     loader = PyPDFLoader(pdf_path)
#     documents.extend(loader.load())
# except Exception as e:
#     print(f"Error loading PDF: {e}")

# 텍스트 파일 로드
# text_path = r"D:\Work\maf\qdrant\utf8_doc.txt"
# try:
#     #loader = TextLoader(text_path)
#     loader = TextLoader(file_path=text_path, encoding="utf-8")
#     documents.extend(loader.load())
# except Exception as e:
#     print(f"Error loading text file: {e}")
#     print(traceback.format_exc())


# CSV 파일 로드
csv_path = r"D:\Work\maf\qdrant\mock.csv"
try:
    loader = CSVLoader(
        file_path=csv_path,
        encoding="utf-8",
        csv_args={
            "delimiter": ","
        }
    )

    documents = loader.load()
    print(f"원본 document 개수: {len(documents)}")
except Exception as e:
    print(f"Error loading text file: {e}")
    print(traceback.format_exc())


# 문서 분할
text_splitter = RecursiveCharacterTextSplitter(
    # chunk_size=1000,
    # chunk_overlap=200
    chunk_size=500,
    chunk_overlap=100
)
texts = text_splitter.split_documents(documents)
print(f"분할된 문서 청크 수: {len(texts)}")

print("------------------------")
# for i, doc in enumerate(texts):
#     print(f"\n--- Chunk {i} ---")
#     print(doc.page_content)