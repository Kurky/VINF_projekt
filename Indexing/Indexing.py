import os
from pathlib import Path

import lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader, IndexReader
from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.index import IndexOptions

# Initialize Java VM
lucene.initVM(vmargs=['-Djava.awt.headless=true'])

# Create or access the index directory
index_dir = Paths.get('index')
fs_dir = MMapDirectory(index_dir)

# Configuring the IndexWriter
analyzer = StandardAnalyzer()
config = IndexWriterConfig(analyzer)
writer = IndexWriter(fs_dir, config)

# Define field type
t1 = FieldType()
t1.setStored(True)
t1.setIndexOptions(IndexOptions.DOCS)

t2 = FieldType()
t2.setStored(False)
t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

# Add a document
doc = Document()
doc.add(Field('id', '418129481', t1))
doc.add(Field('title', 'Lucene in Action', t1))
doc.add(Field('text', 'Hello Lucene, This is the first document', t2))
writer.addDocument(doc)

# Commit the changes
writer.commit()

# Refresh the reader to see the updated documents
reader = DirectoryReader.open(fs_dir)
num_docs = reader.numDocs()
reader.close()  # Close the reader

print(f"{num_docs} docs found in index")
