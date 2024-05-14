class Node:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)


def get_valid_node_name(prompt):
    while True:
        name = input(prompt)
        if name.strip() and name.isalpha():
            return name
        print("Invalid input! Node name must be a non-empty string of alphabetic characters.")


def get_valid_float(prompt, min_val=None, max_val=None):
    while True:
        value_str = input(prompt)
        try:
            value = float(value_str)
            if (min_val is None or value >= min_val) and (max_val is None or value <= max_val):
                return value
            print(f"Invalid input! Value must be a float between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def build_decision_tree():
    try:
        # Create root node
        root_name = get_valid_node_name("Enter the name for the root decision node: ")
        root = Node(root_name)

        # Create test market node
        test_market_name = get_valid_node_name("Enter the name for the test market node: ")
        test_market = Node(test_market_name)
        root.add_child(test_market)

        # Create abandon node
        abandon_name = get_valid_node_name("Enter the name for the abandon node: ")
        abandon = Node(abandon_name, 30000)  # Fixed value for abandoning the project
        root.add_child(abandon)

        # Create test market outcome nodes
        favorable_name = get_valid_node_name("Enter the name for the favorable outcome node: ")
        favorable_failure_prob = get_valid_float("Enter the probability of failure for the favorable outcome node (0-1): ", 0, 1)
        favorable_value = (1 - favorable_failure_prob) * 30000
        unfavorable_value = favorable_failure_prob * 30000
        favorable = Node(favorable_name, favorable_value)
        unfavorable = Node("Unfavorable", unfavorable_value)
        test_market.add_child(favorable)
        test_market.add_child(unfavorable)

        # Create production node
        production_name = get_valid_node_name("Enter the name for the production node: ")
        production = Node(production_name)
        favorable.add_child(production)

        # Create demand nodes
        demand_names = ["low", "medium", "high"]
        demand_nodes = []
        for name in demand_names:
            demand_prob = get_valid_float(f"Enter the probability of {name} demand node (0-1): ", 0, 1)
            value = favorable.value * demand_prob
            demand_node = Node(name, value)
            production.add_child(demand_node)
            demand_nodes.append(demand_node)

        return root
    except ValueError:
        print("Error: Value must be a valid number. Please try again.")
        return None


def calculate_expected_value(node):
    if not node.children:
        return node.value
    else:
        return sum(child.value for child in node.children)


def analyze_decision_tree(root):
    try:
        expected_value = calculate_expected_value(root)
        print(f"The expected value of the decision tree is: {expected_value}")

        best_option = None
        best_option_value = float('-inf')
        for child in root.children:
            child_value = calculate_expected_value(child)
            if child_value > best_option_value:
                best_option = child.name
                best_option_value = child_value

        print(f"The best option for the firm is: {best_option} with an expected value of {best_option_value}")
    except TypeError:
        print("Error: Decision tree is not properly constructed.")


def print_tree(node, level=0):
    indent = "    " * level
    value_str = f": value={node.value}" if node.value is not None else ""
    print(f"{indent}[{node.name}{value_str}]")
    for child in node.children:
        print_tree(child, level + 1)


if __name__ == "__main__":
    decision_tree = build_decision_tree()
    if decision_tree:
        print("\nDecision Tree:")
        print_tree(decision_tree)
        analyze_decision_tree(decision_tree)
