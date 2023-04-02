import os
# 获取要重命名的pdf文件目录路径
pdf_dir = r"C:\Users\Lenovo\Desktop\csdn\英文论文资料\重命名"
# 切换到pdf文件目录
os.chdir(pdf_dir)
# 列出pdf文件列表
pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
#打印pdf文件列表print("pdf文件列表：")
for f in pdf_files:
    print(f)
    # 循环重命名pdf文件
for f in pdf_files:
    # 获取新文件名
    new_name = "Egyptian Informatics Journal Volume 22 " +f
    # 重命名文件
    os.rename(f, new_name)
print("pdf文件重命名完成！")
#input("请输入要重命名的pdf文件目录路径：")
#目录：C:\Users\Lenovo\Desktop\csdn\英文论文资料\重命名