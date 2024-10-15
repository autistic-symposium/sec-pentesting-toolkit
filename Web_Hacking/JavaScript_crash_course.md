# JavaScript: Crash Course


# Installing & Setting up

JavaScript (JS) is a dynamic computer programming language. Install [Google Dev Tools](https://developer.chrome.com/devtools/index) to proceed. 

# JavaScript 101

To include your example.js in an HTML page (usually placed right before </body> will guarantee that elements are defined when the script is executed):

```
<script src="/path/to/example.js"></script>
```

Variables can be defined using multiple var statements or in a single combined var statement. The value of a variable declared without a value is undefined.

## Types in JavaScript

### Primitive:

    - String
    - Number
    - Boolean
    - null (represent the absence of a value, similar to many other programming languages)
    - undefined (represent a state in which no value has been assigned at all)

### Objects:

```
// Creating an object with the constructor:
var person1 = new Object;

person1.firstName = "John";
person1.lastName = "Doe";

alert( person1.firstName + " " + person1.lastName );
// Creating an object with the object literal syntax:
var person2 = {
    firstName: "Jane",
    lastName: "Doe"
};

alert( person2.firstName + " " + person2.lastName );
Array

// Creating an array with the constructor:
var foo = new Array;
// Creating an array with the array literal syntax:
var bar = [];
If/Else

var foo = true;
var bar = false;

if ( bar ) {
    // This code will never run.
    console.log( "hello!" );
}

if ( bar ) {

    // This code won't run.

} else {

    if ( foo ) {
        // This code will run.
    } else {
        // This code would run if foo and bar were both false.
    }

}
```

### Flow Control

#### switch

```
switch ( foo ) {

    case "bar":
        alert( "the value was bar -- yay!" );
        break;

    case "baz":
        alert( "boo baz :(" );
        break;

    default:
        alert( "everything else is just ok" );

}
```

#### for

```
for ( var i = 0; i < 5; i++ ) {
    // Logs "try 0", "try 1", ..., "try 4".
    console.log( "try " + i );
}
```

#### while

```
var i = 0;
while ( i < 100 ) {
    // This block will be executed 100 times.
    console.log( "Currently at " + i );
    i++; // Increment i
}
or

var i = -1;
while ( ++i < 100 ) {
    // This block will be executed 100 times.
    console.log( "Currently at " + i );
}
```


#### do-while

```
do {
    // Even though the condition evaluates to false
    // this loop's body will still execute once.
    alert( "Hi there!" );

} while ( false );
```

### Ternary Operator

```
// Set foo to 1 if bar is true; otherwise, set foo to 0:
var foo = bar ? 1 : 0;
```

### Arrays

```
.length

var myArray = [ "hello", "world", "!" ];

for ( var i = 0; i < myArray.length; i = i + 1 ) {

    console.log( myArray[ i ] );

}
.concat()

var myArray = [ 2, 3, 4 ];
var myOtherArray = [ 5, 6, 7 ];
var wholeArray = myArray.concat( myOtherArray );
.join()

 // Joining elements

var myArray = [ "hello", "world", "!" ];

// The default separator is a comma.
console.log( myArray.join() );     // "hello,world,!"

// Any string can be used as separator...
console.log( myArray.join( " " ) );  // "hello world !";
console.log( myArray.join( "!!" ) ); // "hello!!world!!!";

// ...including an empty one.
console.log( myArray.join( "" ) );
.pop() and .push()
```

#### Remove or add last element

Extracts a part of the array and returns that part in a new array. This method takes one parameter, which is the starting index:
```
.reverse()

var myArray = [ "world" , "hello" ];
myArray.reverse(); // [ "hello", "world" ]
.shift()

var myArray = [];

myArray.push( 0 ); // [ 0 ]
myArray.push( 2 ); // [ 0 , 2 ]
myArray.push( 7 ); // [ 0 , 2 , 7 ]
myArray.shift();   // [ 2 , 7 ]
.slice()
```


#### Remove a certain amount of elements

Abd adds new ones at the given index. It takes at least three parameters:

* Index – The starting index.
* Length – The number of elements to remove.
* Values – The values to be inserted at the index position.

```
var myArray = [ 0, 7, 8, 5 ];
myArray.splice( 1, 2, 1, 2, 3, 4 );
console.log( myArray ); // [ 0, 1, 2, 3, 4, 5 ]
.sort()
```

#### Sorts an array

It takes one parameter, which is a comparing function. If this function is not given, the array is sorted ascending:
```
// Sorting with comparing function.

function descending( a, b ) {
    return b - a;
}

var myArray = [ 3, 4, 6, 1 ];

myArray.sort( descending ); // [ 6, 4, 3, 1 ]
.unshift()
```

#### Inserts an element at the first position of the array

```
.forEach()
function printElement( elem ) {
    console.log( elem );
}

function printElementAndIndex( elem, index ) {
    console.log( "Index " + index + ": " + elem );
}

function negateElement( elem, index, array ) {
    array[ index ] = -elem;
}

myArray = [ 1, 2, 3, 4, 5 ];

// Prints all elements to the consolez
myArray.forEach( printElement );

// Prints "Index 0: 1", "Index 1: 2", "Index 2: 3", ...
myArray.forEach( printElementAndIndex );

// myArray is now [ -1, -2, -3, -4, -5 ]
myArray.forEach( negateElement );

```


### Strings


Strings are a primitive and an object in JavaScript.

Some methods:

* length
* charAt()
* indexOf()
* substring()
* split()
* toLowerCase
* replace
* slice
* lastIndexOf
* concat
* trim
* toUpperCase


### Objects

Nearly everything in JavaScript is an object – arrays, functions, numbers, even strings - and they all have properties and methods.

```
var myObject = {
    sayHello: function() {
        console.log( "hello" );
    },
    myName: "Rebecca"
};

myObject.sayHello(); // "hello"

console.log( myObject.myName ); // "Rebecca"
The key can be any valid identifier:

var myObject = {
    validIdentifier: 123,
    "some string": 456,
    99999: 789
};
```

### Functions

Can be created in many ways:

```
// Named function expression.
var foo = function() {     ----> function expression (load later)
    // Do something.
};

function foo() {        ----> function declaration (load first)
    // Do something.
}
If you declare a local variable and forget to use the var keyword, that variable is automatically made global.

Immediately -Invoked Function Expression:

(function() {
    var foo = "Hello world";
})();
console.log( foo ); // undefined!
```

### Events

JavaScript lets you execute code when events are detected.

Example of code to change a source image:

```
windows.onload = init;
function init(){
    var img = docuemnt.GetEventById("example");
    img.src = "example.jpg"
```

Methods for events:

* click
* resize
* play
* pause
* load
* unload
* dragstart
* drop
* mousemove
* mousedown
* keypress
* mouseout
* touchstart
* touchend


### Closure

Closure is one of the main proprieties of JavaScript.

Example of closure for a counter. Normally we would have the code:

```
 var count = 0;
 function counter(){
     count += 1;
     return count
}
console.log(counter());     --> print 1
console.log(counter());     --> print 2
```

However, in JS we can enclose our counter inside an environment. This is useful for large codes, with multiple collaborations, for example, where we might use count variables more than once:
```
function makeCounter(){
    var count = 0;
    function counter(){
      count += 1;
      return count;
    }
    return counter;   ----> closure holds count!
}
```

### Prototypes
```
function dog(name, color){
    this.name = name;
    this.color = color;
}

dog.prototype.species = "canine"
dog.prototype.bark = function{
}
```

### jQuery

Type Checking with jQuery:

```
// Checking the type of an arbitrary value.

var myValue = [ 1, 2, 3 ];

// Using JavaScript's typeof operator to test for primitive types:
typeof myValue === "string"; // false
typeof myValue === "number"; // false
typeof myValue === "undefined"; // false
typeof myValue === "boolean"; // false

// Using strict equality operator to check for null:
myValue === null; // false

// Using jQuery's methods to check for non-primitive types:
jQuery.isFunction( myValue ); // false
jQuery.isPlainObject( myValue ); // false
jQuery.isArray( myValue ); // true
```

---
Enjoy! This article was originally posted [here](https://coderwall.com/p/skucrq/javascript-crash-course).