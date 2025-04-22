from pathlib import Path
from constants import DATA_DIR_NAME
 
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader

def load_doc_using_langchain():
    loader = DirectoryLoader(path="data/",
                            glob="**/*.txt",  # recursive glob
                            loader_cls=TextLoader,
                            show_progress=True)
    docs = loader.load()
    return docs    


def format_documents(documents):
    seen = set()
    formatted_chunks = []

    for i, doc in enumerate(documents):
        content = doc.page_content.strip()
        if content not in seen:
            seen.add(content)
            formatted_chunks.append(f"\n🔹 **Chunk {i+1}**:\n{content}")

    return "\n".join(formatted_chunks)


def get_all_dirs(path: Path):
    return [p for p in path.iterdir() if p.is_dir()]

def get_all_text_files(folder: Path):
    return list(folder.rglob("*.txt"))

def load_data():
    data_path = Path(DATA_DIR_NAME)
    if not data_path.exists():
        raise FileNotFoundError(f"Path {data_path} does not exist.")

    all_dirs = get_all_dirs(data_path)
    all_texts = []

    for sub_dir in all_dirs:
        text_files = get_all_text_files(sub_dir)
        if not text_files:
            print(f"No text files found in {sub_dir}")
            continue
        with open(text_files[0], "r", encoding="utf-8") as f:
            all_texts.append(f.read())

    return all_texts

if __name__ == "__main__":
    data = load_doc_using_langchain()
    # print(data)
    print(f"Loaded {len(data)} documents.")