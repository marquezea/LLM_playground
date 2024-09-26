import streamlit as st
import utils as utils
import json
import chromadb
import uuid
from PyPDF2 import PdfReader
import pdfplumber
import datetime

def header():
    st.subheader("↗️ Vector DB")
    st.divider()

def add_to_collection(collection, document):
    docs = []
    docs.append('''Elvis Presley, often referred to as the "King of Rock and Roll," revolutionized the music scene in the 1950s with his unique blend of rock, country, and rhythm and blues.
                His charismatic stage presence, combined with his deep, soulful voice, made him an icon whose influence extended beyond music to fashion and culture.
                Songs like "Heartbreak Hotel" and "Jailhouse Rock" remain timeless classics, solidifying his place as one of the most significant cultural figures of the 20th century.''')

    docs.append('''Michael Jackson, known as the "King of Pop," was a musical genius whose career spanned decades, leaving an indelible mark on the entertainment industry.
                With his unmatched talent for singing, dancing, and songwriting, Jackson created groundbreaking albums like Thriller, which remains the best-selling album of all time.
                His innovative music videos, such as "Billie Jean" and "Beat It," set new standards for the medium, making him a global icon and a pioneer in pop culture.''')

    docs.append('''Freddie Mercury, the flamboyant and electrifying frontman of Queen, was a musical powerhouse known for his extraordinary vocal range and theatrical performances.
                Mercury's ability to blend rock with opera, as seen in the iconic song "Bohemian Rhapsody," showcased his creative brilliance and fearless approach to music.
                His dynamic stage presence and timeless hits like "We Will Rock You" and "Somebody to Love" continue to inspire generations of musicians and fans worldwide.''')

    docs.append('''Elton John, with his distinctive voice and flamboyant style, has been a monumental figure in the music industry for over five decades.
                Known for his incredible piano skills and heartfelt lyrics, often in collaboration with lyricist Bernie Taupin, Elton John has produced numerous hits such as "Rocket Man" and "Your Song."
                His ability to connect with audiences through his music, coupled with his extravagant stage costumes and performances, has made him a beloved and enduring figure in popular music.""")''')

    # Add docs to the collection. Can also update and delete. Row-based API coming soon!
    collection.add(
        documents=docs, # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
        metadatas=[
            {"genre": "rock"},
            {"genre": "pop"},
            {"genre": "rock"},
            {"genre": "pop"}
        ],
        ids=["elvis", "michael","mercury","elton"], # unique for each doc
    )

def add_doc_to_collection(collection, document):
    docs = [document['pages'][str(i+1)] for i in range(int(document['metadata']['pages']))]
    ids = [str(uuid.uuid4()) for i in document['pages']]
    meta = [{"filename": document['metadata']['filename'], 
             "last_modified": document['metadata']['last_modified'],
             "filetype": document['metadata']['filetype'],
             "page": str(i+1)} for i in range(int(document['metadata']['pages']))]
    collection.add(
        documents=docs,
        metadatas=meta,
        ids=ids
    )

def extractPDFText_pdfplumber(file):
    # variables to store the text into a single variable and into a document with pages
    raw_text = ""
    document = {"pages": {}, "metadata": {}}

    # load document with unstructuredPDFLoader
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            raw_text += text
            print(page.objects['image'])
            #print(text)
            break
        #print(raw_text)
    

    # # loop through the docs extracted from the PDF
    # for i, x in enumerate(docs):
    #     page_number = str(x.metadata.get('page_number', '0'))
    #     if page_number not in document['pages']:
    #         document['pages'][page_number] = ""
    #     if x.metadata['category'] != 'Footer': 
    #         document['pages'][page_number] += " " + x.page_content
    #         raw_text += " " + x.page_content

    # document['metadata']['filename'] = docs[0].metadata['filename']
    # document['metadata']['last_modified'] = docs[0].metadata['last_modified']
    # document['metadata']['filetype'] = docs[0].metadata['filetype']
    # document['metadata']['pages'] = page_number

    return raw_text, document

def extractPDFText_PyPDF2(file):
    # variables to store the text into a single variable and into a document with pages
    raw_text = ""
    document = {"pages": {}, "metadata": {}}

    # load document with unstructuredPDFLoader
    reader = PdfReader(file)

    # loop through the docs extracted from the PDF
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text
    
    # clean raw_text from duplicate characters
    for _ in range(5):
        raw_text = raw_text.replace(". . . ", ". ")
        raw_text = raw_text.replace("   ", " ")

    return raw_text, document

# setup applicaiton
utils.initialize()

# display header bar
header()

# setup Chroma DB persistent client
client = chromadb.PersistentClient(path="./chromadb/")

# get the collections available
collections = client.list_collections()

# display side bar
utils.display_sidebar(
    display_model=False,
    display_image_model=False,
    display_max_tokens=False, 
    display_temperature=False,
    display_resolution=False,
    display_quality=False,
    display_verbose=False,
    display_usage=False,
    display_voice=False,
    display_voice_speed=False,)

st.markdown("### PDF text extract")
uploadForm = st.form('Upload PDF', clear_on_submit=True)
pdfFile = uploadForm.file_uploader('Upload a PDF file', type=['pdf'])
if pdfFile is not None:
    pdf_text, document = extractPDFText_pdfplumber(pdfFile)
submit = uploadForm.form_submit_button('Upload')
st.write('final')


# st.markdown("### Collections")
# col1, col1b, col2, col3 = st.columns([2, 1, 2, 1], vertical_alignment="bottom")
# sel_collection_name = col1.selectbox("Collection", [collection.name for collection in collections])
# if col1b.button("Delete"):
#     client.delete_collection(sel_collection_name)
# new_collection_name = col2.text_input("Collection Name", "-")
# if col3.button("Add New"):
#     if new_collection_name.strip() != "":
#         new_collection = client.create_collection(new_collection_name)
#     else:
#         st.warning("Please enter a valid collection name!")
# # get the selected collection
# if sel_collection_name:
#     collection = client.get_collection(sel_collection_name)
#     st.caption(f"Chunks: :orange[{collection.count()}]")

# display document loader
# if st.button("Load Documents"):
#     file_paths = [
#         "./rag_source/prova_1_desafio_8_1ed (1).pdf"
#     ]

#     add_doc_to_collection(collection, document)

# query_text = st.text_area("Search query", "Que documento é este?")
# page = st.text_input("Page", "")
# if st.button("Query Vector DB"):
#     # Query/search 2 most similar results. You can also .get by id
#     results = collection.query(
#         query_texts=[query_text],
#         n_results=2,
#         where={"page": { "$eq": f"{page}"}}, # optional filter
#         # where_document={"$contains":"search_string"}  # optional filter
#     )

#     if results:
#         #print('============================================')
#         #print(results)
#         st.write(results['documents'][0])
#         #st.json(results['distances'][0])
#         #st.json(results['metadatas'][0])

