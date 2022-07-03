class Transport_Problem:
    def __init__(self, suppliers, stockers, costs):
        self.suppliers = suppliers
        self.stockers = stockers
        self.supply = {}
        for supplier in suppliers.keys():
            self.supply[supplier] = {"total": suppliers[supplier]}
            for stocker in stockers.keys():
                self.supply[supplier][stocker] = {"supply": 0, "cost": costs[supplier][stocker]}

    def generate_initial_solution(self):

        i = 0
        j = 0
        supplier_names = list(self.suppliers.keys())
        stocker_names = list(self.stockers.keys())
        while (j+i)<len(supplier_names)+len(stocker_names)-1:
            if self.stockers[stocker_names[i]] >= self.suppliers[supplier_names[j]]:
                self.supply[supplier_names[j]][stocker_names[i]]["supply"] = self.suppliers[supplier_names[j]]
                self.stockers[stocker_names[i]] -= self.suppliers[supplier_names[j]]
                j += 1
            else:
                self.supply[supplier_names[j]][stocker_names[i]]["supply"] = self.stockers[stocker_names[i]]
                self.suppliers[supplier_names[j]] -= self.stockers[stocker_names[i]]
                i += 1


    def cost(self):
        cost = 0

        suppliers = list(self.suppliers.keys())
        stockers = list(self.stockers.keys())
        for supplier in suppliers:
            for stocker in stockers:
                cost += self.supply[supplier][stocker]["supply"] * self.supply[supplier][stocker]["cost"]

        return cost

    def find_shadow_costs(self):
        shadow_costs_demand = {name: 0 for name in self.stockers.keys()}
        shadow_costs_supply = {name: 0 for name in self.suppliers.keys()}

        shadow_costs_supply[0] = 0
        for stocker in self.stockers.keys():
            for supplier in self.suppliers.keys():
                if self.supply[supplier][stocker]:
                    if shadow_costs_supply[supplier]:
                        shadow_costs_demand[stocker] = self.supply[supplier][stocker]["cost"] - shadow_costs_supply[supplier]
                    else:
                        shadow_costs_supply[supplier] = self.supply[supplier][stocker]["cost"] - shadow_costs_demand[stocker]


        self.shadow_demand = shadow_costs_demand
        self.shadow_supply = shadow_costs_supply


    def print(self, show_shadow_costs=False):
        to_print = ""
        if show_shadow_costs:
            to_print += "   "
            to_print += "  ".join([str(self.shadow_demand[key]) for key in self.shadow_demand.keys()])
            to_print += "\n"
            to_print += "  "

        to_print = "   "
        to_print += "  ".join([stocker for stocker in self.stockers.keys()])
        to_print += "\n"
        for supplier in self.suppliers.keys():
            if show_shadow_costs:
                to_print += f"{self.shadow_supply[supplier]}  "
            to_print += f"{supplier}  "
            for stocker in self.stockers.keys():
                if self.supply[supplier][stocker]["supply"]:
                    to_print += str(self.supply[supplier][stocker]['supply'])
                else:
                    to_print += "-"
                to_print += "  "
            to_print += "\n"

        print(to_print)


suppliers = {"A": 14, "B": 16, "C": 20}
stockers = {"W": 11, "X": 15, "Y": 14, "Z": 10}
costs = {
        "A": {"W": 180, "X": 110, "Y": 130, "Z": 290},
        "B": {"W": 190, "X": 250, "Y": 150, "Z": 280},
        "C": {"W": 240, "X": 270, "Y": 190, "Z": 120}
        }

solution = Transport_Problem(suppliers, stockers, costs)

solution.generate_initial_solution()
solution.find_shadow_costs()
solution.print(show_shadow_costs=True)
print(solution.cost())
