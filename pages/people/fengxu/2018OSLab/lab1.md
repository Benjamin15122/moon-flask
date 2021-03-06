% Lab1系统引导
% 2018-3-12

# 1. 实验要求

本实验通过实现一个简单的引导程序，介绍系统启动的基本过程

## 1.1. 在实模式下实现一个Hello World程序

在实模式下在终端中打印`Hello, World!`

## 1.2. 在保护模式下实现一个Hello World程序

从实模式切换至保护模式，并在保护模式下在终端中打印`Hello, World!`

## 1.3. 在保护模式下加载磁盘中的Hello World程序运行

从实模式切换至保护模式，在保护模式下读取磁盘1号扇区中的Hello World程序至内存中的相应位置，跳转执行该Hello World程序，并在终端中打印`Hello, World!`

# 2. 相关资料

## 2.1. IA-32的存储管理

在IA-32下，CPU有两种工作模式：源于8086的实模式与源于80386的保护模式；8086为16位CPU，有16位的寄存器（Register），16位的数据总线（Data Bus），20位的地址总线（Address Bus），寻址能力为1MB；8086的访存地址由段（Segment）和偏移（Offset）两部分组成，物理地址的计算公式为

~~~~~~~~~~~~~~~~~~
Physical Address = Segment << 4 + Offset
~~~~~~~~~~~~~~~~~~

80386开始，Intel处理器步入32位CPU；80386有32位地址线，其寻址空间为$2^32=4$GB；为保证兼容性，实模式得以保留，PC启动时CPU工作在实模式，并由Bootloader迅速完成从实模式向保护模式的切换

在实模式下，16位寄存器通过Segment:Offset这种方式实现1MB的寻址能力；在保护模式下，虽然寄存器为32位，能够进行4GB空间的寻址，Segment:Offset这种寻址方式仍然被保留下来，其中Segment仍然由16位的段寄存器表示，称为段选择子（Selector）

在保护模式下，16位段寄存器的高13位存储着一个索引，该索引指向一个数据结构的表项，表项中定义了段的起始32位物理地址，段的界限，属性等内容；而这一数据结构就是Global Descriptor Table，即GDT，GDT中的一个表项称为段描述符；段描述符的结构如下图所示

~~~~~~~~~~~~~~~~~~
       DESCRIPTORS USED FOR APPLICATIONS CODE AND DATA SEGMENTS

 31                23                15                7               0
+-----------------+-+-+-+-+---------+-+-----+-+-----+-+-----------------+
|                 | | | |A|         | |     | |     | |                 |
|   BASE 31..24   |G|X|O|V| LIMIT   |P| DPL |1| TYPE|A|  BASE 23..16    | 4
|                 | | | |L| 19..16  | |     | |     | |                 |
|-----------------+-+-+-+-+---------+-+-----+-+-----+-+-----------------|
|                                   |                                   |
|        SEGMENT BASE 15..0         |       SEGMENT LIMIT 15..0         | 0
|                                   |                                   |
+-----------------+-----------------+-----------------+-----------------+

               DESCRIPTORS USED FOR SPECIAL SYSTEM SEGMENTS

 31                23                15                7               0
+-----------------+-+-+-+-+---------+-+-----+-+-------+-----------------+
|                 | | | |A|         | |     | |       |                 |
|   BASE 31..24   |G|X|O|V| LIMIT   |P| DPL |0|  TYPE |  BASE 23..16    | 4
|                 | | | |L| 19..16  | |     | |       |                 |
|-----------------+-+-+-+-+---------+-+-----+-+-------+-----------------|
|                                   |                                   |
|        SEGMENT BASE 15..0         |       SEGMENT LIMIT 15..0         | 0
|                                   |                                   |
+-----------------+-----------------+-----------------+-----------------+

          A      - ACCESSED
          AVL    - AVAILABLE FOR USE BY SYSTEMS PROGRAMMERS
          DPL    - DESCRIPTOR PRIVILEGE LEVEL
          G      - GRANULARITY
          P      - SEGMENT PRESENT
~~~~~~~~~~~~~~~~~~

为进入保护模式，需要在内存中开辟一块空间存放GDT表；80386提供了一个寄存器`GDTR`用来存放GDT的32位物理基地址以及表长界限；在将GDT设定在内存的某个位置后，可以通过`LDGT`指令将GDT的入口地址装入此寄存器

~~~~~~~~~~~~~~~~~~
          GDT REGISTER

                  15            0
                 +---------------+
                 |   IDT LIMIT   |
+----------------+---------------|
|            IDT BASE            |
+--------------------------------+
 31                             0
~~~~~~~~~~~~~~~~~~

由`GDTR`访问GDT是由段选择子来完成的；为访问一个段，需将段选择子存储入段寄存器，比如数据段选择子存储入`DS`，代码段选择子存储入`CS`；其数据结构如下

~~~~~~~~~~~~~~~~~~
 15                      4 3   0
+-------------------------+-+---+
|                         |T|   |
|           INDEX         | |RPL|
|                         |I|   |
+-------------------------+-+---+

 TI  - TABLE INDICATOR, 0 = GDT, 1 = LDT
 RPL - REQUESTOR'S PRIVILEGE LEVEL
~~~~~~~~~~~~~~~~~~

TI位表示该段选择子为全局段还是局部段，PRL表示该段选择子的特权等级，13位Index表示描述符表中的编号

Selector:Offset表示的逻辑地址可如下图所示转化为线性地址，倘若不采用分页机制，则该线性地址即物理地址

~~~~~~~~~~~~~~~~~~
         15              0    31                                   0
