% Lab4进程同步
% 2018-5-14

# 1. 实验要求

本实验通过实现一个简单的生产者消费者程序，介绍基于信号量的进程同步机制

## 1.1. 实现`SEM_INIT`、`SEM_POST`、`SEM_WAIT`、`SEM_DESTROY`系统调用

实现`SEM_INIT`、`SEM_POST`、`SEM_WAIT`、`SEM_DESTROY`系统调用，并使用以下用户程序测试

~~~~~~~~~~~~~~~~~~
#include "lib.h"
#include "types.h"

int uEntry(void) {
	int i = 4;
	int ret = 0;
	int value = 2;

	sem_t sem;
	printf("Father Process: Semaphore Initializing.\n");
	ret = sem_init(&sem, value);
	if (ret == -1) {
		printf("Father Process: Semaphore Initializing Failed.\n");
		exit();
	}

	ret = fork();
	if (ret == 0) {
		while( i != 0) {
			i --;
			printf("Child Process: Semaphore Waiting.\n");
			sem_wait(&sem);
			printf("Child Process: In Critical Area.\n");
		}
		printf("Child Process: Semaphore Destroying.\n");
		sem_destroy(&sem);
		exit();
	}
	else if (ret != -1) {
		while( i != 0) {
			i --;
			printf("Father Process: Sleeping.\n");
			sleep(128);
			printf("Father Process: Semaphore Posting.\n");
			sem_post(&sem);
		}
		printf("Father Process: Semaphore Destroying.\n");
		sem_destroy(&sem);
		exit();
	}
	
	return 0;
}
~~~~~~~~~~~~~~~~~~

## 1.2. 实现键盘驱动（选做）

有需要的同学可以实现一个键盘驱动，并实现`GETCHAR`、`GETS`、`SCANF`等系统调用

# 2. 相关资料

## 2.1. 信号量机制

内核维护`Semaphore`这一数据结构，并提供`P`，`V`这一对原子操作，其中`W`用于阻塞进程自身在该信号量上，`R`用于释放一个阻塞在该信号量上的进程，其伪代码如下

~~~~~~~~~~~~~~~~~~
struct Semaphore {
	int value;
	...
};

typedef struct Semaphore Semaphore;

void P(Semaphore *s) {
	s->value --;
	if (s->value < 0)
		W(s);
}

void V(Semaphore *s) {
	s->value ++;
	if (s->value <= 0)
		R(s);
}
~~~~~~~~~~~~~~~~~~

### 2.1.1. `SEM_INIT`系统调用

`sem_init`系统调用用于初始化信号量，其中参数`value`用于指定信号量的初始值，初始化成功则返回`0`，指针`sem`指向初始化成功的信号量，否则返回`-1`

~~~~~~~~~~~~~~~~~~
int sem_init(sem_t *sem, uint32_t value);
~~~~~~~~~~~~~~~~~~

### 2.1.2. `SEM_POST`系统调用

`sem_post`系统调用对应信号量的`V`操作，其使得`sem`指向的信号量的`value`增一，若`value`取值不大于`0`，则释放一个阻塞在该信号量上进程（即将该进程设置为就绪态），若操作成功则返回`0`，否则返回`-1`

~~~~~~~~~~~~~~~~~~
int sem_post(sem_t *sem);
~~~~~~~~~~~~~~~~~~

### 2.1.3. `SEM_WAIT`系统调用

`sem_wait`系统调用对应信号量的`P`操作，其使得`sem`指向的信号量的`value`减一，若`value`取值小于`0`，则阻塞自身，否则进程继续执行，若操作成功则返回`0`，否则返回`-1`

~~~~~~~~~~~~~~~~~~
int sem_wait(sem_t *sem);
~~~~~~~~~~~~~~~~~~

### 2.1.4. `SEM_DESTROY`系统调用

`sem_destroy`系统调用用于销毁`sem`指向的信号量，销毁成功则返回`0`，否则返回`-1`，若尚有进程阻塞在该信号量上，可带来未知错误

~~~~~~~~~~~~~~~~~~
int sem_destroy(sem_t *sem);
~~~~~~~~~~~~~~~~~~

## 2.2. 键盘驱动

以下代码用于获取键盘扫描码，每个键的按下与释放都会分别产生一个键盘中断，并对应不同的扫描码；对于不同类型的键盘，其扫描码也不完全一致

~~~~~~~~~~~~~~~~~~
uint32_t getKeyCode() {
	uint32_t code = inByte(0x60);
	uint32_t val = inByte(0x61);
	outByte(0x61, val | 0x80);
	outByte(0x61, val);
	return code;
}
~~~~~~~~~~~~~~~~~~

# 3. 相关资源

* [US-QWERTY键盘扫描码](http://wiki.osdev.org/PS2_Keyboard)

# 4. 作业提交

截止时间：2018-5-28 00:00:00
