from part1 import *


def main():
    robot_price_list = [parse_line(line) for line in iterate_input_file_lines()][:3]
    target_item='geode'
    total_minutes = 32
    total = 1
    for _, robot_price in enumerate(robot_price_list):
        print(robot_price)
        ql = get_quality_level(target_item, total_minutes, robot_price)
        print(ql)
        total *= ql
    
    print(total)
        

if __name__=='__main__':
    main()