LOGICAL +----------------+   +-------------------------------------+
ADDRESS |    SELECTOR    |   |                OFFSET               |
        +---+---------+--+   +-------------------+-----------------+
     +------+         !                          |
     | DESCRIPTOR TABLE                          |
     |  +------------+                           |
     |  |            |                           |
     |  |            |                           |
     |  |            |                           |
     |  |            |                           |
     |  |------------|                           |
     |  |  SEGMENT   | BASE          +---+       |
     +->| DESCRIPTOR |-------------->| + |<------+
        |------------| ADDRESS       +-+-+
        |            |                 |
        +------------+                 |
                                       !
            LINEAR  +------------+-----------+--------------+
            ADDRESS |    DIR     |   PAGE    |    OFFSET    |
                    +------------+-----------+--------------+
~~~~~~~~~~~~~~~~~~

## 2.2. 系统启动

系统启动时，计算机工作在实模式下，其中`CS:IP`指向BIOS的第一条指令，即首先取得控制权的是BIOS，BIOS将检查各部分硬件是否工作正常，然后按照CMOS RAM中设置的启动设备查找顺序来寻找可启动设备

系统启动时，工作在实模式的BIOS程序将主引导扇区（Master Boot Record，0号柱面，0号磁头，0号扇区对应的扇区，512字节，末尾两字节为魔数`0x55`和`0xaa`）加载至内存`0x7c00`处（被加载的程序一般称为Bootloader），紧接着执行一条跳转指令，将`CS`设置为`0x0000`，`IP`设置为`0x7c00`，运行被装入的Bootloader

# 3. 解决思路

## 3.1. 实模式Hello World程序

通过陷入屏幕中断调用BIOS打印字符串`Hello, World!`

~~~~~~~~~~~~~~~~~~
movw $message, %ax
movw %ax, %bp
movw $13, %cx                           #打印的字符串长度
movw $0x1301, %ax                       #AH=0x13 打印字符串
movw $0x000c, %bx                       #BH=0x00 黑底 BL=0x0c 红字
movw $0x0000, %dx                       #在第0行0列开始打印
int $0x10                               #陷入0x10号中断

message:
       .string "Hello, World!"
~~~~~~~~~~~~~~~~~~

通过写显存打印字符`H`

~~~~~~~~~~~~~~~~~~
movl $((80*5+0)*2), %edi                #在第5行第0列打印
movb $0x0c, %ah                         #黑底红字
movb $72, %al                           #72为H的ASCII码
movw %ax, %gs:(%edi)                    #写显存
~~~~~~~~~~~~~~~~~~

## 3.2. 实模式切换保护模式

关闭中断，打开A20数据总线，加载`GDTR`，设置`CR0`的PE位（第0位）为`1b`，通过长跳转设置`CS`进入保护模式，初始化`DS`，`ES`，`FS`，`GS`，`SS`

这里设置了三个GDT表项，其中代码段与数据段的基地址都为`0x0`，视频段的基地址为`0xb8000`

~~~~~~~~~~~~~~~~~~
.code16
start:
        ...
        cli                             #关闭中断
        inb $0x92, %al                  #启动A20总线
        orb $0x02, %al
        outb %al, $0x92
        data32 addr32 lgdt gdtDesc      #加载GDTR
        movl %cr0, %eax                 #启动保护模式
        orb $0x01, %al
        movl %eax, %cr0
        data32 ljmp $0x08, $start32     #长跳转切换至保护模式

.code32
start32:
        ...                             #初始化DS ES FS GS SS 初始化栈顶指针ESP
        jmp bootMain                    #跳转至bootMain函数 定义于boot.c

gdt:
        .word 0,0                       #GDT第一个表项必须为空
        .byte 0,0,0,0

        .word 0xffff,0                  #代码段描述符
        .byte 0,0x9a,0xcf,0
        
        .word 0xffff,0                  #数据段描述符
        .byte 0,0x92,0xcf,0
        
        .word 0xffff,0x8000             #视频段描述符
        .byte 0x0b,0x92,0xcf,0
        ...

gdtDesc:
        .word (gdtDesc - gdt -1)
        .long gdt
~~~~~~~~~~~~~~~~~~

## 3.3. 加载磁盘中的程序并运行

由于中断关闭，无法通过陷入磁盘中断调用BIOS进行磁盘读取，本次实验提供的代码框架中实现了`readSec(void *dst, int offset)`这一接口（定义于`bootloader/boot.c`中），其通过读写（`in`，`out`指令）磁盘的相应端口（Port）来实现磁盘特定扇区的读取

通过上述接口读取磁盘MBR之后扇区中的程序至内存的特定位置并跳转执行（注意代码框架`app/Makefile`中设置的该Hello World程序入口地址）

# 4. 代码框架

本次实验提供一个示范代码框架

~~~~~~~~~~~~~~~~~~
+lab1
|---+bootloader
|   |---boot.h                          #磁盘I/O接口
|   |---boot.c                          #加载磁盘上的用户程序
|   |---start.s                         #引导程序
|   |---Makefile
|---+utils
|   |---genboot.pl                      #生成MBR
|---+app
|   |---app.s                           #用户程序
|   |---Makefile
|---Makefile
~~~~~~~~~~~~~~~~~~

# 5. 相关资源

* [BIOS中断表](BIOS中断表.xlsx)
* [AT&T汇编语法](AT&T汇编语言.ppt)

# 6. 作业提交

本次作业仅需提交保护模式下加载磁盘中的Hello World程序并运行的相关源码与报告

截止时间：2018-3-26 00:00:00
