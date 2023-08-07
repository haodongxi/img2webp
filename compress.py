from PIL import Image
import os

class CompressUtil:

    def compress(self,path,outPath,finish_callBack):
        check_result = self.check(path,outPath,finish_callBack)
        if check_result == False: 
            return
        name_list = []
        abs_path_list = []
        for files in os.listdir(path):
            if files.lower() == '.DS_Store'.lower():
                continue
            abs_files = os.path.join(path,files)
            if os.path.isfile(abs_files):
                ext = os.path.splitext(files)
                real_name = ext[0]+'.webp'
                im = Image.open(abs_files).convert('RGBA')
                im.save(os.path.join(outPath,real_name),'WEBP')
                name_list.append('- images/'+real_name+'\n')
                abs_path_list.append(abs_files)
        finish_callBack('',name_list,abs_path_list)


    def check(self,inputPath,outputPath,finish_callBack):
        inputPath = inputPath.replace("'",'')
        if os.path.exists(inputPath) != True:
            finish_callBack('现有的图片目录不存在')
            return False
        outputPath = outputPath.replace("'",'')
        if os.path.exists(outputPath) != True:
            finish_callBack('输出目录不存在')
            return False

        return True
            

