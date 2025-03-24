import random
from graphviz import Digraph

def generate_dag(n, m):
    adj = {i: [] for i in range(n)}
    
    nodes = list(range(n))
    random.shuffle(nodes)
    
    edges_added = 0
    while edges_added < m:
        u = random.choice(nodes)
        v = random.choice(nodes)
    
        if nodes.index(u) < nodes.index(v) and v not in adj[u]:
            adj[u].append(v)
            edges_added += 1
    
    return adj

def generate_test_case(n_node, n_edge, people):

    times = [random.randint(1, 100) for _ in range(n_node)]
    

    adj = generate_dag(n_node, n_edge)
    
    edges = []
    for u in adj:
        for v in adj[u]:
            edges.append(f"{u} {v}")

    test_case = f"{n_node} {n_edge} {people}\n"
    test_case += " ".join(map(str, times)) + "\n"
    test_case += "\n".join(edges)
    
    return test_case, adj

def write_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
    print(f"Test case written to '{filename}'")

def generate_and_save_test_cases():
    output_files = [
        "input01.txt",
        "input02.txt",
        "input03.txt",
        "input04.txt",
        "input05.txt",
        "input06.txt",
        "input07.txt",
        "input08.txt",
        "input09.txt",
        "input10.txt"
    ]

    for i, filename in enumerate(output_files):
        if i+1<=0 :
            n_node = random.randint(1, 100)
        elif i+1<=4 :
            n_node = random.randint(800, 1000)
        else:
            n_node = random.randint(1800, 2000)
            
        n_edge = random.randint(n_node+n_node//10, 10*n_node)
        people = random.randint(1, 30)

        test_case, adj = generate_test_case(n_node, n_edge, people)
        
        write_to_file("input/"+filename, test_case)
 
        # if i < 3:
        #     dot = Digraph()
        #     for u in adj:
        #         dot.node(str(u))
        #     for u in adj:
        #         for v in adj[u]:
        #             dot.edge(str(u), str(v))
        #     dot.render(f'dag_{i+1}', format='png', cleanup=True)
        #     print(f"DAG visualization saved as 'dag_{i+1}.png'")

generate_and_save_test_cases()