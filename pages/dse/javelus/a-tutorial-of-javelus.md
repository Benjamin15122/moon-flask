title: A Tutorial of Javelus


# A Tutorial of Javelus

We will learn how to use Javelus to perform dynamic updating through this tutorial.
Before start, you may need to first learn how to build and install Javelus.


## Building Javelus

1. Download and build Javelus VM on [Windows](./build_windows) or [Linux](./build_linux).
2. Download and build the [developer interface](https://bitbucket.org/javelus/developer-interface).
3. Download and build the [dynamic patch generator](https://bitbucket.org/javelus/dpg).
    * We provide a script (`run.sh`) to facilitate invoking `dpg`, which is located at `dpg/dist/`.
4. Download and unzip [tutorial.zip](./tutorial.zip)

Now we assume that your fold layout is the same as follows.


```
javelus-tutorial/
├── developer-interface
├── dpg
├── javelus
└── tutorial
    ├── new
    ├── old
    └── transformer
```

## Quick Run

The `tutorial.zip` contains all files that are required to invoke a dynamic update.

First, check the output of the old version.


```
cd tutorial/
../javelus/build/linux/linux_amd64_compiler2/fastdebug/hotspot -cp old/ Main
```


!!! note
    The dynamic updating will not be triggered without a dynamic patch.


The output will tell you that Javelus cannot find a dynamic patch.

```
Version 1: Add listener SshFutureListener@2a139a55
Version 1: Add listener SshFutureListener@15db9742
Version 1: Add listener SshFutureListener@6d06d69c
Version 1: first=SshFutureListener@2a139a55, others=[SshFutureListener@15db9742, SshFutureListener@6d06d69c]
[DSU]-[Warn]: Please set org.javelus.dynamicPatch=/path/to/dynamic/patch!
Version 1: first=SshFutureListener@2a139a55, others=[SshFutureListener@15db9742, SshFutureListener@6d06d69c]
Version 1: Remove listener SshFutureListener@2a139a55
Version 1: Remove listener SshFutureListener@15db9742
Version 1: Remove listener SshFutureListener@6d06d69c
Version 1: Add listener SshFutureListener@2a139a55
Version 1: Add listener SshFutureListener@15db9742
Version 1: Add listener SshFutureListener@6d06d69c
Version 1: first=SshFutureListener@2a139a55, others=[SshFutureListener@15db9742, SshFutureListener@6d06d69c]
```


Now you can invoke the program by specifying the dynamic patch via `-Dorg.javelus.dynamicPatch=javelus.dsu`

```
cd tutorial/
../javelus/build/linux/linux_amd64_compiler2/fastdebug/hotspot -cp old/ -Dorg.javelus.dynamicPatch=javelus.dsu Main
```

!!! note
    To locate your `javelus` launcher,
    Linux users search for a script named `hotspot` in the build directory and
    Windows users search for an exe file named `hospot.exe` in the build directory.

Then you will get the following output.

```
Version 1: Add listener SshFutureListener@2a139a55
Version 1: Add listener SshFutureListener@15db9742
Version 1: Add listener SshFutureListener@6d06d69c
Version 1: first=SshFutureListener@2a139a55, others=[SshFutureListener@15db9742, SshFutureListener@6d06d69c]
[DSU]-[Info]: At safe point, the update will be performed.
[DSU]-[Info]: DSU request pausing time: 0.0000954 (s).
[DSU]-[Info]: DSU request finished at Thu Feb  1 01:30:49 2018
[DSU]-[Info]: DSU Request is finished
Version 2: listeners=[SshFutureListener@2a139a55, SshFutureListener@15db9742, SshFutureListener@6d06d69c]
Version 2: Remove listener SshFutureListener@2a139a55
Version 2: Remove listener SshFutureListener@15db9742
Version 2: Remove listener SshFutureListener@6d06d69c
Version 2: Add listener SshFutureListener@2a139a55
Version 2: Add listener SshFutureListener@15db9742
Version 2: Add listener SshFutureListener@6d06d69c
Version 2: listeners=[null, null, null, SshFutureListener@2a139a55, SshFutureListener@15db9742, SshFutureListener@6d06d69c]```
```


## Intro

We need to update a class `DefaultSshFuture` from [Apache SSHD](https://mina.apache.org/sshd-project/).
[This update](https://github.com/apache/mina-sshd/commit/b98694d7501fd0c9feae9747fd7abf849206f254#diff-75e0c23f54199169b53f78bbc31d9885) tries to make the implementation more lightweight.
We simplify the original implementation to the following classes.

The program contains three classes:

* `DefaultSshFuture`: the only changed classes.
* `SshFutureListener`:
* `Main`: the entry point of the test program.

### Old Version of `DefaultSshFuture`

The old version of `DefaultSshFuture` uses a field `firstListener` to store the first listener and a field `otherListeners` for the other listeners.
This implementation is memory-consuming. Programmers then make a new light-weight implementation.

```
import java.util.ArrayList;
import java.util.List;

public class DefaultSshFuture {

    private SshFutureListener firstListener;
    private List<SshFutureListener> otherListeners;

    public void addListener(SshFutureListener listener) {
        System.out.println("Version 1: Add listener " + listener);
        if (firstListener == null) {
            firstListener = listener;
        } else {
            if (otherListeners == null) {
                otherListeners = new ArrayList<SshFutureListener>(1);
            }
            otherListeners.add(listener);
        }
    }

    public void removeListener(SshFutureListener listener) {
        System.out.println("Version 1: Remove listener " + listener);
        if (listener == firstListener) {
            if (otherListeners != null && !otherListeners.isEmpty()) {
                firstListener = otherListeners.remove(0);
            } else {
                firstListener = null;
            }
        } else if (otherListeners != null) {
            otherListeners.remove(listener);
        }
    }

    public String toString() {
        return "Version 1: first=" + firstListener +  ", others=" + otherListeners;
    }
}
```

### New Version

The new version of `DefaultSshFuture` uses a single field `listeners` for all cases.
If there is only one listener, the listener is referenced by the field `listeners`.
If there are more, all listeners are stored in to an array referenced by the field `listener`.
Programmers make use Reflection API to implement all cases.


```
import java.lang.reflect.Array;
import java.util.Arrays;

public class DefaultSshFuture {

    private Object listeners;

    public void addListener(SshFutureListener listener) {
        System.out.println("Version 2: Add listener " + listener);
        if (listeners == null) {
            listeners = listener;
        } else if (listeners instanceof SshFutureListener) {
            listeners = new Object[] { listeners, listener };
        } else {
            Object[] ol = (Object[]) listeners;
            int l = ol.length;
            Object[] nl = new Object[l + 1];
            System.arraycopy(ol, 0, nl, 0, l);
            nl[l] = listener;
            listeners = nl;
        }
    }

    public void removeListener(SshFutureListener listener) {
        System.out.println("Version 2: Remove listener " + listener);
        if (listeners != null) {
            if (listeners == listener) {
                listeners = null;
            } else {
                int l = Array.getLength(listeners);
                for (int i = 0; i < l; i++) {
                    if (Array.get(listeners, i) == listener) {
                        Array.set(listeners, i, null);
                        break;
                    }
                }
            }
        }
    }

    public String toString() {
        if (listeners instanceof Object[]) {
            return "Version 2: listeners=" + Arrays.asList((Object[])listeners);
        }
        return "Version 2: listeners=" + listeners;
    }
}
```

### `Main`


Class `Main` is a test case used for demonstration.

```
public class Main {

    public static void main(String[] args) {
        DefaultSshFuture object = new DefaultSshFuture();
        SshFutureListener l1 = new SshFutureListener();
        SshFutureListener l2 = new SshFutureListener();
        SshFutureListener l3 = new SshFutureListener();
        object.addListener(l1);
        object.addListener(l2);
        object.addListener(l3);
        System.out.println(object);

        org.javelus.DeveloperInterface.invokeDSU();

        System.out.println(object);
        object.removeListener(l1);
        object.removeListener(l2);
        object.removeListener(l3);
        object.addListener(l1);
        object.addListener(l2);
        object.addListener(l3);
        System.out.println(object);
    }
}
```

Note that to invoke DSU, we here manually insert a call to `org.javelus.DeveloperInterface.invokeDSU` directly in the program.
In real scenarios, programmers can use other methods to invoke DSU without modifying their programs.

To build the two versions, you need to include `developer-interface.jar` in your classpath.

```
cd tutorial/
javac -cp ../developer-interface/developer-interface.jar old/*.java
javac -cp ../developer-interface/developer-interface.jar new/*.java
```

## Preparing Dynamic Software Updating

Before invoking DSU, we should finish the following three tasks.

1. Generate the dynamic patch
2. Program transformers
3. Merge transformers

The following commands are mostly invoked in directory `javelus-tutorial/tutorial`.

### Generating Dynamic Patch


Javelus provides a tool named `dpg` to generate a dynamic patch from Java bytecode binaries of two versions of a program.


```
Usage: DynamicPatchGenerator -o old-file -n new-file [-d output-directory]
   or: DynamicPatchGenerator -t template-class-path -m transformer-name
	-o old-file
	-n new-file
	-d output directory (default: .)
	-g generate template classes (default: off)
	-t transformer class path (default: off)
	-m transformer name (default: JavelusTransformers)
	-x output xml (default: off)
	-u gui version
```

To generate a dynamic patch, simply use the following command.

```
cd tutorial/
../dpg/dist/run.sh -o old/ -n new/ -g
```

You will find two generated files for this update: a manifest file `javelus.dsu` and a transformer template class `DefaultSshFuture.java`.

A dynamic patch includes two types of files:

1. `javelus.dsu`: the manifest file, which is a list of commands.
    * `classpath <path>`: Each `classpath` command adds a path for searching for new version of modified classes, added classes, and the transformer class.
    * `modclass <class-name>`: Each `modclass` command adds a modified class.
    * `addclass <class-name>`: Each `addclass` command adds an added new class.
    * `delclass <class-name>`: Each `delclass` command adds a deleted old class.
    * `transformer  <class-name>`: A `transformer` is optional and specifies the helper class used to loading transformers.

    !!! note
        A manifest file futher requires that:

        * There must be at most one `transformer` command.
        * `classpath` commands should be put at the beginning.
        * `modclass` and `addclass` of super classes should be put before commands of any child classes.

2. A set of *transformer template* classes, each of which corresponds to a type-changed modified class.

    !!! note
        Javelus allows programmers to develop transformer for each type-changed classes separatedly and then use `dpg` to merge them into a single class to facilitate Javelus invoking them at runtime.

The content of `javelus.dsu` is shown as follows.

```
classpath new/
modclass DefaultSshFuture
```

The following class is the template class that is used to program transformers for `DefaultSshFuture`.
Fields in the old classes are passed into the transformer as arguments, which are also decorated with annotations (`@OldField`).

```
import org.javelus.*;

public class DefaultSshFuture {
    private java.lang.Object listeners;
    public void updateObject(
            @OldField(clazz="DefaultSshFuture", name="firstListener",signature="LSshFutureListener;")
            SshFutureListener firstListener,
            @OldField(clazz="DefaultSshFuture", name="otherListeners",signature="Ljava/util/List;")
            java.util.List otherListeners){
        //new fields has already been initialized with default value
        //this.listeners = null;
    }
}
```

The default transformation leaves the new field `listeners` to null.
We need to fill method `updateObject` to add our own transformation.

### Writing Transformer

```
import java.util.ArrayList;
import java.util.List;

import org.javelus.OldField;

public class DefaultSshFuture {

    private Object listeners;

    public void updateObject(
            @OldField(clazz="DefaultSshFuture", name="firstListener",signature="LSshFutureListener;")
            SshFutureListener firstListener,
            @OldField(clazz="DefaultSshFuture", name="otherListeners",signature="Ljava/util/List;")
            java.util.List otherListeners){

        if (firstListener != null) {
            listeners = firstListener;
            if (otherListeners != null) {
                int size = otherListeners.size();
                Object[] array = new Object[size + 1]; // include the firstListener
                array[0] = firstListener;
                for (int i = 0; i < size; i++) {
                    array[i + 1] = otherListeners.get(i);
                }
                listeners = array;
            }
        }
    }
}
```

To build the transformer,
you need to include develpoer interface in your class path.

```
cd tutorial/
javac -cp ../developer-interface/developer-interface.jar:./old/ transformer/DefaultSshFuture.java
```

### Merging Transformers

We need to use `dpg` to merge transformers in all template classes into a single class.

```
cd tutorial/
../dpg/dist/run.sh -t transformer/
```

After that you will find a `JavelusTransformer.class`

You need to update your `javelus.dsu` to specify the path to look for the transformer class and the name of the of the transformer class.

```
classpath new/
classpath .
modclass DefaultSshFuture
transformer JavelusTransformers
```

## Invoking DSU


```
cd tutorial
../javelus/build/<path-to-your-javelus> -cp old/ -Dorg.javelus.dynamicPath=javelus.dsu Main
```

