import numpy as np
import random


def main():
    string = "Humpty Dumpty walks down the street."
    terms = ['mock', 'turtle', 'march', 'rabbit', 'hatter', 'dormouse', 'gryphon', 'mouse', 'hare', 'duchess', 'humpty',
             'knight', 'dumpty', 'looking-glass', 'tweedledum', 'unicorn', 'lion', 'gnat', 'sheep', 'kitten']

    print(calculate_term_doc_vector(string, terms))


def classify(string, terms, matrix):
    """Classifies a string either as Wonderland-string or Looking-Glass-string."""
    count_terms = matrix.shape[0]  # Anzahl Zeilen

    # calculate term-doc-vector of string
    term_doc_vector = calculate_term_doc_vector(terms, string)
    print(term_doc_vector)

    doc_alice = [matrix[i][0] for i in range(count_terms)]
    doc_looking_glass = [matrix[j][1] for j in range(count_terms)]

    angle_alice = cos_of_angle(doc_alice, term_doc_vector)
    angle_looking_glass = cos_of_angle(doc_looking_glass, term_doc_vector)

    if angle_alice > angle_looking_glass:
        print("Wonderland-string")
    if angle_looking_glass > angle_alice:
        print("Looking-Glass-string")
    else:
        random_number = random.uniform(1, 2)
        if random_number == 1:
            print("Wonderland-string")
        if random_number == 2:
            print("Looking-Glass-string")


def calculate_term_doc_vector(string_arr, terms):
    """Calculates the term document vector for a given string."""
    string_arr = string_arr.lower().split()
    anzahl_terms = len(terms)
    term_doc_vector = [0] * anzahl_terms

    for word in string_arr:
        for i in range(len(terms)):
            term = terms[i]
            if term == word:
                term_doc_vector[i] = term_doc_vector[i] + 1

    return term_doc_vector


def cos_of_angle(vector1, string_vec):
    """Calculates the cosine of the angle between two vectors."""
    dot_product = np.dot(vector1, string_vec)
    denominator = (np.linalg.norm(vector1, 2) * np.linalg.norm(string_vec, 2))

    if denominator != 0:  # Kann auch Null werden wenn der Term-Document-Vektor Null ist
        res = dot_product / denominator
        return res
    else:
        return 0


if __name__ == '__main__':
    main()
