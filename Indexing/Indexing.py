import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
import pandas as pd

lucene.initVM()
indexPath = File("index/").toPath()
indexDir = SimpleFSDirectory(indexPath)
writerConfig = IndexWriterConfig(StandardAnalyzer())
writer = IndexWriter(indexDir, writerConfig)


def indexPlayerInfo(df):
    for i, row in df.iterrows():
        doc = Document()
        for col in df.columns:
            doc.add(TextField(col, str(row[col]), TextField.Store.YES))
        writer.addDocument(doc)
        print(f"Indexed document {i + 1}")


def closeWriter():
    writer.close()


if __name__ == "__main__":
    player_info_file_path = '../data/cleanCsvFiles/playersInfo.csv'
    player_data = pd.read_csv(player_info_file_path)

    indexPlayerInfo(player_data)
    closeWriter()
