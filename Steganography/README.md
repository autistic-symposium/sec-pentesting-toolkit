# Steganography



## Images

- Adding two images
- xor_bytes
- color crypto

![](http://i.imgur.com/5IBxKbF.png)

___

## Command Line:

- Pull out the audio with ffmpeg:

```
$ ffmpeg -i windows.mp4 windows.wav
```


- Make a gif from video using [ffmpeg](https://www.ffmpeg.org/download.html)

```sh
$ ffmpeg -i windows.mp4 windows.gif
```

- Online tool for images: 
	* [utilitymill](http://utilitymill.com/utility/Steganography_Decode)
	* [pngcheck](http://www.libpng.org/pub/png/apps/pngcheck.html)
	* [Paranoid.jar](https://ccrma.stanford.edu/~eberdahl/Projects/Paranoia/)


____

### Metadata


[Image metadata](http://regex.info/exif.cgi)

- To find information inside a picture, we can use package [pnginfo] or [pngcheck].

- If we need [base64 decoding] (for example a PGP key with a picture).

- Weird pieces of bytes may need to be XORed.

- If we have a decrypted message and a key:
    1. Import the private key to use it to decrypt the message with ```gpg --allow-secret-key-import --import private.key```
    2. Decrypt with ```gpg --decrypt message.pgp```.

- [ExifTool](http://www.sno.phy.queensu.ca/~phil/exiftool/index.html)


---

## Other Tools

- OpenStego
- OutGuess
- Gimp
- Audacity
- MP3Stego
- ffmpeg
- pngcheck
- StegFS
- Steghide




[Bacon's cipher]:http://en.wikipedia.org/wiki/Bacon's_ciphe
[Carpenter's Formula]:http://security.cs.pub.ro/hexcellents/wiki/writeups/asis_rsang
[pngcheck]: http://www.libpng.org/pub/png/apps/pngcheck.html
[karmadecay]: http://karmadecay.com/
[tineye]:  https://www.tineye.com/
[images.google.com]: https://images.google.com/?gws_rd=ssl
[base64 decoding]: http://www.motobit.com/util/base64-decoder-encoder.asp
[subbrute.py]: https://github.com/SparkleHearts/subbrute
[pnginfo]: http://www.stillhq.com/pngtools/
[namechk]: http://namechk.com

