#!/bin/bash

function number_of_lines {
        echo `cat $1 | sed -n '3,$p' | sed '/^\s*$/d' | wc -l`
}

for i in `ls C*xyz`;do
        filename1=$i
        file1=`echo "${filename1%%_aligned.*}"`
        ext1=`echo "${filename1#*.}"`
        for j in `ls T*xyz`;do
                filename2=$j
                file2=`echo "${filename2%%_aligned.*}"`
                ext2=`echo "${filename2#*.}"`
                filename=${file1}_${file2}
                sed -e "s/file/${filename}/g" gamess > ${filename}.sh
                filename=${filename}.inp
                xyzfile=${file1}_${file2}.xyz
                echo $filename
                cat testinp > ${filename}
                sed -n '3,$p' ${i} >> ${filename}
                sed -n '3,$p' ${i} > ${xyzfile}         
                sed -n '3,$p' ${j} >> ${filename}
                sed -n '3,$p' ${j} >> ${xyzfile}
                printf '$END\n\n' >> ${filename}
                lines1=`number_of_lines $i`
                lines2=`number_of_lines $j`
                sed -i "s/lines1,lines2/${lines1},${lines2}/g" ${filename}
        done
done

