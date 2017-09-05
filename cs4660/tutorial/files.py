"""Files tests simple file read related operations"""

class SimpleFile(object):
    """SimpleFile tests using file read api to do some simple math"""
    def __init__(self, file_path):
        self.numbers = []
        """
        TODO: reads the file by path and parse content into two
        dimension array (numbers)
        """
        file = open(file_path, "r")

        for line in file:
            self.numbers.append(line.split())

        file.close()

    def get_mean(self, line_number):
        """
        get_mean retrieves the mean value of the list by line_number (starts
        with zero)
        """
        sum = 0
        for number in self.numbers[line_number]:
            sum += int(number)

        return float(sum) / len(self.numbers[line_number])

    def get_max(self, line_number):
        """
        get_max retrieves the maximum value of the list by line_number (starts
        with zero)
        """
        return int(max(self.numbers[line_number]))

    def get_min(self, line_number):
        """
        get_min retrieves the minimum value of the list by line_number (starts
        with zero)
        """
        return int(min(self.numbers[line_number]))

    def get_sum(self, line_number):
        """
        get_sum retrieves the sumation of the list by line_number (starts with
        zero)
        """
        sum = 0
        for number in self.numbers[line_number]:
            sum += int(number)

        return sum
