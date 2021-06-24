

class Change:
    ########################
    ###      FIELDS      ###
    ########################

    def __init__(self, swap_or_shift, student1, student2, new_class):
        self.swap_or_shift = swap_or_shift
        self.student1 = student1
        self.student2 = student2
        self.new_class = new_class

    # Calculates how much a given swap or shift will affect utility
    # (Higher is better, lower is worse)
    def relative_utility():
        u = 0
        for s,c in student_assignments.items():
            u += self.preferences[s].index(c)
        return u

    # if a swap, will only look at student1 and student2
    # if a shift, will only look at student1 and new_class
    def change():
        return 0
