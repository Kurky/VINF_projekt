import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.search import IndexSearcher, TermQuery
from org.apache.lucene.store import MMapDirectory

# Initialize Java VM
lucene.initVM(vmargs=['-Djava.awt.headless=true'])

# Access the index directory
index_dir = Paths.get('index')
fs_dir = MMapDirectory(index_dir)

# Create an IndexSearcher
reader = DirectoryReader.open(fs_dir)
searcher = IndexSearcher(reader)

# Create a Term instance
term = Term('text', 'Lucene')

# Create a query to search the term 'Lucene'
query = TermQuery(term)

# Perform the search
hits = searcher.search(query, 10)  # Search for a maximum of 10 hits

# Output the results
print(f"Number of hits for 'Lucene': {hits.totalHits.value}")
for hit in hits.scoreDocs:
    doc_id = hit.doc
    document = searcher.doc(doc_id)
    print(f"Hit score: {hit.score}, Document: {document}")

# Close the reader
reader.close()
