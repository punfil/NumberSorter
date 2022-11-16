class Record:
    def __init__(self, a_probability=0, b_probability=1, probability_sum=1):
        self._a_probability = a_probability
        self._b_probability = b_probability
        self._probabilities_sum = probability_sum

    def calculate_product_of_probabilities(self):
        return self._a_probability + self._b_probability - self._probabilities_sum

    def __gt__(self, other):
        if self.calculate_product_of_probabilities() > other.calculate_product_of_probabilities():
            return True
        else:
            return False

    def __lt__(self, other):
        if self.calculate_product_of_probabilities() < other.calculate_product_of_probabilities():
            return True
        else:
            return False

    def __eq__(self, other):
        return self.calculate_product_of_probabilities() == other.calculate_product_of_probabilities

    def deserialize(self, record_loaded):
        elements = record_loaded.split(' ')
        self._a_probability = elements[0]
        self._b_probability = elements[1]
        self._probabilities_sum = elements[2]

    def serialize(self):
        return str(self._a_probability)+" "+str(self._b_probability)+" "+str(self._probabilities_sum)+"\n"

    @property
    def a_probability(self):
        return self._a_probability

    @a_probability.setter
    def a_probability(self, new_value):
        self._a_probability = new_value

    @property
    def b_probability(self):
        return self._b_probability

    @b_probability.setter
    def b_probability(self, new_value):
        self._b_probability = new_value

    @property
    def probabilities_sum(self):
        return self._probabilities_sum

    @probabilities_sum.setter
    def probabilities_sum(self, new_value):
        self._probabilities_sum = new_value
