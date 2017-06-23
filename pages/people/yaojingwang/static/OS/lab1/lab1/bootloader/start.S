# 系统启动时，BIOS会完成初始化，然后将磁盘第一个512字节保存到物理内存0x00007C00
# 位置，然后设置%CS=0000h, %IP=7C00h

#include "asm.h"
# 从此开始是16位代码
.code16
.globl start
start:
    #real mode code here
loop:
    jmp loop


.code32
start32:
    #protection mode code here
loop32:
    jmp loop32


# GDT
.p2align 2                         # 对齐
    #GDT definition here
gdt:    #NULL
    .word    0,0
    .byte    0,0,0,0


gdtdesc:                           # GDT描述符
	.word   (gdtdesc - gdt - 1)    # GDT长度，留意地址运算
	.long   gdt                    # GDT地址

