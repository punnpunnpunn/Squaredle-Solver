"""Project 2
This file is Copyright (c) Oscar Heath, Max Djaya, Punpun Payapvattanavong, Aayush Karki"""


class Tree:
    """Tree Class
    Instance Attributes:
        root: the value of the root of this tree
        subtrees: a dictionary of values (str) to subtrees (Tree)
    Basically the same as the Tree class implemented in homework assignments, except that
    "sublists" is a dictionary from values of the root of the subtrees to the subtree Tree. This
    allows checking if an element is a value of a child of a Tree in constant time.
    """
    root: str
    # subtrees: dict[str: Tree] (it won't let me assign Tree as the value so I commented the line)

    def __init__(self, value: str) -> None:
        self.root = value
        self.subtrees = {}

    def get_subtrees(self) -> dict:
        """Returns subtrees"""
        return self.subtrees

    def add_string(self, string: str) -> None:
        """Adds a subtree to this Tree in the same manner is in ex2 (see report for more info)"""
        if string == '':
            self.subtrees["END"] = None
        elif string[0] not in self.subtrees:
            self.subtrees[string[0]] = Tree(string[0])
            self.subtrees[string[0]].add_string(string[1:])
        else:
            self.subtrees[string[0]].add_string(string[1:])


class Vertex:
    """One node of our Squaredle game
    Instance Attributes:
        value: the value of this node
        neighbours: adjacent verices to this vertex
    Representation Invariants:
        all(self in vertex.neighbours for vertex in self.neighbours)
    """
    value: str
    # neigbours: set[Vertex]

    def __init__(self, value: str) -> None:
        self.value = value
        self.neighbours = set()

    def add_edge(self, vertex) -> None:
        """Adds an edge between self and vertex"""
        if vertex in self.neighbours:
            return
        self.neighbours.add(vertex)
        vertex.neighbours.add(self)

    def __repr__(self) -> str:
        return self.value


class Squaredle:
    """Graph of our Squaredle game
    Instance Attributes:
        vertices: dictionary of tuples (x, y) indicating the position in the grid to the Vertex
        object in that square of the grid
        size: length of a side of the grid
        letters: set of all letters in the grid
    """
    vertices: dict[tuple: Vertex]
    size: int
    letters: set

    def __init__(self, grid: list[list[str]]) -> None:
        self.vertices = {}
        self.size = len(grid)
        self.letters = set()
        edges_to_add = {}
        for y in range(len(grid)): # This converts a nested list into a Squaredle (a graph)
            for x in range(len(grid[y])):
                self.vertices[(y, x)] = Vertex(grid[y][x])
                self.letters.add(grid[y][x])
                edges_to_add[(y, x)] = set()
                if x + 1 < len(grid[y]):
                    edges_to_add[(y, x)].add((y, x + 1))
                    if y + 1 < len(grid):
                        edges_to_add[(y, x)].add((y + 1, x + 1))
                    if y - 1 >= 0:
                        edges_to_add[(y, x)].add((y - 1, x + 1))
                if x - 1 >= 0:
                    edges_to_add[(y, x)].add((y, x - 1))
                    if y + 1 < len(grid):
                        edges_to_add[(y, x)].add((y + 1, x - 1))
                    if y - 1 >= 0:
                        edges_to_add[(y, x)].add((y - 1, x - 1))
                if y + 1 < len(grid):
                    edges_to_add[(y, x)].add((y + 1, x))
                if y - 1 >= 0:
                    edges_to_add[(y, x)].add((y - 1, x))

        for vertex in edges_to_add:
            for edge in edges_to_add[vertex]:
                self.vertices[vertex].add_edge(self.vertices[edge])

    def __repr__(self) -> str:
        grid = []
        for y in range(self.size):
            this_line = []
            for x in range(self.size):
                this_line.append(self.vertices[(y, x)].value)
            grid.append(' '.join(this_line))
        return '\n'.join(grid)


def make_squaredle(file: str) -> list[list[str]]:
    """Reads a txt file and converts it to a nested list"""
    grid = []
    with open(file, 'r') as letters:
        for row in letters:
            grid.append(row.split())
    return grid


def find_words(squaredle_graph, word_tree) -> set:
    """Takes in a squaredle graph and returns a set of all the words in it"""
    wordbank = []
    for letter in squaredle_graph.vertices.values():
        if letter.value != '#' and letter.value not in word_tree.subtrees:
            raise ValueError
        elif letter.value != '#':
            wordbank += find_words_with_start(letter.value, letter, squaredle_graph, word_tree.subtrees[letter.value], [letter])
    return set(wordbank)


def find_words_with_start(string: str, letter: Vertex, squaredle_graph: Squaredle, word_tree: Tree
                          , used_letters: list[Vertex]) -> list:
    """Recursively finds all the words that can be made starting at the Vertex letter"""
    wordlist = []
    if "END" in word_tree.subtrees:
        wordlist = [string]
    for l in letter.neighbours:
        if l not in used_letters and l.value in word_tree.subtrees:
            wordlist += find_words_with_start(string + l.value,
                                              l, squaredle_graph, word_tree.subtrees[l.value],
                                              used_letters + [l])
    return wordlist


def brute_force_find_words_with_start(string: str, letter: Vertex, squaredle_graph: Squaredle,
                                      words:set[str], used_letters: list[Vertex]) -> list:
    """Brute forces all the words in the squaredle starting in letter, checking every possible
    path from letter and seeing if it is a word in the dictionary"""
    wordlist = []
    if string in words:
        wordlist = [string]
    for l in letter.neighbours:
        if l not in used_letters:
            wordlist += brute_force_find_words_with_start(string + l.value, l, squaredle_graph, words, used_letters + [l])
    return wordlist


def brute_force(squaredle_graph: Squaredle, words: set[str]) -> set:
    """Brute forces all the words in the squaredle, checking every possible
    path from every letter and seeing if it is a word in the dictionary"""
    wordbank = []
    for letter in squaredle_graph.vertices.values():
        wordbank += brute_force_find_words_with_start(letter.value, letter, squaredle_graph, words, [letter])
    return set(wordbank)
