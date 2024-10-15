# Intro to OpenPGP & GPG

[Pretty Good Privacy](http://en.wikipedia.org/wiki/Pretty_Good_Privacy) (PGP) is a model that provides cryptographic privacy and authentication for data communication. It was created by [Phil Zimmermann](http://en.wikipedia.org/wiki/Phil_Zimmermann) in 1991. Today, PGP is a [company](http://en.wikipedia.org/wiki/PGP_Corporation) that sells a proprietary encryption program, [OpenPGP](http://www.openpgp.org/) is the open protocol that defines how PGP encryption works, and [GnuGP](https://www.gnupg.org/) is the free software.


The distribution of PGP keys can be done using the concept of [web of trust](http://en.wikipedia.org/wiki/Web_of_trust). It is a decentralized way of establishing the authenticity of a public key and its owner. If you want a cute (ludic) picture of the web of trust, check [Cory Doctorow](https://twitter.com/doctorow)'s book [Little Brother](http://craphound.com/littlebrother/).


Almost 15 years after its creation, [PGP continues to be *pretty good*](https://firstlook.org/theintercept/2014/10/28/smuggling-snowden-secrets/). But there is still a [need for new solutions](http://blog.cryptographyengineering.com/2014/08/whats-matter-with-pgp.html) (and they appear to be [coming soon](http://googleonlinesecurity.blogspot.com/2014/06/making-end-to-end-encryption-easier-to.html)). Perhaps the main issue with PGP is its persistence. If one key is compromised, any message from the past can be read. That's where the concept of [perfect forward secrecy ](http://en.wikipedia.org/wiki/Forward_secrecy) comes in play, but this is a subject to another post. 

Meanwhile, I wrote this tutorial, and I hope you find it fun. Btw, [this post was first published at CodeWall and it had 1.5k+ views at the time](https://coderwall.com/p/ajtlqa/getting-started-with-pgp-gpg).






### I. Creating GPG keys

Type the following in the terminal:

```sh
$ gpg --gen-key
```

Chose [RSA](http://en.wikipedia.org/wiki/RSA_(cryptosystem)) with 4096 bits long and expiration up to 5 years. Use a [strong passphrase](https://www.eff.org/wp/defending-privacy-us-border-guide-travelers-carrying-digital-devices#passphrase) (keep it safe since it cannot be recovered).

### II. Backup your Private Key

Save it with your soul:

```sh
$ gpg --export-secret-keys --armor YOUR_EMAIL > YOUR_NAME-privkey.asc
```

### III. Sharing your key

There are several ways you can share or publish your public key:

#### By sharing the key's fingerprint

The key's fingerprint is the same as its signature. Each PGP key has a unique fingerprint that allows you to confirm to others that they have received your actual public key without tampering. A fingerprint is a more convenient way to represent a key uniquely.

To check the fingerprint of any key that you have in your keyring, type:

```sh
$ gpg --fingerprint EMAIL
```

#### By sending the ASCII file
You can copy your key to a file to be shared:
```sh
$ gpg --export --armor YOUR_EMAIL > YOUR_NAME-pubkey.asc
```

#### By publishing it in a public key server
You can export your key to the [GnuPG public key server](keys.gnupg.net). For this, use your key's name (the hexadecimal number in front of the key):

```sh
$ gpg --send-key KEY_NAME
```

You can also export it to [pgp.mit.edu](pgp.mit.edu):

```sh
$ gpg --keyserver hkp://pgp.mit.edu --send-key KEY_NAME
```

### V. Importing Someone's Key

There are many ways you can import someone's public key:

#### By a shared file
If you have the ASCII file, you can type:

```sh
$ gpg --import PUBKEY_FILE
```


#### By Public Key Server
To search for someone's key in the public key server, type:

```sh
$ gpg --search-keys NAME
```

Note: this is **not** very safe since you can't be sure of the key's authenticity.

### V. Signing a key: The Web of Trust

Signing a key tells your software that you trust the key that you have been provided (you have verified that it is associated with the person in question).

To sign a key type:

```sh
$ gpg --sign-key PERSON_EMAIL
```

You should allow the person whose key you are signing to enjoy the advantages of your trusted relationship, done by sending her back the signed key:

```sh
$ gpg --export --armor PERSON_EMAIL
```

When you received a similar *trusted* key, you can import it into your GPG database:

```sh
$ gpg --import FILENAME
```

### VI. Other Useful Commands

#### To delete a key from your keyring:
```sh
$ gpg --delete-key-name KEY_NAME
```

#### To edit a key (for example, the expiration date):

```sh
$ gpg --edit KEY_NAME
```



#### If you have more than one key:

Edit ```~/.gnupg/gpg.conf``` with your favorite key:

```
default-key KEY_NAME
```

#### Keep your keys fresh:

```sh
$ gpg --refresh-keys
```



#### To list your keys:

```sh
$ gpg --list-keys
```

#### And of course:
```sh
$ man gpg
```


### VII. Encrypting and Decrypting Messages


With someone's **public key**, you can **encrypt** messages that can only be decrypted with her secret key. You can also **verify signatures** that was generated with her secret key.

On the other hand, with your secret key, you can **decrypt** messages that were encrypted using your public key. You can also and **sign messages**.

With GPG, you encrypt messages using the ```--encrypt``` flag.

The command below encrypts the message signing with your private key (to guarantee that is coming from you). It also generates the message in a text format, instead of raw bytes:

```sh
$ gpg --encrypt --sign --armor -r PERSON_EMAIL FILE_TO_BE_ENCRYPTED
```

If you want to be able to read this message with your own email address, you should add another recipient flag ```-r``` with your email address.

To decrypt a message, type:

```sh
$ gpg FILENAME
```


### VIII. Revoking a key

Whenever you need to revoke a key (because it might be compromised, for example), you can generate a revocation certificate with:

```sh
$ gpg --output my_revocation.asc --gen-revoke KEY_NAME
```

To import the revocation into your keyring:

```sh
$ gpg --import my_revocation.asc
```

Finally, this command sends the revoked key to the public key server:

```sh
$ gpg --keyserver pgp.mit.edu --send-keys KEY_NAME
```



----


## Final Comments

If you prefer a GUI instead of the command line, I strongly recommend [seahorse](https://apps.fedoraproject.org/packages/seahorse/bugs). It makes it really easy to manage all your keys (not only OpenPGP) and passwords.

Another nice (alpha) project is [keybase.io](https://keybase.io/). It's a web of trust social network, where you can sign your key with your public profiles. Check [mine here](https://keybase.io/bt3). Encryption and decryption can be done in the command line with their [node.js](https://keybase.io/docs/command_line) application. I don't trust uploading my private key anywhere, but I do think that the idea is better than a simple public key server.



Finally, a word about browser plugins: although there are several of them to encrypt webmail with OpenPGP, such as [mymail-crypt](https://chrome.google.com/webstore/detail/mymail-crypt-for-gmail/jcaobjhdnlpmopmjhijplpjhlplfkhba?hl=en-US) or [Mailvelope](https://www.mailvelope.com/), I particularly don't recommend this solution if your message is very sensitive.

If you are serious about ensuring your long-term privacy, the safest way to go is to use a text editor to write your email message, encrypting the message outside of the web browser, and then cutting and pasting into your webmail interface. This will guarantee that only the recipient will be able to read your email.

If you really need something in your browser, the creator of [Cryptocat](https://crypto.cat/) recently released [minilock](https://minilock.io/). This tool uses [Curve25519 elliptic curve cryptography](http://en.wikipedia.org/wiki/Curve25519) (the same as in Cryptocat) so that the public keys are much shorter (and easier to share). Remember, it's a new app, so it might not yet be the best choice for the high-stakes environment (but it's worth keeping tabs on this project).

---

## Further Readings

- [The GNU Privacy Handbook](https://www.gnupg.org/gph/en/manual.html)
