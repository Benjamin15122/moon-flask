% Lab5文件系统
% 2017-6-2

# 1. 实验要求

本实验要求实现一个简单的文件系统

## 1.1. 格式化程序

编写一个格式化程序，按照文件系统的数据结构，构建磁盘文件（即`os.img`）

## 1.2. 内核

内核初始化时，按照文件系统的数据结构，读取磁盘，加载用户程序，并对`OPEN`、`READ`、`WRITE`、`LSEEK`、`CLOSE`、`REMOVE`这些系统调用提供相应接口

## 1.3. 用户程序

基于`OPEN`、`READ`等系统调用实现`LS`、`CAT`这两个函数，并使用以下用户程序测试

~~~~~~~~~~~~~~~~~~
#include "types.h"
#include "lib.h"

int uEntry(void) {
    int fd = 0;
    int i = 0;
    char tmp = 0;
    
    ls("/");                                   // 列出"/"目录下的所有文件
    ls("/boot/");                              // 列出"/boot/"目录下的所有文件
    ls("/dev/");                               // 列出"/dev/"目录下的所有文件
    ls("/usr/");                               // 列出"/usr/"目录下的所有文件
    
    printf("create /usr/test and write alphabets to it\n");
    fd = open("/usr/test", O_RDWR | O_CREAT);  // 创建文件"/usr/test"
    for (i = 0; i < 512; i ++) {               // 向"/usr/test"文件中写入字母表
    	tmp = (char)(i % 26 + 'A');
    	write(fd, (uint8_t*)&tmp, 1);
    }
    close(fd);
    ls("/usr/");                               // 列出"/usr/"目录下的所有文件
    cat("/usr/test");                          // 在终端中打印"/usr/test"文件的内容
    
    exit();
    return 0;
}
~~~~~~~~~~~~~~~~~~

# 2. 相关资料

内核使用FCB（File Control Block，文件控制块）这一数据结构对进程打开的文件进行管理，FCB中需要记录其对应的是哪个文件，该文件是以哪种方式打开的（读、写），该文件的读写偏移量

FCB的索引号称为文件描述符，每个进程的PCB中对其打开的文件的文件描述符进行记录

## 2.1. 文件系统操作接口

### 2.1.1. `OPEN`系统调用

`open`为Linux提供的系统原语，其用于打开（或创建）由路径`path`指定的文件，并返回文件描述符`fd`，`fd`为该文件对应的内核数据结构FCB的索引，参数`flags`用于对该文件的类型、访问控制进行设置

~~~~~~~~~~~~~~~~~~
int open(char *path, int flags);
~~~~~~~~~~~~~~~~~~

### 2.1.2. `READ`系统调用

`read`为Linux提供的系统原语，其用于从`fd`索引的FCB中的文件读写偏移量处开始，从文件中读取`size`个字节至从`buffer`开始的内存中，并返回成功读取的字节数，若文件支持seek操作，则同时修改该FCB中的文件读写偏移量

~~~~~~~~~~~~~~~~~~
int read(int fd, void *buffer, int size);
~~~~~~~~~~~~~~~~~~

### 2.1.3. `WRITE`系统调用

`write`为Linux提供的系统原语，其用于向`fd`索引的FCB中的文件读写偏移量处开始，向文件中写入从`buffer`开始的内存中的`size`个字节，并返回成功写入的字节数，若文件支持seek操作，则同时修改该FCB中的文件读写偏移量

~~~~~~~~~~~~~~~~~~
int write(int fd, void *buffer, int size);
~~~~~~~~~~~~~~~~~~

### 2.1.4. `LSEEK`系统调用

`lseek`为Linux提供的系统原语，其用于修改`fd`索引的FCB中的文件读写偏移量（若文件支持seek操作）

~~~~~~~~~~~~~~~~~~
int lseek(int fd, int offset, int whence);
~~~~~~~~~~~~~~~~~~

### 2.1.5. `CLOSE`系统调用

`close`为Linux提供的系统原语，其用于关闭由`fd`索引的FCB

~~~~~~~~~~~~~~~~~~
int close(int fd);
~~~~~~~~~~~~~~~~~~

### 2.1.6. `REMOVE`系统调用

`remove`为C标准库的函数，其用于删除`path`指定的文件

~~~~~~~~~~~~~~~~~~
int remove(char *path);
~~~~~~~~~~~~~~~~~~

