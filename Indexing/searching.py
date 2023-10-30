import lucene
from java.io import File
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer

lucene.initVM()


def retrieve_player_name(index_dir, player_name):
    index_dir = SimpleFSDirectory(File(index_dir).toPath())
    reader = DirectoryReader.open(index_dir)
    searcher = IndexSearcher(reader)
    analyzer = StandardAnalyzer()

    query_parser = QueryParser("Player_Name", analyzer)
    query = query_parser.parse(f'Player_Name:"{player_name}"')

    top_docs = searcher.search(query, 10)  # Search for top 10 documents matching the query

    result_docs = []
    for hit in top_docs.scoreDocs:
        doc = searcher.doc(hit.doc)
        result_docs.append({field.name(): doc.get(field.name()) for field in doc.getFields()})

    reader.close()
    return result_docs


if __name__ == "__main__":
    index_folder = "index"  # Path to the index folder
    player_name_to_search = "Jaromir Jagr"  # Player name to search for

    results = retrieve_player_name(index_folder, player_name_to_search)
    if results:
        print(f"Search Results for Player Name: {player_name_to_search}")
        for result in results:
            print(f"Player Name: {result['Player_Name']} - Country: {result['Country']}")
    else:
        print(f"No results found for Player Name: {player_name_to_search}")
