import random
from collections import Counter
import numpy as np


def main():
    files = ["alice.txt", "looking-glass.txt"]
    terms = calculate_keywords("alice.txt", "looking-glass.txt")

    print("Keywords: ")
    print(terms)

    term_doc_matrix = calculate_term_doc_matrix(terms, files)

    print("\nTerm document matrix: ")
    print(np.array([list(x) for x in zip(*term_doc_matrix)]))

    string = "Humpty Dumpty walks down the street."
    print("\n We are classifying the string: " + string)

    term_doc_vector = calculate_term_doc_vector(terms, string)
    angles = calculate_angles(term_doc_matrix, term_doc_vector)
    file_index = choose_index(angles)

    print("\nDer Term-Dokument-Vector is: ")
    print(term_doc_vector)

    print(f"\nThe angle between the first column and the term-doc-vector is: {angles[0]}")
    print(f"The angle between the second column and the term-doc-vector is: {angles[1]}")

    print(f"\nThe angle number {file_index + 1} is the angle closest to 1.")

    if file_index == 0:
        print("Wonderland-string")
    else:
        print("Looking-Glass-string")

    print("\nNow we are classifying different substrings of different lengths.")
    results = classifying_rounds(terms, term_doc_matrix, files)
    print("\nResults: ")
    print("Percentages of correct classification for string from the alice.txt file:")
    print(results[0])
    print("\nPercentages of correct classification for string from the looking-glass.txt file:")
    print(results[1])


def calculate_keywords(file1, file2):
    """Calculates a set of keywords for file1 and file2."""
    file1 = open(file1, "r", encoding="UTF-8")
    file2 = open(file2, "r", encoding="UTF-8")

    words1 = file1.read().lower().split()
    words2 = file2.read().lower().split()

    counts1 = Counter(words1)
    counts2 = Counter(words2)

    unique1 = set(words1) - set(words2)
    unique2 = set(words2) - set(words1)

    # We only take the counts for the unique words
    counts_unique1 = []
    counts_unique2 = []

    for word, count in counts1.items():
        if word in unique1:
            counts_unique1.append((word, count))

    for word, count in counts2.items():
        if word in unique2:
            counts_unique2.append((word, count))

    # We are interested in the most common unique words

    most_common_unique1 = sorted(counts_unique1, key=lambda x: x[1], reverse=True)
    most_common_unique2 = sorted(counts_unique2, key=lambda x: x[1], reverse=True)

    # We are only interested in the words
    unique_words1 = []
    unique_words2 = []

    # We remove the special characters from the words
    special_chars = ["'", '"', '.', ',', '“', "’"]

    for word, count in most_common_unique1:
        if all(char not in word for char in special_chars):
            unique_words1.append(word)

    for word, count in most_common_unique2:
        if all(char not in word for char in special_chars):
            unique_words2.append(word)

    """ Our set of keywords is now the 10 most common unique words from alice.txt and the 10 most common unique words 
        from looking-glass.txt"""

    terms = unique_words1[:10] + unique_words2[:10]
    return terms


def calculate_term_doc_matrix(terms, files):
    """Calculates the term document matrix for the given files and terms."""
    result = []

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            file_content = f.read()
            file_content_lower = file_content.lower()
            keyword_counts = [file_content_lower.count(term.lower()) for term in terms]
            result.append(keyword_counts)

    return result


def classify(string, terms, matrix):
    """Classifies a string either as Wonderland-string or Looking-glass string."""
    term_document_vector = calculate_term_doc_vector(terms, string)
    angles = calculate_angles(matrix, term_document_vector)
    file_index = choose_index(angles)
    return file_index


def calculate_term_doc_vector(terms, string):
    """Calculates the term document vector for a given string and terms."""
    results = []

    for term in terms:
        input_lower = string.lower()
        keyword_count = input_lower.count(term.lower())
        results.append(keyword_count)

    return results


def calculate_angles(term_doc_matrix, term_doc_vector):
    """Calculates cosine of the angle of the columns of the matrix and the term document vector."""
    angles = []

    for i in range(len(term_doc_matrix)):
        # If the term-document-vector is the zero vector then it has angle 0.
        if all(element == 0 for element in term_doc_vector):
            angles.append(0)
            continue

        dot_product = np.dot(term_doc_vector, term_doc_matrix[i])
        norm1 = np.linalg.norm(term_doc_vector, 2)
        norm2 = np.linalg.norm(term_doc_matrix[i], 2)
        angle = dot_product / (norm1 * norm2)
        angles.append(angle)

    return angles


def choose_index(angles):
    """Returns the index of the angle which is closest to 1."""
    closest_index = None
    min_difference = float('inf')

    for i, value in enumerate(angles):
        difference = abs(value - 1)
        if difference < min_difference:
            min_difference = difference
            closest_index = i

    all_equal = all(value == angles[0] for value in angles)

    if all_equal:
        closest_index = random.randint(0, len(angles) - 1)

    return closest_index


def classifying_rounds(terms, matrix, files):
    """Classifies substrings of different lengths and returns two lists which contain the classification percentages of
       each file for different lengths."""
    full_results = []
    file_indicator = 0

    for file in files:
        results = []
        for i in range(20, 401, 20):
            correct_count = 0
            substrings = calculate_substrings(i, file)
            for substring in substrings:
                file_index = classify(substring, terms, matrix)
                if file_index == file_indicator:
                    correct_count += 1
            results.append(correct_count / len(substrings))
        file_indicator += 1
        full_results.append(results)

    return full_results


def calculate_substrings(n, filepath):
    """Calculates substring of length n from the given filepath."""
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read().lower()
        substrings = []

        for i in range(len(content) - n + 1):
            substrings.append(content[i:i+n])
        return substrings


if __name__ == "__main__":
    main()
