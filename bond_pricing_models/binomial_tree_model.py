"""
Author: Michael Drum, CFA
Email: mdrum29@gmail.com
LinkedIn: https://www.linkedin.com/in/michael-drum29/
Description: Prices a vanilla bond using a basic binomial interest rate tree.
"""

class TreeNode:
    max_level = 0
    def __init__(self, rate=None, parent=None, left=None, right=None, level=None, bond_value=None):
        self.rate = rate
        self.parent = parent
        self.left = left
        self.right = right
        self.level = level
        self.bond_value = bond_value
        if level > TreeNode.max_level:
            TreeNode.max_level = level

    def print_node(self, level=0):
        """
        Print information about the current level's nodes together without spacing.

        Args:
            level (int): Current level of the tree.
        """
        nodes_on_current_level = [self]

        while nodes_on_current_level:
            next_level_nodes = []
            for i, node in enumerate(nodes_on_current_level):
                print(f"{node.value:.4f}", end=" ")

                if node.left:
                    next_level_nodes.append(node.left)
                if node.right:
                    next_level_nodes.append(node.right)

            print()  # Move to the next line for the next level
            nodes_on_current_level = next_level_nodes
            level += 1


class Bond:
    def __init__(self, face_value: float, coupon_rate: float, frequency: int, maturity: int):
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.frequency = int(frequency) # in months
        self.maturity = int(maturity) # in months
        self.periods = int(maturity/frequency)

    def __str__(self):
        return f"Bond(face_value={self.face_value}, coupon_rate={self.coupon_rate}, " \
               f"frequency={self.frequency}, maturity={self.maturity}, periods={self.periods})"
    

def create_binomial_tree(r0: float, u: float, d: float, periods: int) -> TreeNode:
    """
    Creating a binomial interest rate tree.

    Args:
        r0 (float): Interest rate at time 0.
        u (float): Up move factor.
        d (float): Down move factor.
        periods (int): Number of periods. Use the same period as the bond.

    Returns:
        root_node (TreeNode): The root node of the binomial interest rate tree.
    """
    binomial_tree = []
    root_node = TreeNode(rate=r0, level=0)
    binomial_tree.append([root_node])
    current_level = [root_node]
    level = 1
    for i in range(1, periods + 1):
        next_level = []
        for j, node in enumerate(current_level):
            left_value = node.rate * u
            right_value = node.rate * d

            left_node = TreeNode(rate=left_value, parent=node, level=level)
            right_node = TreeNode(rate=right_value, parent=node, level=level)

            node.left = left_node
            node.right = right_node

            next_level.append(left_node)
            next_level.append(right_node)
            
        binomial_tree.append(next_level)
        current_level = next_level
        level += 1

    return binomial_tree

def price_bond_binomial_tree(bond: Bond, binomial_tree: [[TreeNode]], u_prob: float, d_prob: float) -> float:
    """
    Pricing the bond using a binomial interest rate tree.

    Args:
        bond (Bond obj): Bond object.
        binomial_tree (list(list(TreeNode))): The binomial interest rate tree.
        u_prob (float): Probability of an up move.
        d_prob (float): Probability of a down move.

    Returns:
        root_node (TreeNode): The root node of the binomial interest rate tree.
    """
    split = bond.frequency/12
    bond_cash_flows = [bond.coupon_rate*bond.face_value* split for _ in range(1,bond.periods+2)]
    bond_cash_flows[0] = 0


    for level in reversed(binomial_tree):
        max_level = binomial_tree[0][0].max_level
        for i, node in enumerate(level):
            if node.level == max_level:
                node.bond_value = bond_cash_flows[-1] + bond.face_value
            else:

                bond_value_hi = node.left.bond_value/(1+(node.rate*split))
                bond_value_lo = node.right.bond_value/(1+(node.rate*split))

                node.bond_value = bond_value_hi*u_prob + bond_value_lo*d_prob + list(reversed(bond_cash_flows))[max_level - node.level]
    return node.bond_value



if __name__ == "__main__":

    face_value= 100
    coupon_rate = .045
    frequency = 6 # in months
    maturity = 24 # in months

    r0 =.05
    u=1.05 # up move factor
    d=.95  # down move factor

    u_prob = .55 # probability of an up move
    d_prob = .45 # probability of a down move
   

    bond1 = Bond(face_value, coupon_rate, frequency, maturity)
    binomial_tree = create_binomial_tree(r0=r0, u=u, d=d, periods=bond1.periods)
    price = price_bond_binomial_tree(bond=bond1, binomial_tree=binomial_tree, u_prob=u_prob, d_prob=d_prob)

print(f"Bond Price: ${price:.2f}")



# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()
# print()


