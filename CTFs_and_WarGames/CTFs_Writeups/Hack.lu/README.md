# The Peace Pipe at Hack.lu's Final CTF 2014


## Understanding the Problem

The problem starts with this weird story:

    After a long day, you sit around a campfire in the wild wild web with a few Sioux you met today.
    To celebrate friendship one of them takes out his wooden peace pipe and minutes later everyone seems to be pretty dizzy.
    You remember that their war chief "Makawee" started something to say about a secret tipi filled with fire-water (the good stuff). But when he noticed your interest he immediately stopped talking.
    You recall that "Makawee" spoke with "Wahkoowah" about that issue, but it ended with a fight.
    Since then Makawee wouldn't talk to Wahkoowah anymore. While they argued "Chapawee" wrote something down.
    Maybe you can exploit their dizzyness to find out the location of the tipi.

Then it gives us three *ports* in the *host*. With the first one, we  talk to **Chapawee**:

    wildwildweb.fluxfingers.net 1432

With the second, we talk to **Wankoowah**:

    wildwildweb.fluxfingers.net 1433


Finally, with the third, we talk to **Makawee**:

    wildwildweb.fluxfingers.net 1434

It was obvious that  this game was about fooling our fellow *stoned* native-Americans.

### A Dialogue with Chapawee

When we *netcat* to **Chapawee** he answers:
```sh
$  nc wildwildweb.fluxfingers.net 1432
Hi I'm Chapawee. I know the truth about the stars
Say stars for more
```

We answer *stars* and get a funny menu:

```sh
        I can tell you the truth about
        * constellation
        * namestar [starname] [key_of_truth]   Adds a public key to a user.
                                               Existing users cannot be
                                               overwritten. Input is
                                               [a-f0-9]{1,700}.
        * showstar [starname]                  Reads the public key from the
                                               database.
```

The first option *constellation*, shows a very interesting scheme:

