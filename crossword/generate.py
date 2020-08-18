import sys

from crossword import *
import time

start = time.time()

print(time.time() - start)

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.crossword.variables:
            unary= v.length
            dup= self.domains[v].copy()
            for x in dup:
                if len(x)!= unary:
                    self.domains[v].remove(x)
                


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        binary= self.crossword.overlaps[x, y]
        if binary== None:
            return False
        i, j= binary
        revised= False
        dupe= self.domains[x].copy()
        for v in self.domains[x]:
            found= False
            for w in self.domains[y]:
                if w[j]== v[i]:
                    found= True
                    break
            if found== False:
                dupe.remove(v)
                revised= True
        return (revised, dupe)

        raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue= []
        if arcs==None:
            over= self.crossword.overlaps
            for x in over:
                if over[x]!= None:
                    queue.append(x)#queue of (v1, v2) where v1 is a Variable
        else:
            queue= arcs.copy()
        while len(queue)!= 0:
            (x, y)= queue.pop(0)
            (boo, dupe)= self.revise(x, y)
            if boo:
                if len(dupe)== 0:
                    return False
                self.domains[x]= dupe.copy()
                for z in self.crossword.neighbors(x):
                    if z!= y:
                        queue.append((z, x))
        return True




        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        var= self.crossword.variables
        if len(assignment)!= len(var):
            return False
        return True
        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        words=[]
        ass= set()
        for x in assignment:
            ass.add(x)
            words.append(assignment[x])
        if len(words)!= len(set(words)):
            return False
    
        for x in assignment:
            if x.length != len(assignment[x]):
                return False
        
        for x in assignment:
            n= self.crossword.neighbors(x)
            for y in n:
                if y in ass:
                    i, j= self.crossword.overlaps[x, y]
                    if assignment[x][i] != assignment[y][j]:
                        return False
        return True

        
        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        li= []
        ass= set()
        for x in assignment:
            ass.add(x)
        n= self.crossword.neighbors(var)
        for val in self.domains[var]:
            count= 0
            for x in n:
                if x not in ass:
                    i, j= self.crossword.overlaps[var, x]
                    for dom in self.domains[x]:
                        if dom[j] != val[i]:
                            count+=1
            li.append((val, count))
        li= sorted(li, key = lambda x: x[1])
        s=[]
        for x,y in li:
            s.append(x)
        return s




        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        notass= set()#set of not assigned variables
        notass= self.crossword.variables- assignment.keys()
        li=[]
        for x in notass:
            li.append((x, len(self.domains[x])))
        li= sorted(li, key = lambda x: x[1])
        if len(li)== 1:
            return li[0][0]
        if li[0][1] != li[1][1]:
            return li[0][0]
        j=1
        v_max= li[0][0]
        n_max= len(self.crossword.neighbors(li[0][0]))
        while j<len(li) and li[j][1]== li[0][1]:
            if len(self.crossword.neighbors(li[j][0]))> n_max:
                n_max= len(self.crossword.neighbors(li[j][0]))
                v_max= li[j][0]
            j+=1
        return v_max
        return li[0][0]
                
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var= self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var]= value
            if self.consistent(assignment):
                n= self.crossword.neighbors(var)
                arcs= []
                for y in n:
                    arcs.append((y, var))
                inferences= self.ac3(arcs)
                if inferences== False:
                    del assignment[var]
                    continue
                result= self.backtrack(assignment)
                if result== False:
                    del assignment[var]
                else:
                    return result
            else:
                del assignment[var]
        return False
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
