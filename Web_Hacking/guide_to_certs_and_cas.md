# On CRLs, OCSP, and a Short Review of Why Revocation Checking Doesn't Work (for Browsers)

A guide about regulation details of **SSL/TLS connections**. These connections rely on a chain of trust. This chain of trust is established by **certificate authorities** (CAs), which serve as trust anchors to verify the validity of who a device thinks it is talking to. In technical terms, **X.509** is an [ITU-T](http://en.wikipedia.org/wiki/ITU-T) standard that specifies standard formats for things such as *public key certificates* and *certificate revocation lists*.

A **public key certificate** is how websites bind their identity to a *public key* to allow an encrypted session (SSL/TLS) with the user. The certificate includes information about the key, the owner's *identity* (such as the DNS name), and the *digital signature* of the entity that issued the certificate (the [Certificate Authority](http://en.wikipedia.org/wiki/Certificate_authority), also known as CA).  As a consequence, browsers and other [user-agents](http://en.wikipedia.org/wiki/User_agent) should always be able to check the authenticity of these certificates before proceeding.

Some organizations need SSL/TLS simply for confidentiality (encryption), while other organizations use it to enhance trust in their security and identity. Therefore, CAs issue different certificates with different levels of verification, ranging from just confirming the control of the domain name (*Domain Validation*, DV) to more extensive identity checks (*Extended Validation*, EV). For instance, if a site's DNS gets hijacked, while the attacker could be able to issue a controlled DV, she wouldn't be able to issue new EV certificates just with domain validation.

Since EV and DV certificates can be valid for years, they might lose their validity before they expire by age.  For instance, the website can lose control of its key or, as recently in the event of the [Heartbleed bug](http://heartbleed.com/), a very large number of SSL/TLS websites needed to revoke and reissue their certificates. Therefore, the need for efficient revocation machinery is evident.

For many years,  two ways of revoking a certificate have prevailed:

* by checking a  **Certificate Revocation Lists** (CRLs), which are lists of serial numbers of certificates that have been revoked, provided by *each CA*. As one can imagine, they can become quite large.

* by a communication protocol named **Online Certificate Status Protocol** (OCSP), which allows a system to check with a CA for the status of a single certificate without pulling the entire CRL.


While CRLs are long lists and OCSP only deals with a single certificate, they are both methods of getting signed statements about the status of a certificate; and they both present issues concerning privacy, integrity, and availability. In this post, I discuss some of these issues and I review possible alternatives.



----
## Broken Models



### Certificate Revocation Lists (CRLs)


A CRL is a list of  serial numbers (such as ```54:99:05:bd:ca:2a:ad:e3:82:21:95:d6:aa:ee:b6:5a```) of unexpired security certificates which have been revoked by their issuer and should not be trusted.

Each CA maintains and publishes its own CRL. CRLs are in continuous changes: old certificates expire due to their age and serial numbers of newly revoked certificates are added.

The main issue here is that the original *public key infrastructure* (PKI) scheme does not scale. Users all over the Internet are constantly checking for revocation and having to download files that can be many MB.  In addition, although CRL can be cached, they are still very volatile, turning CAs into a major performance bottleneck on the Internet.



### Online Certificate Status Protocol (OCSP)

[OCSP was intended to replace the CRL system](https://tools.ietf.org/html/rfc2560), however, it presented several issues:

* *Reliability*: Every time any user connects to any secured website, her browser must query the CA's OCSP server. The typical CA issues certificates for hundreds of thousands of individual websites and the checks can be up to seconds.  Also, the CA's OCSP server might experience downtime! If a server is offline, overloaded, under attack, or unable to reply for any reason, certificate validity cannot be confirmed.

* *Privacy*: CAs can learn the IP address of users and which websites they wish to securely visit.

* *Security*: Browsers cannot be sure that a CA's server is reachable (*e.g.*, captive portals that require one to sign in on an HTTPS site, but blocks traffic to all other sites, including CA's OCSP servers).


One attempt to circumvent the lack of assurance of a server's reliability was issuing OCSP checks with a **soft-fail** option. In this case, online revocation checks which result in a *network error would be ignored*.

This brings serious issues. A simple example is when an [attacker can intercept HTTPS traffic and make online revocation checks appear to fail, bypassing OCSP checks](http://www.thoughtcrime.org/papers/ocsp-attack.pdf).

On the flip side, it's also not a good idea to enforce a **hard-fail** check:  OCSP servers are pretty flaky/slow and you do not want to rely on their capabilities (DDoS attackers would love this though).



----
## Some Light in a Solution

There are several attempts of a solution for the revocation problem but none of them has been regarded as the definitive one. Here some of them:

### CRLSets


Google Chrome uses [**CRLSets**](https://dev.chromium.org/Home/chromium-security/crlsets) in its update mechanism to send lists of serial numbers of revoked certificates which are constantly added by crawling the CAs.

This method brings more performance and reliability to the browser and, in addition, [CRLSet updates occur at least daily](https://www.imperialviolet.org/2014/04/19/revchecking.html), which is faster than most OCSP validity periods.

A complementary initiative from Google is the  [Certificate Transparency](http://www.certificate-transparency.org/what-is-ct) project. The objective is to help with structural flaws in the SSL certificate system such as domain validation, end-to-end encryption, and the chains of trust set up by CAs.




### OCSP stapling


**OCSP Stapling** ([TLS Certificate Status Request extension](http://tools.ietf.org/html/draft-hallambaker-tlssecuritypolicy-03)) is an alternative approach for checking the revocation status of certificates. It allows the presenter of a certificate to bear the resource cost involved in providing OCSP responses, instead of the CA, in a fashion reminiscent of the [Kerberos Ticket](http://en.wikipedia.org/wiki/Kerberos_(protocol)).

In a simple example, the certificate holder is the one who periodically queries the OCSP server, obtaining a *signed time-stamped OCSP response*. When users attempt to connect to the website, the response is signed with the SSL/TLS handshake via the Certificate Status Request extension response. Since the stapled response is signed by the CA, it cannot be forged (without the CA's signing key).

If the stapled OCSP has the [Must Staple](http://tools.ietf.org/html/draft-hallambaker-muststaple-00) capability, it becomes hard-fail if a valid OCSP response is not stapled. To make a browser know this option, one can add a "must staple" assertion to the site's security certificate and/or create a new HTTP response header similar to [HSTS](http://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security).

Some fixable issue is that OCSP stapling supports only one response at a time. This is insufficient for sites that use several different certificates for a single page. Nevertheless, OCSP stapling is the most promising solution for the problem for now. The idea has been implemented by the servers for years, and recently, a [few browsers are adopting it](https://blog.mozilla.org/security/2013/07/29/ocsp-stapling-in-firefox/). If this solution is going to become mainstream, only time will show.


-----

**tl;dr:** The security of the Internet depends on the agent's ability to revoke compromised certificates, but the status quo is broken. There is a urgent need for rethinking the way things have been done!

-----

**Edited, 11/19/2014:** The **EFF** just announced an attempt to help the CA  problem:  [Let's Encrypt](https://www.eff.org/deeplinks/2014/11/certificate-authority-encrypt-entire-web), "a new certificate authority (CA) initiative that aims to clear the remaining roadblocks to transition the Web from HTTP to HTTPS". The initiative is planned to be released in 2015. These are good news, but it is still not clear whether they are going to address the revocation problem with new solutions.




----

### References:

[Imperial Violet: Revocation Doesn't work](https://www.imperialviolet.org/2011/03/18/revocation.html)

[Imperial Violet: Don't Enable Revocation Checking](https://www.imperialviolet.org/2014/04/19/revchecking.html)

[Imperial Violet: Revocation Still Doesn't Work](https://www.imperialviolet.org/2014/04/29/revocationagain.html)

[Proxy server for testing revocation](https://gist.github.com/agl/876829)

[Revocation checking and Chrome's CRL](https://www.imperialviolet.org/2012/02/05/crlsets.html)

[Discussion about OCSP checking at Chrome](https://code.google.com/p/chromium/issues/detail?id=361820)

[RFC Transport Layer Security (TLS) Channel IDs](http://tools.ietf.org/html/draft-balfanz-tls-channelid-00)

[Fixing Revocation for Web Browsers, iSEC Partners](https://www.isecpartners.com/media/17919/revocation-whitepaper_pdf__2_.pdf)

[Proposal for Better Revocation Model of SSL Certificates](https://wiki.mozilla.org/images/e/e3/SSLcertRevocation.pdf)



[SSL Server Test](https://www.ssllabs.com/ssltest/)

[SSL Certificate Checker](https://www.digicert.com/help/)
