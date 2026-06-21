from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_text_splitter():

    return RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )


def chunk_text(text):

    splitter = get_text_splitter()

    return splitter.split_text(text)