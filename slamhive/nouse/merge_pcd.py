# todo 还要写一个在过程删除的才能用
import os

accept_size = 20000000 # 上限大概20多M

def merge_pcd_files(input_folder, output_file):

    input_pcd_file = []
    origin_total_size = 0
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".pcd") and file_name != "merged.pcd":
            file_path = os.path.join(input_folder, file_name)
            input_pcd_file.append(file_path)
            origin_total_size += os.path.getsize(file_path)
    # print(origin_total_size)

    input_pcd_file = sorted(input_pcd_file)

    fre = max(1, int(origin_total_size/accept_size))

    new_input = []

    for i in range(len(input_pcd_file)):
        if i%fre == 0:
            new_input.append(input_pcd_file[i])
    
    input_pcd_file = new_input
    


    # 遍历输入文件夹中的所有PCD文件
    with open(output_file, 'w') as outfile:
        # 首先计算出新的点云数量

#         # .PCD v0.7 - Point Cloud Data file format
# VERSION 0.7
# FIELDS x y z intensity
# SIZE 4 4 4 4
# TYPE F F F F
# COUNT 1 1 1 1
# WIDTH 11197
# HEIGHT 1
# VIEWPOINT 0 0 0 1 0 0 0
# POINTS 11197
# DATA ascii
        title_path = ""
        total_points_number = 0
        for file_path in input_pcd_file:
            title_path = file_path
            with open(file_path, 'r') as infile:
                for i in range(11):
                    line = infile.readline()
                    if i == 9:
                        print()
                        print(int(line.split(" ")[1]))
                        total_points_number += int(line.split(" ")[1])
        
        # 写入头信息
        with open(title_path, 'r') as infile:
            for i in range(11):
                lines = infile.readline()
                if i == 6: # width
                    outfile.write("WIDTH "+str(total_points_number)+"\n")
                elif i == 9:
                    outfile.write("POINTS "+str(total_points_number)+"\n")
                else:
                    outfile.write(lines)



        # 写入数据信息
        for file_path in input_pcd_file:

            # 加载PCD文件
            with open(file_path, 'r') as infile:
                lines = infile.readlines()
                # 查找每个文件中的数据起始位置
                data_start_index = lines.index('DATA ascii\n') + 1
                # 写入数据到输出文件
                outfile.writelines(lines[data_start_index:])

if __name__ == "__main__":
    input_folder = "/SLAM-Hive/slam_hive_algos/loam/slamhive/pcd"  # 输入文件夹路径
    output_file = "/SLAM-Hive/slam_hive_algos/loam/slamhive/pcd/merged.pcd"  # 输出文件路径

    merge_pcd_files(input_folder, output_file)
