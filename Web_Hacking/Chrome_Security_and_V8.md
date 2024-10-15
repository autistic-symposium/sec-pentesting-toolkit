# A Closer Look at Chrome's Security: Understanding V8

[In 2008, Google released a sandbox-oriented browser](http://blogoscoped.com/google-chrome/), that was assembled from several different code libraries from Google and third parties (for instance, it borrowed a rendering machinery from the open-source [Webkit layout engine](https://www.webkit.org/), later changing it to a forked version, [Blink](http://en.wikipedia.org/wiki/Blink_(layout_engine))). Six years later, Chrome has become the preferred browser for [half of the users on the Internet](http://en.wikipedia.org/wiki/File:Usage_share_of_web_browsers_(Source_StatCounter).svg). In this post I investigate further how security is dealt with in this engine, and I summarize the main features of Chrome and its [Chromium Project](http://www.chromium.org/Home), describing the natural way of processing JavaScript with the **V8 JavaScript virtual machine**.



## They way computers talk...



In mainstream computer languages, a [source code in a ** high-level language** is transformed to a ** low-level language**](http://www.openbookproject.net/thinkcs/python/english2e/ch01.html) (a machine or assembly language) by either being **compiled** or **interpreted** . It is [a very simple concept](https://www.youtube.com/watch?v=_C5AHaS1mOA), but it is a fundamental one!

### Compilers and Interpreters

**Compilers** produce an intermediate form called **code object**, which is like machine code but augmented with symbols tables to make executable blocks (library files, with file objects). A linker is used to combine them to form executables finally.

**Interpreters** execute instructions without compiling into machine language first. They are first translated into a lower-level intermediate representations such as **byte code** or **abstract syntax trees** (ASTs). Then they are interpreted by a **virtual machine**.

The truth is that things are generally mixed. For example, when you type some instruction in Python's REPL, [the language executes four steps](http://akaptur.com/blog/2013/11/17/introduction-to-the-python-interpreter-3/): *lexing* (breaks the code into pieces), *parsing* (generates an AST with those pieces - it is the syntax analysis), *compiling* (converts the AST into code objects - which are attributes of the function objects), and *interpreting* (executes the code objects).

In Python, byte-compiled code, in the form of **.pyc** files, is used by the compiler to speed-up the start-up time (load time) for short programs that use a lot of standard modules. And, by the way, byte codes are attributes of the code object so to see them, you need to call ```func_code``` (code object) and ```co_code```(bytecode)[1]:

```py
>>> def some_function():
... return
...
>>> some_function.func_code.co_code
'd\x00\x00S'
```

On the other hand, traditional JavaScript code is represented as bytecode or an AST, and then executed in a *virtual machine* or further compiled into machine code. When JavaScript interprets code, it executes roughly the following steps: *parsing* and *preprocessing*, *scope analysis*, and *bytecode or translation to native*. Just a note: the JavaScript engine represents bytecode using [SpiderMonkey](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey/Internals/Bytecode).

So we see that when modern languages choose the way they compile or interpret code, they are trading off with the speed they want things to run. Since browsers are preoccupied with delivering content the faster they can, this is a fundamental concept.


### Method JITs and Tracing JITs

To speed things up, instead of having the code being parsed and then executed ([one at a time](http://en.wikipedia.org/wiki/Ahead-of-time_compilation)), **dynamic translators** (*Just-in-time* translators, or JIT) can be used. JITs *translate intermediate representation into machine language at runtime*. They have the efficiency of running native code with the cost of startup time plus increased memory (when the bytecode or AST are first compiled).

Engines have different policies on code generation, which can roughly be grouped into types: **tracing** and **method**.

**Method JITs** emit native code for every block (method) of code and update references dynamically. Method JITs can implement an *inline cache* for rewriting type lookups at runtime.

In **tracing JITs**, native code is only emitted when a certain block (method) is considered *important*. An example is given by traditional JavaScript: if you load a script with functions that are never used, they are never compiled. Additionally, in JavaScript a *cache* is usually implemented due to the nature of its *dynamic typing system*.

 As we will see below, V8 performs direct JIT compilation from (JavaScript) source code to native machine code (IA-32, x86-64, ARM, or MIPS ISAs), **without transforming it to bytecode first**. In addition, V8 performs dynamic several optimizations at runtime (including **inline caching**). But let's not get ahead of ourselves! Also, as a note, Google has implemented a technology called [**Native Client**](http://code.google.com/p/nativeclient/) (NaCl), which allows one to provide compiled code to the Chrome browser.


----
## The way JavaScript rolls...

JavaScript's integration with [Netscape Navigator](http://en.wikipedia.org/wiki/Netscape_Navigator) in the mid-90s made it easier for developers to access HTML page elements such as *forms*, *frames*, and *images*. This was essential for JavaScript's accession to become the most popular scripting engine for the web.

However, the language's high dynamical behavior (that I'm briefly discussing here) came with a price: in the mid-2000s browsers had very slow implementations that did not scale with code size or *object allocation*. Issues such as *memory leaks* when running web apps were becoming mainstream. It was clear that things would only get worse and a new JavaScript engine was a need.


### JavaScript's Structure

In JavaScript, every object has a *prototype*, and a prototype is also an object. All JavaScript objects inherit their properties and methods from their prototype.

So, for example, supposing an application that has an object *Point* (borrowed from the [official documentation](https://developers.google.com/v8/design)):

```JavaScript
function Point(x,y){
 this.x = x;
 this.y = y;
}
```
We can create several objects:

```JavaScript
var a = new Point(0,1);
var b = new Point(2,3);
```

And we can access the propriety ```x``` in these object by:
```
a.x;
b.x;
```

In the above implementation, we would have two different Point objects that do not share any structure. This is because JavaScript is **classless**: you create new objects on the fly and dynamically add or remove proprieties. Functions can move from an object to another. Objects with the same type can appear in the same sites in the program with no constraints.

Furthermore, to store their object proprieties, most JavaScript engines use a *dictionary-like data structure*. Each property access demands a dynamic lookup to resolve their location in memory. This contrasts *static* languages such as Java, where instance variables are located at fixed offsets determined by the compiler (due to the *fixed* object layout by the *object's class*). In this case, access is given by a simple memory load or store (a single instruction).

### JavaScript's Garbage Collection

 Garbage collection is a form of *automatic memory management*: an attempt to reclaim the memory occupied by objects that are not being used any longer (*i.e.*, if an object loses its reference, the object's memory has to be reclaimed).

The other possibility is *manual memory management*, which requires the developer to specify which objects need to be deallocated. However, manual garbage collection can result in bugs such as:

1. **Dangling pointers**: when a piece of memory is freed while there are still pointers to it.

2. **Double free bugs**: when the program tries to free a region of memory that it had already freed.

3. **Memory leaks**: when the program fails to free memory occupied by an object that had become unreachable, leading to memory exhaustion.


As one could guess, JavaScript has automatic memory management. Actually, the core design flaw of traditional JavaScript engines is **bad garbage collection behavior**. The problem is that JavaScript engines do not know exactly where all the pointers are, and they will search through the entire execution stack to see what data looks like pointers (for instance, integers can look like a pointer to an address in the heap).




------------
## Introducing V8

A solution for the issues presented above came from Google, with the **V8 Engine**. V8 is an [open source JavaScript engine](https://code.google.com/p/v8/) written in C++ that gave birth to Chrome. V8 has a way to categorize the highly-dynamic JavaScript objects into classes, bringing techniques from static class-based languages. In addition, as I mentioned in the beginning, V8 compiles JavaScript to native machine code before executing it.

In terms of performance, besides direct compilation to native code, three main features in V8 are fundamental:

 1. Hidden classes.

 2. In-line caching as an optimization technique.

 3. Efficient memory management system (garbage collection).

Let's take a look at each of them.

### V8's Hidden Class

In V8, as execution goes on, objects that end up with the same properties will share the same **hidden class**. This way, the engine applies dynamic optimizations.

Consider the Point example from before: we have two different objects, ```a``` and ```b```. Instead of having them completely independent, V8 makes them share a hidden class. So instead of creating two objects, we have *three*. The hidden class shows that both objects have the same proprieties, and an object changes its hidden class when a new property is added.

So, for our example, if another Point object is created:

1. Initially, the Point object has no properties, so the newly created object refers to the initial class **C0**. The value is stored at offset zero of the Point object.

2. When property ```x``` is added, V8 follows the hidden class transition from **C0** to **C1** and writes the value of ```x``` at the offset specified by **C1**.

3. When property ```y``` is added, V8 follows the hidden class transition from **C1** to **C2** and writes the value of ```y``` at the offset specified by **C2**.

Instead of having a generic lookup for propriety, V8 generates efficient machine code to search the propriety. The machine code generated for accessing ```x``` is something like this:

```
# ebx = the point object
cmp [ebx, <class offset>], <cached class>
jne <inline cache miss>
mv eax, [ebx, <cached x offset>]
```
Instead of a complicated lookup at the propriety, the propriety reading translates into three machine operations!

It might seem inefficient to create a new hidden class whenever a property is added. However, because of the class transitions, the hidden classes can be reused several times. It turns out that most of the access to objects are within the same hidden class.



### V8's Inline caching


When the engine runs the code, it does not know about the hidden class. V8 optimizes property access by predicting that the class will also be used for all future objects accessed in the same section of code, and adds the information to the **inline cache code**.

Inline caching is a class-based object-oriented optimization technique employed by some language runtimes. The concept of inline caching is based on the observation that the objects that occur at a particular call site are often of the same type. Therefore, performance can be increased by storing the result of a method lookup *inline* (at the call site).

If V8 has predicted the property's value correctly, this is assigned in a single operation. If the prediction is incorrect, V8 patches the code to remove the optimization. To facilitate the process, call sites are assigned in four different states:


1. **Unitilized**: Initial state, for any object that was never seen before.

2. **Pre-monomorphic**: Behaves like an uninitialized but do a one-time lookup and rewrite it to the monophorfic state. It's good for code executed only once (such as initialization and setup).

3. **Monomphorpic**: Very fast. Recodes the hidden class of the object already seen.

4. **Megamorphic**: Like the initialized stub (since it always does runtime lookup) except that it never replaces itself.

In conclusion, the combination of using hidden classes to access properties with inline caching (plus machine code generation) does optimize in cases where the type of objects are frequently created and accessed in a similar way. This dramatically improves the speed at which most JavaScript code can be executed.




### V8's Efficient Garbage Collecting


In V8, a **precise garbage collection** is used. *Every pointer's location is known on the execution stack*, so V8 is able to implement incremental garbage collection. V8 can migrate an object to another place and rewire the pointer.

In summary, [V8's garbage collection](https://developers.google.com/v8/design#garb_coll):

 1. stops program execution when performing a garbage collection cycle,

 2. processes only part of the object heap in most collection cycles (minimizing the impact of stopping the application),

 3. always knows exactly where all objects and pointers are in memory (avoiding falsely identifying objects as pointers).



-------------

## Further Readings:

* [Privacy And Security Settings in Chrome](https://noncombatant.org/2014/03/11/privacy-and-security-settings-in-chrome/)

[1] When the Python interpreter is invoked with the ```-O``` flag, optimized code is generated and stored in ***.pyo*** files. The optimizer removes assert statements.
