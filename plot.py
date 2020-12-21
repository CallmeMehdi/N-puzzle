from graphic import AnalysisGraph

print("1* Afficher le graphique de l'heuristique h1")
print("2* Afficher le graphique de l'heuristique h2")
choice = input()
if (choice=='1'):
    heuristic = 'h1'
else:
    heuristic = 'h2'

analysis_graph = AnalysisGraph(heuristic)

analysis_graph.done()