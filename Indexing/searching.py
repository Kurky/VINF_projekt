import lucene
from tabulate import tabulate
from java.io import File
from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import BooleanQuery, BooleanClause, IndexSearcher, TermQuery
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

    top_docs = searcher.search(query, 1)

    result_docs = []
    for hit in top_docs.scoreDocs:
        doc = searcher.doc(hit.doc)
        result_docs.append({field.name(): doc.get(field.name()) for field in doc.getFields()})

    reader.close()
    return result_docs


def retrieve_player_id(index_dir, player_id):
    index_dir = SimpleFSDirectory(File(index_dir).toPath())
    reader = DirectoryReader.open(index_dir)
    searcher = IndexSearcher(reader)
    analyzer = StandardAnalyzer()

    query_parser = QueryParser("Player_ID", analyzer)
    query = query_parser.parse(f'Player_ID:"{player_id}"')

    top_docs = searcher.search(query, 30)

    result_docs = []
    for hit in top_docs.scoreDocs:
        doc = searcher.doc(hit.doc)
        result_docs.append({field.name(): doc.get(field.name()) for field in doc.getFields()})

    reader.close()
    return result_docs


def retrieve_players_by_country_position(index_dir, country, position):
    index_dir = SimpleFSDirectory(File(index_dir).toPath())
    reader = DirectoryReader.open(index_dir)
    searcher = IndexSearcher(reader)
    analyzer = StandardAnalyzer()

    query_parser = QueryParser("Position", analyzer)
    query = query_parser.parse(f'Country:"{country}" AND Position:"{position}"')

    top_docs = searcher.search(query, 1000)

    result_docs = []
    for hit in top_docs.scoreDocs:
        doc = searcher.doc(hit.doc)
        result_docs.append({field.name(): doc.get(field.name()) for field in doc.getFields()})

    reader.close()
    return result_docs


def searchPlayerInfoByName(index_folder, player_name_to_search):
    pleyer_id = 0
    results = retrieve_player_name(index_folder, player_name_to_search)
    if results:
        for result in results:
            pleyer_id = result['Player_ID']
            result.pop('Player_ID', None)
        return pleyer_id, results
    else:
        print(f"No results found for Player Name: {player_name_to_search}")
        return '', []


def searchPlayerSeasonsByPlayerId(index_folder, player_id_to_search, player_name):
    results = retrieve_player_id(index_folder, player_id_to_search)
    if results:
        for result in results:
            result.pop('Player_ID', None)
        return results
    else:
        print(f"No results found for Player ID: {player_id_to_search}")
        return []


def searchPlayerSeasonsByCountryAndPositions(index_folder, country, position):
    results = retrieve_players_by_country_position(index_folder, country, position)
    if results:
        for result in results:
            result.pop('Player_ID', None)
        return results
    else:
        print(f"No results found for Country: {country}, Position {position}")
        return []


def searchPlayerInfoAndSeasonsByName():
    index_folder = "indexPlayerInfo"
    player_name_to_search = input("Enter the player name: ")
    player_id, results_info = searchPlayerInfoByName(index_folder, player_name_to_search)
    print('Results for player: ', player_name_to_search)
    print(tabulate(results_info, headers='keys', tablefmt='fancy_grid'))
    index_folder = "indexPlayerSeasons"
    results = searchPlayerSeasonsByPlayerId(index_folder, player_id, player_name_to_search)
    print(tabulate(results, headers='keys', tablefmt='fancy_grid'))


def did_players_play_together(results_one, results_two):
    if results_one and results_two:
        pairs_one = {(entry['Season'], entry['Team']) for entry in results_one}
        pairs_two = {(entry['Season'], entry['Team']) for entry in results_two}
        common_pairs = pairs_one.intersection(pairs_two)

        return common_pairs
    else:
        return False


def whoScoredMostGoals():
    index_folder_info = "indexPlayerInfo"
    name_list = []
    print('type "end" to finish adding players.')
    while True:
        if name_list:
            print('List of players contain:', name_list)
        player_name_to_list = input("Enter name of player: ")
        if player_name_to_list == 'end':
            break
        else:
            name_list.append(player_name_to_list)
    results_list = []
    for player in name_list:
        player_id, results_info = searchPlayerInfoByName(index_folder_info, player)
        if results_info:
            results_list.append(results_info[0])
    results_list = sorted(results_list, key=lambda x: int(x['Goals']), reverse=True)
    max_table = max(results_list, key=lambda x: int(x['Goals']))
    print(f"Player with most goals is: {max_table['Player_Name']},Goals: {max_table['Goals']}")
    print(tabulate(results_list, headers='keys', tablefmt='fancy_grid'))


def twoPlayersPlayedTogether():
    index_folder_info = "indexPlayerInfo"
    index_folder_seasons = "indexPlayerSeasons"
    player_one_name_to_search = input("Enter name of first player: ")
    player_two_name_to_search = input("Enter name of second player: ")

    player_one_id, results_info_one = searchPlayerInfoByName(index_folder_info, player_one_name_to_search)
    results_one = searchPlayerSeasonsByPlayerId(index_folder_seasons, player_one_id, player_one_name_to_search)

    player_two_id, results_info_two = searchPlayerInfoByName(index_folder_info, player_two_name_to_search)
    results_two = searchPlayerSeasonsByPlayerId(index_folder_seasons, player_two_id, player_two_name_to_search)
    common_seasons = did_players_play_together(results_one, results_two)
    if common_seasons:
        print('Players played together in seasons:')
        print(tabulate(results_info_one, headers='keys', tablefmt='fancy_grid'))
        print(tabulate(results_info_two, headers='keys', tablefmt='fancy_grid'))
        print(tabulate(common_seasons, tablefmt='fancy_grid'))
    else:
        print('Players did not played together.')


def listOfPlayersCountryPosition():
    index_folder_info = "indexPlayerInfo"
    country = input("Enter Country: ")
    position = input("Enter Position: ")
    results = searchPlayerSeasonsByCountryAndPositions(index_folder_info, country, position)
    if results:
        print('List of players from specific country playing on specific position contains ', str(len(results)),
              'records')
        print(tabulate(results, headers='keys', tablefmt='fancy_grid'))


if __name__ == "__main__":
    while True:
        print('Enter 1 - Search player and his seasons by name')
        print('Enter 2 - Did two players played together')
        print('Enter 3 - Who from picked players scored most goals')
        print('Enter 4 - List of players from specific country in specific position')
        print('Enter anything else - End')
        option = input("Option number: ")
        if option == '1':
            searchPlayerInfoAndSeasonsByName()
        elif option == '2':
            twoPlayersPlayedTogether()
        elif option == '3':
            whoScoredMostGoals()
        elif option == '4':
            listOfPlayersCountryPosition()
        else:
            break
