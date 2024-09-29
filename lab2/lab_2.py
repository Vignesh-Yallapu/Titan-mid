import heapq
from typing import List, Tuple

def preprocess_text(text: str) -> List[str]:
    # Tokenize into sentences and normalize
    sentences = text.lower().split('.')
    return [s.strip() for s in sentences if s.strip()]

def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

class State:
    def __init__(self, pos1: int, pos2: int, cost: int, path: List[Tuple[int, int]]):
        self.pos1 = pos1
        self.pos2 = pos2
        self.cost = cost
        self.path = path

    def __lt__(self, other):
        return self.cost < other.cost

def heuristic(state: State, doc1: List[str], doc2: List[str]) -> int:
    return max(len(doc1) - state.pos1, len(doc2) - state.pos2)

def a_star_alignment(doc1: List[str], doc2: List[str]) -> List[Tuple[int, int]]:
    initial_state = State(0, 0, 0, [])
    heap = [(0, initial_state)]
    visited = set()

    while heap:
        _, current_state = heapq.heappop(heap)
        if current_state.pos1 == len(doc1) and current_state.pos2 == len(doc2):
            return current_state.path
        if (current_state.pos1, current_state.pos2) in visited:
            continue
        visited.add((current_state.pos1, current_state.pos2))
        if current_state.pos1 < len(doc1) and current_state.pos2 < len(doc2):
            cost = levenshtein_distance(doc1[current_state.pos1], doc2[current_state.pos2])
            new_state = State(
                current_state.pos1 + 1,
                current_state.pos2 + 1,
                current_state.cost + cost,
                current_state.path + [(current_state.pos1, current_state.pos2)]
            )
            f = new_state.cost + heuristic(new_state, doc1, doc2)
            heapq.heappush(heap, (f, new_state))
        if current_state.pos1 < len(doc1):
            new_state = State(
                current_state.pos1 + 1,
                current_state.pos2,
                current_state.cost + len(doc1[current_state.pos1]),
                current_state.path
            )
            f = new_state.cost + heuristic(new_state, doc1, doc2)
            heapq.heappush(heap, (f, new_state))
        if current_state.pos2 < len(doc2):
            new_state = State(
                current_state.pos1,
                current_state.pos2 + 1,
                current_state.cost + len(doc2[current_state.pos2]),
                current_state.path
            )
            f = new_state.cost + heuristic(new_state, doc1, doc2)
            heapq.heappush(heap, (f, new_state))
    return [] 

def detect_plagiarism(doc1: str, doc2: str, threshold: float = 0.8) -> List[Tuple[str, str, float]]:
    sentences1 = preprocess_text(doc1)
    sentences2 = preprocess_text(doc2)
    alignment = a_star_alignment(sentences1, sentences2)
    plagiarism_instances = []

    for i, j in alignment:
        if i < len(sentences1) and j < len(sentences2):
            similarity = 1 - (levenshtein_distance(sentences1[i], sentences2[j]) / max(len(sentences1[i]), len(sentences2[j])))
            if similarity >= threshold:
                plagiarism_instances.append((sentences1[i], sentences2[j], similarity))
    return plagiarism_instances

def read_document(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def run_test_cases():
    # Test Case 1: Identical Documents
    doc1 = read_document('t1doc1.txt')
    doc2 = read_document('t1doc2.txt')
    result = detect_plagiarism(doc1, doc2)
    print("Test Case 1: Identical Documents\n")
    print(f"Number of plagiarized sentences: {len(result)}")
    print(f"Plagiarism instances: {result}\n")

    # Test Case 2: Slightly Modified Document
    doc1 = read_document('t2doc1.txt')
    doc2 = read_document('t2doc2.txt')
    result = detect_plagiarism(doc1, doc2, threshold=0.6)
    print("Test Case 2: Slightly Modified Document\n")
    print(f"Number of plagiarized sentences: {len(result)}")
    print(f"Plagiarism instances: {result}\n")

    # Test Case 3: Completely Different Documents
    doc1 = read_document('t3doc1.txt')
    doc2 = read_document('t3doc2.txt')
    result = detect_plagiarism(doc1, doc2)
    print("Test Case 3: Completely Different Documents\n")
    print(f"Number of plagiarized sentences: {len(result)}")
    print(f"Plagiarism instances: {result}\n")

    # Test Case 4: Partial Overlap
    doc1 = read_document('t4doc1.txt')
    doc2 = read_document('t4doc2.txt')
    result = detect_plagiarism(doc1, doc2, threshold=0.7)
    print("Test Case 4: Partial Overlap\n")
    print(f"Number of plagiarized sentences: {len(result)}")
    print(f"Plagiarism instances: {result}\n")

if __name__ == "__main__":
    run_test_cases()