## 2.2. 文件、目录、设备、管道、套接字、链接

对类Unix系统，其文件系统中除却真实存储在磁盘上的通常文件与目录这两种类型的文件外，将物理硬件本身、内核提供的功能等等，也作为文件归入文件系统之中，这些作为文件也都有inode与之对应

类Unix系统的文件系统通常将所有文件划分为通常文件（Regular File）、目录文件（Directory）、块设备文件（Block Device）、字符设备文件（Character Device）、管道文件（FIFO）、套接字文件（Socket）、链接文件（Symbolic Link）

其中，块设备文件与字符设备文件是按照存取方式进行的划分，前者例如`/dev/sda`、`/dev/loop0`，后者例如`/dev/tty1`、`/dev/random`，前者支持随机访存，后者仅支持顺序访存，一般看来，前者支持Seek操作，后者不支持Seek操作

对于设备文件同样可以按照其是否具有物理实体进行划分，即物理设备（对实际存在的物理硬件的抽象，例如`/dev/sda`）与虚拟设备（内核提供的功能，例如`/dev/loop0`）

类Unix系统将物理硬件设备与内核提供的功能作为文件归入文件系统是为统一用户操作接口，例如以下代码，通过向标准输出的设备文件中写入`Hello World!`，即可实现在当前终端中打印出该字符串

~~~~~~~~~~~~~~~~~~
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main (int argc, char *argv[]) {
	int fd = open("/dev/stdout", O_WRONLY);
	write(fd, (void*)"Hello World!\n", 13);
	close(fd);
	return 0;
}
~~~~~~~~~~~~~~~~~~

我们实现的简单文件系统中同样可以将物理硬件与内核提供的功能作为文件进行抽象，创建诸如`/dev/stdin`、`/dev/stdout`这些文件

## 2.3. 写磁盘扇区

以下代码用于写一个磁盘扇区

~~~~~~~~~~~~~~~~~~
static inline void outLong(uint16_t port, uint32_t data) {
	asm volatile("out %0, %1" : : "a"(data), "d"(port));
}

void writeSect(void *src, int offset) {
	int i;
	waitDisk();

	outByte(0x1F2, 1);
	outByte(0x1F3, offset);
	outByte(0x1F4, offset >> 8);
	outByte(0x1F5, offset >> 16);
	outByte(0x1F6, (offset >> 24) | 0xE0);
	outByte(0x1F7, 0x30);

	waitDisk();
	for (i = 0; i < SECTOR_SIZE / 4; i ++) {
		outLong(0x1F0, ((uint32_t *)src)[i]);
	}
}
~~~~~~~~~~~~~~~~~~

# 3. 解决思路

## 3.1. 磁盘文件布局

前4次实验中，用户程序放置在从201号扇区开始的磁盘文件中，内核初始化时需要从201号扇区顺序读取，实现对用户程序的加载；这次实验我们要求将用户程序存储入文件系统中，可供参考的磁盘文件的布局如下所示

~~~~~~~~~~~~~~~~~~
                                 Layout of Hard Disk
+--------------------+--------------------+-----------------------------------------+
|     Bootloader     |       Kernel       |               Filesystem                |
+--------------------+--------------------+-----------------------------------------+
      1 Sector             200 Sectors    |              Many Sectors               |
                                          |                                         |
+-----------------------------------------+                                         |
|                                                                                   |
|                                                                                   |
V                                Layout of Filesystem                               V
+--------------------+--------------------+--------------------+--------------------+
|    Block Group 0   |    Block Group 1   |        ...         |    Block Group N   |
+--------------------+--------------------+--------------------+--------------------+
|                    |
|                    |
|                    +--------------------------------------------------------------------------------+
|                                                                                                     |
|                                                                                                     |
V                                        Layout of Block Group 0                                      V
+----------------+----------------+----------------+----------------+----------------+----------------+
|   SuperBlock   | GroupDescTable |   InodeBitmap  |  BlockBitmap   |   InodeTable   |   DataBlocks   |
+----------------+----------------+----------------+----------------+----------------+----------------+
    1024 Bytes   |   Many Blocks  |    1 Block          1 Block     |   Many Blocks  |   Many Blocks
                 |                |                                 |                |
