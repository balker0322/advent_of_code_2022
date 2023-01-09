from copy import deepcopy

INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file=INPUT_FILE):
    with open(input_file, 'r') as file:
        for line in file:
            yield line.strip()

def parse_line(line):
    parsed_line = line.split(':')[-1]
    parsed_line = parsed_line.split('.')
    list_to_dict = lambda x: {
        'ore':x[0],
        'clay':x[1],
        'obsidian':x[2],
        'geode':x[3],
    }
    robot_cost = {}
    robot_cost['ore'] = list_to_dict([int(parsed_line[0].strip().split()[4]), 0, 0, 0])
    robot_cost['clay'] = list_to_dict([int(parsed_line[1].strip().split()[4]), 0, 0, 0])
    robot_cost['obsidian'] = list_to_dict([int(parsed_line[2].strip().split()[4]), int(parsed_line[2].strip().split()[7]), 0, 0])
    robot_cost['geode'] = list_to_dict([int(parsed_line[3].strip().split()[4]), 0, int(parsed_line[3].strip().split()[7]), 0])
    return robot_cost

class ItemInventory:

    def __init__(self, total_minute):
        self.total_minute = total_minute
        self.inventory = [0 for _ in range(total_minute)]
        self.accumulated_inventory = [0 for _ in range(total_minute)]
        self.creator_count = 0
        self.update_accumulated_inventory()

    def update_accumulated_inventory(self):
        running_sum = 0
        for i, value in enumerate(self.inventory):
            running_sum += value
            self.accumulated_inventory[i] = running_sum

    def add_creator(self, minute):
        self.creator_count += 1
        self.inventory[minute:] = [x+1 for x in self.inventory[minute:]]
        self.update_accumulated_inventory()

    def deduct(self, amount, minute):
        self.inventory[minute-1] -= amount
        self.update_accumulated_inventory()

    def get_inventory(self, minute):
        if minute <= 0:
            return 0
        return self.accumulated_inventory[minute-1]
    
    def get_next_spending_minute(self, previous_spend_minute, min_req):
        if min_req==0:
            return previous_spend_minute + 1
        result = [m for m in range(previous_spend_minute+1, self.total_minute+1) if self.get_inventory(m-1) >= min_req]
        if result:
            return max(result[0], previous_spend_minute+1)
        return self.total_minute+1

    def print_inventory(self):
        for i in range(self.total_minute):
            minute = i+1
            print(minute, self.get_inventory(minute))


class Inventory:

    def __init__(self, starting_robots, total_minutes, robot_prices):
        self.robot_prices = robot_prices
        self.robot_types = ['ore','clay','obsidian','geode']
        self.total_minutes = total_minutes
        self.inventory = {
            'ore' : ItemInventory(total_minutes),
            'clay' : ItemInventory(total_minutes),
            'obsidian' : ItemInventory(total_minutes),
            'geode' : ItemInventory(total_minutes),
        }
        self.item_type = ['ore','clay','obsidian','geode']
        self.last_minute_robot_added = 0
        self.robot_seq_list = []
        
        for robot in starting_robots:
            self.inventory[robot].add_creator(minute=0)
            self.robot_seq_list.append(robot)
    
    def can_afford(self, robot_price):
        for key, item in self.inventory.items():
            if item.get_inventory(self.total_minutes-1) < robot_price[key]:
                return False
        return True
    
    def add_robot(self, robot_type):
        minute = self.get_next_minute_to_add_robot(self.robot_prices[robot_type])
        if minute > self.total_minutes - 1:
            return False
        for key, item in self.inventory.items():
            item.deduct(self.robot_prices[robot_type][key], minute)
        self.inventory[robot_type].add_creator(minute)
        self.robot_seq_list.append(robot_type)
        self.last_minute_robot_added = minute
        return True
    
    def get_final_inventory(self, item_type):
        return self.inventory[item_type].get_inventory(self.total_minutes)
    
    def get_all_final_inventory(self):
        return {item_type:self.get_final_inventory(item_type) for item_type in self.item_type}

    def get_all_recent_inventory(self):
        func = lambda item_type: self.inventory[item_type].get_inventory(self.last_minute_robot_added+1)
        return {item_type:func(item_type) for item_type in self.item_type}
    
    def get_all_robot_counts(self):
        return {item_type:self.inventory[item_type].creator_count for item_type in self.item_type}
    
    def get_existing_robot_list(self):
        robot_counts = self.get_all_robot_counts()
        return [item_type for item_type, count in robot_counts.items() if count > 0]
    
    def get_inventory_status_id(self):
        # return '_'.join(self.robot_seq_list)
        id1 = self.get_all_recent_inventory()
        id1 = '_'.join([f'{key}_{value}' for key, value in id1.items()])
        id2 = self.get_all_robot_counts()
        id2 = '_'.join([f'{key}_{value}' for key, value in id2.items()])
        return f'{self.last_minute_robot_added+1}_{id1}_{id2}'

    def get_next_minute_to_add_robot(self, robot_price):
        func = lambda item, price: self.inventory[item].get_next_spending_minute(self.last_minute_robot_added, price)
        # print(robot_price, [func(item, price) for item, price in robot_price.items()], self.last_minute_robot_added)
        return max([func(item, price) for item, price in robot_price.items()])
    
    def print_all_inventory(self, minute):
        all_inv = [self.inventory[item_type].get_inventory(minute) for item_type in self.inventory.keys()]
        print(minute, all_inv)




