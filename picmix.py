from PIL import Image
import os
# ==========图片拼接===========
def picmix(root):
    if not os.path.exists('dl\\'+root):
        os.mkdir('dl\\'+root)
    # 遍历每一章的文件夹
    for dirs in os.listdir(root+'\\'):
        index=0
        ty=0
        tx=0
        # 遍历文件夹下的所有图片
        # 计算图片总长度
        for file in os.listdir(root+'\\'+dirs):
            fp=Image.open(root+'\\'+dirs+'\\'+str(index)+'.jpg')
            if fp.size[0]>tx:
                tx=fp.size[0]
            ty+=fp.size[1]
            index+=1
        index=0
        # 构造新图片
        result=Image.new('RGB',(tx,ty))
        yloc=0
        # 再次遍历 按顺序拼接
        for file in os.listdir(root+'\\'+dirs):
            fp=Image.open(root+'\\'+dirs+'\\'+str(index)+'.jpg')
            result.paste(fp,(0,yloc))
            yloc+=fp.size[1]
            
            index+=1
        # 写入硬盘
        try:
            result.save('dl\\'+root+'\\'+dirs+'.jpg','JPEG',quality=100)
        except:
            result.save('dl\\'+root+'\\'+dirs+'.jpg','PNG',quality=100)
        print('已合并'+dirs)

# ==========图片拼接===========

    