+----------------+                +------------+     +--------------+                +--------------+
|                                              |     |                                              |
|                                              |     |                                              |
V          Layout of GroupDescTable            V     V              Layout of InodeTable            V
+-------------+-------------+------------------+     +-------------+-------------+------------------+
| GroupDesc 0 | GroupDesc 1 |       ...        |     |   Inode 0   |   Inode 1   |        ...       |
+-------------+-------------+------------------+     +-------------+-------------+------------------+
~~~~~~~~~~~~~~~~~~

0号扇区仍为主引导扇区（MBR），1到200号扇区依旧存储内核程序，201号开始的扇区按照文件系统的数据结构进行格式化，用户程序也依照文件系统的数据结构写入其中

文件系统的布局仿照EXT4文件系统，将扇区划分为Block进行管理（例如连续两个扇区作为一个Block），连续的Block又进一步划分为Block Group

每个Block Group在头部为Meta Block，记录文件系统的元数据，依次包含Super Block、Group Descriptor Table、Inode Bitmap、Block Bitmap；Meta Block之后则为Inode Table以及真正存储通常文件以及目录文件的Data Block

Super Block中记录了整个文件系统的信息，例如总扇区数，Inode总数，Block总数，可用Inode数，可用Block数等

Group Descriptor Table中则记录了各个Block Group的信息，例如可用Inode数，可用Block数

Inode Bitmap以及Block Bitmap则分别用于对该Block Group中Inode Table以及Data Block的使用情况进行记录

## 3.2. 文件系统数据结构

以下为本次实验可供参考的文件系统数据结构

~~~~~~~~~~~~~~~~~~
union SuperBlock {
      uint8_t byte[SUPER_BLOCK_SIZE];
      struct {
             int32_t sectorNum;                   // 文件系统中扇区总数
             int32_t inodeNum;                    // 文件系统中inode总数
             int32_t blockNum;                    // 文件系统中data block总数
             int32_t availInodeNum;               // 文件系统中可用inode总数
             int32_t availBlockNum;               // 文件系统中可用data block总数
             int32_t blockSize;                   // 每个block所含字节数
             int32_t inodesPerGroup;              // 每个group所含inode数
             int32_t blocksPerGroup;              // 每个group所含data block数
      };
};

union GroupDesc {                                 // Group Descriptor Table的表项
      uint8_t byte[GROUP_DESC_SIZE];
      struct {
             int32_t inodeBitmap;                 // 该group中inodeBitmap的偏移量
             int32_t blockBitmap;                 // 该group中blockBitmap的偏移量
             int32_t inodeTable;                  // 该group中inodeTable的偏移量
             int32_t availInodeNum;               // 该group中可用inode总数
             int32_t availBlockNum;               // 该group中可用data block总数
      };
};

union Inode {                                     // Inode Table的表项
      uint8_t byte[INODE_SIZE];
      struct {
      	     int16_t type;                        // 该文件的类型、访存控制等
      	     int16_t linkCount;                   // 该文件的链接数
      	     int32_t blockCount;                  // 该文件的data block总数
      	     int32_t size;                        // 该文件所含字节数
      	     int32_t pointer[POINTER_NUM];        // data block偏移量
      	     int32_t singlyPointer;               // 一级data block偏移量索引
      	     int32_t doublyPointer;               // 二级data block偏移量索引
      	     int32_t triplyPointer;               // 三级data block偏移量索引
      };
};

union DirEntry {                                  // 目录文件的表项
      uint8_t byte[DIRENTRY_SIZE];
      struct {
             int32_t inode;                       // 该目录项对应的inode的偏移量
             char name[NAME_LENGTH];              // 该目录项对应的文件名
      };
};
~~~~~~~~~~~~~~~~~~

## 3.3. 文件系统目录结构

文件系统的目录结构如下所示，本次实验要求编写格式化程序对其进行构建

~~~~~~~~~~~~~~~~~~
+/
|---+boot
|   |---initrd        #用户态初始化程序
|   |---...
|---+dev
|   |---stdin         #标准输入设备文件
|   |---stdout        #标准输出设备文件
|   |---...
|---+usr
|   |---...           #用户文件
|---...
~~~~~~~~~~~~~~~~~~

其中`/boot/initrd`为用户态初始化程序（对应前4次实验的`uMain.elf`）

# 4. 相关资源

* [框架代码](lab05.zip)
* [EXT4文件系统](https://ext4.wiki.kernel.org/index.php/Ext4_Disk_Layout)

# 5. 作业提交

截止时间：2017-6-23 00:00:00