def get_quality_level(
    target_item,
    total_minutes,
    robot_price,
    ):
    visited = set([])
    stack = []
    inv_dict = {}

    inv = Inventory(['ore'], total_minutes, dict(robot_price))
    inv_key = inv.get_inventory_status_id()
    inv_dict[inv_key] = inv
    stack.append(inv_key)

    max_score = 0

    max_item_per_minute_required = {}
    max_item_per_minute_required['ore'] = max([price['ore'] for _, price in robot_price.items()])
    max_item_per_minute_required['clay'] = max([price['clay'] for _, price in robot_price.items()])
    max_item_per_minute_required['obsidian'] = max([price['obsidian'] for _, price in robot_price.items()])

    while stack:

        current_inv_key = stack.pop()
        current_inv = inv_dict[current_inv_key]

        for item in ['ore', 'clay', 'obsidian', 'geode']:

            existing_robot_list = current_inv.get_existing_robot_list()

            if item=='geode' and 'obsidian' not in existing_robot_list:
                continue

            if item=='obsidian' and 'clay' not in existing_robot_list:
                continue
        
            new_inv = deepcopy(current_inv)
            if not new_inv.add_robot(item):
                continue
            
            new_inv_key = new_inv.get_inventory_status_id()

            if new_inv_key in visited:
                continue

            if new_inv_key in stack:
                continue

            remaining_minute = total_minutes - new_inv.last_minute_robot_added

            
            if new_inv.get_final_inventory('ore') > (remaining_minute+1)*max_item_per_minute_required['ore']:
                continue

            score = new_inv.get_final_inventory(target_item)

            b1 = score + sum([x for x in range(remaining_minute)])
            if b1 < max_score:
                continue
            
            b2 = score + sum([x for x in range(remaining_minute-1)])
            if b2 < max_score:
                temp_inv = deepcopy(new_inv)
                if not temp_inv.add_robot(target_item):
                    continue
                new_inv = deepcopy(temp_inv)
                new_inv_key = new_inv.get_inventory_status_id()
                score = new_inv.get_final_inventory(target_item)

            if score > max_score:
                max_score = score
                new_inv.robot_seq_list
                print(max_score, '->'.join(new_inv.robot_seq_list))

            stack.append(new_inv_key)
            inv_dict[new_inv_key] = new_inv

        visited.add(current_inv_key)
        del inv_dict[current_inv_key]

    return max_score


def main():

    robot_price_list = [parse_line(line) for line in iterate_input_file_lines()]
    target_item='geode'
    total_minutes = 24
    total = 0
    for i, robot_price in enumerate(robot_price_list):
        print(robot_price)
        ql = get_quality_level(target_item, total_minutes, robot_price)
        print(ql)
        total += ((i+1)*ql)
    
    print(total)
        

if __name__=='__main__':
    main()