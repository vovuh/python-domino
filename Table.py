class Table:
    def __init__(self):
        self._table = []

    def can_add_to_the_left(self, value):
        if len(self._table) == 0:
            return True
        _, value_right = value
        table_left, _ = self._table[0]
        return table_left == value_right

    def can_add_to_the_right(self, value):
        if len(self._table) == 0:
            return True
        value_left, _ = value
        _, table_right = self._table[-1]
        return table_right == value_left

    def add_to_the_left(self, value):
        assert self.can_add_to_the_left(value), 'Wrong move: %s can not be added to the left' % list(value)
        self._table.insert(0, value)

    def add_to_the_right(self, value):
        assert self.can_add_to_the_right(value), 'Wrong move: %s can not be added to the right' % list(value)
        self._table.append(value)

    def draw(self):
        # Example of a table
        # +---------------+
        # |[1:1][1:2][2:6]|
        # +---------------+

        width = 5 * len(self._table)
        border = '+' + '-' * width + '+'
        middle = ''
        for (left, right) in self._table:
            middle += '[%d:%d]' % (left, right)
        middle = '|' + middle + '|'
        return '\n'.join([border, middle, border])