![cyber](http://i.imgur.com/OzVjrVh.png)

Choosing the options **namestar** we are able to pick a (new) name to add a key. Picking the option **showstar** we are able to see the key for some name (for example, for Wahkoowar, Makawee, or any new name we had added before).

So, from the above scheme, we know:

1. How a **message** (t) is created with someone's public key, a **random rational number** (r_w), and a given **modulo number** (p). The only unknown here is r_w, which is a rational number (Q). This mean that any plans to brute force the messages wouldn't work (however, if r_w was an integer, this task could be achieved).

2. Everyone has a private key that is modulo p. We never learn anything about anyone's private keys. We just know that they could be of the order of p (which is a really large number, ~1E2048).

3. Wahkoowah and Makawee have a shared secret key. The way they share this key without knowing each other's private key is by this tricky transformation:

![cyber](http://i.imgur.com/TwxShK9.jpg)

Notice that we can move the multiplications' modulo operation to the end, due to [this propriety](http://en.wikipedia.org/wiki/Modular_arithmetic#Congruence_relation).


In conclusion, all we need to do is to convince Wahkoowah  that we are Makawee (by telling him we are Makawee, so he can use his public key, and by sending him a correct *t_m*). If this works, he will give us a token. Then, if we send this token to Makawee, we get our flag.



### A Dialogue with Wankoowah

Now, let's see what Wankoowah has to say:

```sh
$ nc wildwildweb.fluxfingers.net 1433
Hi, I'm Wahkoowah. Who are you? Too foggy...
```

We try a couple of possibilities to check the outputs:
```sh
$ nc wildwildweb.fluxfingers.net 1433
Hi, I'm Wahkoowah. Who are you? Too foggy...
noone
Hi noone
Cannot find it...
Ncat: Broken pipe.

$ nc wildwildweb.fluxfingers.net 1433
Hi, I'm Wahkoowah. Who are you? Too foggy...
makawee
Oh its you, Im so sorry. Can we talk now?
This is your key of truth
50e7e1957c1786a9442f0c9f372ec19f74f52839e9e38849b47438153f9d2483213a43ad2d988fab4a8707922060aaefe6504a70637596fbcf9d58362b23e5d5e2177fd4e919b80437bab51eda931e065b6d66fce343d7cb2b7c1ca26214792d461895095ae58354af0dec6e63869007e23835892f26aabc96fe3d9084a829b4d6c5b92c6f3e0dd9a70cbd5c72d6434f2b94d21c3b0c58a288c140642b813ffb1b632bc358b3a6af0124902acd8792202c848de7f9d5d98bee51ca69040c8a2457ad3fa6276d6510701b9a875df612e035322cad06579a0a11f5e7cb4ebb7b69171c38585fc0f4fe07b0c889442397029d05dc801026a0648d7aa8c847420e9c
With magic I did this:
922a7f4b150eb83eab929e2a44bcbbb45435851262a6e7b84d2777d995ffbc315a2e57a580f4982797b45efde6d30b493880ecea33fe26e6c8ff636b75b7cb3f647f0c6f606249bc48ef09bd20738cf472bf47c7f52b9e11afcefc1548155637b0d2054d37cd74301e534208408074938ae4e7b54ef50fa0a39cb090dd34de7a4040024ba2394bac62262ccda529d2d69effe24338f0ec1b842539d2b89b081fa77a266a7c9f62c25d2a1ee1af3da8054d79d87ae88da61b8333e1fc195d2957341458700a3be70c98e1a8ab35bfe527ff6a2f255c66d753d03c59404993f1ed295a722bf1d0241eec9c01efe06e3cd5b845e84de3d29de17f9b68351bdc2d65
We continue our conversation, right?


```

The *magic* is the message *t_w*, created with Makawee's public key. Wahkoowah then ask for *t_m*...


### A Dialogue with Makawee

Let's see what Makawee has to say:

```sh
$ nc wildwildweb.fluxfingers.net 1434
Hi, I'm, Makawee, and you are? Too bright here...
noone
noone ... do I know you?
Cannot find it...

Ncat: Broken pipe.

$ nc wildwildweb.fluxfingers.net 1434
Hi, I'm, Makawee, and you are? Too bright here...
wahkoowah
I dont talk to you anymore. That thing with my daughter...

Ncat: Broken pipe.
```

Mmmm, we need to make Makawee use Wankoowah's key without him knowing it!

Since Chapawee allows us to add keys to names, let's create some name with Wahkoowah's key (say "mrwhite") and send this to Makawee:

```sh
$ nc wildwildweb.fluxfingers.net 1432
Hi I'm Chapawee. I know the truth about the stars
Say stars for more
stars

        I can tell you the truth about
        * stars
        * constellation
        * namestar [starname] [key_of_truth]   Adds a public key to a user.
                                               Existing users cannot be
                                               overwritten. Input is
                                               [a-f0-9]{1,700}.
        * showstar [starname]                  Reads the public key from the
                                               database.

namestar mrwhite 218b783ec5676cbddd378ceb724820444599f22cdcfda0a5a195b3a8fbf4ab5c915703420ad3b84531c54b838b23858fb84fcaf04d4932d4b9ef861c7ae9b635c9d3f56dfb100aa47297afcd94df41efa9f5ecba6483c5328e43ec457027ee4efcecefa094a83945106d7da1878c1f47516c2f2578170eeb36955d8bd16e0d106f9e2effe9debff41e551db4ac2e87bc8a9378d8eadb042bee18f4ad72ab721833a27154a7318b8cbe6f98fb3c82da32d1688fdcdb718fb15d9d5e6276b037cef62d953c09b23ebe90d0b13f61cd1643e5e1b0a433d5e2522ec5a028817891b6df444e983e1e0ff2356044fea67c616dce6b4bd53b17ea8bc51ef816ab8f2d9e
Add the star to the sky...
Set the star for mrwhite: 218b783ec5676cbddd378ceb724820444599f22cdcfda0a5a195b3a8fbf4ab5c915703420ad3b84531c54b838b23858fb84fcaf04d4932d4b9ef861c7ae9b635c9d3f56dfb100aa47297afcd94df41efa9f5ecba6483c5328e43ec457027ee4efcecefa094a83945106d7da1878c1f47516c2f2578170eeb36955d8bd16e0d106f9e2effe9debff41e551db4ac2e87bc8a9378d8eadb042bee18f4ad72ab721833a27154a7318b8cbe6f98fb3c82da32d1688fdcdb718fb15d9d5e6276b037cef62d953c09b23ebe90d0b13f61cd1643e5e1b0a433d5e2522ec5a028817891b6df444e983e1e0ff2356044fea67c616dce6b4bd53b17ea8bc51ef816ab8f2d9e
```

Sending it to Makawee:
```sh
$ nc wildwildweb.fluxfingers.net 1434
Hi, I'm, Makawee, and you are? Too bright here...
mrwhite
mrwhite ... do I know you?
Disguise does not help
```

Oh no, the plan did not work! We can't send **exactly** Wahkoowah's key! We need to be even more tricky...


## Crafting a Solution

### Master in Disguising

Every key in this problem is given by *mudulus p*. This means that we have infinite values that map to the same original key. My first attempt was to multiply the original key by p, so that, when it receives the modulo operation, it circles once more returning to the original value.

It didn't work. The reason is that p is too large. When multiplied by the key (that is large itself) we loose precision and we don't go back to the original value. We need to keep the values in the same scale!

Let's take a look again at the way the messages are generated:

![cyber](http://i.imgur.com/Hz5uf7X.jpg)

We notice that the public key is exponentiated by r_m. It means that, if r_m is an even number, two values of the public key are mapped to the same value of the final message: +pubk and -pubk.

That's all we need! We are going to disguise Makawee by creating a *star* with the negative value of Wahkoowah's key.


### Automatizing the Process and getting the Flag!


All right, now we know how to make Wahkoowah and Makawee talk and how to get *t_m* and *t_w*. We are ready to generate the token that will lead us to the flag.

Notice again that since these messages are generated with random numbers, they will differ each time. However, we know from above that they carry unique information that leads to a common key (and the flag). I wrote the following script to automatize the process:

```python
import socket

PORTm = 1434
PORTw = 1433
HOST = 'wildwildweb.fluxfingers.net'

def peace_pipe():

    """ Get the magic message from some user to calculate rm """
    # create sockets
    sm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to w
    sw.connect((HOST, PORTw))
    sw.recv(4096)
    sw.send(b'makawee')
    sw.recv(4096)
    sec = sw.recv(4096)
    tw = sec.split("did this:")[1].split("\n")[1].strip()
    print "\nMagic from w to m: " + tw

    # connect to m
    sm.connect((HOST, PORTm))
    sm.recv(4096)
    sm.send(b'mrblack')
    sm.recv(4096)
    sec = sm.recv(4096)
    tm = sec.split("did this:")[1].split("\n")[1].strip()
    print "\nMagic from m to w: " + tm

    # send w's magic to m's
    sm.send(tw)
    print sm.recv(4096)

    # send m's magic to get the token
    sw.send(tm)
    token = sw.recv(4096)
    token = token.split('\n')[1].strip()
    print "Token is: " + token

    # finally, send token back to m
    sm.send(token)
    print sm.recv(4096)

    sm.close()
    sw.close()

if __name__ == "__main__":
    peace_pipe()
```


Running it leads us to the flag:
```sh
python 300_peace_pipe.py

Magic from w to m: 2f2f5d280871947836e9b5665986c1b75e732d88ae3d464b65d24ea7e41c33c491060379ac4f3dc4a7231f43d6a11b5bfd3a780d8ac46bd1a4cfd99ac041434cb82c5941f17e68a4f180101ece166a1b4da6ea32d62455bd7472892ed9b67fe2122e0b331048e4a11d98422f04ec3063a3652a0e1a90e13a740905bb3a22c9b5e39d1e0fa97f10bff34d76243b9211afd1131b0f6e33d4d99c8069c462677ce67401214c943fee13252060aa02b8b1525ed0af8c9aa5ad5dee64dbb0c275dd6147754c7dfaf3218caf35d7837925215a04bb315e91441306ef0d29f0da733b7e4ac92b500dc522de11c5f5af58248ed5f762b854f40f0adf4b681a937d17a1c0

Magic from m to w: e9eedf64931d5f77f5d061a0f411f9d385144f33fe1419905fdb24a0537cc205a7f99e083f37f98af8553795f1a71f83b7924620790845c3a48bb71a9b70a0f9e5ab95dda40ec4e229bc6a6cd146779de74b7237e42d01e2538c093407165afc79776bbd9bcdefa1d9af27a39f17610b4b9060c2b0ca5203457061facdc68257433253366937cef469261492ac81c177f42f10beea386ddfa09069a5fa2ae2e39a41eeecebdba622b79231cd5f206d0a70c71aa3eb5f706a16c99173f79f97e7f3408b544df556e3779f6d49441c04d33438b9604392f90bca6c2a8c3181b12ec5d492ef2184b9db69fdd1b6247150e3b55f8ee65d113c5350b4b097abadddc9
Bit more truth is missing

Token is: 5QAWhcwSaQicM8LitDGz6To69sBtsO8ASL27zxql8hW8aziveW0B0epJz2PKIFo/K4A=
I knew you are able to see IT. Lets get drunk, I tell you where
flag{FreeBoozeForEverone-Party!}
```
